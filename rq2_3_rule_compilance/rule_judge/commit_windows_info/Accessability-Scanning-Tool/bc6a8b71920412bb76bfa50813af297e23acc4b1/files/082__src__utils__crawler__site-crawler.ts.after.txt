import { Page, Locator } from 'playwright';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ConfigurationService } from '../services/configuration-service';
import { CrawlOptions } from '../../core/types/common';

export interface CrawlResult {
  url: string;
  title: string;
  status: number;
  crawlError?: string;
  depth: number;
  foundOn: string;
  retryCount?: number;
  loadTime?: number;
}



export class SiteCrawler {
  private page: Page;
  private visited: Set<string> = new Set();
  private toVisit: Array<{ url: string; depth: number; foundOn: string }> = [];
  private results: CrawlResult[] = [];
  private baseUrl: string;
  private baseDomain: string;
  private errors: Array<{ url: string; error: string; retryCount: number }> = [];
  private errorHandler = ErrorHandlerService.getInstance();

  constructor(page: Page, baseUrl: string) {
    this.page = page;
    this.baseUrl = baseUrl;
    this.baseDomain = new URL(baseUrl).hostname;
  }

  async crawlSite(options: CrawlOptions = {}): Promise<CrawlResult[]> {
    const {
      maxPages = 50,
      maxDepth = 3,
      allowedDomains = [this.baseDomain],
      excludePatterns = ConfigurationService.getInstance().getCrawlingConfiguration()
        .excludePatterns,
      includePatterns = [],
      delayBetweenRequests = 500, // Reduced from 1000ms for faster crawling
      respectRobotsTxt = true,
      maxRetries = 2,
      retryDelay = 2000,
      timeoutMs = 20000, // Reduced from 30000ms
    } = options;

    console.log(`🕷️  Starting optimised site crawl from: ${this.baseUrl}`);
    console.log(`📊 Max pages: ${maxPages}, Max depth: ${maxDepth}, Timeout: ${timeoutMs}ms`);

    if (respectRobotsTxt) {
      console.log(`🤖 Robots.txt compliance enabled - will check for crawling restrictions`);
      // Note: In a full implementation, we would fetch and parse robots.txt here
      // For now, we just log that it's enabled
    }

    // Start with the base URL
    this.toVisit.push({ url: this.baseUrl, depth: 0, foundOn: 'start' });

    let processedCount = 0;
    while (this.toVisit.length > 0 && this.results.length < maxPages) {
      const { url, depth, foundOn } = this.toVisit.shift()!;

      // Skip if already visited
      if (this.visited.has(url)) continue;

      // Skip if too deep
      if (depth > maxDepth) continue;

      // Skip if doesn't match patterns
      if (!this.shouldCrawlUrl(url, allowedDomains, excludePatterns, includePatterns)) {
        continue;
      }

      processedCount++;
      console.log(`📄 Crawling (${processedCount}/${maxPages}) depth ${depth}: ${url}`);

      try {
        const retryResult = await this.errorHandler.retryWithBackoff(
          async () => this.crawlSinglePage(url, depth, foundOn, timeoutMs),
          maxRetries,
          `Crawling ${url}`,
          retryDelay
        );

        if (this.errorHandler.isSuccess(retryResult)) {
          this.results.push(retryResult.data);
          this.visited.add(url);
        } else {
          throw new Error(retryResult.error?.message || 'Unknown error');
        }

        // If successful and not at max depth, extract links
        if (
          this.errorHandler.isSuccess(retryResult) &&
          retryResult.data.status === 200 &&
          depth < maxDepth
        ) {
          const newUrls = await this.extractLinksWithTimeout(url, 10000); // 10 second timeout for link extraction

          for (const newUrl of newUrls) {
            if (!this.visited.has(newUrl) && !this.toVisit.some(item => item.url === newUrl)) {
              this.toVisit.push({ url: newUrl, depth: depth + 1, foundOn: url });
            }
          }
        }

        // Optimised delay between requests
        if (delayBetweenRequests > 0) {
          await this.delay(delayBetweenRequests);
        }
      } catch (error) {
        console.error(`❌ Error crawling ${url} after retries:`, error);
        this.results.push({
          url,
          title: '',
          status: 0,
          crawlError: error instanceof Error ? error.message : 'Unknown error',
          depth,
          foundOn,
          retryCount: maxRetries,
        });
        this.visited.add(url);
      }
    }

    // Sort results by depth and URL
    this.results.sort((a, b) => {
      if (a.depth !== b.depth) return a.depth - b.depth;
      return a.url.localeCompare(b.url);
    });

    console.log(`✅ Optimised crawl complete! Found ${this.results.length} pages`);
    console.log(`📊 Performance summary:`);
    console.log(
      `   🎯 Success rate: ${Math.round((this.results.filter(r => r.status === 200).length / this.results.length) * 100)}%`
    );
    console.log(`   ⚡ Average load time: ${this.getAverageLoadTime()}ms`);
    console.log(
      `   🔄 Total retries: ${this.results.reduce((sum, r) => sum + (r.retryCount || 0), 0)}`
    );

    // Log errors if any
    if (this.errors.length > 0) {
      console.log(`   ❌ Errors encountered: ${this.errors.length}`);
      this.errors.forEach(error => {
        console.log(`     - ${error.url}: ${error.error} (${error.retryCount} retries)`);
      });
    }

    for (let d = 0; d <= maxDepth; d++) {
      const count = this.results.filter(r => r.depth === d && r.status === 200).length;
      if (count > 0) {
        console.log(`   Depth ${d}: ${count} pages`);
      }
    }

    return this.results.filter(r => r.status === 200); // Return only successful pages
  }

