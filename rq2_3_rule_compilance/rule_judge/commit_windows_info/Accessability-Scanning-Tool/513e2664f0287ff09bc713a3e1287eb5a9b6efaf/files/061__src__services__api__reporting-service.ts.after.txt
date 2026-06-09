import { EventEmitter } from 'events';
import { AccessibilityTestOptions, ServiceResult } from '../../core/types/common';
import { PerformanceMonitor } from '../../core/utils/performance-monitor';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { AnalysisCache } from '../orchestration/analysis-cache';
import { BrowserManager } from '../../core/utils/browser-manager';

// Import existing PDF generation components
import { PdfOrchestrator } from '../../../playwright/tests/utils/pdf-generators/pdf-orchestrator';
import { SiteWideAccessibilityPdfGenerator } from '../../../playwright/tests/utils/site-wide-pdf-generator';

export class ReportingService extends EventEmitter {
  private static instance: ReportingService;
  private performanceMonitor: PerformanceMonitor;
  private errorHandler: ErrorHandlerService;
  private analysisCache: AnalysisCache;
  private browserManager: BrowserManager;
  private activeReports: Map<
    string,
    {
      type: string;
      startTime: Date;
      status: 'pending' | 'generating' | 'completed' | 'failed';
      progress: number;
      outputPath?: string;
    }
  > = new Map();

  private constructor() {
    super();
    this.performanceMonitor = PerformanceMonitor.getInstance();
    this.errorHandler = ErrorHandlerService.getInstance();
    this.analysisCache = AnalysisCache.getInstance();
    this.browserManager = BrowserManager.getInstance();
  }

  public static getInstance(): ReportingService {
    if (!ReportingService.instance) {
      ReportingService.instance = new ReportingService();
    }
    return ReportingService.instance;
  }

