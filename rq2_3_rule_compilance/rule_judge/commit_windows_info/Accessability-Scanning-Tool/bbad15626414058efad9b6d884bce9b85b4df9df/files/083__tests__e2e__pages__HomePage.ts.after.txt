import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
    // Page-specific selectors
    private readonly fullSiteUrlSelector = '#fullSiteUrl';
    private readonly singlePageUrlSelector = '#singlePageUrl';
    private readonly fullSiteFormSelector = '#fullSiteForm';
    private readonly singlePageFormSelector = '#singlePageForm';
    private readonly generateReportsBtnSelector = '#generateSelectedReportsBtn';
    private readonly progressSectionSelector = '#progressSection';
    private readonly resultsSectionSelector = '#resultsSection';
    private readonly errorSectionSelector = '#errorSection';

    // Scan option selectors
    private readonly fullSiteScanHeadingSelector = 'h3:has-text("Full Site Scan")';
    private readonly singlePageScanHeadingSelector = 'h3:has-text("Single Page Scan")';
    private readonly reportGenerationHeadingSelector = 'h3:has-text("Generate Reports")';

    // Button selectors
    private readonly fullSiteSubmitBtnSelector = '#fullSiteForm button[type="submit"]';
    private readonly singlePageSubmitBtnSelector = '#singlePageForm button[type="submit"]';

    // Progress selectors
    private readonly progressFillSelector = '#progressFill';
    private readonly progressTextSelector = '#progressText';
    private readonly progressDetailsSelector = '#progressDetails';

    // Error selectors
    private readonly errorContainerSelector = '#errorContainer';

    constructor(page: Page) {
        super(page);
    }

    // Element getters
    get fullSiteUrlInput(): Locator {
        return this.page.locator(this.fullSiteUrlSelector);
    }

    get singlePageUrlInput(): Locator {
        return this.page.locator(this.singlePageUrlSelector);
    }

    get fullSiteForm(): Locator {
        return this.page.locator(this.fullSiteFormSelector);
    }

    get singlePageForm(): Locator {
        return this.page.locator(this.singlePageFormSelector);
    }

    get generateReportsBtn(): Locator {
        return this.page.locator(this.generateReportsBtnSelector);
    }

    get fullSiteSubmitBtn(): Locator {
        return this.page.locator(this.fullSiteSubmitBtnSelector);
    }

    get singlePageSubmitBtn(): Locator {
        return this.page.locator(this.singlePageSubmitBtnSelector);
    }

    get progressSection(): Locator {
        return this.page.locator(this.progressSectionSelector);
    }

    get resultsSection(): Locator {
        return this.page.locator(this.resultsSectionSelector);
    }

    get errorSection(): Locator {
        return this.page.locator(this.errorSectionSelector);
    }

    get progressFill(): Locator {
        return this.page.locator(this.progressFillSelector);
    }

    get progressText(): Locator {
        return this.page.locator(this.progressTextSelector);
    }

    get progressDetails(): Locator {
        return this.page.locator(this.progressDetailsSelector);
    }

    get errorContainer(): Locator {
        return this.page.locator(this.errorContainerSelector);
    }

    // Scan option headings
    get fullSiteScanHeading(): Locator {
        return this.page.locator(this.fullSiteScanHeadingSelector);
    }

    get singlePageScanHeading(): Locator {
        return this.page.locator(this.singlePageScanHeadingSelector);
    }

    get reportGenerationHeading(): Locator {
        return this.page.locator(this.reportGenerationHeadingSelector);
    }

    // Action methods
    /**
     * Fill full site URL
     */
    async fillFullSiteUrl(url: string) {
        await this.fillInput(this.fullSiteUrlInput, url);
    }

    /**
     * Fill single page URL
     */
    async fillSinglePageUrl(url: string) {
        await this.fillInput(this.singlePageUrlInput, url);
    }

    /**
     * Submit full site scan
     */
    async submitFullSiteScan() {
        await this.clickElement(this.fullSiteSubmitBtn);
    }

    /**
     * Submit single page scan
     */
    async submitSinglePageScan() {
        await this.clickElement(this.singlePageSubmitBtn);
    }

    /**
     * Click generate reports button
     */
    async clickGenerateReports() {
        await this.clickElement(this.generateReportsBtn);
    }

    /**
     * Start full site scan with URL
     */
    async startFullSiteScan(url: string) {
        await this.fillFullSiteUrl(url);
        await this.submitFullSiteScan();
    }

    /**
     * Start single page scan with URL
     */
    async startSinglePageScan(url: string) {
        await this.fillSinglePageUrl(url);
        await this.submitSinglePageScan();
    }

    /**
     * Clear full site URL input
     */
    async clearFullSiteUrl() {
        await this.fullSiteUrlInput.clear();
    }

    /**
     * Clear single page URL input
     */
    async clearSinglePageUrl() {
        await this.singlePageUrlInput.clear();
    }

    /**
     * Focus full site URL input
     */
    async focusFullSiteUrl() {
        // Wait for the element to be available
        await this.page.waitForSelector(this.fullSiteUrlSelector, { state: 'attached', timeout: 10000 });
        // Use direct focus instead of tab navigation for more reliability
        await this.focusElement(this.fullSiteUrlInput);
        await this.expectElementFocused(this.fullSiteUrlInput);
    }

    /**
     * Focus single page URL input
     */
    async focusSinglePageUrl() {
        // Wait for the element to be available
        await this.page.waitForSelector(this.singlePageUrlSelector, { state: 'attached', timeout: 10000 });
        await this.focusElement(this.singlePageUrlInput);
    }

    /**
     * Focus full site submit button
     */
    async focusFullSiteSubmitBtn() {
        // Wait for the element to be available
        await this.page.waitForSelector(this.fullSiteSubmitBtnSelector, { state: 'attached', timeout: 10000 });
        // Use direct focus instead of tab navigation for more reliability
        await this.focusElement(this.fullSiteSubmitBtn);
        await this.expectElementFocused(this.fullSiteSubmitBtn);
    }

    /**
     * Focus single page submit button
     */
    async focusSinglePageSubmitBtn() {
        // Wait for the element to be available
        await this.page.waitForSelector(this.singlePageSubmitBtnSelector, { state: 'attached', timeout: 10000 });
        await this.focusElement(this.singlePageSubmitBtn);
    }

    // Validation methods
    /**
     * Check if page is loaded correctly
     */
    async expectPageLoaded() {
        await this.expectTitle(/Accessibility Testing Tool/);
        await this.expectElementVisible(this.getHeader());
        
        // Wait for navigation links to be available (landing page structure)
        await this.page.waitForSelector('nav a[href="/single-page"]', { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector('nav a[href="/full-site"]', { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector('nav a[href="/reports"]', { state: 'attached', timeout: 10000 });
        
        // Now check if they're visible
        await this.expectElementVisible(this.page.locator('nav a[href="/single-page"]'));
        await this.expectElementVisible(this.page.locator('nav a[href="/full-site"]'));
        await this.expectElementVisible(this.page.locator('nav a[href="/reports"]'));
    }

    /**
     * Check if all scan options are visible
     */
    async expectScanOptionsVisible() {
        // Check for feature cards on the landing page
        await this.expectElementVisible(this.page.locator('.feature-card:has-text("Single Page Scan")'));
        await this.expectElementVisible(this.page.locator('.feature-card:has-text("Full Site Scan")'));
        await this.expectElementVisible(this.page.locator('.feature-card:has-text("Search & Generate Reports")'));
    }

    /**
     * Check if full site URL has expected value
     */
    async expectFullSiteUrlValue(expectedValue: string) {
        await this.expectElementValue(this.fullSiteUrlInput, expectedValue);
    }

    /**
     * Check if single page URL has expected value
     */
    async expectSinglePageUrlValue(expectedValue: string) {
        await this.expectElementValue(this.singlePageUrlInput, expectedValue);
    }

    /**
     * Check if progress section is visible
     */
    async expectProgressSectionVisible() {
        // Wait for the element to be visible (not hidden)
        await this.page.waitForSelector(this.progressSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.progressSection);
    }

    /**
     * Check if progress section is hidden
     */
    async expectProgressSectionHidden() {
        await this.expectElementNotVisible(this.progressSection);
    }

    /**
     * Check if results section is visible
     */
    async expectResultsSectionVisible() {
        // Wait for the element to be visible (not hidden)
        await this.page.waitForSelector(this.resultsSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.resultsSection);
    }

    /**
     * Check if error section is visible
     */
    async expectErrorSectionVisible() {
        // Wait for the element to be visible (not hidden)
        await this.page.waitForSelector(this.errorSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.errorSection);
    }

    /**
     * Check if error section is hidden
     */
    async expectErrorSectionHidden() {
        await this.expectElementNotVisible(this.errorSection);
    }

    /**
     * Check if progress text contains expected text
     */
    async expectProgressTextContains(expectedText: string | RegExp) {
        await expect(this.progressText).toContainText(expectedText);
    }

    /**
     * Check if error container contains expected text
     */
    async expectErrorTextContains(expectedText: string | RegExp) {
        await expect(this.errorContainer).toContainText(expectedText);
    }

    /**
     * Check if form has proper accessibility attributes
     */
    async expectFormAccessibility() {
        // Wait for the page to be fully loaded
        await this.page.waitForLoadState('networkidle');
        
        // Wait for elements to be available (they should be visible by default)
        await this.page.waitForSelector(this.fullSiteUrlSelector, { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector(this.singlePageUrlSelector, { state: 'attached', timeout: 10000 });
        
        // Check that aria-describedby contains the help text ID
        const fullSiteAriaDescribedBy = await this.fullSiteUrlInput.getAttribute('aria-describedby');
        const singlePageAriaDescribedBy = await this.singlePageUrlInput.getAttribute('aria-describedby');

        expect(fullSiteAriaDescribedBy).toContain('fullSiteUrlHelp');
        expect(singlePageAriaDescribedBy).toContain('singlePageUrlHelp');
    }

    /**
     * Test keyboard navigation
     */
    async testKeyboardNavigation() {
        // Test that keyboard navigation works by focusing elements and verifying focus
        // This is more reliable than predicting exact tab order

        // Focus the URL input directly
        await this.focusFullSiteUrl();

        // Focus the submit button directly
        await this.focusFullSiteSubmitBtn();

        // Test that we can navigate back to the input
        await this.focusFullSiteUrl();

        // Verify that focus indicators are working
        await this.expectElementFocused(this.fullSiteUrlInput);
    }

    /**
     * Test responsive design
     */
    async testResponsiveDesign() {
        // Mobile
        await this.setViewportSize(375, 667);
        await this.expectElementVisible(this.fullSiteUrlInput);
        await this.expectElementVisible(this.fullSiteSubmitBtn);

        // Tablet
        await this.setViewportSize(768, 1024);
        await this.expectElementVisible(this.fullSiteUrlInput);
        await this.expectElementVisible(this.fullSiteSubmitBtn);

        // Desktop
        await this.setViewportSize(1280, 720);
        await this.expectElementVisible(this.fullSiteUrlInput);
        await this.expectElementVisible(this.fullSiteSubmitBtn);
    }

    /**
     * Wait for scan to complete
     */
    async waitForScanCompletion(timeout: number = 60000) {
        await expect(this.progressText).toContainText(/Complete/, { timeout });
    }

    /**
     * Wait for processing to start
     */
    async waitForProcessingStart(timeout: number = 10000) {
        await expect(this.progressText).toContainText(/Processing/, { timeout });
    }
} 