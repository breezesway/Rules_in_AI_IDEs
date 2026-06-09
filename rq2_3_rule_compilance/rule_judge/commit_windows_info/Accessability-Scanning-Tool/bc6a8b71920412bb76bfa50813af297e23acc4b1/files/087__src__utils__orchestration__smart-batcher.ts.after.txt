import { EventEmitter } from 'events';
import { AccessibilityTestOptions, AnalysisTask, ServiceResult } from '../../core/types/common.js';
import { AnalysisCache } from './analysis-cache.js';
import { TaskQueue } from './task-queue.js';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ConfigurationService } from '../services/configuration-service';

interface PageInfo {
  url: string;
  domain: string;
  path: string;
  depth: number;
  priority: 'low' | 'medium' | 'high';
  metadata?: Record<string, unknown>;
}

interface DomainBatch {
  domain: string;
  pages: PageInfo[];
  priority: 'low' | 'medium' | 'high';
  estimatedTime: number;
  batchSize: number;
}

export class SmartBatcher extends EventEmitter {
  private static instance: SmartBatcher;
  private analysisCache: AnalysisCache;
  private taskQueue: TaskQueue;
  private batchSizeConfig = {
    small: { maxSize: 5, domains: ['localhost', 'staging', 'dev'] },
    medium: { maxSize: 10, domains: ['medium-traffic'] },
    large: { maxSize: 20, domains: ['production', 'high-traffic'] },
  };
  private domainSpecificSettings: Map<
    string,
    {
      maxConcurrency: number;
      batchSize: number;
      timeout: number;
      retryCount: number;
    }
  > = new Map();

  private constructor() {
    super();
    this.analysisCache = AnalysisCache.getInstance();
    this.taskQueue = TaskQueue.getInstance();
    this.initializeDomainSettings();
  }

  public static getInstance(): SmartBatcher {
    if (!SmartBatcher.instance) {
      SmartBatcher.instance = new SmartBatcher();
    }
    return SmartBatcher.instance;
  }

  private initializeDomainSettings(): void {
    // Common domain patterns and their optimal settings
    this.domainSpecificSettings.set('localhost', {
      maxConcurrency: 10,
      batchSize: 20,
      timeout: 15000,
      retryCount: 2,
    });

    this.domainSpecificSettings.set('default', {
      maxConcurrency: 5,
      batchSize: 10,
      timeout: 30000,
      retryCount: 3,
    });

    // Add more domain-specific settings as needed
  }

  public async batchAnalysis(
    pages: PageInfo[],
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<AnalysisTask[]>> {
    try {
      // Group pages by domain
      const domainGroups = this.groupByDomain(pages);

      // Create optimized batches
      const batches = this.createOptimizedBatches(domainGroups, options);

      // Process batches in parallel with concurrency control
      const results = await this.processBatches(batches, options);

      const successCount = results.filter(r => r.success).length;
      const errorCount = results.length - successCount;

      return {
        success: errorCount === 0,
        data: results as any,
        message: `Batch analysis completed: ${successCount} successful, ${errorCount} failed`,
        metadata: {
          totalPages: pages.length,
          totalBatches: batches.length,
          successCount,
          errorCount,
          domains: Array.from(domainGroups.keys()),
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error as Error,
        message: `Batch analysis failed: ${(error as Error).message}`,
        metadata: {
          totalPages: pages.length,
          failedAt: new Date(),
        },
      };
    }
  }

  private groupByDomain(pages: PageInfo[]): Map<string, PageInfo[]> {
    const domainGroups = new Map<string, PageInfo[]>();

    for (const page of pages) {
      const domain = page.domain || this.extractDomain(page.url);

      if (!domainGroups.has(domain)) {
        domainGroups.set(domain, []);
      }

      domainGroups.get(domain)!.push({
        ...page,
        domain, // Ensure domain is set
      });
    }

    // Sort pages within each domain by priority and depth
    for (const [_domain, domainPages] of domainGroups) {
      domainPages.sort((a, b) => {
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];

        if (priorityDiff !== 0) {
          return priorityDiff;
        }

        // Secondary sort by depth (shallower pages first)
        return a.depth - b.depth;
      });
    }

    return domainGroups;
  }

  private createOptimizedBatches(
    domainGroups: Map<string, PageInfo[]>,
    options: AccessibilityTestOptions
  ): DomainBatch[] {
    const batches: DomainBatch[] = [];

    for (const [domain, pages] of domainGroups) {
      const domainSettings = this.getDomainSettings(domain);
      const batchSize = this.calculateOptimalBatchSize(domain, pages.length, options);

      // Split pages into batches
      for (let i = 0; i < pages.length; i += batchSize) {
        const batchPages = pages.slice(i, i + batchSize);
        const batch: DomainBatch = {
          domain,
          pages: batchPages,
          priority: this.calculateBatchPriority(batchPages),
          estimatedTime: this.estimateProcessingTime(batchPages, domainSettings),
          batchSize: batchPages.length,
        };

        batches.push(batch);
      }
    }

    // Sort batches by priority and estimated processing time
    batches.sort((a, b) => {
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];

      if (priorityDiff !== 0) {
        return priorityDiff;
      }

      // Secondary sort by estimated time (faster batches first)
      return a.estimatedTime - b.estimatedTime;
    });

    return batches;
  }

