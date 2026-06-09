import { expect, test } from '@playwright/test';
import { SiteCrawler } from './utils/site-crawler';
import { CachedPageList, PageListCache } from './utils/page-list-cache';

// Debug logging utility
const debugLog = (message: string, data?: any) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`, data ? JSON.stringify(data, null, 2) : '');
};

// Performance monitoring utility
const performanceMonitor = {
  start: (operation: string) => {
    const startTime = Date.now();
    debugLog(`🚀 Starting ${operation}`);
    return {
      end: () => {
        const duration = Date.now() - startTime;
        debugLog(`✅ Completed ${operation} in ${duration}ms`);
        return duration;
      },
    };
  },
};

// Helper function to get viewport information (Chrome-only)
function getViewportInfo(page: any): string {
  const viewport = page.viewportSize();
  if (!viewport) return 'Desktop Chrome (1280x720)';

  const width = viewport.width;
  const height = viewport.height;
  return `Desktop Chrome (${width}x${height})`;
}

// Memory usage monitoring
const logMemoryUsage = (context: string) => {
  if (typeof process !== 'undefined' && process.memoryUsage) {
    const usage = process.memoryUsage();
    const formatBytes = (bytes: number) => Math.round(bytes / 1024 / 1024) + 'MB';
    debugLog(`🧠 Memory usage (${context}):`, {
      rss: formatBytes(usage.rss),
      heapTotal: formatBytes(usage.heapTotal),
      heapUsed: formatBytes(usage.heapUsed),
      external: formatBytes(usage.external),
    });
  }
};

test.describe('Pre-crawl Site Discovery', () => {
  test.beforeEach(async ({ page, browserName }) => {
    debugLog('🔧 Test setup starting', { browserName });
    logMemoryUsage('test-setup');

    // Set browser context information
    (page as any).browserName = browserName;
    (page as any).viewportInfo = getViewportInfo(page);

    // Add page error listeners for debugging
    page.on('pageerror', (error) => {
      debugLog('🚨 Page error detected', { error: error.message });
    });

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        const message = msg.text();

        // Filter out resource loading errors (404s for images, CSS, JS, etc.)
        const isResourceError = message.includes('Failed to load resource') ||
          message.includes('404') ||
          message.includes('net::ERR_ABORTED') ||
          message.includes('net::ERR_FAILED');

        // Only log actual JavaScript errors that might affect accessibility
        if (!isResourceError) {
          debugLog('🚨 Console error detected', { message });
        }
      }
    });

    debugLog('✅ Test setup completed');
  });

  test('@pre-crawl @setup Discover all pages on the site and cache for parallel tests', async ({
    page,
    browserName,
  }) => {
    const testMonitor = performanceMonitor.start('Pre-crawl Site Discovery');

    try {
      console.log('🕷️  Starting enhanced site discovery and caching...');
      console.log(`🌐 Browser: ${browserName}`);
      console.log(`📱 Viewport: ${getViewportInfo(page)}`);

      logMemoryUsage('pre-crawl-start');

      // Only run pre-crawl on chromium to avoid duplicate work
      if (browserName !== 'chromium') {
        debugLog('⏭️  Skipping pre-crawl for non-chromium browser');
        console.log('⏭️  Skipping pre-crawl for non-chromium browser (using chromium results)');
        return;
      }

      // Check if we already have a valid cache
      const cacheCheckMonitor = performanceMonitor.start('Cache validation');
      const cacheValid = PageListCache.isCacheValid(60); // 60 minutes cache
      cacheCheckMonitor.end();

      if (cacheValid) {
        console.log('✅ Valid page cache found, skipping crawl');
        console.log(`📊 Cache info: ${PageListCache.getCacheInfo()}`);
        debugLog('✅ Using existing cache, skipping crawl');
        return;
      }

      const startTime = Date.now();
      const targetSiteUrl = process.env.TARGET_SITE_URL || 'https://nimbleapproach.com';
      const siteCrawler = new SiteCrawler(page, targetSiteUrl);

      console.log('\n📡 Phase 1: Discovering all pages on the site...');
      debugLog('📡 Starting site crawl phase');

      // Universal crawl options that work for any website
      const crawlOptions = {
        maxPages: parseInt(process.env.MAX_PAGES || '50'),
        maxDepth: parseInt(process.env.MAX_DEPTH || '4'),
        delayBetweenRequests: parseInt(process.env.DELAY_BETWEEN_REQUESTS || '300'),
        maxRetries: parseInt(process.env.MAX_RETRIES || '3'),
        retryDelay: parseInt(process.env.RETRY_DELAY || '1500'),
        timeoutMs: parseInt(process.env.PAGE_TIMEOUT || '20000'),
        excludePatterns: [
          // Universal patterns that should be excluded from any website
          /\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z)$/i, // Documents
          /\.(jpg|jpeg|png|gif|svg|webp|ico|bmp|tiff)$/i, // Images
          /\.(mp4|avi|mov|wmv|flv|webm|mkv|mp3|wav|ogg)$/i, // Media files
          /\.(css|js|json|xml|txt|csv)$/i, // Static resources
          /\/wp-admin\//i, // WordPress admin
          /\/admin\//i, // Generic admin
          /\/login\//i, // Login pages
          /\/logout\//i, // Logout pages
          /\/signin\//i, // Sign in pages
          /\/signup\//i, // Sign up pages
          /\/register\//i, // Registration pages
          /\/search\?/i, // Search results
          /\/cart\//i, // Shopping cart
          /\/checkout\//i, // Checkout process
          /\/payment\//i, // Payment pages
          /\/api\//i, // API endpoints
          /\/feed\//i, // RSS/Atom feeds
          /\/feeds\//i, // RSS/Atom feeds
          /\/rss\//i, // RSS feeds
          /\/sitemap/i, // Sitemap files
          /\/robots\.txt$/i, // Robots.txt
          /\?.*utm_/i, // UTM tracking parameters
          /\?.*fbclid/i, // Facebook tracking
          /\?.*gclid/i, // Google tracking
          /#/i, // URL fragments
          /mailto:/i, // Email links
          /tel:/i, // Phone links
          /ftp:/i, // FTP links
          /javascript:/i, // JavaScript links
          /\/\d{4}\/\d{2}\/\d{2}\//i, // Date-based URLs (often paginated)
          /\/page\/\d+/i, // Pagination
          /\/p\/\d+/i, // Alternative pagination
          /\?page=/i, // Query-based pagination
          /\?p=/i, // Query-based pagination
        ],
      };

      debugLog('🔧 Universal crawl options configured', crawlOptions);
      logMemoryUsage('pre-crawl');

      const crawlMonitor = performanceMonitor.start('Site crawling');
      const pages = await siteCrawler.crawlSite(crawlOptions);
      crawlMonitor.end();

      const crawlSummary = siteCrawler.getSummary();
      const crawlErrors = siteCrawler.getErrors();

      console.log(`✅ Site crawl completed!`);
      console.log(`📊 Found ${pages.length} pages`);
      console.log(`📈 Enhanced crawl summary:`, crawlSummary);

      debugLog('📊 Detailed crawl results', {
        totalPages: pages.length,
        summary: crawlSummary,
        errors: crawlErrors,
      });

      // Log detailed error information
      if (crawlErrors.length > 0) {
        console.log('⚠️  Errors encountered during crawl:');
        crawlErrors.forEach((error, index) => {
          console.log(`   ${index + 1}. ${error.url}: ${error.error} (${error.retryCount} retries)`);
        });
      }

      // Validate we found pages
      expect(pages.length).toBeGreaterThan(0);
      debugLog('✅ Page count validation passed', { count: pages.length });

      // Calculate page distribution by depth
      const pagesByDepth: Record<number, number> = {};
      pages.forEach(page => {
        pagesByDepth[page.depth] = (pagesByDepth[page.depth] || 0) + 1;
      });

      // Memory check after crawling
      logMemoryUsage('post-crawl');

      // Create cache object
      const cacheCreationMonitor = performanceMonitor.start('Cache creation');
      const endTime = Date.now();
      const cachedPageList: CachedPageList = {
        siteUrl: targetSiteUrl,
        timestamp: new Date().toISOString(),
        crawlOptions: {
          maxPages: crawlOptions.maxPages,
          maxDepth: crawlOptions.maxDepth,
          delayBetweenRequests: crawlOptions.delayBetweenRequests,
        },
        pages: pages,
        summary: {
          totalPages: pages.length,
          pagesByDepth: pagesByDepth,
          crawlDuration: endTime - startTime,
        },
      };

      // Save to cache
      PageListCache.savePageList(cachedPageList);
      cacheCreationMonitor.end();

      debugLog('💾 Cache saved successfully', {
        pages: cachedPageList.pages.length,
        duration: cachedPageList.summary.crawlDuration,
      });

      // Performance summary
      const totalDuration = testMonitor.end();
      const duration = Math.round((endTime - startTime) / 1000);

      console.log('\n='.repeat(60));
      console.log('ENHANCED PRE-CRAWL SUMMARY');
      console.log('='.repeat(60));
      console.log(`🕷️  Site: ${targetSiteUrl}`);
      console.log(`📊 Pages Discovered: ${pages.length}`);
      console.log(`📈 Pages by Depth:`);
      Object.entries(pagesByDepth).forEach(([depth, count]) => {
        console.log(`   Depth ${depth}: ${count} pages`);
      });
      console.log(`⏱️  Crawl Duration: ${duration} seconds`);
      console.log(`⚡ Total Test Duration: ${Math.round(totalDuration / 1000)} seconds`);
      console.log(`🎯 Success Rate: ${crawlSummary.performance.successRate.toFixed(1)}%`);
      console.log(`📊 Average Load Time: ${crawlSummary.performance.averageLoadTime}ms`);
      console.log(`🔄 Total Retries: ${crawlSummary.performance.totalRetries}`);
      console.log(`❌ Errors: ${crawlErrors.length}`);
      console.log(`💾 Cache Location: ${PageListCache.getCacheInfo()}`);
      console.log('='.repeat(60));

      // Final memory check
      logMemoryUsage('pre-crawl-complete');

      console.log(
        '✅ Enhanced pre-crawl completed successfully! All parallel tests can now use the cached page list.'
      );

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      debugLog('❌ Pre-crawl test failed', { error: errorMessage, stack: error instanceof Error ? error.stack : undefined });
      logMemoryUsage('pre-crawl-error');
      throw error;
    }
  });

  test.afterEach(async ({ page }) => {
    debugLog('🧹 Test cleanup starting');
    logMemoryUsage('test-cleanup');

    try {
      // Clean up page resources
      await page.close();
      debugLog('✅ Test cleanup completed');
    } catch (error) {
      debugLog('⚠️  Test cleanup warning', { error: error instanceof Error ? error.message : String(error) });
    }
  });
});
