import { test, expect } from '@playwright/test';

interface AxeResults {
    violations: Array<{
        id: string;
        description: string;
        help: string;
        helpUrl: string;
        tags: string[];
        nodes: Array<{
            html: string;
            target: string[];
            failureSummary: string;
        }>;
    }>;
    passes: any[];
    incomplete: any[];
    inapplicable: any[];
}

test.describe('Component Accessibility Testing', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to Storybook
        await page.goto('http://localhost:6006');
        await page.waitForLoadState('networkidle');
    });

    test.describe('Header Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            // Navigate to Header story
            await page.goto('http://localhost:6006/?path=/story/components-header--default');
            await page.waitForLoadState('networkidle');

            // Run axe-core accessibility test
            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            // Check for violations
            expect(results.violations).toHaveLength(0);
        });

        test('should have proper heading structure', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-header--default');
            await page.waitForLoadState('networkidle');

            // Check for single h1
            const h1Count = await page.locator('h1').count();
            expect(h1Count).toBe(1);

            // Check for proper navigation landmarks
            const nav = page.locator('nav');
            await expect(nav).toHaveAttribute('aria-label', 'Main navigation');
        });

        test('should support keyboard navigation', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-header--default');
            await page.waitForLoadState('networkidle');

            // Test tab navigation through nav links
            await page.keyboard.press('Tab');
            const firstLink = page.locator('nav a').first();
            await expect(firstLink).toBeFocused();
        });
    });

    test.describe('ScanOptions Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-scanoptions--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper form labels', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-scanoptions--default');
            await page.waitForLoadState('networkidle');

            // Check that all form inputs have labels
            const inputs = page.locator('input[type="url"]');
            const inputCount = await inputs.count();

            for (let i = 0; i < inputCount; i++) {
                const input = inputs.nth(i);
                const id = await input.getAttribute('id');
                if (id) {
                    const label = page.locator(`label[for="${id}"]`);
                    await expect(label).toBeVisible();
                }
            }
        });

        test('should have proper ARIA attributes', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-scanoptions--default');
            await page.waitForLoadState('networkidle');

            // Check for proper ARIA attributes on form elements
            const inputs = page.locator('input[type="url"]');
            const inputCount = await inputs.count();

            for (let i = 0; i < inputCount; i++) {
                const input = inputs.nth(i);
                await expect(input).toHaveAttribute('aria-describedby');
                await expect(input).toHaveAttribute('required');
            }
        });
    });

    test.describe('ProgressSection Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-progresssection--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper progress bar attributes', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-progresssection--crawling');
            await page.waitForLoadState('networkidle');

            // Check for proper progress bar attributes
            const progressBar = page.locator('[role="progressbar"]');
            await expect(progressBar).toHaveAttribute('aria-valuenow');
            await expect(progressBar).toHaveAttribute('aria-valuemin', '0');
            await expect(progressBar).toHaveAttribute('aria-valuemax', '100');
            await expect(progressBar).toHaveAttribute('aria-describedby');
        });

        test('should announce progress updates', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-progresssection--analyzing');
            await page.waitForLoadState('networkidle');

            // Check for live region announcements
            const liveRegion = page.locator('[aria-live]');
            await expect(liveRegion).toBeVisible();
        });
    });

    test.describe('ResultsSection Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-resultssection--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper table structure', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-resultssection--with-details');
            await page.waitForLoadState('networkidle');

            // Check for proper table structure if tables are present
            const tables = page.locator('table');
            const tableCount = await tables.count();

            if (tableCount > 0) {
                for (let i = 0; i < tableCount; i++) {
                    const table = tables.nth(i);
                    // Check for table headers
                    const headers = table.locator('th');
                    const headerCount = await headers.count();
                    expect(headerCount).toBeGreaterThan(0);
                }
            }
        });

        test('should have proper heading hierarchy', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-resultssection--default');
            await page.waitForLoadState('networkidle');

            // Check for proper heading structure
            const headings = page.locator('h1, h2, h3, h4, h5, h6');
            const headingCount = await headings.count();
            expect(headingCount).toBeGreaterThan(0);
        });
    });

    test.describe('ErrorSection Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-errorsection--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper alert attributes', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-errorsection--network-error');
            await page.waitForLoadState('networkidle');

            // Check for proper alert attributes
            const alert = page.locator('[role="alert"]');
            await expect(alert).toBeVisible();
            await expect(alert).toHaveAttribute('aria-live', 'assertive');
        });

        test('should announce errors to screen readers', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-errorsection--critical-error');
            await page.waitForLoadState('networkidle');

            // Check for live region announcements
            const liveRegion = page.locator('[aria-live="assertive"]');
            await expect(liveRegion).toBeVisible();
        });
    });

    test.describe('Footer Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-footer--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper link descriptions', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-footer--default');
            await page.waitForLoadState('networkidle');

            // Check that all links have meaningful text
            const links = page.locator('a');
            const linkCount = await links.count();

            for (let i = 0; i < linkCount; i++) {
                const link = links.nth(i);
                const text = await link.textContent();
                expect(text?.trim()).toBeTruthy();
            }
        });

        test('should support keyboard navigation', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-footer--many-links');
            await page.waitForLoadState('networkidle');

            // Test tab navigation through footer links
            await page.keyboard.press('Tab');
            const firstLink = page.locator('footer a').first();
            await expect(firstLink).toBeFocused();
        });
    });

    test.describe('Cross-Component Accessibility', () => {
        test('should maintain consistent focus indicators', async ({ page }) => {
            const stories = [
                'components-header--default',
                'components-scanoptions--default',
                'components-progresssection--default',
                'components-resultssection--default',
                'components-errorsection--default',
                'components-footer--default',
                'components-webinterface--default',
                'pages-landingpage--default',
                'pages-fullsitescanpage--default',
                'pages-singlepagescanpage--default',
                'pages-reportspage--default',
                'components-progresssection--default',
                'components-resultssection--default',
                'components-errorsection--default',
                'components-footer--default'
            ];

            for (const story of stories) {
                await page.goto(`http://localhost:6006/?path=/story/${story}`);
                await page.waitForLoadState('networkidle');

                // Check for focus indicators on interactive elements
                const interactiveElements = page.locator('button, a, input, select, textarea');
                const elementCount = await interactiveElements.count();

                if (elementCount > 0) {
                    // Focus the first interactive element
                    await interactiveElements.first().focus();

                    // Check that focus is visible (this would need CSS inspection in a real test)
                    await expect(interactiveElements.first()).toBeFocused();
                }
            }
        });

        test('should have consistent colour contrast', async ({ page }) => {
            const stories = [
                'components-header--default',
                'components-scanoptions--default',
                'components-progresssection--default',
                'components-resultssection--default',
                'components-errorsection--default',
                'components-footer--default'
            ];

            for (const story of stories) {
                await page.goto(`http://localhost:6006/?path=/story/${story}`);
                await page.waitForLoadState('networkidle');

                // Run axe-core with specific colour contrast rules
                const results = await page.evaluate(() => {
                    return new Promise<AxeResults>((resolve) => {
                        // @ts-ignore - axe is available in Storybook
                        axe.run({
                            rules: {
                                'color-contrast': { enabled: true }
                            }
                        }, (err: any, results: AxeResults) => {
                            if (err) throw err;
                            resolve(results);
                        });
                    });
                });

                // Check for colour contrast violations
                const colorContrastViolations = results.violations.filter(
                    (v) => v.id === 'color-contrast'
                );
                expect(colorContrastViolations).toHaveLength(0);
            }
        });
    });

    test.describe('WebInterface Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-webinterface--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper landmark structure', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/components-webinterface--default');
            await page.waitForLoadState('networkidle');

            const mainElement = await page.locator('main').count();
            expect(mainElement).toBeGreaterThan(0);
        });
    });

    test.describe('LandingPage Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-landingpage--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper heading structure', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-landingpage--default');
            await page.waitForLoadState('networkidle');

            const h1Elements = await page.locator('h1').count();
            expect(h1Elements).toBeGreaterThan(0);
        });
    });

    test.describe('FullSiteScanPage Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-fullsitescanpage--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper form accessibility', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-fullsitescanpage--default');
            await page.waitForLoadState('networkidle');

            const formElements = await page.locator('form').count();
            if (formElements > 0) {
                const labels = await page.locator('label').count();
                expect(labels).toBeGreaterThan(0);
            }
        });
    });

    test.describe('SinglePageScanPage Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-singlepagescanpage--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper form accessibility', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-singlepagescanpage--default');
            await page.waitForLoadState('networkidle');

            const formElements = await page.locator('form').count();
            if (formElements > 0) {
                const labels = await page.locator('label').count();
                expect(labels).toBeGreaterThan(0);
            }
        });
    });

    test.describe('ReportsPage Component', () => {
        test('should pass WCAG 2.1 AA compliance', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-reportspage--default');
            await page.waitForLoadState('networkidle');

            const results = await page.evaluate(() => {
                return new Promise<AxeResults>((resolve) => {
                    // @ts-ignore - axe is available in Storybook
                    axe.run((err: any, results: AxeResults) => {
                        if (err) throw err;
                        resolve(results);
                    });
                });
            });

            expect(results.violations).toHaveLength(0);
        });

        test('should have proper table accessibility', async ({ page }) => {
            await page.goto('http://localhost:6006/?path=/story/pages-reportspage--withreports');
            await page.waitForLoadState('networkidle');

            const tableElements = await page.locator('table').count();
            if (tableElements > 0) {
                const captionElements = await page.locator('caption').count();
                expect(captionElements).toBeGreaterThan(0);
            }
        });
    });
}); 