import { Page, expect } from '@playwright/test';

export class TestUtils {
    private page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    /**
     * Wait for network to be idle
     */
    async waitForNetworkIdle() {
        await this.page.waitForLoadState('networkidle');
    }

    /**
     * Wait for DOM to be ready
     */
    async waitForDOMReady() {
        await this.page.waitForLoadState('domcontentloaded');
    }

    /**
     * Wait for page to be fully loaded
     */
    async waitForPageLoad() {
        await this.page.waitForLoadState('load');
    }

    /**
     * Wait for element to be visible
     */
    async waitForElementVisible(selector: string, timeout: number = 10000) {
        await expect(this.page.locator(selector)).toBeVisible({ timeout });
    }

    /**
     * Wait for element to be hidden
     */
    async waitForElementHidden(selector: string, timeout: number = 10000) {
        await expect(this.page.locator(selector)).not.toBeVisible({ timeout });
    }

    /**
     * Wait for text to appear
     */
    async waitForText(text: string | RegExp, timeout: number = 10000) {
        await expect(this.page.getByText(text)).toBeVisible({ timeout });
    }

    /**
     * Wait for text to disappear
     */
    async waitForTextToDisappear(text: string | RegExp, timeout: number = 10000) {
        await expect(this.page.getByText(text)).not.toBeVisible({ timeout });
    }

    /**
     * Wait for URL to change
     */
    async waitForURLChange(expectedURL: string | RegExp, timeout: number = 10000) {
        await expect(this.page).toHaveURL(expectedURL, { timeout });
    }

    /**
     * Wait for page title to change
     */
    async waitForTitleChange(expectedTitle: string | RegExp, timeout: number = 10000) {
        await expect(this.page).toHaveTitle(expectedTitle, { timeout });
    }

    /**
     * Wait for function to return true
     */
    async waitForFunction(fn: () => boolean, timeout: number = 10000) {
        await this.page.waitForFunction(fn, { timeout });
    }

    /**
     * Wait for timeout
     */
    async wait(ms: number) {
        await this.page.waitForTimeout(ms);
    }

    /**
     * Take screenshot
     */
    async takeScreenshot(name: string) {
        await this.page.screenshot({ path: `test-results/${name}.png` });
    }

    /**
     * Get page title
     */
    async getPageTitle(): Promise<string> {
        return await this.page.title();
    }

    /**
     * Get current URL
     */
    async getCurrentURL(): Promise<string> {
        return this.page.url();
    }

    /**
     * Check if element exists
     */
    async elementExists(selector: string): Promise<boolean> {
        return await this.page.locator(selector).count() > 0;
    }

    /**
     * Check if element is visible
     */
    async elementIsVisible(selector: string): Promise<boolean> {
        return await this.page.locator(selector).isVisible();
    }

    /**
     * Get element text
     */
    async getElementText(selector: string): Promise<string> {
        return await this.page.locator(selector).textContent() || '';
    }

    /**
     * Get element attribute
     */
    async getElementAttribute(selector: string, attribute: string): Promise<string | null> {
        return await this.page.locator(selector).getAttribute(attribute);
    }

    /**
     * Click element if it exists
     */
    async clickIfExists(selector: string) {
        if (await this.elementExists(selector)) {
            await this.page.locator(selector).click();
        }
    }

    /**
     * Fill input if it exists
     */
    async fillIfExists(selector: string, value: string) {
        if (await this.elementExists(selector)) {
            await this.page.locator(selector).fill(value);
        }
    }

    /**
     * Clear input if it exists
     */
    async clearIfExists(selector: string) {
        if (await this.elementExists(selector)) {
            await this.page.locator(selector).clear();
        }
    }

    /**
     * Focus element if it exists
     */
    async focusIfExists(selector: string) {
        if (await this.elementExists(selector)) {
            await this.page.locator(selector).focus();
        }
    }

