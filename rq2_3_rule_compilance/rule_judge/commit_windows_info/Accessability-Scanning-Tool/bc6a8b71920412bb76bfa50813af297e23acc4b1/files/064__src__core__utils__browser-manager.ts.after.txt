import {
  Browser,
  BrowserContext,
  chromium,
  Page,
  BrowserContextOptions as PlaywrightBrowserContextOptions,
} from 'playwright';
import { ErrorHandlerService } from '../../utils/services/error-handler-service';
import { ConfigurationService } from '../../utils/services/configuration-service';

export interface CustomBrowserContextOptions {
  viewport?: { width: number; height: number };
  userAgent?: string;
  locale?: string;
  timezone?: string;
  permissions?: string[];
  extraHTTPHeaders?: Record<string, string>;
}

export class BrowserManager {
  private static instance: BrowserManager;
  private browser: Browser | null = null;
  private contexts: Map<string, BrowserContext> = new Map();
  private pages: Map<string, Page> = new Map();
  private errorHandler = ErrorHandlerService.getInstance();
  private config = ConfigurationService.getInstance();
  private isInitialized = false;

  private constructor() { }

  static getInstance(): BrowserManager {
    if (!BrowserManager.instance) {
      BrowserManager.instance = new BrowserManager();
    }
    return BrowserManager.instance;
  }

