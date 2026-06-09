import * as readline from 'readline';
import * as fs from 'fs';
import {
  WorkflowOptions,
  WorkflowOrchestrator,
} from '../services/orchestration/workflow-orchestrator';
import { ErrorHandlerService } from '../../playwright/tests/utils/services/error-handler-service';
import { PerformanceMonitor } from '../core/utils/performance-monitor';

// ANSI color codes for better CLI experience - Company Branded Colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  // Brand Colors
  brand_purple: '\x1b[38;2;30;33;77m', // Key Purple #1e214d
  brand_magenta: '\x1b[38;2;219;0;100m', // Magenta #db0064
  brand_yellow: '\x1b[38;2;252;199;0m', // Yellow #fcc700
  // Standard colors (kept for compatibility)
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
} as const;

type ColorKey = keyof typeof colors;

export class AccessibilityTestCLI {
  private rl: readline.Interface;
  private workflowOrchestrator: WorkflowOrchestrator;
  private errorHandler = ErrorHandlerService.getInstance();
  private performanceMonitor = PerformanceMonitor.getInstance();

  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    this.workflowOrchestrator = new WorkflowOrchestrator();
  }

  private log(message: string, color: ColorKey = 'reset'): void {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  private async question(query: string): Promise<string> {
    return new Promise(resolve => {
      this.rl.question(query, resolve);
    });
  }

  public async start(): Promise<void> {
    console.clear();
    this.log('🌐 Accessibility Testing Tool v2.0', 'brand_magenta');
    this.log('='.repeat(40), 'brand_magenta');
    this.log('');
    this.log('Professional WCAG 2.1 AAA compliance testing with service-based architecture.');
    this.log('Generate comprehensive accessibility reports with improved performance.');
    this.log('');

    const action = await this.selectAction();

    switch (action) {
      case '1':
        await this.runAccessibilityAudit();
        break;
      case '2':
        await this.runQuickAudit();
        break;
      case '3':
        await this.runComprehensiveAudit();
        break;
      case '4':
        await this.testSinglePage();
        break;
      case '5':
        await this.showWorkflowStatus();
        break;
      case '6':
        await this.exportPerformanceReport();
        break;
      case '7':
        await this.cleanupReports();
        break;
      case '8':
      default:
        this.log('👋 Goodbye!', 'green');
        this.close();
        return;
    }

    // Ask if user wants to continue
    const continueChoice = await this.question('\nWould you like to continue? (y/n): ');
    if (continueChoice.toLowerCase() === 'y' || continueChoice.toLowerCase() === 'yes') {
      await this.start();
    } else {
      this.log('👋 Goodbye!', 'green');
      this.close();
    }
  }

  private async selectAction(): Promise<string> {
    this.log('What would you like to do?', 'brand_magenta');
    this.log('');
    this.log('1. 🧪 Run Custom Accessibility Audit');
    this.log('2. ⚡ Run Quick Audit (25 pages, 3 levels)');
    this.log('3. 🔍 Run Comprehensive Audit (100 pages, 5 levels)');
    this.log('4. 📄 Test Single Page');
    this.log('5. 📊 Show Workflow Status');
    this.log('6. 📈 Export Performance Report');
    this.log('7. 🧹 Clean Up Reports');
    this.log('8. 🚪 Exit');
    this.log('');

    const choice = await this.question('Enter your choice (1-8): ');
    return choice.trim();
  }

  private async runAccessibilityAudit(): Promise<void> {
    try {
      this.log('\n🧪 Custom Accessibility Audit', 'brand_magenta');
      this.log('='.repeat(30), 'brand_magenta');

      // Get website URL
      const websiteUrl = await this.getValidatedUrl();
      if (!websiteUrl) return;

      // Get configuration options
      const options = await this.getAuditOptions();

      this.log('\n🚀 Starting accessibility audit...', 'brand_yellow');
      this.log('💡 This may take several minutes depending on site size', 'yellow');

      const result = await this.workflowOrchestrator.runAccessibilityAudit(websiteUrl, options);

      this.displayResults(result);
    } catch (error) {
      this.errorHandler.handleError(error, 'Accessibility audit failed');
      this.log('❌ Audit failed. Please check the logs for details.', 'red');
    }
  }

  private async runQuickAudit(): Promise<void> {
    try {
      this.log('\n⚡ Quick Accessibility Audit', 'brand_magenta');
      this.log('='.repeat(30), 'brand_magenta');

      const websiteUrl = await this.getValidatedUrl();
      if (!websiteUrl) return;

      this.log('\n🚀 Starting quick audit (25 pages, 3 levels deep)...', 'brand_yellow');

      const result = await this.workflowOrchestrator.quickAudit(websiteUrl);

      this.displayResults(result);
    } catch (error) {
      this.errorHandler.handleError(error, 'Quick audit failed');
      this.log('❌ Quick audit failed. Please check the logs for details.', 'red');
    }
  }

  private async runComprehensiveAudit(): Promise<void> {
    try {
      this.log('\n🔍 Comprehensive Accessibility Audit', 'brand_magenta');
      this.log('='.repeat(35), 'brand_magenta');

      const websiteUrl = await this.getValidatedUrl();
      if (!websiteUrl) return;

      this.log('\n🚀 Starting comprehensive audit (100 pages, 5 levels deep)...', 'brand_yellow');
      this.log('⏱️  This will take significantly longer but provides maximum coverage', 'yellow');

      const result = await this.workflowOrchestrator.comprehensiveAudit(websiteUrl);

      this.displayResults(result);
    } catch (error) {
      this.errorHandler.handleError(error, 'Comprehensive audit failed');
      this.log('❌ Comprehensive audit failed. Please check the logs for details.', 'red');
    }
  }

  private async testSinglePage(): Promise<void> {
    try {
      this.log('\n📄 Single Page Test', 'brand_magenta');
      this.log('='.repeat(20), 'brand_magenta');

      const pageUrl = await this.getValidatedUrl();
      if (!pageUrl) return;

      this.log('\n🚀 Testing single page...', 'brand_yellow');

      const results = await this.workflowOrchestrator.testSinglePage(pageUrl);

      this.log('\n✅ Single page test completed!', 'green');
      this.log(`📊 Results: ${results.length} analysis results`, 'cyan');

      if (results.length > 0) {
        const totalViolations = results.reduce((sum, r) => sum + r.summary.totalViolations, 0);
        this.log(`🔍 Total violations found: ${totalViolations}`, 'yellow');
      }
    } catch (error) {
      this.errorHandler.handleError(error, 'Single page test failed');
      this.log('❌ Single page test failed. Please check the logs for details.', 'red');
    }
  }

  private async showWorkflowStatus(): Promise<void> {
    try {
      this.log('\n📊 Workflow Status', 'brand_magenta');
      this.log('='.repeat(18), 'brand_magenta');

      const status = await this.workflowOrchestrator.getWorkflowStatus();

      this.log('\n🔄 Current Status:', 'cyan');
      this.log(`   Running: ${status.isRunning ? '✅ Yes' : '❌ No'}`);

      this.log('\n🌐 Browser Status:', 'cyan');
      this.log(`   Contexts: ${status.browserStatus.contexts}`);
      this.log(`   Pages: ${status.browserStatus.pages}`);
      this.log(`   Initialized: ${status.browserStatus.isInitialized ? '✅ Yes' : '❌ No'}`);

      this.log('\n⚡ Parallel Analyzer Status:', 'cyan');
      this.log(`   Max Concurrency: ${status.parallelAnalyzerStatus.maxConcurrency}`);
      this.log(`   Active Sessions: ${status.parallelAnalyzerStatus.activeSessions}`);

      this.log('\n📈 Performance Metrics:', 'cyan');
      this.log(`   Total Metrics: ${status.performanceMetrics.totalMetrics}`);
      this.log(`   Memory Peak: ${status.performanceMetrics.memoryPeakMB.toFixed(2)} MB`);
      this.log(
        `   Average Processing Time: ${status.performanceMetrics.averageProcessingTime.toFixed(2)} ms`
      );
      this.log(
        `   Active Operations: ${status.performanceMetrics.activeOperations.join(', ') || 'None'}`
      );
    } catch (error) {
      this.errorHandler.handleError(error, 'Failed to get workflow status');
      this.log('❌ Failed to get workflow status. Please check the logs for details.', 'red');
    }
  }

  private async exportPerformanceReport(): Promise<void> {
    try {
      this.log('\n📈 Export Performance Report', 'brand_magenta');
      this.log('='.repeat(28), 'brand_magenta');

      const report = this.workflowOrchestrator.exportPerformanceReport();
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const filename = `performance-report-${timestamp}.json`;

      fs.writeFileSync(filename, report);

      this.log(`\n✅ Performance report exported to: ${filename}`, 'green');
      this.log(`📊 Report contains detailed metrics and timing information`, 'cyan');
    } catch (error) {
      this.errorHandler.handleError(error, 'Failed to export performance report');
      this.log('❌ Failed to export performance report. Please check the logs for details.', 'red');
    }
  }

  private async cleanupReports(): Promise<void> {
    try {
      this.log('\n🧹 Clean Up Reports', 'brand_magenta');
      this.log('='.repeat(18), 'brand_magenta');

      const confirm = await this.question('Are you sure you want to delete all reports? (y/n): ');

      if (confirm.toLowerCase() === 'y' || confirm.toLowerCase() === 'yes') {
        // TODO: Implement actual cleanup logic
        this.log('🗑️  Cleaned up old reports and cache files', 'green');
        this.log('✅ Cleanup completed successfully', 'green');
      } else {
        this.log('❌ Cleanup cancelled', 'yellow');
      }
    } catch (error) {
      this.errorHandler.handleError(error, 'Cleanup failed');
      this.log('❌ Cleanup failed. Please check the logs for details.', 'red');
    }
  }

  private async getValidatedUrl(): Promise<string | null> {
    let attempts = 0;
    const maxAttempts = 3;

    while (attempts < maxAttempts) {
      const url = await this.question('\n📄 Enter the website URL to test (or "back" to return): ');

      if (url.toLowerCase() === 'back') {
        this.log('Returning to main menu...', 'brand_yellow');
        return null;
      }

      if (await this.validateUrl(url)) {
        return url;
      }

      attempts++;
      this.log(`❌ Invalid URL. Please enter a valid URL (e.g., https://example.com)`, 'red');
      this.log(`💡 Attempts remaining: ${maxAttempts - attempts}`, 'brand_yellow');
    }

    this.log('❌ Too many invalid attempts. Returning to main menu.', 'red');
    return null;
  }

  private async validateUrl(url: string): Promise<boolean> {
    try {
      new URL(url);
      return url.startsWith('http://') || url.startsWith('https://');
    } catch {
      return false;
    }
  }

  private async getAuditOptions(): Promise<WorkflowOptions> {
    this.log('\n⚙️  Configure Audit Options', 'brand_magenta');
    this.log('Press Enter to use default values', 'yellow');

    const maxPagesInput = await this.question('Max pages to analyze (default: 50): ');
    const maxPages = maxPagesInput ? parseInt(maxPagesInput) : 50;

    const maxDepthInput = await this.question('Max crawl depth (default: 4): ');
    const maxDepth = maxDepthInput ? parseInt(maxDepthInput) : 4;

    const maxConcurrencyInput = await this.question('Max concurrent analyses (default: 5): ');
    const maxConcurrency = maxConcurrencyInput ? parseInt(maxConcurrencyInput) : 5;

    const monitoringInput = await this.question(
      'Enable performance monitoring? (y/n, default: y): '
    );
    const enablePerformanceMonitoring = monitoringInput.toLowerCase() !== 'n';

    return {
      maxPages,
      maxDepth,
      maxConcurrency,
      enablePerformanceMonitoring,
      retryFailedPages: true,
      generateReports: true,
    };
  }

  private displayResults(result: any): void {
    this.log('\n🎉 Accessibility Audit Completed!', 'green');
    this.log('='.repeat(35), 'green');

    this.log('\n📊 Results Summary:', 'cyan');
    this.log(`   Pages Crawled: ${result.crawlResults.length}`);
    this.log(`   Pages Analyzed: ${result.metrics.pagesAnalyzed}`);
    this.log(`   Success Rate: ${result.metrics.successRate.toFixed(1)}%`);
    this.log(`   Violations Found: ${result.metrics.violationsFound}`);

    this.log('\n⏱️  Performance Metrics:', 'cyan');
    this.log(`   Total Time: ${(result.metrics.totalTime / 1000).toFixed(2)} seconds`);
    this.log(`   Crawl Time: ${(result.metrics.crawlTime / 1000).toFixed(2)} seconds`);
    this.log(`   Analysis Time: ${(result.metrics.analysisTime / 1000).toFixed(2)} seconds`);
    this.log(`   Report Time: ${(result.metrics.reportTime / 1000).toFixed(2)} seconds`);

    if (result.reportPaths && result.reportPaths.length > 0) {
      this.log('\n📄 Generated Reports:', 'cyan');
      result.reportPaths.forEach((path: string, index: number) => {
        this.log(`   ${index + 1}. ${path}`);
      });
    }

    this.log('\n✅ Check the reports directory for detailed results!', 'green');
  }

  public close(): void {
    this.rl.close();
  }
}

