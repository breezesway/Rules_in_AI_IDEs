import { expect, test } from '@playwright/test';
import { AccessibilityTestUtils } from './utils/accessibility-helpers';
import { PageListCache } from './utils/page-list-cache';
import { existsSync, mkdirSync, writeFileSync } from 'fs';
import path from 'path';

// Helper function to get viewport information (Chrome-only)
function getViewportInfo(page: any): string {
  const viewport = page.viewportSize();
  if (!viewport) return 'Desktop Chrome (1280x720)';

  const width = viewport.width;
  const height = viewport.height;
  return `Desktop Chrome (${width}x${height})`;
}

test.describe('Pa11y Accessibility Analysis', () => {
  let accessibilityUtils: AccessibilityTestUtils;

  test.beforeEach(async ({ page, browserName }) => {
    accessibilityUtils = new AccessibilityTestUtils(page);

    // Set browser context information
    (page as any).browserName = browserName;
    (page as any).viewportInfo = getViewportInfo(page);
  });

  test('@accessibility @pa11y @parallel Comprehensive Pa11y analysis across all pages', async ({
    page,
    browserName,
  }) => {
    console.log('🔍 Starting comprehensive Pa11y accessibility analysis...');
    console.log(`🌐 Browser: ${browserName}`);
    console.log(`📱 Viewport: ${getViewportInfo(page)}`);

    const startTime = Date.now();

    // Step 1: Load cached page list (pre-crawl should have run first)
    console.log('\n📡 Phase 1: Loading cached page list...');
    const targetSiteUrl = process.env.TARGET_SITE_URL || 'https://nimbleapproach.com';
    const cachedPageList = PageListCache.loadPageList(targetSiteUrl);

    if (!cachedPageList) {
      throw new Error(
        'No cached page list found. Please run pre-crawl first: npm run audit:pre-crawl'
      );
    }

    const pages = cachedPageList.pages;
    console.log(`✅ Using cached page list for Pa11y analysis!`);
    console.log(`📊 Found ${pages.length} pages for Pa11y testing`);
    console.log(`📅 Cache created: ${new Date(cachedPageList.timestamp).toLocaleString()}`);
    console.log(`📈 Pages by depth:`, cachedPageList.summary.pagesByDepth);

    // Validate we found pages
    expect(pages.length).toBeGreaterThan(0);

    // Step 2: Run Pa11y analysis on all pages
    console.log('\n🔍 Phase 2: Running Pa11y analysis on all discovered pages...');

    const pa11yResults = [];
    const urls = pages.map(p => p.url);

    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      console.log(`🔍 Pa11y analysis ${i + 1}/${urls.length}: ${url}`);

      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

        // Run comprehensive Pa11y analysis
        const pa11yResult = await accessibilityUtils.runPa11yAnalysis();

        // Process Pa11y issues for this page
        const processedViolations = await accessibilityUtils.processPa11yIssues(
          pa11yResult.issues || [],
          false // No screenshots in Pa11y analysis for performance
        );

        pa11yResults.push({
          url: url,
          timestamp: new Date().toISOString(),
          browser: browserName,
          viewport: getViewportInfo(page),
          tool: 'pa11y',
          violations: processedViolations,
          rawIssues: pa11yResult.issues?.length || 0,
          summary: {
            totalViolations: processedViolations.length,
            criticalViolations: processedViolations.filter(v => v.impact === 'critical').length,
            seriousViolations: processedViolations.filter(v => v.impact === 'serious').length,
            moderateViolations: processedViolations.filter(v => v.impact === 'moderate').length,
            minorViolations: processedViolations.filter(v => v.impact === 'minor').length,
          },
        });

        console.log(
          `   ✅ Found ${pa11yResult.issues?.length || 0} Pa11y issues (${processedViolations.length} processed)`
        );
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.warn(`   ⚠️ Failed to analyze ${url}:`, errorMessage);
        pa11yResults.push({
          url: url,
          timestamp: new Date().toISOString(),
          browser: browserName,
          viewport: getViewportInfo(page),
          tool: 'pa11y',
          error: errorMessage,
          violations: [],
          rawIssues: 0,
          summary: {
            totalViolations: 0,
            criticalViolations: 0,
            seriousViolations: 0,
            moderateViolations: 0,
            minorViolations: 0,
          },
        });
      }

      // Small delay between pages
      await page.waitForTimeout(1000);
    }

    // Step 3: Save results to shared data file
    console.log('\n💾 Phase 3: Saving Pa11y results...');

    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const outputDir = path.join(
      process.cwd(),
      'playwright',
      'accessibility-reports',
      'parallel-analysis'
    );

    if (!existsSync(outputDir)) {
      mkdirSync(outputDir, { recursive: true });
    }

    const pa11yResultsFile = path.join(outputDir, `pa11y-results-${timestamp}.json`);
    writeFileSync(
      pa11yResultsFile,
      JSON.stringify(
        {
          tool: 'pa11y',
          timestamp,
          browser: browserName,
          viewport: getViewportInfo(page),
          totalPages: pa11yResults.length,
          results: pa11yResults,
          summary: {
            totalViolations: pa11yResults.reduce((sum, r) => sum + r.summary.totalViolations, 0),
            criticalViolations: pa11yResults.reduce(
              (sum, r) => sum + r.summary.criticalViolations,
              0
            ),
            seriousViolations: pa11yResults.reduce(
              (sum, r) => sum + r.summary.seriousViolations,
              0
            ),
            moderateViolations: pa11yResults.reduce(
              (sum, r) => sum + r.summary.moderateViolations,
              0
            ),
            minorViolations: pa11yResults.reduce((sum, r) => sum + r.summary.minorViolations, 0),
            totalRawIssues: pa11yResults.reduce((sum, r) => sum + r.rawIssues, 0),
          },
        },
        null,
        2
      )
    );

    console.log(`✅ Pa11y results saved to: ${pa11yResultsFile}`);

    // Performance summary
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    const avgTimePerPage = Math.round(duration / pa11yResults.length);

    console.log('\n='.repeat(60));
    console.log('PA11Y ANALYSIS SUMMARY');
    console.log('='.repeat(60));
    console.log(`🔍 Tool: Pa11y`);
    console.log(`📊 Pages Analyzed: ${pa11yResults.length}`);
    console.log(
      `🚨 Total Violations: ${pa11yResults.reduce((sum, r) => sum + r.summary.totalViolations, 0)}`
    );
    console.log(`📋 Total Raw Issues: ${pa11yResults.reduce((sum, r) => sum + r.rawIssues, 0)}`);
    console.log(`⏱️  Total Time: ${duration} seconds`);
    console.log(`📈 Average Time per Page: ${avgTimePerPage} seconds`);
    console.log(`💾 Results File: ${pa11yResultsFile}`);
    console.log('='.repeat(60));

    // Validate we got results
    expect(pa11yResults.length).toBeGreaterThan(0);
    expect(pa11yResultsFile).toBeTruthy();

    console.log('✅ Pa11y analysis completed successfully!');
  });
});
