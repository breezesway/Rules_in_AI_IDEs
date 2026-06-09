import { Page } from '@playwright/test';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';
import fetch from 'node-fetch';

export interface WaveResult {
  statistics: {
    pagetitle: string;
    pageurl: string;
    time: number;
    creditsremaining: number;
    allitemcount: number;
    totalelements: number;
    waveurl: string;
  };
  categories: {
    error: {
      description: string;
      count: number;
      items: WaveItem[];
    };
    contrast: {
      description: string;
      count: number;
      items: WaveItem[];
    };
    alert: {
      description: string;
      count: number;
      items: WaveItem[];
    };
    feature: {
      description: string;
      count: number;
      items: WaveItem[];
    };
    structure: {
      description: string;
      count: number;
      items: WaveItem[];
    };
    aria: {
      description: string;
      count: number;
      items: WaveItem[];
    };
  };
}

export interface WaveItem {
  id: string;
  description: string;
  count: number;
  selectors: string[];
  wcag: string[];
  position: {
    x: number;
    y: number;
  };
  page: number;
}

export interface WaveTestOptions {
  reporttype?: 1 | 2 | 3 | 4; // 1=errors, 2=errors+alerts, 3=errors+alerts+features, 4=all
  evaldelay?: number; // Delay in milliseconds before evaluation
  username?: string; // For authenticated pages
  password?: string; // For authenticated pages
}

export class WaveTestRunner {
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private apiKey: string;
  private baseUrl = 'https://wave.webaim.org/api/request';

  constructor(
    private page: Page,
    apiKey?: string
  ) {
    this.apiKey = apiKey || this.getWaveApiKey();
  }

  /**
   * Runs WAVE API analysis
   */
  async runAnalysis(options: WaveTestOptions = {}): Promise<ServiceResult<WaveResult>> {
    const config = this.config.getWaveConfiguration();
    const currentUrl = this.page.url();

    this.errorHandler.logInfo(`Running WAVE API analysis for: ${currentUrl}`);

    return this.errorHandler.withTimeout(
      this.performWaveAnalysis(currentUrl, options),
      config.timeout,
      'WAVE API analysis'
    );
  }

  /**
   * Runs WAVE analysis focusing on errors and critical issues
   */
  async runErrorAnalysis(): Promise<ServiceResult<WaveResult>> {
    return this.runAnalysis({
      reporttype: 1, // Errors only
      evaldelay: 1000,
    });
  }

  /**
   * Runs WAVE analysis focusing on contrast issues
   */
  async runContrastAnalysis(): Promise<ServiceResult<WaveResult>> {
    return this.runAnalysis({
      reporttype: 2, // Errors + alerts (includes contrast)
      evaldelay: 2000,
    });
  }

  /**
   * Runs comprehensive WAVE analysis
   */
  async runComprehensiveAnalysis(): Promise<ServiceResult<WaveResult>> {
    return this.runAnalysis({
      reporttype: 4, // All categories
      evaldelay: 3000,
    });
  }

  /**
   * Runs WAVE ARIA analysis
   */
  async runAriaAnalysis(): Promise<ServiceResult<WaveResult>> {
    const result = await this.runAnalysis({
      reporttype: 4,
      evaldelay: 2000,
    });

    if (result.success && result.data) {
      // Filter results to focus on ARIA-related items
      const ariaFilteredResult = {
        ...result.data,
        categories: {
          ...result.data.categories,
          error: {
            ...result.data.categories.error,
            items: result.data.categories.error.items.filter(
              item => item.id.includes('aria') || item.description.toLowerCase().includes('aria')
            ),
          },
          alert: {
            ...result.data.categories.alert,
            items: result.data.categories.alert.items.filter(
              item => item.id.includes('aria') || item.description.toLowerCase().includes('aria')
            ),
          },
          aria: result.data.categories.aria, // Keep all ARIA-specific items
        },
      };

      return { success: true, data: ariaFilteredResult };
    }

    return result;
  }

  /**
   * Runs WAVE structural analysis
   */
  async runStructuralAnalysis(): Promise<ServiceResult<WaveResult>> {
    const result = await this.runAnalysis({
      reporttype: 4,
      evaldelay: 2000,
    });

    if (result.success && result.data) {
      // Filter results to focus on structural items
      const structureFilteredResult = {
        ...result.data,
        categories: {
          ...result.data.categories,
          structure: result.data.categories.structure, // Keep all structural items
          feature: {
            ...result.data.categories.feature,
            items: result.data.categories.feature.items.filter(
              item =>
                item.id.includes('heading') ||
                item.id.includes('landmark') ||
                item.id.includes('list') ||
                item.description.toLowerCase().includes('structure')
            ),
          },
        },
      };

      return { success: true, data: structureFilteredResult };
    }

    return result;
  }

