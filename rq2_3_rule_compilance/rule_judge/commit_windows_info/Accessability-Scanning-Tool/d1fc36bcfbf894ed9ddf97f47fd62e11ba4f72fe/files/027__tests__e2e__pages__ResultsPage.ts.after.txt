import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class ResultsPage extends BasePage {
    // Results-specific selectors
    private readonly resultsSectionSelector = '#resultsSection';
    private readonly resultsContainerSelector = '#resultsContainer';
    private readonly resultsHeadingSelector = '#results-heading';

    // Error-specific selectors
    private readonly errorSectionSelector = '#errorSection';
    private readonly errorContainerSelector = '#errorContainer';
    private readonly errorHeadingSelector = '#error-heading';

    // Common result elements
    private readonly summarySectionSelector = '.summary-section';
    private readonly violationsSectionSelector = '.violations-section';
    private readonly recommendationsSectionSelector = '.recommendations-section';
    private readonly downloadSectionSelector = '.download-section';

    constructor(page: Page) {
        super(page);
    }

    // Element getters
    get resultsSection(): Locator {
        return this.page.locator(this.resultsSectionSelector);
    }

    get resultsContainer(): Locator {
        return this.page.locator(this.resultsContainerSelector);
    }

    get resultsHeading(): Locator {
        return this.page.locator(this.resultsHeadingSelector);
    }

    get errorSection(): Locator {
        return this.page.locator(this.errorSectionSelector);
    }

    get errorContainer(): Locator {
        return this.page.locator(this.errorContainerSelector);
    }

    get errorHeading(): Locator {
        return this.page.locator(this.errorHeadingSelector);
    }

    get summarySection(): Locator {
        return this.page.locator(this.summarySectionSelector);
    }

    get violationsSection(): Locator {
        return this.page.locator(this.violationsSectionSelector);
    }

    get recommendationsSection(): Locator {
        return this.page.locator(this.recommendationsSectionSelector);
    }

    get downloadSection(): Locator {
        return this.page.locator(this.downloadSectionSelector);
    }

    // Validation methods
    /**
     * Check if results section is visible
     */
    async expectResultsSectionVisible() {
        await this.expectElementVisible(this.resultsSection);
    }

    /**
     * Check if results section is hidden
     */
    async expectResultsSectionHidden() {
        await this.expectElementNotVisible(this.resultsSection);
    }

    /**
     * Check if error section is visible
     */
    async expectErrorSectionVisible() {
        await this.expectElementVisible(this.errorSection);
    }

    /**
     * Check if error section is hidden
     */
    async expectErrorSectionHidden() {
        await this.expectElementNotVisible(this.errorSection);
    }

    /**
     * Check if results container contains expected text
     */
    async expectResultsContain(expectedText: string | RegExp) {
        await expect(this.resultsContainer).toContainText(expectedText);
    }

    /**
     * Check if error container contains expected text
     */
    async expectErrorContain(expectedText: string | RegExp) {
        await expect(this.errorContainer).toContainText(expectedText);
    }

    /**
     * Check if results heading is visible
     */
    async expectResultsHeadingVisible() {
        await this.expectElementVisible(this.resultsHeading);
    }

    /**
     * Check if error heading is visible
     */
    async expectErrorHeadingVisible() {
        await this.expectElementVisible(this.errorHeading);
    }

    /**
     * Check if summary section is visible
     */
    async expectSummarySectionVisible() {
        await this.expectElementVisible(this.summarySection);
    }

    /**
     * Check if violations section is visible
     */
    async expectViolationsSectionVisible() {
        await this.expectElementVisible(this.violationsSection);
    }

    /**
     * Check if recommendations section is visible
     */
    async expectRecommendationsSectionVisible() {
        await this.expectElementVisible(this.recommendationsSection);
    }

    /**
     * Check if download section is visible
     */
    async expectDownloadSectionVisible() {
        await this.expectElementVisible(this.downloadSection);
    }

    // Wait methods
    /**
     * Wait for results section to appear
     */
    async waitForResultsSection(timeout: number = 30000) {
        await expect(this.resultsSection).toBeVisible({ timeout });
    }

    /**
     * Wait for error section to appear
     */
    async waitForErrorSection(timeout: number = 10000) {
        await expect(this.errorSection).toBeVisible({ timeout });
    }

    /**
     * Wait for results to contain specific text
     */
    async waitForResultsText(expectedText: string | RegExp, timeout: number = 30000) {
        await expect(this.resultsContainer).toContainText(expectedText, { timeout });
    }

    /**
     * Wait for error to contain specific text
     */
    async waitForErrorText(expectedText: string | RegExp, timeout: number = 10000) {
        await expect(this.errorContainer).toContainText(expectedText, { timeout });
    }

    // Content methods
    /**
     * Get results content
     */
    async getResultsContent(): Promise<string> {
        return await this.resultsContainer.textContent() || '';
    }

    /**
     * Get error content
     */
    async getErrorContent(): Promise<string> {
        return await this.errorContainer.textContent() || '';
    }

    /**
     * Get summary content
     */
    async getSummaryContent(): Promise<string> {
        return await this.summarySection.textContent() || '';
    }

    /**
     * Get violations content
     */
    async getViolationsContent(): Promise<string> {
        return await this.violationsSection.textContent() || '';
    }

    /**
     * Get recommendations content
     */
    async getRecommendationsContent(): Promise<string> {
        return await this.recommendationsSection.textContent() || '';
    }

    // Status checking methods
    /**
     * Check if scan was successful
     */
    async isScanSuccessful(): Promise<boolean> {
        const resultsVisible = await this.resultsSection.isVisible();
        const errorVisible = await this.errorSection.isVisible();
        return resultsVisible && !errorVisible;
    }

    /**
     * Check if scan failed
     */
    async isScanFailed(): Promise<boolean> {
        const errorVisible = await this.errorSection.isVisible();
        return errorVisible;
    }

    /**
     * Check if results contain violations
     */
    async hasViolations(): Promise<boolean> {
        const content = await this.getViolationsContent();
        return content.includes('violation') || content.includes('error') || content.includes('issue');
    }

    /**
     * Check if results contain recommendations
     */
    async hasRecommendations(): Promise<boolean> {
        const content = await this.getRecommendationsContent();
        return content.includes('recommendation') || content.includes('suggestion') || content.includes('improvement');
    }

    /**
     * Check if download links are available
     */
    async hasDownloadLinks(): Promise<boolean> {
        const content = await this.downloadSection.textContent() || '';
        return content.includes('download') || content.includes('PDF') || content.includes('JSON');
    }

    // Download methods
    /**
     * Click download PDF button
     */
    async downloadPDF() {
        const pdfButton = this.page.locator('button:has-text("Download PDF")');
        if (await pdfButton.count() > 0) {
            await this.clickElement(pdfButton);
        }
    }

    /**
     * Click download JSON button
     */
    async downloadJSON() {
        const jsonButton = this.page.locator('button:has-text("Download JSON")');
        if (await jsonButton.count() > 0) {
            await this.clickElement(jsonButton);
        }
    }

    /**
     * Click download summary button
     */
    async downloadSummary() {
        const summaryButton = this.page.locator('button:has-text("Download Summary")');
        if (await summaryButton.count() > 0) {
            await this.clickElement(summaryButton);
        }
    }

    // Navigation methods
    /**
     * Click retry button
     */
    async clickRetry() {
        const retryButton = this.page.locator('button:has-text("Retry")');
        if (await retryButton.count() > 0) {
            await this.clickElement(retryButton);
        }
    }

    /**
     * Click new scan button
     */
    async clickNewScan() {
        const newScanButton = this.page.locator('button:has-text("New Scan")');
        if (await newScanButton.count() > 0) {
            await this.clickElement(newScanButton);
        }
    }

    /**
     * Click back to home button
     */
    async clickBackToHome() {
        const backButton = this.page.locator('button:has-text("Back to Home")');
        if (await backButton.count() > 0) {
            await this.clickElement(backButton);
        }
    }

    // Accessibility methods
    /**
     * Check if results are accessible
     */
    async expectResultsAccessible() {
        // Check for proper heading structure
        await this.expectElementVisible(this.resultsHeading);

        // Check for proper ARIA attributes
        await this.expectElementAttribute(this.resultsSection, 'aria-labelledby', 'results-heading');

        // Check for proper semantic structure
        await this.expectElementVisible(this.summarySection);
        await this.expectElementVisible(this.violationsSection);
        await this.expectElementVisible(this.recommendationsSection);
    }

    /**
     * Check if error is accessible
     */
    async expectErrorAccessible() {
        // Check for proper heading structure
        await this.expectElementVisible(this.errorHeading);

        // Check for proper ARIA attributes
        await this.expectElementAttribute(this.errorSection, 'aria-labelledby', 'error-heading');

        // Check for proper error announcement
        await this.expectElementVisible(this.errorContainer);
    }

    // Content validation methods
    /**
     * Validate scan results structure
     */
    async validateScanResults() {
        await this.expectResultsSectionVisible();
        await this.expectResultsHeadingVisible();
        await this.expectSummarySectionVisible();
        await this.expectViolationsSectionVisible();
        await this.expectRecommendationsSectionVisible();
        await this.expectDownloadSectionVisible();
    }

    /**
     * Validate error structure
     */
    async validateErrorStructure() {
        await this.expectErrorSectionVisible();
        await this.expectErrorHeadingVisible();
        await this.expectElementVisible(this.errorContainer);
    }

    /**
     * Check for specific result content
     */
    async expectResultContains(keyword: string) {
        await this.expectResultsContain(new RegExp(keyword, 'i'));
    }

    /**
     * Check for specific error content
     */
    async expectErrorContains(keyword: string) {
        await this.expectErrorContain(new RegExp(keyword, 'i'));
    }
} 