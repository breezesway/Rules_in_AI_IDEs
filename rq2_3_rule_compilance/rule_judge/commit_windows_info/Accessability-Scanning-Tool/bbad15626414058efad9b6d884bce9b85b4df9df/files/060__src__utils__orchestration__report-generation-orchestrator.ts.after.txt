import { AnalysisResult, ServiceResult } from '@/core/types/common';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { DatabaseService } from '@/utils/services/database-service';
import { MetricsCalculator, ReportMetrics } from './metrics-calculator';

export interface ReportGenerationOptions {
    wcagLevel?: string;
    generatePdfReports?: boolean;
    generateDatabaseReports?: boolean;
    audience?: string;
    generateAll?: boolean;
}

export interface ScanMetadata {
    scanConfiguration?: {
        maxPages?: number;
        maxDepth?: number;
        maxConcurrency?: number;
        retryFailedPages?: boolean;
        generateReports?: boolean;
        wcagLevel?: string;
    };
    performanceMetrics?: {
        totalScanTime?: number;
        averageTimePerPage?: number;
        successRate?: number;
        pagesAnalyzed?: number;
        pagesWithViolations?: number;
    };
    toolsUsed?: string[];
    scanId?: string;
    scanType?: 'full-site' | 'single-page' | 'quick';
    userAgent?: string;
    crawlDepth?: number;
    excludedPatterns?: string[];
}

export interface ReportGenerationResult {
    reportPaths: string[];
    databaseIds: string[];
    pdfReports?: Array<{ filePath: string; audience: string; displayName: string; sizeKB: number }>;
    metrics: ReportMetrics;
}

/**
 * Orchestrator class for report generation operations
 * Extracted from WorkflowOrchestrator to improve maintainability and testability
 */
export class ReportGenerationOrchestrator {
    private errorHandler: ErrorHandlerService;
    private databaseService: DatabaseService;
    private metricsCalculator: MetricsCalculator;

    constructor(
        databaseService: DatabaseService,
        errorHandler: ErrorHandlerService
    ) {
        this.databaseService = databaseService;
        this.errorHandler = errorHandler;
        this.metricsCalculator = new MetricsCalculator();
    }

    /**
     * Generate comprehensive reports from analysis results
     */
    async generateReports(
        analysisResults: AnalysisResult[],
        targetUrl: string,
        options: ReportGenerationOptions = {},
        scanMetadata?: ScanMetadata
    ): Promise<ReportGenerationResult> {
        this.errorHandler.logInfo('Phase 3: Starting report generation', {
            analysisResults: analysisResults.length,
            targetUrl,
            wcagLevel: options.wcagLevel || 'WCAG2AA',
        });

        const startTime = Date.now();
        const reportPaths: string[] = [];
        const databaseIds: string[] = [];

        try {
            // Convert analysis results to site-wide report format
            const siteWideReport = this.convertAnalysisResultsToSiteWideReport(
                analysisResults,
                targetUrl,
                options.wcagLevel || 'WCAG2AA'
            );

            // Store reports in database if enabled
            if (options.generateDatabaseReports !== false) {
                const databaseResult = await this.storeReportsInDatabase(
                    analysisResults,
                    siteWideReport,
                    scanMetadata
                );
                reportPaths.push(...databaseResult.reportPaths);
                databaseIds.push(...databaseResult.databaseIds);
            }

            // Generate PDF reports if enabled
            let pdfReports: Array<{ filePath: string; audience: string; displayName: string; sizeKB: number }> | undefined;
            if (options.generatePdfReports) {
                const pdfResult = await this.generatePdfReports(
                    siteWideReport,
                    options,
                    scanMetadata
                );
                if (pdfResult.success && pdfResult.data) {
                    pdfReports = pdfResult.data;
                    reportPaths.push(...pdfReports.map(report => report.filePath));
                }
            }

            // Calculate report generation metrics
            const reportMetrics = this.getReportMetrics(startTime);

            this.errorHandler.logSuccess('Report generation completed', {
                totalReports: reportPaths.length,
                databaseReports: databaseIds.length,
                pdfReports: pdfReports?.length || 0,
                reportMetrics,
            });

                  const result: ReportGenerationResult = {
        reportPaths,
        databaseIds,
        metrics: reportMetrics,
      };

      if (pdfReports) {
        result.pdfReports = pdfReports;
      }

      return result;
        } catch (error) {
            this.errorHandler.logWarning(
                `Report generation failed: ${error instanceof Error ? error.message : error}`
            );
            this.errorHandler.handleError(error, 'Report generation failed');
            throw error;
        }
    }

    /**
     * Store reports in database
     */
    async storeReportsInDatabase(
        analysisResults: AnalysisResult[],
        siteWideReport: any,
        scanMetadata?: ScanMetadata
    ): Promise<{ reportPaths: string[]; databaseIds: string[] }> {
        const reportPaths: string[] = [];
        const databaseIds: string[] = [];

        try {
            // Initialize database service if not already initialized
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    throw new Error(`Failed to initialize database service: ${initResult.message}`);
                }
            }

