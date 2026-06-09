import { Page } from 'playwright';
import { AxeTestRunner } from '@/utils/runners/axe-test-runner';
import { Pa11yTestRunner } from '@/utils/runners/pa11y-test-runner';
import {
  ProcessedViolation,
  AccessibilityReport,
  SiteWideAccessibilityReport,
  ServiceResult,
} from '@/core/types/common';
import { ViolationProcessor } from '@/utils/processors/violation-processor';
import { PageAnalysisResult, PageAnalyzer } from '@/utils/analyzers/page-analyzer';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService } from '../services/error-handler-service';
import { FileOperationsService } from '@/utils/services/file-operations-service';
import { TestSetupUtil } from '@/utils/test-setup-util';
import { AxeResults } from 'axe-core';

export interface MultiToolResults {
  axe: AxeResults | null;
  pa11y: any;
}

export interface MultiPageTestOptions {
  maxConcurrency?: number;
  delayBetweenPages?: number;
  skipErrors?: boolean;
  handleRedirects?: boolean;
  captureScreenshots?: boolean;
}

export class AccessibilityTestOrchestrator {
  private axeRunner: AxeTestRunner;
  private pa11yRunner: Pa11yTestRunner;
  private violationProcessor: ViolationProcessor;
  private pageAnalyzer: PageAnalyzer;
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private fileOps = FileOperationsService.getInstance();
  private testSetup = TestSetupUtil.getInstance();

  constructor(private page: Page) {
    this.axeRunner = new AxeTestRunner(page);
    this.pa11yRunner = new Pa11yTestRunner(page);
    this.violationProcessor = new ViolationProcessor(page);
    this.pageAnalyzer = new PageAnalyzer(page);
  }

  /**
   * Runs comprehensive accessibility analysis using all available tools
   */
  async runComprehensiveAnalysis(
    captureScreenshots: boolean = true
  ): Promise<ServiceResult<ProcessedViolation[]>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      this.errorHandler.logInfo('Starting comprehensive accessibility analysis');

      // Run all tools in parallel for efficiency
      const [axeResult, pa11yResult] = await Promise.all([
        this.axeRunner.runDevToolsAnalysis(),
        this.pa11yRunner.runAnalysis(),
      ]);

      // Prepare results for processing
      const results: MultiToolResults = {
        axe: this.errorHandler.isSuccess(axeResult) ? (axeResult.data as AxeResults) : null,
        pa11y: this.errorHandler.isSuccess(pa11yResult) ? pa11yResult.data : null,
      };

      // Process violations from all tools
      const processedResult = await this.violationProcessor.processMultiToolViolations(
        results,
        captureScreenshots
      );

      if (this.errorHandler.isError(processedResult)) {
        throw new Error(processedResult.error?.message || processedResult.message || 'Unknown error');
      }

