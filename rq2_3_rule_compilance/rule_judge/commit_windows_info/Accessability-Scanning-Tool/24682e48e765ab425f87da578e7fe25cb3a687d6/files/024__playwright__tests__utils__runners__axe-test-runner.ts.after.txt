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
                'tabindex': { enabled: true },
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
                'label': { enabled: true },
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
     * Performs the actual axe analysis
     */
    private async performAxeAnalysis(options: AxeTestOptions): Promise<AxeResults> {
        const config = this.config.getAxeConfiguration();

        // Merge options with default configuration
        const mergedOptions = {
            tags: options.tags || config.tags,
            rules: options.rules || config.rules,
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

        this.errorHandler.logInfo(`Running axe-core analysis with tags: ${mergedOptions.tags?.join(', ')}`);

        const results = await axeBuilder.analyze();

        this.errorHandler.logSuccess(`Axe analysis completed: ${results.violations.length} violations found`);

        return results;
    }
} 