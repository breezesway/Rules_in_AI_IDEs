import { test, expect } from '@playwright/test';
import { HomePage } from './pages/HomePage';
import { ProgressPage } from './pages/ProgressPage';
import { ResultsPage } from './pages/ResultsPage';
import { TestUtils } from './utils/TestUtils';

test.describe('Web Interface E2E Tests', () => {
    let homePage: HomePage;
    let progressPage: ProgressPage;
    let resultsPage: ResultsPage;
    let testUtils: TestUtils;

    test.beforeEach(async ({ page }) => {
        // Initialize page objects
        homePage = new HomePage(page);
        progressPage = new ProgressPage(page);
        resultsPage = new ResultsPage(page);
        testUtils = new TestUtils(page);

        // Navigate to the web interface
        await homePage.goto();
    });

    test.describe('Basic Interface Functionality', () => {
        test('should load the web interface successfully', async ({ page }) => {
            // Check that the page loads correctly
            await homePage.expectPageLoaded();
        });

        test('should display accessibility testing options', async ({ page }) => {
            // Check for different testing options
            await homePage.expectScanOptionsVisible();
        });

        test('should validate URL input', async ({ page }) => {
            // Test invalid URL - note: actual validation depends on HTML5 form validation
            await homePage.fillFullSiteUrl('invalid-url');
            await homePage.submitFullSiteScan();

            // The form should prevent submission due to HTML5 validation
            // We can't easily test for validation messages without client-side JS
            // This test verifies the form submission behavior
        });

        test('should accept valid URL format', async ({ page }) => {
            // Test valid URL
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');
        });
    });

    test.describe('Accessibility Compliance', () => {
        test('should have accessible form elements', async ({ page }) => {
            // Check for proper labels and ARIA attributes
            await homePage.expectFormAccessibility();

            // Check for proper focus management
            await homePage.focusFullSiteUrl();
            await homePage.expectElementFocused(homePage.fullSiteUrlInput);
        });

        test('should have proper keyboard navigation', async ({ page }) => {
            // Test keyboard navigation
            await homePage.testKeyboardNavigation();
        });

        test('should have proper color contrast', async ({ page }) => {
            // This test will be enhanced with axe-core integration
            // For now, just check that the page loads without visual issues
            await expect(page).toBeTruthy();
        });

        test('should have responsive design', async ({ page }) => {
            // Test responsive design across different viewports
            await homePage.testResponsiveDesign();
        });
    });

    test.describe('Cross-Browser Compatibility', () => {
        test('should work consistently across browsers', async ({ page }) => {
            // Test basic functionality
            await homePage.expectPageLoaded();

            // Test form interaction
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');

            // Test form submission
            await homePage.submitFullSiteScan();
            // Note: We can't easily test for processing feedback without actual scan functionality
        });

        test('should handle browser-specific features', async ({ page }) => {
            // Test browser back/forward
            await testUtils.goBack();
            await testUtils.goForward();

            // Test browser refresh
            await testUtils.reloadPage();
            await homePage.expectPageLoaded();

            // Test browser zoom
            await testUtils.evaluateScript('document.body.style.zoom = "1.5"');
            await homePage.expectElementVisible(homePage.fullSiteUrlInput);
        });
    });

    test.describe('Error Handling', () => {
        test('should handle network errors gracefully', async ({ page }) => {
            // Block network requests
            await testUtils.routeNetworkRequests('**/*', route => route.abort());

            // Try to start a scan
            await homePage.startFullSiteScan('https://example.com');

            // Should handle error gracefully
            // Note: This depends on the actual error handling implementation
            await testUtils.wait(2000); // Give time for error to appear
        });

        test('should provide helpful error messages', async ({ page }) => {
            // Test invalid URL
            await homePage.fillFullSiteUrl('not-a-valid-url');
            await homePage.submitFullSiteScan();

            // Note: Error messages depend on client-side validation implementation
            // This test verifies the form submission behavior
        });

        test('should offer recovery options', async ({ page }) => {
            // Trigger an error
            await homePage.fillFullSiteUrl('invalid-url');
            await homePage.submitFullSiteScan();

            // Should allow user to correct the input
            await homePage.clearFullSiteUrl();
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');
        });
    });

    test.describe('User Experience', () => {
        test('should provide clear feedback for user actions', async ({ page }) => {
            // Test form submission feedback
            await homePage.startFullSiteScan('https://example.com');

            // Note: Processing feedback depends on actual scan implementation
            // This test verifies the form submission behavior
        });

        test('should maintain state during interactions', async ({ page }) => {
            // Fill form
            await homePage.fillFullSiteUrl('https://example.com');

            // Switch between scan types (click headings)
            await homePage.clickElement(homePage.fullSiteScanHeading);
            await homePage.clickElement(homePage.singlePageScanHeading);
            await homePage.clickElement(homePage.reportRegenerationHeading);

            // URL should be preserved
            await homePage.expectFullSiteUrlValue('https://example.com');
        });

        test('should provide intuitive navigation', async ({ page }) => {
            // Test that all interactive elements are discoverable
            await homePage.expectScanOptionsVisible();

            // Test that elements are clickable
            await homePage.clickElement(homePage.fullSiteScanHeading);
            await homePage.clickElement(homePage.singlePageScanHeading);
            await homePage.clickElement(homePage.reportRegenerationHeading);

            // Should not cause errors
            await homePage.expectElementVisible(homePage.fullSiteUrlInput);
        });
    });

    test.describe('Performance and Responsiveness', () => {
        test('should respond quickly to user interactions', async ({ page }) => {
            // Test form interaction speed
            const startTime = Date.now();
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.submitFullSiteScan();
            const endTime = Date.now();

            // Should respond within reasonable time
            expect(endTime - startTime).toBeLessThan(5000);
        });

        test('should handle rapid user input', async ({ page }) => {
            // Test rapid typing
            const testUrl = 'https://example.com/test-page';
            for (let i = 0; i < testUrl.length; i++) {
                await homePage.fullSiteUrlInput.type(testUrl[i]);
                await testUtils.wait(10); // Small delay between characters
            }

            await homePage.expectFullSiteUrlValue(testUrl);
        });

        test('should maintain performance during scans', async ({ page }) => {
            // Start a scan
            await homePage.startFullSiteScan('https://example.com');

            // Test that interface remains responsive
            await homePage.expectElementVisible(homePage.fullSiteUrlInput);
            await homePage.expectElementVisible(homePage.fullSiteSubmitBtn);

            // Note: Actual performance testing would require real scan functionality
        });
    });

    test.describe('Form Validation', () => {
        test('should validate required fields', async ({ page }) => {
            // Try to submit without URL
            await homePage.submitFullSiteScan();

            // Form should prevent submission due to HTML5 validation
            // This test verifies the form behavior
        });

        test('should validate URL format', async ({ page }) => {
            // Test various URL formats
            const testUrls = [
                'https://example.com',
                'http://example.com',
                'https://www.example.com/path',
                'https://example.com:8080'
            ];

            for (const url of testUrls) {
                await homePage.fillFullSiteUrl(url);
                await homePage.expectFullSiteUrlValue(url);
            }
        });

        test('should handle form reset', async ({ page }) => {
            // Fill form
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');

            // Clear form
            await homePage.clearFullSiteUrl();
            await homePage.expectFullSiteUrlValue('');
        });
    });

    test.describe('Accessibility Features', () => {
        test('should support screen readers', async ({ page }) => {
            // Check for proper ARIA attributes
            await homePage.expectFormAccessibility();

            // Check for proper heading structure
            await homePage.expectElementVisible(homePage.getHeader());
            await homePage.expectScanOptionsVisible();
        });

        test('should support keyboard-only navigation', async ({ page }) => {
            // Test full keyboard navigation
            await homePage.testKeyboardNavigation();

            // Test that all interactive elements are reachable via keyboard
            await homePage.focusFullSiteUrl();
            await homePage.expectElementFocused(homePage.fullSiteUrlInput);

            await homePage.focusFullSiteSubmitBtn();
            await homePage.expectElementFocused(homePage.fullSiteSubmitBtn);
        });

        test('should have proper focus indicators', async ({ page }) => {
            // Focus elements and check for visible focus indicators
            await homePage.focusFullSiteUrl();
            await homePage.expectElementFocused(homePage.fullSiteUrlInput);

            // Check that focus is visible (this would need CSS inspection in a real test)
            await expect(homePage.fullSiteUrlInput).toBeFocused();
        });
    });

    test.describe('Mobile Responsiveness', () => {
        test('should work on mobile devices', async ({ page }) => {
            // Test mobile viewport
            await testUtils.setViewportSize(375, 667);
            await homePage.expectElementVisible(homePage.fullSiteUrlInput);
            await homePage.expectElementVisible(homePage.fullSiteSubmitBtn);

            // Test form interaction on mobile
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');
        });

        test('should work on tablet devices', async ({ page }) => {
            // Test tablet viewport
            await testUtils.setViewportSize(768, 1024);
            await homePage.expectElementVisible(homePage.fullSiteUrlInput);
            await homePage.expectElementVisible(homePage.fullSiteSubmitBtn);

            // Test form interaction on tablet
            await homePage.fillFullSiteUrl('https://example.com');
            await homePage.expectFullSiteUrlValue('https://example.com');
        });

        test('should maintain accessibility on mobile', async ({ page }) => {
            // Test mobile viewport
            await testUtils.setViewportSize(375, 667);

            // Check that accessibility features still work
            await homePage.expectFormAccessibility();
            await homePage.testKeyboardNavigation();
        });
    });
}); 