import { MetricsCalculator, WorkflowMetrics, ComplianceMetrics, ViolationPatterns, CrawlMetrics, AnalysisMetrics, ReportMetrics } from '@/utils/orchestration/metrics-calculator';
import { PageInfo, AnalysisResult, ProcessedViolation } from '@/core/types/common';

describe('MetricsCalculator', () => {
    let calculator: MetricsCalculator;

    beforeEach(() => {
        calculator = new MetricsCalculator();
    });

    // Helper function to create valid ProcessedViolation objects
    const createMockViolation = (id: string, impact: 'minor' | 'moderate' | 'serious' | 'critical'): ProcessedViolation => ({
        id,
        impact,
        description: `${id} issue`,
        help: `Fix ${id}`,
        helpUrl: 'https://example.com/help',
        wcagTags: ['1.1.1'],
        wcagLevel: 'A',
        occurrences: 1,
        tools: ['axe-core'],
        elements: [{
            html: `<div>${id}</div>`,
            target: { selector: 'div' },
            failureSummary: `${id} failure`,
            selector: 'div'
        }],
        scenarioRelevance: ['All users'],
        remediation: {
            priority: 'High',
            effort: 'Medium',
            suggestions: [`Fix ${id}`]
        }
    });

    // Helper function to create valid AnalysisResult objects
    const createMockAnalysisResult = (url: string, totalViolations: number, violations: ProcessedViolation[] = []): AnalysisResult => ({
        url,
        timestamp: new Date().toISOString(),
        tool: 'axe-core',
        violations,
        passes: [],
        warnings: [],
        summary: {
            totalViolations,
            totalPasses: 10,
            totalWarnings: 2,
            criticalViolations: violations.filter(v => v.impact === 'critical').length,
            seriousViolations: violations.filter(v => v.impact === 'serious').length,
            moderateViolations: violations.filter(v => v.impact === 'moderate').length,
            minorViolations: violations.filter(v => v.impact === 'minor').length
        }
    });

    // Helper function to create valid PageInfo objects
    const createMockPageInfo = (url: string, status: number, depth: number): PageInfo => ({
        url,
        title: `Page ${depth}`,
        depth,
        foundOn: 'https://example.com',
        status,
        loadTime: 1000
    });

    describe('calculateWorkflowMetrics', () => {
        it('should calculate workflow metrics correctly', () => {
            const crawlResults: PageInfo[] = [
                createMockPageInfo('https://example.com', 200, 0),
                createMockPageInfo('https://example.com/page1', 200, 1),
                createMockPageInfo('https://example.com/page2', 200, 1)
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 5),
                createMockAnalysisResult('https://example.com/page1', 3)
            ];

            const metrics = calculator.calculateWorkflowMetrics(
                crawlResults,
                analysisResults,
                1000, // totalTime
                300,  // crawlTime
                600,  // analysisTime
                100   // reportTime
            );

            expect(metrics).toEqual({
                totalTime: 1000,
                crawlTime: 300,
                analysisTime: 600,
                reportTime: 100,
                successRate: 66.67, // 2/3 * 100
                pagesAnalyzed: 2,
                violationsFound: 8 // 5 + 3
            });
        });

        it('should handle empty results', () => {
            const metrics = calculator.calculateWorkflowMetrics([], [], 0);

            expect(metrics).toEqual({
                totalTime: 0,
                crawlTime: 0,
                analysisTime: 0,
                reportTime: 0,
                successRate: 0,
                pagesAnalyzed: 0,
                violationsFound: 0
            });
        });

        it('should handle zero crawl results', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 5)
            ];

            const metrics = calculator.calculateWorkflowMetrics([], analysisResults, 1000);

            expect(metrics.successRate).toBe(0);
            expect(metrics.pagesAnalyzed).toBe(1);
        });
    });

    describe('calculateComplianceMetrics', () => {
        it('should calculate compliance metrics correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, [violations[0]!, violations[2]!]),
                createMockAnalysisResult('https://example.com/page1', 1, [violations[1]!]),
                createMockAnalysisResult('https://example.com/page2', 0, [])
            ];

            const compliance = calculator.calculateComplianceMetrics(analysisResults);

            expect(compliance).toEqual({
                totalPages: 3,
                pagesWithViolations: 2,
                compliancePercentage: 33.33, // 1/3 * 100
                totalViolations: 3,
                criticalViolations: 1,
                seriousViolations: 2,
                moderateViolations: 0,
                minorViolations: 0,
                wcagAAViolations: 2, // serious violations
                wcagAAAViolations: 1 // critical violations
            });
        });

        it('should handle empty analysis results', () => {
            const compliance = calculator.calculateComplianceMetrics([]);

            expect(compliance).toEqual({
                totalPages: 0,
                pagesWithViolations: 0,
                compliancePercentage: 100,
                totalViolations: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0,
                wcagAAViolations: 0,
                wcagAAAViolations: 0
            });
        });

        it('should handle pages with no violations', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 0)
            ];

            const compliance = calculator.calculateComplianceMetrics(analysisResults);

            expect(compliance.compliancePercentage).toBe(100);
            expect(compliance.pagesWithViolations).toBe(0);
        });
    });

    describe('analyzeViolationPatterns', () => {
        it('should analyze violation patterns correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

                  const analysisResults: AnalysisResult[] = [
        createMockAnalysisResult('https://example.com', 2, [violations[0]!, violations[2]!]),
        createMockAnalysisResult('https://example.com/page1', 1, [violations[1]!])
      ];

            const patterns = calculator.analyzeViolationPatterns(analysisResults);

            expect(patterns.mostCommonViolations).toHaveLength(2);
            expect(patterns.mostCommonViolations[0]?.id).toBe('color-contrast');
            expect(patterns.mostCommonViolations[0]?.totalOccurrences).toBe(2);
            expect(patterns.mostCommonViolations[1]?.id).toBe('missing-alt');
            expect(patterns.mostCommonViolations[1]?.totalOccurrences).toBe(1);

            expect(patterns.violationCounts['color-contrast']).toBeDefined();
            expect(patterns.violationCounts['color-contrast']?.count).toBe(2);
            expect(patterns.violationCounts['color-contrast']?.pages.size).toBe(2);
        });

        it('should handle empty analysis results', () => {
            const patterns = calculator.analyzeViolationPatterns([]);

            expect(patterns.mostCommonViolations).toHaveLength(0);
            expect(Object.keys(patterns.violationCounts)).toHaveLength(0);
        });
    });

    describe('calculateCrawlMetrics', () => {
        it('should calculate crawl metrics correctly', () => {
            const crawlResults: PageInfo[] = [
                createMockPageInfo('https://example.com', 200, 0),
                createMockPageInfo('https://example.com/page1', 200, 1),
                createMockPageInfo('https://example.com/page2', 404, 1)
            ];

            const startTime = Date.now() - 1000; // 1 second ago
            const metrics = calculator.calculateCrawlMetrics(crawlResults, startTime);

            expect(metrics.totalPages).toBe(3);
            expect(metrics.crawlTime).toBeGreaterThan(0);
            expect(metrics.averageTimePerPage).toBeGreaterThan(0);
            expect(metrics.successRate).toBe(66.67); // 2/3 * 100
            expect(metrics.pagesWithErrors).toBe(1);
        });

        it('should handle empty crawl results', () => {
            const startTime = Date.now();
            const metrics = calculator.calculateCrawlMetrics([], startTime);

            expect(metrics.totalPages).toBe(0);
            expect(metrics.crawlTime).toBe(0);
            expect(metrics.averageTimePerPage).toBe(0);
            expect(metrics.successRate).toBe(0);
            expect(metrics.pagesWithErrors).toBe(0);
        });
    });

    describe('calculateAnalysisMetrics', () => {
        it('should calculate analysis metrics correctly', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2),
                createMockAnalysisResult('https://example.com/page1', 0)
            ];

            const startTime = Date.now() - 1000; // 1 second ago
            const metrics = calculator.calculateAnalysisMetrics(analysisResults, startTime);

            expect(metrics.totalPages).toBe(2);
            expect(metrics.analysisTime).toBeGreaterThan(0);
            expect(metrics.averageTimePerPage).toBeGreaterThan(0);
            expect(metrics.successRate).toBe(100);
            expect(metrics.pagesWithViolations).toBe(1);
            expect(metrics.totalViolations).toBe(2);
        });

        it('should handle empty analysis results', () => {
            const startTime = Date.now();
            const metrics = calculator.calculateAnalysisMetrics([], startTime);

            expect(metrics.totalPages).toBe(0);
            expect(metrics.analysisTime).toBe(0);
            expect(metrics.averageTimePerPage).toBe(0);
            expect(metrics.successRate).toBe(100);
            expect(metrics.pagesWithViolations).toBe(0);
            expect(metrics.totalViolations).toBe(0);
        });
    });

    describe('calculateReportMetrics', () => {
        it('should calculate report metrics correctly', () => {
            const startTime = Date.now() - 1000; // 1 second ago
            const metrics = calculator.calculateReportMetrics(startTime);

            expect(metrics.reportTime).toBeGreaterThan(0);
            expect(metrics.totalReports).toBe(0);
            expect(metrics.databaseReports).toBe(0);
            expect(metrics.pdfReports).toBe(0);
            expect(metrics.averageReportSize).toBe(0);
            expect(metrics.successRate).toBe(100);
        });

        it('should handle zero report time', () => {
            const startTime = Date.now();
            const metrics = calculator.calculateReportMetrics(startTime);

            expect(metrics.reportTime).toBe(0);
        });
    });

    describe('generatePerformanceReport', () => {
        it('should generate performance report correctly', () => {
            const metrics: WorkflowMetrics = {
                totalTime: 5000,
                crawlTime: 2000,
                analysisTime: 2500,
                reportTime: 500,
                successRate: 85.5,
                pagesAnalyzed: 10,
                violationsFound: 25
            };

            const report = calculator.generatePerformanceReport(metrics);

            expect(report).toContain('Performance Report');
            expect(report).toContain('Total Time: 5.00s');
            expect(report).toContain('Crawl Time: 2.00s');
            expect(report).toContain('Analysis Time: 2.50s');
            expect(report).toContain('Report Time: 0.50s');
            expect(report).toContain('Success Rate: 85.50%');
            expect(report).toContain('Pages Analyzed: 10');
            expect(report).toContain('Violations Found: 25');
        });

        it('should handle zero times', () => {
            const metrics: WorkflowMetrics = {
                totalTime: 0,
                crawlTime: 0,
                analysisTime: 0,
                reportTime: 0,
                successRate: 0,
                pagesAnalyzed: 0,
                violationsFound: 0
            };

            const report = calculator.generatePerformanceReport(metrics);

            expect(report).toContain('Total Time: 0.00s');
            expect(report).toContain('Success Rate: 0.00%');
        });
    });

    describe('generateComplianceReport', () => {
        it('should generate compliance report correctly', () => {
            const compliance: ComplianceMetrics = {
                totalPages: 10,
                pagesWithViolations: 3,
                compliancePercentage: 70,
                totalViolations: 15,
                criticalViolations: 2,
                seriousViolations: 8,
                moderateViolations: 3,
                minorViolations: 2,
                wcagAAViolations: 10,
                wcagAAAViolations: 5
            };

            const report = calculator.generateComplianceReport(compliance);

            expect(report).toContain('Compliance Report');
            expect(report).toContain('Total Pages: 10');
            expect(report).toContain('Pages with Violations: 3');
            expect(report).toContain('Compliance Percentage: 70.00%');
            expect(report).toContain('Total Violations: 15');
            expect(report).toContain('Critical Violations: 2');
            expect(report).toContain('Serious Violations: 8');
            expect(report).toContain('Moderate Violations: 3');
            expect(report).toContain('Minor Violations: 2');
            expect(report).toContain('WCAG AA Violations: 10');
            expect(report).toContain('WCAG AAA Violations: 5');
        });

        it('should handle zero violations', () => {
            const compliance: ComplianceMetrics = {
                totalPages: 5,
                pagesWithViolations: 0,
                compliancePercentage: 100,
                totalViolations: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0,
                wcagAAViolations: 0,
                wcagAAAViolations: 0
            };

            const report = calculator.generateComplianceReport(compliance);

            expect(report).toContain('Compliance Percentage: 100.00%');
            expect(report).toContain('Total Violations: 0');
        });
    });
}); 