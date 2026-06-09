import { AnalysisResult, BatchResult, PageInfo, ProcessedViolation } from '../../core/types/common';
import { BrowserManager } from '../../core/utils/browser-manager';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ConfigurationService } from '../services/configuration-service';
import { Page } from '@playwright/test';

export interface ParallelAnalysisOptions {
  maxConcurrency?: number;
  batchSize?: number;
  delayBetweenBatches?: number;
  retryFailedPages?: boolean;
  maxRetries?: number;
  skipOnError?: boolean;
}

export interface ToolRunners {
  axeRunner: any;
  pa11yRunner: any;
}

export class ParallelAnalyzer {
  private browserManager = BrowserManager.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private config = ConfigurationService.getInstance();
  private semaphore: (string | null)[] = [];

  constructor(private maxConcurrency: number = 5) {
    this.semaphore = new Array(maxConcurrency).fill(null);
  }

  async analyzePages(
    pages: PageInfo[],
    options: ParallelAnalysisOptions = {}
  ): Promise<BatchResult> {
    const {
      maxConcurrency = this.maxConcurrency,
      batchSize = 10,
      delayBetweenBatches = 1000,
      retryFailedPages = true,
      maxRetries = 2,
      skipOnError = false,
    } = options;

    this.errorHandler.logInfo('Starting parallel analysis', {
      totalPages: pages.length,
      maxConcurrency,
      batchSize,
    });

    const startTime = Date.now();
    const successful: AnalysisResult[] = [];
    const failed: Array<{ page: PageInfo; error: string }> = [];

    // Create batches
    const batches = this.createBatches(pages, batchSize);

    for (let i = 0; i < batches.length; i++) {
      const batch = batches[i];
      if (!batch) continue;

      this.errorHandler.logInfo(`Processing batch ${i + 1}/${batches.length}`, {
        batchSize: batch.length,
      });

      try {
        const batchResults = await this.processBatch(
          batch,
          maxConcurrency,
          retryFailedPages,
          maxRetries
        );

        successful.push(...batchResults.successful);
        failed.push(...batchResults.failed);

        // Delay between batches to prevent overwhelming the target server
        if (i < batches.length - 1 && delayBetweenBatches > 0) {
          await this.delay(delayBetweenBatches);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';

        if (skipOnError) {
          this.errorHandler.logWarning(`Batch ${i + 1} failed, skipping`, { error: errorMessage });

          // Mark all pages in this batch as failed
          batch?.forEach(page => {
            failed.push({ page, error: errorMessage });
          });
        } else {
          this.errorHandler.handleError(error, `Batch ${i + 1} processing failed`);
          throw error;
        }
      }
    }

    const totalTime = Date.now() - startTime;
    const totalProcessed = successful.length + failed.length;
    const successRate = totalProcessed > 0 ? (successful.length / totalProcessed) * 100 : 0;

    const metrics = {
      totalTime,
      averageTimePerPage: totalProcessed > 0 ? totalTime / totalProcessed : 0,
      successRate,
    };

    this.errorHandler.logSuccess('Parallel analysis completed', {
      successful: successful.length,
      failed: failed.length,
      successRate: `${successRate.toFixed(1)}%`,
      totalTime: `${totalTime}ms`,
    });

    return {
      successful,
      failed,
      metrics,
    };
  }

  private createBatches<T>(items: T[], batchSize: number): T[][] {
    const batches: T[][] = [];

    for (let i = 0; i < items.length; i += batchSize) {
      batches.push(items.slice(i, i + batchSize));
    }

    return batches;
  }

  private async processBatch(
    batch: PageInfo[],
    maxConcurrency: number,
    retryFailedPages: boolean,
    maxRetries: number
  ): Promise<BatchResult> {
    const successful: AnalysisResult[] = [];
    const failed: Array<{ page: PageInfo; error: string }> = [];
    const semaphore = new Array(maxConcurrency).fill(null);

    const processPage = async (page: PageInfo, retryCount: number = 0): Promise<void> => {
      try {
        this.errorHandler.logInfo(`[DEBUG] Starting analysis for page: ${page.url}`);
        const sessionId = `analysis-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        // Navigate to page
        this.errorHandler.logInfo(`[DEBUG] Navigating to page: ${page.url}`);
        const playwrightPage = await this.browserManager.navigateToUrl(sessionId, page.url);
        this.errorHandler.logInfo(`[DEBUG] Navigation complete for: ${page.url}`);

        // Create tool runners for this page
        this.errorHandler.logInfo(`[DEBUG] Registering accessibility tools for: ${page.url}`);
        const toolRunners = await this.registerAccessibilityTools(playwrightPage);
        this.errorHandler.logInfo(`[DEBUG] Tool runners created for: ${page.url}`);

        // Run comprehensive accessibility analysis
        this.errorHandler.logInfo(`[DEBUG] Running comprehensive analysis for: ${page.url}`);
        const analysisResult = await this.runComprehensiveAnalysis(page, toolRunners);
        this.errorHandler.logInfo(`[DEBUG] Analysis complete for: ${page.url}`);

        successful.push(analysisResult);

        // Only close the specific page, not the entire session
        // This allows the browser to remain open for PDF generation
        await this.browserManager.closePage(sessionId);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';
        this.errorHandler.logWarning(
          `[DEBUG] Error during analysis for ${page.url}: ${errorMessage}`
        );
        if (retryFailedPages && retryCount < maxRetries) {
          this.errorHandler.logWarning(
            `Retrying page ${page.url} (attempt ${retryCount + 1}/${maxRetries})`
          );
          await this.delay(1000 * (retryCount + 1)); // Exponential backoff
          await processPage(page, retryCount + 1);
        } else {
          this.errorHandler.handleError(error, `Failed to analyze page: ${page.url}`);
          failed.push({ page, error: errorMessage });
        }
      }
    };

    // Process pages with concurrency control
    const pagePromises = batch.map(async (page, _index) => {
      return new Promise<void>(resolve => {
        let timeoutId: NodeJS.Timeout | undefined;
        const runWhenReady = () => {
          const availableSlot = semaphore.findIndex(slot => slot === null);
          if (availableSlot !== -1) {
            // Clear any pending timeout
            if (timeoutId) {
              clearTimeout(timeoutId);
            }
            semaphore[availableSlot] = page.url;
            processPage(page).finally(() => {
              semaphore[availableSlot] = null;
              resolve();
            });
          } else {
            timeoutId = setTimeout(runWhenReady, 100);
          }
        };
        runWhenReady();
      });
    });

    await Promise.all(pagePromises);

    return {
      successful,
      failed,
      metrics: {
        totalTime: 0, // Will be calculated by parent
        averageTimePerPage: 0,
        successRate: (successful.length / (successful.length + failed.length)) * 100,
      },
    };
  }

  /**
   * Registers all available accessibility testing tools with the ToolOrchestrator
   * @param page The Playwright page instance
   */
  private async registerAccessibilityTools(page: Page): Promise<ToolRunners> {
    try {
      this.errorHandler.logInfo(`[DEBUG] Importing accessibility tool runners...`);
      // Import accessibility testing tools
      const { AxeTestRunner } = await import('@/utils/runners/axe-test-runner');
      const { Pa11yTestRunner } = await import('@/utils/runners/pa11y-test-runner');

      this.errorHandler.logInfo(`[DEBUG] Instantiating tool runners...`);
      // Create tool instances with the page
      const axeRunner = new AxeTestRunner(page);
      const pa11yRunner = new Pa11yTestRunner(page);

      this.errorHandler.logSuccess('Successfully created all accessibility testing tools', {
        tools: ['axe-core', 'pa11y'],
      });

      return {
        axeRunner,
        pa11yRunner,
      };
    } catch (error) {
      this.errorHandler.handleError(
        error,
        'Failed to create one or more accessibility testing tools'
      );
      throw new Error('Could not create accessibility tool runners');
    }
  }

  /**
   * Runs a comprehensive accessibility analysis using all registered tools
   * @param page The page to analyze
   * @param toolRunners The tool runners to use
   * @returns The analysis result
   */
  private async runComprehensiveAnalysis(
    page: PageInfo,
    toolRunners: ToolRunners
  ): Promise<AnalysisResult> {
    const { axeRunner, pa11yRunner } = toolRunners;

    this.errorHandler.logInfo(`Running multi-tool analysis for ${page.url}`);
    const startTime = Date.now();

    try {
      this.errorHandler.logInfo(`[DEBUG] Running axe-core and pa11y analysis for ${page.url}`);
      const results = await Promise.all([axeRunner.run(), pa11yRunner.run()]);

      this.errorHandler.logInfo(`[DEBUG] Tool results received for ${page.url}:`, {
        axeStatus: results[0]?.status,
        pa11yStatus: results[1]?.status,
        axeData: results[0]?.data ? 'present' : 'missing',
        pa11yData: results[1]?.data ? 'present' : 'missing',
      });

      const toolErrors = results
        .filter(result => result.status === 'error')
        .map(result => result.error || 'Unknown error');

      if (toolErrors.length > 0) {
        this.errorHandler.logWarning(`Some tools failed during analysis of ${page.url}`, {
          errors: toolErrors,
        });
      }

      const successfulResults = results.filter(
        result => result.status === 'success' && result.data
      );

      this.errorHandler.logInfo(`[DEBUG] Successful results for ${page.url}:`, {
        count: successfulResults.length,
        tools: successfulResults.map((r: any) => r.data?.tool),
      });

      const allViolations: ProcessedViolation[] = successfulResults.flatMap((result: any) => {
        const toolName = result.data.tool;
        this.errorHandler.logInfo(`[DEBUG] Processing ${toolName} data for ${page.url}:`, {
          violationsCount: result.data.violations?.length || 0,
          dataKeys: Object.keys(result.data),
        });

        try {
          const violations = this.extractViolations(result.data, toolName);
          this.errorHandler.logInfo(`Extracted ${violations.length} violations for ${toolName}`);
          return violations;
        } catch (error) {
          this.errorHandler.logWarning(`Failed to extract violations for ${toolName}: ${error}`, {
            toolName,
            url: page.url,
            resultData: result.data,
          });
          return [];
        }
      });

      this.errorHandler.logSuccess(`Multi-tool analysis complete for ${page.url}`, {
        violations: allViolations.length,
        duration: Date.now() - startTime,
      });

      const violationSummary = this.calculateViolationSummary(allViolations);

      return {
        url: page.url,
        timestamp: new Date().toISOString(),
        tool: 'parallel-analyzer',
        violations: allViolations,
        summary: violationSummary,
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      this.errorHandler.handleError(error, `Comprehensive analysis failed for ${page.url}`);

      return {
        url: page.url,
        timestamp: new Date().toISOString(),
        tool: 'parallel-analyzer',
        violations: [],
        summary: {
          totalViolations: 0,
          criticalViolations: 0,
          seriousViolations: 0,
          moderateViolations: 0,
          minorViolations: 0,
        },
      };
    }
  }

  private extractViolations(toolData: any, toolName: string): ProcessedViolation[] {
    this.errorHandler.logInfo(`[DEBUG] Extracting violations for ${toolName}:`, {
      hasToolData: !!toolData,
      hasViolations: !!toolData?.violations,
      violationsLength: toolData?.violations?.length || 0,
      toolDataKeys: toolData ? Object.keys(toolData) : [],
    });

    if (!toolData || !toolData.violations) {
      this.errorHandler.logWarning(`No violations data found for ${toolName}`, { toolData });
      return [];
    }

    // Add detailed debugging for the first few violations
    if (toolData.violations.length > 0) {
      this.errorHandler.logInfo(`[DEBUG] Sample violation structure for ${toolName}:`, {
        sampleViolation: toolData.violations[0],
        totalViolations: toolData.violations.length,
      });
    }

    const violations: ProcessedViolation[] = [];

    switch (toolName) {
      case 'axe-core':
        for (const v of toolData.violations) {
          try {
            violations.push({
              id: v.id || 'axe-' + v.ruleId || 'unknown',
              tools: ['axe-core'],
              description: v.description,
              impact: v.impact,
              wcagLevel: this.mapWcagTagsToLevel(v.tags),
              helpUrl: v.helpUrl,
              help: v.help || v.description,
              wcagTags: v.tags || [],
              occurrences: v.nodes?.length || 1,
              elements: v.nodes?.map((n: any) => ({
                html: n.html,
                target: n.target,
                failureSummary: n.failureSummary,
                selector: n.target?.join(', ') || '',
              })) || [],
              scenarioRelevance: [],
              remediation: {
                priority: v.impact === 'critical' ? 'High' : v.impact === 'serious' ? 'High' : 'Medium',
                effort: v.impact === 'critical' ? 'High' : 'Medium',
                suggestions: [v.help || v.description],
              },
            });
          } catch (error) {
            this.errorHandler.logWarning(`Failed to process axe-core violation: ${error}`, { violation: v });
          }
        }
        return violations;
      case 'pa11y':
        for (const v of toolData.violations) {
          try {
            violations.push({
              id: v.id || 'pa11y-' + v.code || 'unknown',
              tools: ['pa11y'],
              description: v.description,
              impact: v.impact,
              wcagLevel: this.mapPa11yWcagLevel(v.code),
              helpUrl: v.helpUrl,
              help: v.description,
              wcagTags: v.tags || [],
              occurrences: 1,
              elements: v.nodes?.map((n: any) => ({
                html: n.html,
                target: n.target,
                failureSummary: n.failureSummary,
                selector: Array.isArray(n.target) ? n.target.join(', ') : n.target || '',
              })) || [],
              scenarioRelevance: [],
              remediation: {
                priority: v.impact === 'critical' ? 'High' : v.impact === 'serious' ? 'High' : 'Medium',
                effort: v.impact === 'critical' ? 'High' : 'Medium',
                suggestions: [v.description],
              },
            });
          } catch (error) {
            this.errorHandler.logWarning(`Failed to process pa11y violation: ${error}`, { violation: v });
          }
        }
        return violations;
      default:
        this.errorHandler.logWarning(`Unknown tool for violation extraction: ${toolName}`);
        return [];
    }
  }

  private mapWcagTagsToLevel(tags: string[] | undefined | null): 'A' | 'AA' | 'AAA' | 'Unknown' {
    // Handle undefined or null tags
    if (!tags || !Array.isArray(tags)) {
      return 'Unknown';
    }

    // Check for WCAG 2.1 and 2.2 tags first
    if (tags.includes('wcag21aaa') || tags.includes('wcag22aaa') || tags.includes('wcag2aaa')) return 'AAA';
    if (tags.includes('wcag21aa') || tags.includes('wcag22aa') || tags.includes('wcag2aa')) return 'AA';
    if (tags.includes('wcag21a') || tags.includes('wcag22a') || tags.includes('wcag2a')) return 'A';

    // Check for WCAG 2.0 tags
    if (tags.includes('wcag2aaa')) return 'AAA';
    if (tags.includes('wcag2aa')) return 'AA';
    if (tags.includes('wcag2a')) return 'A';

    // Check for section tags that indicate WCAG levels
    if (tags.some(tag => tag.includes('section508'))) return 'AA'; // Section 508 is roughly equivalent to AA

    return 'Unknown';
  }

  private mapPa11yWcagLevel(code: string | undefined | null): 'A' | 'AA' | 'AAA' | 'Unknown' {
    // Handle undefined or null code
    if (!code || typeof code !== 'string') {
      return 'Unknown';
    }

    // Pa11y codes often contain WCAG level information
    if (code.includes('AAA') || code.includes('3')) return 'AAA';
    if (code.includes('AA') || code.includes('2')) return 'AA';
    if (code.includes('A') || code.includes('1')) return 'A';

    // Check for specific Pa11y rule codes that indicate WCAG levels
    const wcagLevelMap: Record<string, 'A' | 'AA' | 'AAA'> = {
      'WCAG2AA.Principle1.Guideline1_1.1_1_1': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_1': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_2': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_3': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_4': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_5': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_6': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_7': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_8': 'A',
      'WCAG2AA.Principle1.Guideline1_2.1_2_9': 'A',
      'WCAG2AA.Principle1.Guideline1_3.1_3_1': 'A',
      'WCAG2AA.Principle1.Guideline1_3.1_3_2': 'A',
      'WCAG2AA.Principle1.Guideline1_3.1_3_3': 'A',
      'WCAG2AA.Principle1.Guideline1_4.1_4_1': 'AA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_2': 'AA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_3': 'AAA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_4': 'AA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_5': 'AA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_6': 'AAA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_7': 'AAA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_8': 'AAA',
      'WCAG2AA.Principle1.Guideline1_4.1_4_9': 'AAA',
      'WCAG2AA.Principle2.Guideline2_1.2_1_1': 'A',
      'WCAG2AA.Principle2.Guideline2_1.2_1_2': 'A',
      'WCAG2AA.Principle2.Guideline2_1.2_1_3': 'AAA',
      'WCAG2AA.Principle2.Guideline2_1.2_1_4': 'AAA',
      'WCAG2AA.Principle2.Guideline2_2.2_2_1': 'A',
      'WCAG2AA.Principle2.Guideline2_2.2_2_2': 'A',
      'WCAG2AA.Principle2.Guideline2_3.2_3_1': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_1': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_2': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_3': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_4': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_5': 'AA',
      'WCAG2AA.Principle2.Guideline2_4.2_4_6': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_7': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_8': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_9': 'A',
      'WCAG2AA.Principle2.Guideline2_4.2_4_10': 'A',
      'WCAG2AA.Principle3.Guideline3_1.3_1_1': 'A',
      'WCAG2AA.Principle3.Guideline3_1.3_1_2': 'AA',
      'WCAG2AA.Principle3.Guideline3_1.3_1_3': 'AAA',
      'WCAG2AA.Principle3.Guideline3_1.3_1_4': 'AA',
      'WCAG2AA.Principle3.Guideline3_1.3_1_5': 'AAA',
      'WCAG2AA.Principle3.Guideline3_1.3_1_6': 'AAA',
      'WCAG2AA.Principle3.Guideline3_2.3_2_1': 'A',
      'WCAG2AA.Principle3.Guideline3_2.3_2_2': 'A',
      'WCAG2AA.Principle3.Guideline3_2.3_2_3': 'A',
      'WCAG2AA.Principle3.Guideline3_2.3_2_4': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_1': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_2': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_3': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_4': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_5': 'AA',
      'WCAG2AA.Principle3.Guideline3_3.3_3_6': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_7': 'A',
      'WCAG2AA.Principle3.Guideline3_3.3_3_8': 'A',
      'WCAG2AA.Principle4.Guideline4_1.4_1_1': 'A',
      'WCAG2AA.Principle4.Guideline4_1.4_1_2': 'A',
      'WCAG2AA.Principle4.Guideline4_1.4_1_3': 'AA',
      'WCAG2AA.Principle4.Guideline4_1.4_1_4': 'A',
    };

    return wcagLevelMap[code] || 'Unknown';
  }

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

  private calculateViolationSummary(violations: ProcessedViolation[]): {
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
  } {
    const summary = {
      totalViolations: violations.length,
      criticalViolations: 0,
      seriousViolations: 0,
      moderateViolations: 0,
      minorViolations: 0,
    };

    violations.forEach(violation => {
      switch (violation.impact) {
        case 'critical':
          summary.criticalViolations++;
          break;
        case 'serious':
          summary.seriousViolations++;
          break;
        case 'moderate':
          summary.moderateViolations++;
          break;
        case 'minor':
          summary.minorViolations++;
          break;
      }
    });

    return summary;
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async cleanup(): Promise<void> {
    this.errorHandler.logInfo('Cleaning up parallel analyzer');

    // Clear any pending timeouts
    if (typeof jest !== 'undefined') {
      jest.clearAllTimers();
    }

    // Reset semaphore
    this.semaphore = [];

    await this.browserManager.cleanupAll();
  }

  getStatus(): {
    maxConcurrency: number;
    activeSessions: number;
    semaphoreState: (string | null)[];
  } {
    return {
      maxConcurrency: this.maxConcurrency,
      activeSessions: this.semaphore.filter(slot => slot !== null).length,
      semaphoreState: [...this.semaphore],
    };
  }

  updateConcurrency(newConcurrency: number): void {
    if (newConcurrency < 1) {
      throw new Error('Concurrency must be at least 1');
    }

    this.maxConcurrency = newConcurrency;

    // Adjust semaphore size
    if (newConcurrency > this.semaphore.length) {
      // Expand semaphore
      const expansion = new Array(newConcurrency - this.semaphore.length).fill(null);
      this.semaphore.push(...expansion);
    } else if (newConcurrency < this.semaphore.length) {
      // Shrink semaphore (only if no active sessions in the slots being removed)
      const slotsToRemove = this.semaphore.slice(newConcurrency);
      if (slotsToRemove.every(slot => slot === null)) {
        this.semaphore = this.semaphore.slice(0, newConcurrency);
      } else {
        this.errorHandler.logWarning(
          'Cannot reduce concurrency while sessions are active in affected slots'
        );
      }
    }

    this.errorHandler.logInfo(`Updated concurrency to ${newConcurrency}`);
  }
}