  async initialize(): Promise<void> {
    if (this.isInitialized && this.browser) {
      // Check if the existing browser is still healthy
      try {
        const isHealthy = await this.isBrowserHealthy();
        if (isHealthy) {
          return; // Browser is already initialized and healthy
        }
      } catch (error) {
        this.errorHandler.logWarning('Existing browser health check failed, reinitializing...');
      }
    }

    try {
      this.errorHandler.logInfo('Initializing browser manager');

      // Clean up any existing browser instance
      if (this.browser) {
        try {
          await this.cleanupAll();
        } catch (error) {
          this.errorHandler.logWarning('Error during cleanup of existing browser: ' + (error instanceof Error ? error.message : 'Unknown error'));
        }
      }

      // Launch browser with optimized settings
      this.browser = await chromium.launch({
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-extensions',
          '--disable-default-apps',
          '--disable-sync',
          '--disable-background-timer-throttling',
          '--disable-backgrounding-occluded-windows',
          '--disable-renderer-backgrounding',
          '--disable-ipc-flooding-protection',
          '--memory-pressure-off',
          '--max_old_space_size=4096',
          '--enable-automation',
          '--disable-blink-features=AutomationControlled',
          '--disable-background-networking',
          '--disable-component-update',
          '--disable-domain-reliability',
          '--disable-hang-monitor',
          '--disable-prompt-on-repost',
          '--metrics-recording-only',
          '--no-first-run',
          '--safebrowsing-disable-auto-update',
          '--use-mock-keychain',
        ],
      });

      this.isInitialized = true;
      this.errorHandler.logSuccess('Browser manager initialized successfully');
    } catch (error) {
      this.errorHandler.handleError(error, 'Browser manager initialization');
      throw error;
    }
  }

  async forceReinitialize(): Promise<void> {
    this.errorHandler.logInfo('Force reinitializing browser manager');
    this.isInitialized = false;
    this.browser = null;
    this.contexts.clear();
    this.pages.clear();
    await this.initialize();
  }

  async getContext(
    sessionId: string,
    options: CustomBrowserContextOptions = {}
  ): Promise<BrowserContext> {
    // Check if browser is still valid, reinitialize if needed
    if (!this.browser || !this.isInitialized) {
      this.errorHandler.logInfo('Browser not initialized or closed, reinitializing...');
      await this.initialize();
    }

    if (this.contexts.has(sessionId)) {
      const context = this.contexts.get(sessionId)!;
      // Check if context is still valid
      try {
        // Check if context is still connected to the browser
        if (context.pages().length === 0) {
          // Context exists but has no pages, which is fine
          return context;
        }

        // Try to create a new page to test if context is still working
        const testPage = await context.newPage();
        await testPage.close();
        return context;
      } catch (error) {
        this.errorHandler.logWarning(`Context ${sessionId} is no longer valid, creating new one: ${error instanceof Error ? error.message : 'Unknown error'}`);
        this.contexts.delete(sessionId);
      }
    }

    this.errorHandler.logInfo(`Creating new browser context for session: ${sessionId}`);

    try {
      const contextOptions: PlaywrightBrowserContextOptions = {
        viewport: options.viewport || { width: 1920, height: 1080 },
        userAgent:
          options.userAgent ||
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        locale: options.locale || 'en-US',
        timezoneId: options.timezone || 'America/New_York',
        permissions: options.permissions || [],
        extraHTTPHeaders: options.extraHTTPHeaders || {},
      };

      const context = await this.browser!.newContext(contextOptions);
      this.contexts.set(sessionId, context);

      this.errorHandler.logSuccess(`Browser context created for session: ${sessionId}`);
      return context;
    } catch (error) {
      this.errorHandler.handleError(
        error,
        `Failed to create browser context for session: ${sessionId}`
      );
      throw error;
    }
  }

  async getPage(sessionId: string, pageId: string = 'default'): Promise<Page> {
    const pageKey = `${sessionId}:${pageId}`;

    if (!this.pages.has(pageKey)) {
      const context = await this.getContext(sessionId);
      const page = await context.newPage();

      // Set up page-specific configurations
      await page.setDefaultNavigationTimeout(45000);
      await page.setDefaultTimeout(30000);

      this.pages.set(pageKey, page);
      this.errorHandler.logInfo(`Created new page for session: ${sessionId}, page: ${pageId}`);
    }

    const page = this.pages.get(pageKey)!;

    // Check if page is still valid - use a more robust check
    try {
      // Check if the page is still connected to the browser
      if (page.isClosed()) {
        this.errorHandler.logWarning(`Page ${pageKey} is closed, creating new one`);
        this.pages.delete(pageKey);
        return this.getPage(sessionId, pageId);
      }

      // Try a simple operation to verify the page is working
      await page.evaluate(() => true);
      return page;
    } catch (error) {
      this.errorHandler.logWarning(`Page ${pageKey} is no longer valid, creating new one: ${error instanceof Error ? error.message : 'Unknown error'}`);
      this.pages.delete(pageKey);
      return this.getPage(sessionId, pageId);
    }
  }

  async isBrowserHealthy(): Promise<boolean> {
    if (!this.browser || !this.isInitialized) {
      return false;
    }

    try {
      // Try to create a test context to verify browser is working
      const testContext = await this.browser.newContext();
      const testPage = await testContext.newPage();
      await testPage.close();
      await testContext.close();
      return true;
    } catch (error) {
      this.errorHandler.logWarning('Browser health check failed, browser needs reinitialization');
      return false;
    }
  }

  async closePage(sessionId: string, pageId: string = 'default'): Promise<void> {
    const pageKey = `${sessionId}:${pageId}`;
    const page = this.pages.get(pageKey);

    if (page) {
      await page.close();
      this.pages.delete(pageKey);
      this.errorHandler.logInfo(`Closed page for session: ${sessionId}, page: ${pageId}`);
    }
  }

  async cleanup(sessionId: string): Promise<void> {
    try {
      this.errorHandler.logInfo(`Cleaning up browser resources for session: ${sessionId}`);

      // Close all pages for this session
      const pagesToClose = Array.from(this.pages.keys()).filter(key => key.startsWith(sessionId));
      for (const pageKey of pagesToClose) {
        const page = this.pages.get(pageKey);
        if (page) {
          await page.close();
          this.pages.delete(pageKey);
        }
      }

      // Close context
      const context = this.contexts.get(sessionId);
      if (context) {
        await context.close();
        this.contexts.delete(sessionId);
      }

      this.errorHandler.logSuccess(`Cleaned up resources for session: ${sessionId}`);
    } catch (error) {
      this.errorHandler.handleError(error, `Cleanup session: ${sessionId}`);
    }
  }

  async cleanupAll(): Promise<void> {
    try {
      this.errorHandler.logInfo('Cleaning up all browser resources');

      // Close all pages
      for (const [_pageKey, page] of this.pages) {
        await page.close();
      }
      this.pages.clear();

      // Close all contexts
      for (const [_sessionId, context] of this.contexts) {
        await context.close();
      }
      this.contexts.clear();

      // Close browser
      if (this.browser) {
        await this.browser.close();
        this.browser = null;
      }

      this.isInitialized = false;
      this.errorHandler.logSuccess('All browser resources cleaned up');
    } catch (error) {
      this.errorHandler.handleError(error, 'Cleanup all browser resources');
    }
  }

  getResourceUsage(): {
    contexts: number;
    pages: number;
    isInitialized: boolean;
  } {
    return {
      contexts: this.contexts.size,
      pages: this.pages.size,
      isInitialized: this.isInitialized,
    };
  }

  async navigateToUrl(
    sessionId: string,
    url: string,
    options: {
      waitUntil?: 'load' | 'domcontentloaded' | 'networkidle';
      timeout?: number;
      pageId?: string;
    } = {}
  ): Promise<Page> {
    const { waitUntil = 'domcontentloaded', timeout = 30000, pageId = 'default' } = options;

    const page = await this.getPage(sessionId, pageId);

    await page.goto(url, {
      waitUntil,
      timeout,
    });

    // Wait for page to stabilize
    await page.waitForTimeout(1000);

    return page;
  }
}
