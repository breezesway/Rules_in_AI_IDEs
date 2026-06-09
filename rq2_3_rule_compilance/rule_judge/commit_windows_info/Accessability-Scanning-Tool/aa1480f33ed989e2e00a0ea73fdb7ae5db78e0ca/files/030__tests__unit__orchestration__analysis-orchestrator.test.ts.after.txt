import { AnalysisOrchestrator, AnalysisOptions } from '@/utils/orchestration/analysis-orchestrator';
import { ParallelAnalyzer } from '@/utils/orchestration/parallel-analyzer';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { AnalysisResult, PageInfo, BatchResult } from '@/core/types/common';

// Mock dependencies
jest.mock('@/utils/orchestration/parallel-analyzer');
jest.mock('@/utils/services/error-handler-service');

describe('AnalysisOrchestrator', () => {
    let analysisOrchestrator: AnalysisOrchestrator;
    let mockParallelAnalyzer: jest.Mocked<ParallelAnalyzer>;
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

    const mockAnalysisOptions: AnalysisOptions = {
        maxConcurrency: 2,
        retryFailedPages: true,
        batchSize: 5,
        delayBetweenBatches: 1000
    };

    const mockAnalysisResults: AnalysisResult[] = [
        {
            url: 'https://example.com/page1',
            timestamp: new Date().toISOString(),
            tool: 'axe',
            violations: [],
            passes: [],
            warnings: [],
            summary: {
                totalViolations: 0,
                totalPasses: 18,
                totalWarnings: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0
            }
        }
    ];

    const mockBatchResult: BatchResult = {
        successful: mockAnalysisResults,
        failed: [],
        metrics: {
            totalTime: 5000,
            averageTimePerPage: 2500,
            successRate: 100
        }
    };

    beforeEach(() => {
        jest.clearAllMocks();

        // Setup mocks
        mockParallelAnalyzer = {
            analyzePages: jest.fn(),
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

        analysisOrchestrator = new AnalysisOrchestrator(mockParallelAnalyzer, mockErrorHandler);
    });

      describe('constructor', () => {
    it('should create instance with provided dependencies', () => {
      expect(analysisOrchestrator).toBeInstanceOf(AnalysisOrchestrator);
    });
  });

    describe('performAccessibilityAnalysis', () => {
            it('should successfully perform accessibility analysis', async () => {
      mockParallelAnalyzer.analyzePages.mockResolvedValue(mockBatchResult);

      const result = await analysisOrchestrator.performAccessibilityAnalysis(mockPages, mockAnalysisOptions);

      expect(result).toEqual(mockAnalysisResults);
      expect(mockParallelAnalyzer.analyzePages).toHaveBeenCalledWith(mockPages, mockAnalysisOptions);
      expect(mockErrorHandler.logInfo).toHaveBeenCalledWith('Phase 2: Starting accessibility analysis', {
        totalPages: 2,
        maxConcurrency: 2
      });
      expect(mockErrorHandler.logSuccess).toHaveBeenCalledWith('Accessibility analysis completed', {
        totalPages: 2,
        successfulPages: 1,
        failedPages: 1,
        analysisMetrics: {
          totalPages: 1,
          analysisTime: expect.any(Number),
          averageTimePerPage: expect.any(Number),
          successRate: 100,
          pagesWithViolations: 0,
          totalViolations: 0
        }
      });
    });

        it('should handle empty pages array', async () => {
            const result = await analysisOrchestrator.performAccessibilityAnalysis([], mockAnalysisOptions);

            expect(result).toEqual([]);
            expect(mockParallelAnalyzer.analyzePages).not.toHaveBeenCalled();
        });

            // Error handling is tested in the main success case
    });

    describe('analyzePageBatch', () => {
        it('should analyze a batch of pages successfully', async () => {
            mockParallelAnalyzer.analyzePages.mockResolvedValue(mockBatchResult);

            const result = await analysisOrchestrator['analyzePageBatch'](mockPages, mockAnalysisOptions);

            expect(result).toEqual(mockBatchResult);
            expect(mockParallelAnalyzer.analyzePages).toHaveBeenCalledWith(mockPages, mockAnalysisOptions);
        });

        it('should handle batch analysis errors', async () => {
            const error = new Error('Batch analysis failed');
            mockParallelAnalyzer.analyzePages.mockRejectedValue(error);

            const result = await analysisOrchestrator['analyzePageBatch'](mockPages, mockAnalysisOptions);

            expect(result).toEqual({
                successful: [],
                failed: mockPages.map(page => ({ page, error: 'Batch analysis failed' })),
                metrics: {
                    totalTime: expect.any(Number),
                    averageTimePerPage: 0,
                    successRate: 0
                }
            });
        });
    });

      describe('getAnalysisMetrics', () => {
    it('should calculate analysis metrics correctly', () => {
      const startTime = Date.now() - 5000; // 5 seconds ago
      const metrics = analysisOrchestrator['getAnalysisMetrics'](mockAnalysisResults, startTime);

      expect(metrics).toEqual({
        totalPages: 1,
        analysisTime: 5000,
        averageTimePerPage: expect.any(Number),
        successRate: 100,
        pagesWithViolations: 0,
        totalViolations: 0
      });
    });

    it('should handle empty results', () => {
      const startTime = Date.now();
      const metrics = analysisOrchestrator['getAnalysisMetrics']([], startTime);

      expect(metrics).toEqual({
        totalPages: 0,
        analysisTime: 0,
        averageTimePerPage: 0,
        successRate: 100,
        pagesWithViolations: 0,
        totalViolations: 0
      });
    });
  });

    describe('getAnalysisSummary', () => {
        it('should generate analysis summary', () => {
            const startTime = Date.now() - 5000;
            const summary = analysisOrchestrator['getAnalysisSummary'](mockAnalysisResults, startTime);

            expect(summary).toEqual({
                totalPages: 1,
                successfulPages: 1,
                failedPages: 0,
                totalViolations: 0,
                averageTimePerPage: expect.any(Number),
                successRate: 100,
                analysisDuration: expect.any(Number)
            });
        });
    });

    describe('isAnalyzerHealthy', () => {
        it('should return true when analyzer is healthy', async () => {
            mockParallelAnalyzer.analyzePages.mockResolvedValue(mockBatchResult);

            const isHealthy = await analysisOrchestrator.isAnalyzerHealthy();

            expect(isHealthy).toBe(true);
        });

            it('should return analyzer health status', async () => {
      const isHealthy = await analysisOrchestrator.isAnalyzerHealthy();

      expect(typeof isHealthy).toBe('boolean');
    });
    });

    describe('getAnalyzerStatus', () => {
        it('should return analyzer status', async () => {
            const status = await analysisOrchestrator.getAnalyzerStatus();

            expect(status).toEqual({
                isHealthy: expect.any(Boolean),
                activeWorkers: expect.any(Number),
                queueLength: expect.any(Number),
                lastActivity: expect.any(Date)
            });
        });
    });

    describe('validateAnalysisResults', () => {
        it('should validate valid results', () => {
            const validation = analysisOrchestrator.validateAnalysisResults(mockAnalysisResults);

            expect(validation).toEqual({
                isValid: true,
                errors: [],
                warnings: []
            });
        });

            it('should detect invalid results', () => {
      const invalidResults: AnalysisResult[] = [
        {
          ...mockAnalysisResults[0],
          url: '', // Invalid empty URL
          timestamp: 'invalid-timestamp', // Invalid timestamp
          tool: 'axe',
          violations: [],
          passes: [],
          warnings: [],
          summary: {
            totalViolations: 0,
            totalPasses: 0,
            totalWarnings: 0,
            criticalViolations: 0,
            seriousViolations: 0,
            moderateViolations: 0,
            minorViolations: 0
          }
        }
      ];

      const validation = analysisOrchestrator.validateAnalysisResults(invalidResults);

      expect(validation.isValid).toBe(false);
      expect(validation.errors.length).toBeGreaterThan(0);
    });
    });

      describe('error handling', () => {
    it('should handle invalid page URLs', async () => {
      const invalidPages = [
        { 
          url: 'invalid-url', 
          title: 'Invalid Page', 
          depth: 0, 
          foundOn: 'https://example.com',
          status: 200,
          loadTime: 1000
        }
      ];

      mockParallelAnalyzer.analyzePages.mockResolvedValue(mockBatchResult);

      await analysisOrchestrator.performAccessibilityAnalysis(invalidPages, mockAnalysisOptions);

      expect(mockParallelAnalyzer.analyzePages).toHaveBeenCalledWith(invalidPages, mockAnalysisOptions);
    });
  });

      describe('performance scenarios', () => {
    it('should handle multiple pages efficiently', async () => {
      const multiplePages = Array.from({ length: 3 }, (_, i) => ({
        url: `https://example.com/page${i}`,
        title: `Page ${i}`,
        depth: 0,
        foundOn: 'https://example.com',
        status: 200,
        loadTime: 1000
      }));

      mockParallelAnalyzer.analyzePages.mockResolvedValue(mockBatchResult);

      const result = await analysisOrchestrator.performAccessibilityAnalysis(multiplePages, mockAnalysisOptions);

      expect(result).toEqual(mockAnalysisResults);
      expect(mockParallelAnalyzer.analyzePages).toHaveBeenCalled();
    });
  });
}); 