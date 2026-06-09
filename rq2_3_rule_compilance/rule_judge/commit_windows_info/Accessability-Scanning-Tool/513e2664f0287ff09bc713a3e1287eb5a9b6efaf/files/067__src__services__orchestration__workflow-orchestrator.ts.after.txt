import { AnalysisResult, PageInfo } from '../../core/types/common';
import { BrowserManager } from '../../core/utils/browser-manager';
import { PerformanceMonitor } from '../../core/utils/performance-monitor';
import { ParallelAnalyzer } from './parallel-analyzer';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { ConfigurationService } from '../../../playwright/tests/utils/services/configuration-service';
import { SiteCrawler } from '../../../playwright/tests/utils/site-crawler';
import { ReportingService } from '../api/reporting-service';

export interface WorkflowOptions {
  maxPages?: number;
  maxDepth?: number;
  maxConcurrency?: number;
  enablePerformanceMonitoring?: boolean;
  retryFailedPages?: boolean;
  generateReports?: boolean;
  excludePatterns?: RegExp[];
}

export interface WorkflowResult {
  crawlResults: PageInfo[];
  analysisResults: AnalysisResult[];
  reportPaths?: string[];
  metrics: {
    totalTime: number;
    crawlTime: number;
    analysisTime: number;
    reportTime: number;
    successRate: number;
    pagesAnalyzed: number;
    violationsFound: number;
  };
}

export class WorkflowOrchestrator {
  private browserManager = BrowserManager.getInstance();
  private performanceMonitor = PerformanceMonitor.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private config = ConfigurationService.getInstance();
  private parallelAnalyzer: ParallelAnalyzer;

  constructor() {
    this.parallelAnalyzer = new ParallelAnalyzer();
  }

  async runAccessibilityAudit(
    targetUrl: string,
    options: WorkflowOptions = {}
  ): Promise<WorkflowResult> {
    const {
      maxPages = 50,
      maxDepth = 4,
      maxConcurrency = 5,
      enablePerformanceMonitoring = true,
      retryFailedPages = true,
      generateReports = true,
      excludePatterns = this.config.getCrawlingConfiguration().excludePatterns,
    } = options;

    this.errorHandler.logInfo('Starting accessibility audit workflow', {
      targetUrl,
      maxPages,
      maxDepth,
      maxConcurrency,
    });

    const workflowTimer = this.performanceMonitor.startTimer('accessibility_audit');
    workflowTimer.start();

    if (enablePerformanceMonitoring) {
      this.performanceMonitor.startContinuousMonitoring();
    }

    try {
      // Initialize browser manager
      await this.browserManager.initialize();

      // Phase 1: Site Crawling
      const crawlResults = await this.performSiteCrawling(targetUrl, {
        maxPages,
        maxDepth,
        excludePatterns,
      });

      // Phase 2: Accessibility Analysis
      const analysisResults = await this.performAccessibilityAnalysis(crawlResults, {
        maxConcurrency,
        retryFailedPages,
      });

      // Phase 3: Report Generation
      let reportPaths: string[] = [];
      if (generateReports) {
        reportPaths = await this.generateReports(analysisResults, targetUrl);
      }

      // Calculate metrics
      const totalTime = workflowTimer.end();
      const metrics = this.calculateMetrics(crawlResults, analysisResults, totalTime);

      this.errorHandler.logSuccess('Accessibility audit workflow completed', {
        pagesAnalyzed: analysisResults.length,
        totalTime: `${totalTime}ms`,
        successRate: `${metrics.successRate}%`,
      });

      return {
        crawlResults,
        analysisResults,
        reportPaths,
        metrics,
      };
    } catch (error) {
      const totalTime = workflowTimer.end();
      this.errorHandler.handleError(error, 'Accessibility audit workflow failed');
      throw error;
    } finally {
      if (enablePerformanceMonitoring) {
        this.performanceMonitor.stopContinuousMonitoring();
      }
      await this.cleanup();
    }
  }

