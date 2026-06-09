import { Page } from '@playwright/test';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ServiceResult } from '@/core/types/common';
// Fix: Use default import for pa11y instead of named import
import pa11y from 'pa11y';

export interface Pa11yIssue {
  code: string;
  type: string;
  message: string;
  context: string;
  selector: string;
  runner: string;
  runnerExtras: Record<string, unknown>;
}

export interface Pa11yResult {
  documentTitle: string;
  pageUrl: string;
  issues: Pa11yIssue[];
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

    // Create a timeout promise that can be cleaned up
    let timeoutId: NodeJS.Timeout | undefined;
    const timeoutPromise = new Promise<never>((_, reject) => {
      timeoutId = setTimeout(() => {
        reject(new Error(`Pa11y analysis timed out after ${config.timeout}ms`));
      }, config.timeout);
    });

    let results: any;
    try {
      results = await Promise.race([
        pa11y(this.page.url(), pa11yOptions),
        timeoutPromise,
      ]);

      // Clear the timeout if the promise resolves
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    } catch (error) {
      // Clear the timeout if there's an error
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      throw error;
    }

    if (!results || typeof results !== 'object') {
      throw new Error('Pa11y returned invalid results');
    }

    // Process results
    const pa11yResults = results as Pa11yResult;
    const duration = Date.now() - startTime;

    // Filter out notices if we have too many issues to keep output focused
    if (pa11yResults.issues && pa11yResults.issues.length > 500) {
      const originalCount = pa11yResults.issues.length;
      pa11yResults.issues = pa11yResults.issues.filter(
        (issue: Pa11yIssue) => issue.type !== 'notice'
      );
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
 * Main run method called by the ParallelAnalyzer
 * Returns data in the format expected by the orchestrator
 */
  public async run(): Promise<{ status: string; data?: any; error?: string }> {
    try {
      this.errorHandler.logInfo('Starting Pa11y analysis');

      // Use basic analysis instead of retry logic to avoid potential issues
      const results = await this.runAnalysis();

      if (results.success && results.data) {
        this.errorHandler.logInfo('Pa11y analysis completed successfully', {
          issues: results.data.issues?.length || 0,
        });

        // Convert Pa11y issues to violations format
        const violations = results.data.issues?.map((issue: Pa11yIssue) => ({
          id: issue.code,
          code: issue.code, // Add code field for WCAG level mapping
          description: issue.message,
          impact: this.mapPa11yTypeToImpact(issue.type),
          tags: [issue.code],
          helpUrl: `https://www.w3.org/TR/WCAG21/#${issue.code.split('.')[3]}`,
          nodes: [{
            html: issue.context,
            target: [issue.selector],
            failureSummary: issue.message,
          }],
        })) || [];

        return {
          status: 'success',
          data: {
            tool: 'pa11y',
            violations: violations,
            timestamp: new Date().toISOString(),
          },
        };
      } else {
        const errorMessage = 'error' in results ? (results.error instanceof Error ? results.error.message : results.error) : 'Pa11y analysis failed';
        throw new Error(errorMessage);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      this.errorHandler.handleError(error, 'Pa11y run method failed');

      return {
        status: 'error',
        error: errorMessage,
      };
    }
  }

  /**
   * Maps Pa11y issue types to impact levels
   */
  private mapPa11yTypeToImpact(type: string): 'minor' | 'moderate' | 'serious' | 'critical' {
    switch (type.toLowerCase()) {
      case 'error':
        return 'critical';
      case 'warning':
        return 'moderate';
      case 'notice':
        return 'minor';
      default:
        return 'moderate';
    }
  }
}
