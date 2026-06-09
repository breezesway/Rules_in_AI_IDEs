import {
  Browser,
  BrowserContext,
  chromium,
  Page,
  BrowserContextOptions as PlaywrightBrowserContextOptions,
} from 'playwright';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { ConfigurationService } from '../../../playwright/tests/utils/services/configuration-service';

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

  private constructor() {}

  static getInstance(): BrowserManager {
    if (!BrowserManager.instance) {
      BrowserManager.instance = new BrowserManager();
    }
    return BrowserManager.instance;
  }

  async initialize(): Promise<void> {
    if (this.isInitialized) {
      return;
    }

    try {
      this.errorHandler.logInfo('Initializing browser manager');

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

  async getContext(
    sessionId: string,
    options: CustomBrowserContextOptions = {}
  ): Promise<BrowserContext> {
    if (!this.browser) {
      throw new Error('Browser not initialized. Call initialize() first.');
    }

    if (this.contexts.has(sessionId)) {
      return this.contexts.get(sessionId)!;
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

      const context = await this.browser.newContext(contextOptions);
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

    return this.pages.get(pageKey)!;
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
      for (const [pageKey, page] of this.pages) {
        await page.close();
      }
      this.pages.clear();

      // Close all contexts
      for (const [sessionId, context] of this.contexts) {
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
