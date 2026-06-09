import { test, expect } from '@playwright/test';

test.describe('Accessibility Scanning E2E Tests', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the web interface
        await page.goto('/');
        // Wait for the page to load completely
        await page.waitForLoadState('networkidle');
    });

    test.describe('Full Site Accessibility Scanning', () => {
        test('should complete full site scan workflow', async ({ page }) => {
            // Enter a test URL
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');

            // Submit the scan
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            // Wait for progress updates
            await expect(page.getByText(/Progress/)).toBeVisible();

            // Wait for completion (with timeout)
            await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 60000 });

            // Verify results are displayed
            await expect(page.getByText(/Results/)).toBeVisible();
        });

        test('should handle scan errors gracefully', async ({ page }) => {
            // Enter an invalid URL that will cause errors
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://invalid-domain-that-does-not-exist-12345.com');

            // Submit the scan
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for error handling
            await expect(page.getByText(/Error/)).toBeVisible({ timeout: 30000 });

            // Verify retry option is available
            await expect(page.getByText(/Retry/)).toBeVisible();
        });

        test('should display real-time progress updates', async ({ page }) => {
            // Enter a test URL
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');

            // Submit the scan
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Verify progress stages are displayed
            await expect(page.getByText(/Initializing/)).toBeVisible();
            await expect(page.getByText(/Crawling/)).toBeVisible();
            await expect(page.getByText(/Analyzing/)).toBeVisible();
            await expect(page.getByText(/Generating/)).toBeVisible();
        });
    });

    test.describe('Single Page Accessibility Scanning', () => {
        test('should complete single page scan workflow', async ({ page }) => {
            // Enter a test URL
            const urlInput = page.locator('#singlePageUrl');
            await urlInput.fill('https://example.com');

            // Submit the scan
            await page.locator('#singlePageForm button[type="submit"]').click();

            // Wait for scan to complete
            await expect(page.getByText(/Complete/)).toBeVisible({ timeout: 30000 });

            // Verify results are displayed
            await expect(page.getByText(/Results/)).toBeVisible();
        });

        test('should validate URL before starting scan', async ({ page }) => {
            // Enter an invalid URL
            const urlInput = page.locator('#singlePageUrl');
            await urlInput.fill('not-a-valid-url');

            // Submit the scan
            await page.locator('#singlePageForm button[type="submit"]').click();

            // Verify validation error is shown
            await expect(page.getByText(/Invalid URL/)).toBeVisible();
        });
    });

    test.describe('Report Regeneration', () => {
        test('should regenerate reports from existing data', async ({ page }) => {
            // Submit the regeneration request
            await page.locator('#regenerateForm button[type="submit"]').click();

            // Wait for regeneration to complete
            await expect(page.getByText(/Regenerated/)).toBeVisible({ timeout: 30000 });

            // Verify reports are available
            await expect(page.getByText(/Reports/)).toBeVisible();
        });

        test('should handle no existing data gracefully', async ({ page }) => {
            // Submit the regeneration request
            await page.locator('#regenerateForm button[type="submit"]').click();

            // Verify appropriate message when no data exists
            await expect(page.getByText(/No reports found/)).toBeVisible({ timeout: 10000 });
        });
    });

    test.describe('User Interaction Testing', () => {
        test('should handle URL input and validation', async ({ page }) => {
            const urlInput = page.locator('#fullSiteUrl');

            // Test valid URL
            await urlInput.fill('https://example.com');
            await expect(page.getByText(/Invalid URL/)).not.toBeVisible();

            // Test invalid URL
            await urlInput.fill('invalid-url');
            await page.locator('#fullSiteForm button[type="submit"]').click();
            await expect(page.getByText(/Invalid URL/)).toBeVisible();

            // Test empty URL
            await urlInput.clear();
            await page.locator('#fullSiteForm button[type="submit"]').click();
            await expect(page.getByText(/URL is required/)).toBeVisible();
        });

        test('should handle form submission and feedback', async ({ page }) => {
            // Enter URL and submit
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Verify loading state
            await expect(page.locator('#fullSiteForm button[type="submit"]')).toBeDisabled();
            await expect(page.getByText(/Processing/)).toBeVisible();
        });

        test('should handle scan cancellation', async ({ page }) => {
            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for scan to start
            await expect(page.getByText(/Processing/)).toBeVisible();

            // Cancel the scan
            await page.getByText(/Cancel/).click();

            // Verify cancellation
            await expect(page.getByText(/Cancelled/)).toBeVisible();
        });
    });

    test.describe('Real-time Progress Tracking', () => {
        test('should display WebSocket progress updates', async ({ page }) => {
            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Verify WebSocket connection and progress updates
            await expect(page.getByText(/Connected/)).toBeVisible();
            await expect(page.getByText(/Progress/)).toBeVisible();

            // Wait for progress updates
            await expect(page.getByText(/0%/)).toBeVisible();
            await expect(page.getByText(/25%/)).toBeVisible({ timeout: 30000 });
        });

        test('should handle WebSocket disconnection', async ({ page }) => {
            // Start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Simulate network interruption
            await page.route('**/*', route => route.abort());

            // Verify reconnection handling
            await expect(page.getByText(/Reconnecting/)).toBeVisible();
        });
    });

    test.describe('Error Handling and Recovery', () => {
        test('should handle network errors gracefully', async ({ page }) => {
            // Block network requests
            await page.route('**/*', route => route.abort());

            // Try to start a scan
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://example.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Verify error handling
            await expect(page.getByText(/Network error/)).toBeVisible();
        });

        test('should provide retry options for failed scans', async ({ page }) => {
            // Start a scan that will fail
            const urlInput = page.locator('#fullSiteUrl');
            await urlInput.fill('https://invalid-domain-that-does-not-exist-12345.com');
            await page.locator('#fullSiteForm button[type="submit"]').click();

            // Wait for failure
            await expect(page.getByText(/Error/)).toBeVisible({ timeout: 30000 });

            // Verify retry button is available
            await expect(page.getByText(/Retry/)).toBeVisible();

            // Test retry functionality
            await page.getByText(/Retry/).click();
            await expect(page.getByText(/Retrying/)).toBeVisible();
        });
    });
}); 