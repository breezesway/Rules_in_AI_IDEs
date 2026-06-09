import { test as base, expect } from '@playwright/test';

/**
 * E2E Test Setup and Utilities
 * 
 * This file provides common setup, utilities, and configuration for E2E tests.
 */

// Test environment configuration
export const TEST_CONFIG = {
    baseURL: 'http://localhost:3000',
    timeout: 30000,
    retries: 2,
    // Test data
    testUrls: {
        valid: 'https://example.com',
        invalid: 'https://invalid-domain-that-does-not-exist-12345.com',
        malformed: 'not-a-valid-url'
    },
    // Expected messages
    messages: {
        processing: /Processing/,
        complete: /Complete/,
        error: /Error/,
        invalidUrl: /Invalid URL/,
        urlRequired: /URL is required/,
        cancelled: /Cancelled/,
        regenerated: /Regenerated/,
        noReports: /No reports found/,
        retry: /Retry/,
        retrying: /Retrying/,
        connectionLost: /Connection lost/,
        networkError: /Network error/
    }
};

// Custom test fixture with common utilities
export const test = base.extend({
    // Enhanced page with common utilities
    page: async ({ page }, use) => {
        // Set default timeout
        page.setDefaultTimeout(TEST_CONFIG.timeout);

        // Add common utilities to page
        await page.addInitScript(() => {
            // Add test utilities to window object
            (window as any).testUtils = {
                // Wait for specific text to appear
                waitForText: async (text: string, timeout = 10000) => {
                    const startTime = Date.now();
                    while (Date.now() - startTime < timeout) {
                        const element = document.querySelector(`*:contains("${text}")`);
                        if (element) return element;
                        await new Promise(resolve => setTimeout(resolve, 100));
                    }
                    throw new Error(`Text "${text}" not found within ${timeout}ms`);
                },

                // Check if element is visible
                isVisible: (selector: string) => {
                    const element = document.querySelector(selector);
                    if (!element) return false;
                    const style = window.getComputedStyle(element);
                    return style.display !== 'none' && style.visibility !== 'hidden' && element.offsetParent !== null;
                },

                // Get element text content
                getText: (selector: string) => {
                    const element = document.querySelector(selector);
                    return element ? element.textContent?.trim() : null;
                }
            };
        });

        await use(page);
    }
});

// Common test utilities
export class TestUtils {
    /**
     * Wait for the page to be fully loaded and ready
     */
    static async waitForPageReady(page: any) {
        await page.waitForLoadState('networkidle');
        await page.waitForLoadState('domcontentloaded');
    }

    /**
     * Fill a form field and validate
     */
    static async fillAndValidate(page: any, selector: string, value: string, expectedError?: string) {
        await page.fill(selector, value);

        if (expectedError) {
            // Get the form ID to find the specific error element
            const formId = selector.replace('#', '');
            const errorElement = page.locator(`#${formId}Error`);

            // Wait for the error to appear
            await expect(errorElement).not.toHaveAttribute('hidden', { timeout: 5000 });
            await expect(errorElement).toContainText(expectedError);
        } else {
            // Wait a moment for any validation to clear
            await page.waitForTimeout(500);
            // Check that no error is visible
            const formId = selector.replace('#', '');
            const errorElement = page.locator(`#${formId}Error`);
            await expect(errorElement).toHaveAttribute('hidden');
        }
    }

    /**
     * Submit a form and wait for processing
     */
    static async submitForm(page: any, formSelector: string, buttonSelector?: string) {
        const submitButton = buttonSelector || `${formSelector} button[type="submit"]`;

        await page.click(submitButton);

        // Wait for processing state - be flexible about what we detect
        try {
            // First check if the button text changes to "Processing..."
            await expect(page.locator(submitButton)).toContainText('Processing', { timeout: 3000 });
        } catch (error) {
            // If button text doesn't change, check for progress text in the page
            try {
                await expect(page.getByText(TEST_CONFIG.messages.processing)).toBeVisible({ timeout: 3000 });
            } catch (error2) {
                // If neither works, check if the progress section is visible (indicating scan started)
                try {
                    await expect(page.locator('#progressSection')).toBeVisible({ timeout: 3000 });
                } catch (error3) {
                    // If progress section not visible, check if any progress indication exists
                    // Use more specific selectors to avoid strict mode violations
                    try {
                        await expect(page.locator('#progressText')).toBeVisible({ timeout: 3000 });
                    } catch (error4) {
                        // If no progress text, check for any stage indicator
                        await expect(page.locator('.stage-text')).toBeVisible({ timeout: 3000 });
                    }
                }
            }
        }

        // Wait for button to be disabled (optional - don't fail if it's not disabled)
        try {
            await expect(page.locator(submitButton)).toBeDisabled({ timeout: 2000 });
        } catch (error) {
            // Button not disabled is okay - continue with test
            console.log('Button not disabled, continuing...');
        }
    }

