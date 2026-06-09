import { AnalysisResult, BatchResult, PageInfo } from '../../core/types/common';
import { BrowserManager } from '../../core/utils/browser-manager';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { ConfigurationService } from '../../../playwright/tests/utils/services/configuration-service';

export interface ParallelAnalysisOptions {
  maxConcurrency?: number;
  batchSize?: number;
  delayBetweenBatches?: number;
  retryFailedPages?: boolean;
  maxRetries?: number;
  skipOnError?: boolean;
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
          batch.forEach(page => {
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
        const sessionId = `analysis-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        // Navigate to page
        const playwrightPage = await this.browserManager.navigateToUrl(sessionId, page.url);

        // Create tool orchestrator for this page
        const toolOrchestrator = new ToolOrchestrator(playwrightPage);

        // TODO: Register tools - this would be done during service initialization
        // For now, we'll simulate the analysis
        const analysisResult = await this.simulateAnalysis(page, playwrightPage);

        successful.push(analysisResult);

        // Cleanup
        await toolOrchestrator.cleanup();
        await this.browserManager.cleanup(sessionId);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';

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
        const runWhenReady = () => {
          const availableSlot = semaphore.findIndex(slot => slot === null);
          if (availableSlot !== -1) {
            semaphore[availableSlot] = page.url;
            processPage(page).finally(() => {
              semaphore[availableSlot] = null;
              resolve();
            });
          } else {
            setTimeout(runWhenReady, 100);
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

  private async simulateAnalysis(page: PageInfo, _playwrightPage: any): Promise<AnalysisResult> {
    // This is a placeholder - in the real implementation, this would use the ToolOrchestrator
    // to run actual accessibility analysis

    const _startTime = Date.now();

    // Simulate analysis time
    await this.delay(2000);

    return {
      url: page.url,
      timestamp: new Date().toISOString(),
      tool: 'parallel-analyzer',
      violations: [], // Would be populated by actual analysis
      summary: {
        totalViolations: 0,
        criticalViolations: 0,
        seriousViolations: 0,
        moderateViolations: 0,
        minorViolations: 0,
      },
    };
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async cleanup(): Promise<void> {
    this.errorHandler.logInfo('Cleaning up parallel analyzer');
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