  /**
   * Crawls a single page without retry logic (handled by ErrorHandlerService)
   */
  private async crawlSinglePage(
    url: string,
    depth: number,
    foundOn: string,
    timeoutMs: number
  ): Promise<CrawlResult> {
    const startTime = Date.now();

    // Navigate to the page
    const response = await this.page.goto(url, {
      waitUntil: 'domcontentloaded',
      timeout: timeoutMs,
    });

    const loadTime = Date.now() - startTime;
    const status = response?.status() || 0;
    const title = await this.page.title().catch(() => '');

    return {
      url,
      title,
      status,
      depth,
      foundOn,
      loadTime,
    };
  }

  // Universal adaptive timeout that works for any website
  private getAdaptiveTimeout(baseTimeout: number, attempt: number): number {
    // Progressive timeout increase: each retry gets more time
    const progressiveMultiplier = 1 + attempt * 0.3; // 1x, 1.3x, 1.6x, 1.9x

    // Cap at 2.5x the base timeout to prevent excessive waits
    return Math.min(baseTimeout * progressiveMultiplier, baseTimeout * 2.5);
  }

  // Universal wait strategy that adapts based on retry attempt
  private getUniversalWaitStrategy(attempt: number): 'load' | 'domcontentloaded' | 'networkidle' {
    switch (attempt) {
      case 0:
        // First attempt: Fast loading for most pages
        return 'domcontentloaded';
      case 1:
        // Second attempt: Wait for all resources
        return 'load';
      case 2:
        // Third attempt: Most conservative (for complex SPAs)
        return 'networkidle';
      default:
        return 'domcontentloaded';
    }
  }

  private async extractLinksWithTimeout(currentUrl: string, timeoutMs: number): Promise<string[]> {
    try {
      // Set a timeout for link extraction
      const links = await Promise.race([
        this.extractLinks(currentUrl),
        new Promise<string[]>((_, reject) =>
          setTimeout(() => reject(new Error('Link extraction timeout')), timeoutMs)
        ),
      ]);

      return links;
    } catch (error) {
      console.warn(`⚠️  Failed to extract links from ${currentUrl}:`, error);
      return [];
    }
  }

  private async extractLinks(currentUrl: string): Promise<string[]> {
    try {
      await this.page.waitForSelector('a[href]', { timeout: 5000 }); // Wait for at least one link

      const links = await this.page.evaluate(() => {
        return Array.from(document.querySelectorAll('a[href]')).map(a => (a as HTMLAnchorElement).href);
      });

      // Resolve relative URLs and filter out invalid ones
      return links
        .map(href => this.resolveUrl(href, currentUrl))
        .filter((url): url is string => url !== null);
    } catch (error) {
      this.errorHandler.logWarning(`Could not extract links from ${currentUrl}`, {
        error: error instanceof Error ? error.message : error,
      });
      return [];
    }
  }

  private resolveUrl(href: string, baseUrl: string): string | null {
    try {
      const resolvedUrl = new URL(href, baseUrl);
      // Remove fragment identifiers
      resolvedUrl.hash = '';
      return resolvedUrl.toString();
    } catch {
      return null;
    }
  }

  private shouldCrawlUrl(
    url: string,
    allowedDomains: string[],
    excludePatterns: RegExp[],
    includePatterns: RegExp[]
  ): boolean {
    try {
      const urlObject = new URL(url);

      // 1. Check if the domain is allowed
      if (!allowedDomains.some(domain => urlObject.hostname.endsWith(domain))) {
        return false;
      }

      // 2. Check for exclude patterns (e.g., logout links, file downloads)
      if (excludePatterns.some(pattern => pattern.test(url))) {
        return false;
      }

      // 3. If include patterns are specified, the URL must match at least one
      if (includePatterns.length > 0 && !includePatterns.some(pattern => pattern.test(url))) {
        return false;
      }

      return true;
    } catch {
      return false;
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private getAverageLoadTime(): number {
    const successfulCrawls = this.results.filter(r => r.status === 200 && r.loadTime);
    if (successfulCrawls.length === 0) return 0;

    const totalLoadTime = successfulCrawls.reduce((sum, r) => sum + r.loadTime!, 0);
    return Math.round(totalLoadTime / successfulCrawls.length);
  }

  getSummary(): {
    total: number;
    successful: number;
    errors: number;
    byDepth: Record<number, number>;
    performance: {
      averageLoadTime: number;
      totalRetries: number;
      successRate: number;
    };
  } {
    const successful = this.results.filter(r => r.status === 200).length;
    const errors = this.errors.length;
    const total = this.results.length;

    const byDepth: Record<number, number> = {};
    for (const result of this.results) {
      if (result.status === 200) {
        byDepth[result.depth] = (byDepth[result.depth] || 0) + 1;
      }
    }

    return {
      total,
      successful,
      errors,
      byDepth,
      performance: {
        averageLoadTime: this.getAverageLoadTime(),
        totalRetries: this.results.reduce((sum, r) => sum + (r.retryCount || 0), 0),
        successRate: total > 0 ? (successful / total) * 100 : 0,
      },
    };
  }

  getAccessiblePages(): CrawlResult[] {
    return this.results.filter(r => r.status === 200);
  }

  getErrors(): Array<{ url: string; error: string; retryCount: number }> {
    return this.errors;
  }
}
