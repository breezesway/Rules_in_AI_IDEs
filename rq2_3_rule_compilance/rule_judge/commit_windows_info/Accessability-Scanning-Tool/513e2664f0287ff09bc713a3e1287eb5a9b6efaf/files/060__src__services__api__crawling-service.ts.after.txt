import { EventEmitter } from 'events';
import { AccessibilityTestOptions, ServiceResult } from '../../core/types/common';
import { PerformanceMonitor } from '../../core/utils/performance-monitor';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { AnalysisCache } from '../orchestration/analysis-cache';

// Import the existing site crawler
import { SiteCrawler } from '../../playwright/tests/utils/site-crawler';

export class CrawlingService extends EventEmitter {
  private static instance: CrawlingService;
  private siteCrawler: SiteCrawler;
  private performanceMonitor: PerformanceMonitor;
  private errorHandler: ErrorHandlerService;
  private analysisCache: AnalysisCache;
  private activeCrawls: Map<
    string,
    {
      url: string;
      startTime: Date;
      status: 'pending' | 'crawling' | 'completed' | 'failed';
      pagesFound: number;
      pagesProcessed: number;
    }
  > = new Map();

  private constructor() {
    super();
    this.siteCrawler = new SiteCrawler();
    this.performanceMonitor = PerformanceMonitor.getInstance();
    this.errorHandler = ErrorHandlerService.getInstance();
    this.analysisCache = AnalysisCache.getInstance();
  }

  public static getInstance(): CrawlingService {
    if (!CrawlingService.instance) {
      CrawlingService.instance = new CrawlingService();
    }
    return CrawlingService.instance;
  }

  public async crawlSite(
    url: string,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const crawlId = this.generateCrawlId();
    const timer = this.performanceMonitor.startTimer(`crawl_${crawlId}`);

    try {
      // Check cache first
      const cachedResult = await this.analysisCache.getOrAnalyze(
        `crawl_${url}`,
        () => this.performCrawl(url, options, crawlId),
        { ttl: 3600000 } // 1 hour cache
      );

      if (cachedResult) {
        return cachedResult;
      }

      // Perform the crawl
      const result = await this.performCrawl(url, options, crawlId);

      timer.stop();
      return result;
    } catch (error) {
      timer.stop();
      this.updateCrawlStatus(crawlId, 'failed', 0, 0);
      this.errorHandler.handleError(error as Error, 'CrawlingService.crawlSite');

      return {
        success: false,
        error: error as Error,
        message: `Site crawling failed: ${(error as Error).message}`,
      };
    }
  }

  private async performCrawl(
    url: string,
    options: AccessibilityTestOptions,
    crawlId: string
  ): Promise<ServiceResult<any>> {
    // Initialize crawl tracking
    this.activeCrawls.set(crawlId, {
      url,
      startTime: new Date(),
      status: 'pending',
      pagesFound: 0,
      pagesProcessed: 0,
    });

    try {
      this.updateCrawlStatus(crawlId, 'crawling', 0, 0);
      this.emit('crawlStarted', { crawlId, url });

      // Configure crawl options
      const crawlOptions = {
        maxPages: options.maxPages || 100,
        timeout: options.timeout || 30000,
        excludePatterns: options.excludePatterns || [],
        includePatterns: options.includePatterns || [],
        maxDepth: options.maxDepth || 3,
        respectRobotsTxt: options.respectRobotsTxt !== false,
        userAgent: options.userAgent || 'Accessibility-Testing-Bot/1.0',
        ...options,
      };

      // Start crawling
      const crawlResult = await this.siteCrawler.crawl(url, crawlOptions);

      if (crawlResult.success) {
        const pages = crawlResult.data?.pages || [];
        this.updateCrawlStatus(crawlId, 'completed', pages.length, pages.length);

        const result = {
          success: true,
          data: {
            pages: pages,
            crawlMetrics: {
              totalPages: pages.length,
              crawlTime: Date.now() - this.activeCrawls.get(crawlId)!.startTime.getTime(),
              baseUrl: url,
              crawlId,
            },
          },
          message: `Successfully crawled ${pages.length} pages from ${url}`,
        };

        this.emit('crawlCompleted', { crawlId, result });
        return result;
      } else {
        this.updateCrawlStatus(crawlId, 'failed', 0, 0);

        const result = {
          success: false,
          error: crawlResult.error,
          message: crawlResult.message || 'Crawl failed',
        };

        this.emit('crawlFailed', { crawlId, error: crawlResult.error });
        return result;
      }
    } catch (error) {
      this.updateCrawlStatus(crawlId, 'failed', 0, 0);
      this.emit('crawlFailed', { crawlId, error });

      return {
        success: false,
        error: error as Error,
        message: `Crawl failed: ${(error as Error).message}`,
      };
    } finally {
      // Clean up crawl tracking after a delay
      setTimeout(() => {
        this.activeCrawls.delete(crawlId);
      }, 300000); // 5 minutes
    }
  }

