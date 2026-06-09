import { AnalysisResult, SiteWideAccessibilityReport } from '@/core/types/common';
import { MetricsCalculator, ComplianceMetrics, ViolationPatterns } from './metrics-calculator';

export interface WcagComplianceMatrix {
  [criterion: string]: {
    status: 'pass' | 'fail' | 'not-assessed';
    description: string;
    violations: number;
    pages: string[];
  };
}

export interface ViolationAggregation {
  violationsByType: Record<string, any>;
  mostCommonViolations: Array<{
    id: string;
    description: string;
    impact: string;
    affectedPages: number;
    totalOccurrences: number;
  }>;
}

export interface PdfReportData {
  siteUrl: string;
  timestamp: string;
  scanDate: string;
  testSuite: string;
  wcagLevel: string;
  totalPages: number;
  pagesAnalyzed: number;
  totalViolations: number;
  summary: {
    totalPages: number;
    pagesAnalyzed: number;
    pagesWithViolations: number;
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    compliancePercentage: number;
    wcagAAViolations: number;
    wcagAAAViolations: number;
    mostCommonViolations: any[];
  };
  violationsByType: Record<string, any>;
  mostCommonViolations: any[];
  overallSummary: {
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    compliancePercentage: number;
  };
  pageAnalysis: Array<{
    url: string;
    title: string;
    timestamp: string;
    violations: any[];
    summary: any;
    tool: string;
  }>;
  wcagComplianceMatrix: WcagComplianceMatrix;
}

/**
 * Utility class for transforming and aggregating data for reports
 * Extracted from WorkflowOrchestrator to improve maintainability and testability
 */
export class DataTransformer {
  private metricsCalculator: MetricsCalculator;

  constructor() {
    this.metricsCalculator = new MetricsCalculator();
  }

  /**
* Convert analysis results to site-wide report format
*/
  convertAnalysisResultsToSiteWideReport(
    analysisResults: AnalysisResult[],
    targetUrl: string,
    wcagLevel: string = 'WCAG2AA'
  ): SiteWideAccessibilityReport {
    const timestamp = new Date().toISOString();

    // Calculate compliance metrics
    const complianceMetrics = this.metricsCalculator.calculateComplianceMetrics(analysisResults);

    // Analyze violation patterns
    const violationPatterns = this.metricsCalculator.analyzeViolationPatterns(analysisResults);

    return {
      siteUrl: targetUrl,
      timestamp,
      testSuite: 'Phase 2 Accessibility Testing',
      wcagLevel: wcagLevel,
      summary: {
        totalPages: analysisResults.length,
        pagesWithViolations: complianceMetrics.pagesWithViolations,
        totalViolations: complianceMetrics.totalViolations,
        criticalViolations: complianceMetrics.criticalViolations,
        seriousViolations: complianceMetrics.seriousViolations,
        moderateViolations: complianceMetrics.moderateViolations,
        minorViolations: complianceMetrics.minorViolations,
        compliancePercentage: complianceMetrics.compliancePercentage,
        mostCommonViolations: violationPatterns.mostCommonViolations,
      },
      pageReports: analysisResults.map(result => ({
        url: result.url,
        timestamp: result.timestamp,
        testSuite: 'Phase 2 Accessibility Testing',
        summary: {
          totalViolations: result.summary.totalViolations,
          criticalViolations: result.summary.criticalViolations,
          seriousViolations: result.summary.seriousViolations,
          moderateViolations: result.summary.moderateViolations,
          minorViolations: result.summary.minorViolations,
          wcagAAViolations: result.summary.criticalViolations + result.summary.seriousViolations,
          wcagAAAViolations: result.summary.moderateViolations + result.summary.minorViolations,
        },
        violations: result.violations || [],
        pageAnalysis: {
          title: result.url.split('/').pop() || result.url,
          headingStructure: [],
          landmarks: { main: false, nav: false, footer: false },
          skipLink: { exists: false, isVisible: false, targetExists: false },
          images: [],
          links: [],
          forms: [],
          keyboardNavigation: [],
        },
      })),
      violationsByType: violationPatterns.violationsByType,
    };
  }

  /**
   * Generate WCAG compliance matrix from analysis results
   */
      generateWcagComplianceMatrix(analysisResults: AnalysisResult[]): WcagComplianceMatrix {
        const matrix: WcagComplianceMatrix = {};

        // Return empty matrix for empty results
        if (analysisResults.length === 0) {
            return matrix;
        }

        // Collect all unique violation types
        const violationTypes = new Set<string>();
        analysisResults.forEach(result => {
            result.violations?.forEach((violation: any) => {
                violationTypes.add(violation.id || violation.code || 'unknown');
            });
        });

        // Initialize matrix with violation types
        violationTypes.forEach(violationType => {
            matrix[violationType] = {
                status: 'not-assessed',
                description: `Violation: ${violationType}`,
                violations: 0,
                pages: [],
            };
        });

        // Analyze violations and update matrix
        analysisResults.forEach(result => {
            result.violations?.forEach((violation: any) => {
                const violationType = violation.id || violation.code || 'unknown';
                
                if (matrix[violationType]) {
                    matrix[violationType].violations++;
                    if (!matrix[violationType].pages.includes(result.url)) {
                        matrix[violationType].pages.push(result.url);
                    }
                    matrix[violationType].status = 'fail';
                }
            });
        });

        // Mark violation types as pass if no violations found
        Object.keys(matrix).forEach(violationType => {
            const violationData = matrix[violationType];
            if (violationData && violationData.violations === 0) {
                violationData.status = 'pass';
            }
        });

        return matrix;
    }