  /**
   * Performs the actual WAVE API analysis
   */
  private async performWaveAnalysis(url: string, options: WaveTestOptions): Promise<WaveResult> {
    if (!this.apiKey) {
      throw new Error(
        'WAVE API key is required. Set WAVE_API_KEY environment variable or provide it in configuration.'
      );
    }

    const requestUrl = new URL(this.baseUrl);
    requestUrl.searchParams.append('key', this.apiKey);
    requestUrl.searchParams.append('url', url);
    requestUrl.searchParams.append('format', 'json');

    // Add optional parameters
    if (options.reporttype) {
      requestUrl.searchParams.append('reporttype', options.reporttype.toString());
    }
    if (options.evaldelay) {
      requestUrl.searchParams.append('evaldelay', options.evaldelay.toString());
    }
    if (options.username) {
      requestUrl.searchParams.append('username', options.username);
    }
    if (options.password) {
      requestUrl.searchParams.append('password', options.password);
    }

    this.errorHandler.logInfo(
      `Making WAVE API request to: ${requestUrl.toString().replace(/key=[^&]*/, 'key=***')}`
    );

    const startTime = Date.now();
    const response = await fetch(requestUrl.toString());
    const duration = Date.now() - startTime;

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `WAVE API request failed: ${response.status} ${response.statusText} - ${errorText}`
      );
    }

    const result = (await response.json()) as WaveResult;

    if (!result || !result.statistics) {
      throw new Error('WAVE API returned invalid response format');
    }

    this.errorHandler.logSuccess(
      `WAVE API analysis completed in ${duration}ms: ${result.statistics.allitemcount} items found, ${result.statistics.creditsremaining} credits remaining`
    );

    return result;
  }

  /**
   * Gets WAVE API key from environment or configuration
   */
  private getWaveApiKey(): string {
    // Try environment variable first
    const envKey = process.env.WAVE_API_KEY;
    if (envKey) {
      return envKey;
    }

    // Try configuration service
    const config = this.config.getWaveConfiguration();
    if (config.apiKey) {
      return config.apiKey;
    }

    // Return empty string - will be handled by performWaveAnalysis
    return '';
  }

  /**
   * Runs WAVE analysis with retry logic
   */
  async runAnalysisWithRetry(
    options: WaveTestOptions = {},
    maxRetries: number = 3
  ): Promise<ServiceResult<WaveResult>> {
    return this.errorHandler.retryWithBackoff(
      () => this.performWaveAnalysis(this.page.url(), options),
      maxRetries,
      1000,
      'WAVE API analysis'
    );
  }

  /**
   * Converts WAVE results to standardized format for integration
   */
  convertToStandardFormat(waveResult: WaveResult): any[] {
    const standardViolations: any[] = [];

    // Process errors
    waveResult.categories.error.items.forEach(item => {
      standardViolations.push({
        id: item.id,
        impact: 'serious',
        description: item.description,
        help: item.description,
        helpUrl: `https://wave.webaim.org/help#${item.id}`,
        tags: ['wcag2a', 'wave'],
        nodes: item.selectors.map(selector => ({
          target: [selector],
          html: selector,
          impact: 'serious',
          any: [],
          all: [],
          none: [],
        })),
        wcag: item.wcag,
        tool: 'wave',
      });
    });

    // Process alerts
    waveResult.categories.alert.items.forEach(item => {
      standardViolations.push({
        id: item.id,
        impact: 'moderate',
        description: item.description,
        help: item.description,
        helpUrl: `https://wave.webaim.org/help#${item.id}`,
        tags: ['wcag2a', 'wave'],
        nodes: item.selectors.map(selector => ({
          target: [selector],
          html: selector,
          impact: 'moderate',
          any: [],
          all: [],
          none: [],
        })),
        wcag: item.wcag,
        tool: 'wave',
      });
    });

    // Process contrast issues
    waveResult.categories.contrast.items.forEach(item => {
      standardViolations.push({
        id: item.id,
        impact: 'serious',
        description: item.description,
        help: item.description,
        helpUrl: `https://wave.webaim.org/help#${item.id}`,
        tags: ['wcag2aa', 'color', 'wave'],
        nodes: item.selectors.map(selector => ({
          target: [selector],
          html: selector,
          impact: 'serious',
          any: [],
          all: [],
          none: [],
        })),
        wcag: item.wcag,
        tool: 'wave',
      });
    });

    return standardViolations;
  }
}
