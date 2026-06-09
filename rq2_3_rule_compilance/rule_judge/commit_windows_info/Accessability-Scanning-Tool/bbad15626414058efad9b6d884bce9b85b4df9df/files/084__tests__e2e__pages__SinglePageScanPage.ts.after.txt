import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class SinglePageScanPage extends BasePage {
    // Page-specific selectors
    private readonly singlePageUrlSelector = '#singlePageUrl';
    private readonly singlePageFormSelector = '#singlePageForm';
    private readonly singlePageWcagLevelSelector = '#singlePageWcagLevel';
    private readonly progressSectionSelector = '#progressSection';
    private readonly resultsSectionSelector = '#resultsSection';
    private readonly errorSectionSelector = '#errorSection';

    // Button selectors
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
    get singlePageUrlInput(): Locator {
        return this.page.locator(this.singlePageUrlSelector);
    }

    get singlePageForm(): Locator {
        return this.page.locator(this.singlePageFormSelector);
    }

    get singlePageWcagLevelSelect(): Locator {
        return this.page.locator(this.singlePageWcagLevelSelector);
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

    // Form interaction methods
    async fillSinglePageUrl(url: string) {
        await this.singlePageUrlInput.fill(url);
    }

    async selectWcagLevel(level: string) {
        await this.singlePageWcagLevelSelect.selectOption(level);
    }

    async submitSinglePageScan() {
        await this.singlePageSubmitBtn.click();
    }

    async startSinglePageScan(url: string, wcagLevel: string = 'WCAG2AA') {
        await this.fillSinglePageUrl(url);
        await this.selectWcagLevel(wcagLevel);
        await this.submitSinglePageScan();
    }

    async clearSinglePageUrl() {
        await this.singlePageUrlInput.clear();
    }

    async focusSinglePageUrl() {
        await this.singlePageUrlInput.focus();
    }

    async focusSinglePageSubmitBtn() {
        await this.singlePageSubmitBtn.focus();
    }

    // Page validation methods
    async expectPageLoaded() {
        await this.expectTitle(/Single Page Scan/);
        await this.expectElementVisible(this.getHeader());

        // Wait for form elements to be available
        await this.page.waitForSelector(this.singlePageUrlSelector, { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector(this.singlePageWcagLevelSelector, { state: 'attached', timeout: 10000 });
        await this.page.waitForSelector(this.singlePageSubmitBtnSelector, { state: 'attached', timeout: 10000 });

        // Now check if they're visible
        await this.expectElementVisible(this.singlePageUrlInput);
        await this.expectElementVisible(this.singlePageWcagLevelSelect);
        await this.expectElementVisible(this.singlePageSubmitBtn);
    }

    async expectSinglePageUrlValue(expectedValue: string) {
        await this.expectElementValue(this.singlePageUrlInput, expectedValue);
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
        await expect(this.singlePageForm).toBeVisible();
        await expect(this.singlePageUrlInput).toBeVisible();
        await expect(this.singlePageWcagLevelSelect).toBeVisible();
        await expect(this.singlePageSubmitBtn).toBeVisible();

        // Check for proper labels
        await expect(this.page.locator('label[for="singlePageUrl"]')).toBeVisible();
        await expect(this.page.locator('label[for="singlePageWcagLevel"]')).toBeVisible();

        // Check for proper ARIA attributes
        await expect(this.singlePageUrlInput).toHaveAttribute('aria-describedby');
        await expect(this.singlePageWcagLevelSelect).toHaveAttribute('aria-describedby');
    }

    // Wait methods
    async waitForScanCompletion(timeout: number = 60000) {
        await this.page.waitForSelector(this.resultsSectionSelector + ':not([hidden])', { timeout });
    }

    async waitForProcessingStart(timeout: number = 10000) {
        await this.page.waitForSelector(this.progressSectionSelector + ':not([hidden])', { timeout });
    }
} 