  /**
   * Generate a quick report for immediate results
   */
  public async generateQuickReport(
    analysisData: any,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<string>> {
    const reportId = `quick-${Date.now()}`;

    try {
      this.activeReports.set(reportId, {
        type: 'quick',
        startTime: new Date(),
        status: 'generating',
        progress: 0,
      });

      // Create a browser context for PDF generation
      const sessionId = `report-${reportId}`;
      const page = await this.browserManager.navigateToUrl(sessionId, 'about:blank');

      // Create PDF orchestrator with the page
      const pdfOrchestrator = new PdfOrchestrator(page);

      // Generate PDF using the actual method available
      const reportResult = await pdfOrchestrator.generatePdfReports(analysisData, {
        audiences: [{ name: 'executive', displayName: 'Executive Summary' }], // Quick report is executive summary
      });

      // Cleanup browser context
      await this.browserManager.cleanup(sessionId);

      if (reportResult.success && reportResult.data) {
        const outputPath = reportResult.data[0]?.filePath || 'report-generated.pdf';
        this.activeReports.get(reportId)!.status = 'completed';
        this.activeReports.get(reportId)!.outputPath = outputPath;
        this.activeReports.get(reportId)!.progress = 100;

        this.emit('reportCompleted', { reportId, outputPath, type: 'quick' });

        return {
          success: true,
          data: outputPath,
        };
      } else {
        throw new Error('PDF generation failed');
      }
    } catch (error) {
      this.activeReports.get(reportId)!.status = 'failed';
      this.errorHandler.handleError(error as Error, 'ReportingService.generateQuickReport');

      return {
        success: false,
        error: error as Error,
        message: `Quick report generation failed: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Generate a comprehensive report with detailed analysis
   */
  public async generateComprehensiveReport(
    analysisData: any,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<string>> {
    const reportId = `comprehensive-${Date.now()}`;

    try {
      this.activeReports.set(reportId, {
        type: 'comprehensive',
        startTime: new Date(),
        status: 'generating',
        progress: 0,
      });

      this.emit('reportStarted', { reportId, type: 'comprehensive' });

      // Create a browser context for PDF generation
      const sessionId = `report-${reportId}`;
      const page = await this.browserManager.navigateToUrl(sessionId, 'about:blank');

      // Create site-wide PDF generator with the page
      const siteWidePDFGenerator = new SiteWideAccessibilityPdfGenerator(page);

      // Generate comprehensive report using the actual method available
      const reportResult = await siteWidePDFGenerator.generateSiteWidePdfReport(
        analysisData,
        `comprehensive-report-${Date.now()}`
      );

      // Cleanup browser context
      await this.browserManager.cleanup(sessionId);

      if (reportResult && reportResult.length > 0) {
        const outputPath = reportResult[0]; // First report path
        this.activeReports.get(reportId)!.status = 'completed';
        this.activeReports.get(reportId)!.outputPath = outputPath;
        this.activeReports.get(reportId)!.progress = 100;

        this.emit('reportCompleted', { reportId, outputPath, type: 'comprehensive' });

        return {
          success: true,
          data: outputPath,
        };
      } else {
        throw new Error('Site-wide PDF generation failed');
      }
    } catch (error) {
      this.activeReports.get(reportId)!.status = 'failed';
      this.emit('reportFailed', { reportId, error });

      return {
        success: false,
        error: error as Error,
        message: `Comprehensive report generation failed: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Generate a detailed research report
   */
  public async generateDetailedReport(
    analysisData: any,
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<string>> {
    const reportId = `detailed-${Date.now()}`;

    try {
      this.activeReports.set(reportId, {
        type: 'detailed',
        startTime: new Date(),
        status: 'generating',
        progress: 0,
      });

      this.emit('reportStarted', { reportId, type: 'detailed' });

      // Create a browser context for PDF generation
      const sessionId = `report-${reportId}`;
      const page = await this.browserManager.navigateToUrl(sessionId, 'about:blank');

      // Create PDF orchestrator with the page
      const pdfOrchestrator = new PdfOrchestrator(page);

      // Generate detailed report using the actual method available
      const reportResult = await pdfOrchestrator.generatePdfReports(analysisData, {
        audiences: [
          { name: 'research', displayName: 'Research Report' },
          { name: 'developer', displayName: 'Developer Report' },
        ], // Detailed report includes both
      });

      // Cleanup browser context
      await this.browserManager.cleanup(sessionId);

      if (reportResult.success && reportResult.data) {
        const outputPath = reportResult.data[0]?.filePath || 'detailed-report-generated.pdf';
        this.activeReports.get(reportId)!.status = 'completed';
        this.activeReports.get(reportId)!.outputPath = outputPath;
        this.activeReports.get(reportId)!.progress = 100;

        this.emit('reportCompleted', { reportId, outputPath, type: 'detailed' });

        return {
          success: true,
          data: outputPath,
        };
      } else {
        throw new Error('Detailed PDF generation failed');
      }
    } catch (error) {
      this.activeReports.get(reportId)!.status = 'failed';
      this.emit('reportFailed', { reportId, error });

      return {
        success: false,
        error: error as Error,
        message: `Detailed report generation failed: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Generate a custom report with specified configuration
   */
  public async generateCustomReport(
    analysisData: any,
    reportConfig: {
      type: 'executive' | 'research' | 'developer' | 'custom';
      audiences?: Array<{ name: string; displayName: string }>;
    },
    options: AccessibilityTestOptions = {}
  ): Promise<ServiceResult<string>> {
    const reportId = `custom-${Date.now()}`;

    try {
      this.activeReports.set(reportId, {
        type: 'custom',
        startTime: new Date(),
        status: 'generating',
        progress: 0,
      });

      this.emit('reportStarted', { reportId, type: 'custom' });

      // Create a browser context for PDF generation
      const sessionId = `report-${reportId}`;
      const page = await this.browserManager.navigateToUrl(sessionId, 'about:blank');

      let reportResult: any;

      if (reportConfig.type === 'custom') {
        // Use PdfOrchestrator for custom reports
        const pdfOrchestrator = new PdfOrchestrator(page);
        const audience = reportConfig.audiences?.[0] || {
          name: 'custom',
          displayName: 'Custom Report',
        };
        const filename = `custom-report-${Date.now()}.pdf`;

        reportResult = await pdfOrchestrator.generateCustomPdf(analysisData, audience, filename, {
          format: 'A4',
          includeBackground: true,
        });
      } else {
        // Use standard PDF generation
        const pdfOrchestrator = new PdfOrchestrator(page);
        const defaultAudiences = {
          executive: { name: 'executive', displayName: 'Executive Summary' },
          research: { name: 'research', displayName: 'Research Report' },
          developer: { name: 'developer', displayName: 'Developer Report' },
        };

        reportResult = await pdfOrchestrator.generatePdfReports(analysisData, {
          audiences: reportConfig.audiences || [defaultAudiences[reportConfig.type]],
        });
      }

      // Cleanup browser context
      await this.browserManager.cleanup(sessionId);

      if (reportResult && (reportResult.success || reportResult.length > 0)) {
        const outputPath =
          reportResult.data?.[0]?.filePath || reportResult[0] || 'custom-report-generated.pdf';
        this.activeReports.get(reportId)!.status = 'completed';
        this.activeReports.get(reportId)!.outputPath = outputPath;
        this.activeReports.get(reportId)!.progress = 100;

        this.emit('reportCompleted', { reportId, outputPath, type: 'custom' });

        return {
          success: true,
          data: outputPath,
        };
      } else {
        throw new Error('Custom PDF generation failed');
      }
    } catch (error) {
      this.activeReports.get(reportId)!.status = 'failed';
      this.emit('reportFailed', { reportId, error });

      return {
        success: false,
        error: error as Error,
        message: `Custom report generation failed: ${(error as Error).message}`,
      };
    }
  }

  /**
   * Get the status of a report generation
   */
  public getReportStatus(reportId: string): any {
    const report = this.activeReports.get(reportId);
    if (!report) {
      return {
        success: false,
        error: 'Report not found',
        message: 'No report found with the specified ID',
      };
    }

    return {
      success: true,
      data: {
        reportId,
        ...report,
        elapsedTime: Date.now() - report.startTime.getTime(),
      },
    };
  }

  /**
   * Get all active reports
   */
  public getActiveReports(): any[] {
    return Array.from(this.activeReports.entries()).map(([id, report]) => ({
      reportId: id,
      ...report,
      elapsedTime: Date.now() - report.startTime.getTime(),
    }));
  }

  /**
   * Cancel a report generation
   */
  public cancelReport(reportId: string): ServiceResult<boolean> {
    const report = this.activeReports.get(reportId);
    if (!report) {
      return {
        success: false,
        error: new Error('Report not found'),
        message: 'No report found with the specified ID',
      };
    }

    if (report.status === 'completed' || report.status === 'failed') {
      return {
        success: false,
        error: new Error('Cannot cancel completed or failed report'),
        message: 'Report has already finished processing',
      };
    }

    report.status = 'failed';
    report.progress = 0;
    this.activeReports.set(reportId, report);

    this.emit('reportCancelled', { reportId });

    return {
      success: true,
      data: true,
    };
  }

  /**
   * Clean up completed reports
   */
  public cleanup(): void {
    const now = Date.now();
    const maxAge = 1000 * 60 * 60 * 24; // 24 hours

    for (const [reportId, report] of this.activeReports.entries()) {
      if (
        (report.status === 'completed' || report.status === 'failed') &&
        now - report.startTime.getTime() > maxAge
      ) {
        this.activeReports.delete(reportId);
      }
    }
  }
}
