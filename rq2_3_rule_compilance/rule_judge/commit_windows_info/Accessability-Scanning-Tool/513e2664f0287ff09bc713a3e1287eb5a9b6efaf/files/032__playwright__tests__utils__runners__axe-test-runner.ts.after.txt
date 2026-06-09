import { Page } from '@playwright/test';
import { AxeResults } from 'axe-core';
import AxeBuilder from '@axe-core/playwright';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';

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

  constructor(private page: Page) {}

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

    return this.errorHandler.withTimeout(
      this.performAxeAnalysis(options),
      config.timeout,
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
      reporter: 'v2',
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
      reporter: 'v2',
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
      reporter: 'v2',
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
  async runCustomDevToolsAnalysis(customConfig: any): Promise<ServiceResult<AxeResults>> {
    return this.runAnalysis({
      devtools: true,
      shadow: true,
      iframes: true,
      reporter: 'v2',
      ...customConfig,
    });
  }

  /**
   * Performs the actual axe analysis
   */
  private async performAxeAnalysis(options: AxeTestOptions): Promise<AxeResults> {
    const config = this.config.getAxeConfiguration();

    // Merge options with default configuration
    const mergedOptions = {
      tags: options.tags || config?.tags || [],
      rules: options.rules || config?.rules || {},
      devtools: options.devtools || false,
      shadow: options.shadow || false,
      iframes: options.iframes || false,
      reporter: options.reporter || 'v2',
      allowedOrigins: options.allowedOrigins || [],
    };

    let axeBuilder = new AxeBuilder({ page: this.page });

    // Configure axe builder
    if (mergedOptions.tags?.length) {
      axeBuilder = axeBuilder.withTags(mergedOptions.tags);
    }

    if (mergedOptions.rules) {
      for (const [rule, config] of Object.entries(mergedOptions.rules)) {
        if (config.enabled) {
          axeBuilder = axeBuilder.withRules([rule]);
        } else {
          axeBuilder = axeBuilder.disableRules([rule]);
        }
      }
    }

    if (options.include?.length) {
      axeBuilder = axeBuilder.include(options.include);
    }

    if (options.exclude?.length) {
      axeBuilder = axeBuilder.exclude(options.exclude);
    }

    // DevTools-specific configuration
    if (mergedOptions.devtools) {
      // Enable DevTools mode with enhanced analysis
      await this.page.addScriptTag({
        content: `
          window.axeDevToolsMode = true;
          window.axeEnhancedAnalysis = true;
        `,
      });
    }

    // Shadow DOM configuration
    if (mergedOptions.shadow) {
      await this.page.addScriptTag({
        content: `
          if (window.axe) {
            window.axe.configure({
              shadowdom: true,
              rules: {
                'color-contrast': { enabled: true },
                'focus-order-semantics': { enabled: true },
                'landmark-one-main': { enabled: true },
              }
            });
          }
        `,
      });
    }

    // Iframe configuration
    if (mergedOptions.iframes) {
      await this.page.addScriptTag({
        content: `
          if (window.axe) {
            window.axe.configure({
              iframes: true,
              allowedOrigins: ${JSON.stringify(mergedOptions.allowedOrigins)},
            });
          }
        `,
      });
    }

    // Custom reporter configuration
    if (mergedOptions.reporter && mergedOptions.reporter !== 'v2') {
      await this.page.addScriptTag({
        content: `
          if (window.axe) {
            window.axe.configure({
              reporter: '${mergedOptions.reporter}',
            });
          }
        `,
      });
    }

    this.errorHandler.logInfo(
      `Running axe-core analysis with tags: ${mergedOptions.tags?.join(', ')}, DevTools: ${mergedOptions.devtools}, Shadow DOM: ${mergedOptions.shadow}, Iframes: ${mergedOptions.iframes}`
    );

    const results = await axeBuilder.analyze();

    this.errorHandler.logSuccess(
      `Axe DevTools analysis completed: ${results.violations.length} violations found`
    );

    return results;
  }
}
