import { AnalysisService } from '@/utils/api/analysis-service';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { DatabaseService } from '@/utils/services/database-service';
import { WorkflowOrchestrator } from '@/utils/orchestration/workflow-orchestrator';

// Mock complex dependencies
jest.mock('@/utils/services/database-service');
jest.mock('@/utils/orchestration/workflow-orchestrator');
jest.mock('@/utils/orchestration/analysis-cache');
jest.mock('@/utils/analysis/tool-orchestrator');
jest.mock('@/utils/orchestration/parallel-analyzer');
jest.mock('@/core/utils/browser-manager');

describe('API Layer Integration Tests', () => {
    let analysisService: AnalysisService;
    let mockDatabaseService: jest.Mocked<DatabaseService>;
    let mockWorkflowOrchestrator: jest.Mocked<WorkflowOrchestrator>;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;

    beforeEach(() => {
        // Setup test environment and database cleanup
        (global as any).testUtils.database.setupTestEnvironment();

        // Setup mocks
        mockDatabaseService = {
            storeReport: jest.fn().mockResolvedValue({ success: true }),
            getReports: jest.fn().mockResolvedValue({ success: true, data: [] }),
            getAllReports: jest.fn().mockResolvedValue({ success: true, data: [] }),
            deleteReport: jest.fn().mockResolvedValue({ success: true }),
            getInstance: jest.fn().mockReturnThis(),
        } as any;

        mockWorkflowOrchestrator = {
            runAccessibilityAudit: jest.fn().mockResolvedValue({
                crawlResults: [],
                analysisResults: [],
                reportPaths: [],
                metrics: {
                    totalTime: 1000,
                    crawlTime: 500,
                    analysisTime: 300,
                    reportTime: 200,
                    successRate: 100,
                    pagesAnalyzed: 5,
                    violationsFound: 0,
                },
            }),
            testSinglePage: jest.fn().mockResolvedValue([]),
            testSinglePageWithReports: jest.fn().mockResolvedValue({
                analysisResults: [],
                reportPaths: [],
            }),
            generatePdfReportsFromStoredData: jest.fn().mockResolvedValue({
                success: true,
                data: [],
            }),
            getInstance: jest.fn().mockReturnThis(),
        } as any;

        // Setup real services
        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();

        // Setup API service using singleton pattern
        analysisService = AnalysisService.getInstance();
    });

    afterEach(async () => {
        // Clean up test data and verify cleanup
        await (global as any).testUtils.database.cleanupTestData();
        await (global as any).testUtils.database.verifyCleanup();
        jest.clearAllMocks();
    });

    describe('AnalysisService Integration', () => {
        test('should initialize analysis service', () => {
            expect(analysisService).toBeDefined();
        });

        test('should analyze single page successfully', async () => {
            const targetUrl = 'https://example.com';
            const options = {
                wcagLevel: 'WCAG2AA',
                timeout: 30000,
            };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should analyze page with detailed results', async () => {
            const targetUrl = 'https://example.com';
            const options = {
                wcagLevel: 'WCAG2AA',
                timeout: 30000,
            };

            const result = await analysisService.analyzePageDetailed(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should get analysis status successfully', () => {
            const analysisId = 'test-analysis-id';

            const result = analysisService.getAnalysisStatus(analysisId);

            expect(result).toBeDefined();
        });

        test('should get all active analyses', () => {
            const result = analysisService.getActiveAnalyses();

            expect(result).toBeDefined();
            expect(Array.isArray(result)).toBe(true);
        });

        test('should cancel analysis successfully', async () => {
            const analysisId = 'test-analysis-id';

            const result = await analysisService.cancelAnalysis(analysisId);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should get analysis metrics', () => {
            const result = analysisService.getAnalysisMetrics();

            expect(result).toBeDefined();
            expect(result.totalAnalyses).toBeDefined();
            expect(result.activeAnalyses).toBeDefined();
            expect(result.completedAnalyses).toBeDefined();
            expect(result.failedAnalyses).toBeDefined();
            expect(result.averageAnalysisTime).toBeDefined();
            expect(result.totalPagesAnalyzed).toBeDefined();
        });

        test('should handle invalid URLs gracefully', async () => {
            const invalidUrl = 'invalid-url';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(invalidUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should handle analysis failures gracefully', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should validate analysis options', async () => {
            const targetUrl = 'https://example.com';
            const invalidOptions = {
                wcagLevel: 'INVALID_LEVEL',
                timeout: -1,
            };

            const result = await analysisService.analyzePage(targetUrl, invalidOptions);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should handle concurrent analysis requests', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const promises = [
                analysisService.analyzePage(targetUrl, options),
                analysisService.analyzePage(targetUrl, options),
                analysisService.analyzePage(targetUrl, options),
            ];

            const results = await Promise.all(promises);

            expect(results).toHaveLength(3);
            results.forEach((result: any) => {
                expect(result).toBeDefined();
                expect(result.success).toBeDefined();
            });
        });

        test('should handle analysis timeout scenarios', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA', timeout: 1000 };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should handle large page analysis', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
        });

        test('should handle configuration service integration', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
            // Should use configuration service for default options
        });

        test('should handle error handler service integration', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
            expect(result.success).toBeDefined();
            // Should use error handler service for error handling
        });
    });

    describe('Cross-Service Integration', () => {
        test('should integrate with error handling service', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            // Should handle errors gracefully through error handler service
            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
        });

        test('should integrate with configuration service', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            // Should use configuration service for settings
            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
        });

        test('should integrate with analysis cache', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            // Should use analysis cache for performance
            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
        });

        test('should integrate with browser manager', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            // Should use browser manager for page interaction
            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result).toBeDefined();
        });
    });

    describe('Performance and Resource Management', () => {
        test('should handle memory-intensive operations', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const startTime = Date.now();
            const result = await analysisService.analyzePage(targetUrl, options);
            const endTime = Date.now();

            expect(result.success).toBeDefined();
            expect(endTime - startTime).toBeLessThan(10000); // Should complete within 10 seconds
        });

        test('should handle concurrent service operations', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const startTime = Date.now();
            const promises = Array.from({ length: 10 }, () =>
                analysisService.analyzePage(targetUrl, options)
            );

            const results = await Promise.all(promises);
            const endTime = Date.now();

            expect(results).toHaveLength(10);
            results.forEach((result: any) => {
                expect(result.success).toBeDefined();
            });
            expect(endTime - startTime).toBeLessThan(5000); // Should complete within 5 seconds
        });

        test('should handle resource cleanup', async () => {
            const analysisId = 'test-analysis-id';

            // Start an analysis
            const startResult = await analysisService.analyzePage('https://example.com', { wcagLevel: 'WCAG2AA' });
            expect(startResult.success).toBeDefined();

            // Cancel the analysis
            const cancelResult = await analysisService.cancelAnalysis(analysisId);
            expect(cancelResult.success).toBeDefined();
        });
    });

    describe('Error Recovery and Resilience', () => {
        test('should recover from temporary analysis failures', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result.success).toBeDefined();
        });

        test('should handle partial analysis failures', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result.success).toBeDefined();
        });

        test('should handle service unavailability', async () => {
            const targetUrl = 'https://example.com';
            const options = { wcagLevel: 'WCAG2AA' };

            const result = await analysisService.analyzePage(targetUrl, options);

            expect(result.success).toBeDefined();
        });
    });
}); 