  public async crawlPage(
    url: string,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const timer = this.performanceMonitor.startTimer(`crawl_page_${url}`);

    try {
      // Check cache first
      const cachedResult = await this.analysisCache.getOrAnalyze(
        `page_${url}`,
        () => this.performPageCrawl(url, options),
        { ttl: 1800000 } // 30 minutes cache
      );

      if (cachedResult) {
        return cachedResult;
      }

      const result = await this.performPageCrawl(url, options);
      timer.stop();
      return result;
    } catch (error) {
      timer.stop();
      this.errorHandler.handleError(error as Error, 'CrawlingService.crawlPage');

      return {
        success: false,
        error: error as Error,
        message: `Page crawling failed: ${(error as Error).message}`,
      };
    }
  }

  private async performPageCrawl(
    url: string,
    options: AccessibilityTestOptions
  ): Promise<ServiceResult<any>> {
    try {
      // Get page information
      const pageInfo = await this.siteCrawler.getPageInfo(url, options);

      return {
        success: true,
        data: {
          page: pageInfo,
          crawlMetrics: {
            totalPages: 1,
            crawlTime: 0,
            baseUrl: url,
          },
        },
        message: `Successfully crawled page ${url}`,
      };
    } catch (error) {
      return {
        success: false,
        error: error as Error,
        message: `Page crawl failed: ${(error as Error).message}`,
      };
    }
  }

