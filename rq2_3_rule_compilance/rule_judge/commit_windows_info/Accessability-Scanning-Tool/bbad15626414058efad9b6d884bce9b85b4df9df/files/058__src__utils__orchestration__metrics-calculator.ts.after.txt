import { PageInfo, AnalysisResult } from '@/core/types/common';

export interface WorkflowMetrics {
    totalTime: number;
    crawlTime: number;
    analysisTime: number;
    reportTime: number;
    successRate: number;
    pagesAnalyzed: number;
    violationsFound: number;
}

export interface ComplianceMetrics {
    totalPages: number;
    pagesWithViolations: number;
    compliancePercentage: number;
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    wcagAAViolations: number;
    wcagAAAViolations: number;
}

export interface ViolationPatterns {
    mostCommonViolations: Array<{
        id: string;
        description: string;
        impact: string;
        affectedPages: number;
        totalOccurrences: number;
    }>;
    violationsByType: Record<string, any>;
    violationCounts: Record<string, {
        count: number;
        pages: Set<string>;
        impact: string;
        description: string;
    }>;
}

export interface CrawlMetrics {
    totalPages: number;
    crawlTime: number;
    averageTimePerPage: number;
    successRate: number;
    pagesWithErrors: number;
}

export interface AnalysisMetrics {
    totalPages: number;
    analysisTime: number;
    averageTimePerPage: number;
    successRate: number;
    pagesWithViolations: number;
    totalViolations: number;
}

export interface ReportMetrics {
    reportTime: number;
    totalReports: number;
    databaseReports: number;
    pdfReports: number;
    averageReportSize: number;
    successRate: number;
}

/**
 * Utility class for calculating various metrics and performance indicators
 * Extracted from WorkflowOrchestrator to improve maintainability and testability
 */
export class MetricsCalculator {
    /**
     * Calculate overall workflow metrics from crawl and analysis results
     */
    calculateWorkflowMetrics(
        crawlResults: PageInfo[],
        analysisResults: AnalysisResult[],
        totalTime: number,
        crawlTime: number = 0,
        analysisTime: number = 0,
        reportTime: number = 0
    ): WorkflowMetrics {
        const totalViolations = analysisResults.reduce(
            (sum, result) => sum + result.summary.totalViolations,
            0
        );

        const successRate = crawlResults.length > 0
            ? (analysisResults.length / crawlResults.length) * 100
            : 0;

        return {
            totalTime,
            crawlTime,
            analysisTime,
            reportTime,
            successRate: Math.round(successRate * 100) / 100, // Round to 2 decimal places
            pagesAnalyzed: analysisResults.length,
            violationsFound: totalViolations,
        };
    }

    /**
     * Calculate compliance metrics from analysis results
     */
    calculateComplianceMetrics(analysisResults: AnalysisResult[]): ComplianceMetrics {
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

        const pagesWithViolations = analysisResults.filter(
            result => result.summary.totalViolations > 0
        ).length;

        const compliancePercentage = analysisResults.length > 0
            ? Math.round(((analysisResults.length - pagesWithViolations) / analysisResults.length) * 100)
            : 0;

        return {
            totalPages: analysisResults.length,
            pagesWithViolations,
            compliancePercentage,
            totalViolations,
            criticalViolations: totalCritical,
            seriousViolations: totalSerious,
            moderateViolations: totalModerate,
            minorViolations: totalMinor,
            wcagAAViolations: totalCritical + totalSerious,
            wcagAAAViolations: totalModerate + totalMinor,
        };
    }

    /**
     * Analyze violation patterns and identify most common issues
     */
    analyzeViolationPatterns(analysisResults: AnalysisResult[]): ViolationPatterns {
        const violationsByType: Record<string, any> = {};
        const violationCounts: Record<
            string,
            { count: number; pages: Set<string>; impact: string; description: string }
        > = {};

        // Process violations by type for detailed analysis
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
            mostCommonViolations,
            violationsByType,
            violationCounts,
        };
    }

    /**
     * Calculate crawl-specific metrics
     */
    calculateCrawlMetrics(results: PageInfo[], startTime: number): CrawlMetrics {
        const endTime = Date.now();
        const crawlTime = endTime - startTime;
        const pagesWithErrors = results.filter(page => page.status !== 200).length;
        const successRate = results.length > 0
            ? ((results.length - pagesWithErrors) / results.length) * 100
            : 0;

        return {
            totalPages: results.length,
            crawlTime,
            averageTimePerPage: results.length > 0 ? crawlTime / results.length : 0,
            successRate: Math.round(successRate * 100) / 100,
            pagesWithErrors,
        };
    }

    /**
     * Calculate analysis-specific metrics
     */
    calculateAnalysisMetrics(results: AnalysisResult[], startTime: number): AnalysisMetrics {
        const endTime = Date.now();
        const analysisTime = endTime - startTime;
        const totalViolations = results.reduce(
            (sum, result) => sum + result.summary.totalViolations,
            0
        );
        const pagesWithViolations = results.filter(
            result => result.summary.totalViolations > 0
        ).length;

        return {
            totalPages: results.length,
            analysisTime,
            averageTimePerPage: results.length > 0 ? analysisTime / results.length : 0,
            successRate: 100, // Analysis results are successful if they exist
            pagesWithViolations,
            totalViolations,
        };
    }

    /**
     * Calculate report generation metrics
     */
    calculateReportMetrics(startTime: number): ReportMetrics {
        const endTime = Date.now();
        const reportTime = endTime - startTime;

        return {
            reportTime,
            totalReports: 0, // Will be set by the orchestrator
            databaseReports: 0, // Will be set by the orchestrator
            pdfReports: 0, // Will be set by the orchestrator
            averageReportSize: 0, // Will be calculated based on actual reports
            successRate: 100, // Will be calculated based on actual success rate
        };
    }

    /**
     * Generate a human-readable performance report
     */
    generatePerformanceReport(metrics: WorkflowMetrics): string {
        const formatTime = (ms: number) => {
            if (ms < 1000) return `${ms}ms`;
            if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
            return `${(ms / 60000).toFixed(1)}m`;
        };

        return `
Performance Report:
==================
Total Time: ${formatTime(metrics.totalTime)}
├── Crawl Time: ${formatTime(metrics.crawlTime)}
├── Analysis Time: ${formatTime(metrics.analysisTime)}
└── Report Time: ${formatTime(metrics.reportTime)}

Pages Analyzed: ${metrics.pagesAnalyzed}
Success Rate: ${metrics.successRate.toFixed(1)}%
Violations Found: ${metrics.violationsFound}

Average Time per Page: ${formatTime(metrics.totalTime / metrics.pagesAnalyzed)}
`.trim();
    }

    /**
     * Generate a compliance summary report
     */
    generateComplianceReport(compliance: ComplianceMetrics): string {
        return `
Compliance Summary:
==================
Total Pages: ${compliance.totalPages}
Pages with Violations: ${compliance.pagesWithViolations}
Compliance Percentage: ${compliance.compliancePercentage}%

Violation Breakdown:
├── Critical: ${compliance.criticalViolations}
├── Serious: ${compliance.seriousViolations}
├── Moderate: ${compliance.moderateViolations}
└── Minor: ${compliance.minorViolations}

WCAG Compliance:
├── AA Level Violations: ${compliance.wcagAAViolations}
└── AAA Level Violations: ${compliance.wcagAAAViolations}
`.trim();
    }
} 