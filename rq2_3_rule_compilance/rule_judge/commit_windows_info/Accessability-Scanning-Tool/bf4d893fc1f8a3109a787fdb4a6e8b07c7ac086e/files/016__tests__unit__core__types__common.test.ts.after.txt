import { describe, it, expect } from '@jest/globals';
import {
    PageInfo,
    AnalysisResult,
    ServiceResult,
    ProcessedViolation,
    SiteWideAccessibilityReport,
    AccessibilityReport,
    AnalysisSummary
} from '@/core/types/common';

describe('Core Types', () => {
    describe('PageInfo', () => {
        it('should create valid PageInfo object', () => {
            const pageInfo: PageInfo = {
                url: 'https://example.com',
                title: 'Test Page',
                depth: 0,
                foundOn: 'https://example.com',
                status: 200,
                loadTime: 1000
            };

            expect(pageInfo.url).toBe('https://example.com');
            expect(pageInfo.title).toBe('Test Page');
            expect(pageInfo.depth).toBe(0);
            expect(pageInfo.foundOn).toBe('https://example.com');
            expect(pageInfo.status).toBe(200);
            expect(pageInfo.loadTime).toBe(1000);
        });

        it('should handle different HTTP status codes', () => {
            const statusCodes = [200, 301, 404, 500];

            statusCodes.forEach(status => {
                const pageInfo: PageInfo = {
                    url: 'https://example.com',
                    title: 'Test Page',
                    depth: 0,
                    foundOn: 'https://example.com',
                    status,
                    loadTime: 1000
                };

                expect(pageInfo.status).toBe(status);
            });
        });

        it('should handle different depth levels', () => {
            const depths = [0, 1, 2, 3, 4];

            depths.forEach(depth => {
                const pageInfo: PageInfo = {
                    url: 'https://example.com',
                    title: 'Test Page',
                    depth,
                    foundOn: 'https://example.com',
                    status: 200,
                    loadTime: 1000
                };

                expect(pageInfo.depth).toBe(depth);
            });
        });
    });

    describe('ProcessedViolation', () => {
        it('should create valid ProcessedViolation object', () => {
            const violation: ProcessedViolation = {
                id: 'color-contrast',
                impact: 'serious',
                description: 'Ensures the color contrast of elements meets WCAG 2 AA contrast ratio thresholds',
                help: 'Elements must meet minimum color contrast ratio requirements',
                helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/color-contrast',
                wcagTags: ['wcag2aa', 'wcag143'],
                wcagLevel: 'AA',
                occurrences: 1,
                browsers: ['chrome'],
                tools: ['axe-core'],
                elements: [
                    {
                        html: '<button class="btn">Submit</button>',
                        target: { selector: 'button.btn' },
                        failureSummary: 'Fix any of the following:\n  Element has insufficient color contrast of 2.51 (foreground color: #ffffff, background color: #f0f0f0, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1',
                        selector: 'button.btn'
                    }
                ],
                scenarioRelevance: ['keyboard', 'screen-reader'],
                remediation: {
                    priority: 'High',
                    effort: 'Medium',
                    suggestions: ['Increase color contrast ratio to 4.5:1 or higher']
                }
            };

            expect(violation.id).toBe('color-contrast');
            expect(violation.impact).toBe('serious');
            expect(violation.wcagTags).toContain('wcag2aa');
            expect(violation.elements).toHaveLength(1);
        });

        it('should handle different impact levels', () => {
            const impactLevels = ['minor', 'moderate', 'serious', 'critical'] as const;

            impactLevels.forEach(impact => {
                const violation: ProcessedViolation = {
                    id: 'test-violation',
                    impact,
                    description: 'Test violation',
                    help: 'Test help',
                    helpUrl: 'https://example.com',
                    wcagTags: ['test'],
                    wcagLevel: 'AA',
                    occurrences: 1,
                    tools: ['axe-core'],
                    elements: [],
                    scenarioRelevance: [],
                    remediation: {
                        priority: 'Medium',
                        effort: 'Low',
                        suggestions: []
                    }
                };

                expect(violation.impact).toBe(impact);
            });
        });
    });

    describe('AnalysisResult', () => {
        it('should create valid AnalysisResult object', () => {
            const analysisResult: AnalysisResult = {
                url: 'https://example.com',
                timestamp: '2024-01-01T00:00:00.000Z',
                tool: 'axe-core',
                violations: [
                    {
                        id: 'color-contrast',
                        impact: 'serious',
                        description: 'Color contrast violation',
                        help: 'Fix color contrast',
                        helpUrl: 'https://example.com',
                        wcagTags: ['wcag2aa'],
                        wcagLevel: 'AA',
                        occurrences: 1,
                        tools: ['axe-core'],
                        elements: [],
                        scenarioRelevance: [],
                        remediation: {
                            priority: 'High',
                            effort: 'Medium',
                            suggestions: []
                        }
                    }
                ],
                summary: {
                    totalViolations: 1,
                    criticalViolations: 0,
                    seriousViolations: 1,
                    moderateViolations: 0,
                    minorViolations: 0
                }
            };

            expect(analysisResult.url).toBe('https://example.com');
            expect(analysisResult.tool).toBe('axe-core');
            expect(analysisResult.violations).toHaveLength(1);
            expect(analysisResult.summary.totalViolations).toBe(1);
        });
    });

    describe('ServiceResult', () => {
        it('should create successful ServiceResult', () => {
            const data = { test: 'data' };
            const serviceResult: ServiceResult<typeof data> = {
                success: true,
                data,
                message: 'Operation successful',
                metadata: {}
            };

            expect(serviceResult.success).toBe(true);
            expect(serviceResult.data).toEqual(data);
            expect(serviceResult.message).toBe('Operation successful');
        });

        it('should create error ServiceResult', () => {
            const serviceResult: ServiceResult<null> = {
                success: false,
                error: new Error('Test error'),
                message: 'Operation failed',
                metadata: {}
            };

            expect(serviceResult.success).toBe(false);
            expect(serviceResult.error).toBeDefined();
            expect(serviceResult.error?.message).toBe('Test error');
        });

        it('should handle generic types correctly', () => {
            const stringResult: ServiceResult<string> = {
                success: true,
                data: 'test string',
                message: 'String operation',
                metadata: {}
            };

            const numberResult: ServiceResult<number> = {
                success: true,
                data: 42,
                message: 'Number operation',
                metadata: {}
            };

            const arrayResult: ServiceResult<string[]> = {
                success: true,
                data: ['item1', 'item2'],
                message: 'Array operation',
                metadata: {}
            };

            expect(typeof stringResult.data).toBe('string');
            expect(typeof numberResult.data).toBe('number');
            expect(Array.isArray(arrayResult.data)).toBe(true);
        });
    });

    describe('SiteWideAccessibilityReport', () => {
        it('should create valid SiteWideAccessibilityReport object', () => {
            const siteReport: SiteWideAccessibilityReport = {
                siteUrl: 'https://example.com',
                timestamp: '2024-01-01T00:00:00.000Z',
                testSuite: 'WCAG 2.1 AA',
                summary: {
                    totalPages: 10,
                    pagesWithViolations: 5,
                    totalViolations: 15,
                    criticalViolations: 2,
                    seriousViolations: 8,
                    moderateViolations: 3,
                    minorViolations: 2,
                    compliancePercentage: 75.0,
                    mostCommonViolations: [
                        {
                            id: 'color-contrast',
                            affectedPages: 8,
                            totalOccurrences: 12,
                            impact: 'serious',
                            description: 'Color contrast violation'
                        }
                    ]
                },
                pageReports: [],
                violationsByType: {
                    'color-contrast': {
                        count: 8,
                        pages: ['https://example.com/page1', 'https://example.com/page2'],
                        impact: 'serious',
                        description: 'Color contrast violation',
                        totalOccurrences: 12,
                        browsers: ['chrome'],
                        tools: ['axe-core']
                    }
                }
            };

            expect(siteReport.siteUrl).toBe('https://example.com');
            expect(siteReport.summary.totalPages).toBe(10);
            expect(siteReport.summary.compliancePercentage).toBe(75.0);
            expect(siteReport.summary.mostCommonViolations).toHaveLength(1);
        });

        it('should handle edge cases in summary calculations', () => {
            const edgeCaseReport: SiteWideAccessibilityReport = {
                siteUrl: 'https://example.com',
                timestamp: '2024-01-01T00:00:00.000Z',
                testSuite: 'WCAG 2.1 AA',
                summary: {
                    totalPages: 0,
                    pagesWithViolations: 0,
                    totalViolations: 0,
                    criticalViolations: 0,
                    seriousViolations: 0,
                    moderateViolations: 0,
                    minorViolations: 0,
                    compliancePercentage: 100.0,
                    mostCommonViolations: []
                },
                pageReports: [],
                violationsByType: {}
            };

            expect(edgeCaseReport.summary.totalPages).toBe(0);
            expect(edgeCaseReport.summary.compliancePercentage).toBe(100.0);
            expect(edgeCaseReport.summary.mostCommonViolations).toHaveLength(0);
        });
    });

    describe('Type validation', () => {
        it('should ensure required properties are present', () => {
            // This test ensures TypeScript compilation works correctly
            // and that all required properties are defined in the types

            const pageInfo: PageInfo = {
                url: 'https://example.com',
                title: 'Test Page',
                depth: 0,
                foundOn: 'https://example.com',
                status: 200,
                loadTime: 1000
            };

            const analysisResult: AnalysisResult = {
                url: 'https://example.com',
                timestamp: '2024-01-01T00:00:00.000Z',
                tool: 'axe-core',
                violations: [],
                summary: {
                    totalViolations: 0,
                    criticalViolations: 0,
                    seriousViolations: 0,
                    moderateViolations: 0,
                    minorViolations: 0
                }
            };

            const serviceResult: ServiceResult<AnalysisResult> = {
                success: true,
                data: analysisResult,
                message: 'Test result',
                metadata: {}
            };

            // If this compiles, the types are correctly defined
            expect(pageInfo).toBeDefined();
            expect(analysisResult).toBeDefined();
            expect(serviceResult).toBeDefined();
        });

        it('should handle optional properties correctly', () => {
            const violationWithOptional: ProcessedViolation = {
                id: 'test-violation',
                impact: 'minor',
                description: 'Test violation',
                help: 'Test help',
                helpUrl: 'https://example.com',
                wcagTags: ['test'],
                wcagLevel: 'AA',
                occurrences: 1,
                tools: ['axe-core'],
                elements: [],
                scenarioRelevance: [],
                remediation: {
                    priority: 'Medium',
                    effort: 'Low',
                    suggestions: []
                }
                // browsers is optional and can be omitted
            };

            expect(violationWithOptional.id).toBe('test-violation');
            expect(violationWithOptional.browsers).toBeUndefined();
        });
    });
}); 