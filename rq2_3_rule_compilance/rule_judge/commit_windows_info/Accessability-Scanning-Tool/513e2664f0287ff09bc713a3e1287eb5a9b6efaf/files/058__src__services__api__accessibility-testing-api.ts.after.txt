import { EventEmitter } from 'events';
import { ServiceResult } from '../../core/types/common';
import { PerformanceMonitor } from '../../core/utils/performance-monitor';
import { TaskQueue } from '../orchestration/task-queue';
import { AnalysisService } from './analysis-service';
import { ReportingService } from './reporting-service';
import { CrawlingService } from './crawling-service';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';

export class AccessibilityTestingAPI extends EventEmitter {
  private static instance: AccessibilityTestingAPI;
  private crawlingService: CrawlingService;
  private analysisService: AnalysisService;
  private reportingService: ReportingService;
  private taskQueue: TaskQueue;
  private performanceMonitor: PerformanceMonitor;
  private errorHandler: ErrorHandlerService;
  private activeRequests: Map<
    string,
    {
      request: TestRequest;
      startTime: Date;
      status: 'pending' | 'processing' | 'completed' | 'failed';
      progress: number;
      results?: ServiceResult<any>;
      error?: string;
    }
  > = new Map();

  private constructor() {
    super();
    this.crawlingService = CrawlingService.getInstance();
    this.analysisService = AnalysisService.getInstance();
    this.reportingService = ReportingService.getInstance();
    this.taskQueue = TaskQueue.getInstance();
    this.performanceMonitor = PerformanceMonitor.getInstance();
    this.errorHandler = ErrorHandlerService.getInstance();

    this.setupEventListeners();
  }

  public static getInstance(): AccessibilityTestingAPI {
    if (!AccessibilityTestingAPI.instance) {
      AccessibilityTestingAPI.instance = new AccessibilityTestingAPI();
    }
    return AccessibilityTestingAPI.instance;
  }

  private setupEventListeners(): void {
    // Listen to task queue events
    this.taskQueue.on('taskCompleted', result => {
      this.handleTaskCompletion(result);
    });

    this.taskQueue.on('taskFailed', result => {
      this.handleTaskFailure(result);
    });

    this.taskQueue.on('taskStarted', task => {
      this.updateRequestProgress(task.id, 'processing', 10);
    });

    // Listen to service events
    this.crawlingService.on('crawlingProgress', progress => {
      this.handleCrawlingProgress(progress);
    });

    this.analysisService.on('analysisProgress', progress => {
      this.handleAnalysisProgress(progress);
    });

    this.reportingService.on('reportingProgress', progress => {
      this.handleReportingProgress(progress);
    });
  }

  public async testWebsite(request: TestRequest): Promise<TestResponse> {
    const requestId = this.generateRequestId();
    const startTime = new Date();

    try {
      // Validate request
      this.validateRequest(request);

      // Initialize request tracking
      this.activeRequests.set(requestId, {
        request,
        startTime,
        status: 'pending',
        progress: 0,
      });

      // Start processing asynchronously
      this.processRequest(requestId, request);

      // Return immediate response
      return {
        requestId,
        status: 'pending',
        progress: 0,
        metrics: {
          startTime,
          pagesProcessed: 0,
          totalPages: 0,
          memoryUsage: process.memoryUsage().heapUsed,
          cacheHits: 0,
          cacheMisses: 0,
        },
      };
    } catch (error) {
      this.activeRequests.set(requestId, {
        request,
        startTime,
        status: 'failed',
        progress: 0,
        error: (error as Error).message,
      });

      return {
        requestId,
        status: 'failed',
        progress: 0,
        error: (error as Error).message,
        metrics: {
          startTime,
          pagesProcessed: 0,
          totalPages: 0,
          memoryUsage: process.memoryUsage().heapUsed,
          cacheHits: 0,
          cacheMisses: 0,
        },
      };
    }
  }

  private async processRequest(requestId: string, request: TestRequest): Promise<void> {
    const timer = this.performanceMonitor.startTimer(`api_request_${requestId}`);

    try {
      let result: ServiceResult<any>;

      switch (request.type) {
        case 'quick':
          result = await this.processQuickTest(requestId, request);
          break;
        case 'comprehensive':
          result = await this.processComprehensiveTest(requestId, request);
          break;
        case 'single-page':
          result = await this.processSinglePageTest(requestId, request);
          break;
        default:
          throw new Error(`Unsupported test type: ${request.type}`);
      }

      // Update request with results
      const requestData = this.activeRequests.get(requestId)!;
      requestData.status = result.success ? 'completed' : 'failed';
      requestData.progress = 100;
      requestData.results = result;
      requestData.error = result.success ? undefined : result.error?.message;

      this.emit('requestCompleted', { requestId, result });
    } catch (error) {
      const requestData = this.activeRequests.get(requestId)!;
      requestData.status = 'failed';
      requestData.progress = 0;
      requestData.error = (error as Error).message;

      this.emit('requestFailed', { requestId, error });
      this.errorHandler.handleError(error as Error, 'AccessibilityTestingAPI.processRequest');
    } finally {
      timer.stop();
    }
  }

