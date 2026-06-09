import { test, expect } from '@playwright/test';

test.describe('Report Details Page', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to reports page first
        await page.goto('/reports');
    });

    test('should display report details page with sample report ID', async ({ page }) => {
        // Mock successful API response for this test
        await page.route('/api/reports/**', async route => {
            const mockReportData = {
                success: true,
                data: {
                    id: 'test-report-123',
                    siteUrl: 'https://example.com',
                    reportType: 'site-wide',
                    timestamp: new Date().toISOString(),
                    wcagLevel: 'WCAG2AA',
                    metadata: {
                        toolsUsed: ['axe-core', 'pa11y']
                    },
                    data: {
                        siteUrl: 'https://example.com',
                        reportType: 'site-wide',
                        timestamp: new Date().toISOString(),
                        wcagLevel: 'WCAG2AA',
                        summary: {
                            totalPages: 5,
                            totalViolations: 3,
                            criticalViolations: 1,
                            seriousViolations: 1,
                            moderateViolations: 1,
                            minorViolations: 0,
                            compliancePercentage: 85
                        },
                        violations: [],
                        pageReports: []
                    }
                }
            };

            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify(mockReportData)
            });
        });

        // Navigate directly to a report details page
        const sampleReportId = 'test-report-123';
        await page.goto(`/reports/${sampleReportId}`);

        // Check that the page loads
        await expect(page).toHaveTitle(/Report Details/);

        // Wait for page to load
        await page.waitForSelector('main', { state: 'visible' });

        // Wait for JavaScript to load and render content
        await page.waitForSelector('#reportContent', { state: 'visible' });

        // Check for back button (use more specific selector)
        await expect(page.locator('.back-button')).toBeVisible();
        await expect(page.locator('.back-button')).toContainText('Back to Reports');
    });

    test('should handle missing report ID gracefully', async ({ page }) => {
        // Navigate to reports page without ID
        await page.goto('/reports/');

        // Should redirect to reports page or show error
        await expect(page).toHaveTitle(/Search Reports/);
    });

    test('should display error for invalid report ID', async ({ page }) => {
        // Navigate to a non-existent report
        await page.goto('/reports/invalid-report-id');

        // Wait for error to appear
        await expect(page.locator('#errorSection')).toBeVisible();
        await expect(page.locator('#errorMessage')).toContainText('Failed to load report');
    });

    test('should have proper accessibility structure', async ({ page }) => {
        await page.goto('/reports/test-report-123');

        // Wait for page to load
        await page.waitForSelector('main', { state: 'visible' });

        // Check for proper heading structure
        await expect(page.locator('h1')).toBeVisible();

        // Check for proper navigation
        await expect(page.locator('nav')).toBeVisible();
    });

    test('should handle back navigation correctly', async ({ page }) => {
        // Mock successful API response for this test
        await page.route('/api/reports/**', async route => {
            const mockReportData = {
                success: true,
                data: {
                    id: 'test-report-123',
                    siteUrl: 'https://example.com',
                    reportType: 'site-wide',
                    timestamp: new Date().toISOString(),
                    wcagLevel: 'WCAG2AA',
                    metadata: {
                        toolsUsed: ['axe-core', 'pa11y']
                    },
                    data: {
                        siteUrl: 'https://example.com',
                        reportType: 'site-wide',
                        timestamp: new Date().toISOString(),
                        wcagLevel: 'WCAG2AA',
                        summary: {
                            totalPages: 5,
                            totalViolations: 3,
                            criticalViolations: 1,
                            seriousViolations: 1,
                            moderateViolations: 1,
                            minorViolations: 0,
                            compliancePercentage: 85
                        },
                        violations: [],
                        pageReports: []
                    }
                }
            };

            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify(mockReportData)
            });
        });

        await page.goto('/reports/test-report-123');

        // Wait for page to load and content to render
        await page.waitForSelector('#reportContent', { state: 'visible' });
        await page.waitForSelector('.back-button', { state: 'visible' });

        // Click back button
        await page.click('.back-button');

        // Should navigate back to reports page
        await expect(page).toHaveURL('/reports');
    });

    test('should have loading functionality available', async ({ page }) => {
        await page.goto('/reports/test-report-123');

        // Wait for page to load
        await page.waitForSelector('main', { state: 'visible' });

        // Check that the page has loading elements (they may be hidden by JavaScript)
        await expect(page.locator('#loadingSection')).toBeAttached();
        await expect(page.locator('.loading-spinner')).toBeAttached();
    });

            test('should have responsive design', async ({ page }) => {
        // Mock successful API response for this test
        await page.route('/api/reports/**', async route => {
            const mockReportData = {
                success: true,
                data: {
                    id: 'test-report-123',
                    siteUrl: 'https://example.com',
                    reportType: 'site-wide',
                    timestamp: new Date().toISOString(),
                    wcagLevel: 'WCAG2AA',
                    metadata: {
                        toolsUsed: ['axe-core', 'pa11y']
                    },
                    data: {
                        siteUrl: 'https://example.com',
                        reportType: 'site-wide',
                        timestamp: new Date().toISOString(),
                        wcagLevel: 'WCAG2AA',
                        summary: {
                            totalPages: 5,
                            totalViolations: 3,
                            criticalViolations: 1,
                            seriousViolations: 1,
                            moderateViolations: 1,
                            minorViolations: 0,
                            compliancePercentage: 85
                        },
                        violations: [],
                        pageReports: []
                    }
                }
            };

            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify(mockReportData)
            });
        });

        await page.goto('/reports/test-report-123');

        // Wait for page to load and content to render
        await page.waitForSelector('#reportContent', { state: 'visible' });

        // Test mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        
        // Check that content is still accessible
        await expect(page.locator('main')).toBeVisible();
        await expect(page.locator('.back-button')).toBeVisible();

        // Test tablet viewport
        await page.setViewportSize({ width: 768, height: 1024 });
        await expect(page.locator('main')).toBeVisible();

        // Test desktop viewport
        await page.setViewportSize({ width: 1920, height: 1080 });
        await expect(page.locator('main')).toBeVisible();
    });

    test('should handle network errors gracefully', async ({ page }) => {
        // Mock network failure
        await page.route('/api/reports/**', route => {
            route.abort('failed');
        });

        await page.goto('/reports/test-report-123');

        // Should show error message
        await expect(page.locator('#errorSection')).toBeVisible();
        await expect(page.locator('#errorMessage')).toContainText('Failed to load report');
    });

    test('should display report content when data is available', async ({ page }) => {
        // Mock successful API response
        await page.route('/api/reports/**', async route => {
            const mockReportData = {
                success: true,
                data: {
                    id: 'test-report-123',
                    siteUrl: 'https://example.com',
                    reportType: 'site-wide',
                    timestamp: new Date().toISOString(),
                    wcagLevel: 'WCAG2AA',
                    metadata: {
                        toolsUsed: ['axe-core', 'pa11y'],
                        totalViolations: 5,
                        compliancePercentage: 85
                    },
                    summary: {
                        totalPages: 10,
                        totalViolations: 5,
                        criticalViolations: 1,
                        seriousViolations: 2,
                        moderateViolations: 1,
                        minorViolations: 1,
                        compliancePercentage: 85
                    },
                    violations: [
                        {
                            id: 'color-contrast',
                            impact: 'serious',
                            description: 'Elements must meet minimum color contrast ratio requirements',
                            help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                            wcagLevel: 'AA',
                            occurrences: 3,
                            tools: ['axe-core'],
                            elements: [
                                {
                                    html: '<button class="low-contrast">Submit</button>',
                                    selector: 'button.low-contrast',
                                    failureSummary: 'Element has insufficient color contrast'
                                }
                            ],
                            remediation: {
                                priority: 'High',
                                effort: 'Medium',
                                suggestions: ['Increase the contrast ratio of the element']
                            }
                        }
                    ],
                    pageReports: [
                        {
                            url: 'https://example.com',
                            violations: [],
                            summary: {
                                totalViolations: 0,
                                criticalViolations: 0,
                                seriousViolations: 0,
                                moderateViolations: 0,
                                minorViolations: 0
                            }
                        }
                    ]
                }
            };

            await route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify(mockReportData)
            });
        });

        await page.goto('/reports/test-report-123');

        // Wait for content to load
        await expect(page.locator('#reportContent')).toBeVisible();

        // Check for report header
        await expect(page.locator('.report-header h1')).toContainText('Accessibility Report');
        await expect(page.locator('.report-header')).toContainText('https://example.com');

        // Check for summary section (class name changed to results-section)
        await expect(page.locator('.results-section').first()).toBeVisible();
        await expect(page.locator('.summary-value').first()).toContainText('85%');

        // Check for violations section (violations are now within results-section)
        await expect(page.locator('.violation-card')).toBeVisible();
        await expect(page.locator('.violation-title')).toContainText('color-contrast');
    });
}); 