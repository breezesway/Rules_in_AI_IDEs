import { expect, test } from '@playwright/test';
import { AccessibilityTestUtils } from './utils/accessibility-helpers';
import { existsSync, readdirSync, readFileSync } from 'fs';
import path from 'path';

// Helper function to get viewport information (Chrome-only)
function getViewportInfo(page: any): string {
  const viewport = page.viewportSize();
  if (!viewport) return 'Desktop Chrome (1280x720)';

  const width = viewport.width;
  const height = viewport.height;
  return `Desktop Chrome (${width}x${height})`;
}

/**
 * Creates a clickable terminal link using ANSI escape codes
 * @param text - The text to display
 * @param url - The URL or file path to link to
 * @param color - The color to apply to the link (default: magenta)
 * @returns Formatted clickable link
 */
function createClickableLink(text: string, url: string, color: string = '\x1b[35m'): string {
  const reset = '\x1b[0m';
  // Convert file path to file:// URL for better compatibility
  const linkUrl = url.startsWith('/') ? `file://${url}` : url;

  // OSC 8 hyperlink format: \x1b]8;;URL\x1b\\TEXT\x1b]8;;\x1b\\
  return `${color}\x1b]8;;${linkUrl}\x1b\\${text}\x1b]8;;\x1b\\${reset}`;
}

// Helper function to merge violations from multiple tools
function mergeViolationsFromMultipleTools(violations: any[]): any[] {
  const violationMap = new Map<string, any>();

  violations.forEach(violation => {
    if (violationMap.has(violation.id)) {
      const existing = violationMap.get(violation.id)!;
      // Merge tools
      existing.tools = [...new Set([...existing.tools, ...violation.tools])];
      // Merge elements
      existing.elements.push(...violation.elements);
      // Update occurrences
      existing.occurrences += violation.occurrences;
    } else {
      violationMap.set(violation.id, violation);
    }
  });

  return Array.from(violationMap.values());
}

