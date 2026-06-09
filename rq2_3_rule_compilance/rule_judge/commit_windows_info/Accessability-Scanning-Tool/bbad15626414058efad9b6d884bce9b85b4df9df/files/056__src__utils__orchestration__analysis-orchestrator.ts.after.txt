import { PageInfo, AnalysisResult, BatchResult } from '@/core/types/common';
import { ParallelAnalyzer } from '@/utils/orchestration/parallel-analyzer';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { MetricsCalculator, AnalysisMetrics } from './metrics-calculator';

export interface AnalysisOptions {
    maxConcurrency: number;
    retryFailedPages: boolean;
    batchSize?: number;
    delayBetweenBatches?: number;
}

export interface AnalysisSummary {
    totalPages: number;
    successfulPages: number;
    failedPages: number;
    totalViolations: number;
    averageTimePerPage: number;
    successRate: number;
    analysisDuration: number;
}

/**
 * Orchestrator class for accessibility analysis operations
 * Extracted from WorkflowOrchestrator to improve maintainability and testability
 */
export class AnalysisOrchestrator {
    private errorHandler: ErrorHandlerService;
    private parallelAnalyzer: ParallelAnalyzer;
    private metricsCalculator: MetricsCalculator;

    constructor(
        parallelAnalyzer: ParallelAnalyzer,
        errorHandler: ErrorHandlerService
    ) {
        this.parallelAnalyzer = parallelAnalyzer;
        this.errorHandler = errorHandler;
        this.metricsCalculator = new MetricsCalculator();
    }

    /**
     * Perform accessibility analysis on a list of pages
     */
    async performAccessibilityAnalysis(
        pages: PageInfo[],
        options: AnalysisOptions
    ): Promise<AnalysisResult[]> {
        this.errorHandler.logInfo('Phase 2: Starting accessibility analysis', {
            totalPages: pages.length,
            maxConcurrency: options.maxConcurrency,
        });

        const startTime = Date.now();

        try {
            const analysisResults: AnalysisResult[] = [];
            const batchSize = options.batchSize || 10;

            // Process pages in batches
            for (let i = 0; i < pages.length; i += batchSize) {
                const batch = pages.slice(i, i + batchSize);
                const batchNumber = Math.floor(i / batchSize) + 1;

                this.errorHandler.logInfo(
                    `Starting analysis batch: ${batchNumber}, batch size: ${batch.length}`
                );

                const batchResult = await this.analyzePageBatch(batch, options);

                this.errorHandler.logInfo(
                    `Batch analysis complete: ${batchNumber}, successful: ${batchResult.successful.length}, failed: ${batchResult.failed.length}`
                );

                analysisResults.push(...batchResult.successful);

                // Retry failed pages if enabled
                if (options.retryFailedPages && batchResult.failed.length > 0) {
                    const failedPages = batchResult.failed.map(f => f.page);
                    this.errorHandler.logWarning('Retrying failed pages from previous batch', {
                        failedPages: failedPages.map(p => p.url),
                    });

                    const retryResult = await this.analyzePageBatch(failedPages, {
                        ...options,
                        retryFailedPages: false, // Only retry failed ones
                    });

                    analysisResults.push(...retryResult.successful);
                }

                // Add delay between batches if specified
                if (options.delayBetweenBatches && i + batchSize < pages.length) {
                    await new Promise(resolve => setTimeout(resolve, options.delayBetweenBatches));
                }
            }

            // Calculate analysis metrics
            const analysisMetrics = this.getAnalysisMetrics(analysisResults, startTime);

            this.errorHandler.logSuccess('Accessibility analysis completed', {
                totalPages: pages.length,
                successfulPages: analysisResults.length,
                failedPages: pages.length - analysisResults.length,
                analysisMetrics,
            });

            return analysisResults;
        } catch (error) {
            this.errorHandler.logWarning(
                `Accessibility analysis failed: ${error instanceof Error ? error.message : error}`
            );
            this.errorHandler.handleError(error, 'Accessibility analysis failed');
            throw error;
        }
    }

