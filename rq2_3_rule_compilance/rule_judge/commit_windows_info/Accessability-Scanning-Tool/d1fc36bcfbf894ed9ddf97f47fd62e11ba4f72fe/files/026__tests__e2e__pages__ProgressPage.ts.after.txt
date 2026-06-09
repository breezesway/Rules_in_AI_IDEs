import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class ProgressPage extends BasePage {
    // Progress-specific selectors
    private readonly progressSectionSelector = '#progressSection';
    private readonly progressFillSelector = '#progressFill';
    private readonly progressTextSelector = '#progressText';
    private readonly progressDetailsSelector = '#progressDetails';
    private readonly progressStagesSelector = '.progress-stages';
    private readonly stageItemSelector = '.stage-item';

    // Stage-specific selectors
    private readonly browserStageSelector = '[data-stage="browser"]';
    private readonly navigationStageSelector = '[data-stage="navigation"]';
    private readonly axeStageSelector = '[data-stage="axe"]';
    private readonly pa11yStageSelector = '[data-stage="pa11y"]';
    private readonly processingStageSelector = '[data-stage="processing"]';
    private readonly reportsStageSelector = '[data-stage="reports"]';

    constructor(page: Page) {
        super(page);
    }

    // Element getters
    get progressSection(): Locator {
        return this.page.locator(this.progressSectionSelector);
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

    get progressStages(): Locator {
        return this.page.locator(this.progressStagesSelector);
    }

    get stageItems(): Locator {
        return this.page.locator(this.stageItemSelector);
    }

    // Stage-specific getters
    get browserStage(): Locator {
        return this.page.locator(this.browserStageSelector);
    }

    get navigationStage(): Locator {
        return this.page.locator(this.navigationStageSelector);
    }

    get axeStage(): Locator {
        return this.page.locator(this.axeStageSelector);
    }

    get pa11yStage(): Locator {
        return this.page.locator(this.pa11yStageSelector);
    }

    get processingStage(): Locator {
        return this.page.locator(this.processingStageSelector);
    }

    get reportsStage(): Locator {
        return this.page.locator(this.reportsStageSelector);
    }

    // Validation methods
    /**
     * Check if progress section is visible
     */
    async expectProgressSectionVisible() {
        await this.expectElementVisible(this.progressSection);
    }

    /**
     * Check if progress section is hidden
     */
    async expectProgressSectionHidden() {
        await this.expectElementNotVisible(this.progressSection);
    }

    /**
     * Check if progress text contains expected text
     */
    async expectProgressTextContains(expectedText: string | RegExp) {
        await expect(this.progressText).toContainText(expectedText);
    }

    /**
     * Check if progress details contain expected text
     */
    async expectProgressDetailsContain(expectedText: string | RegExp) {
        await expect(this.progressDetails).toContainText(expectedText);
    }

    /**
     * Check if progress fill has expected width
     */
    async expectProgressFillWidth(expectedWidth: string) {
        await expect(this.progressFill).toHaveCSS('width', expectedWidth);
    }

    /**
     * Check if all progress stages are visible
     */
    async expectAllStagesVisible() {
        await this.expectElementVisible(this.browserStage);
        await this.expectElementVisible(this.navigationStage);
        await this.expectElementVisible(this.axeStage);
        await this.expectElementVisible(this.pa11yStage);
        await this.expectElementVisible(this.processingStage);
        await this.expectElementVisible(this.reportsStage);
    }

    /**
     * Check if specific stage is active
     */
    async expectStageActive(stageLocator: Locator) {
        await expect(stageLocator).toHaveClass(/active/);
    }

    /**
     * Check if specific stage is completed
     */
    async expectStageCompleted(stageLocator: Locator) {
        await expect(stageLocator).toHaveClass(/completed/);
    }

    /**
     * Check if specific stage is pending
     */
    async expectStagePending(stageLocator: Locator) {
        await expect(stageLocator).toHaveClass(/pending/);
    }

    // Wait methods
    /**
     * Wait for progress section to appear
     */
    async waitForProgressSection(timeout: number = 10000) {
        await expect(this.progressSection).toBeVisible({ timeout });
    }

    /**
     * Wait for progress text to contain specific text
     */
    async waitForProgressText(expectedText: string | RegExp, timeout: number = 30000) {
        await expect(this.progressText).toContainText(expectedText, { timeout });
    }

    /**
     * Wait for progress details to contain specific text
     */
    async waitForProgressDetails(expectedText: string | RegExp, timeout: number = 30000) {
        await expect(this.progressDetails).toContainText(expectedText, { timeout });
    }

    /**
     * Wait for scan to complete
     */
    async waitForScanCompletion(timeout: number = 60000) {
        await this.waitForProgressText(/Complete/, timeout);
    }

    /**
     * Wait for processing to start
     */
    async waitForProcessingStart(timeout: number = 10000) {
        await this.waitForProgressText(/Processing/, timeout);
    }

    /**
     * Wait for browser initialization
     */
    async waitForBrowserInit(timeout: number = 15000) {
        await this.waitForProgressText(/Browser/, timeout);
    }

    /**
     * Wait for navigation to start
     */
    async waitForNavigationStart(timeout: number = 20000) {
        await this.waitForProgressText(/Navigation/, timeout);
    }

    /**
     * Wait for axe analysis to start
     */
    async waitForAxeAnalysis(timeout: number = 30000) {
        await this.waitForProgressText(/Axe/, timeout);
    }

    /**
     * Wait for Pa11y analysis to start
     */
    async waitForPa11yAnalysis(timeout: number = 30000) {
        await this.waitForProgressText(/Pa11y/, timeout);
    }

    /**
     * Wait for processing to start
     */
    async waitForProcessingStage(timeout: number = 30000) {
        await this.waitForProgressText(/Processing/, timeout);
    }

    /**
     * Wait for report generation to start
     */
    async waitForReportGeneration(timeout: number = 30000) {
        await this.waitForProgressText(/Reports/, timeout);
    }

    // Progress monitoring methods
    /**
     * Get current progress percentage
     */
    async getProgressPercentage(): Promise<string> {
        const width = await this.progressFill.evaluate(el =>
            getComputedStyle(el).width
        );
        return width;
    }

    /**
     * Get current progress text
     */
    async getProgressText(): Promise<string> {
        return await this.progressText.textContent() || '';
    }

    /**
     * Get current progress details
     */
    async getProgressDetails(): Promise<string> {
        return await this.progressDetails.textContent() || '';
    }

    /**
     * Check if scan is in progress
     */
    async isScanInProgress(): Promise<boolean> {
        const text = await this.getProgressText();
        return text.includes('Processing') || text.includes('Scanning');
    }

    /**
     * Check if scan is completed
     */
    async isScanCompleted(): Promise<boolean> {
        const text = await this.getProgressText();
        return text.includes('Complete') || text.includes('Finished');
    }

    /**
     * Check if scan has failed
     */
    async isScanFailed(): Promise<boolean> {
        const text = await this.getProgressText();
        return text.includes('Error') || text.includes('Failed');
    }

    // Stage monitoring methods
    /**
     * Get active stage
     */
    async getActiveStage(): Promise<string> {
        const activeStage = await this.page.locator('.stage-item.active').first();
        if (await activeStage.count() > 0) {
            return await activeStage.getAttribute('data-stage') || '';
        }
        return '';
    }

    /**
     * Get completed stages
     */
    async getCompletedStages(): Promise<string[]> {
        const completedStages = await this.page.locator('.stage-item.completed').all();
        const stages: string[] = [];
        for (const stage of completedStages) {
            const stageName = await stage.getAttribute('data-stage');
            if (stageName) {
                stages.push(stageName);
            }
        }
        return stages;
    }

    /**
     * Check if specific stage is active
     */
    async isStageActive(stageName: string): Promise<boolean> {
        const activeStage = await this.getActiveStage();
        return activeStage === stageName;
    }

    /**
     * Check if specific stage is completed
     */
    async isStageCompleted(stageName: string): Promise<boolean> {
        const completedStages = await this.getCompletedStages();
        return completedStages.includes(stageName);
    }

    // WebSocket integration methods
    /**
     * Wait for WebSocket connection
     */
    async waitForWebSocketConnection(timeout: number = 5000) {
        // This would typically wait for WebSocket connection to be established
        // For now, we'll wait for progress updates to start
        await this.waitForProgressSection(timeout);
    }

    /**
     * Wait for real-time progress update
     */
    async waitForRealTimeUpdate(timeout: number = 10000) {
        // Wait for progress text to change (indicating real-time update)
        const initialText = await this.getProgressText();
        await this.page.waitForFunction(
            (selector, initialText) => {
                const element = document.querySelector(selector);
                return element && element.textContent !== initialText;
            },
            this.progressTextSelector,
            initialText,
            { timeout }
        );
    }
} 