test.describe('Comprehensive Accessibility Reporting', () => {
  let accessibilityUtils: AccessibilityTestUtils;

  test.beforeEach(async ({ page, browserName }) => {
    accessibilityUtils = new AccessibilityTestUtils(page);

    // Set browser context information
    (page as any).browserName = browserName;
    (page as any).viewportInfo = getViewportInfo(page);
  });

  test('@accessibility @reporting @parallel Combine all parallel analysis results into comprehensive reports', async ({
    page,
    browserName,
  }) => {
    console.log('📄 Starting comprehensive accessibility reporting...');
    console.log(`🌐 Browser: ${browserName}`);
    console.log(`📱 Viewport: ${getViewportInfo(page)}`);

    const startTime = Date.now();

    // Step 1: Wait for all parallel analysis to complete and find result files
    console.log('\n📡 Phase 1: Locating parallel analysis results...');
    const resultsDir = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      'parallel-analysis'
    );

    if (!existsSync(resultsDir)) {
      console.log(
        '⚠️  No parallel analysis results found. Please run the parallel analysis tests first.'
      );
      console.log('Run: npm test -- --grep "@parallel"');
      return;
    }

    // Find the latest result files
    const files = readdirSync(resultsDir).filter(f => f.endsWith('.json'));
    const axeResultFile = files.find(f => f.startsWith('axe-core-results-'));
    const pa11yResultFile = files.find(f => f.startsWith('pa11y-results-'));
    const visualResultFile = files.find(f => f.startsWith('visual-results-'));

    console.log(`📊 Found analysis files:`);
    console.log(`   🔍 Axe-core: ${axeResultFile || 'Not found'}`);
    console.log(`   🔍 Pa11y: ${pa11yResultFile || 'Not found'}`);
    console.log(`   📸 Visual: ${visualResultFile || 'Not found'}`);

    if (!axeResultFile && !pa11yResultFile && !visualResultFile) {
      console.log(
        '❌ No analysis result files found. Please run the parallel analysis tests first.'
      );
      return;
    }

    // Step 2: Load and combine all results
    console.log('\n🔄 Phase 2: Loading and combining analysis results...');

    let axeResults: any[] | null = null;
    let pa11yResults: any[] | null = null;
    let visualResults: any[] | null = null;

    if (axeResultFile) {
      try {
        const axeData = JSON.parse(readFileSync(path.join(resultsDir, axeResultFile), 'utf8'));
        axeResults = axeData.results;
        console.log(`✅ Loaded ${axeResults?.length || 0} axe-core results`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.warn(`⚠️ Failed to load axe-core results:`, errorMessage);
      }
    }

    if (pa11yResultFile) {
      try {
        const pa11yData = JSON.parse(readFileSync(path.join(resultsDir, pa11yResultFile), 'utf8'));
        pa11yResults = pa11yData.results;
        console.log(`✅ Loaded ${pa11yResults?.length || 0} Pa11y results`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.warn(`⚠️ Failed to load Pa11y results:`, errorMessage);
      }
    }

    if (visualResultFile) {
      try {
        const visualData = JSON.parse(
          readFileSync(path.join(resultsDir, visualResultFile), 'utf8')
        );
        visualResults = visualData.results;
        console.log(`✅ Loaded ${visualResults?.length || 0} visual analysis results`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.warn(`⚠️ Failed to load visual analysis results:`, errorMessage);
      }
    }

    // Step 3: Merge results into comprehensive reports
    console.log('\n🔄 Phase 3: Merging results into comprehensive accessibility reports...');

    // Create combined reports structure
    const combinedReports: any[] = [];
    const allUrls = new Set<string>();

    // Collect all unique URLs
    if (axeResults) axeResults.forEach(r => allUrls.add(r.url));
    if (pa11yResults) pa11yResults.forEach(r => allUrls.add(r.url));
    if (visualResults) visualResults.forEach(r => allUrls.add(r.url));

    for (const url of allUrls) {
      const axeResult = axeResults?.find(r => r.url === url);
      const pa11yResult = pa11yResults?.find(r => r.url === url);
      const visualResult = visualResults?.find(r => r.url === url);

      // Combine all violations from all tools
      const allViolations: any[] = [];
      const toolsUsed: string[] = [];

      if (axeResult?.violations) {
        allViolations.push(...axeResult.violations);
        toolsUsed.push('axe-core');
      }

      if (pa11yResult?.violations) {
        allViolations.push(...pa11yResult.violations);
        toolsUsed.push('pa11y');
      }

      if (visualResult?.colorContrastViolations) {
        allViolations.push(...visualResult.colorContrastViolations);
        toolsUsed.push('visual-analysis');
      }

      // Merge violations with same ID from different tools
      const mergedViolations = mergeViolationsFromMultipleTools(allViolations);

      // Create page analysis info
      const pageAnalysis = {
        title: visualResult?.pageInfo?.title || axeResult?.pageInfo?.title || 'Unknown',
        description: visualResult?.pageInfo?.description || '',
        language: visualResult?.pageInfo?.language || 'en',
        screenshot: visualResult?.screenshot || null,
        totalElements: visualResult?.visualElements?.length || 0,
        missingAltText: visualResult?.summary?.missingAltText || 0,
        potentialContrastIssues: visualResult?.summary?.potentialContrastIssues || 0,
        toolsUsed,
      };

      // Create comprehensive report for this page
      const comprehensiveReport = {
        url,
        timestamp: new Date().toISOString(),
        testSuite: 'Comprehensive Parallel Accessibility Analysis',
        browser: browserName,
        viewport: getViewportInfo(page),
        summary: {
          totalViolations: mergedViolations.length,
          criticalViolations: mergedViolations.filter(v => v.impact === 'critical').length,
          seriousViolations: mergedViolations.filter(v => v.impact === 'serious').length,
          moderateViolations: mergedViolations.filter(v => v.impact === 'moderate').length,
          minorViolations: mergedViolations.filter(v => v.impact === 'minor').length,
          compliancePercentage:
            mergedViolations.length === 0 ? 100 : Math.max(0, 100 - mergedViolations.length * 10),
        },
        violations: mergedViolations,
        pageAnalysis,
        toolsUsed,
        rawResults: {
          axe: axeResult || null,
          pa11y: pa11yResult || null,
          visual: visualResult || null,
        },
      };

      combinedReports.push(comprehensiveReport);
    }

    const allToolsUsed = Array.from(new Set(combinedReports.flatMap(r => r.toolsUsed)));
    console.log(
      `✅ Combined ${combinedReports.length} page reports from ${allToolsUsed.length} analysis tools`
    );

    // Step 4: Generate comprehensive reports using existing utilities
    console.log('\n📄 Phase 4: Generating comprehensive accessibility reports...');

    // Generate user-friendly filename
    const siteUrl = combinedReports.length > 0 ? combinedReports[0].url : 'unknown-site';
    const domain = siteUrl
      .replace(/^https?:\/\//, '')
      .replace(/^www\./, '')
      .split('/')[0]
      .replace(/[^a-z0-9]/gi, '-');
    const date = new Date().toLocaleDateString('en-GB').replace(/\//g, '-');
    const time = new Date()
      .toLocaleTimeString('en-GB', { hour12: false, hour: '2-digit', minute: '2-digit' })
      .replace(/:/g, '-');
    const filename = `${domain}-accessibility-report-${date}-${time}`;

    console.log(`📄 Creating report: ${filename}`);

    // Use existing report generation utilities
    await accessibilityUtils.generateSiteWideReport(combinedReports, filename, true);

    // Step 5: Generate detailed analysis summary
    const aggregatedReport = accessibilityUtils.aggregateReports(combinedReports);

    console.log(`\n${'='.repeat(80)}`);
    console.log('COMPREHENSIVE PARALLEL ACCESSIBILITY AUDIT RESULTS');
    console.log('='.repeat(80));
    console.log(`🌐 Site: ${aggregatedReport.siteUrl}`);
    console.log(`📊 Pages Tested: ${aggregatedReport.summary.totalPages}`);
    console.log(`🎯 Overall Compliance: ${aggregatedReport.summary.compliancePercentage}%`);
    console.log(`📈 Total Violations: ${aggregatedReport.summary.totalViolations}`);
    console.log(`🚨 Critical Issues: ${aggregatedReport.summary.criticalViolations}`);
    console.log(`⚠️  Serious Issues: ${aggregatedReport.summary.seriousViolations}`);
    console.log(`🔍 Moderate Issues: ${aggregatedReport.summary.moderateViolations}`);
    console.log(`ℹ️  Minor Issues: ${aggregatedReport.summary.minorViolations}`);
    console.log(
      `📋 Pages with Issues: ${aggregatedReport.summary.pagesWithViolations}/${aggregatedReport.summary.totalPages}`
    );
    console.log(
      `🔧 Tools Used: ${Array.from(new Set(combinedReports.flatMap(r => r.toolsUsed))).join(', ')}`
    );
    console.log('='.repeat(80));

    // Show most common violations across the entire site
    if (aggregatedReport.summary.mostCommonViolations.length > 0) {
      console.log('\n🔍 MOST COMMON VIOLATIONS ACROSS ENTIRE SITE:');
      aggregatedReport.summary.mostCommonViolations.forEach((violation, index) => {
        console.log(`${index + 1}. ${violation.id} [${violation.impact.toUpperCase()}]`);
        console.log(
          `   📊 Affects ${violation.affectedPages} pages (${violation.totalOccurrences} total occurrences)`
        );
        console.log(`   📝 ${violation.description}`);

        // Show browser and tools information if available
        const violationData = aggregatedReport.violationsByType[violation.id];
        if (violationData && violationData.browsers && violationData.browsers.length > 0) {
          console.log(`   🌐 Found in browsers: ${violationData.browsers.join(', ')}`);
        }
        if (violationData && violationData.tools && violationData.tools.length > 0) {
          console.log(`   🔧 Detected by tools: ${violationData.tools.join(', ')}`);
        }
        console.log('');
      });
    }

    // Performance and completion summary
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);

    console.log('\n='.repeat(80));
    console.log('PARALLEL AUDIT COMPLETION SUMMARY');
    console.log('='.repeat(80));
    console.log(`⏱️  Total reporting time: ${duration} seconds`);
    console.log(`📊 Combined analysis from multiple parallel workers`);
    const jsonPath = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      `${filename}.json`
    );
    const stakeholdersPath = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      `${filename}-stakeholders.pdf`
    );
    const researchersPath = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      `${filename}-researchers.pdf`
    );
    const developersPath = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      `${filename}-developers.pdf`
    );

    console.log(`📄 Detailed JSON report: ${createClickableLink(`${filename}.json`, jsonPath)}`);
    console.log(`📄 Audience-specific PDF reports (click to open):`);
    console.log(`   ${createClickableLink('📊 Product Owners & Stakeholders', stakeholdersPath)}`);
    console.log(`   ${createClickableLink('🔬 User Researchers & UCD', researchersPath)}`);
    console.log(`   ${createClickableLink('💻 Developers & Testers', developersPath)}`);

    // Recommendations based on results
    console.log('\n💡 RECOMMENDATIONS:');
    if (aggregatedReport.summary.compliancePercentage === 100) {
      console.log('🏆 Excellent! Your website is fully accessible!');
      console.log('🔄 Continue running regular accessibility audits to maintain compliance');
    } else if (aggregatedReport.summary.compliancePercentage >= 80) {
      console.log('👍 Good accessibility compliance with room for improvement');
      console.log('🔧 Focus on fixing the most common violations first');
    } else {
      console.log('🔧 Significant accessibility improvements needed:');
      console.log(
        `🚨 Immediate action required for ${aggregatedReport.summary.criticalViolations} critical violations`
      );
      console.log(
        `⚠️  High priority: ${aggregatedReport.summary.seriousViolations} serious violations`
      );
      console.log('📚 Consider accessibility training for development team');
      console.log('🔄 Implement accessibility testing in CI/CD pipeline');
    }

    console.log('\n🚀 PARALLEL TESTING BENEFITS:');
    console.log('⚡ Faster execution through parallel worker processes');
    console.log('🔧 Specialized analysis by tool type for focused results');
    console.log('📊 Comprehensive coverage from multiple accessibility engines');
    console.log('🎯 Maintained all existing functionality while improving performance');
    console.log('='.repeat(80));

    // Validate we got comprehensive results
    expect(combinedReports.length).toBeGreaterThan(0);
    expect(aggregatedReport.summary.totalPages).toBeGreaterThan(0);

    console.log('✅ Comprehensive accessibility reporting completed successfully!');
  });
});