            // Store individual page reports
            const pageReportIds: string[] = [];
            for (const analysisResult of analysisResults) {
                const pageReport = this.convertAnalysisResultToPageReport(analysisResult);
                const storePageResult = await this.databaseService.storeSinglePageReport(pageReport, scanMetadata);

                if (storePageResult.success && storePageResult.data) {
                    pageReportIds.push(storePageResult.data);
                    this.errorHandler.logSuccess(`Page report stored for ${analysisResult.url} with ID: ${storePageResult.data}`);
                } else {
                    this.errorHandler.logWarning(`Failed to store page report for ${analysisResult.url}`, {
                        error: storePageResult.message
                    });
                }
            }

            // Store the site-wide report
            const storeResult = await this.databaseService.storeSiteWideReport(siteWideReport, scanMetadata);
            if (storeResult.success && storeResult.data) {
                this.errorHandler.logSuccess(`Site-wide report stored in database with ID: ${storeResult.data}`);
                this.errorHandler.logSuccess(`Stored ${pageReportIds.length} individual page reports and 1 site-wide report`);

                // Add database record IDs to report paths for reference
                reportPaths.push(`db://site-wide:${storeResult.data}`);
                pageReportIds.forEach(id => reportPaths.push(`db://page:${id}`));

                databaseIds.push(storeResult.data, ...pageReportIds);
            } else {
                this.errorHandler.logWarning('Failed to store site-wide report in database', {
                    error: storeResult.message
                });
            }