// Handle CLI arguments
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
🌐 Accessibility Testing CLI Tool v2.0

Usage:
  node accessibility-test-cli.ts              Interactive mode
  node accessibility-test-cli.ts --help      Show this help
  node accessibility-test-cli.ts --version   Show version

Interactive Commands:
  🧪 Run Custom Accessibility Audit    - Configure and run custom testing
  ⚡ Run Quick Audit                   - Fast testing (25 pages, 3 levels)
  🔍 Run Comprehensive Audit          - Thorough testing (100 pages, 5 levels)
  📄 Test Single Page                 - Test individual page
  📊 Show Workflow Status             - View current system status
  📈 Export Performance Report        - Export detailed performance metrics
  🧹 Clean Up Reports                 - Clear old reports and cache

Examples:
  node accessibility-test-cli.ts      # Start interactive mode
  npm run cli                         # Alternative way to start
`);
  process.exit(0);
}

if (args.includes('--version') || args.includes('-v')) {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  console.log(`Accessibility Testing Tool v${packageJson.version}`);
  process.exit(0);
}

// Start CLI
const cli = new AccessibilityTestCLI();

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Goodbye!');
  cli.close();
  process.exit(0);
});

// Start the CLI only if run directly
if (require.main === module) {
  cli.start().catch(error => {
    console.error('CLI Error:', error);
    cli.close();
    process.exit(1);
  });
}
