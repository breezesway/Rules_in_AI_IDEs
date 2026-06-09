import { PdfOrchestrator, PdfGenerationOptions, PdfGenerationResult, ScanMetadata } from '@/utils/reporting/pdf-generators/pdf-orchestrator';
import { SiteWideAccessibilityReport } from '@/core/types/common';
import { Page } from '@playwright/test';

// Mock Playwright Page
const mockPage = {
    goto: jest.fn(),
    setContent: jest.fn(),
    pdf: jest.fn(),
    close: jest.fn()
} as unknown as Page;

// Mock browser
const mockBrowser = {
    newPage: jest.fn().mockResolvedValue(mockPage),
    close: jest.fn()
};

// Mock chromium
jest.mock('@playwright/test', () => ({
    chromium: {
        launch: jest.fn().mockResolvedValue(mockBrowser)
    }
}));

describe('PdfOrchestrator', () => {
    let orchestrator: PdfOrchestrator;
    let mockReport: SiteWideAccessibilityReport;

    beforeEach(() => {
        orchestrator = new PdfOrchestrator(mockPage);

        mockReport = {
            siteUrl: 'https://example.com',
            timestamp: new Date().toISOString(),
            testSuite: 'Phase 2 Accessibility Testing',
            wcagLevel: 'WCAG2AA',
            summary: {
                totalPages: 2,
                pagesWithViolations: 1,
                totalViolations: 3,
                criticalViolations: 1,
                seriousViolations: 2,
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

        // Reset mocks
        jest.clearAllMocks();
    });

    describe('generatePdfReports', () => {
        it('should generate PDF reports for default audiences', async () => {
            const options: PdfGenerationOptions = {
                format: 'A4',
                includeBackground: true,
                margins: {
                    top: '0.75in',
                    right: '0.75in',
                    bottom: '0.75in',
                    left: '0.75in'
                }
            };

            // Mock successful PDF generation
            (mockPage.pdf as jest.Mock).mockResolvedValue(Buffer.from('mock-pdf-content'));

            const result = await orchestrator.generatePdfReports(mockReport, options);

            expect(result.success).toBe(true);
            if (result.success && result.data) {
                expect(result.data).toBeDefined();
                expect(Array.isArray(result.data)).toBe(true);
                expect(result.data.length).toBeGreaterThan(0);
            }
        });

        it('should generate PDF reports for custom audiences', async () => {
            const options: PdfGenerationOptions = {
                audiences: [
                    { name: 'stakeholder', displayName: 'Stakeholder Report' },
                    { name: 'developer', displayName: 'Developer Report' }
                ],
                format: 'Letter',
                includeBackground: false
            };

            // Mock successful PDF generation
            (mockPage.pdf as jest.Mock).mockResolvedValue(Buffer.from('mock-pdf-content'));

            const result = await orchestrator.generatePdfReports(mockReport, options);

            expect(result.success).toBe(true);
            if (result.success && result.data) {
                expect(result.data).toHaveLength(2);
                expect(result.data[0]?.audience).toBe('stakeholder');
                expect(result.data[1]?.audience).toBe('developer');
            }
        });

        it('should handle PDF generation errors gracefully', async () => {
            // Mock PDF generation failure
            (mockPage.pdf as jest.Mock).mockRejectedValue(new Error('PDF generation failed'));

            const result = await orchestrator.generatePdfReports(mockReport);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('PDF generation failed');
            }
        });

        it('should use custom filename when provided', async () => {
            const options: PdfGenerationOptions = {
                filename: 'custom-report.pdf'
            };

            // Mock successful PDF generation
            (mockPage.pdf as jest.Mock).mockResolvedValue(Buffer.from('mock-pdf-content'));

            const result = await orchestrator.generatePdfReports(mockReport, options);

            expect(result.success).toBe(true);
            if (result.success && result.data) {
                expect(result.data[0]?.filePath).toContain('custom-report');
            }
        });

        it('should include scan metadata when provided', async () => {
            const scanMetadata: ScanMetadata = {
                totalPages: 5,
                totalViolations: 10,
                compliancePercentage: 80,
                wcagLevel: 'WCAG2AA',
                criticalViolations: 2,
                seriousViolations: 5,
                moderateViolations: 2,
                minorViolations: 1,
                browser: 'Chrome',
                viewport: '1920x1080',
                scanConfiguration: {
                    maxPages: 10,
                    maxDepth: 3,
                    maxConcurrency: 5,
                    retryFailedPages: true,
                    generateReports: true,
                    wcagLevel: 'WCAG2AA'
                },
                performanceMetrics: {
                    totalScanTime: 30000,
                    averageTimePerPage: 6000,
                    successRate: 90,
                    pagesAnalyzed: 5,
                    pagesWithViolations: 3
                },
                toolsUsed: ['axe-core', 'pa11y'],
                scanStartedAt: new Date(),
                scanCompletedAt: new Date(),
                scanId: 'test-scan-123',
                scanType: 'full-site',
                userAgent: 'Mozilla/5.0...',
                crawlDepth: 3,
                excludedPatterns: ['/admin/*', '/private/*']
            };

            const options: PdfGenerationOptions = {
                scanMetadata
            };

            // Mock successful PDF generation
            (mockPage.pdf as jest.Mock).mockResolvedValue(Buffer.from('mock-pdf-content'));

            const result = await orchestrator.generatePdfReports(mockReport, options);

            expect(result.success).toBe(true);
        });
    });

    describe('generateCustomPdf', () => {
        it('should generate custom PDF report', async () => {
            const audience = { name: 'custom', displayName: 'Custom Report' };
            const filename = 'custom-report.pdf';

            // Mock successful PDF generation
            (mockPage.pdf as jest.Mock).mockResolvedValue(Buffer.from('mock-pdf-content'));

            const result = await orchestrator.generateCustomPdf(mockReport, audience, filename);

            expect(result.success).toBe(true);
            if (result.success && result.data) {
                expect(result.data.audience).toBe('custom');
                expect(result.data.displayName).toBe('Custom Report');
                expect(result.data.filePath).toContain('custom-report');
            }
        });

        it('should handle custom PDF generation errors', async () => {
            const audience = { name: 'custom', displayName: 'Custom Report' };
            const filename = 'custom-report.pdf';

            // Mock PDF generation failure
            (mockPage.pdf as jest.Mock).mockRejectedValue(new Error('Custom PDF generation failed'));

            const result = await orchestrator.generateCustomPdf(mockReport, audience, filename);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Custom PDF generation failed');
            }
        });
    });

    describe('validateOptions', () => {
        it('should validate valid options', () => {
            const options: PdfGenerationOptions = {
                audiences: [
                    { name: 'stakeholder', displayName: 'Stakeholder Report' }
                ],
                format: 'A4',
                includeBackground: true,
                margins: {
                    top: '0.75in',
                    right: '0.75in',
                    bottom: '0.75in',
                    left: '0.75in'
                }
            };

            const result = orchestrator.validateOptions(options);

            expect(result.success).toBe(true);
        });

        it('should reject invalid format', () => {
            const options: PdfGenerationOptions = {
                format: 'Invalid' as any
            };

            const result = orchestrator.validateOptions(options);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Invalid format');
            }
        });

        it('should reject invalid margins', () => {
            const options: PdfGenerationOptions = {
                margins: {
                    top: 'invalid',
                    right: '0.75in',
                    bottom: '0.75in',
                    left: '0.75in'
                }
            };

            const result = orchestrator.validateOptions(options);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Invalid margins');
            }
        });

        it('should reject empty audiences array', () => {
            const options: PdfGenerationOptions = {
                audiences: []
            };

            const result = orchestrator.validateOptions(options);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('At least one audience');
            }
        });
    });

    describe('cleanup', () => {
        it('should cleanup resources successfully', async () => {
            await expect(orchestrator.cleanup()).resolves.not.toThrow();
        });

        it('should handle cleanup errors gracefully', async () => {
            // Mock cleanup error
            (mockPage.close as jest.Mock).mockRejectedValue(new Error('Cleanup failed'));

            await expect(orchestrator.cleanup()).resolves.not.toThrow();
        });
    });

    describe('private methods', () => {
        it('should generate default filename correctly', () => {
            const filename = (orchestrator as any).generateDefaultFilename(mockReport);

            expect(filename).toContain('accessibility-report');
            expect(filename).toContain('example.com');
            expect(filename).toMatch(/^\d{4}-\d{2}-\d{2}/); // Date format
        });

        it('should get default audiences', () => {
            const audiences = (orchestrator as any).getDefaultAudiences();

            expect(audiences).toHaveLength(4);
            expect(audiences.map((a: { name: string; displayName: string }) => a.name)).toEqual([
                'stakeholder',
                'researcher',
                'developer',
                'compliance'
            ]);
        });

        it('should generate PDF file path correctly', () => {
            const baseFilename = 'test-report';
            const audience = 'stakeholder';

            const filePath = (orchestrator as any).generatePdfFilePath(baseFilename, audience);

            expect(filePath).toContain('accessibility-reports');
            expect(filePath).toContain('test-report');
            expect(filePath).toContain('stakeholder');
            expect(filePath).toMatch(/\.pdf$/);
        });
    });

    describe('error handling', () => {
        it('should handle browser launch errors', async () => {
            // Mock browser launch failure
            const { chromium } = require('@playwright/test');
            (chromium.launch as jest.Mock).mockRejectedValue(new Error('Browser launch failed'));

            const result = await orchestrator.generatePdfReports(mockReport);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Browser launch failed');
            }
        });

        it('should handle page creation errors', async () => {
            // Mock page creation failure
            (mockBrowser.newPage as jest.Mock).mockRejectedValue(new Error('Page creation failed'));

            const result = await orchestrator.generatePdfReports(mockReport);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Page creation failed');
            }
        });

        it('should handle content setting errors', async () => {
            // Mock content setting failure
            (mockPage.setContent as jest.Mock).mockRejectedValue(new Error('Content setting failed'));

            const result = await orchestrator.generatePdfReports(mockReport);

            expect(result.success).toBe(false);
            if (!result.success) {
                expect(result.error).toContain('Content setting failed');
            }
        });
    });
}); 