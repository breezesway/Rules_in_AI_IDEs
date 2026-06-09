import { Page, test } from '@playwright/test';
import { ConfigurationService } from './services/configuration-service';
import { ErrorHandlerService } from './services/error-handler-service';
import { FileOperationsService } from './services/file-operations-service';

export interface TestSetupOptions {
    url?: string;
    skipInitialNavigation?: boolean;
    enableConsoleLogging?: boolean;
    timeout?: number;
    waitForNetworkIdle?: boolean;
}

export class TestSetupUtil {
    private static instance: TestSetupUtil;
    private config = ConfigurationService.getInstance();
    private errorHandler = ErrorHandlerService.getInstance();
    private fileOps = FileOperationsService.getInstance();

    private constructor() { }

    static getInstance(): TestSetupUtil {
        if (!TestSetupUtil.instance) {
            TestSetupUtil.instance = new TestSetupUtil();
        }
        return TestSetupUtil.instance;
    }

    /**
     * Common setup for all accessibility tests
     */
    async setupAccessibilityTest(
        page: Page,
        options: TestSetupOptions = {}
    ): Promise<void> {
        const {
            url = 'https://nimbleapproach.com/',
            skipInitialNavigation = false,
            enableConsoleLogging = true,
            timeout = 30000,
            waitForNetworkIdle = true,
        } = options;

        // Set test timeout
        test.setTimeout(timeout);

        // Setup console logging if enabled
        if (enableConsoleLogging) {
            this.setupConsoleLogging(page);
        }

        // Setup network request filtering
        this.setupNetworkFiltering(page);

        // Setup accessibility-specific page configuration
        await this.setupAccessibilityPageConfig(page);

        // Navigate to URL if not skipped
        if (!skipInitialNavigation && url) {
            await this.navigateToUrl(page, url, waitForNetworkIdle);
        }

        // Ensure reports directory exists
        this.ensureReportsDirectoryExists();
    }

    /**
     * Setup console logging with filtering
     */
    private setupConsoleLogging(page: Page): void {
        page.on('console', (msg) => {
            if (msg.type() === 'error') {
                const message = msg.text();

                // Filter out resource loading errors (404s for images, CSS, JS, etc.)
                const isResourceError = message.includes('Failed to load resource') ||
                    message.includes('404') ||
                    message.includes('net::ERR_ABORTED') ||
                    message.includes('net::ERR_FAILED');

                // Only log actual JavaScript errors that might affect accessibility
                if (!isResourceError) {
                    this.errorHandler.logWarning('Console error detected', { message });
                }
            }
        });

        // Log uncaught exceptions
        page.on('pageerror', (error) => {
            this.errorHandler.logWarning('Page error detected', {
                message: error.message,
                stack: error.stack,
            });
        });
    }

    /**
     * Setup network request filtering
     */
    private setupNetworkFiltering(page: Page): void {
        // Block unnecessary resources for faster testing
        page.route('**/*', (route) => {
            const request = route.request();
            const resourceType = request.resourceType();

            // Block analytics, ads, and other non-essential resources
            if (resourceType === 'image' && request.url().includes('analytics')) {
                route.abort();
            } else if (resourceType === 'script' && request.url().includes('ads')) {
                route.abort();
            } else {
                route.continue();
            }
        });
    }

    /**
     * Setup accessibility-specific page configuration
     */
    private async setupAccessibilityPageConfig(page: Page): Promise<void> {
        // Set extra HTTP headers for accessibility testing
        await page.setExtraHTTPHeaders({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 AccessibilityTester/1.0',
        });

        // Configure viewport for consistent testing
        await page.setViewportSize({ width: 1920, height: 1080 });

        // Disable animations for more consistent testing
        await page.addInitScript(() => {
            // Disable CSS animations and transitions
            const style = document.createElement('style');
            style.textContent = `
        *,
        *::before,
        *::after {
          animation-duration: 0s !important;
          animation-delay: 0s !important;
          transition-duration: 0s !important;
          transition-delay: 0s !important;
        }
      `;
            document.head.appendChild(style);
        });
    }

    /**
     * Navigate to URL with proper error handling
     */
    private async navigateToUrl(
        page: Page,
        url: string,
        waitForNetworkIdle: boolean = true
    ): Promise<void> {
        try {
            this.errorHandler.logInfo(`Navigating to: ${url}`);

            const options: any = {
                timeout: this.config.getReportingConfiguration().screenshotTimeout,
                waitUntil: waitForNetworkIdle ? 'networkidle' : 'domcontentloaded',
            };

            await page.goto(url, options);

            // Wait for page to be fully loaded
            await page.waitForLoadState('networkidle', { timeout: 10000 });

            this.errorHandler.logSuccess(`Successfully navigated to: ${url}`);
        } catch (error) {
            this.errorHandler.handleError(error, `Navigation to ${url}`);
            throw error;
        }
    }

    /**
     * Ensure reports directory exists
     */
    private ensureReportsDirectoryExists(): void {
        const result = this.fileOps.ensureDirectoryExists(
            this.config.getReportingConfiguration().reportsDirectory
        );

        if (!result.success) {
            this.errorHandler.logWarning('Failed to create reports directory', {
                error: result.message,
            });
        }
    }

    /**
     * Common teardown for tests
     */
    async teardownAccessibilityTest(page: Page): Promise<void> {
        try {
            // Remove any event listeners
            page.removeAllListeners();

            // Clear any storage
            await page.evaluate(() => {
                localStorage.clear();
                sessionStorage.clear();
            });

            this.errorHandler.logInfo('Test teardown completed');
        } catch (error) {
            this.errorHandler.handleError(error, 'Test teardown');
        }
    }

    /**
     * Wait for page to be ready for testing
     */
    async waitForPageReady(page: Page, timeout: number = 30000): Promise<void> {
        try {
            // Wait for the page to be loaded
            await page.waitForLoadState('networkidle', { timeout });

            // Wait for any dynamic content to load
            await page.waitForFunction(() => {
                return document.readyState === 'complete';
            }, { timeout });

            // Small additional wait for any final rendering
            await page.waitForTimeout(1000);

            this.errorHandler.logSuccess('Page ready for testing');
        } catch (error) {
            this.errorHandler.handleError(error, 'Waiting for page ready');
            throw error;
        }
    }

    /**
     * Setup common beforeEach for accessibility tests
     */
    setupCommonBeforeEach(testName: string, options: TestSetupOptions = {}) {
        return async ({ page }: { page: Page }) => {
            this.errorHandler.logInfo(`Setting up test: ${testName}`);
            await this.setupAccessibilityTest(page, options);
        };
    }

    /**
     * Setup common afterEach for accessibility tests
     */
    setupCommonAfterEach(testName: string) {
        return async ({ page }: { page: Page }) => {
            this.errorHandler.logInfo(`Tearing down test: ${testName}`);
            await this.teardownAccessibilityTest(page);
        };
    }
} 