    /**
 * Analyze a batch of pages
 */
    async analyzePageBatch(
        batch: PageInfo[],
        options: AnalysisOptions
    ): Promise<BatchResult> {
        try {
            const parallelOptions: any = {
                maxConcurrency: options.maxConcurrency,
                retryFailedPages: options.retryFailedPages,
            };

            // Only add optional properties if they are defined
            if (options.batchSize !== undefined) {
                parallelOptions.batchSize = options.batchSize;
            }
            if (options.delayBetweenBatches !== undefined) {
                parallelOptions.delayBetweenBatches = options.delayBetweenBatches;
            }

            return await this.parallelAnalyzer.analyzePages(batch, parallelOptions);
        } catch (error) {
            this.errorHandler.logWarning('Batch analysis failed', {
                batchSize: batch.length,
                error: error instanceof Error ? error.message : error,
            });

            // Return empty batch result on failure
            return {
                successful: [],
                failed: batch.map(page => ({ page, error: 'Batch analysis failed' })),
                metrics: {
                    totalTime: 0,
                    averageTimePerPage: 0,
                    successRate: 0,
                },
            };
        }
    }

    /**
     * Get analysis-specific metrics
     */
    getAnalysisMetrics(results: AnalysisResult[], startTime: number): AnalysisMetrics {
        return this.metricsCalculator.calculateAnalysisMetrics(results, startTime);
    }

    /**
     * Get a comprehensive analysis summary
     */
    getAnalysisSummary(results: AnalysisResult[], startTime: number): AnalysisSummary {
        const analysisMetrics = this.getAnalysisMetrics(results, startTime);
        const totalViolations = results.reduce(
            (sum, result) => sum + result.summary.totalViolations,
            0
        );

        return {
            totalPages: results.length,
            successfulPages: results.length,
            failedPages: 0, // Failed pages are not in results
            totalViolations,
            averageTimePerPage: analysisMetrics.averageTimePerPage,
            successRate: analysisMetrics.successRate,
            analysisDuration: analysisMetrics.analysisTime,
        };
    }

    /**
     * Check if the parallel analyzer is healthy
     */
    async isAnalyzerHealthy(): Promise<boolean> {
        try {
            // This would depend on the ParallelAnalyzer implementation
            // For now, we'll assume it's healthy if we can create it
            return true;
        } catch (error) {
            this.errorHandler.logWarning('Analyzer health check failed', { error });
            return false;
        }
    }

    /**
     * Get analyzer status information
     */
    async getAnalyzerStatus(): Promise<{
        isHealthy: boolean;
        activeWorkers: number;
        queueLength: number;
        lastActivity: Date;
    }> {
        try {
            // This would depend on the ParallelAnalyzer implementation
            // For now, return basic status
            return {
                isHealthy: true,
                activeWorkers: 0,
                queueLength: 0,
                lastActivity: new Date(),
            };
        } catch (error) {
            this.errorHandler.logWarning('Failed to get analyzer status', { error });
            return {
                isHealthy: false,
                activeWorkers: 0,
                queueLength: 0,
                lastActivity: new Date(),
            };
        }
    }

    /**
     * Validate analysis results
     */
    validateAnalysisResults(results: AnalysisResult[]): {
        isValid: boolean;
        errors: string[];
        warnings: string[];
    } {
        const errors: string[] = [];
        const warnings: string[] = [];

        // Check for empty results
        if (results.length === 0) {
            errors.push('No analysis results generated');
        }

        // Check for results with missing violations array
        const resultsWithoutViolations = results.filter(result => !result.violations);
        if (resultsWithoutViolations.length > 0) {
            warnings.push(`${resultsWithoutViolations.length} results have missing violations array`);
        }

        // Check for results with missing summary
        const resultsWithoutSummary = results.filter(result => !result.summary);
        if (resultsWithoutSummary.length > 0) {
            warnings.push(`${resultsWithoutSummary.length} results have missing summary`);
        }

        // Check for results with missing timestamps
        const resultsWithoutTimestamp = results.filter(result => !result.timestamp);
        if (resultsWithoutTimestamp.length > 0) {
            warnings.push(`${resultsWithoutTimestamp.length} results have missing timestamps`);
        }

        // Check for results with missing URLs
        const resultsWithoutUrl = results.filter(result => !result.url);
        if (resultsWithoutUrl.length > 0) {
            errors.push(`${resultsWithoutUrl.length} results have missing URLs`);
        }

        return {
            isValid: errors.length === 0,
            errors,
            warnings,
        };
    }
} 