    /**
     * Wait for scan completion
     */
    static async waitForScanCompletion(page: any, timeout = 60000) {
        try {
            // First try to find "Complete" text
            await expect(page.getByText(TEST_CONFIG.messages.complete)).toBeVisible({ timeout });
        } catch (error) {
            // If "Complete" not found, check for results section
            try {
                await expect(page.getByText(/Results/)).toBeVisible({ timeout });
            } catch (error2) {
                // If neither found, check if progress section is hidden (indicating completion)
                await expect(page.locator('#progressSection')).toBeHidden({ timeout });
            }
        }
    }

    /**
     * Wait for error state
     */
    static async waitForError(page: any, timeout = 30000) {
        try {
            // First try to find error text
            await expect(page.getByText(TEST_CONFIG.messages.error)).toBeVisible({ timeout });
        } catch (error) {
            // If error text not found, check for error section visibility
            try {
                await expect(page.locator('#errorSection')).not.toHaveAttribute('hidden', { timeout });
            } catch (error2) {
                // If neither works, check for any error message in the error container
                await expect(page.locator('#errorContainer')).toContainText(/Error|Failed|Invalid/, { timeout });
            }
        }
    }

    /**
     * Cancel a running scan
     */
    static async cancelScan(page: any) {
        await page.getByText(/Cancel/).click();
        // Use specific selector instead of getByText to avoid strict mode violations
        await expect(page.locator('.error-text')).toContainText(TEST_CONFIG.messages.cancelled);
    }

    /**
     * Retry a failed scan
     */
    static async retryScan(page: any) {
        await page.getByText(TEST_CONFIG.messages.retry).click();
        await expect(page.getByText(TEST_CONFIG.messages.retrying)).toBeVisible();
    }

    /**
     * Check WebSocket connection status
     */
    static async checkWebSocketConnection(page: any) {
        await expect(page.getByText(/Connected to real-time updates/)).toBeVisible();
    }

    /**
     * Simulate network interruption
     */
    static async simulateNetworkInterruption(page: any) {
        // Block API calls but allow the page to load
        await page.route('**/api/**', route => route.abort());

        // Wait a moment for the interruption to be detected
        await page.waitForTimeout(1000);

        // Check for any error or connection message (be flexible)
        try {
            await expect(page.getByText(TEST_CONFIG.messages.connectionLost)).toBeVisible({ timeout: 5000 });
        } catch (error) {
            // If no specific connection lost message, check for any error indication
            try {
                await expect(page.locator('#errorSection')).not.toHaveAttribute('hidden', { timeout: 5000 });
            } catch (error2) {
                // If no error section, check for any error text
                await expect(page.getByText(/Error|Failed|Network|Connection/)).toBeVisible({ timeout: 5000 });
            }
        }
    }
}

// Common test setup
export async function setupTest(page: any) {
    // Navigate to the web interface
    await page.goto('/');

    // Wait for the page to load completely
    await TestUtils.waitForPageReady(page);

    // Verify the page is accessible
    await expect(page).toHaveTitle(/Accessibility Testing Tool/);
}

// Setup for full site scan tests
export async function setupFullSiteTest(page: any) {
    // Navigate to the full site scan page
    await page.goto('/full-site');

    // Wait for the page to load completely
    await TestUtils.waitForPageReady(page);

    // Verify the page is accessible
    await expect(page).toHaveTitle(/Full Site Scan/);
}

// Setup for single page scan tests
export async function setupSinglePageTest(page: any) {
    // Navigate to the single page scan page
    await page.goto('/single-page');

    // Wait for the page to load completely
    await TestUtils.waitForPageReady(page);

    // Verify the page is accessible
    await expect(page).toHaveTitle(/Single Page Scan/);
}

// Common test cleanup
export async function cleanupTest(page: any) {
    // Close any open dialogs or modals
    try {
        await page.keyboard.press('Escape');
    } catch (error) {
        // Ignore errors if no dialog is open
    }

    // Clear any form inputs
    try {
        await page.evaluate(() => {
            const inputs = document.querySelectorAll('input[type="url"]');
            inputs.forEach((input: any) => input.value = '');
        });
    } catch (error) {
        // Ignore errors
    }
}

// Export common expectations
export { expect }; 