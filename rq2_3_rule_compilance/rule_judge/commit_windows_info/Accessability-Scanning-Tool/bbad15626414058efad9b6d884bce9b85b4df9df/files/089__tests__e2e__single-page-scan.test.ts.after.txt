import { test, expect } from '@playwright/test';
import { SinglePageScanPage } from './pages/SinglePageScanPage';
import { setupSinglePageTest, cleanupTest } from './setup/test-setup';

test.describe('Single Page Scan E2E Tests', () => {
    let singlePagePage: SinglePageScanPage;

    test.beforeEach(async ({ page }) => {
        await setupSinglePageTest(page);
        singlePagePage = new SinglePageScanPage(page);
    });

    test.afterEach(async ({ page }) => {
        await cleanupTest(page);
    });

    test.describe('Page Loading', () => {
        test('should load the single page scan page successfully', async ({ page }) => {
            await singlePagePage.expectPageLoaded();
        });

        test('should display the single page scan form', async ({ page }) => {
            await expect(singlePagePage.singlePageForm).toBeVisible();
            await expect(singlePagePage.singlePageUrlInput).toBeVisible();
            await expect(singlePagePage.singlePageWcagLevelSelect).toBeVisible();
            await expect(singlePagePage.singlePageSubmitBtn).toBeVisible();
        });
    });

    test.describe('Form Functionality', () => {
        test('should accept valid URL input', async ({ page }) => {
            await singlePagePage.fillSinglePageUrl('https://example.com/page');
            await singlePagePage.expectSinglePageUrlValue('https://example.com/page');
        });

        test('should allow WCAG level selection', async ({ page }) => {
            await singlePagePage.selectWcagLevel('WCAG2AAA');
            await expect(singlePagePage.singlePageWcagLevelSelect).toHaveValue('WCAG2AAA');
        });

        test('should submit form with valid data', async ({ page }) => {
            await singlePagePage.startSinglePageScan('https://example.com/page', 'WCAG2AA');
            // The form should submit successfully (we don't test the actual scan here)
        });
    });

    test.describe('Accessibility', () => {
        test('should have accessible form elements', async ({ page }) => {
            await singlePagePage.expectFormAccessibility();
        });

        test('should support keyboard navigation', async ({ page }) => {
            await singlePagePage.focusSinglePageUrl();
            await expect(singlePagePage.singlePageUrlInput).toBeFocused();

            await singlePagePage.focusSinglePageSubmitBtn();
            await expect(singlePagePage.singlePageSubmitBtn).toBeFocused();
        });
    });
}); 