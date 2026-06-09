import { EventEmitter } from 'events';
import { AccessibilityTestOptions, ServiceResult } from '../../core/types/common';
import { PerformanceMonitor } from '../../core/utils/performance-monitor';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { AnalysisCache } from '../orchestration/analysis-cache';
import { ToolOrchestrator } from '../analysis/tool-orchestrator';
import { ParallelAnalyzer } from '../orchestration/parallel-analyzer';
import { BrowserManager } from '../../core/utils/browser-manager';

export class AnalysisService extends EventEmitter {
  private static instance: AnalysisService;
  private toolOrchestrator: ToolOrchestrator;
  private parallelAnalyzer: ParallelAnalyzer;
  private performanceMonitor: PerformanceMonitor;
  private errorHandler: ErrorHandlerService;
  private analysisCache: AnalysisCache;
  private browserManager: BrowserManager;
  private activeAnalyses: Map<
    string,
    {
      url: string;
      startTime: Date;
      status: 'pending' | 'analyzing' | 'completed' | 'failed';
      pagesTotal: number;
      pagesCompleted: number;
      type: 'single' | 'site' | 'batch';
    }
  > = new Map();

  private constructor() {
    super();
    this.toolOrchestrator = ToolOrchestrator.getInstance();
    this.parallelAnalyzer = ParallelAnalyzer.getInstance();
    this.performanceMonitor = PerformanceMonitor.getInstance();
    this.errorHandler = ErrorHandlerService.getInstance();
    this.analysisCache = AnalysisCache.getInstance();
    this.browserManager = BrowserManager.getInstance();
  }

  public static getInstance(): AnalysisService {
    if (!AnalysisService.instance) {
      AnalysisService.instance = new AnalysisService();
    }
    return AnalysisService.instance;
  }

  public async analyzePage(
    url: string,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const analysisId = this.generateAnalysisId();
    const timer = this.performanceMonitor.startTimer(`analysis_page_${analysisId}`);

    try {
      // Check cache first
      const cachedResult = await this.analysisCache.getOrAnalyze(
        `page_analysis_${url}`,
        () => this.performPageAnalysis(url, options, analysisId),
        { ttl: 1800000 } // 30 minutes cache
      );

      timer.stop();
      return cachedResult;
    } catch (error) {
      timer.stop();
      this.updateAnalysisStatus(analysisId, 'failed', 1, 0);
      this.errorHandler.handleError(error as Error, 'AnalysisService.analyzePage');

      return {
        success: false,
        error: error as Error,
        message: `Page analysis failed: ${(error as Error).message}`,
      };
    }
  }

  private async performPageAnalysis(
    url: string,
    options: AccessibilityTestOptions,
    analysisId: string
  ): Promise<ServiceResult<any>> {
    this.activeAnalyses.set(analysisId, {
      url,
      startTime: new Date(),
      status: 'pending',
      pagesTotal: 1,
      pagesCompleted: 0,
      type: 'single',
    });

    try {
      this.updateAnalysisStatus(analysisId, 'analyzing', 1, 0);
      this.emit('analysisStarted', { analysisId, url, type: 'single' });

      const page = await this.browserManager.getPage();

      try {
        await page.goto(url, {
          waitUntil: 'networkidle',
          timeout: options.timeout || 30000,
        });

        const result = await this.toolOrchestrator.analyzePageWithTools(page, options);

        this.updateAnalysisStatus(analysisId, 'completed', 1, 1);

        const serviceResult = {
          success: true,
          data: result,
          message: `Page analysis completed for ${url}`,
        };

        this.emit('analysisCompleted', { analysisId, result: serviceResult });
        return serviceResult;
      } finally {
        await this.browserManager.releasePage(page);
      }
    } catch (error) {
      this.updateAnalysisStatus(analysisId, 'failed', 1, 0);
      this.emit('analysisFailed', { analysisId, error });

      return {
        success: false,
        error: error as Error,
        message: `Page analysis failed: ${(error as Error).message}`,
      };
    } finally {
      setTimeout(() => {
        this.activeAnalyses.delete(analysisId);
      }, 300000); // 5 minutes
    }
  }