  private calculateOptimalBatchSize(
    domain: string,
    _totalPages: number,
    _options: AccessibilityTestOptions
  ): number {
    const domainSettings = this.getDomainSettings(domain);
    let optimalSize = domainSettings.batchSize;

    // Adjust based on cache hit ratio for this domain
    // TODO: Fix this type error
    const cacheStats = (this.analysisCache as any).getCacheStats();
    const domainCacheEntry = cacheStats.topDomains.find((d: any) => d.domain === domain);

    if (domainCacheEntry) {
      const cachePerformance = (this.analysisCache as any).getPerformance();
      if (cachePerformance.hitRate > 0.7) {
        // High cache hit rate, can increase batch size
        optimalSize = Math.min(optimalSize * 1.5, 30);
      } else if (cachePerformance.hitRate < 0.3) {
        // Low cache hit rate, decrease batch size
        optimalSize = Math.max(optimalSize * 0.7, 5);
      }
    }

    // Adjust based on system resources
    const memoryUsage = process.memoryUsage();
    const memoryPressure = memoryUsage.heapUsed / memoryUsage.heapTotal;

    if (memoryPressure > 0.8) {
      optimalSize = Math.max(optimalSize * 0.5, 3);
    } else if (memoryPressure < 0.4) {
      optimalSize = Math.min(optimalSize * 1.2, 25);
    }

    return Math.round(optimalSize);
  }

  private calculateBatchPriority(pages: PageInfo[]): 'low' | 'medium' | 'high' {
    const priorities = pages.map(p => p.priority);
    const highCount = priorities.filter(p => p === 'high').length;
    const mediumCount = priorities.filter(p => p === 'medium').length;

    if (highCount > pages.length * 0.5) {
      return 'high';
    } else if (mediumCount > pages.length * 0.3) {
      return 'medium';
    } else {
      return 'low';
    }
  }

  private estimateProcessingTime(pages: PageInfo[], domainSettings: { timeout: number }): number {
    // Base time estimation per page
    const baseTimePerPage = 8000; // 8 seconds average
    const timeoutBuffer = domainSettings.timeout * 0.1; // 10% of timeout as buffer

    // Adjust based on page depth (deeper pages might take longer)
    const averageDepth = pages.reduce((sum, p) => sum + p.depth, 0) / pages.length;
    const depthMultiplier = 1 + averageDepth * 0.1;

    return Math.round(
      baseTimePerPage * pages.length * depthMultiplier + timeoutBuffer * pages.length
    );
  }