      const violations = processedResult.data || [];
      this.errorHandler.logSuccess(
        `Comprehensive analysis completed: ${violations.length} violations found`
      );
      return violations;
    }, 'runComprehensiveAnalysis');
  }

  /**
   * Runs specific accessibility tests
   */
  async runSpecificTests(options: {
    colorContrast?: boolean;
    keyboard?: boolean;
    aria?: boolean;
    forms?: boolean;
    images?: boolean;
    landmarks?: boolean;
  }): Promise<ServiceResult<ProcessedViolation[]>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      const allViolations: ProcessedViolation[] = [];

      // Run specified tests
      if (options.colorContrast) {
        const result = await this.axeRunner.runColorContrastAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      if (options.keyboard) {
        const result = await this.axeRunner.runKeyboardAccessibilityAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      if (options.aria) {
        const result = await this.axeRunner.runAriaAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      if (options.forms) {
        const result = await this.axeRunner.runFormAccessibilityAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      if (options.images) {
        const result = await this.axeRunner.runImageAccessibilityAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      if (options.landmarks) {
        const result = await this.axeRunner.runLandmarksAndHeadingsAnalysis();
        if (this.errorHandler.isSuccess(result)) {
          const processed = await this.violationProcessor.processMultiToolViolations({
            axe: result.data as AxeResults,
            pa11y: null,
          });
          if (this.errorHandler.isSuccess(processed)) {
            allViolations.push(...(processed.data as ProcessedViolation[]));
          }
        }
      }

      return allViolations;
    }, 'runSpecificTests');
  }

  /**
   * Generates a complete accessibility report
   */
  async generateAccessibilityReport(
    url: string,
    testSuite: string,
    browser: string = 'chromium',
    viewport: string = 'Desktop',
    captureScreenshots: boolean = true
  ): Promise<ServiceResult<AccessibilityReport>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      this.errorHandler.logInfo(`Generating accessibility report for: ${url}`);

      // Run comprehensive analysis and page analysis in parallel
      const [violationsResult, pageAnalysisResult] = await Promise.all([
        this.runComprehensiveAnalysis(captureScreenshots),
        this.pageAnalyzer.analyzeCurrentPage(),
      ]);

      if (this.errorHandler.isError(violationsResult)) {
        throw new Error(violationsResult.error?.message || violationsResult.message || 'Unknown error');
      }

      if (this.errorHandler.isError(pageAnalysisResult)) {
        throw new Error(pageAnalysisResult.error?.message || pageAnalysisResult.message || 'Unknown error');
      }

      const violations = violationsResult.data || [];
      const pageAnalysis = pageAnalysisResult.data;

      if (!pageAnalysis) {
        throw new Error('Page analysis failed to return data');
      }

      // Create summary
      const summary = this.createSummary(violations);

      const report: AccessibilityReport = {
        url,
        timestamp: new Date().toISOString(),
        testSuite,
        browser,
        viewport,
        summary,
        violations,
        pageAnalysis,
      };

      this.errorHandler.logSuccess(`Report generated with ${violations.length} violations`);
      return report;
    }, 'generateAccessibilityReport');
  }

  /**
   * Tests multiple pages with advanced options
   */
  async testMultiplePages(
    urls: string[],
    testSuite: string,
    options: MultiPageTestOptions = {}
  ): Promise<ServiceResult<AccessibilityReport[]>> {
    const {
      maxConcurrency = this.config.getReportingConfiguration().maxConcurrency,
      delayBetweenPages = this.config.getReportingConfiguration().delayBetweenPages,
      skipErrors = true,
      handleRedirects = true,
      captureScreenshots = true,
    } = options;

    return this.errorHandler.executeWithErrorHandling(async () => {
      this.errorHandler.logInfo(`Testing ${urls.length} pages with concurrency: ${maxConcurrency}`);

      if (handleRedirects) {
        this.errorHandler.logInfo(
          'Redirect handling enabled - will track URL changes during navigation'
        );
      }

      if (!captureScreenshots) {
        this.errorHandler.logInfo('Screenshot capture disabled for performance optimization');
      }

      const reports: AccessibilityReport[] = [];
      const semaphore = new Array(maxConcurrency).fill(null);
      const processedUrls = new Set<string>(); // Track processed URLs for redirect handling

      const processUrl = async (url: string, index: number): Promise<void> => {
        try {
          this.errorHandler.logInfo(`Processing page ${index + 1}/${urls.length}: ${url}`);

          // Check for redirect handling
          if (handleRedirects && processedUrls.has(url)) {
            this.errorHandler.logInfo(`Skipping already processed URL: ${url}`);
            return;
          }

          // Navigate to URL
          await this.testSetup.setupAccessibilityTest(this.page, {
            url,
            skipInitialNavigation: false,
            waitForNetworkIdle: true,
          });

          // Track URL after navigation (in case of redirects)
          if (handleRedirects) {
            const currentUrl = this.page.url();
            if (currentUrl !== url) {
              this.errorHandler.logInfo(`Redirect detected: ${url} → ${currentUrl}`);
              processedUrls.add(currentUrl);
            }
            processedUrls.add(url);
          }

          // Wait for page to be ready
          await this.testSetup.waitForPageReady(this.page);

          // Generate report
          const reportResult = await this.generateAccessibilityReport(
            url,
            testSuite,
            'chromium',
            'Desktop',
            captureScreenshots
          );

          if (this.errorHandler.isSuccess(reportResult)) {
            reports.push(reportResult.data);
            this.errorHandler.logSuccess(`Completed page ${index + 1}/${urls.length}`);
          } else if (!skipErrors) {
            throw new Error(reportResult.error?.message || reportResult.message || 'Unknown error');
          }

          // Delay between pages
          if (delayBetweenPages > 0) {
            await new Promise(resolve => setTimeout(resolve, delayBetweenPages));
          }
        } catch (error) {
          this.errorHandler.handleError(error, `Processing URL: ${url}`);
          if (!skipErrors) {
            throw error;
          }
        }
      };

      // Process URLs with concurrency control
      const urlPromises = urls.map(async (url, index) => {
        await new Promise(resolve => {
          const runWhenReady = () => {
            const availableSlot = semaphore.findIndex(slot => slot === null);
            if (availableSlot !== -1) {
              semaphore[availableSlot] = url;
              processUrl(url, index).finally(() => {
                semaphore[availableSlot] = null;
                resolve(void 0);
              });
            } else {
              setTimeout(runWhenReady, 100);
            }
          };
          runWhenReady();
        });
      });

      await Promise.all(urlPromises);

      this.errorHandler.logSuccess(`Completed testing ${reports.length}/${urls.length} pages`);
      return reports;
    }, 'testMultiplePages');
  }

  /**
   * Aggregates multiple reports into a site-wide report
   */
  aggregateReports(reports: AccessibilityReport[]): SiteWideAccessibilityReport {
    const siteUrl = reports.length > 0 ? new URL(reports[0]?.url || '').origin : '';
    const timestamp = new Date().toISOString();
    const testSuite = reports.length > 0 ? reports[0]?.testSuite || 'Unknown' : 'Unknown';

    // Aggregate violations by type
    const violationsByType: Record<string, any> = {};
    let totalViolations = 0;

    reports.forEach(report => {
      report.violations.forEach(violation => {
        if (!violationsByType[violation.id]) {
          violationsByType[violation.id] = {
            count: 0,
            pages: [],
            impact: violation.impact,
            totalOccurrences: 0,
            browsers: [],
            tools: [],
          };
        }

        violationsByType[violation.id].count++;
        violationsByType[violation.id].pages.push(report.url);
        violationsByType[violation.id].totalOccurrences += violation.occurrences;
        violationsByType[violation.id].tools = [
          ...new Set([...violationsByType[violation.id].tools, ...violation.tools]),
        ];
        totalViolations++;
      });
    });

    // Calculate summary statistics
    const summary = {
      totalPages: reports.length,
      pagesWithViolations: reports.filter(r => r.violations.length > 0).length,
      totalViolations,
      criticalViolations: reports.reduce((sum, r) => sum + r.summary.criticalViolations, 0),
      seriousViolations: reports.reduce((sum, r) => sum + r.summary.seriousViolations, 0),
      moderateViolations: reports.reduce((sum, r) => sum + r.summary.moderateViolations, 0),
      minorViolations: reports.reduce((sum, r) => sum + r.summary.minorViolations, 0),
      compliancePercentage:
        reports.length > 0
          ? ((reports.length - reports.filter(r => r.violations.length > 0).length) /
            reports.length) *
          100
          : 0,
      mostCommonViolations: Object.entries(violationsByType)
        .sort(([, a], [, b]) => b.totalOccurrences - a.totalOccurrences)
        .slice(0, 10)
        .map(([id, data]) => ({
          id,
          affectedPages: data.pages.length,
          totalOccurrences: data.totalOccurrences,
          impact: data.impact,
          description: `${id} violation`,
        })),
    };

    return {
      siteUrl,
      timestamp,
      testSuite,
      summary,
      pageReports: reports,
      violationsByType,
    };
  }

  /**
   * Saves a report to file
   */
  async saveReportToFile(
    report: AccessibilityReport | SiteWideAccessibilityReport,
    filename: string
  ): Promise<ServiceResult<string>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      const reportsDir = this.fileOps.getReportsDirectory();
      const filePath = `${reportsDir}/${filename}.json`;

      const result = this.fileOps.writeFile(filePath, JSON.stringify(report, null, 2));

      if (!result.success) {
        throw new Error(result.message);
      }

      this.errorHandler.logSuccess(`Report saved to: ${filePath}`);
      return filePath;
    }, 'saveReportToFile');
  }

  /**
   * Creates a summary of violations
   */
  private createSummary(violations: ProcessedViolation[]): AccessibilityReport['summary'] {
    const summary = {
      totalViolations: violations.length,
      criticalViolations: violations.filter(v => v.impact === 'critical').length,
      seriousViolations: violations.filter(v => v.impact === 'serious').length,
      moderateViolations: violations.filter(v => v.impact === 'moderate').length,
      minorViolations: violations.filter(v => v.impact === 'minor').length,
      wcagAAViolations: violations.filter(v => v.wcagLevel === 'AA').length,
      wcagAAAViolations: violations.filter(v => v.wcagLevel === 'AAA').length,
    };

    return summary;
  }
}
