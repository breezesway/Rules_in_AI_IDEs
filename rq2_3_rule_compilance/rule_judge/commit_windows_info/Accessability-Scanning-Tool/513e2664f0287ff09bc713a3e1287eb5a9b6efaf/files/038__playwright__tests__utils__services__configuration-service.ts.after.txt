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
  /** Configuration for Lighthouse accessibility testing */
  lighthouse: {
    /** Timeout for Lighthouse analysis in milliseconds */
    timeout: number;
    /** Port number for Lighthouse debugging */
    port: number;
    /** Chrome launch configuration for Lighthouse */
    chromeLaunchConfig: {
      /** Command line arguments for Chrome */
      args: string[];
    };
  };
  /** Configuration for WAVE API accessibility testing */
  wave: {
    /** Timeout for WAVE API analysis in milliseconds */
    timeout: number;
    /** WAVE API key for authentication */
    apiKey: string;
    /** Report type for WAVE analysis (1-4) */
    reportType: 1 | 2 | 3 | 4;
    /** Evaluation delay in milliseconds */
    evalDelay: number;
    /** Base URL for WAVE API */
    baseUrl: string;
  };
  /** Configuration for Tenon.io accessibility testing */
  tenon: {
    /** Timeout for Tenon API analysis in milliseconds */
    timeout: number;
    /** Tenon API key for authentication */
    apiKey: string;
    /** WCAG level for Tenon analysis */
    level: 'A' | 'AA' | 'AAA';
    /** Certainty threshold (0-100) */
    certainty: number;
    /** Priority threshold (0-100) */
    priority: number;
    /** Store results in Tenon project */
    store: boolean;
    /** Base URL for Tenon API */
    baseUrl: string;
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
  getAxeConfiguration() {
    return this.config.axe;
  }

  /**
   * Gets the Pa11y specific configuration
   * @returns The Pa11y configuration object
   */
  getPa11yConfiguration() {
    return this.config.pa11y;
  }

  /**
   * Gets the Lighthouse specific configuration
   * @returns The Lighthouse configuration object
   */
  getLighthouseConfiguration() {
    return this.config.lighthouse;
  }

  /**
   * Gets the WAVE API specific configuration
   * @returns The WAVE configuration object
   */
  getWaveConfiguration() {
    return this.config.wave;
  }

  /**
   * Gets the Tenon.io specific configuration
   * @returns The Tenon configuration object
   */
  getTenonConfiguration() {
    return this.config.tenon;
  }

  /**
   * Gets the reporting specific configuration
   * @returns The reporting configuration object
   */
  getReportingConfiguration() {
    return this.config.reporting;
  }

  /**
   * Gets the crawling configuration for website discovery and page exclusion
   * @returns The crawling configuration object
   */
  getCrawlingConfiguration() {
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
        timeout: 30000,
        wait: 2000,
        standard: 'WCAG2AA',
        includeNotices: true,
        includeWarnings: true,
        chromeLaunchConfig: {
          args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-default-apps',
            '--disable-sync',
            '--memory-pressure-off',
            '--max_old_space_size=2048',
            '--single-process',
          ],
        },
      },
      lighthouse: {
        timeout: 60000,
        port: 9222,
        chromeLaunchConfig: {
          args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-default-apps',
            '--disable-sync',
            '--memory-pressure-off',
            '--max_old_space_size=2048',
          ],
        },
      },
      wave: {
        timeout: 45000,
        apiKey: process.env.WAVE_API_KEY || '',
        reportType: 4, // All categories
        evalDelay: 2000,
        baseUrl: 'https://wave.webaim.org/api/request',
      },
      tenon: {
        timeout: 45000,
        apiKey: process.env.TENON_API_KEY || '',
        level: 'AA',
        certainty: 80,
        priority: 60,
        store: true,
        baseUrl: 'https://tenon.io/api/',
      },
      reporting: {
        maxConcurrency: 5,
        delayBetweenPages: 1000,
        screenshotTimeout: 5000,
        reportsDirectory: 'playwright/accessibility-reports',
      },
      crawling: {
        excludePatterns: [
          // File extensions - These are not HTML pages and cannot be tested for accessibility
          /\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z)$/i, // Documents
          /\.(jpg|jpeg|png|gif|svg|webp|ico|bmp|tiff)$/i, // Images
          /\.(mp4|avi|mov|wmv|flv|webm|mkv|mp3|wav|ogg)$/i, // Media files
          /\.(css|js|json|xml|txt|csv)$/i, // Static resources

          // Admin areas - Backend admin interfaces (not customer-facing)
          /\/wp-admin\//i, // WordPress admin
          /\/wp-login\.php/i, // WordPress login
          /\/administrator\//i, // Joomla admin
          /\/admin\.php/i, // Generic admin files
          /\/phpmyadmin\//i, // Database admin
          /\/admin\//i, // Generic admin directories
          /\/login\//i, // Login pages
          /\/logout\//i, // Logout pages
          /\/signin\//i, // Sign in pages
          /\/signup\//i, // Sign up pages
          /\/register\//i, // Registration pages

          // Non-HTML resources and technical endpoints
          /\/api\//i, // API endpoints
          /\/feed\//i, // RSS/Atom feeds
          /\/feeds\//i, // RSS/Atom feeds
          /\/rss\//i, // RSS feeds
          /\/sitemap/i, // Sitemap files
          /\/robots\.txt$/i, // Robots.txt
          /\/\.well-known\//i, // Well-known URIs

          // Tracking and analytics - Duplicate content with tracking parameters
          /\?.*utm_/i, // UTM tracking parameters
          /\?.*fbclid/i, // Facebook tracking
          /\?.*gclid/i, // Google tracking
          /\?.*msclkid/i, // Microsoft tracking
          /\?.*ref=/i, // Referrer tracking

          // Non-HTTP protocols - Cannot be tested with browser automation
          /mailto:/i, // Email links
          /tel:/i, // Phone links
          /ftp:/i, // FTP links
          /javascript:/i, // JavaScript links
          /data:/i, // Data URIs

          // Excessive pagination to prevent infinite crawling (keep reasonable pagination)
          /\/page\/(?:[5-9]\d|\d{3,})/i, // Pages 50+ to prevent excessive crawling
          /\/p\/(?:[5-9]\d|\d{3,})/i, // Alternative pagination 50+
          /\?page=(?:[5-9]\d|\d{3,})/i, // Query-based pagination 50+
          /\?p=(?:[5-9]\d|\d{3,})/i, // Alternative query pagination 50+

          // Fragments that are not meaningful for accessibility testing
          /^[^#]*#(?:top|bottom|header|footer|nav|menu)$/i, // Common anchor links without unique content
          /#/i, // Fragment identifiers (simplified version)

          // Development and testing artifacts
          /\/test\//i, // Test directories
          /\/staging\//i, // Staging areas
          /\/dev\//i, // Development areas
          /\/demo\//i, // Demo areas (unless specifically testing demos)
        ],
        customExcludePatterns: [
          // Site-specific patterns can be added here
        ],
      },
    };
  }
}