  public async analyzePageDetailed(
    url: string,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const analysisId = this.generateAnalysisId();
    const timer = this.performanceMonitor.startTimer(`analysis_detailed_${analysisId}`);

    try {
      // Enhanced options for detailed analysis
      const detailedOptions = {
        ...options,
        includeScreenshots: true,
        detailedReporting: true,
        runAllTools: true,
        includePerformanceMetrics: true,
      };

      const result = await this.performPageAnalysis(url, detailedOptions, analysisId);
      timer.stop();
      return result;
    } catch (error) {
      timer.stop();
      this.errorHandler.handleError(error as Error, 'AnalysisService.analyzePageDetailed');

      return {
        success: false,
        error: error as Error,
        message: `Detailed page analysis failed: ${(error as Error).message}`,
      };
    }
  }

  public async analyzeSite(
    crawlData: any,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const analysisId = this.generateAnalysisId();
    const timer = this.performanceMonitor.startTimer(`analysis_site_${analysisId}`);

    try {
      const pages = crawlData.pages || [];

      this.activeAnalyses.set(analysisId, {
        url: crawlData.crawlMetrics?.baseUrl || 'unknown',
        startTime: new Date(),
        status: 'pending',
        pagesTotal: pages.length,
        pagesCompleted: 0,
        type: 'site',
      });

      this.updateAnalysisStatus(analysisId, 'analyzing', pages.length, 0);
      this.emit('analysisStarted', {
        analysisId,
        url: crawlData.crawlMetrics?.baseUrl,
        type: 'site',
      });

      // Use parallel analyzer for site analysis
      const analysisResult = await this.parallelAnalyzer.analyzeBatch(pages, options);

      this.updateAnalysisStatus(analysisId, 'completed', pages.length, pages.length);

      const result = {
        success: analysisResult.success,
        data: {
          ...analysisResult.data,
          crawlMetrics: crawlData.crawlMetrics,
          analysisMetrics: {
            totalPages: pages.length,
            analysisTime: Date.now() - this.activeAnalyses.get(analysisId)!.startTime.getTime(),
            analysisId,
          },
        },
        message: `Site analysis completed for ${pages.length} pages`,
      };

      this.emit('analysisCompleted', { analysisId, result });
      timer.stop();
      return result;
    } catch (error) {
      this.updateAnalysisStatus(analysisId, 'failed', 0, 0);
      this.emit('analysisFailed', { analysisId, error });
      timer.stop();

      return {
        success: false,
        error: error as Error,
        message: `Site analysis failed: ${(error as Error).message}`,
      };
    } finally {
      setTimeout(() => {
        this.activeAnalyses.delete(analysisId);
      }, 300000); // 5 minutes
    }
  }

