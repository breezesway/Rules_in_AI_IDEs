import { Page } from '@playwright/test';
import { AxeResults, RunOptions } from 'axe-core';
import AxeBuilder from '@axe-core/playwright';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ServiceResult } from '@/core/types/common';

export interface AxeTestOptions {
  include?: string[];
  exclude?: string[];
  tags?: string[];
  rules?: Record<string, { enabled: boolean }>;
  devtools?: boolean;
  shadow?: boolean;
  iframes?: boolean;
  reporter?: 'v1' | 'v2' | 'raw' | 'no-passes';
  allowedOrigins?: string[];
}

export class AxeTestRunner {
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();

  constructor(private page: Page) { }

  /**
   * Injects axe-core into the page
   */
  async injectAxe(): Promise<ServiceResult<void>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      await this.page.addScriptTag({
        url: 'https://unpkg.com/axe-core@4.8.2/axe.min.js',
      });
    }, 'injectAxe');
  }

  /**
   * Runs axe-core analysis
   */
  async runAnalysis(options: AxeTestOptions = {}): Promise<ServiceResult<AxeResults>> {
    const config = this.config.getAxeConfiguration();
    const timeout = config?.timeout || 30000; // Default 30 seconds if config is null

    return this.errorHandler.withTimeout(
      this.performAxeAnalysis(options),
      timeout,
      'axe-core analysis'
    );
  }

  /**
   * Runs specific axe-core rules for color contrast
   */
  async runColorContrastAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.color'],
      rules: {
        'color-contrast': { enabled: true },
        'color-contrast-enhanced': { enabled: true },
      },
    });
  }

  /**
   * Runs keyboard accessibility analysis
   */
  async runKeyboardAccessibilityAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.keyboard'],
      rules: {
        'focus-order-semantics': { enabled: true },
        'focusable-content': { enabled: true },
        tabindex: { enabled: true },
      },
    });
  }

  /**
   * Runs ARIA implementation analysis
   */
  async runAriaAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.aria'],
      rules: {
        'aria-valid-attr': { enabled: true },
        'aria-valid-attr-value': { enabled: true },
        'aria-required-attr': { enabled: true },
      },
    });
  }

  /**
   * Runs form accessibility analysis
   */
  async runFormAccessibilityAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.forms'],
      rules: {
        label: { enabled: true },
        'label-title-only': { enabled: true },
        'form-field-multiple-labels': { enabled: true },
      },
    });
  }

  /**
   * Runs image accessibility analysis
   */
  async runImageAccessibilityAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.text-alternatives'],
      rules: {
        'image-alt': { enabled: true },
        'image-redundant-alt': { enabled: true },
        'input-image-alt': { enabled: true },
      },
    });
  }

  /**
   * Runs landmarks and headings analysis
   */
  async runLandmarksAndHeadingsAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      tags: ['cat.structure'],
      rules: {
        'landmark-one-main': { enabled: true },
        'landmark-no-duplicate-banner': { enabled: true },
        'landmark-no-duplicate-contentinfo': { enabled: true },
        'heading-order': { enabled: true },
        'page-has-heading-one': { enabled: true },
      },
    });
  }

  /**
   * Runs DevTools-enhanced comprehensive analysis
   */
  async runDevToolsAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      shadow: true,
      iframes: true,
      reporter: 'v2',
      tags: ['wcag2a', 'wcag2aa', 'wcag21aa'],
      rules: {
        'color-contrast': { enabled: true },
        'color-contrast-enhanced': { enabled: true },
        'focus-order-semantics': { enabled: true },
        'landmark-contentinfo-is-top-level': { enabled: true },
        'landmark-main-is-top-level': { enabled: true },
        'landmark-no-duplicate-banner': { enabled: true },
        'landmark-no-duplicate-contentinfo': { enabled: true },
        'landmark-no-duplicate-main': { enabled: true },
        'landmark-one-main': { enabled: true },
        'aria-allowed-attr': { enabled: true },
        'aria-command-name': { enabled: true },
        'aria-hidden-body': { enabled: true },
        'aria-hidden-focus': { enabled: true },
        'aria-input-field-name': { enabled: true },
        'aria-meter-name': { enabled: true },
        'aria-progressbar-name': { enabled: true },
        'aria-required-attr': { enabled: true },
        'aria-required-children': { enabled: true },
        'aria-required-parent': { enabled: true },
        'aria-roles': { enabled: true },
        'aria-toggle-field-name': { enabled: true },
        'aria-tooltip-name': { enabled: true },
        'aria-valid-attr': { enabled: true },
        'aria-valid-attr-value': { enabled: true },
      },
    });
  }

  /**
   * Runs shadow DOM analysis with DevTools
   */
  async runShadowDOMAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      shadow: true,
      reporter: 'v2' as const,
      tags: ['wcag2a', 'wcag2aa'],
    });
  }

  /**
   * Runs iframe analysis with DevTools
   */
  async runIframeAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      iframes: true,
      reporter: 'v2' as const,
      tags: ['wcag2a', 'wcag2aa'],
      allowedOrigins: ['*'], // Allow all origins for comprehensive iframe testing
    });
  }

  /**
   * Runs experimental rules analysis
   */
  async runExperimentalAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      shadow: true,
      iframes: true,
      reporter: 'v2' as const,
      tags: ['experimental'],
      rules: {
        'autocomplete-valid': { enabled: true },
        'avoid-inline-spacing': { enabled: true },
        'css-orientation-lock': { enabled: true },
        'focus-order-semantics': { enabled: true },
        'hidden-content': { enabled: true },
        'label-content-name-mismatch': { enabled: true },
        'landmark-banner-is-top-level': { enabled: true },
        'landmark-contentinfo-is-top-level': { enabled: true },
        'landmark-main-is-top-level': { enabled: true },
        'landmark-no-duplicate-banner': { enabled: true },
        'landmark-no-duplicate-contentinfo': { enabled: true },
        'landmark-no-duplicate-main': { enabled: true },
        'landmark-unique': { enabled: true },
        'no-autoplay-audio': { enabled: true },
        'p-as-heading': { enabled: true },
        'page-has-heading-one': { enabled: true },
        'presentation-role-conflict': { enabled: true },
        region: { enabled: true },
        'scope-attr-valid': { enabled: true },
        'svg-img-alt': { enabled: true },
        'target-size': { enabled: true },
      },
    });
  }

  /**
   * Runs comprehensive DevTools analysis with all capabilities
   */
  async runComprehensiveDevToolsAnalysis(): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      shadow: true,
      iframes: true,
      reporter: 'v2',
      tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag21aaa', 'best-practice', 'experimental'],
      allowedOrigins: ['*'],
    });
  }

  /**
   * Runs DevTools analysis with custom configuration
   */
  async runCustomDevToolsAnalysis(
    customConfig: Partial<AxeTestOptions>
  ): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis(customConfig);
  }

  private async performAxeAnalysis(options: AxeTestOptions): Promise<AxeResults> {
    const config = this.config.getAxeConfiguration();

    try {
      this.errorHandler.logInfo('Starting axe-core analysis with options', { options });

      const axeBuilder = new AxeBuilder({ page: this.page });

      if (options.include) {
        axeBuilder.include(options.include);
      }

      if (options.exclude) {
        axeBuilder.exclude(options.exclude);
      }

      if (options.tags) {
        axeBuilder.withTags(options.tags);
      }

      if (options.rules) {
        axeBuilder.withRules(Object.keys(options.rules));
        for (const [ruleId, ruleConfig] of Object.entries(options.rules)) {
          if (ruleConfig.enabled === false) {
            axeBuilder.disableRules([ruleId]);
          }
        }
      }

      // Check for devtools-specific features if enabled in config
      if (config?.devtools) {
        if (options.shadow) {
          // axeBuilder.withShadowDom();
        }

        if (options.iframes) {
          // axeBuilder.withFrames();
        }
      }

      const results = await axeBuilder.analyze();

      this.errorHandler.logSuccess('Axe-core analysis completed', {
        violations: results.violations.length,
        passes: results.passes.length,
      });

      return results;
    } catch (error) {
      this.errorHandler.handleError(error, 'Axe-core analysis failed');
      throw error;
    }
  }

  public async runAxeAnalysis(options?: AxeTestOptions): Promise<AxeResults> {
    const analysisOptions = options || {};
    const result = await this.runAnalysis(analysisOptions);
    if (result.success && result.data) {
      return result.data;
    } else {
      throw (result as any).error;
    }
  }

  /**
   * Main run method called by the ParallelAnalyzer
   * Returns data in the format expected by the orchestrator
   */
  public async run(): Promise<{ status: string; data?: any; error?: string }> {
    try {
      this.errorHandler.logInfo('Starting axe-core analysis');

      // Use basic analysis instead of DevTools to avoid potential issues
      const results = await this.runAnalysis({
        tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag21aaa'],
        rules: {
          'color-contrast': { enabled: true },
          'html-has-lang': { enabled: true },
          'label': { enabled: true },
          'landmark-one-main': { enabled: true },
          'page-has-heading-one': { enabled: true },
          'region': { enabled: true },
        },
      });

      if (results.success && results.data) {
        this.errorHandler.logSuccess('Axe-core analysis completed successfully', {
          violations: results.data.violations?.length || 0,
          passes: results.data.passes?.length || 0,
        });

        return {
          status: 'success',
          data: {
            tool: 'axe-core',
            violations: results.data.violations || [],
            passes: results.data.passes || [],
            timestamp: new Date().toISOString(),
          },
        };
      } else {
        const errorMessage = 'error' in results ? (results.error instanceof Error ? results.error.message : results.error) : 'Axe-core analysis failed';
        throw new Error(errorMessage);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      this.errorHandler.handleError(error, 'Axe-core run method failed');

      return {
        status: 'error',
        error: errorMessage,
      };
    }
  }
}