            return { reportPaths, databaseIds };
        } catch (error) {
            this.errorHandler.handleError(error, 'Database report storage failed');
            throw error;
        }
    }

    /**
     * Generate PDF reports
     */
    async generatePdfReports(
        siteWideReport: any,
        options: ReportGenerationOptions,
        scanMetadata?: ScanMetadata
    ): Promise<ServiceResult<Array<{ filePath: string; audience: string; displayName: string; sizeKB: number }>>> {
        try {
            // This would integrate with the existing PDF generation system
            // For now, return a placeholder result
            this.errorHandler.logInfo('PDF report generation not yet implemented');

            return {
                success: true,
                data: [],
                message: 'PDF report generation placeholder'
            };
        } catch (error) {
            this.errorHandler.handleError(error, 'PDF report generation failed');
            return {
                success: false,
                message: error instanceof Error ? error.message : 'Unknown error'
            };
        }
    }

    /**
     * Convert analysis results to site-wide report format
     */
    convertAnalysisResultsToSiteWideReport(
        analysisResults: AnalysisResult[],
        targetUrl: string,
        wcagLevel: string = 'WCAG2AA'
    ): any {
        const timestamp = new Date().toISOString();
        const totalViolations = analysisResults.reduce(
            (sum, result) => sum + result.summary.totalViolations,
            0
        );
        const totalCritical = analysisResults.reduce(
            (sum, result) => sum + result.summary.criticalViolations,
            0
        );
        const totalSerious = analysisResults.reduce(
            (sum, result) => sum + result.summary.seriousViolations,
            0
        );
        const totalModerate = analysisResults.reduce(
            (sum, result) => sum + result.summary.moderateViolations,
            0
        );
        const totalMinor = analysisResults.reduce(
            (sum, result) => sum + result.summary.minorViolations,
            0
        );

        // Calculate detailed metrics
        const pagesWithViolations = analysisResults.filter(
            result => result.summary.totalViolations > 0
        ).length;
        const compliancePercentage =
            analysisResults.length > 0
                ? Math.round(
                    ((analysisResults.length - pagesWithViolations) / analysisResults.length) * 100
                )
                : 0;

        // Process violations by type for detailed analysis
        const violationsByType: Record<string, any> = {};
        const violationCounts: Record<
            string,
            { count: number; pages: Set<string>; impact: string; description: string }
        > = {};

        analysisResults.forEach(result => {
            result.violations?.forEach((violation: any) => {
                const violationId = violation.id || violation.code || 'unknown';

                if (!violationCounts[violationId]) {
                    violationCounts[violationId] = {
                        count: 0,
                        pages: new Set(),
                        impact: violation.impact || violation.type || 'moderate',
                        description:
                            violation.description || violation.message || `Accessibility issue: ${violationId}`,
                    };
                }

                violationCounts[violationId].count++;
                violationCounts[violationId].pages.add(result.url);

                if (!violationsByType[violationId]) {
                    violationsByType[violationId] = {
                        id: violationId,
                        description: violationCounts[violationId].description,
                        impact: violationCounts[violationId].impact,
                        pages: [],
                    };
                }
                violationsByType[violationId].pages.push(result.url);
            });
        });

        // Generate most common violations list
        const mostCommonViolations = Object.entries(violationCounts)
            .map(([id, data]) => ({
                id,
                description: data.description,
                impact: data.impact,
                affectedPages: data.pages.size,
                totalOccurrences: data.count,
            }))
            .sort((a, b) => b.totalOccurrences - a.totalOccurrences)
            .slice(0, 10);

        return {
            siteUrl: targetUrl,
            timestamp,
            scanDate: timestamp,
            testSuite: 'Phase 2 Accessibility Testing',
            wcagLevel: wcagLevel,
            totalPages: analysisResults.length,
            pagesAnalyzed: analysisResults.length,
            totalViolations,
            summary: {
                totalPages: analysisResults.length,
                pagesAnalyzed: analysisResults.length,
                pagesWithViolations,
                totalViolations,
                criticalViolations: totalCritical,
                seriousViolations: totalSerious,
                moderateViolations: totalModerate,
                minorViolations: totalMinor,
                compliancePercentage,
                wcagAAViolations: totalCritical + totalSerious,
                wcagAAAViolations: totalModerate + totalMinor,
            },
            violations: Object.values(violationsByType),
            mostCommonViolations,
            wcagComplianceMatrix: this.generateWcagComplianceMatrix(analysisResults),
            compliancePercentage,
        };
    }

    /**
     * Convert analysis result to page report format
     */
    convertAnalysisResultToPageReport(analysisResult: AnalysisResult): any {
        return {
            url: analysisResult.url,
            timestamp: analysisResult.timestamp,
            testSuite: analysisResult.tool || 'Accessibility Testing',
            summary: {
                ...analysisResult.summary,
                wcagAAViolations: analysisResult.summary.criticalViolations + analysisResult.summary.seriousViolations,
                wcagAAAViolations: analysisResult.summary.moderateViolations + analysisResult.summary.minorViolations
            },
            violations: analysisResult.violations || [],
            pageAnalysis: {
                title: analysisResult.url.split('/').pop() || analysisResult.url,
                headingStructure: [],
                landmarks: { main: false, nav: false, footer: false },
                skipLink: { exists: false, isVisible: false, targetExists: false },
                images: [],
                links: [],
                forms: [],
                keyboardNavigation: []
            }
        };
    }

    /**
     * Generate WCAG compliance matrix
     */
    private generateWcagComplianceMatrix(analysisResults: AnalysisResult[]): any {
        const matrix = {
            A: { compliant: 0, nonCompliant: 0, total: 0 },
            AA: { compliant: 0, nonCompliant: 0, total: 0 },
            AAA: { compliant: 0, nonCompliant: 0, total: 0 },
        };

        analysisResults.forEach(result => {
            const hasViolations = result.summary.totalViolations > 0;

            // Count by WCAG level based on violation severity
            if (result.summary.criticalViolations > 0 || result.summary.seriousViolations > 0) {
                matrix.AA.total++;
                if (hasViolations) {
                    matrix.AA.nonCompliant++;
                } else {
                    matrix.AA.compliant++;
                }
            }

            if (result.summary.moderateViolations > 0 || result.summary.minorViolations > 0) {
                matrix.AAA.total++;
                if (hasViolations) {
                    matrix.AAA.nonCompliant++;
                } else {
                    matrix.AAA.compliant++;
                }
            }
        });

        return matrix;
    }

    /**
     * Get report generation metrics
     */
    getReportMetrics(startTime: number): ReportMetrics {
        return this.metricsCalculator.calculateReportMetrics(startTime);
    }

    /**
     * Validate report generation results
     */
    validateReportGeneration(results: ReportGenerationResult): {
        isValid: boolean;
        errors: string[];
        warnings: string[];
    } {
        const errors: string[] = [];
        const warnings: string[] = [];

        // Check for empty results
        if (results.reportPaths.length === 0) {
            errors.push('No reports were generated');
        }

        // Check for database reports
        const databaseReports = results.reportPaths.filter(path => path.startsWith('db://'));
        if (databaseReports.length === 0) {
            warnings.push('No database reports were generated');
        }

        // Check for PDF reports
        if (results.pdfReports && results.pdfReports.length === 0) {
            warnings.push('No PDF reports were generated');
        }

        // Check for valid database IDs
        if (results.databaseIds.length === 0) {
            warnings.push('No database IDs were returned');
        }

        return {
            isValid: errors.length === 0,
            errors,
            warnings,
        };
    }

    /**
     * Clean up report generation resources
     */
    async cleanup(): Promise<void> {
        try {
            this.errorHandler.logInfo('Cleaning up report generation resources...');
            // Add any cleanup logic here
            this.errorHandler.logSuccess('Report generation cleanup completed');
        } catch (error) {
            this.errorHandler.handleError(error, 'Report generation cleanup failed');
            throw error;
        }
    }
} 