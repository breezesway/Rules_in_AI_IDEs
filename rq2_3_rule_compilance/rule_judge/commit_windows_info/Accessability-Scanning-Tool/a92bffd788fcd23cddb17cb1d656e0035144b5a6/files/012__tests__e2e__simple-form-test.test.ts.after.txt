import { test, expect } from './setup/test-setup';
import { setupTest, setupFullSiteTest, cleanupTest, TestUtils, TEST_CONFIG } from './setup/test-setup';

test.describe('Simple Form Tests', () => {
    test.beforeEach(async ({ page }) => {
        await setupFullSiteTest(page);
    });

    test.afterEach(async ({ page }) => {
        await cleanupTest(page);
    });

    test('should validate URL input correctly', async ({ page }) => {
        const urlInput = page.locator('#fullSiteUrl');
        const errorElement = page.locator('#fullSiteUrlError');

        // Test valid URL
        await urlInput.fill(TEST_CONFIG.testUrls.valid);
        await expect(errorElement).toHaveAttribute('hidden');

        // Test invalid URL
        await urlInput.fill(TEST_CONFIG.testUrls.malformed);
        await page.locator('#fullSiteForm button[type="submit"]').click();
        await expect(errorElement).not.toHaveAttribute('hidden');
        await expect(errorElement).toContainText('Invalid URL');

        // Test empty URL
        await urlInput.clear();
        await page.locator('#fullSiteForm button[type="submit"]').click();
        await expect(errorElement).not.toHaveAttribute('hidden');
        await expect(errorElement).toContainText('URL is required');
    });

    test('should submit form and show progress section', async ({ page }) => {
        // Enter a valid URL
        const urlInput = page.locator('#fullSiteUrl');
        await urlInput.fill(TEST_CONFIG.testUrls.valid);

        // Submit the form
        await page.locator('#fullSiteForm button[type="submit"]').click();

        // Wait for progress section to appear
        await expect(page.locator('#progressSection')).toBeVisible({ timeout: 10000 });
    });

    test('should handle server health check', async ({ page }) => {
        // Check if the page loads correctly
        await expect(page).toHaveTitle(/Accessibility Testing Tool/);

        // Check if forms are present
        await expect(page.locator('#fullSiteForm')).toBeVisible();
        await expect(page.locator('#singlePageForm')).toBeVisible();
        await expect(page.locator('#regenerateForm')).toBeVisible();
    });
}); 