import { Page, Locator, expect } from '@playwright/test';

export class BasePage {
    protected page: Page;

    // Common selectors
    protected readonly headerSelector = 'h1';
    protected readonly footerSelector = '.footer';
    protected readonly mainContentSelector = '.main';

    constructor(page: Page) {
        this.page = page;
    }

    /**
     * Navigate to the page
     */
    async goto(path: string = '/') {
        await this.page.goto(path);
        await this.page.waitForLoadState('networkidle');
    }

    /**
     * Wait for page to be fully loaded
     */
    async waitForPageLoad() {
        await this.page.waitForLoadState('networkidle');
    }

    /**
     * Get page title
     */
    async getTitle(): Promise<string> {
        return await this.page.title();
    }

    /**
     * Check if page has expected title
     */
    async expectTitle(expectedTitle: string | RegExp) {
        await expect(this.page).toHaveTitle(expectedTitle);
    }

    /**
     * Get header element
     */
    getHeader(): Locator {
        return this.page.locator(this.headerSelector);
    }

    /**
     * Get footer element
     */
    getFooter(): Locator {
        return this.page.locator(this.footerSelector);
    }

    /**
     * Get main content area
     */
    getMainContent(): Locator {
        return this.page.locator(this.mainContentSelector);
    }

    /**
     * Check if element is visible
     */
    async expectElementVisible(locator: Locator) {
        await expect(locator).toBeVisible();
    }

    /**
     * Check if element is not visible
     */
    async expectElementNotVisible(locator: Locator) {
        await expect(locator).not.toBeVisible();
    }

    /**
     * Fill input field
     */
    async fillInput(locator: Locator, value: string) {
        await locator.fill(value);
    }

    /**
     * Click element
     */
    async clickElement(locator: Locator) {
        await locator.click();
    }

    /**
     * Focus element
     */
    async focusElement(locator: Locator) {
        await locator.focus();
    }

    /**
     * Check if element is focused
     */
    async expectElementFocused(locator: Locator) {
        await expect(locator).toBeFocused();
    }

    /**
     * Get element value
     */
    async getElementValue(locator: Locator): Promise<string> {
        return await locator.inputValue();
    }

    /**
     * Check element value
     */
    async expectElementValue(locator: Locator, expectedValue: string) {
        await expect(locator).toHaveValue(expectedValue);
    }

    /**
     * Check element attribute
     */
    async expectElementAttribute(locator: Locator, attribute: string, value: string) {
        await expect(locator).toHaveAttribute(attribute, value);
    }

    /**
     * Set viewport size
     */
    async setViewportSize(width: number, height: number) {
        await this.page.setViewportSize({ width, height });
    }

    /**
     * Reload page
     */
    async reload() {
        await this.page.reload();
        await this.waitForPageLoad();
    }

    /**
     * Go back in browser history
     */
    async goBack() {
        await this.page.goBack();
        await this.waitForPageLoad();
    }

    /**
     * Go forward in browser history
     */
    async goForward() {
        await this.page.goForward();
        await this.waitForPageLoad();
    }

    /**
     * Press keyboard key
     */
    async pressKey(key: string) {
        await this.page.keyboard.press(key);
    }

    /**
     * Wait for timeout
     */
    async waitForTimeout(ms: number) {
        await this.page.waitForTimeout(ms);
    }

    /**
     * Route network requests
     */
    async routeNetworkRequests(pattern: string, handler: (route: any) => void) {
        await this.page.route(pattern, handler);
    }

    /**
     * Evaluate JavaScript in page context
     */
    async evaluateScript(script: string) {
        return await this.page.evaluate(script);
    }
} 