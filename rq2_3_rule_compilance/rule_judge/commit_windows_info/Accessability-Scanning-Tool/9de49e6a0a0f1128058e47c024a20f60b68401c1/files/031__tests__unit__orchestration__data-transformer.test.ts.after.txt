import { DataTransformer, WcagComplianceMatrix, ViolationAggregation, PdfReportData } from '@/utils/orchestration/data-transformer';
import { AnalysisResult, ProcessedViolation, SiteWideAccessibilityReport } from '@/core/types/common';

describe('DataTransformer', () => {
    let transformer: DataTransformer;

    beforeEach(() => {
        transformer = new DataTransformer();
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

    describe('convertAnalysisResultsToSiteWideReport', () => {
        it('should convert analysis results to site-wide report correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, violations),
                createMockAnalysisResult('https://example.com/page1', 0, [])
            ];

            const report = transformer.convertAnalysisResultsToSiteWideReport(
                analysisResults,
                'https://example.com',
                'WCAG2AA'
            );

            expect(report.siteUrl).toBe('https://example.com');
            expect(report.wcagLevel).toBe('WCAG2AA');
            expect(report.testSuite).toBe('Phase 2 Accessibility Testing');
            expect(report.summary.totalPages).toBe(2);
            expect(report.summary.pagesWithViolations).toBe(1);
            expect(report.summary.totalViolations).toBe(2);
            expect(report.summary.criticalViolations).toBe(1);
            expect(report.summary.seriousViolations).toBe(1);
            expect(report.pageReports).toHaveLength(2);
        });

        it('should handle empty analysis results', () => {
            const report = transformer.convertAnalysisResultsToSiteWideReport(
                [],
                'https://example.com',
                'WCAG2AAA'
            );

            expect(report.siteUrl).toBe('https://example.com');
            expect(report.wcagLevel).toBe('WCAG2AAA');
            expect(report.summary.totalPages).toBe(0);
            expect(report.summary.pagesWithViolations).toBe(0);
            expect(report.summary.totalViolations).toBe(0);
            expect(report.summary.compliancePercentage).toBe(100);
        });

        it('should use default WCAG level when not specified', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 0)
            ];

            const report = transformer.convertAnalysisResultsToSiteWideReport(
                analysisResults,
                'https://example.com'
            );

            expect(report.wcagLevel).toBe('WCAG2AA');
        });
    });

    describe('generateWcagComplianceMatrix', () => {
        it('should generate WCAG compliance matrix correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, violations)
            ];

            const matrix = transformer.generateWcagComplianceMatrix(analysisResults);

            expect(matrix).toBeDefined();
            expect(Object.keys(matrix).length).toBeGreaterThan(0);

            // Check that matrix contains expected WCAG criteria
            const criteriaKeys = Object.keys(matrix);
            expect(criteriaKeys.some(key => key.includes('color-contrast'))).toBe(true);
            expect(criteriaKeys.some(key => key.includes('missing-alt'))).toBe(true);
        });

        it('should handle empty analysis results', () => {
            const matrix = transformer.generateWcagComplianceMatrix([]);

            expect(matrix).toBeDefined();
            expect(Object.keys(matrix)).toHaveLength(0);
        });

        it('should handle analysis results with no violations', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 0)
            ];

            const matrix = transformer.generateWcagComplianceMatrix(analysisResults);

            expect(matrix).toBeDefined();
            // Should be empty when no violations exist
            expect(Object.keys(matrix)).toHaveLength(0);
        });
    });

    describe('aggregateViolations', () => {
        it('should aggregate violations correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, [violations[0]!, violations[2]!]),
                createMockAnalysisResult('https://example.com/page1', 1, [violations[1]!])
            ];

            const aggregation = transformer.aggregateViolations(analysisResults);

            expect(aggregation.mostCommonViolations).toHaveLength(2);
            expect(aggregation.mostCommonViolations[0]?.id).toBe('color-contrast');
            expect(aggregation.mostCommonViolations[0]?.totalOccurrences).toBe(2);
            expect(aggregation.mostCommonViolations[1]?.id).toBe('missing-alt');
            expect(aggregation.mostCommonViolations[1]?.totalOccurrences).toBe(1);
            expect(aggregation.violationsByType).toBeDefined();
        });

        it('should handle empty analysis results', () => {
            const aggregation = transformer.aggregateViolations([]);

            expect(aggregation.mostCommonViolations).toHaveLength(0);
            expect(Object.keys(aggregation.violationsByType)).toHaveLength(0);
        });
    });

    describe('transformForPdfGeneration', () => {
        it('should transform site-wide report for PDF generation', () => {
            const siteWideReport: SiteWideAccessibilityReport = {
                siteUrl: 'https://example.com',
                timestamp: new Date().toISOString(),
                testSuite: 'Phase 2 Accessibility Testing',
                wcagLevel: 'WCAG2AA',
                summary: {
                    totalPages: 2,
                    pagesWithViolations: 1,
                    totalViolations: 2,
                    criticalViolations: 1,
                    seriousViolations: 1,
                    moderateViolations: 0,
                    minorViolations: 0,
                    compliancePercentage: 50,
                    mostCommonViolations: []
                },
                pageReports: [
                    {
                        url: 'https://example.com',
                        timestamp: new Date().toISOString(),
                        testSuite: 'Phase 2 Accessibility Testing',
                        summary: { totalViolations: 2, criticalViolations: 1, seriousViolations: 1, moderateViolations: 0, minorViolations: 0, wcagAAViolations: 1, wcagAAAViolations: 1 },
                        violations: [],
                        pageAnalysis: {
                            title: 'Example Page',
                            headingStructure: [],
                            landmarks: { main: true, nav: false, footer: false },
                            skipLink: { exists: false, isVisible: false, targetExists: false },
                            images: [],
                            links: [],
                            forms: [],
                            keyboardNavigation: []
                        }
                    }
                ],
                violationsByType: {}
            };

            const pdfData = transformer.transformForPdfGeneration(siteWideReport);

            expect(pdfData.siteUrl).toBe('https://example.com');
            expect(pdfData.wcagLevel).toBe('WCAG2AA');
            expect(pdfData.totalPages).toBe(2);
            expect(pdfData.pagesAnalyzed).toBe(2);
            expect(pdfData.totalViolations).toBe(2);
            expect(pdfData.summary.totalPages).toBe(2);
            expect(pdfData.summary.pagesWithViolations).toBe(1);
            expect(pdfData.summary.totalViolations).toBe(2);
            expect(pdfData.pageAnalysis).toHaveLength(1);
            expect(pdfData.wcagComplianceMatrix).toBeDefined();
        });

        it('should handle site-wide report with empty data', () => {
            const siteWideReport: SiteWideAccessibilityReport = {
                siteUrl: 'https://example.com',
                timestamp: new Date().toISOString(),
                testSuite: 'Phase 2 Accessibility Testing',
                wcagLevel: 'WCAG2AA',
                summary: {
                    totalPages: 0,
                    pagesWithViolations: 0,
                    totalViolations: 0,
                    criticalViolations: 0,
                    seriousViolations: 0,
                    moderateViolations: 0,
                    minorViolations: 0,
                    compliancePercentage: 100,
                    mostCommonViolations: []
                },
                pageReports: [],
                violationsByType: {}
            };

            const pdfData = transformer.transformForPdfGeneration(siteWideReport);

            expect(pdfData.siteUrl).toBe('https://example.com');
            expect(pdfData.totalPages).toBe(0);
            expect(pdfData.pagesAnalyzed).toBe(0);
            expect(pdfData.totalViolations).toBe(0);
            expect(pdfData.summary.compliancePercentage).toBe(100);
            expect(pdfData.pageAnalysis).toHaveLength(0);
        });
    });

    describe('calculateCompliancePercentage', () => {
        it('should calculate compliance percentage correctly', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2),
                createMockAnalysisResult('https://example.com/page1', 0)
            ];

            const percentage = transformer.calculateCompliancePercentage(analysisResults);

            expect(percentage).toBe(50); // 1 out of 2 pages has violations
        });

        it('should return 100 for empty results', () => {
            const percentage = transformer.calculateCompliancePercentage([]);

            expect(percentage).toBe(100);
        });

        it('should return 100 for results with no violations', () => {
            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 0)
            ];

            const percentage = transformer.calculateCompliancePercentage(analysisResults);

            expect(percentage).toBe(100);
        });
    });

    describe('analyzeMostCommonViolations', () => {
        it('should analyze most common violations correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, [violations[0]!, violations[2]!]),
                createMockAnalysisResult('https://example.com/page1', 1, [violations[1]!])
            ];

            const commonViolations = transformer.analyzeMostCommonViolations(analysisResults);

            expect(commonViolations).toHaveLength(2);
            expect(commonViolations[0]?.id).toBe('color-contrast');
            expect(commonViolations[0]?.totalOccurrences).toBe(2);
            expect(commonViolations[1]?.id).toBe('missing-alt');
            expect(commonViolations[1]?.totalOccurrences).toBe(1);
        });

        it('should handle empty analysis results', () => {
            const commonViolations = transformer.analyzeMostCommonViolations([]);

            expect(commonViolations).toHaveLength(0);
        });
    });

    describe('createSummaryReport', () => {
        it('should create summary report correctly', () => {
            const violations: ProcessedViolation[] = [
                createMockViolation('color-contrast', 'serious'),
                createMockViolation('missing-alt', 'critical')
            ];

            const analysisResults: AnalysisResult[] = [
                createMockAnalysisResult('https://example.com', 2, violations)
            ];

            const summary = transformer.createSummaryReport(analysisResults, 'https://example.com');

            expect(summary.siteUrl).toBe('https://example.com');
            expect(summary.totalPages).toBe(1);
            expect(summary.totalViolations).toBe(2);
            expect(summary.compliancePercentage).toBe(0);
            expect(summary.criticalViolations).toBe(1);
            expect(summary.seriousViolations).toBe(1);
            expect(summary.moderateViolations).toBe(0);
            expect(summary.minorViolations).toBe(0);
            expect(summary.timestamp).toBeDefined();
        });

        it('should handle empty analysis results', () => {
            const summary = transformer.createSummaryReport([], 'https://example.com');

            expect(summary.siteUrl).toBe('https://example.com');
            expect(summary.totalPages).toBe(0);
            expect(summary.totalViolations).toBe(0);
            expect(summary.compliancePercentage).toBe(100);
            expect(summary.criticalViolations).toBe(0);
            expect(summary.seriousViolations).toBe(0);
            expect(summary.moderateViolations).toBe(0);
            expect(summary.minorViolations).toBe(0);
        });
    });
}); 