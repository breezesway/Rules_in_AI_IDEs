import { Page } from '@playwright/test';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';

export interface Pa11yResult {
    documentTitle: string;
    pageUrl: string;
    issues: Array<{
        code: string;
        type: string;
        message: string;
        context: string;
        selector: string;
        runner: string;
        runnerExtras: any;
    }>;
}

export class Pa11yTestRunner {
    private config = ConfigurationService.getInstance();
    private errorHandler = ErrorHandlerService.getInstance();

    constructor(private page: Page) { }

    /**
     * Runs Pa11y analysis
     */
    async runAnalysis(): Promise<ServiceResult<Pa11yResult>> {
        const config = this.config.getPa11yConfiguration();
        const currentUrl = this.page.url();

        this.errorHandler.logInfo(`Analyzing: ${currentUrl}`);

        return this.errorHandler.withTimeout(
            this.performPa11yAnalysis(),
            config.timeout,
            'Pa11y analysis'
        );
    }

    /**
     * Performs the actual Pa11y analysis
     */
    private async performPa11yAnalysis(): Promise<Pa11yResult> {
        const config = this.config.getPa11yConfiguration();
        const pa11y = require('pa11y');

        const pa11yOptions = {
            standard: config.standard,
            includeNotices: config.includeNotices,
            includeWarnings: config.includeWarnings,
            timeout: config.timeout,
            wait: config.wait,
            chromeLaunchConfig: config.chromeLaunchConfig,
            actions: [],
            hideElements: '',
            ignore: [],
        };

        // Run Pa11y analysis
        const startTime = Date.now();
        const results = await Promise.race([
            pa11y(this.page.url(), pa11yOptions),
            new Promise((_, reject) => {
                setTimeout(() => {
                    reject(new Error(`Pa11y analysis timed out after ${config.timeout}ms`));
                }, config.timeout);
            }),
        ]);

        const duration = Date.now() - startTime;

        if (!results || typeof results !== 'object') {
            throw new Error('Pa11y returned invalid results');
        }

        // Process results
        const pa11yResults = results as Pa11yResult;

        // Filter out notices if we have too many issues to keep output focused
        if (pa11yResults.issues && pa11yResults.issues.length > 500) {
            const originalCount = pa11yResults.issues.length;
            pa11yResults.issues = pa11yResults.issues.filter((issue: any) => issue.type !== 'notice');
            this.errorHandler.logInfo(`Filtered ${originalCount - pa11yResults.issues.length} notices to focus on actionable issues`);
        }

        this.errorHandler.logSuccess(`Pa11y analysis completed in ${duration}ms: ${pa11yResults.issues?.length || 0} issues found`);

        return pa11yResults;
    }

    /**
     * Runs Pa11y analysis with retry logic
     */
    async runAnalysisWithRetry(maxRetries: number = 3): Promise<ServiceResult<Pa11yResult>> {
        return this.errorHandler.retryWithBackoff(
            () => this.performPa11yAnalysis(),
            maxRetries,
            'Pa11y analysis with retry'
        );
    }
} 