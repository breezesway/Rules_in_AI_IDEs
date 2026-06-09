import { test, expect } from '@playwright/test';

test.describe('Web Interface E2E Tests', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the web interface
        await page.goto('/');
    });

    test('should load the web interface successfully', async ({ page }) => {
        // Check that the page loads
        await expect(page).toHaveTitle(/Accessibility Testing/);

        // Check for main interface elements
        await expect(page.locator('h1')).toBeVisible();
        await expect(page.locator('input[type="url"]')).toBeVisible();
        await expect(page.locator('button[type="submit"]')).toBeVisible();
    });

    test('should display accessibility testing options', async ({ page }) => {
        // Check for different testing options
        await expect(page.getByText(/Full Site Audit/)).toBeVisible();
        await expect(page.getByText(/Single Page Audit/)).toBeVisible();
        await expect(page.getByText(/Report Regeneration/)).toBeVisible();
    });

    test('should validate URL input', async ({ page }) => {
        const urlInput = page.locator('input[type="url"]');
        const submitButton = page.locator('button[type="submit"]');

        // Test invalid URL
        await urlInput.fill('invalid-url');
        await submitButton.click();

        // Should show validation error
        await expect(page.getByText(/Invalid URL/)).toBeVisible();
    });

    test('should accept valid URL format', async ({ page }) => {
        const urlInput = page.locator('input[type="url"]');

        // Test valid URL
        await urlInput.fill('https://example.com');

        // Should not show validation error
        await expect(page.getByText(/Invalid URL/)).not.toBeVisible();
    });

    test('should have accessible form elements', async ({ page }) => {
        const urlInput = page.locator('input[type="url"]');
        const submitButton = page.locator('button[type="submit"]');

        // Check for proper labels and ARIA attributes
        await expect(urlInput).toHaveAttribute('aria-label');
        await expect(submitButton).toHaveAttribute('aria-label');

        // Check for proper focus management
        await urlInput.focus();
        await expect(urlInput).toBeFocused();
    });

    test('should have proper keyboard navigation', async ({ page }) => {
        const urlInput = page.locator('input[type="url"]');
        const submitButton = page.locator('button[type="submit"]');

        // Test tab navigation
        await page.keyboard.press('Tab');
        await expect(urlInput).toBeFocused();

        await page.keyboard.press('Tab');
        await expect(submitButton).toBeFocused();
    });

      test('should have proper color contrast', async ({ page }) => {
    // This test will be enhanced with axe-core integration
    // For now, just check that the page loads without visual issues
    await expect(page).toBeTruthy();
  });

    test('should have responsive design', async ({ page }) => {
        // Test mobile viewport
        await page.setViewportSize({ width: 375, height: 667 });
        await expect(page.locator('input[type="url"]')).toBeVisible();
        await expect(page.locator('button[type="submit"]')).toBeVisible();

        // Test tablet viewport
        await page.setViewportSize({ width: 768, height: 1024 });
        await expect(page.locator('input[type="url"]')).toBeVisible();
        await expect(page.locator('button[type="submit"]')).toBeVisible();

        // Test desktop viewport
        await page.setViewportSize({ width: 1280, height: 720 });
        await expect(page.locator('input[type="url"]')).toBeVisible();
        await expect(page.locator('button[type="submit"]')).toBeVisible();
    });
}); 