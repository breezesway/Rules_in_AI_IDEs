import { ViolationProcessor, ProcessedViolation, MultiToolResults } from '@/utils/processors/violation-processor';
import { ServiceResult } from '@/core/types/common';

// Mock Playwright Page
const mockPage = {
    locator: jest.fn().mockReturnValue({
        first: jest.fn().mockReturnValue({
            boundingBox: jest.fn().mockResolvedValue({ x: 0, y: 0, width: 100, height: 50 }),
            evaluate: jest.fn().mockResolvedValue('/html/body/button')
        })
    }),
    screenshot: jest.fn().mockResolvedValue('base64-screenshot-data')
};

describe('ViolationProcessor', () => {
    let processor: ViolationProcessor;

    beforeEach(() => {
        jest.clearAllMocks();
        processor = new ViolationProcessor(mockPage as any);
    });

    describe('processMultiToolViolations', () => {
        test('should process axe violations successfully', async () => {
            const mockAxeResults = {
                axe: {
                    violations: [
                        {
                            id: 'color-contrast',
                            impact: 'serious',
                            description: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                            help: 'Elements must meet minimum color contrast ratio requirements',
                            helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/color-contrast',
                            tags: ['wcag2aa', 'wcag143'],
                            nodes: [
                                {
                                    html: '<button class="low-contrast">Submit</button>',
                                    target: ['button.low-contrast'],
                                    failureSummary: 'Fix any of the following:\n  Element has insufficient color contrast of 2.51 (foreground color: #ffffff, background color: #cccccc, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1'
                                }
                            ]
                        }
                    ]
                },
                pa11y: null
            };

            const result = await processor.processMultiToolViolations(mockAxeResults);

            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();
            expect(Array.isArray(result.data)).toBe(true);
            expect(result.data!.length).toBeGreaterThan(0);
        });

        test('should process pa11y issues successfully', async () => {
            const mockPa11yResults = {
                axe: null,
                pa11y: {
                    issues: [
                        {
                            code: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                            type: 'error',
                            typeCode: 1,
                            message: 'Images must have alternate text',
                            context: '<img src="image.jpg" alt="">',
                            selector: 'img[src="image.jpg"]',
                            runner: 'htmlcs'
                        }
                    ]
                }
            };

            const result = await processor.processMultiToolViolations(mockPa11yResults);

            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();
            expect(Array.isArray(result.data)).toBe(true);
            expect(result.data!.length).toBeGreaterThan(0);
        });

        test('should handle empty results', async () => {
            const emptyResults = {
                axe: null,
                pa11y: null
            };

            const result = await processor.processMultiToolViolations(emptyResults);

            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();
            expect(Array.isArray(result.data)).toBe(true);
            expect(result.data!.length).toBe(0);
        });

        test('should handle mixed results from both tools', async () => {
            const mixedResults = {
                axe: {
                    violations: [
                        {
                            id: 'color-contrast',
                            impact: 'serious',
                            description: 'Color contrast issue',
                            help: 'Fix color contrast',
                            helpUrl: 'https://example.com',
                            tags: ['wcag2aa'],
                            nodes: [
                                {
                                    html: '<button>Submit</button>',
                                    target: ['button'],
                                    failureSummary: 'Low contrast'
                                }
                            ]
                        }
                    ]
                },
                pa11y: {
                    issues: [
                        {
                            code: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                            type: 'error',
                            typeCode: 1,
                            message: 'Missing alt text',
                            context: '<img src="image.jpg">',
                            selector: 'img',
                            runner: 'htmlcs'
                        }
                    ]
                }
            };

            const result = await processor.processMultiToolViolations(mixedResults);

            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();
            expect(Array.isArray(result.data)).toBe(true);
            expect(result.data!.length).toBeGreaterThan(0);
        });

        test('should handle processing errors gracefully', async () => {
            // Mock a page that throws errors
            const errorPage = {
                locator: jest.fn().mockImplementation(() => {
                    throw new Error('Page error');
                })
            };

            const errorProcessor = new ViolationProcessor(errorPage as any);
            const mockResults = {
                axe: {
                    violations: [
                        {
                            id: 'test-violation',
                            impact: 'serious',
                            description: 'Test violation',
                            help: 'Test help',
                            helpUrl: 'https://example.com',
                            tags: ['wcag2aa'],
                            nodes: [
                                {
                                    html: '<div>test</div>',
                                    target: ['div'],
                                    failureSummary: 'Test failure'
                                }
                            ]
                        }
                    ]
                },
                pa11y: null
            };

            const result = await errorProcessor.processMultiToolViolations(mockResults);

            expect(result.success).toBe(false);
            expect(result.error).toBeDefined();
        });

        test('should respect screenshot capture setting', async () => {
            const mockResults = {
                axe: {
                    violations: [
                        {
                            id: 'color-contrast',
                            impact: 'serious',
                            description: 'Color contrast issue',
                            help: 'Fix color contrast',
                            helpUrl: 'https://example.com',
                            tags: ['wcag2aa'],
                            nodes: [
                                {
                                    html: '<button>Submit</button>',
                                    target: ['button'],
                                    failureSummary: 'Low contrast'
                                }
                            ]
                        }
                    ]
                },
                pa11y: null
            };

            // Test with screenshots enabled
            const resultWithScreenshots = await processor.processMultiToolViolations(mockResults, true);
            expect(resultWithScreenshots.success).toBe(true);

            // Test with screenshots disabled
            const resultWithoutScreenshots = await processor.processMultiToolViolations(mockResults, false);
            expect(resultWithoutScreenshots.success).toBe(true);
        });
    });

    describe('ProcessedViolation structure', () => {
        test('should create valid ProcessedViolation objects', async () => {
            const mockResults = {
                axe: {
                    violations: [
                        {
                            id: 'color-contrast',
                            impact: 'serious',
                            description: 'Color contrast issue',
                            help: 'Fix color contrast',
                            helpUrl: 'https://example.com',
                            tags: ['wcag2aa', 'wcag143'],
                            nodes: [
                                {
                                    html: '<button>Submit</button>',
                                    target: ['button'],
                                    failureSummary: 'Low contrast'
                                }
                            ]
                        }
                    ]
                },
                pa11y: null
            };

            const result = await processor.processMultiToolViolations(mockResults);

            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();

            if (result.data && result.data.length > 0) {
                const violation = result.data[0];

                // Check required properties
                expect(violation).toHaveProperty('id');
                expect(violation).toHaveProperty('impact');
                expect(violation).toHaveProperty('description');
                expect(violation).toHaveProperty('help');
                expect(violation).toHaveProperty('helpUrl');
                expect(violation).toHaveProperty('wcagTags');
                expect(violation).toHaveProperty('wcagLevel');
                expect(violation).toHaveProperty('occurrences');
                expect(violation).toHaveProperty('tools');
                expect(violation).toHaveProperty('elements');
                expect(violation).toHaveProperty('scenarioRelevance');
                expect(violation).toHaveProperty('remediation');

                // Check impact is valid
                expect(['minor', 'moderate', 'serious', 'critical']).toContain(violation.impact);

                // Check wcagLevel is valid
                expect(['A', 'AA', 'AAA', 'Unknown']).toContain(violation.wcagLevel);

                // Check tools array
                expect(Array.isArray(violation.tools)).toBe(true);
                expect(violation.tools.length).toBeGreaterThan(0);

                // Check elements array
                expect(Array.isArray(violation.elements)).toBe(true);
                expect(violation.elements.length).toBeGreaterThan(0);

                // Check remediation structure
                expect(violation.remediation).toHaveProperty('priority');
                expect(violation.remediation).toHaveProperty('effort');
                expect(violation.remediation).toHaveProperty('suggestions');
                expect(['High', 'Medium', 'Low']).toContain(violation.remediation.priority);
                expect(['Low', 'Medium', 'High']).toContain(violation.remediation.effort);
                expect(Array.isArray(violation.remediation.suggestions)).toBe(true);
            }
        });
    });

    describe('Error handling', () => {
        test('should handle null/undefined inputs', async () => {
            const nullResults = {
                axe: null,
                pa11y: null
            };

            const result = await processor.processMultiToolViolations(nullResults);
            expect(result.success).toBe(true);
            expect(result.data).toEqual([]);
        });

        test('should handle malformed violation data', async () => {
            const malformedResults = {
                axe: {
                    violations: [
                        {
                            id: 'test',
                            impact: 'serious',
                            description: 'Test',
                            help: 'Test',
                            helpUrl: 'https://example.com',
                            tags: [],
                            nodes: [] // Empty nodes
                        }
                    ]
                },
                pa11y: null
            };

            const result = await processor.processMultiToolViolations(malformedResults);
            expect(result.success).toBe(true);
            expect(result.data).toBeDefined();
        });
    });
}); 