  /**
   * Extract WCAG criteria from violation data
   */
  private extractWcagCriteria(violation: any): string[] {
    const criteria: string[] = [];

    // Check various possible locations for WCAG criteria
    if (violation.wcag) {
      criteria.push(...violation.wcag);
    }
    if (violation.criteria) {
      criteria.push(...violation.criteria);
    }
    if (violation.wcagTags) {
      criteria.push(...violation.wcagTags);
    }
    if (violation.tags) {
      const wcagTags = violation.tags.filter((tag: string) =>
        /^\d+\.\d+\.\d+$/.test(tag)
      );
      criteria.push(...wcagTags);
    }

    return criteria;
  }

  /**
   * Aggregate violations by type and frequency
   */
  aggregateViolations(analysisResults: AnalysisResult[]): ViolationAggregation {
    const violationPatterns = this.metricsCalculator.analyzeViolationPatterns(analysisResults);

    return {
      violationsByType: violationPatterns.violationsByType,
      mostCommonViolations: violationPatterns.mostCommonViolations,
    };
  }

  /**
* Transform data specifically for PDF generation
*/
  transformForPdfGeneration(siteWideReport: SiteWideAccessibilityReport): PdfReportData {
    return {
      siteUrl: siteWideReport.siteUrl,
      timestamp: siteWideReport.timestamp,
      scanDate: siteWideReport.timestamp, // Use timestamp as scanDate
      testSuite: siteWideReport.testSuite,
      wcagLevel: siteWideReport.wcagLevel || 'WCAG2AA',
      totalPages: siteWideReport.summary.totalPages,
      pagesAnalyzed: siteWideReport.summary.totalPages,
      totalViolations: siteWideReport.summary.totalViolations,
      summary: {
        totalPages: siteWideReport.summary.totalPages,
        pagesAnalyzed: siteWideReport.summary.totalPages,
        pagesWithViolations: siteWideReport.summary.pagesWithViolations,
        totalViolations: siteWideReport.summary.totalViolations,
        criticalViolations: siteWideReport.summary.criticalViolations,
        seriousViolations: siteWideReport.summary.seriousViolations,
        moderateViolations: siteWideReport.summary.moderateViolations,
        minorViolations: siteWideReport.summary.minorViolations,
        compliancePercentage: siteWideReport.summary.compliancePercentage,
        wcagAAViolations: siteWideReport.summary.criticalViolations + siteWideReport.summary.seriousViolations,
        wcagAAAViolations: siteWideReport.summary.moderateViolations + siteWideReport.summary.minorViolations,
        mostCommonViolations: siteWideReport.summary.mostCommonViolations,
      },
      violationsByType: siteWideReport.violationsByType,
      mostCommonViolations: siteWideReport.summary.mostCommonViolations,
      overallSummary: {
        totalViolations: siteWideReport.summary.totalViolations,
        criticalViolations: siteWideReport.summary.criticalViolations,
        seriousViolations: siteWideReport.summary.seriousViolations,
        moderateViolations: siteWideReport.summary.moderateViolations,
        minorViolations: siteWideReport.summary.minorViolations,
        compliancePercentage: siteWideReport.summary.compliancePercentage,
      },
      pageAnalysis: siteWideReport.pageReports.map(report => ({
        url: report.url,
        title: report.pageAnalysis.title,
        timestamp: report.timestamp,
        violations: report.violations,
        summary: report.summary,
        tool: 'combined',
      })),
      wcagComplianceMatrix: this.generateWcagComplianceMatrix(siteWideReport.pageReports.map(r => ({
        url: r.url,
        timestamp: r.timestamp,
        tool: 'combined',
        violations: r.violations,
        passes: [],
        warnings: [],
        summary: {
          totalViolations: r.summary.totalViolations,
          totalPasses: 0,
          totalWarnings: 0,
          criticalViolations: r.summary.criticalViolations,
          seriousViolations: r.summary.seriousViolations,
          moderateViolations: r.summary.moderateViolations,
          minorViolations: r.summary.minorViolations,
        },
      }))),
    };
  }

  /**
   * Calculate compliance percentage from analysis results
   */
  calculateCompliancePercentage(analysisResults: AnalysisResult[]): number {
    const pagesWithViolations = analysisResults.filter(
      result => result.summary.totalViolations > 0
    ).length;

    return analysisResults.length > 0
      ? Math.round(((analysisResults.length - pagesWithViolations) / analysisResults.length) * 100)
      : 100;
  }

  /**
   * Analyze most common violations from analysis results
   */
  analyzeMostCommonViolations(analysisResults: AnalysisResult[]): any[] {
    const violationPatterns = this.metricsCalculator.analyzeViolationPatterns(analysisResults);
    return violationPatterns.mostCommonViolations;
  }

  /**
   * Create a simplified summary for quick reporting
   */
  createSummaryReport(analysisResults: AnalysisResult[], targetUrl: string): {
    siteUrl: string;
    timestamp: string;
    totalPages: number;
    totalViolations: number;
    compliancePercentage: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
  } {
    const complianceMetrics = this.metricsCalculator.calculateComplianceMetrics(analysisResults);

    return {
      siteUrl: targetUrl,
      timestamp: new Date().toISOString(),
      totalPages: complianceMetrics.totalPages,
      totalViolations: complianceMetrics.totalViolations,
      compliancePercentage: complianceMetrics.compliancePercentage,
      criticalViolations: complianceMetrics.criticalViolations,
      seriousViolations: complianceMetrics.seriousViolations,
      moderateViolations: complianceMetrics.moderateViolations,
      minorViolations: complianceMetrics.minorViolations,
    };
  }
} 