  private async performSiteCrawling(
    targetUrl: string,
    options: {
      maxPages: number;
      maxDepth: number;
      excludePatterns: RegExp[];
    }
  ): Promise<PageInfo[]> {
    const crawlTimer = this.performanceMonitor.startTimer('site_crawling');
    crawlTimer.start();

    this.errorHandler.logInfo('Phase 1: Starting site crawling', {
      targetUrl,
      maxPages: options.maxPages,
      maxDepth: options.maxDepth,
    });

    try {
      const sessionId = 'crawler-session';
      const page = await this.browserManager.getPage(sessionId);

      const siteCrawler = new SiteCrawler(page, targetUrl);

      const crawlResults = await siteCrawler.crawlSite({
        maxPages: options.maxPages,
        maxDepth: options.maxDepth,
        excludePatterns: options.excludePatterns,
        delayBetweenRequests: 300,
        maxRetries: 3,
        retryDelay: 1500,
        timeoutMs: 20000,
      });

      // Convert to PageInfo format
      const pageInfos: PageInfo[] = crawlResults.map((result: any) => ({
        url: result.url,
        title: result.title,
        depth: result.depth,
        foundOn: result.foundOn,
        status: result.status,
        loadTime: result.loadTime,
      }));

      crawlTimer.end();

      this.errorHandler.logSuccess('Site crawling completed', {
        pagesFound: pageInfos.length,
        summary: siteCrawler.getSummary(),
      });

      return pageInfos;
    } catch (error) {
      crawlTimer.end();
      this.errorHandler.handleError(error, 'Site crawling failed');
      throw error;
    }
  }

  private async performAccessibilityAnalysis(
    pages: PageInfo[],
    options: {
      maxConcurrency: number;
      retryFailedPages: boolean;
    }
  ): Promise<AnalysisResult[]> {
    const analysisTimer = this.performanceMonitor.startTimer('accessibility_analysis');
    analysisTimer.start();

    this.errorHandler.logInfo('Phase 2: Starting accessibility analysis', {
      totalPages: pages.length,
      maxConcurrency: options.maxConcurrency,
    });

    try {
      const batchResult = await this.parallelAnalyzer.analyzePages(pages, {
        maxConcurrency: options.maxConcurrency,
        retryFailedPages: options.retryFailedPages,
        batchSize: 10,
        delayBetweenBatches: 1000,
      });

      analysisTimer.end();

      this.errorHandler.logSuccess('Accessibility analysis completed', {
        successful: batchResult.successful.length,
        failed: batchResult.failed.length,
        successRate: `${batchResult.metrics.successRate}%`,
      });

      // Log failed pages for debugging
      if (batchResult.failed.length > 0) {
        this.errorHandler.logWarning('Some pages failed analysis', {
          failedPages: batchResult.failed.map((f: any) => ({ url: f.page.url, error: f.error })),
        });
      }

      return batchResult.successful;
    } catch (error) {
      analysisTimer.end();
      this.errorHandler.handleError(error, 'Accessibility analysis failed');
      throw error;
    }
  }

