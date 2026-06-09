import { SiteCrawlingOrchestrator, CrawlOptions } from '@/utils/orchestration/site-crawling-orchestrator';
import { BrowserManager } from '@/core/utils/browser-manager';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { PageInfo } from '@/core/types/common';

// Mock dependencies
jest.mock('@/core/utils/browser-manager');
jest.mock('@/utils/services/error-handler-service');
jest.mock('@/utils/crawler/site-crawler');

describe('SiteCrawlingOrchestrator', () => {
    let siteCrawlingOrchestrator: SiteCrawlingOrchestrator;
    let mockBrowserManager: jest.Mocked<BrowserManager>;
    let mockErrorHandler: jest.Mocked<ErrorHandlerService>;

    const mockPages: PageInfo[] = [
        {
            url: 'https://example.com/page1',
            title: 'Page 1',
            depth: 0,
            foundOn: 'https://example.com',
            status: 200,
            loadTime: 1500
        },
        {
            url: 'https://example.com/page2',
            title: 'Page 2',
            depth: 1,
            foundOn: 'https://example.com/page1',
            status: 200,
            loadTime: 1200
        }
    ];

    const mockCrawlOptions: CrawlOptions = {
        maxPages: 10,
        maxDepth: 3,
        excludePatterns: [/admin/, /private/],
        delayBetweenRequests: 1000,
        maxRetries: 3,
        retryDelay: 2000,
        timeoutMs: 30000
    };

    beforeEach(() => {
        jest.clearAllMocks();

        // Setup mocks
        mockBrowserManager = {
            getPage: jest.fn(),
            getContext: jest.fn(),
            cleanup: jest.fn()
        } as any;

        mockErrorHandler = {
            handleError: jest.fn(),
            logError: jest.fn(),
            logWarning: jest.fn(),
            logInfo: jest.fn(),
            logSuccess: jest.fn()
        } as any;

        // Mock singleton getInstance methods
        (ErrorHandlerService.getInstance as jest.Mock).mockReturnValue(mockErrorHandler);

        siteCrawlingOrchestrator = new SiteCrawlingOrchestrator(mockBrowserManager, mockErrorHandler);
    });

    describe('constructor', () => {
        it('should create instance with provided dependencies', () => {
            expect(siteCrawlingOrchestrator).toBeInstanceOf(SiteCrawlingOrchestrator);
        });
    });

    describe('performSiteCrawling', () => {
        it('should successfully perform site crawling', async () => {
            const targetUrl = 'https://example.com';

            // Mock the crawling process
            const mockPage = {
                evaluate: jest.fn(),
                goto: jest.fn()
            };
            mockBrowserManager.getPage.mockResolvedValue(mockPage as any);

            // Mock SiteCrawler
            const mockSiteCrawler = {
                crawlSite: jest.fn().mockResolvedValue([
                    {
                        url: 'https://example.com/page1',
                        title: 'Page 1',
                        depth: 0,
                        foundOn: 'https://example.com',
                        status: 200,
                        loadTime: 1500
                    }
                ]),
                getSummary: jest.fn().mockReturnValue({
                    totalPages: 1,
                    successfulPages: 1,
                    failedPages: 0
                })
            };

            // Mock the SiteCrawler constructor
            const { SiteCrawler } = require('@/utils/crawler/site-crawler');
            SiteCrawler.mockImplementation(() => mockSiteCrawler);

            const result = await siteCrawlingOrchestrator.performSiteCrawling(targetUrl, mockCrawlOptions);

            expect(result).toBeDefined();
            expect(mockBrowserManager.getPage).toHaveBeenCalledWith('crawler-session');
            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith('Phase 1: Starting site crawling', {
                targetUrl,
                maxPages: 10,
                maxDepth: 3
            });
        });

        it('should handle empty target URL', async () => {
            const result = await siteCrawlingOrchestrator.performSiteCrawling('', mockCrawlOptions);

            expect(result).toEqual([]);
            expect(mockErrorHandler.logWarning).toHaveBeenCalledWith('Empty target URL provided');
        });

        it('should handle invalid URL', async () => {
            const result = await siteCrawlingOrchestrator.performSiteCrawling('invalid-url', mockCrawlOptions);

            expect(result).toEqual([]);
            expect(mockErrorHandler.logWarning).toHaveBeenCalledWith('Invalid URL format', {
                url: 'invalid-url'
            });
        });
    });

    describe('validateCrawlResults', () => {
        it('should validate valid results', () => {
            const validation = siteCrawlingOrchestrator.validateCrawlResults(mockPages);

            expect(validation).toEqual({
                isValid: true,
                errors: [],
                warnings: []
            });
        });

            it('should detect invalid results', () => {
      const invalidResults: PageInfo[] = [
        {
          ...mockPages[0],
          url: '', // Invalid empty URL
          title: '', // Invalid empty title
          depth: 0,
          foundOn: 'https://example.com',
          status: 200,
          loadTime: 1500
        }
      ];

      const validation = siteCrawlingOrchestrator.validateCrawlResults(invalidResults);

      expect(validation.isValid).toBe(false);
      expect(validation.errors.length).toBeGreaterThan(0);
    });
    });

    describe('getCrawlMetrics', () => {
        it('should calculate crawl metrics correctly', () => {
            const startTime = Date.now() - 5000; // 5 seconds ago
            const metrics = siteCrawlingOrchestrator.getCrawlMetrics(mockPages, startTime);

            expect(metrics).toEqual({
                totalPages: 2,
                crawlTime: 5000,
                averageTimePerPage: expect.any(Number),
                successRate: 100,
                pagesWithErrors: 0
            });
        });

        it('should handle empty results', () => {
            const startTime = Date.now();
            const metrics = siteCrawlingOrchestrator.getCrawlMetrics([], startTime);

            expect(metrics).toEqual({
                totalPages: 0,
                crawlTime: 0,
                averageTimePerPage: 0,
                successRate: 0,
                pagesWithErrors: 0
            });
        });
    });

    describe('getCrawlSummary', () => {
        it('should generate crawl summary', () => {
            const startTime = Date.now() - 5000;
            const summary = siteCrawlingOrchestrator.getCrawlSummary(mockPages, startTime);

            expect(summary).toEqual({
                totalPages: 2,
                successfulPages: 2,
                failedPages: 0,
                averageLoadTime: expect.any(Number),
                crawlDuration: 5000,
                successRate: 100
            });
        });
    });

    describe('isBrowserHealthy', () => {
        it('should return browser health status', async () => {
            const isHealthy = await siteCrawlingOrchestrator.isBrowserHealthy();

            expect(typeof isHealthy).toBe('boolean');
        });
    });

    describe('getBrowserStatus', () => {
        it('should return browser status', async () => {
            const status = await siteCrawlingOrchestrator.getBrowserStatus();

            expect(status).toEqual({
                isHealthy: expect.any(Boolean),
                isInitialized: expect.any(Boolean),
                activePages: expect.any(Number)
            });
        });
    });

    describe('error handling', () => {
        it('should handle browser manager errors', async () => {
            const error = new Error('Browser error');
            mockBrowserManager.getPage.mockRejectedValue(error);

            const result = await siteCrawlingOrchestrator.performSiteCrawling('https://example.com', mockCrawlOptions);

            expect(result).toEqual([]);
            expect(mockErrorHandler.handleError).toHaveBeenCalledWith(error, 'Site crawling failed');
        });
    });
}); 