  private async processQuickTest(
    requestId: string,
    request: TestRequest
  ): Promise<ServiceResult<any>> {
    // Quick test: analyze a single page or small set of pages
    this.updateRequestProgress(requestId, 'processing', 20);

    const analysisResult = await this.analysisService.analyzePage(request.url, request.options);
    this.updateRequestProgress(requestId, 'processing', 80);

    const reportResult = await this.reportingService.generateQuickReport(analysisResult);
    this.updateRequestProgress(requestId, 'processing', 100);

    return {
      success: analysisResult.success && reportResult.success,
      data: {
        analysis: analysisResult,
        report: reportResult,
      },
      message: 'Quick test completed successfully',
    };
  }

  private async processComprehensiveTest(
    requestId: string,
    request: TestRequest
  ): Promise<ServiceResult<any>> {
    // Comprehensive test: crawl site and analyze all pages
    this.updateRequestProgress(requestId, 'processing', 10);

    const crawlResult = await this.crawlingService.crawlSite(request.url, request.options);
    this.updateRequestProgress(requestId, 'processing', 30);

    if (!crawlResult.success) {
      return crawlResult;
    }

    const analysisResult = await this.analysisService.analyzeSite(
      crawlResult.data,
      request.options
    );
    this.updateRequestProgress(requestId, 'processing', 70);

    const reportResult = await this.reportingService.generateComprehensiveReport(analysisResult);
    this.updateRequestProgress(requestId, 'processing', 100);

    return {
      success: analysisResult.success && reportResult.success,
      data: {
        crawl: crawlResult,
        analysis: analysisResult,
        report: reportResult,
      },
      message: 'Comprehensive test completed successfully',
    };
  }

  private async processSinglePageTest(
    requestId: string,
    request: TestRequest
  ): Promise<ServiceResult<any>> {
    // Single page test: detailed analysis of one page
    this.updateRequestProgress(requestId, 'processing', 30);

    const analysisResult = await this.analysisService.analyzePageDetailed(
      request.url,
      request.options
    );
    this.updateRequestProgress(requestId, 'processing', 80);

    const reportResult = await this.reportingService.generateDetailedReport(analysisResult);
    this.updateRequestProgress(requestId, 'processing', 100);

    return {
      success: analysisResult.success && reportResult.success,
      data: {
        analysis: analysisResult,
        report: reportResult,
      },
      message: 'Single page test completed successfully',
    };
  }

  public async getTestStatus(requestId: string): Promise<TestResponse> {
    const requestData = this.activeRequests.get(requestId);

    if (!requestData) {
      return {
        requestId,
        status: 'failed',
        progress: 0,
        error: 'Request not found',
        metrics: {
          startTime: new Date(),
          pagesProcessed: 0,
          totalPages: 0,
          memoryUsage: process.memoryUsage().heapUsed,
          cacheHits: 0,
          cacheMisses: 0,
        },
      };
    }

    const metrics: ProcessingMetrics = {
      startTime: requestData.startTime,
      endTime: requestData.status === 'completed' ? new Date() : undefined,
      duration:
        requestData.status === 'completed'
          ? new Date().getTime() - requestData.startTime.getTime()
          : undefined,
      pagesProcessed: 0, // Would be updated by progress handlers
      totalPages: 0, // Would be updated by progress handlers
      memoryUsage: process.memoryUsage().heapUsed,
      cacheHits: 0, // Would be updated from cache service
      cacheMisses: 0, // Would be updated from cache service
    };

    return {
      requestId,
      status: requestData.status,
      progress: requestData.progress,
      results: requestData.results,
      error: requestData.error,
      metrics,
      estimatedCompletion: this.calculateEstimatedCompletion(requestData),
    };
  }

