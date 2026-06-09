import { PageInfo, AnalysisResult, ServiceResult } from '../../core/types/common';
import { BrowserManager } from '../../core/utils/browser-manager';

import { ParallelAnalyzer } from './parallel-analyzer';
import { ErrorHandlerService } from '../services/error-handler-service';
import { ConfigurationService } from '../services/configuration-service';
import { FileOperationsService } from '../services/file-operations-service';
import { SiteCrawler, CrawlResult } from '../crawler/site-crawler';
import * as fs from 'fs';
import { AccessibilityTool } from '../analysis/accessibility-tool';
import { ToolOrchestrator } from '../analysis/tool-orchestrator';
import { ViolationProcessor } from '../processors/violation-processor';
import { PdfOrchestrator } from '../reporting/pdf-generators/pdf-orchestrator';
import { AnalysisCache } from './analysis-cache';
import { TaskQueue } from './task-queue';
import { SmartBatcher } from './smart-batcher';
import { AnalysisWorker } from './analysis-worker';

export interface WorkflowOptions {
  maxPages?: number;
  maxDepth?: number;
  maxConcurrency?: number;
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
  public browserManager = BrowserManager.getInstance();
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

    // Automatic cleanup before starting audit
    if (generateReports) {
      this.errorHandler.logInfo('Cleaning up old reports before starting audit');
      await this.cleanupReportsDirectory();
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
      const metrics = this.calculateMetrics(crawlResults, analysisResults, 0);

      this.errorHandler.logSuccess('Accessibility audit workflow completed', {
        pagesAnalyzed: analysisResults.length,
        successRate: `${metrics.successRate}%`,
        reportsGenerated: reportPaths.length,
      });

      return {
        crawlResults,
        analysisResults,
        reportPaths,
        metrics,
      };
    } catch (error) {
      this.errorHandler.handleError(error, 'Accessibility audit workflow failed');
      throw error;
    } finally {
      await this.cleanup();
    }
  }

  public async performSiteCrawling(
    targetUrl: string,
    options: {
      maxPages: number;
      maxDepth: number;
      excludePatterns: RegExp[];
    }
  ): Promise<PageInfo[]> {
    this.errorHandler.logInfo('Phase 1: Starting site crawling', {
      targetUrl,
      maxPages: options.maxPages,
      maxDepth: options.maxDepth,
    });

    try {
      const sessionId = 'crawler-session';
      const page = await this.browserManager.getPage(sessionId);

      const siteCrawler = new SiteCrawler(page, targetUrl);

      this.errorHandler.logInfo(`Starting crawl for: ${targetUrl}`);
      const crawlResults = await siteCrawler.crawlSite({
        maxPages: options.maxPages,
        maxDepth: options.maxDepth,
        excludePatterns: options.excludePatterns,
        delayBetweenRequests: 300,
        maxRetries: 3,
        retryDelay: 1500,
        timeoutMs: 20000,
      });
      this.errorHandler.logInfo(
        `Crawl complete for: ${targetUrl}, pages found: ${crawlResults.length}`
      );

      // Convert to PageInfo format
      const pageInfos: PageInfo[] = crawlResults.map((result: CrawlResult) => ({
        url: result.url,
        title: result.title,
        depth: result.depth,
        foundOn: result.foundOn,
        status: result.status,
        loadTime: typeof result.loadTime === 'number' ? result.loadTime : 0,
      }));

      this.errorHandler.logSuccess('Site crawling completed', {
        pagesFound: pageInfos.length,
        summary: siteCrawler.getSummary(),
      });

      return pageInfos;
    } catch (error) {
      this.errorHandler.logWarning(
        `Site crawling failed: ${error instanceof Error ? error.message : error}`
      );
      this.errorHandler.handleError(error, 'Site crawling failed');
      throw error;
    }
  }

  public async performAccessibilityAnalysis(
    pages: PageInfo[],
    options: Record<string, unknown>
  ): Promise<AnalysisResult[]> {
    this.errorHandler.logInfo('Phase 2: Starting accessibility analysis', {
      totalPages: pages.length,
      maxConcurrency: options['maxConcurrency'] as number,
    });

    try {
      const analysisResults: AnalysisResult[] = [];

      // Process pages in batches
      for (let i = 0; i < pages.length; i += (options['batchSize'] as number) || 10) {
        const batch = pages.slice(i, i + (options['batchSize'] as number) || 10);
        this.errorHandler.logInfo(
          `Starting analysis batch: ${i / ((options['batchSize'] as number) || 10) + 1}, batch size: ${batch.length}`
        );
        const batchResult = await this.parallelAnalyzer.analyzePages(batch, {
          maxConcurrency: options['maxConcurrency'] as number,
          retryFailedPages: options['retryFailedPages'] as boolean,
          batchSize: options['batchSize'] as number,
          delayBetweenBatches: options['delayBetweenBatches'] as number,
        });
        this.errorHandler.logInfo(
          `Batch analysis complete: ${i / ((options['batchSize'] as number) || 10) + 1}, successful: ${batchResult.successful.length}, failed: ${batchResult.failed.length}`
        );

        analysisResults.push(...batchResult.successful);
        if (options['retryFailedPages'] as boolean) {
          const failedPages = batchResult.failed.map(f => f.page);
          if (failedPages.length > 0) {
            this.errorHandler.logWarning('Retrying failed pages from previous batch', {
              failedPages: failedPages.map(p => p.url),
            });
            const retryResult = await this.parallelAnalyzer.analyzePages(failedPages, {
              maxConcurrency: options['maxConcurrency'] as number,
              retryFailedPages: false, // Only retry failed ones
              batchSize: options['batchSize'] as number,
              delayBetweenBatches: options['delayBetweenBatches'] as number,
            });
            this.errorHandler.logInfo(
              `Retry batch complete: successful: ${retryResult.successful.length}, failed: ${retryResult.failed.length}`
            );
            analysisResults.push(...retryResult.successful);
          }
        }
      }

      this.errorHandler.logSuccess('Accessibility analysis completed', {
        successful: analysisResults.length,
        failed: pages.length - analysisResults.length,
        successRate: `${((analysisResults.length / pages.length) * 100).toFixed(1)}%`,
      });

      return analysisResults;
    } catch (error) {
      this.errorHandler.logWarning(
        `Accessibility analysis failed: ${error instanceof Error ? error.message : error}`
      );
      this.errorHandler.handleError(error, 'Accessibility analysis failed');
      throw error;
    }
  }

  public async generateReports(
    analysisResults: AnalysisResult[],
    targetUrl: string
  ): Promise<string[]> {
    this.errorHandler.logInfo('Phase 3: Starting report generation', {
      analysisResults: analysisResults.length,
      targetUrl,
    });

    const reportPaths: string[] = [];
    try {
      const siteWideReport = this.convertAnalysisResultsToSiteWideReport(
        analysisResults,
        targetUrl,
        'WCAG2AA'
      );
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const baseFilename = `accessibility-audit-${timestamp}`;

      // Ensure accessibility-reports directory exists
      const reportsDir = './accessibility-reports';
      if (!fs.existsSync(reportsDir)) {
        fs.mkdirSync(reportsDir, { recursive: true });
        this.errorHandler.logInfo(`Created accessibility-reports directory: ${reportsDir}`);
      }

      // 1. Generate JSON Report (Raw Data)
      const jsonReportPath = `${reportsDir}/${baseFilename}-results.json`;
      try {
        fs.writeFileSync(jsonReportPath, JSON.stringify(siteWideReport, null, 2));
        reportPaths.push(jsonReportPath);
        this.errorHandler.logSuccess(`JSON report saved: ${jsonReportPath}`);
      } catch (error) {
        this.errorHandler.logWarning('Failed to save JSON report', { error });
      }

      // 2. Generate PDF Reports for Different Audiences
      try {
        // Ensure browser is healthy before PDF generation
        const isHealthy = await this.browserManager.isBrowserHealthy();
        if (!isHealthy) {
          this.errorHandler.logInfo('Browser not healthy, force reinitializing for PDF generation...');
          await this.browserManager.forceReinitialize();
        }

        // Dynamically import the PDFOrchestrator
        const pdfGenerator = new PdfOrchestrator(await this.browserManager.getPage('pdf-generation'));

        // Generate all 3 audience-specific PDF reports
        const pdfResults = await pdfGenerator.generatePdfReports(siteWideReport, {
          filename: baseFilename,
          audiences: [
            { name: 'stakeholders', displayName: 'Product Owners & Stakeholders' },
            { name: 'researchers', displayName: 'User Researchers & UCD' },
            { name: 'developers', displayName: 'Developers & Testers' },
          ],
        });

        if (pdfResults.success && pdfResults.data) {
          pdfResults.data.forEach((pdfResult: any) => {
            reportPaths.push(pdfResult.filePath);
            this.errorHandler.logSuccess(
              `${pdfResult.displayName} PDF generated: ${pdfResult.filePath} (${pdfResult.sizeKB}KB)`
            );
          });
        }

        this.errorHandler.logSuccess('PDF reports generated successfully');
      } catch (error) {
        this.errorHandler.logWarning('Failed to generate PDF reports', { error });
      }

      // Log report summary
      this.logReportSummary(reportPaths);

      return reportPaths;
    } catch (error) {
      this.errorHandler.handleError(error, 'Report generation failed');
      throw error;
    }
  }

  /**
   * Convert analysis results to site-wide report format
   */
  // Private method removed - now using public convertAnalysisResultsToSiteWideReport method

  // Make convertAnalysisResultsToSiteWideReport public for web server access
  public convertAnalysisResultsToSiteWideReport(
    analysisResults: AnalysisResult[],
    targetUrl: string,
    wcagLevel: string = 'WCAG2AA'
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

    // Calculate detailed metrics needed for audience-specific content
    const pagesWithViolations = analysisResults.filter(
      result => result.summary.totalViolations > 0
    ).length;
    const compliancePercentage =
      analysisResults.length > 0
        ? Math.round(
          ((analysisResults.length - pagesWithViolations) / analysisResults.length) * 100
        )
        : 0;

    // Process violations by type for detailed analysis
    const violationsByType: Record<string, any> = {};
    const violationCounts: Record<
      string,
      { count: number; pages: Set<string>; impact: string; description: string }
    > = {};

    analysisResults.forEach(result => {
      result.violations?.forEach((violation: any) => {
        const violationId = violation.id || violation.code || 'unknown';

        if (!violationCounts[violationId]) {
          violationCounts[violationId] = {
            count: 0,
            pages: new Set(),
            impact: violation.impact || violation.type || 'moderate',
            description:
              violation.description || violation.message || `Accessibility issue: ${violationId}`,
          };
        }

        violationCounts[violationId].count++;
        violationCounts[violationId].pages.add(result.url);

        if (!violationsByType[violationId]) {
          violationsByType[violationId] = {
            id: violationId,
            description: violationCounts[violationId].description,
            impact: violationCounts[violationId].impact,
            pages: [],
          };
        }
        violationsByType[violationId].pages.push(result.url);
      });
    });

    // Generate most common violations list
    const mostCommonViolations = Object.entries(violationCounts)
      .map(([id, data]) => ({
        id,
        description: data.description,
        impact: data.impact,
        affectedPages: data.pages.size,
        totalOccurrences: data.count,
      }))
      .sort((a, b) => b.totalOccurrences - a.totalOccurrences)
      .slice(0, 10);

    return {
      siteUrl: targetUrl,
      timestamp,
      wcagLevel,
      summary: {
        totalPages: analysisResults.length,
        totalViolations,
        criticalViolations: totalCritical,
        seriousViolations: totalSerious,
        moderateViolations: totalModerate,
        minorViolations: totalMinor,
        pagesWithViolations,
        compliancePercentage,
        wcagAAViolations: totalCritical + totalSerious,
        wcagAAAViolations: totalModerate + totalMinor,
      },
      pageAnalysis: analysisResults.map(result => ({
        url: result.url,
        title: result.url.split('/').pop() || result.url,
        timestamp: result.timestamp,
        testSuite: result.tool || 'Accessibility Testing',
        summary: {
          ...result.summary,
          wcagAAViolations: result.summary.criticalViolations + result.summary.seriousViolations,
          wcagAAAViolations: result.summary.moderateViolations + result.summary.minorViolations,
        },
        violations: result.violations || [],
        pageAnalysis: {
          title: result.url.split('/').pop() || result.url,
          headingStructure: [],
          landmarks: { main: false, nav: false, footer: false },
          skipLink: { exists: false, isVisible: false, targetExists: false },
          images: [],
          links: [],
          forms: [],
          keyboardNavigation: [],
        },
      })),
      violationsByType,
      mostCommonViolations,
      wcagComplianceMatrix: this.generateWcagComplianceMatrix(analysisResults),
    };
  }

  /**
   * Generate WCAG compliance matrix
   */
  private generateWcagComplianceMatrix(analysisResults: AnalysisResult[]): any {
    const wcagCriteria: Record<string, Record<string, { violations: number; pages: Set<string>; status: string }>> = {
      'text-alternatives': {
        '1.1': { violations: 0, pages: new Set(), status: 'pass' },
        '1.2': { violations: 0, pages: new Set(), status: 'pass' },
      },
      'time-based-media': {
        '1.3': { violations: 0, pages: new Set(), status: 'pass' },
        '1.4': { violations: 0, pages: new Set(), status: 'pass' },
      },
      'adaptable': {
        '1.3': { violations: 0, pages: new Set(), status: 'pass' },
        '1.4': { violations: 0, pages: new Set(), status: 'pass' },
      },
      'distinguishable': {
        '1.4': { violations: 0, pages: new Set(), status: 'pass' },
      },
    };

    // Analyze violations against WCAG criteria
    analysisResults.forEach(result => {
      if (result.violations) {
        result.violations.forEach((violation: any) => {
          const wcagTags = violation.wcagTags || [];
          wcagTags.forEach((tag: string) => {
            const [principle, guideline] = tag.split('.');
            if (principle && guideline && wcagCriteria[principle] && wcagCriteria[principle][guideline]) {
              wcagCriteria[principle][guideline].violations++;
              wcagCriteria[principle][guideline].pages.add(result.url);
              wcagCriteria[principle][guideline].status = 'fail';
            }
          });
        });
      }
    });

    // Convert Sets to arrays for JSON serialization
    Object.keys(wcagCriteria).forEach(principle => {
      const principleData = wcagCriteria[principle];
      if (principleData) {
        Object.keys(principleData).forEach(guideline => {
          const criteria = principleData[guideline];
          if (criteria) {
            (criteria as any).pages = Array.from(criteria.pages);
          }
        });
      }
    });

    return wcagCriteria;
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
    const crawlTime = 0; // No performance monitoring, so no average time
    const analysisTime = 0; // No performance monitoring, so no average time
    const reportTime = 0; // No performance monitoring, so no average time

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
    const isRunning = false; // No performance monitoring, so no active operations
    const browserStatus = this.browserManager.getResourceUsage();
    const parallelAnalyzerStatus = this.parallelAnalyzer.getStatus();
    const performanceMetrics = {}; // No performance monitoring, so no report

    return { isRunning, browserStatus, parallelAnalyzerStatus, performanceMetrics };
  }

  getBrowserManager() {
    return this.browserManager;
  }

  async cleanup(): Promise<void> {
    this.errorHandler.logInfo('Cleaning up workflow orchestrator');
    // Only cleanup specific sessions, don't close the entire browser
    // This allows the browser to remain open for subsequent operations
    await this.browserManager.cleanup('crawler-session');
    await this.browserManager.cleanup('pdf-generation');
    this.errorHandler.logSuccess('Workflow orchestrator cleanup completed');
  }

  exportPerformanceReport(): string {
    return ''; // No performance monitoring, so no metrics to export
  }

  // Convenience methods for common operations
  async quickAudit(targetUrl: string): Promise<WorkflowResult> {
    return this.runAccessibilityAudit(targetUrl, {
      maxPages: 25,
      maxDepth: 3,
      maxConcurrency: 4,
      generateReports: true,
    });
  }

  async comprehensiveAudit(targetUrl: string): Promise<WorkflowResult> {
    return this.runAccessibilityAudit(targetUrl, {
      maxPages: 100,
      maxDepth: 5,
      maxConcurrency: 8,
      generateReports: true,
    });
  }

  async testSinglePage(url: string): Promise<AnalysisResult[]> {
    this.errorHandler.logInfo('Starting single page test', { url });

    try {
      // Initialize browser manager if not already initialized
      await this.browserManager.initialize();
      this.errorHandler.logInfo('Browser manager initialized for single page test');

      const pageInfo: PageInfo = {
        url,
        title: 'Single Page Test',
        depth: 0,
        foundOn: 'manual',
        status: 200,
        loadTime: 0, // Default loadTime for single page test
      };

      this.errorHandler.logInfo('Starting accessibility analysis for single page');
      const result = await this.performAccessibilityAnalysis([pageInfo], {
        maxConcurrency: 1,
        retryFailedPages: false,
      });

      this.errorHandler.logInfo('Single page analysis completed', {
        resultsCount: result.length,
        violationsFound: result.reduce((sum, r) => sum + r.summary.totalViolations, 0)
      });

      return result;
    } catch (error) {
      this.errorHandler.handleError(error, 'Single page test failed');
      throw error;
    }
  }

  private async cleanupReportsDirectory(): Promise<void> {
    const reportsDir = './accessibility-reports';
    const historyDir = './accessibility-reports/history';
    const fileOps = FileOperationsService.getInstance();

    try {
      if (fs.existsSync(reportsDir)) {
        const files = fs.readdirSync(reportsDir);
        let deletedCount = 0;
        let movedCount = 0;

        // First, move JSON files to history folder
        const jsonFiles = files.filter(file => file.endsWith('.json'));
        if (jsonFiles.length > 0) {
          // Ensure history directory exists
          const historyResult = fileOps.ensureDirectoryExists(historyDir);
          if (historyResult.success) {
            // Move JSON files to history
            const moveResult = fileOps.moveFilesByPattern(reportsDir, historyDir, /\.json$/);
            if (moveResult.success && moveResult.movedFiles) {
              movedCount = moveResult.movedFiles.length;
              this.errorHandler.logInfo(`Moved ${movedCount} JSON files to history folder`, {
                historyDir,
                movedFiles: moveResult.movedFiles,
              });
            } else {
              this.errorHandler.logWarning('Failed to move some JSON files to history', {
                errors: moveResult.errors,
              });
            }
          } else {
            this.errorHandler.logWarning('Failed to create history directory', {
              error: historyResult.message,
            });
          }
        }

        // Then delete all PDF files (clean slate for new scan)
        const remainingFiles = fs.readdirSync(reportsDir);
        const pdfFiles = remainingFiles.filter(file => file.endsWith('.pdf'));

        if (pdfFiles.length > 0) {
          // Delete all PDF files to prepare for new scan
          pdfFiles.forEach(file => {
            const filePath = `${reportsDir}/${file}`;
            fs.unlinkSync(filePath);
            deletedCount++;
          });

          this.errorHandler.logInfo(`Deleted all existing PDF reports (${pdfFiles.length} files) to prepare for new scan`, {
            deletedFiles: pdfFiles,
          });
        }

        // Remove any remaining non-PDF files and directories (but preserve history folder)
        const finalRemainingFiles = fs.readdirSync(reportsDir);
        finalRemainingFiles.forEach(file => {
          const filePath = `${reportsDir}/${file}`;
          const stat = fs.statSync(filePath);

          if (stat.isDirectory()) {
            // Remove subdirectories (like parallel-analysis, page-cache) but preserve history folder
            if (file !== 'history') {
              fs.rmSync(filePath, { recursive: true, force: true });
              deletedCount++;
            }
          } else if (!file.endsWith('.pdf')) {
            // Remove any remaining non-PDF files
            fs.unlinkSync(filePath);
            deletedCount++;
          }
        });

        this.errorHandler.logSuccess(`Cleaned up accessibility reports directory`, {
          directory: reportsDir,
          itemsDeleted: deletedCount,
          itemsMoved: movedCount,
          historyDirectory: historyDir,
        });
      } else {
        // Create the directory if it doesn't exist
        fs.mkdirSync(reportsDir, { recursive: true });
        this.errorHandler.logInfo('Created accessibility reports directory', {
          directory: reportsDir,
        });
      }
    } catch (error) {
      this.errorHandler.logWarning('Failed to cleanup reports directory', { error });
    }
  }

  private logReportSummary(reportPaths: string[]): void {
    this.errorHandler.logInfo('\n🎉 Accessibility Audit Complete!');
    this.errorHandler.logInfo('='.repeat(40));

    if (reportPaths.length === 0) {
      this.errorHandler.logWarning('No reports were generated');
      return;
    }

    this.errorHandler.logInfo(`\n📄 Generated ${reportPaths.length} Reports:`);

    reportPaths.forEach((path, index) => {
      const fileName = path.split('/').pop() || path;
      let reportType = 'Unknown';

      if (fileName.includes('stakeholders')) {
        reportType = '📊 Product Owners & Stakeholders';
      } else if (fileName.includes('researchers')) {
        reportType = '🔬 User Researchers & UCD';
      } else if (fileName.includes('developers')) {
        reportType = '💻 Developers & Testers';
      } else if (fileName.includes('results.json')) {
        reportType = '📋 Raw Data (JSON)';
      }

      this.errorHandler.logInfo(`   ${index + 1}. ${reportType}`);
      this.errorHandler.logInfo(`      File: ${fileName}`);
    });

    this.errorHandler.logInfo(`\n✅ All reports saved to: accessibility-reports/`);
    this.errorHandler.logInfo(
      '💡 Each report is tailored for its specific audience with relevant insights and recommendations.'
    );
  }

  /**
   * Regenerates reports from existing JSON data files
   */
  async regenerateReportsFromExistingData(_targetUrl: string): Promise<ServiceResult<string[]>> {
    try {
      const reportsDir = './accessibility-reports';
      const historyDir = './accessibility-reports/history';

      if (!fs.existsSync(reportsDir)) {
        return {
          success: false,
          message: 'No accessibility reports directory found. Please run an audit first.',
        };
      }

      // Look for JSON files in both reports directory and history directory
      const allJsonFiles: Array<{ name: string; path: string; mtime: Date }> = [];

      // Check main reports directory
      if (fs.existsSync(reportsDir)) {
        const files = fs.readdirSync(reportsDir);
        const jsonFiles = files.filter(
          file =>
            file.endsWith('-results.json') ||
            (file.includes('-accessibility-report-') && file.endsWith('.json'))
        );

        jsonFiles.forEach(file => {
          const filePath = `${reportsDir}/${file}`;
          const stats = fs.statSync(filePath);
          allJsonFiles.push({
            name: file,
            path: filePath,
            mtime: stats.mtime,
          });
        });
      }

      // Check history directory
      if (fs.existsSync(historyDir)) {
        const historyFiles = fs.readdirSync(historyDir);
        const historyJsonFiles = historyFiles.filter(
          file =>
            file.endsWith('-results.json') ||
            (file.includes('-accessibility-report-') && file.endsWith('.json'))
        );

        historyJsonFiles.forEach(file => {
          const filePath = `${historyDir}/${file}`;
          const stats = fs.statSync(filePath);
          allJsonFiles.push({
            name: file,
            path: filePath,
            mtime: stats.mtime,
          });
        });
      }

      if (allJsonFiles.length === 0) {
        return {
          success: false,
          message: 'No existing analysis data found in reports or history directories. Please run an accessibility audit first.',
        };
      }

      // Sort by modification time to get the most recent
      const sortedFiles = allJsonFiles.sort((a, b) => b.mtime.getTime() - a.mtime.getTime());
      const mostRecentFile = sortedFiles[0];

      if (!mostRecentFile) {
        return {
          success: false,
          message: 'No valid analysis files found.',
        };
      }

      this.errorHandler.logInfo('Found existing analysis data', {
        file: mostRecentFile.name,
        lastModified: mostRecentFile.mtime.toISOString(),
      });

      // Load the existing data
      const existingData = JSON.parse(fs.readFileSync(mostRecentFile.path, 'utf8'));

      // Validate that we have the necessary data structure
      if (!existingData.pageAnalysis || !Array.isArray(existingData.pageAnalysis)) {
        return {
          success: false,
          message: 'Invalid data format in existing analysis file. Cannot regenerate reports.',
        };
      }

      // Check if pageAnalysis is empty
      if (existingData.pageAnalysis.length === 0) {
        return {
          success: false,
          message:
            'The existing analysis file contains no page data. This usually means the previous audit failed or was incomplete. Please run a fresh accessibility audit first.',
        };
      }

      this.errorHandler.logInfo('Regenerating reports from existing data', {
        pages: existingData.pageAnalysis.length,
        totalViolations: existingData.summary?.totalViolations || 0,
      });

      // Initialize browser manager for PDF generation
      try {
        await this.browserManager.initialize();
        this.errorHandler.logInfo('Browser manager initialized for PDF generation');
      } catch (browserError) {
        this.errorHandler.logWarning('Failed to initialize browser manager', { browserError });
        return {
          success: false,
          message: 'Failed to initialize browser for PDF generation. Please try again.',
        };
      }

      // Convert to AnalysisResult format for report generation
      const analysisResults: AnalysisResult[] = existingData.pageAnalysis.map((page: any) => ({
        url: page.url,
        title: page.title || page.url.split('/').pop() || page.url,
        timestamp: page.timestamp || new Date().toISOString(),
        violations: page.violations || [],
        summary: page.summary || {
          totalViolations: 0,
          criticalViolations: 0,
          seriousViolations: 0,
          moderateViolations: 0,
          minorViolations: 0,
        },
        tool: page.tool || 'regenerated-report',
      }));

      // Extract target URL from the existing data
      const extractedTargetUrl =
        existingData.siteUrl || (analysisResults.length > 0 ? analysisResults[0]?.url || 'unknown' : 'unknown');

      // Generate reports using existing method
      const reportPaths = await this.generateReports(analysisResults, extractedTargetUrl);

      return {
        success: true,
        message: `Successfully regenerated ${reportPaths.length} reports from existing data.`,
        data: reportPaths,
      };
    } catch (error) {
      this.errorHandler.handleError(error, 'Failed to regenerate reports from existing data');
      return {
        success: false,
        message: `Failed to regenerate reports: ${(error as Error).message}`,
      };
    } finally {
      // Cleanup browser resources
      try {
        await this.cleanup();
        this.errorHandler.logInfo('Browser cleanup completed after report regeneration');
      } catch (cleanupError) {
        this.errorHandler.logWarning('Failed to cleanup browser resources', { cleanupError });
      }
    }
  }

  // Add testSinglePageWithReports method for web server
  async testSinglePageWithReports(
    url: string,
    wcagLevel: string = 'WCAG2AA',
    scanMetadata?: any
  ): Promise<{ analysisResults: AnalysisResult[]; reportPaths: string[] }> {
    this.errorHandler.logInfo('Starting single page accessibility test with reports', { url });

    try {
      // Initialize browser manager
      await this.browserManager.initialize();

      // Create a single page info object
      const pageInfo: PageInfo = {
        url,
        title: url.split('/').pop() || url,
        depth: 0,
        foundOn: url,
        status: 200,
        loadTime: 0,
      };

      // Run analysis on the single page
      const analysisResults = await this.performAccessibilityAnalysis([pageInfo], {
        maxConcurrency: 1,
        retryFailedPages: false,
      });

      // Generate reports
      const reportPaths = await this.generateReports(analysisResults, url);

      this.errorHandler.logSuccess('Single page test with reports completed', {
        url,
        analysisResults: analysisResults.length,
        reportPaths: reportPaths.length,
      });

      return {
        analysisResults,
        reportPaths,
      };
    } catch (error) {
      this.errorHandler.handleError(error, 'Single page test with reports failed');
      throw error;
    } finally {
      await this.cleanup();
    }
  }

  // Add generatePdfReportsFromStoredData method for web server
  async generatePdfReportsFromStoredData(
    storedReport: any,
    options: {
      reportId: string;
      audience?: string;
      generateAll?: boolean;
      scanMetadata?: any;
    }
  ): Promise<ServiceResult<Array<{ filePath: string; audience: string; displayName: string; sizeKB: number }>>> {
    try {
      this.errorHandler.logInfo('Generating PDF reports from stored data', {
        reportId: options.reportId,
        audience: options.audience,
        generateAll: options.generateAll,
      });

      // Ensure browser is healthy before PDF generation
      const isHealthy = await this.browserManager.isBrowserHealthy();
      if (!isHealthy) {
        this.errorHandler.logInfo('Browser not healthy, force reinitializing for PDF generation...');
        await this.browserManager.forceReinitialize();
      }

      const pdfGenerator = new PdfOrchestrator(await this.browserManager.getPage('pdf-generation'));

      // Determine which audiences to generate reports for
      let audiences: Array<{ name: string; displayName: string }> = [];

      if (options.generateAll) {
        audiences = [
          { name: 'stakeholders', displayName: 'Product Owners & Stakeholders' },
          { name: 'researchers', displayName: 'User Researchers & UCD' },
          { name: 'developers', displayName: 'Developers & Testers' },
        ];
      } else if (options.audience) {
        const audienceMap: Record<string, { name: string; displayName: string }> = {
          stakeholders: { name: 'stakeholders', displayName: 'Product Owners & Stakeholders' },
          researchers: { name: 'researchers', displayName: 'User Researchers & UCD' },
          developers: { name: 'developers', displayName: 'Developers & Testers' },
        };
        const audience = audienceMap[options.audience];
        if (audience) {
          audiences = [audience];
        } else {
          return {
            success: false,
            message: `Invalid audience: ${options.audience}. Valid options are: stakeholders, researchers, developers`,
          };
        }
      } else {
        return {
          success: false,
          message: 'Either generateAll or audience must be specified',
        };
      }

      // Generate PDF reports
      const pdfResults = await pdfGenerator.generatePdfReports(storedReport, {
        filename: `accessibility-audit-${options.reportId}`,
        audiences,
      });

      if (pdfResults.success && pdfResults.data) {
        this.errorHandler.logSuccess('PDF reports generated successfully from stored data', {
          reportId: options.reportId,
          totalReports: pdfResults.data.length,
          audiences: audiences.map(a => a.displayName),
        });

        return {
          success: true,
          data: pdfResults.data,
          message: `Successfully generated ${pdfResults.data.length} PDF reports from stored data.`,
        };
      } else {
        return {
          success: false,
          message: pdfResults.message || 'Failed to generate PDF reports from stored data',
        };
      }
    } catch (error) {
      this.errorHandler.handleError(error, 'Failed to generate PDF reports from stored data');
      return {
        success: false,
        message: `Failed to generate PDF reports: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  }
}
