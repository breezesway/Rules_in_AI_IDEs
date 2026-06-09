import { existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync } from 'fs';
import path from 'path';

export interface CachedPageList {
  siteUrl: string;
  timestamp: string;
  crawlOptions: {
    maxPages: number;
    maxDepth: number;
    delayBetweenRequests: number;
  };
  pages: Array<{
    url: string;
    title: string;
    status: number;
    depth: number;
    foundOn: string;
  }>;
  excludedPages?: Array<{
    url: string;
    title: string;
    status: number;
    depth: number;
    foundOn: string;
  }>;
  summary: {
    totalPages: number;
    pagesByDepth: Record<number, number>;
    crawlDuration: number;
    excludedPages?: number;
  };
}

export class PageListCache {
  private static readonly CACHE_DIR = path.join(
    process.cwd(),
    'accessibility-reports',
    'page-cache'
  );
  private static readonly CACHE_FILE = path.join(PageListCache.CACHE_DIR, 'page-list.json');

  static ensureCacheDir(): void {
    if (!existsSync(PageListCache.CACHE_DIR)) {
      mkdirSync(PageListCache.CACHE_DIR, { recursive: true });
    }
  }

  static savePageList(cachedPageList: CachedPageList): void {
    console.log('💾 Saving page list to cache...');
    PageListCache.ensureCacheDir();
    writeFileSync(PageListCache.CACHE_FILE, JSON.stringify(cachedPageList, null, 2));
    console.log(`✅ Page list cached: ${cachedPageList.pages.length} pages saved`);
  }

  static loadPageList(targetUrl?: string): CachedPageList | null {
    if (!existsSync(PageListCache.CACHE_FILE)) {
      console.log('⚠️  No cached page list found');
      return null;
    }

    try {
      const cached = JSON.parse(readFileSync(PageListCache.CACHE_FILE, 'utf8'));

      // Validate that cached URL matches target URL if provided
      if (targetUrl && cached.siteUrl) {
        const normalizeUrl = (url: string): string => {
          // Remove trailing slashes and normalize protocol
          return url
            .replace(/\/+$/, '')
            .replace(/^https?:\/\//, '')
            .toLowerCase();
        };

        const cachedUrlNormalized = normalizeUrl(cached.siteUrl);
        const targetUrlNormalized = normalizeUrl(targetUrl);

        if (cachedUrlNormalized !== targetUrlNormalized) {
          console.log(`❌ Cache URL mismatch:`);
          console.log(`   📋 Cached:  ${cached.siteUrl}`);
          console.log(`   🎯 Target:  ${targetUrl}`);
          console.log(`   🔄 Cache will be regenerated for the new URL`);
          return null;
        }
      }

      console.log(`✅ Loaded cached page list: ${cached.pages.length} pages`);
      console.log(`📅 Cache created: ${new Date(cached.timestamp).toLocaleString()}`);
      if (cached.siteUrl) {
        console.log(`🌐 Site URL: ${cached.siteUrl}`);
      }
      return cached;
    } catch (error) {
      console.warn('⚠️  Failed to load cached page list:', error);
      return null;
    }
  }

  static isCacheValid(maxAgeMinutes: number = 60, targetUrl?: string): boolean {
    const cached = PageListCache.loadPageList(targetUrl);
    if (!cached) return false;

    const cacheAge = Date.now() - new Date(cached.timestamp).getTime();
    const maxAge = maxAgeMinutes * 60 * 1000;

    const isValid = cacheAge < maxAge;

    if (!isValid) {
      console.log(
        `⏰ Cache expired (${Math.round(cacheAge / 1000 / 60)} minutes old, max ${maxAgeMinutes} minutes)`
      );
    }

    return isValid;
  }

  static clearCache(): void {
    try {
      if (existsSync(PageListCache.CACHE_FILE)) {
        unlinkSync(PageListCache.CACHE_FILE);
        console.log('🗑️  Page list cache cleared');
      }
    } catch (error) {
      console.error('🔥 Failed to clear cache:', error);
    }
  }

  static getCacheInfo(): string {
    if (!existsSync(PageListCache.CACHE_FILE)) {
      return 'No cache found';
    }

    const cached = PageListCache.loadPageList();
    if (!cached) return 'Cache corrupted';

    const age = Math.round((Date.now() - new Date(cached.timestamp).getTime()) / 1000 / 60);
    const excludedCount = cached.excludedPages?.length || 0;
    const activeCount = cached.pages.length;
    const totalCount = activeCount + excludedCount;

    if (excludedCount > 0) {
      return `${totalCount} total pages (${activeCount} active, ${excludedCount} excluded), ${age} minutes old`;
    } else {
      return `${activeCount} pages, ${age} minutes old`;
    }
  }

  /**
   * Get only the active (non-excluded) pages from the cache
   * @returns {Array|null} Array of active pages or null if no cache exists
   */
  static getActivePages(): Array<{
    url: string;
    title: string;
    status: number;
    depth: number;
    foundOn: string;
  }> | null {
    const cached = PageListCache.loadPageList();
    if (!cached) return null;

    // The 'pages' array in cache should already be filtered to exclude excluded pages
    // but we return it explicitly for clarity
    return cached.pages || [];
  }

  /**
   * Get the excluded pages from the cache
   * @returns {Array|null} Array of excluded pages or null if no cache exists
   */
  static getExcludedPages(): Array<{
    url: string;
    title: string;
    status: number;
    depth: number;
    foundOn: string;
  }> | null {
    const cached = PageListCache.loadPageList();
    if (!cached) return null;

    return cached.excludedPages || [];
  }

  /**
   * Get both active and excluded pages from the cache
   * @returns {Object|null} Object with active and excluded pages or null if no cache exists
   */
  static getAllPages(): { active: Array<any>; excluded: Array<any> } | null {
    const cached = PageListCache.loadPageList();
    if (!cached) return null;

    return {
      active: cached.pages || [],
      excluded: cached.excludedPages || [],
    };
  }
}