  public async cancelTest(requestId: string): Promise<ServiceResult<void>> {
    const requestData = this.activeRequests.get(requestId);

    if (!requestData) {
      return {
        success: false,
        message: 'Request not found',
      };
    }

    if (requestData.status === 'completed' || requestData.status === 'failed') {
      return {
        success: false,
        message: 'Cannot cancel completed request',
      };
    }

    // Cancel the request
    requestData.status = 'failed';
    requestData.error = 'Request cancelled by user';

    this.emit('requestCancelled', { requestId });

    return {
      success: true,
      message: 'Request cancelled successfully',
    };
  }

  public getActiveRequests(): Array<{
    requestId: string;
    url: string;
    type: string;
    status: string;
    progress: number;
    startTime: Date;
  }> {
    return Array.from(this.activeRequests.entries()).map(([requestId, data]) => ({
      requestId,
      url: data.request.url,
      type: data.request.type,
      status: data.status,
      progress: data.progress,
      startTime: data.startTime,
    }));
  }

  public getSystemStatus(): {
    totalRequests: number;
    activeRequests: number;
    completedRequests: number;
    failedRequests: number;
    systemHealth: 'healthy' | 'warning' | 'critical';
    performance: any;
  } {
    const totalRequests = this.activeRequests.size;
    const activeRequests = Array.from(this.activeRequests.values()).filter(
      r => r.status === 'processing' || r.status === 'pending'
    ).length;
    const completedRequests = Array.from(this.activeRequests.values()).filter(
      r => r.status === 'completed'
    ).length;
    const failedRequests = Array.from(this.activeRequests.values()).filter(
      r => r.status === 'failed'
    ).length;

    const performanceSummary = this.performanceMonitor.getSummary();

    return {
      totalRequests,
      activeRequests,
      completedRequests,
      failedRequests,
      systemHealth: performanceSummary.systemHealth,
      performance: performanceSummary,
    };
  }

  private validateRequest(request: TestRequest): void {
    if (!request.url || typeof request.url !== 'string') {
      throw new Error('Invalid URL provided');
    }

    if (!request.type || !['quick', 'comprehensive', 'single-page'].includes(request.type)) {
      throw new Error('Invalid test type');
    }

    if (!request.priority || !['low', 'medium', 'high'].includes(request.priority)) {
      throw new Error('Invalid priority level');
    }

    // Validate URL format
    try {
      new URL(request.url);
    } catch {
      throw new Error('Invalid URL format');
    }
  }

  private generateRequestId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  private updateRequestProgress(
    requestId: string,
    status: 'pending' | 'processing' | 'completed' | 'failed',
    progress: number
  ): void {
    const requestData = this.activeRequests.get(requestId);
    if (requestData) {
      requestData.status = status;
      requestData.progress = progress;

      this.emit('requestProgress', { requestId, status, progress });
    }
  }

  private calculateEstimatedCompletion(requestData: {
    request: TestRequest;
    startTime: Date;
    progress: number;
  }): Date | undefined {
    if (requestData.progress === 0) return undefined;

    const elapsed = Date.now() - requestData.startTime.getTime();
    const estimatedTotal = elapsed / (requestData.progress / 100);
    const remaining = estimatedTotal - elapsed;

    return new Date(Date.now() + remaining);
  }

  private handleTaskCompletion(result: any): void {
    // Update request progress based on task completion
    this.emit('taskCompleted', result);
  }

  private handleTaskFailure(result: any): void {
    // Handle task failure
    this.emit('taskFailed', result);
  }

  private handleCrawlingProgress(progress: any): void {
    // Update progress for crawling phase
    this.emit('crawlingProgress', progress);
  }

  private handleAnalysisProgress(progress: any): void {
    // Update progress for analysis phase
    this.emit('analysisProgress', progress);
  }

  private handleReportingProgress(progress: any): void {
    // Update progress for reporting phase
    this.emit('reportingProgress', progress);
  }

  public cleanupOldRequests(olderThanHours: number = 24): void {
    const cutoffTime = Date.now() - olderThanHours * 60 * 60 * 1000;

    for (const [requestId, requestData] of this.activeRequests.entries()) {
      if (requestData.startTime.getTime() < cutoffTime) {
        this.activeRequests.delete(requestId);
      }
    }
  }

  public async shutdown(): Promise<void> {
    // Cancel all active requests
    for (const [requestId, requestData] of this.activeRequests.entries()) {
      if (requestData.status === 'processing' || requestData.status === 'pending') {
        await this.cancelTest(requestId);
      }
    }

    // Shutdown services
    await this.crawlingService.shutdown();
    await this.analysisService.shutdown();
    await this.reportingService.shutdown();

    this.removeAllListeners();
  }
}