  public async discoverPages(
    baseUrl: string,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<string[]>> {
    const timer = this.performanceMonitor.startTimer(`discover_pages_${baseUrl}`);

    try {
      // Use lighter discovery method
      const discoveryResult = await this.siteCrawler.discoverPages(baseUrl, {
        maxPages: options.maxPages || 50,
        maxDepth: options.maxDepth || 2,
        timeout: options.timeout || 15000,
        ...options,
      });

      if (discoveryResult.success) {
        const pages = discoveryResult.data?.pages || [];
        const urls = pages.map(p => p.url);

        timer.stop();
        return {
          success: true,
          data: urls,
          message: `Discovered ${urls.length} pages from ${baseUrl}`,
        };
      } else {
        timer.stop();
        return {
          success: false,
          error: discoveryResult.error,
          message: discoveryResult.message || 'Page discovery failed',
        };
      }
    } catch (error) {
      timer.stop();
      this.errorHandler.handleError(error as Error, 'CrawlingService.discoverPages');

      return {
        success: false,
        error: error as Error,
        message: `Page discovery failed: ${(error as Error).message}`,
      };
    }
  }

  public getCrawlStatus(crawlId: string): {
    crawlId: string;
    status: string;
    progress: number;
    pagesFound: number;
    pagesProcessed: number;
    startTime: Date;
  } | null {
    const crawl = this.activeCrawls.get(crawlId);
    if (!crawl) return null;

    const progress = crawl.pagesFound > 0 ? (crawl.pagesProcessed / crawl.pagesFound) * 100 : 0;

    return {
      crawlId,
      status: crawl.status,
      progress,
      pagesFound: crawl.pagesFound,
      pagesProcessed: crawl.pagesProcessed,
      startTime: crawl.startTime,
    };
  }

  public getActiveCrawls(): Array<{
    crawlId: string;
    url: string;
    status: string;
    pagesFound: number;
    pagesProcessed: number;
    startTime: Date;
  }> {
    return Array.from(this.activeCrawls.entries()).map(([crawlId, crawl]) => ({
      crawlId,
      url: crawl.url,
      status: crawl.status,
      pagesFound: crawl.pagesFound,
      pagesProcessed: crawl.pagesProcessed,
      startTime: crawl.startTime,
    }));
  }

  public async cancelCrawl(crawlId: string): Promise<ServiceResult<void>> {
    const crawl = this.activeCrawls.get(crawlId);

    if (!crawl) {
      return {
        success: false,
        message: 'Crawl not found',
      };
    }

    if (crawl.status === 'completed' || crawl.status === 'failed') {
      return {
        success: false,
        message: 'Cannot cancel completed crawl',
      };
    }

    // Cancel the crawl
    this.updateCrawlStatus(crawlId, 'failed', crawl.pagesFound, crawl.pagesProcessed);
    this.emit('crawlCancelled', { crawlId });

    return {
      success: true,
      message: 'Crawl cancelled successfully',
    };
  }

  private updateCrawlStatus(
    crawlId: string,
    status: 'pending' | 'crawling' | 'completed' | 'failed',
    pagesFound: number,
    pagesProcessed: number
  ): void {
    const crawl = this.activeCrawls.get(crawlId);
    if (crawl) {
      crawl.status = status;
      crawl.pagesFound = pagesFound;
      crawl.pagesProcessed = pagesProcessed;

      this.emit('crawlingProgress', {
        crawlId,
        status,
        pagesFound,
        pagesProcessed,
        progress: pagesFound > 0 ? (pagesProcessed / pagesFound) * 100 : 0,
      });
    }
  }

  private generateCrawlId(): string {
    return `crawl_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  public getCrawlMetrics(): {
    totalCrawls: number;
    activeCrawls: number;
    completedCrawls: number;
    failedCrawls: number;
    averageCrawlTime: number;
    totalPagesFound: number;
  } {
    const crawls = Array.from(this.activeCrawls.values());
    const totalCrawls = crawls.length;
    const activeCrawls = crawls.filter(
      c => c.status === 'crawling' || c.status === 'pending'
    ).length;
    const completedCrawls = crawls.filter(c => c.status === 'completed').length;
    const failedCrawls = crawls.filter(c => c.status === 'failed').length;

    const completedCrawlsWithTime = crawls.filter(c => c.status === 'completed');
    const averageCrawlTime =
      completedCrawlsWithTime.length > 0
        ? completedCrawlsWithTime.reduce(
            (sum, crawl) => sum + (Date.now() - crawl.startTime.getTime()),
            0
          ) / completedCrawlsWithTime.length
        : 0;

    const totalPagesFound = crawls.reduce((sum, crawl) => sum + crawl.pagesFound, 0);

    return {
      totalCrawls,
      activeCrawls,
      completedCrawls,
      failedCrawls,
      averageCrawlTime,
      totalPagesFound,
    };
  }

  public async optimizeCrawlSettings(): Promise<void> {
    // Analyze recent crawl performance and optimize settings
    const metrics = this.getCrawlMetrics();
    const cachePerformance = this.analysisCache.getPerformance();

    // Optimization logic would go here
    // For now, just emit an event
    this.emit('settingsOptimized', {
      metrics,
      cachePerformance,
    });
  }

  public async shutdown(): Promise<void> {
    // Cancel all active crawls
    for (const crawlId of this.activeCrawls.keys()) {
      await this.cancelCrawl(crawlId);
    }

    // Cleanup
    this.activeCrawls.clear();
    this.removeAllListeners();
  }
}
