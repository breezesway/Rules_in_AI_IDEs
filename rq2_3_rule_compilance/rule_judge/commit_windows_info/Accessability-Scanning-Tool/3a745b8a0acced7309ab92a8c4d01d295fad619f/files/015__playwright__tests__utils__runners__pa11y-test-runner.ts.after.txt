import { Page } from '@playwright/test';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';
import { Pa11yReporterFactory } from './pa11y-reporters';
import * as pa11y from 'pa11y';

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
      this.errorHandler.logInfo(
        `Filtered ${originalCount - pa11yResults.issues.length} notices to focus on actionable issues`
      );
    }

    this.errorHandler.logSuccess(
      `Pa11y analysis completed in ${duration}ms: ${pa11yResults.issues?.length || 0} issues found`
    );

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

  /**
   * Runs Pa11y analysis with custom reporter
   */
  async runAnalysisWithReporter(reporterType: string): Promise<ServiceResult<string>> {
    const result = await this.runAnalysis();

    if (!result.success || !result.data) {
      return { success: false, error: result.error };
    }

    try {
      const reporter = Pa11yReporterFactory.create(reporterType);
      const output = reporter.results(result.data);
      return { success: true, data: output };
    } catch (error) {
      return { success: false, error: `Failed to generate report: ${error.message}` };
    }
  }

  /**
   * Runs Pa11y analysis with WCAG-focused reporting
   */
  async runWCAGAnalysis(): Promise<ServiceResult<string>> {
    return this.runAnalysisWithReporter('wcag');
  }

  /**
   * Runs Pa11y analysis with JSON structured reporting
   */
  async runJSONStructuredAnalysis(): Promise<ServiceResult<string>> {
    return this.runAnalysisWithReporter('json-structured');
  }

  /**
   * Runs Pa11y analysis with category-based reporting
   */
  async runCategoryAnalysis(): Promise<ServiceResult<string>> {
    return this.runAnalysisWithReporter('category');
  }

  /**
   * Runs Pa11y analysis with executive summary reporting
   */
  async runExecutiveSummaryAnalysis(): Promise<ServiceResult<string>> {
    return this.runAnalysisWithReporter('executive');
  }

  /**
   * Runs Pa11y analysis with multiple reporters
   */
  async runMultiReporterAnalysis(
    reporterTypes: string[]
  ): Promise<ServiceResult<Record<string, string>>> {
    const result = await this.runAnalysis();

    if (!result.success || !result.data) {
      return { success: false, error: result.error };
    }

    try {
      const reports: Record<string, string> = {};

      for (const reporterType of reporterTypes) {
        const reporter = Pa11yReporterFactory.create(reporterType);
        reports[reporterType] = reporter.results(result.data);
      }

      return { success: true, data: reports };
    } catch (error) {
      return {
        success: false,
        error: `Failed to generate multi-reporter analysis: ${error.message}`,
      };
    }
  }

  /**
   * Gets available reporter types
   */
  getAvailableReporters(): string[] {
    return Pa11yReporterFactory.getAvailableReporters();
  }
}
