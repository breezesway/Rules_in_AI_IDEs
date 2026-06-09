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

test.describe('Axe-Core Accessibility Analysis', () => {
  let accessibilityUtils: AccessibilityTestUtils;

  test.beforeEach(async ({ page, browserName }) => {
    accessibilityUtils = new AccessibilityTestUtils(page);

    // Set browser context information
    (page as any).browserName = browserName;
    (page as any).viewportInfo = getViewportInfo(page);
  });

  test('@accessibility @axe-core @parallel Comprehensive axe-core analysis across all pages', async ({
    page,
    browserName,
  }) => {
    console.log('🔍 Starting comprehensive axe-core accessibility analysis...');
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
    console.log(`✅ Using cached page list for axe-core analysis!`);
    console.log(`📊 Found ${pages.length} pages for axe-core testing`);
    console.log(`📅 Cache created: ${new Date(cachedPageList.timestamp).toLocaleString()}`);
    console.log(`📈 Pages by depth:`, cachedPageList.summary.pagesByDepth);

    // Validate we found pages
    expect(pages.length).toBeGreaterThan(0);

    // Step 2: Run axe-core analysis on all pages
    console.log('\n🔍 Phase 2: Running axe-core analysis on all discovered pages...');

    const axeResults = [];
    const urls = pages.map(p => p.url);

    for (let i = 0; i < urls.length; i++) {
      const url = urls[i];
      console.log(`🔍 Axe-core analysis ${i + 1}/${urls.length}: ${url}`);

      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

        // Run comprehensive axe-core analysis
        const axeResult = await accessibilityUtils.runAxeAnalysis({
          tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa', 'best-practice', 'experimental'],
        });

        // Process violations for this page
        const processedViolations = await accessibilityUtils.processViolations(
          axeResult.violations,
          false // No screenshots in axe-core analysis for performance
        );

        axeResults.push({
          url: url,
          timestamp: new Date().toISOString(),
          browser: browserName,
          viewport: getViewportInfo(page),
          tool: 'axe-core',
          violations: processedViolations,
          summary: {
            totalViolations: processedViolations.length,
            criticalViolations: processedViolations.filter(v => v.impact === 'critical').length,
            seriousViolations: processedViolations.filter(v => v.impact === 'serious').length,
            moderateViolations: processedViolations.filter(v => v.impact === 'moderate').length,
            minorViolations: processedViolations.filter(v => v.impact === 'minor').length,
          },
        });

        console.log(`   ✅ Found ${processedViolations.length} axe-core violations`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.warn(`   ⚠️ Failed to analyze ${url}:`, errorMessage);
        axeResults.push({
          url: url,
          timestamp: new Date().toISOString(),
          browser: browserName,
          viewport: getViewportInfo(page),
          tool: 'axe-core',
          error: errorMessage,
          violations: [],
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
    console.log('\n💾 Phase 3: Saving axe-core results...');

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

    const axeResultsFile = path.join(outputDir, `axe-core-results-${timestamp}.json`);
    writeFileSync(
      axeResultsFile,
      JSON.stringify(
        {
          tool: 'axe-core',
          timestamp,
          browser: browserName,
          viewport: getViewportInfo(page),
          totalPages: axeResults.length,
          results: axeResults,
          summary: {
            totalViolations: axeResults.reduce((sum, r) => sum + r.summary.totalViolations, 0),
            criticalViolations: axeResults.reduce(
              (sum, r) => sum + r.summary.criticalViolations,
              0
            ),
            seriousViolations: axeResults.reduce((sum, r) => sum + r.summary.seriousViolations, 0),
            moderateViolations: axeResults.reduce(
              (sum, r) => sum + r.summary.moderateViolations,
              0
            ),
            minorViolations: axeResults.reduce((sum, r) => sum + r.summary.minorViolations, 0),
          },
        },
        null,
        2
      )
    );

    console.log(`✅ Axe-core results saved to: ${axeResultsFile}`);

    // Performance summary
    const endTime = Date.now();
    const duration = Math.round((endTime - startTime) / 1000);
    const avgTimePerPage = Math.round(duration / axeResults.length);

    console.log('\n='.repeat(60));
    console.log('AXE-CORE ANALYSIS SUMMARY');
    console.log('='.repeat(60));
    console.log(`🔍 Tool: axe-core`);
    console.log(`📊 Pages Analyzed: ${axeResults.length}`);
    console.log(
      `🚨 Total Violations: ${axeResults.reduce((sum, r) => sum + r.summary.totalViolations, 0)}`
    );
    console.log(`⏱️  Total Time: ${duration} seconds`);
    console.log(`📈 Average Time per Page: ${avgTimePerPage} seconds`);
    console.log(`💾 Results File: ${axeResultsFile}`);
    console.log('='.repeat(60));

    // Validate we got results
    expect(axeResults.length).toBeGreaterThan(0);
    expect(axeResultsFile).toBeTruthy();

    console.log('✅ Axe-core analysis completed successfully!');
  });
});