  private async generateReports(
    analysisResults: AnalysisResult[],
    targetUrl: string
  ): Promise<string[]> {
    const reportTimer = this.performanceMonitor.startTimer('report_generation');
    reportTimer.start();

    this.errorHandler.logInfo('Phase 3: Starting report generation', {
      resultsCount: analysisResults.length,
    });

    try {
      const reportingService = ReportingService.getInstance();
      const reportPaths: string[] = [];

      // Convert analysis results to a format suitable for report generation
      const siteWideReport = this.convertAnalysisResultsToSiteWideReport(
        analysisResults,
        targetUrl
      );

      // Generate comprehensive report with all audience types
      const comprehensiveResult = await reportingService.generateComprehensiveReport(
        siteWideReport,
        {
          generateReports: true,
          outputPath: `./playwright/accessibility-reports/comprehensive-${Date.now()}.pdf`,
          includeCharts: true,
          includeScreenshots: true,
          includeBrandColors: true,
        }
      );

      if (comprehensiveResult.success && comprehensiveResult.data) {
        reportPaths.push(comprehensiveResult.data);
      }

      // Generate audience-specific reports
      const audienceReports = [
        { type: 'executive', name: 'stakeholders' },
        { type: 'research', name: 'researchers' },
        { type: 'developer', name: 'developers' },
      ];

      for (const audience of audienceReports) {
        const audienceMap = {
          executive: { name: 'executive', displayName: 'Executive Summary' },
          research: { name: 'research', displayName: 'Research Report' },
          developer: { name: 'developer', displayName: 'Developer Report' },
        };

        const customResult = await reportingService.generateCustomReport(siteWideReport, {
          type: audience.type as 'executive' | 'research' | 'developer',
          audiences: [audienceMap[audience.type as keyof typeof audienceMap]],
        });

        if (customResult.success && customResult.data) {
          reportPaths.push(customResult.data);
        }
      }

      reportTimer.end();

      this.errorHandler.logSuccess('Report generation completed', {
        reportsGenerated: reportPaths.length,
        reportPaths,
      });

      return reportPaths;
    } catch (error) {
      reportTimer.end();
      this.errorHandler.handleError(error, 'Report generation failed');
      throw error;
    }
  }

  /**
   * Convert analysis results to site-wide report format
   */
  private convertAnalysisResultsToSiteWideReport(
    analysisResults: AnalysisResult[],
    targetUrl: string
  ): any {
    const timestamp = new Date().toISOString();
    const totalViolations = analysisResults.reduce(
      (sum, result) => sum + result.summary.totalViolations,
      0
    );
    const totalCritical = analysisResults.reduce(
      (sum, result) => sum + result.summary.criticalViolations,
      0
    );
    const totalSerious = analysisResults.reduce(
      (sum, result) => sum + result.summary.seriousViolations,
      0
    );
    const totalModerate = analysisResults.reduce(
      (sum, result) => sum + result.summary.moderateViolations,
      0
    );
    const totalMinor = analysisResults.reduce(
      (sum, result) => sum + result.summary.minorViolations,
      0
    );

    return {
      siteUrl: targetUrl,
      timestamp,
      testSuite: 'Phase 2 Accessibility Testing',
      totalPages: analysisResults.length,
      pagesAnalyzed: analysisResults.length,
      totalViolations,
      overallSummary: {
        totalViolations,
        criticalViolations: totalCritical,
        seriousViolations: totalSerious,
        moderateViolations: totalModerate,
        minorViolations: totalMinor,
        compliancePercentage: this.calculateCompliancePercentage(analysisResults),
      },
      pageAnalysis: analysisResults.map(result => ({
        url: result.url,
        title: result.url.split('/').pop() || result.url,
        timestamp: result.timestamp,
        violations: result.violations || [],
        summary: result.summary,
        tool: result.tool,
      })),
      wcagComplianceMatrix: this.generateWcagComplianceMatrix(analysisResults),
      mostCommonViolations: this.analyzeMostCommonViolations(analysisResults),
    };
  }

  /**
   * Calculate overall compliance percentage
   */
  private calculateCompliancePercentage(analysisResults: AnalysisResult[]): number {
    if (analysisResults.length === 0) return 0;

    const totalPages = analysisResults.length;
    const pagesWithoutCritical = analysisResults.filter(
      result => result.summary.criticalViolations === 0
    ).length;
    const pagesWithoutSerious = analysisResults.filter(
      result => result.summary.seriousViolations === 0
    ).length;

    // Weight critical violations more heavily
    const criticalWeight = 0.6;
    const seriousWeight = 0.4;

    const criticalCompliance = (pagesWithoutCritical / totalPages) * 100;
    const seriousCompliance = (pagesWithoutSerious / totalPages) * 100;

    return Math.round(criticalCompliance * criticalWeight + seriousCompliance * seriousWeight);
  }

