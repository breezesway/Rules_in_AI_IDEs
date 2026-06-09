import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class FullSiteScanPage extends BasePage {
    // Page-specific selectors
    private readonly fullSiteUrlSelector = '#fullSiteUrl';
    private readonly fullSiteFormSelector = '#fullSiteForm';
    private readonly fullSiteWcagLevelSelector = '#fullSiteWcagLevel';
    private readonly progressSectionSelector = '#progressSection';
    private readonly resultsSectionSelector = '#resultsSection';
    private readonly errorSectionSelector = '#errorSection';

    // Button selectors
    private readonly fullSiteSubmitBtnSelector = '#fullSiteForm button[type="submit"]';

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

    get fullSiteForm(): Locator {
        return this.page.locator(this.fullSiteFormSelector);
    }

    get fullSiteWcagLevelSelect(): Locator {
        return this.page.locator(this.fullSiteWcagLevelSelector);
    }

    get fullSiteSubmitBtn(): Locator {
        return this.page.locator(this.fullSiteSubmitBtnSelector);
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

    // Form interaction methods
    async fillFullSiteUrl(url: string) {
        await this.fullSiteUrlInput.fill(url);
    }

    async selectWcagLevel(level: string) {
        await this.fullSiteWcagLevelSelect.selectOption(level);
    }

    async submitFullSiteScan() {
        await this.fullSiteSubmitBtn.click();
    }

    async startFullSiteScan(url: string, wcagLevel: string = 'WCAG2AA') {
        await this.fillFullSiteUrl(url);
        await this.selectWcagLevel(wcagLevel);
        await this.submitFullSiteScan();
    }

    async clearFullSiteUrl() {
        await this.fullSiteUrlInput.clear();
    }

    async focusFullSiteUrl() {
        await this.fullSiteUrlInput.focus();
    }

    async focusFullSiteSubmitBtn() {
        await this.fullSiteSubmitBtn.focus();
    }

    // Page validation methods
    async expectPageLoaded() {
        await this.expectTitle(/Full Site Scan/);
        await this.expectElementVisible(this.getHeader());

        // Wait for form elements to be available
        await this.page.waitForSelector(this.fullSiteUrlSelector, { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector(this.fullSiteWcagLevelSelector, { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector(this.fullSiteSubmitBtnSelector, { state: 'attached', timeout: 10000 });

        // Now check if they're visible
        await this.expectElementVisible(this.fullSiteUrlInput);
        await this.expectElementVisible(this.fullSiteWcagLevelSelect);
        await this.expectElementVisible(this.fullSiteSubmitBtn);
    }

    async expectFullSiteUrlValue(expectedValue: string) {
        await this.expectElementValue(this.fullSiteUrlInput, expectedValue);
    }

    async expectProgressSectionVisible() {
        await this.page.waitForSelector(this.progressSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.progressSection);
    }

    async expectProgressSectionHidden() {
        await this.expectElementNotVisible(this.progressSection);
    }

    async expectResultsSectionVisible() {
        await this.page.waitForSelector(this.resultsSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.resultsSection);
    }

    async expectErrorSectionVisible() {
        await this.page.waitForSelector(this.errorSectionSelector + ':not([hidden])', { timeout: 10000 });
        await this.expectElementVisible(this.errorSection);
    }

    async expectErrorSectionHidden() {
        await this.expectElementNotVisible(this.errorSection);
    }

    async expectProgressTextContains(expectedText: string | RegExp) {
        await expect(this.progressText).toContainText(expectedText);
    }

    async expectErrorTextContains(expectedText: string | RegExp) {
        await expect(this.errorContainer).toContainText(expectedText);
    }

    // Form accessibility testing
    async expectFormAccessibility() {
        // Wait for the page to be fully loaded
        await this.expectPageLoaded();

        // Check for proper form structure
        await expect(this.fullSiteForm).toBeVisible();
        await expect(this.fullSiteUrlInput).toBeVisible();
        await expect(this.fullSiteWcagLevelSelect).toBeVisible();
        await expect(this.fullSiteSubmitBtn).toBeVisible();

        // Check for proper labels
        await expect(this.page.locator('label[for="fullSiteUrl"]')).toBeVisible();
        await expect(this.page.locator('label[for="fullSiteWcagLevel"]')).toBeVisible();

        // Check for proper ARIA attributes
        await expect(this.fullSiteUrlInput).toHaveAttribute('aria-describedby');
        await expect(this.fullSiteWcagLevelSelect).toHaveAttribute('aria-describedby');
    }

    // Wait methods
    async waitForScanCompletion(timeout: number = 60000) {
        await this.page.waitForSelector(this.resultsSectionSelector + ':not([hidden])', { timeout });
    }

    async waitForProcessingStart(timeout: number = 10000) {
        await this.page.waitForSelector(this.progressSectionSelector + ':not([hidden])', { timeout });
    }
} 