import { Page } from '@playwright/test';

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

export interface CrawlOptions {
  maxPages?: number;
  maxDepth?: number;
  allowedDomains?: string[];
  excludePatterns?: RegExp[];
  includePatterns?: RegExp[];
  delayBetweenRequests?: number;
  respectRobotsTxt?: boolean;
  maxRetries?: number;
  retryDelay?: number;
  timeoutMs?: number;
}

export class SiteCrawler {
  private page: Page;
  private visited: Set<string> = new Set();
  private toVisit: Array<{ url: string; depth: number; foundOn: string }> = [];
  private results: CrawlResult[] = [];
  private baseUrl: string;
  private baseDomain: string;
  private errors: Array<{ url: string; error: string; retryCount: number }> = [];

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
      excludePatterns = [
        /\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz)$/i,
        /\/wp-admin\//,
        /\/admin\//,
        /\/login/,
        /\/logout/,
        /\/search\?/,
        /\/cart/,
        /\/checkout/,
        /\?.*utm_/,
        /#/,
      ],
      includePatterns = [],
      delayBetweenRequests = 500, // Reduced from 1000ms for faster crawling
      respectRobotsTxt = true,
      maxRetries = 2,
      retryDelay = 2000,
      timeoutMs = 20000, // Reduced from 30000ms
    } = options;

    console.log(`🕷️  Starting optimised site crawl from: ${this.baseUrl}`);
    console.log(`📊 Max pages: ${maxPages}, Max depth: ${maxDepth}, Timeout: ${timeoutMs}ms`);

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
        const result = await this.crawlPageWithRetry(url, depth, foundOn, maxRetries, retryDelay, timeoutMs);
        this.results.push(result);
        this.visited.add(url);

        // If successful and not at max depth, extract links
        if (result.status === 200 && depth < maxDepth) {
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
    console.log(`   🎯 Success rate: ${Math.round((this.results.filter(r => r.status === 200).length / this.results.length) * 100)}%`);
    console.log(`   ⚡ Average load time: ${this.getAverageLoadTime()}ms`);
    console.log(`   🔄 Total retries: ${this.results.reduce((sum, r) => sum + (r.retryCount || 0), 0)}`);

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

  private async crawlPageWithRetry(url: string, depth: number, foundOn: string, maxRetries: number, retryDelay: number, timeoutMs: number): Promise<CrawlResult> {
    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const startTime = Date.now();

        // Add progress indicator for retries
        if (attempt > 0) {
          console.log(`   🔄 Retry ${attempt}/${maxRetries} for ${url}`);
        }

        // Universal adaptive timeout strategy
        const adaptiveTimeout = this.getAdaptiveTimeout(timeoutMs, attempt);
        const waitStrategy = this.getUniversalWaitStrategy(attempt);

        const response = await this.page.goto(url, {
          waitUntil: waitStrategy,
          timeout: adaptiveTimeout,
        });

        const loadTime = Date.now() - startTime;
        const status = response?.status() || 0;
        const title = await this.page.title().catch(() => '');

        // Success
        if (attempt > 0) {
          console.log(`   ✅ Success after ${attempt} retries (${loadTime}ms)`);
        }

        return {
          url,
          title,
          status,
          depth,
          foundOn,
          retryCount: attempt,
          loadTime,
        };
      } catch (error) {
        lastError = error as Error;
        const errorMsg = error instanceof Error ? error.message : 'Unknown error';

        if (attempt < maxRetries) {
          console.warn(`   ⚠️  Attempt ${attempt + 1} failed for ${url}: ${errorMsg}`);
          await this.delay(retryDelay);
        } else {
          console.error(`   ❌ All attempts failed for ${url}: ${errorMsg}`);
          this.errors.push({ url, error: errorMsg, retryCount: attempt });
        }
      }
    }

    throw lastError || new Error('Max retries exceeded');
  }

  // Universal adaptive timeout that works for any website
  private getAdaptiveTimeout(baseTimeout: number, attempt: number): number {
    // Progressive timeout increase: each retry gets more time
    const progressiveMultiplier = 1 + (attempt * 0.3); // 1x, 1.3x, 1.6x, 1.9x

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
      const links = await this.page.$$eval('a[href]', anchors => {
        return anchors
          .map(anchor => anchor.getAttribute('href'))
          .filter((href): href is string => href !== null)
          .filter(href => href.trim() !== '');
      });

      const absoluteUrls = links
        .map(href => this.resolveUrl(href, currentUrl))
        .filter(url => url !== null) as string[];

      return [...new Set(absoluteUrls)]; // Remove duplicates
    } catch (error) {
      console.warn(`⚠️  Failed to extract links from ${currentUrl}:`, error);
      return [];
    }
  }

  private resolveUrl(href: string, baseUrl: string): string | null {
    try {
      // Handle various URL formats
      if (href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) {
        return null;
      }

      if (href.startsWith('//')) {
        href = new URL(baseUrl).protocol + href;
      }

      const resolvedUrl = new URL(href, baseUrl);

      // Remove fragments and clean query params
      resolvedUrl.hash = '';

      // Remove common tracking parameters
      const paramsToRemove = [
        'utm_source',
        'utm_medium',
        'utm_campaign',
        'utm_term',
        'utm_content',
        'fbclid',
        'gclid',
      ];
      paramsToRemove.forEach(param => {
        resolvedUrl.searchParams.delete(param);
      });

      return resolvedUrl.href;
    } catch (error) {
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
      const urlObj = new URL(url);

      // Check allowed domains
      if (
        !allowedDomains.some(
          domain => urlObj.hostname === domain || urlObj.hostname.endsWith(`.${domain}`)
        )
      ) {
        return false;
      }

      // Check exclude patterns
      if (excludePatterns.some(pattern => pattern.test(url))) {
        return false;
      }

      // Check include patterns (if any specified)
      if (includePatterns.length > 0 && !includePatterns.some(pattern => pattern.test(url))) {
        return false;
      }

      return true;
    } catch (error) {
      return false;
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private getAverageLoadTime(): number {
    const loadTimes = this.results
      .filter(r => r.loadTime !== undefined)
      .map(r => r.loadTime!);

    if (loadTimes.length === 0) return 0;

    return Math.round(loadTimes.reduce((sum, time) => sum + time, 0) / loadTimes.length);
  }

  // Get a summary of the crawl results
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
    const byDepth: Record<number, number> = {};

    this.results.forEach(result => {
      if (result.status === 200) {
        byDepth[result.depth] = (byDepth[result.depth] || 0) + 1;
      }
    });

    return {
      total: this.results.length,
      successful,
      errors: this.results.length - successful,
      byDepth,
      performance: {
        averageLoadTime: this.getAverageLoadTime(),
        totalRetries: this.results.reduce((sum, r) => sum + (r.retryCount || 0), 0),
        successRate: this.results.length > 0 ? (successful / this.results.length) * 100 : 0,
      },
    };
  }

  getAccessiblePages(): CrawlResult[] {
    return this.results.filter(result => result.status === 200);
  }

  getErrors(): Array<{ url: string; error: string; retryCount: number }> {
    return this.errors;
  }
}
