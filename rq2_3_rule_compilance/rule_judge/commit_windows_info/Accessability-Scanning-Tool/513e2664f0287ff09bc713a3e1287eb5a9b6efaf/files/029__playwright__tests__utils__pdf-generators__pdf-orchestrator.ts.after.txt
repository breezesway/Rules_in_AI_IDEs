import { Page } from '@playwright/test';
import { SiteWideAccessibilityReport } from '../accessibility-test-orchestrator';
import { PdfTemplateGenerator } from './pdf-template-generator';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';
import { FileOperationsService } from '../services/file-operations-service';

export interface PdfGenerationResult {
  filePath: string;
  audience: string;
  displayName: string;
  sizeKB: number;
}

export interface PdfGenerationOptions {
  audiences?: Array<{ name: string; displayName: string }>;
  filename?: string;
  format?: 'A4' | 'Letter';
  includeBackground?: boolean;
  margins?: {
    top: string;
    right: string;
    bottom: string;
    left: string;
  };
  includeScreenshot?: boolean;
}

export class PdfOrchestrator {
  private templateGenerator: PdfTemplateGenerator;
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private fileOps = FileOperationsService.getInstance();

  constructor(private page: Page) {
    this.templateGenerator = new PdfTemplateGenerator();
  }

  /**
   * Generates PDF reports for all specified audiences
   */
  async generatePdfReports(
    report: SiteWideAccessibilityReport,
    options: PdfGenerationOptions = {}
  ): Promise<ServiceResult<PdfGenerationResult[]>> {
    const {
      audiences = this.getDefaultAudiences(),
      filename = this.generateDefaultFilename(report),
      format = 'A4',
      includeBackground = true,
      includeScreenshot = true,
      margins = {
        top: '0.75in',
        right: '0.75in',
        bottom: '0.75in',
        left: '0.75in',
      },
    } = options;

    return this.errorHandler.executeWithErrorHandling(async () => {
      this.errorHandler.logInfo(`Generating PDF reports for ${audiences.length} audiences`);

      const results: PdfGenerationResult[] = [];
      let screenshotPath: string | null = null;

      try {
        // Capture screenshot of the main page if requested
        if (includeScreenshot) {
          const screenshotResult = await this.captureMainPageScreenshot(report.siteUrl);
          screenshotPath = this.errorHandler.isSuccess(screenshotResult)
            ? screenshotResult.data
            : null;
        }

        // Create a new browser instance specifically for PDF generation
        const { chromium } = require('playwright');
        const browser = await chromium.launch({ headless: true });

        try {
          for (const audience of audiences) {
            const result = await this.generateSinglePdfReport(
              browser,
              report,
              audience,
              filename,
              {
                format,
                includeBackground,
                margins,
              },
              screenshotPath
            );

            if (this.errorHandler.isSuccess(result)) {
              results.push(result.data);
            } else {
              this.errorHandler.logWarning(`Failed to generate PDF for ${audience.displayName}`, {
                error: result.error,
              });
            }
          }

          this.errorHandler.logSuccess(
            `Generated ${results.length}/${audiences.length} PDF reports`
          );
          return results;
        } finally {
          await browser.close();
        }
      } finally {
        // Clean up screenshot file
        if (screenshotPath) {
          this.fileOps.deleteFile(screenshotPath);
        }
      }
    }, 'generatePdfReports');
  }

  /**
   * Captures a screenshot of the main page
   */
  private async captureMainPageScreenshot(siteUrl: string): Promise<ServiceResult<string>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      this.errorHandler.logInfo('Capturing main page screenshot for PDF reports');

      // Generate unique filename for the screenshot
      const timestamp = Date.now();
      const screenshotFilename = `main-page-screenshot-${timestamp}.png`;
      const screenshotPath = require('path').join(process.cwd(), screenshotFilename);