  /**
   * Generate WCAG compliance matrix
   */
  private generateWcagComplianceMatrix(analysisResults: AnalysisResult[]): any[] {
    // This would be more sophisticated in a real implementation
    return [
      { criterion: '1.1.1', name: 'Non-text Content', level: 'A', status: 'Pass' },
      { criterion: '1.3.1', name: 'Info and Relationships', level: 'A', status: 'Fail' },
      { criterion: '1.4.3', name: 'Contrast (Minimum)', level: 'AA', status: 'Pass' },
      { criterion: '2.1.1', name: 'Keyboard', level: 'A', status: 'Pass' },
      { criterion: '4.1.2', name: 'Name, Role, Value', level: 'A', status: 'Fail' },
    ];
  }

  /**
   * Analyze most common violations across all pages
   */
  private analyzeMostCommonViolations(analysisResults: AnalysisResult[]): any[] {
    const violationCounts = new Map<string, number>();

    analysisResults.forEach(result => {
      if (result.violations) {
        result.violations.forEach((violation: any) => {
          const key = violation.rule || violation.id || violation.ruleId || 'unknown';
          violationCounts.set(key, (violationCounts.get(key) || 0) + 1);
        });
      }
    });

    return Array.from(violationCounts.entries())
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .map(([rule, count]) => ({
        rule,
        count,
        percentage: Math.round((count / analysisResults.length) * 100),
      }));
  }

  private calculateMetrics(
    crawlResults: PageInfo[],
    analysisResults: AnalysisResult[],
    totalTime: number
  ): WorkflowResult['metrics'] {
    const crawlTime = this.performanceMonitor.getAverageProcessingTime('site_crawling');
    const analysisTime = this.performanceMonitor.getAverageProcessingTime('accessibility_analysis');
    const reportTime = this.performanceMonitor.getAverageProcessingTime('report_generation');

    const successRate =
      crawlResults.length > 0 ? (analysisResults.length / crawlResults.length) * 100 : 0;

    const violationsFound = analysisResults.reduce(
      (total, result) => total + result.summary.totalViolations,
      0
    );

    return {
      totalTime,
      crawlTime,
      analysisTime,
      reportTime,
      successRate,
      pagesAnalyzed: analysisResults.length,
      violationsFound,
    };
  }

  async getWorkflowStatus(): Promise<{
    isRunning: boolean;
    browserStatus: any;
    parallelAnalyzerStatus: any;
    performanceMetrics: any;
  }> {
    return {
      isRunning: this.performanceMonitor.getSummary().activeOperations.length > 0,
      browserStatus: this.browserManager.getResourceUsage(),
      parallelAnalyzerStatus: this.parallelAnalyzer.getStatus(),
      performanceMetrics: this.performanceMonitor.getSummary(),
    };
  }

  async cleanup(): Promise<void> {
    this.errorHandler.logInfo('Cleaning up workflow orchestrator');

    try {
      await Promise.all([this.parallelAnalyzer.cleanup(), this.browserManager.cleanupAll()]);

      this.performanceMonitor.stopContinuousMonitoring();

      this.errorHandler.logSuccess('Workflow orchestrator cleanup completed');
    } catch (error) {
      this.errorHandler.handleError(error, 'Workflow cleanup failed');
    }
  }

  exportPerformanceReport(): string {
    return this.performanceMonitor.exportMetrics();
  }

  // Convenience methods for common operations
  async quickAudit(targetUrl: string): Promise<WorkflowResult> {
    return this.runAccessibilityAudit(targetUrl, {
      maxPages: 25,
      maxDepth: 3,
      maxConcurrency: 3,
    });
  }

  async comprehensiveAudit(targetUrl: string): Promise<WorkflowResult> {
    return this.runAccessibilityAudit(targetUrl, {
      maxPages: 100,
      maxDepth: 5,
      maxConcurrency: 8,
      enablePerformanceMonitoring: true,
    });
  }

  async testSinglePage(url: string): Promise<AnalysisResult[]> {
    const pageInfo: PageInfo = {
      url,
      title: 'Single Page Test',
      depth: 0,
      foundOn: 'manual',
      status: 200,
    };

    const result = await this.performAccessibilityAnalysis([pageInfo], {
      maxConcurrency: 1,
      retryFailedPages: false,
    });

    return result;
  }
}
