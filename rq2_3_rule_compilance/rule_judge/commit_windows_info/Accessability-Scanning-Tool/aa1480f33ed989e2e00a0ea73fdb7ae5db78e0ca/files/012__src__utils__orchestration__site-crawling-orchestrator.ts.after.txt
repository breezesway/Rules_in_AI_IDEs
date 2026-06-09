import { PageInfo } from '@/core/types/common';
import { BrowserManager } from '@/core/utils/browser-manager';
import { SiteCrawler, CrawlResult } from '@/utils/crawler/site-crawler';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { MetricsCalculator, CrawlMetrics } from './metrics-calculator';

export interface CrawlOptions {
    maxPages: number;
    maxDepth: number;
    excludePatterns: RegExp[];
    delayBetweenRequests?: number;
    maxRetries?: number;
    retryDelay?: number;
    timeoutMs?: number;
}

export interface ValidationResult {
    isValid: boolean;
    errors: string[];
    warnings: string[];
}

/**
 * Orchestrator class for site crawling operations
 * Extracted from WorkflowOrchestrator to improve maintainability and testability
 */
export class SiteCrawlingOrchestrator {
    private errorHandler: ErrorHandlerService;
    private browserManager: BrowserManager;
    private metricsCalculator: MetricsCalculator;

    constructor(
        browserManager: BrowserManager,
        errorHandler: ErrorHandlerService
    ) {
        this.browserManager = browserManager;
        this.errorHandler = errorHandler;
        this.metricsCalculator = new MetricsCalculator();
    }

    /**
     * Perform site crawling with the given options
     */
    async performSiteCrawling(
        targetUrl: string,
        options: CrawlOptions
    ): Promise<PageInfo[]> {
        this.errorHandler.logInfo('Phase 1: Starting site crawling', {
            targetUrl,
            maxPages: options.maxPages,
            maxDepth: options.maxDepth,
        });

        // Validate URL before starting crawl
        if (!targetUrl || targetUrl.trim() === '') {
            this.errorHandler.logWarning('Empty target URL provided');
            return [];
        }

        try {
            new URL(targetUrl); // This will throw for invalid URLs
        } catch (error) {
            this.errorHandler.logWarning('Invalid URL format', { url: targetUrl });
            return [];
        }

        const startTime = Date.now();

        try {
            const sessionId = 'crawler-session';
            const page = await this.browserManager.getPage(sessionId);

            const siteCrawler = new SiteCrawler(page, targetUrl);

            this.errorHandler.logInfo(`Starting crawl for: ${targetUrl}`);
            const crawlResults = await siteCrawler.crawlSite({
                maxPages: options.maxPages,
                maxDepth: options.maxDepth,
                excludePatterns: options.excludePatterns,
                delayBetweenRequests: options.delayBetweenRequests || 300,
                maxRetries: options.maxRetries || 3,
                retryDelay: options.retryDelay || 1500,
                timeoutMs: options.timeoutMs || 20000,
            });
            this.errorHandler.logInfo(
                `Crawl complete for: ${targetUrl}, pages found: ${crawlResults.length}`
            );

            // Convert to PageInfo format
            const pageInfos: PageInfo[] = crawlResults.map((result: CrawlResult) => ({
                url: result.url,
                title: result.title,
                depth: result.depth,
                foundOn: result.foundOn,
                status: result.status,
                loadTime: typeof result.loadTime === 'number' ? result.loadTime : 0,
            }));

            // Validate crawl results
            const validation = this.validateCrawlResults(pageInfos);
            if (!validation.isValid) {
                this.errorHandler.logWarning('Crawl validation failed', {
                    errors: validation.errors,
                    warnings: validation.warnings,
                });
            }

            // Calculate crawl metrics
            const crawlMetrics = this.getCrawlMetrics(pageInfos, startTime);
            this.errorHandler.logSuccess('Site crawling completed', {
                pagesFound: pageInfos.length,
                crawlMetrics,
                summary: siteCrawler.getSummary(),
            });

            return pageInfos;
        } catch (error) {
            this.errorHandler.logWarning(
                `Site crawling failed: ${error instanceof Error ? error.message : error}`
            );
            this.errorHandler.handleError(error, 'Site crawling failed');
            return [];
        }
    }