  public async analyzeBatch(
    urls: string[],
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<any>> {
    const analysisId = this.generateAnalysisId();
    const timer = this.performanceMonitor.startTimer(`analysis_batch_${analysisId}`);

    try {
      const pages = urls.map(url => ({ url, title: '', depth: 0 }));

      this.activeAnalyses.set(analysisId, {
        url: urls[0] || 'batch',
        startTime: new Date(),
        status: 'pending',
        pagesTotal: urls.length,
        pagesCompleted: 0,
        type: 'batch',
      });

      this.updateAnalysisStatus(analysisId, 'analyzing', urls.length, 0);
      this.emit('analysisStarted', { analysisId, url: 'batch', type: 'batch' });

      const analysisResult = await this.parallelAnalyzer.analyzeBatch(pages, options);

      this.updateAnalysisStatus(analysisId, 'completed', urls.length, urls.length);

      const result = {
        success: analysisResult.success,
        data: {
          ...analysisResult.data,
          analysisMetrics: {
            totalPages: urls.length,
            analysisTime: Date.now() - this.activeAnalyses.get(analysisId)!.startTime.getTime(),
            analysisId,
          },
        },
        message: `Batch analysis completed for ${urls.length} pages`,
      };

      this.emit('analysisCompleted', { analysisId, result });
      timer.stop();
      return result;
    } catch (error) {
      this.updateAnalysisStatus(analysisId, 'failed', 0, 0);
      this.emit('analysisFailed', { analysisId, error });
      timer.stop();

      return {
        success: false,
        error: error as Error,
        message: `Batch analysis failed: ${(error as Error).message}`,
      };
    } finally {
      setTimeout(() => {
        this.activeAnalyses.delete(analysisId);
      }, 300000); // 5 minutes
    }
  }

  public getAnalysisStatus(analysisId: string): {
    analysisId: string;
    status: string;
    progress: number;
    pagesTotal: number;
    pagesCompleted: number;
    startTime: Date;
    type: string;
  } | null {
    const analysis = this.activeAnalyses.get(analysisId);
    if (!analysis) return null;

    const progress =
      analysis.pagesTotal > 0 ? (analysis.pagesCompleted / analysis.pagesTotal) * 100 : 0;

    return {
      analysisId,
      status: analysis.status,
      progress,
      pagesTotal: analysis.pagesTotal,
      pagesCompleted: analysis.pagesCompleted,
      startTime: analysis.startTime,
      type: analysis.type,
    };
  }

  public getActiveAnalyses(): Array<{
    analysisId: string;
    url: string;
    status: string;
    progress: number;
    pagesTotal: number;
    pagesCompleted: number;
    startTime: Date;
    type: string;
  }> {
    return Array.from(this.activeAnalyses.entries()).map(([analysisId, analysis]) => ({
      analysisId,
      url: analysis.url,
      status: analysis.status,
      progress: analysis.pagesTotal > 0 ? (analysis.pagesCompleted / analysis.pagesTotal) * 100 : 0,
      pagesTotal: analysis.pagesTotal,
      pagesCompleted: analysis.pagesCompleted,
      startTime: analysis.startTime,
      type: analysis.type,
    }));
  }

  public async cancelAnalysis(analysisId: string): Promise<ServiceResult<void>> {
    const analysis = this.activeAnalyses.get(analysisId);

    if (!analysis) {
      return {
        success: false,
        message: 'Analysis not found',
      };
    }

    if (analysis.status === 'completed' || analysis.status === 'failed') {
      return {
        success: false,
        message: 'Cannot cancel completed analysis',
      };
    }

    this.updateAnalysisStatus(analysisId, 'failed', analysis.pagesTotal, analysis.pagesCompleted);
    this.emit('analysisCancelled', { analysisId });

    return {
      success: true,
      message: 'Analysis cancelled successfully',
    };
  }

  private updateAnalysisStatus(
    analysisId: string,
    status: 'pending' | 'analyzing' | 'completed' | 'failed',
    pagesTotal: number,
    pagesCompleted: number
  ): void {
    const analysis = this.activeAnalyses.get(analysisId);
    if (analysis) {
      analysis.status = status;
      analysis.pagesTotal = pagesTotal;
      analysis.pagesCompleted = pagesCompleted;

      this.emit('analysisProgress', {
        analysisId,
        status,
        pagesTotal,
        pagesCompleted,
        progress: pagesTotal > 0 ? (pagesCompleted / pagesTotal) * 100 : 0,
      });
    }
  }

  private generateAnalysisId(): string {
    return `analysis_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  public getAnalysisMetrics(): {
    totalAnalyses: number;
    activeAnalyses: number;
    completedAnalyses: number;
    failedAnalyses: number;
    averageAnalysisTime: number;
    totalPagesAnalyzed: number;
  } {
    const analyses = Array.from(this.activeAnalyses.values());
    const totalAnalyses = analyses.length;
    const activeAnalyses = analyses.filter(
      a => a.status === 'analyzing' || a.status === 'pending'
    ).length;
    const completedAnalyses = analyses.filter(a => a.status === 'completed').length;
    const failedAnalyses = analyses.filter(a => a.status === 'failed').length;

    const completedAnalysesWithTime = analyses.filter(a => a.status === 'completed');
    const averageAnalysisTime =
      completedAnalysesWithTime.length > 0
        ? completedAnalysesWithTime.reduce(
            (sum, analysis) => sum + (Date.now() - analysis.startTime.getTime()),
            0
          ) / completedAnalysesWithTime.length
        : 0;

    const totalPagesAnalyzed = analyses.reduce((sum, analysis) => sum + analysis.pagesCompleted, 0);

    return {
      totalAnalyses,
      activeAnalyses,
      completedAnalyses,
      failedAnalyses,
      averageAnalysisTime,
      totalPagesAnalyzed,
    };
  }

  public async optimizeAnalysisSettings(): Promise<void> {
    // Analyze recent analysis performance and optimize settings
    const metrics = this.getAnalysisMetrics();
    const cachePerformance = this.analysisCache.getPerformance();

    // Optimization logic would go here
    this.emit('settingsOptimized', {
      metrics,
      cachePerformance,
    });
  }

  public async shutdown(): Promise<void> {
    // Cancel all active analyses
    for (const analysisId of this.activeAnalyses.keys()) {
      await this.cancelAnalysis(analysisId);
    }

    // Cleanup
    this.activeAnalyses.clear();
    this.removeAllListeners();
  }
}