      try {
        // Navigate to the main page if not already there
        const currentUrl = this.page.url();
        if (currentUrl !== siteUrl) {
          await this.page.goto(siteUrl, { waitUntil: 'networkidle', timeout: 30000 });
        }

        // Wait for page to be ready
        await this.page.waitForLoadState('networkidle');
        await this.page.waitForTimeout(1000);

        // Capture screenshot with optimized settings for PDF inclusion
        await this.page.screenshot({
          path: screenshotPath,
          fullPage: false, // Capture only the viewport for better PDF layout
          type: 'png',
          timeout: 10000,
          clip: {
            x: 0,
            y: 0,
            width: 1200, // Fixed width for consistent PDF layout
            height: 800, // Fixed height for consistent PDF layout
          },
        });

        this.errorHandler.logSuccess(`Screenshot captured: ${screenshotPath}`);
        return screenshotPath;
      } catch (error) {
        this.errorHandler.logWarning('Failed to capture screenshot, continuing without it', {
          error,
        });
        return '';
      }
    }, 'captureMainPageScreenshot');
  }

  /**
   * Generates a single PDF report for a specific audience
   */
  private async generateSinglePdfReport(
    browser: import('playwright').Browser,
    report: SiteWideAccessibilityReport,
    audience: { name: string; displayName: string },
    baseFilename: string,
    pdfOptions: {
      format: string;
      includeBackground: boolean;
      margins: { top: string; right: string; bottom: string; left: string };
    },
    screenshotPath: string | null = null
  ): Promise<ServiceResult<PdfGenerationResult>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      const pdfPage = await browser.newPage();

      try {
        // Generate HTML content with screenshot
        const htmlContent = this.templateGenerator.generateAudienceSpecificTemplate(
          report,
          audience.name,
          audience.displayName,
          screenshotPath
        );

        // Create temporary HTML file
        const tempHtmlPath = await this.createTemporaryHtmlFile(htmlContent, audience.name);

        try {
          // Navigate to the HTML file
          await pdfPage.goto(`file://${tempHtmlPath}`);

          // Wait for any dynamic content to load
          await pdfPage.waitForTimeout(2000);

          // Generate PDF
          const pdfPath = this.generatePdfFilePath(baseFilename, audience.name);

          await pdfPage.pdf({
            path: pdfPath,
            format: pdfOptions.format,
            printBackground: pdfOptions.includeBackground,
            margin: pdfOptions.margins,
          });

          // Get file size
          const stats = require('fs').statSync(pdfPath);
          const sizeKB = Math.round(stats.size / 1024);

          this.errorHandler.logSuccess(`PDF generated: ${pdfPath} (${sizeKB}KB)`);

          return {
            filePath: pdfPath,
            audience: audience.name,
            displayName: audience.displayName,
            sizeKB,
          };
        } finally {
          // Clean up temporary HTML file
          this.fileOps.deleteFile(tempHtmlPath);
        }
      } finally {
        await pdfPage.close();
      }
    }, `generateSinglePdfReport-${audience.name}`);
  }

  /**
   * Creates a temporary HTML file for PDF generation
   */
  private async createTemporaryHtmlFile(content: string, audience: string): Promise<string> {
    const tempFilename = `temp-${audience}-report-${Date.now()}.html`;
    const tempPath = require('path').join(process.cwd(), tempFilename);

    const result = this.fileOps.writeFile(tempPath, content);

    if (!result.success) {
      throw new Error(`Failed to create temporary HTML file: ${result.message}`);
    }

    return tempPath;
  }

  /**
   * Generates the PDF file path
   */
  private generatePdfFilePath(baseFilename: string, audience: string): string {
    const reportsDir = this.fileOps.getReportsDirectory();
    return require('path').join(reportsDir, `${baseFilename}-${audience}.pdf`);
  }

  /**
   * Generates default filename from report
   */
  private generateDefaultFilename(report: SiteWideAccessibilityReport): string {
    try {
      const url = new URL(report.siteUrl);
      return this.fileOps.generateUserFriendlyFilename(url.href);
    } catch {
      return this.fileOps.generateUniqueFilename('accessibility-report', 'pdf').replace('.pdf', '');
    }
  }

  /**
   * Gets default audiences for PDF generation
   */
  private getDefaultAudiences(): Array<{ name: string; displayName: string }> {
    return [
      { name: 'stakeholders', displayName: 'Product Owners & Stakeholders' },
      { name: 'researchers', displayName: 'User Researchers & UCD' },
      { name: 'developers', displayName: 'Developers & Testers' },
    ];
  }

  /**
   * Generates a single PDF for a specific audience with custom options
   */
  async generateCustomPdf(
    report: SiteWideAccessibilityReport,
    audience: { name: string; displayName: string },
    filename: string,
    customOptions: Partial<PdfGenerationOptions> = {}
  ): Promise<ServiceResult<PdfGenerationResult>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      const options: PdfGenerationOptions = {
        audiences: [audience],
        filename,
        format: 'A4',
        includeBackground: true,
        includeScreenshot: true,
        margins: {
          top: '0.75in',
          right: '0.75in',
          bottom: '0.75in',
          left: '0.75in',
        },
        ...customOptions,
      };

      const results = await this.generatePdfReports(report, options);

      if (this.errorHandler.isError(results)) {
        throw new Error(results.error);
      }

      if (results.data.length === 0) {
        throw new Error('No PDF was generated');
      }

      return results.data[0];
    }, 'generateCustomPdf');
  }

  /**
   * Cleans up any temporary files
   */
  async cleanup(): Promise<void> {
    try {
      const tempFiles = require('fs')
        .readdirSync(process.cwd())
        .filter((file: string) => file.startsWith('temp-') && file.endsWith('.html'));

      for (const file of tempFiles) {
        this.fileOps.deleteFile(file);
      }

      this.errorHandler.logInfo(`Cleaned up ${tempFiles.length} temporary files`);
    } catch (_error) {
      this.errorHandler.logWarning('Failed to cleanup temporary files', { error: _error });
    }
  }

  /**
   * Validates PDF generation options
   */
  validateOptions(options: PdfGenerationOptions): ServiceResult<void> {
    return this.errorHandler.executeWithErrorHandlingSync(() => {
      if (options.audiences && options.audiences.length === 0) {
        throw new Error('At least one audience must be specified');
      }

      if (options.format && !['A4', 'Letter'].includes(options.format)) {
        throw new Error('Format must be either A4 or Letter');
      }

      if (options.margins) {
        const { top, right, bottom, left } = options.margins;
        if (!top || !right || !bottom || !left) {
          throw new Error('All margin values must be specified');
        }
      }

      return undefined;
    }, 'validateOptions');
  }
}
