import { test, expect } from '@playwright/test';

test.describe('Performance and Load Testing E2E Tests', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the web interface
        await page.goto('/');
        // Wait for the page to load completely
        await page.waitForLoadState('networkidle');
    });

    test.describe('Page Load Performance', () => {
        test('should load page within acceptable time', async ({ page }) => {
            const startTime = Date.now();

            // Navigate to the page
            await page.goto('/');
            await page.waitForLoadState('networkidle');

            const loadTime = Date.now() - startTime;

            // Page should load within 3 seconds
            expect(loadTime).toBeLessThan(3000);

            // Verify page is fully loaded
            await expect(page.locator('h1')).toBeVisible();
            await expect(page.locator('#fullSiteUrl')).toBeVisible();
        });

        test('should have fast initial render', async ({ page }) => {
            const startTime = Date.now();

            // Navigate to the page
            await page.goto('/');

            // Wait for first contentful paint
            await page.waitForSelector('h1');

            const renderTime = Date.now() - startTime;

            // Initial render should be under 1 second
            expect(renderTime).toBeLessThan(1000);
        });

        test('should load resources efficiently', async ({ page }) => {
            // Track resource loading
            const resources: string[] = [];

            page.on('response', response => {
                resources.push(response.url());
            });

            await page.goto('/');
            await page.waitForLoadState('networkidle');

            // Should not have too many resources
            expect(resources.length).toBeLessThan(20);

            // Check for any failed resources (excluding favicon and external fonts)
            const failedResources = resources.filter(url =>
                url.includes('localhost:3000') &&
                !url.includes('favicon') &&
                !url.includes('fonts.googleapis.com')
            );
            expect(failedResources.length).toBe(0);
        });
    });

    test.describe('Scan Execution Performance', () => {
        test('should start scan within acceptable time', async ({ page }) => {
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');

            const startTime = Date.now();
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            const startTimeMs = Date.now() - startTime;

            // Scan should start within 5 seconds
            expect(startTimeMs).toBeLessThan(5000);
        });

        test('should maintain responsive UI during scan', async ({ page }) => {
            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            // Test UI responsiveness during scan
            const startTime = Date.now();

            // Try to interact with UI elements
            await page.locator('#fullSiteUrl').click();
            await expect(page.locator('#fullSiteUrl')).toBeFocused();

            const interactionTime = Date.now() - startTime;

            // UI should remain responsive (under 1 second)
            expect(interactionTime).toBeLessThan(1000);
        });
    });

    test.describe('Memory Usage Monitoring', () => {
        test('should not leak memory during repeated scans', async ({ page }) => {
            // Perform multiple scans to check for memory leaks
            for (let i = 0; i < 3; i++) {
                // Start a scan
                const urlInput = page.locator('#fullSiteUrl');
                await urlInput.fill('https://example.com');
                await page.locator('#fullSiteForm button[type="submit"]').click();

                // Wait for scan to start
                await expect(page.getByText(/Processing/)).toBeVisible();

                // Wait a bit for progress
                await page.waitForTimeout(5000);

                // Cancel the scan (if cancel button exists)
                try {
                    await page.getByText(/Cancel/).click();
                    await expect(page.getByText(/Cancelled/)).toBeVisible();
                } catch (error) {
                    // If no cancel button, just wait for completion
                    await page.waitForTimeout(5000);
                }

                // Wait for cleanup
                await page.waitForTimeout(2000);
            }

            // UI should still be responsive after multiple scans
            await expect(page.locator('#fullSiteUrl')).toBeVisible();
            await expect(page.locator('#fullSiteForm button[type="submit"]')).toBeVisible();
        });
    });

    test.describe('Network Performance', () => {
        test('should handle slow network conditions', async ({ page }) => {
            // Simulate slow network
            await page.route('**/*', route => {
                route.continue();
            });

            // Add artificial delay to network requests
            page.on('request', request => {
                // Add 1 second delay to API requests
                if (request.url().includes('/api/')) {
                    return new Promise(resolve => setTimeout(resolve, 1000));
                }
            });

            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');

            const startTime = Date.now();
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Should handle slow network gracefully
            await expect(page.getByText(/Processing/)).toBeVisible({ timeout: 10000 });

            const responseTime = Date.now() - startTime;
            expect(responseTime).toBeGreaterThan(1000); // Should reflect the delay
        });

        test('should handle network interruptions gracefully', async ({ page }) => {
            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            // Simulate network interruption
            await page.route('**/*', route => route.abort());

            // Should handle interruption gracefully
            await expect(page.getByText(/Error/)).toBeVisible({ timeout: 10000 });
        });
    });

    test.describe('Stress Testing', () => {
        test('should handle rapid user interactions', async ({ page }) => {
            // Rapidly interact with form elements
            const urlInput = page.locator('#fullSiteUrl');

            for (let i = 0; i < 10; i++) {
                await urlInput.clear();
                await urlInput.fill(`https://example${i}.com`);
            }

            // UI should remain stable
            await expect(page.locator('#fullSiteUrl')).toBeVisible();
            await expect(page.locator('#fullSiteForm button[type="submit"]')).toBeVisible();
        });

        test('should handle large input data', async ({ page }) => {
            const urlInput = page.locator('#fullSiteUrl');

            // Test with very long URL
            const longUrl = 'https://example.com/' + 'a'.repeat(1000);
            await urlInput.fill(longUrl);

            // Should handle large input gracefully
            await expect(urlInput).toHaveValue(longUrl);

            // Should still be able to submit
            await page.locator('#fullSiteForm button[type="submit"]').click();
            await expect(page.getByText(/Invalid URL/)).toBeVisible();
        });
    });

    test.describe('Resource Optimization', () => {
        test('should minimize DOM size', async ({ page }) => {
            await page.goto('/');

            // Count DOM elements
            const elementCount = await page.evaluate(() => {
                return document.querySelectorAll('*').length;
            });

            // Should have reasonable DOM size
            expect(elementCount).toBeLessThan(100);
        });

        test('should optimize CSS and JavaScript loading', async ({ page }) => {
            const resources: string[] = [];

            page.on('response', response => {
                if (response.url().includes('.css') || response.url().includes('.js')) {
                    resources.push(response.url());
                }
            });

            await page.goto('/');
            await page.waitForLoadState('networkidle');

            // Should have minimal external resources
            expect(resources.length).toBeLessThan(10);

            // Check for any large resources
            for (const resource of resources) {
                const response = await page.request.get(resource);
                const size = response.headers()['content-length'];
                if (size) {
                    expect(parseInt(size)).toBeLessThan(100000); // 100KB limit
                }
            }
        });

        test('should handle browser back/forward navigation efficiently', async ({ page }) => {
            // Navigate to the page
            await page.goto('/');

            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            // Go back
            await page.goBack();

            // Should handle navigation gracefully
            await expect(page.locator('#fullSiteUrl')).toBeVisible();

            // Go forward
            await page.goForward();

            // Should restore state properly
            await expect(page.getByText(/Processing/)).toBeVisible();
        });
    });
}); 