  private async processBatches(
    batches: DomainBatch[],
    options: AccessibilityTestOptions
  ): Promise<ServiceResult<any>[]> {
    const results: ServiceResult<any>[] = [];
    const concurrencyLimit = 3; // Process up to 3 batches simultaneously

    // Process batches in chunks to control concurrency
    for (let i = 0; i < batches.length; i += concurrencyLimit) {
      const batchChunk = batches.slice(i, i + concurrencyLimit);

      const chunkPromises = batchChunk.map(batch => this.processSingleBatch(batch, options));

      const chunkResults = await Promise.all(chunkPromises);
      results.push(...chunkResults);

      // Emit progress event
      this.emit('batchProgress', {
        completed: i + batchChunk.length,
        total: batches.length,
        currentBatch: batchChunk.map(b => b.domain),
      });
    }

    return results;
  }

  private async processSingleBatch(
    batch: DomainBatch,
    options: AccessibilityTestOptions
  ): Promise<ServiceResult<any>> {
    const domainSettings = this.getDomainSettings(batch.domain);
    const batchUrls = batch.pages.map(p => p.url) as any;

    // Create analysis task
    const task: AnalysisTask = {
      id: `batch-${batch.domain}-${Date.now()}`,
      type: 'batch',
      url: batch.domain,
      priority: batch.priority,
      options: {
        ...options,
        // TODO: Fix this type error
        batchUrls: batch.pages.map(p => p.url) as any,
        domainSettings: this.getDomainSettings(batch.domain),
      },
      retryCount: 0,
      maxRetries: this.getDomainSettings(batch.domain).retryCount,
      createdAt: new Date(),
    };

    try {
      // Add task to queue
      const taskId = await this.taskQueue.addTask(task);

      // Wait for completion
      const result = await this.taskQueue.waitForCompletion(taskId, batch.estimatedTime + 30000);

      this.emit('batchCompleted', {
        domain: batch.domain,
        pagesProcessed: batch.pages.length,
        success: result.success,
        duration: result.duration,
      });

      return (
        result.result || {
          success: result.success,
          data: null,
          message: result.success ? 'Batch completed successfully' : 'Batch failed',
        }
      );
    } catch (error) {
      this.emit('batchError', {
        domain: batch.domain,
        error: (error as Error).message,
        pagesAffected: batch.pages.length,
      });

      return {
        success: false,
        error: error as Error,
        message: `Batch processing failed for domain ${batch.domain}: ${(error as Error).message}`,
        metadata: {
          domain: batch.domain,
          pagesAffected: batch.pages.length,
        },
      };
    }
  }

  private getDomainSettings(domain: string) {
    return this.domainSpecificSettings.get(domain) || this.domainSpecificSettings.get('default')!;
  }

  private extractDomain(url: string): string {
    try {
      return new URL(url).hostname;
    } catch {
      return 'unknown';
    }
  }

  public addDomainSettings(
    domain: string,
    settings: {
      maxConcurrency: number;
      batchSize: number;
      timeout: number;
      retryCount: number;
    }
  ): void {
    this.domainSpecificSettings.set(domain, settings);
  }

  public getBatchingStats(): {
    totalBatchesProcessed: number;
    averageBatchSize: number;
    averageProcessingTime: number;
    domainDistribution: Array<{ domain: string; batches: number }>;
  } {
    // This would be tracked and calculated based on processed batches
    return {
      totalBatchesProcessed: 0,
      averageBatchSize: 0,
      averageProcessingTime: 0,
      domainDistribution: [],
    };
  }

  public async optimizeBatchSizes(): Promise<void> {
    const cacheStats = (this.analysisCache as any).getCacheStats();

    for (const [domain, settings] of this.domainSpecificSettings) {
      // Analyze performance metrics for this domain
      const domainCacheEntry = cacheStats.topDomains.find((d: any) => d.domain === domain);
      if (domainCacheEntry) {
        const hitRate =
          domainCacheEntry.hits / (domainCacheEntry.hits + domainCacheEntry.misses);
        if (hitRate > 0.8 && settings.batchSize < 25) {
          settings.batchSize = Math.min(settings.batchSize + 2, 25);
        } else if (hitRate < 0.2 && settings.batchSize > 5) {
          settings.batchSize = Math.max(settings.batchSize - 2, 5);
        }
      }

      // Adjust based on overall system health
      // No-op as PerformanceMonitor is removed
    }
  }
}
