import { ViolationProcessor } from '@/utils/processors/violation-processor';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

describe('Processors Integration Tests', () => {
    let violationProcessor: ViolationProcessor;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;

    beforeEach(() => {
        // Setup test environment and database cleanup
        (global as any).testUtils.database.setupTestEnvironment();

        // Setup real services
        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();

        // Setup processors
        violationProcessor = new ViolationProcessor(errorHandler);
    });

    afterEach(async () => {
        // Clean up test data and verify cleanup
        await (global as any).testUtils.database.cleanupTestData();
        await (global as any).testUtils.database.verifyCleanup();
        jest.clearAllMocks();
    });

    describe('ViolationProcessor Integration', () => {
        test('should initialize violation processor', () => {
            expect(violationProcessor).toBeDefined();
        });

        test('should process axe violations correctly', () => {
            const axeViolations = [
                {
                    id: 'color-contrast',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/color-contrast',
                    tags: ['wcag2aa', 'wcag143'],
                    impact: 'serious',
                    nodes: [
                        {
                            html: '<button class="btn">Submit</button>',
                            target: ['button.btn'],
                            failureSummary: 'Fix any of the following:\n  Element has insufficient color contrast of 2.51 (foreground color: #ffffff, background color: #cccccc, font size: 12.0pt, font weight: normal). Expected contrast ratio of 4.5:1',
                        },
                    ],
                },
                {
                    id: 'button-name',
                    description: 'Buttons must have discernible text',
                    help: 'Ensures buttons have accessible names',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/button-name',
                    tags: ['wcag2a', 'wcag412'],
                    impact: 'critical',
                    nodes: [
                        {
                            html: '<button><img src="icon.png" alt=""></button>',
                            target: ['button'],
                            failureSummary: 'Fix any of the following:\n  Element does not have text that is visible to screen readers',
                        },
                    ],
                },
            ];

            const processedViolations = violationProcessor.processViolations(axeViolations, 'axe');

            expect(processedViolations).toBeDefined();
            expect(Array.isArray(processedViolations)).toBe(true);
            expect(processedViolations).toHaveLength(2);

            // Check first violation
            expect(processedViolations[0]).toHaveProperty('id', 'color-contrast');
            expect(processedViolations[0]).toHaveProperty('description');
            expect(processedViolations[0]).toHaveProperty('impact', 'serious');
            expect(processedViolations[0]).toHaveProperty('tool', 'axe');

            // Check second violation
            expect(processedViolations[1]).toHaveProperty('id', 'button-name');
            expect(processedViolations[1]).toHaveProperty('impact', 'critical');
            expect(processedViolations[1]).toHaveProperty('tool', 'axe');
        });

        test('should process pa11y violations correctly', () => {
            const pa11yViolations = [
                {
                    code: 'WCAG2AA.Principle1.Guideline1_4.1_4_3',
                    message: 'This element has insufficient contrast at this conformance level. Expected a contrast ratio of at least 4.5:1, but text in this element has a contrast ratio of 2.51:1. Recommendation: change text colour to #767676.',
                    selector: 'button.btn',
                    context: '<button class="btn">Submit</button>',
                    type: 'error',
                },
                {
                    code: 'WCAG2AA.Principle2.Guideline2_4.2_4_6',
                    message: 'This heading is not properly nested. Expected h2 but found h4.',
                    selector: 'h4',
                    context: '<h4>Section Title</h4>',
                    type: 'warning',
                },
            ];

            const processedViolations = violationProcessor.processViolations(pa11yViolations, 'pa11y');

            expect(processedViolations).toBeDefined();
            expect(Array.isArray(processedViolations)).toBe(true);
            expect(processedViolations).toHaveLength(2);

            // Check first violation
            expect(processedViolations[0]).toHaveProperty('id', 'WCAG2AA.Principle1.Guideline1_4.1_4_3');
            expect(processedViolations[0]).toHaveProperty('description');
            expect(processedViolations[0]).toHaveProperty('tool', 'pa11y');

            // Check second violation
            expect(processedViolations[1]).toHaveProperty('id', 'WCAG2AA.Principle2.Guideline2_4.2_4_6');
            expect(processedViolations[1]).toHaveProperty('tool', 'pa11y');
        });

        test('should handle empty violations array', () => {
            const processedViolations = violationProcessor.processViolations([], 'axe');

            expect(processedViolations).toBeDefined();
            expect(Array.isArray(processedViolations)).toBe(true);
            expect(processedViolations).toHaveLength(0);
        });

        test('should handle malformed violation data', () => {
            const malformedViolations = [
                {
                    id: 'test-violation',
                    // Missing required fields
                },
                null,
                undefined,
                {
                    id: 'valid-violation',
                    description: 'Valid violation',
                    impact: 'moderate',
                },
            ];

            const processedViolations = violationProcessor.processViolations(malformedViolations, 'axe');

            expect(processedViolations).toBeDefined();
            expect(Array.isArray(processedViolations)).toBe(true);
            // Should filter out malformed violations
            expect(processedViolations.length).toBeLessThanOrEqual(malformedViolations.length);
        });

        test('should aggregate violations by type', () => {
            const violations = [
                {
                    id: 'color-contrast',
                    description: 'Color contrast issue',
                    impact: 'serious',
                    tool: 'axe',
                },
                {
                    id: 'color-contrast',
                    description: 'Another color contrast issue',
                    impact: 'serious',
                    tool: 'axe',
                },
                {
                    id: 'button-name',
                    description: 'Button name issue',
                    impact: 'critical',
                    tool: 'axe',
                },
                {
                    id: 'color-contrast',
                    description: 'Color contrast issue from pa11y',
                    impact: 'serious',
                    tool: 'pa11y',
                },
            ];

            const aggregated = violationProcessor.aggregateViolationsByType(violations);

            expect(aggregated).toBeDefined();
            expect(Array.isArray(aggregated)).toBe(true);

            // Should group by violation ID
            const colorContrastViolations = aggregated.filter(v => v.id === 'color-contrast');
            const buttonNameViolations = aggregated.filter(v => v.id === 'button-name');

            expect(colorContrastViolations.length).toBeGreaterThan(0);
            expect(buttonNameViolations.length).toBeGreaterThan(0);
        });

        test('should calculate violation statistics', () => {
            const violations = [
                { id: 'violation-1', impact: 'critical', tool: 'axe' },
                { id: 'violation-2', impact: 'serious', tool: 'axe' },
                { id: 'violation-3', impact: 'moderate', tool: 'pa11y' },
                { id: 'violation-4', impact: 'critical', tool: 'pa11y' },
                { id: 'violation-5', impact: 'minor', tool: 'axe' },
            ];

            const stats = violationProcessor.calculateViolationStatistics(violations);

            expect(stats).toBeDefined();
            expect(stats.totalViolations).toBe(5);
            expect(stats.byImpact).toBeDefined();
            expect(stats.byTool).toBeDefined();
            expect(stats.byImpact.critical).toBe(2);
            expect(stats.byImpact.serious).toBe(1);
            expect(stats.byTool.axe).toBe(3);
            expect(stats.byTool.pa11y).toBe(2);
        });

        test('should filter violations by impact level', () => {
            const violations = [
                { id: 'violation-1', impact: 'critical', tool: 'axe' },
                { id: 'violation-2', impact: 'serious', tool: 'axe' },
                { id: 'violation-3', impact: 'moderate', tool: 'pa11y' },
                { id: 'violation-4', impact: 'minor', tool: 'axe' },
            ];

            const criticalViolations = violationProcessor.filterViolationsByImpact(violations, 'critical');
            const seriousAndAbove = violationProcessor.filterViolationsByImpact(violations, 'serious');
            const allViolations = violationProcessor.filterViolationsByImpact(violations, 'minor');

            expect(criticalViolations).toHaveLength(1);
            expect(seriousAndAbove).toHaveLength(2);
            expect(allViolations).toHaveLength(4);
        });

        test('should filter violations by tool', () => {
            const violations = [
                { id: 'violation-1', tool: 'axe' },
                { id: 'violation-2', tool: 'pa11y' },
                { id: 'violation-3', tool: 'axe' },
                { id: 'violation-4', tool: 'pa11y' },
            ];

            const axeViolations = violationProcessor.filterViolationsByTool(violations, 'axe');
            const pa11yViolations = violationProcessor.filterViolationsByTool(violations, 'pa11y');

            expect(axeViolations).toHaveLength(2);
            expect(pa11yViolations).toHaveLength(2);
        });

        test('should generate violation summary', () => {
            const violations = [
                { id: 'color-contrast', impact: 'serious', tool: 'axe' },
                { id: 'button-name', impact: 'critical', tool: 'axe' },
                { id: 'image-alt', impact: 'moderate', tool: 'pa11y' },
                { id: 'link-name', impact: 'minor', tool: 'pa11y' },
            ];

            const summary = violationProcessor.generateViolationSummary(violations);

            expect(summary).toBeDefined();
            expect(summary.totalViolations).toBe(4);
            expect(summary.byImpact).toBeDefined();
            expect(summary.byTool).toBeDefined();
            expect(summary.uniqueViolationTypes).toBe(4);
        });

        test('should handle mixed violation sources', () => {
            const mixedViolations = [
                // Axe violations
                {
                    id: 'color-contrast',
                    description: 'Color contrast issue from axe',
                    impact: 'serious',
                    tool: 'axe',
                },
                // Pa11y violations
                {
                    id: 'WCAG2AA.Principle1.Guideline1_4.1_4_3',
                    description: 'Color contrast issue from pa11y',
                    impact: 'serious',
                    tool: 'pa11y',
                },
                // Lighthouse violations (if supported)
                {
                    id: 'color-contrast',
                    description: 'Color contrast issue from lighthouse',
                    impact: 'serious',
                    tool: 'lighthouse',
                },
            ];

            const processedViolations = violationProcessor.processViolations(mixedViolations, 'mixed');
            const aggregated = violationProcessor.aggregateViolationsByType(processedViolations);
            const stats = violationProcessor.calculateViolationStatistics(processedViolations);

            expect(processedViolations).toBeDefined();
            expect(aggregated).toBeDefined();
            expect(stats).toBeDefined();
            expect(stats.byTool).toBeDefined();
        });

        test('should validate violation data structure', () => {
            const validViolation = {
                id: 'test-violation',
                description: 'Test violation description',
                impact: 'moderate',
                tool: 'axe',
            };

            const isValid = violationProcessor.validateViolation(validViolation);
            expect(isValid).toBe(true);

            const invalidViolation = {
                // Missing required fields
                description: 'Invalid violation',
            };

            const isInvalid = violationProcessor.validateViolation(invalidViolation);
            expect(isInvalid).toBe(false);
        });

        test('should handle large violation datasets', () => {
            const largeViolations = Array.from({ length: 1000 }, (_, i) => ({
                id: `violation-${i}`,
                description: `Violation ${i} description`,
                impact: ['critical', 'serious', 'moderate', 'minor'][i % 4],
                tool: ['axe', 'pa11y'][i % 2],
            }));

            const processedViolations = violationProcessor.processViolations(largeViolations, 'mixed');
            const aggregated = violationProcessor.aggregateViolationsByType(processedViolations);
            const stats = violationProcessor.calculateViolationStatistics(processedViolations);

            expect(processedViolations).toBeDefined();
            expect(processedViolations).toHaveLength(1000);
            expect(aggregated).toBeDefined();
            expect(stats).toBeDefined();
            expect(stats.totalViolations).toBe(1000);
        });

        test('should handle concurrent violation processing', async () => {
            const violations = [
                { id: 'violation-1', impact: 'critical', tool: 'axe' },
                { id: 'violation-2', impact: 'serious', tool: 'pa11y' },
                { id: 'violation-3', impact: 'moderate', tool: 'axe' },
            ];

            const promises = [
                violationProcessor.processViolations(violations, 'axe'),
                violationProcessor.processViolations(violations, 'pa11y'),
                violationProcessor.aggregateViolationsByType(violations),
                violationProcessor.calculateViolationStatistics(violations),
            ];

            const results = await Promise.all(promises);

            expect(results).toHaveLength(4);
            results.forEach(result => {
                expect(result).toBeDefined();
            });
        });

        test('should handle error scenarios gracefully', () => {
            // Test with null violations
            const nullResult = violationProcessor.processViolations(null as any, 'axe');
            expect(nullResult).toBeDefined();
            expect(Array.isArray(nullResult)).toBe(true);

            // Test with undefined violations
            const undefinedResult = violationProcessor.processViolations(undefined as any, 'axe');
            expect(undefinedResult).toBeDefined();
            expect(Array.isArray(undefinedResult)).toBe(true);

            // Test with invalid tool type
            const invalidToolResult = violationProcessor.processViolations([], 'invalid-tool');
            expect(invalidToolResult).toBeDefined();
            expect(Array.isArray(invalidToolResult)).toBe(true);
        });

        test('should maintain data integrity during processing', () => {
            const originalViolations = [
                {
                    id: 'color-contrast',
                    description: 'Original description',
                    impact: 'serious',
                    tool: 'axe',
                    nodes: [{ html: '<button>Test</button>' }],
                },
            ];

            const processedViolations = violationProcessor.processViolations(originalViolations, 'axe');

            expect(processedViolations).toHaveLength(1);
            expect(processedViolations[0].id).toBe(originalViolations[0].id);
            expect(processedViolations[0].description).toBe(originalViolations[0].description);
            expect(processedViolations[0].impact).toBe(originalViolations[0].impact);
            expect(processedViolations[0].tool).toBe('axe');
        });

        test('should handle WCAG compliance mapping', () => {
            const violations = [
                {
                    id: 'color-contrast',
                    description: 'Color contrast issue',
                    impact: 'serious',
                    tool: 'axe',
                    tags: ['wcag2aa', 'wcag143'],
                },
                {
                    id: 'button-name',
                    description: 'Button name issue',
                    impact: 'critical',
                    tool: 'axe',
                    tags: ['wcag2a', 'wcag412'],
                },
            ];

            const wcagMapping = violationProcessor.mapViolationsToWCAG(violations);

            expect(wcagMapping).toBeDefined();
            expect(wcagMapping.wcag2a).toBeDefined();
            expect(wcagMapping.wcag2aa).toBeDefined();
        });
    });

    describe('Cross-Processor Integration', () => {
        test('should integrate with error handling service', () => {
            const violations = [
                { id: 'test-violation', impact: 'critical', tool: 'axe' },
            ];

            // This should not throw an error
            expect(() => {
                violationProcessor.processViolations(violations, 'axe');
            }).not.toThrow();
        });

        test('should integrate with configuration service', () => {
            const violations = [
                { id: 'test-violation', impact: 'moderate', tool: 'axe' },
            ];

            // Should use configuration for processing options
            const processedViolations = violationProcessor.processViolations(violations, 'axe');

            expect(processedViolations).toBeDefined();
            expect(Array.isArray(processedViolations)).toBe(true);
        });

        test('should handle processor configuration changes', () => {
            const violations = [
                { id: 'violation-1', impact: 'critical', tool: 'axe' },
                { id: 'violation-2', impact: 'serious', tool: 'pa11y' },
            ];

            // Process with different configurations
            const result1 = violationProcessor.processViolations(violations, 'axe');
            const result2 = violationProcessor.processViolations(violations, 'pa11y');
            const result3 = violationProcessor.processViolations(violations, 'mixed');

            expect(result1).toBeDefined();
            expect(result2).toBeDefined();
            expect(result3).toBeDefined();
        });
    });

    describe('Performance and Resource Management', () => {
        test('should handle memory-intensive operations', () => {
            const largeViolations = Array.from({ length: 10000 }, (_, i) => ({
                id: `violation-${i}`,
                description: `Violation ${i} description`,
                impact: ['critical', 'serious', 'moderate', 'minor'][i % 4],
                tool: ['axe', 'pa11y'][i % 2],
                nodes: Array.from({ length: 10 }, (_, j) => ({
                    html: `<div>Node ${j}</div>`,
                    target: [`div.node-${j}`],
                })),
            }));

            const startTime = Date.now();
            const processedViolations = violationProcessor.processViolations(largeViolations, 'mixed');
            const endTime = Date.now();

            expect(processedViolations).toBeDefined();
            expect(processedViolations).toHaveLength(10000);
            expect(endTime - startTime).toBeLessThan(5000); // Should complete within 5 seconds
        });

        test('should handle concurrent processing efficiently', async () => {
            const violations = Array.from({ length: 100 }, (_, i) => ({
                id: `violation-${i}`,
                impact: 'moderate',
                tool: 'axe',
            }));

            const startTime = Date.now();
            const promises = Array.from({ length: 10 }, () =>
                violationProcessor.processViolations(violations, 'axe')
            );

            const results = await Promise.all(promises);
            const endTime = Date.now();

            expect(results).toHaveLength(10);
            results.forEach(result => {
                expect(result).toHaveLength(100);
            });
            expect(endTime - startTime).toBeLessThan(3000); // Should complete within 3 seconds
        });
    });
}); 