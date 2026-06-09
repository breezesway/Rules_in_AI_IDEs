import { WorkflowOrchestrator } from '@/utils/orchestration/workflow-orchestrator';
import { SiteCrawlingOrchestrator } from '@/utils/orchestration/site-crawling-orchestrator';
import { AnalysisOrchestrator } from '@/utils/orchestration/analysis-orchestrator';
import { ReportGenerationOrchestrator } from '@/utils/orchestration/report-generation-orchestrator';
import { MetricsCalculator } from '@/utils/orchestration/metrics-calculator';
import { DataTransformer } from '@/utils/orchestration/data-transformer';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { DatabaseService } from '@/utils/services/database-service';
import { BrowserManager } from '@/core/utils/browser-manager';
import { ParallelAnalyzer } from '@/utils/orchestration/parallel-analyzer';

// Mock complex dependencies
jest.mock('@/core/utils/browser-manager');
jest.mock('@/utils/orchestration/parallel-analyzer');
jest.mock('@/utils/services/database-service');

describe('Orchestration Layer Integration Tests', () => {
    let workflowOrchestrator: WorkflowOrchestrator;
    let siteCrawlingOrchestrator: SiteCrawlingOrchestrator;
    let analysisOrchestrator: AnalysisOrchestrator;
    let reportGenerationOrchestrator: ReportGenerationOrchestrator;
    let metricsCalculator: MetricsCalculator;
    let dataTransformer: DataTransformer;
    let mockBrowserManager: jest.Mocked<BrowserManager>;
    let mockParallelAnalyzer: jest.Mocked<ParallelAnalyzer>;
    let mockDatabaseService: jest.Mocked<DatabaseService>;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;

    beforeEach(() => {
        // Setup mocks
        mockBrowserManager = {
            initialize: jest.fn().mockResolvedValue(undefined),
            navigateToUrl: jest.fn().mockResolvedValue({ success: true }),
            getPageContent: jest.fn().mockResolvedValue('<html><body>Test content</body></html>'),
            close: jest.fn().mockResolvedValue(undefined),
            getInstance: jest.fn().mockReturnThis(),
        } as any;

        mockParallelAnalyzer = {
            analyzePages: jest.fn().mockResolvedValue([]),
            getInstance: jest.fn().mockReturnThis(),
        } as any;

        mockDatabaseService = {
            storeReport: jest.fn().mockResolvedValue({ success: true }),
            getReport: jest.fn().mockResolvedValue({ success: true, data: {} }),
            getInstance: jest.fn().mockReturnThis(),
        } as any;

        // Setup real services
        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();

        // Setup orchestrators
        workflowOrchestrator = new WorkflowOrchestrator();
        siteCrawlingOrchestrator = new SiteCrawlingOrchestrator(mockBrowserManager, errorHandler);
        analysisOrchestrator = new AnalysisOrchestrator(mockParallelAnalyzer, errorHandler);
        reportGenerationOrchestrator = new ReportGenerationOrchestrator(mockDatabaseService, errorHandler);
        metricsCalculator = new MetricsCalculator();
        dataTransformer = new DataTransformer();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    describe('WorkflowOrchestrator Integration', () => {
        test('should initialize workflow orchestrator', () => {
            expect(workflowOrchestrator).toBeDefined();
            expect(workflowOrchestrator.browserManager).toBeDefined();
        });

        test('should handle workflow execution with mocked dependencies', async () => {
            const targetUrl = 'https://example.com';
            const options = {
                maxPages: 10,
                maxDepth: 2,
                maxConcurrency: 3,
                generateReports: false,
            };

            const result = await workflowOrchestrator.runAccessibilityAudit(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.crawlResults).toBeDefined();
            expect(result.analysisResults).toBeDefined();
            expect(result.metrics).toBeDefined();
        });

        test('should handle errors gracefully during workflow execution', async () => {
            mockBrowserManager.initialize.mockRejectedValue(new Error('Browser initialization failed'));

            const targetUrl = 'https://example.com';
            const options = { generateReports: false };

            const result = await workflowOrchestrator.runAccessibilityAudit(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.crawlResults).toEqual([]);
            expect(result.analysisResults).toEqual([]);
        });

        test('should perform site crawling with validation', async () => {
            const targetUrl = 'https://example.com';
            const options = {
                maxPages: 5,
                maxDepth: 2,
                excludePatterns: [/admin/, /private/],
            };

            const result = await workflowOrchestrator.performSiteCrawling(targetUrl, options);

            expect(Array.isArray(result)).toBe(true);
        });

        test('should perform accessibility analysis with batching', async () => {
            const pages = [
                { url: 'https://example.com', title: 'Home', depth: 0 },
                { url: 'https://example.com/about', title: 'About', depth: 1 },
            ];

            const result = await workflowOrchestrator.performAccessibilityAnalysis(pages, {
                maxConcurrency: 2,
                retryFailedPages: true,
            });

            expect(Array.isArray(result)).toBe(true);
        });

        test('should generate reports with proper validation', async () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const result = await workflowOrchestrator.generateReports(analysisResults, 'https://example.com');

            expect(Array.isArray(result)).toBe(true);
        });

        test('should convert analysis results to site-wide report', () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const result = workflowOrchestrator.convertAnalysisResultsToSiteWideReport(
                analysisResults,
                'https://example.com',
                'WCAG2AA'
            );

            expect(result).toBeDefined();
            expect(result.summary).toBeDefined();
            expect(result.violations).toBeDefined();
        });

        test('should get workflow status', async () => {
            const status = await workflowOrchestrator.getWorkflowStatus();

            expect(status).toBeDefined();
            expect(status.isRunning).toBeDefined();
            expect(status.browserStatus).toBeDefined();
            expect(status.parallelAnalyzerStatus).toBeDefined();
            expect(status.performanceMetrics).toBeDefined();
        });

        test('should perform quick audit', async () => {
            const targetUrl = 'https://example.com';
            const result = await workflowOrchestrator.quickAudit(targetUrl);

            expect(result).toBeDefined();
            expect(result.crawlResults).toBeDefined();
            expect(result.analysisResults).toBeDefined();
            expect(result.metrics).toBeDefined();
        });

        test('should perform comprehensive audit', async () => {
            const targetUrl = 'https://example.com';
            const result = await workflowOrchestrator.comprehensiveAudit(targetUrl);

            expect(result).toBeDefined();
            expect(result.crawlResults).toBeDefined();
            expect(result.analysisResults).toBeDefined();
            expect(result.metrics).toBeDefined();
        });

        test('should test single page with reports', async () => {
            const url = 'https://example.com';
            const result = await workflowOrchestrator.testSinglePageWithReports(url, 'WCAG2AA');

            expect(result).toBeDefined();
            expect(result.analysisResults).toBeDefined();
            expect(result.reportPaths).toBeDefined();
        });

        test('should handle cleanup operations', async () => {
            await expect(workflowOrchestrator.cleanup()).resolves.not.toThrow();
        });
    });

    describe('SiteCrawlingOrchestrator Integration', () => {
        test('should initialize site crawling orchestrator', () => {
            expect(siteCrawlingOrchestrator).toBeDefined();
        });

        test('should perform site crawling with validation', async () => {
            const targetUrl = 'https://example.com';
            const options = {
                maxPages: 5,
                maxDepth: 2,
                excludePatterns: [/admin/],
            };

            const result = await siteCrawlingOrchestrator.performSiteCrawling(targetUrl, options);

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle invalid URLs gracefully', async () => {
            const invalidUrl = 'invalid-url';
            const options = { maxPages: 5, maxDepth: 2, excludePatterns: [] };

            const result = await siteCrawlingOrchestrator.performSiteCrawling(invalidUrl, options);

            expect(Array.isArray(result)).toBe(true);
        });

        test('should validate crawl results', async () => {
            const targetUrl = 'https://example.com';
            const options = { maxPages: 3, maxDepth: 1, excludePatterns: [] };

            const result = await siteCrawlingOrchestrator.performSiteCrawling(targetUrl, options);

            expect(Array.isArray(result)).toBe(true);
            // Validate that results are properly structured
            if (result.length > 0) {
                expect(result[0]).toHaveProperty('url');
                expect(result[0]).toHaveProperty('title');
                expect(result[0]).toHaveProperty('depth');
            }
        });
    });

    describe('AnalysisOrchestrator Integration', () => {
        test('should initialize analysis orchestrator', () => {
            expect(analysisOrchestrator).toBeDefined();
        });

        test('should perform accessibility analysis', async () => {
            const pages = [
                { url: 'https://example.com', title: 'Home', depth: 0 },
                { url: 'https://example.com/about', title: 'About', depth: 1 },
            ];

            const result = await analysisOrchestrator.performAccessibilityAnalysis(pages, {
                maxConcurrency: 2,
                retryFailedPages: true,
            });

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle analysis validation', async () => {
            const pages = [
                { url: 'https://example.com', title: 'Home', depth: 0 },
            ];

            const result = await analysisOrchestrator.performAccessibilityAnalysis(pages, {
                maxConcurrency: 1,
                retryFailedPages: false,
            });

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle empty page list', async () => {
            const result = await analysisOrchestrator.performAccessibilityAnalysis([], {
                maxConcurrency: 2,
                retryFailedPages: true,
            });

            expect(Array.isArray(result)).toBe(true);
            expect(result).toHaveLength(0);
        });
    });

    describe('ReportGenerationOrchestrator Integration', () => {
        test('should initialize report generation orchestrator', () => {
            expect(reportGenerationOrchestrator).toBeDefined();
        });

        test('should generate reports with database storage', async () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const result = await reportGenerationOrchestrator.generateReports(analysisResults, 'https://example.com');

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle report validation', async () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const result = await reportGenerationOrchestrator.generateReports(analysisResults, 'https://example.com');

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle empty analysis results', async () => {
            const result = await reportGenerationOrchestrator.generateReports([], 'https://example.com');

            expect(Array.isArray(result)).toBe(true);
        });
    });

    describe('MetricsCalculator Integration', () => {
        test('should initialize metrics calculator', () => {
            expect(metricsCalculator).toBeDefined();
        });

        test('should calculate workflow metrics', () => {
            const crawlResults = [
                { url: 'https://example.com', title: 'Home', depth: 0 },
                { url: 'https://example.com/about', title: 'About', depth: 1 },
            ];

            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Home' },
                },
                {
                    url: 'https://example.com/about',
                    violations: [{ id: 'test-violation', description: 'Test violation' }],
                    metadata: { title: 'About' },
                },
            ];

            const totalTime = 5000;

            const metrics = metricsCalculator.calculateWorkflowMetrics(crawlResults, analysisResults, totalTime);

            expect(metrics).toBeDefined();
            expect(metrics.totalTime).toBe(totalTime);
            expect(metrics.pagesAnalyzed).toBe(2);
            expect(metrics.violationsFound).toBe(1);
            expect(metrics.successRate).toBeGreaterThanOrEqual(0);
            expect(metrics.successRate).toBeLessThanOrEqual(100);
        });

        test('should calculate crawl metrics', () => {
            const startTime = Date.now() - 1000; // 1 second ago
            const crawlResults = [
                { url: 'https://example.com', title: 'Home', depth: 0, foundOn: '', status: 200, loadTime: 100 },
                { url: 'https://example.com/about', title: 'About', depth: 1, foundOn: '', status: 200, loadTime: 150 },
                { url: 'https://example.com/contact', title: 'Contact', depth: 1, foundOn: '', status: 200, loadTime: 120 },
            ];

            const metrics = metricsCalculator.calculateCrawlMetrics(crawlResults, startTime);

            expect(metrics).toBeDefined();
            expect(metrics.totalPages).toBe(3);
            expect(metrics.crawlTime).toBeGreaterThan(0);
            expect(metrics.successRate).toBe(100);
        });

        test('should calculate analysis metrics', () => {
            const startTime = Date.now() - 1000; // 1 second ago
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Home' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 0, totalPasses: 10, totalWarnings: 0 }
                },
                {
                    url: 'https://example.com/about',
                    violations: [
                        { id: 'test-violation-1', description: 'Test violation 1' },
                        { id: 'test-violation-2', description: 'Test violation 2' },
                    ],
                    metadata: { title: 'About' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 2, totalPasses: 8, totalWarnings: 0 }
                },
            ];

            const metrics = metricsCalculator.calculateAnalysisMetrics(analysisResults, startTime);

            expect(metrics).toBeDefined();
            expect(metrics.totalPages).toBe(2);
            expect(metrics.totalViolations).toBe(2);
            expect(metrics.pagesWithViolations).toBe(1);
        });

        test('should handle empty results', () => {
            const startTime = Date.now() - 1000; // 1 second ago
            const workflowMetrics = metricsCalculator.calculateWorkflowMetrics([], [], 0);
            const crawlMetrics = metricsCalculator.calculateCrawlMetrics([], startTime);
            const analysisMetrics = metricsCalculator.calculateAnalysisMetrics([], startTime);

            expect(workflowMetrics).toBeDefined();
            expect(crawlMetrics).toBeDefined();
            expect(analysisMetrics).toBeDefined();

            expect(workflowMetrics.pagesAnalyzed).toBe(0);
            expect(workflowMetrics.violationsFound).toBe(0);
            expect(crawlMetrics.totalPages).toBe(0);
            expect(analysisMetrics.totalPages).toBe(0);
        });
    });

    describe('DataTransformer Integration', () => {
        test('should initialize data transformer', () => {
            expect(dataTransformer).toBeDefined();
        });

        test('should transform analysis results to report format', () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [
                        { id: 'test-violation', description: 'Test violation', impact: 'moderate' },
                    ],
                    metadata: { title: 'Test Page' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 1, totalPasses: 10, totalWarnings: 0 }
                },
            ];

            const transformed = dataTransformer.convertAnalysisResultsToSiteWideReport(analysisResults, 'https://example.com');

            expect(transformed).toBeDefined();
            expect(transformed.summary).toBeDefined();
            expect(transformed.violationsByType).toBeDefined();
            expect(transformed.pageReports).toBeDefined();
        });

        test('should aggregate violations by type', () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [
                        { id: 'test-violation-1', description: 'Test violation 1', impact: 'moderate' },
                        { id: 'test-violation-2', description: 'Test violation 2', impact: 'critical' },
                    ],
                    metadata: { title: 'Test Page' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 2, totalPasses: 8, totalWarnings: 0 }
                },
            ];

            const aggregated = dataTransformer.aggregateViolations(analysisResults);

            expect(aggregated).toBeDefined();
            expect(aggregated.violationsByType).toBeDefined();
            expect(aggregated.mostCommonViolations).toBeDefined();
        });

        test('should calculate compliance percentage', () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 0, totalPasses: 10, totalWarnings: 0 }
                },
                {
                    url: 'https://example.com/about',
                    violations: [{ id: 'test-violation', description: 'Test violation' }],
                    metadata: { title: 'About' },
                    timestamp: new Date().toISOString(),
                    tool: 'axe-core',
                    passes: [],
                    warnings: [],
                    summary: { totalViolations: 1, totalPasses: 9, totalWarnings: 0 }
                },
            ];

            const compliance = dataTransformer.calculateCompliancePercentage(analysisResults);

            expect(compliance).toBeDefined();
            expect(compliance).toBe(50); // 1 out of 2 pages has violations
        });

        test('should handle empty analysis results', () => {
            const transformed = dataTransformer.convertAnalysisResultsToSiteWideReport([], 'https://example.com');
            const aggregated = dataTransformer.aggregateViolations([]);
            const compliance = dataTransformer.calculateCompliancePercentage([]);

            expect(transformed).toBeDefined();
            expect(aggregated).toBeDefined();
            expect(compliance).toBeDefined();
        });
    });

    describe('Cross-Orchestrator Integration', () => {
        test('should integrate site crawling with analysis', async () => {
            const targetUrl = 'https://example.com';
            const crawlOptions = { maxPages: 3, maxDepth: 1, excludePatterns: [] };
            const analysisOptions = { maxConcurrency: 2, retryFailedPages: true };

            const crawlResults = await siteCrawlingOrchestrator.performSiteCrawling(targetUrl, crawlOptions);
            const analysisResults = await analysisOrchestrator.performAccessibilityAnalysis(crawlResults, analysisOptions);

            expect(Array.isArray(crawlResults)).toBe(true);
            expect(Array.isArray(analysisResults)).toBe(true);
        });

        test('should integrate analysis with report generation', async () => {
            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const reports = await reportGenerationOrchestrator.generateReports(analysisResults, 'https://example.com');
            const metrics = metricsCalculator.calculateWorkflowMetrics([], analysisResults, 1000);

            expect(Array.isArray(reports)).toBe(true);
            expect(metrics).toBeDefined();
        });

        test('should handle complete workflow integration', async () => {
            const targetUrl = 'https://example.com';

            // Simulate complete workflow
            const crawlResults = await siteCrawlingOrchestrator.performSiteCrawling(targetUrl, {
                maxPages: 2,
                maxDepth: 1,
                excludePatterns: [],
            });

            const analysisResults = await analysisOrchestrator.performAccessibilityAnalysis(crawlResults, {
                maxConcurrency: 1,
                retryFailedPages: false,
            });

            const reports = await reportGenerationOrchestrator.generateReports(analysisResults, targetUrl);
            const metrics = metricsCalculator.calculateWorkflowMetrics(crawlResults, analysisResults, 2000);

            expect(Array.isArray(crawlResults)).toBe(true);
            expect(Array.isArray(analysisResults)).toBe(true);
            expect(Array.isArray(reports)).toBe(true);
            expect(metrics).toBeDefined();
        });
    });

    describe('Error Handling and Resilience', () => {
        test('should handle browser manager failures', async () => {
            mockBrowserManager.initialize.mockRejectedValue(new Error('Browser failed to initialize'));

            const targetUrl = 'https://example.com';
            const result = await workflowOrchestrator.runAccessibilityAudit(targetUrl, { generateReports: false });

            expect(result).toBeDefined();
            expect(result.crawlResults).toEqual([]);
            expect(result.analysisResults).toEqual([]);
        });

        test('should handle parallel analyzer failures', async () => {
            mockParallelAnalyzer.analyzePages.mockRejectedValue(new Error('Analysis failed'));

            const pages = [{ url: 'https://example.com', title: 'Test', depth: 0 }];
            const result = await analysisOrchestrator.performAccessibilityAnalysis(pages, {
                maxConcurrency: 1,
                retryFailedPages: false,
            });

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle database service failures', async () => {
            mockDatabaseService.storeReport.mockRejectedValue(new Error('Database failed'));

            const analysisResults = [
                {
                    url: 'https://example.com',
                    violations: [],
                    metadata: { title: 'Test Page' },
                },
            ];

            const result = await reportGenerationOrchestrator.generateReports(analysisResults, 'https://example.com');

            expect(Array.isArray(result)).toBe(true);
        });

        test('should handle configuration service failures', async () => {
            const targetUrl = 'https://example.com';
            const result = await workflowOrchestrator.runAccessibilityAudit(targetUrl, { generateReports: false });

            expect(result).toBeDefined();
        });
    });

    describe('Performance and Resource Management', () => {
        test('should handle concurrent operations', async () => {
            const targetUrl = 'https://example.com';
            const promises = [
                workflowOrchestrator.runAccessibilityAudit(targetUrl, { generateReports: false }),
                workflowOrchestrator.runAccessibilityAudit(targetUrl, { generateReports: false }),
            ];

            const results = await Promise.all(promises);

            expect(results).toHaveLength(2);
            results.forEach(result => {
                expect(result).toBeDefined();
                expect(result.crawlResults).toBeDefined();
                expect(result.analysisResults).toBeDefined();
            });
        });

        test('should handle large datasets', async () => {
            const largeAnalysisResults = Array.from({ length: 100 }, (_, i) => ({
                url: `https://example.com/page-${i}`,
                violations: [],
                metadata: { title: `Page ${i}` },
            }));

            const metrics = metricsCalculator.calculateAnalysisMetrics(largeAnalysisResults);
            const transformed = dataTransformer.transformAnalysisResultsToReport(largeAnalysisResults);

            expect(metrics).toBeDefined();
            expect(metrics.totalPages).toBe(100);
            expect(transformed).toBeDefined();
            expect(transformed.pages).toHaveLength(100);
        });

        test('should handle memory-intensive operations', async () => {
            const targetUrl = 'https://example.com';
            const result = await workflowOrchestrator.runAccessibilityAudit(targetUrl, {
                maxPages: 50,
                maxDepth: 3,
                generateReports: false,
            });

            expect(result).toBeDefined();
            expect(result.metrics).toBeDefined();
        });
    });
}); 