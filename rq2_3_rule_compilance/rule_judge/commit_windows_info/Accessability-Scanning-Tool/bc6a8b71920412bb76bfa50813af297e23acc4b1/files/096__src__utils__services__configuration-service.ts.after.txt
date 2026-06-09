/**
 * Configuration interface for all accessibility testing tools and settings
 */
export interface TestConfiguration {
  /** Configuration for axe-core accessibility testing */
  axe: {
    /** Timeout for axe-core analysis in milliseconds */
    timeout: number;
    /** WCAG tags to include in axe-core analysis */
    tags: string[];
    /** Custom rules configuration for axe-core */
    rules: Record<string, { enabled: boolean }>;
  };
  /** Configuration for Pa11y accessibility testing */
  pa11y: {
    /** Timeout for Pa11y analysis in milliseconds */
    timeout: number;
    /** Wait time before starting Pa11y analysis in milliseconds */
    wait: number;
    /** WCAG standard to use for Pa11y testing */
    standard: string;
    /** Whether to include notices in Pa11y results */
    includeNotices: boolean;
    /** Whether to include warnings in Pa11y results */
    includeWarnings: boolean;
    /** Chrome launch configuration for Pa11y */
    chromeLaunchConfig: {
      /** Command line arguments for Chrome */
      args: string[];
    };
  };
  /** Configuration for report generation and file operations */
  reporting: {
    /** Maximum number of concurrent operations */
    maxConcurrency: number;
    /** Delay between page processing in milliseconds */
    delayBetweenPages: number;
    /** Timeout for screenshot capture in milliseconds */
    screenshotTimeout: number;
    /** Directory path for accessibility reports */
    reportsDirectory: string;
  };
  /** Configuration for website crawling and page discovery */
  crawling: {
    /** Patterns to exclude from crawling and accessibility testing */
    excludePatterns: RegExp[];
    /** Custom site-specific patterns to exclude */
    customExcludePatterns: RegExp[];
  };
}

/**
 * Singleton service for managing accessibility testing configuration
 * Provides centralized configuration management for all testing tools
 */
export class ConfigurationService {
  private static instance: ConfigurationService;
  private config: TestConfiguration;

  private constructor() {
    this.config = this.getDefaultConfiguration();
  }

  /**
   * Gets the singleton instance of ConfigurationService
   * @returns The singleton ConfigurationService instance
   */
  static getInstance(): ConfigurationService {
    if (!ConfigurationService.instance) {
      ConfigurationService.instance = new ConfigurationService();
    }
    return ConfigurationService.instance;
  }

  /**
   * Gets the complete configuration object
   * @returns The complete TestConfiguration object
   */
  getConfiguration(): TestConfiguration {
    return this.config;
  }

  /**
   * Gets the axe-core specific configuration
   * @returns The axe-core configuration object
   */
  public getAxeConfiguration(): any {
    return this.config.axe;
  }

  /**
   * Gets the Pa11y specific configuration
   * @returns The Pa11y configuration object
   */
  public getPa11yConfiguration(): any {
    return this.config.pa11y;
  }

  /**
   * Gets the reporting specific configuration
   * @returns The reporting configuration object
   */
  public getReportingConfiguration(): any {
    return this.config.reporting;
  }

  /**
   * Gets the crawling configuration for website discovery and page exclusion
   * @returns The crawling configuration object
   */
  public getCrawlingConfiguration(): any {
    return this.config.crawling;
  }

  /**
   * Updates the configuration with new values
   * @param updates Partial configuration updates to apply
   */
  updateConfiguration(updates: Partial<TestConfiguration>): void {
    this.config = { ...this.config, ...updates };
  }

  /**
   * Creates and returns the default configuration for all accessibility testing tools
   * @returns The default TestConfiguration object with optimized settings
   */
  private getDefaultConfiguration(): TestConfiguration {
    return {
      axe: {
        timeout: 30000,
        tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'],
        rules: {
          'color-contrast': { enabled: true },
          keyboard: { enabled: true },
          'focus-order-semantics': { enabled: true },
        },
      },
      pa11y: {
        timeout: 60000,
        wait: 1000,
        standard: 'WCAG2AA',
        includeNotices: false,
        includeWarnings: true,
        chromeLaunchConfig: {
          args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
        },
      },
      reporting: {
        maxConcurrency: 5,
        delayBetweenPages: 500,
        screenshotTimeout: 5000,
        reportsDirectory: 'accessibility-reports',
      },
      crawling: {
        excludePatterns: [
          /login/,
          /register/,
          /cart/,
          /checkout/,
          /account/,
          /logout/,
          /wp-admin/,
          /admin/,
          /.\.pdf$/,
          /.\.jpg$/,
          /.\.png$/,
        ],
        customExcludePatterns: [],
      },
    };
  }
}
