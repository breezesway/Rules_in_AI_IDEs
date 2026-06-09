import { test, expect } from '@playwright/test';
import { FullSiteScanPage } from './pages/FullSiteScanPage';
import { setupFullSiteTest, cleanupTest } from './setup/test-setup';

test.describe('Full Site Scan E2E Tests', () => {
    let fullSitePage: FullSiteScanPage;

    test.beforeEach(async ({ page }) => {
        await setupFullSiteTest(page);
        fullSitePage = new FullSiteScanPage(page);
    });

    test.afterEach(async ({ page }) => {
        await cleanupTest(page);
    });

    test.describe('Page Loading', () => {
        test('should load the full site scan page successfully', async ({ page }) => {
            await fullSitePage.expectPageLoaded();
        });

        test('should display the full site scan form', async ({ page }) => {
            await expect(fullSitePage.fullSiteForm).toBeVisible();
            await expect(fullSitePage.fullSiteUrlInput).toBeVisible();
            await expect(fullSitePage.fullSiteWcagLevelSelect).toBeVisible();
            await expect(fullSitePage.fullSiteSubmitBtn).toBeVisible();
        });
    });

    test.describe('Form Functionality', () => {
        test('should accept valid URL input', async ({ page }) => {
            await fullSitePage.fillFullSiteUrl('https://example.com');
            await fullSitePage.expectFullSiteUrlValue('https://example.com');
        });

        test('should allow WCAG level selection', async ({ page }) => {
            await fullSitePage.selectWcagLevel('WCAG2AAA');
            await expect(fullSitePage.fullSiteWcagLevelSelect).toHaveValue('WCAG2AAA');
        });

        test('should submit form with valid data', async ({ page }) => {
            await fullSitePage.startFullSiteScan('https://example.com', 'WCAG2AA');
            // The form should submit successfully (we don't test the actual scan here)
        });
    });

    test.describe('Accessibility', () => {
        test('should have accessible form elements', async ({ page }) => {
            await fullSitePage.expectFormAccessibility();
        });

        test('should support keyboard navigation', async ({ page }) => {
            await fullSitePage.focusFullSiteUrl();
            await expect(fullSitePage.fullSiteUrlInput).toBeFocused();

            await fullSitePage.focusFullSiteSubmitBtn();
            await expect(fullSitePage.fullSiteSubmitBtn).toBeFocused();
        });
    });
}); 