    /**
     * Validate crawl results for quality and completeness
     */
    validateCrawlResults(results: PageInfo[]): ValidationResult {
        const errors: string[] = [];
        const warnings: string[] = [];

        // Check for empty results
        if (results.length === 0) {
            errors.push('No pages were crawled');
        }

        // Check for pages with errors
        const pagesWithErrors = results.filter(page => page.status !== 200);
        if (pagesWithErrors.length > 0) {
            warnings.push(`${pagesWithErrors.length} pages had non-200 status codes`);
        }

        // Check for duplicate URLs
        const urls = results.map(page => page.url);
        const uniqueUrls = new Set(urls);
        if (urls.length !== uniqueUrls.size) {
            warnings.push('Duplicate URLs found in crawl results');
        }

        // Check for pages with empty or invalid URLs
        const pagesWithEmptyUrls = results.filter(page => !page.url || page.url.trim() === '');
        if (pagesWithEmptyUrls.length > 0) {
            errors.push(`${pagesWithEmptyUrls.length} pages have empty URLs`);
        }

        // Check for pages with missing titles
        const pagesWithoutTitles = results.filter(page => !page.title || page.title.trim() === '');
        if (pagesWithoutTitles.length > 0) {
            errors.push(`${pagesWithoutTitles.length} pages have missing titles`);
        }

        // Check for pages with excessive load times
        const slowPages = results.filter(page => page.loadTime > 10000); // 10 seconds
        if (slowPages.length > 0) {
            warnings.push(`${slowPages.length} pages have load times over 10 seconds`);
        }

        return {
            isValid: errors.length === 0,
            errors,
            warnings,
        };
    }

    /**
     * Calculate crawl-specific metrics
     */
    getCrawlMetrics(results: PageInfo[], startTime: number): CrawlMetrics {
        return this.metricsCalculator.calculateCrawlMetrics(results, startTime);
    }

    /**
     * Get a summary of crawl performance
     */
    getCrawlSummary(results: PageInfo[], startTime: number): {
        totalPages: number;
        successfulPages: number;
        failedPages: number;
        averageLoadTime: number;
        crawlDuration: number;
        successRate: number;
    } {
        const crawlMetrics = this.getCrawlMetrics(results, startTime);
        const successfulPages = results.filter(page => page.status === 200).length;
        const averageLoadTime = results.reduce((sum, page) => sum + page.loadTime, 0) / results.length;

        return {
            totalPages: results.length,
            successfulPages,
            failedPages: results.length - successfulPages,
            averageLoadTime,
            crawlDuration: crawlMetrics.crawlTime,
            successRate: crawlMetrics.successRate,
        };
    }

    /**
     * Check if the browser is healthy for crawling
     */
    async isBrowserHealthy(): Promise<boolean> {
        try {
            return await this.browserManager.isBrowserHealthy();
        } catch (error) {
            this.errorHandler.logWarning('Browser health check failed', { error });
            return false;
        }
    }

    /**
     * Force reinitialize browser if needed
     */
    async forceReinitializeBrowser(): Promise<void> {
        try {
            this.errorHandler.logInfo('Force reinitializing browser for crawling...');
            await this.browserManager.forceReinitialize();
            this.errorHandler.logSuccess('Browser reinitialized successfully');
        } catch (error) {
            this.errorHandler.handleError(error, 'Browser reinitialization failed');
            throw error;
        }
    }

    /**
 * Get browser status information
 */
    async getBrowserStatus(): Promise<{
        isHealthy: boolean;
        isInitialized: boolean;
        activePages: number;
    }> {
        try {
            const isHealthy = await this.browserManager.isBrowserHealthy();
            const resourceUsage = this.browserManager.getResourceUsage();

            return {
                isHealthy,
                isInitialized: resourceUsage.isInitialized,
                activePages: resourceUsage.pages,
            };
        } catch (error) {
            this.errorHandler.logWarning('Failed to get browser status', { error });
            return {
                isHealthy: false,
                isInitialized: false,
                activePages: 0,
            };
        }
    }
} 