    /**
     * Check if element has class
     */
    async elementHasClass(selector: string, className: string): Promise<boolean> {
        const classAttribute = await this.getElementAttribute(selector, 'class');
        return classAttribute ? classAttribute.includes(className) : false;
    }

    /**
     * Check if element has attribute
     */
    async elementHasAttribute(selector: string, attribute: string, value: string): Promise<boolean> {
        const attributeValue = await this.getElementAttribute(selector, attribute);
        return attributeValue === value;
    }

    /**
     * Check if element has value
     */
    async elementHasValue(selector: string, expectedValue: string): Promise<boolean> {
        const value = await this.page.locator(selector).inputValue();
        return value === expectedValue;
    }

    /**
     * Check if element contains text
     */
    async elementContainsText(selector: string, expectedText: string): Promise<boolean> {
        const text = await this.getElementText(selector);
        return text.includes(expectedText);
    }

    /**
     * Reload page and wait for load
     */
    async reloadPage() {
        await this.page.reload();
        await this.waitForPageLoad();
    }

    /**
     * Navigate back and wait for load
     */
    async goBack() {
        await this.page.goBack();
        await this.waitForPageLoad();
    }

    /**
     * Navigate forward and wait for load
     */
    async goForward() {
        await this.page.goForward();
        await this.waitForPageLoad();
    }

    /**
     * Set viewport size
     */
    async setViewportSize(width: number, height: number) {
        await this.page.setViewportSize({ width, height });
    }

    /**
     * Press key
     */
    async pressKey(key: string) {
        await this.page.keyboard.press(key);
    }

    /**
     * Type text
     */
    async typeText(text: string) {
        await this.page.keyboard.type(text);
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
    async evaluateScript<T>(script: string): Promise<T> {
        return await this.page.evaluate(script);
    }

    /**
     * Check if page is accessible (basic checks)
     */
    async checkBasicAccessibility() {
        // Check for main heading
        await expect(this.page.locator('h1')).toBeVisible();

        // Check for main content area
        await expect(this.page.locator('main')).toBeVisible();

        // Check for proper language attribute
        await expect(this.page.locator('html')).toHaveAttribute('lang');
    }

    /**
     * Check if page has proper meta tags
     */
    async checkMetaTags() {
        // Check for viewport meta tag
        await expect(this.page.locator('meta[name="viewport"]')).toBeVisible();

        // Check for charset meta tag
        await expect(this.page.locator('meta[charset]')).toBeVisible();
    }

    /**
     * Check if page has proper title
     */
    async checkPageTitle() {
        const title = await this.getPageTitle();
        expect(title).toBeTruthy();
        expect(title.length).toBeGreaterThan(0);
    }

    /**
     * Check if page has proper URL
     */
    async checkPageURL() {
        const url = await this.getCurrentURL();
        expect(url).toBeTruthy();
        expect(url.length).toBeGreaterThan(0);
    }

    /**
     * Generate random string
     */
    generateRandomString(length: number = 10): string {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    /**
     * Generate random email
     */
    generateRandomEmail(): string {
        const randomString = this.generateRandomString(8);
        return `${randomString}@example.com`;
    }

    /**
     * Generate random URL
     */
    generateRandomURL(): string {
        const randomString = this.generateRandomString(8);
        return `https://${randomString}.example.com`;
    }

    /**
     * Wait for animation to complete
     */
    async waitForAnimation(selector: string, timeout: number = 5000) {
        await this.page.waitForFunction(
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return true;

                const style = window.getComputedStyle(element);
                const transition = style.transition;
                const animation = style.animation;

                return !transition || transition === 'none' || !animation || animation === 'none';
            },
            selector,
            { timeout }
        );
    }

    /**
     * Wait for element to stop moving
     */
    async waitForElementToStopMoving(selector: string, timeout: number = 5000) {
        await this.page.waitForFunction(
            (selector) => {
                const element = document.querySelector(selector);
                if (!element) return true;

                const rect = element.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            },
            selector,
            { timeout }
        );
    }
} 