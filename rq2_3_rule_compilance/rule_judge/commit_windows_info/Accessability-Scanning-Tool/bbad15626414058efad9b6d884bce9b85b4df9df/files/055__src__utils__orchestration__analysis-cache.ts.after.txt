import { EventEmitter } from 'events';
import { createHash } from 'crypto';
import {
  AnalysisResult,
  CacheConfig,
  CachedResult,
  CacheMetadata,
  CachePerformance,
} from '@/core/types/common';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

export class AnalysisCache extends EventEmitter {
  private static instance: AnalysisCache;
  private cache: Map<string, CachedResult> = new Map();
  private accessOrder: string[] = []; // For LRU eviction
  private cleanupInterval: NodeJS.Timeout | null = null;
  private hitCount: number = 0;
  private missCount: number = 0;
  private evictionCount: number = 0;
  private config: CacheConfig = {
    maxSize: 1000, // Maximum number of cached entries
    defaultTTL: 3600000, // 1 hour in milliseconds
    cleanupInterval: 300000, // 5 minutes in milliseconds
    compressionEnabled: true,
  };

  private constructor() {
    super();
    this.startCleanupInterval();
  }

  public static getInstance(): AnalysisCache {
    if (!AnalysisCache.instance) {
      AnalysisCache.instance = new AnalysisCache();
    }
    return AnalysisCache.instance;
  }

  public configure(config: Partial<CacheConfig>): void {
    this.config = { ...this.config, ...config };

    // Restart cleanup interval with new timing
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
    }
    this.startCleanupInterval();
  }

  private startCleanupInterval(): void {
    if (this.config.cleanupInterval > 0) {
      this.cleanupInterval = setInterval(() => {
        this.cleanupExpiredEntries();
      }, this.config.cleanupInterval);
    }
  }

  public async getOrAnalyze<T>(
    key: string,
    analysisFunction: () => Promise<T>,
    options: { ttl?: number; forceRefresh?: boolean } = {}
  ): Promise<T> {
    const fullKey = this.generateKey(key);

    // Check for forced refresh
    if (options.forceRefresh) {
      const result = await analysisFunction();
      await this.store(fullKey, result, options.ttl);
      return result;
    }

    // Try to get from cache
    const cached = this.get(fullKey);
    if (cached) {
      this.hitCount++;
      return cached as T;
    }

    // Cache miss - perform analysis
    this.missCount++;

    const startTime = Date.now();
    const result = await analysisFunction();
    const analysisTime = Date.now() - startTime;

    // Store in cache
    await this.store(fullKey, result, options.ttl);

    return result;
  }

  private get(key: string): AnalysisResult | null {
    const cached = this.cache.get(key);
    if (!cached) {
      return null;
    }

    // Check if expired using ttl
    if (Date.now() - cached.timestamp > cached.ttl) {
      this.cache.delete(key);
      this.removeFromAccessOrder(key);
      return null;
    }

    // Update access order for LRU
    this.updateAccessOrder(key);

    return cached.result;
  }

  private async store(key: string, result: any, ttl?: number): Promise<void> {
    const resultTTL = ttl || this.config.defaultTTL;

    // Create metadata to satisfy interface
    const metadata: CacheMetadata = {
      size: Buffer.byteLength(JSON.stringify(result), 'utf8'),
      accessCount: 1,
      lastAccessed: new Date(),
      cacheKey: key,
      domain: 'unknown',
    };

    const cachedResult: CachedResult = {
      result: result,
      timestamp: Date.now(),
      ttl: resultTTL,
      url: key, // Use key as URL for simplicity
      hash: this.generateKey(JSON.stringify(result)),
      metadata,
    };

    this.cache.set(key, cachedResult);
    this.updateAccessOrder(key);

    // Check if we need to evict entries
    if (this.cache.size > this.config.maxSize) {
      this.evictLRU();
    }
  }

  private updateAccessOrder(key: string): void {
    this.removeFromAccessOrder(key);
    this.accessOrder.push(key);
  }

  private removeFromAccessOrder(key: string): void {
    const index = this.accessOrder.indexOf(key);
    if (index > -1) {
      this.accessOrder.splice(index, 1);
    }
  }

  private evictLRU(): void {
    while (this.cache.size > this.config.maxSize && this.accessOrder.length > 0) {
      const keyToEvict = this.accessOrder.shift();
      if (keyToEvict) {
        this.cache.delete(keyToEvict);
        this.evictionCount++;
      }
    }
  }

  private generateKey(input: string): string {
    return createHash('sha256').update(input).digest('hex');
  }

  private cleanupExpiredEntries(): void {
    const now = Date.now();
    const expiredKeys: string[] = [];

    for (const [key, cached] of this.cache.entries()) {
      if (now - cached.timestamp > cached.ttl) {
        expiredKeys.push(key);
      }
    }

    for (const key of expiredKeys) {
      this.cache.delete(key);
      this.removeFromAccessOrder(key);
    }
  }

  public getPerformance(): CachePerformance {
    const totalRequests = this.hitCount + this.missCount;
    const hitRate = totalRequests > 0 ? (this.hitCount / totalRequests) * 100 : 0;
    const missRate = totalRequests > 0 ? (this.missCount / totalRequests) * 100 : 0;

    // Return minimal performance data to match interface
    return {
      hitRate,
      missRate,
      evictionRate: totalRequests > 0 ? this.evictionCount / totalRequests : 0,
      memoryUsage: this.getMemoryUsage(),
      entryCount: this.cache.size,
    };
  }

  private getMemoryUsage(): number {
    let totalSize = 0;
    for (const cached of this.cache.values()) {
      totalSize += cached.metadata.size;
    }
    return totalSize;
  }

  public clear(): void {
    this.cache.clear();
    this.accessOrder = [];
    this.hitCount = 0;
    this.missCount = 0;
    this.evictionCount = 0;
    this.emit('cacheCleared');
  }

  public getStats(): {
    size: number;
    hitRate: number;
    missRate: number;
    evictionCount: number;
    memoryUsage: number;
  } {
    const performance = this.getPerformance();
    return {
      size: this.cache.size,
      hitRate: performance.hitRate,
      missRate: performance.missRate,
      evictionCount: this.evictionCount,
      memoryUsage: performance.memoryUsage,
    };
  }

  public delete(key: string): boolean {
    const fullKey = this.generateKey(key);
    const existed = this.cache.delete(fullKey);
    if (existed) {
      this.removeFromAccessOrder(fullKey);
    }
    return existed;
  }

  public has(key: string): boolean {
    const fullKey = this.generateKey(key);
    const cached = this.cache.get(fullKey);

    if (!cached) {
      return false;
    }

    // Check if expired using ttl
    if (Date.now() - cached.timestamp > cached.ttl) {
      this.cache.delete(fullKey);
      this.removeFromAccessOrder(fullKey);
      return false;
    }

    return true;
  }

  public async preWarm(entries: Array<{ key: string; data: any; ttl?: number }>): Promise<void> {
    for (const entry of entries) {
      await this.store(this.generateKey(entry.key), entry.data, entry.ttl);
    }
  }

  public async invalidatePattern(pattern: string): Promise<string[]> {
    const regex = new RegExp(pattern);
    const keysToDelete: string[] = [];

    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        keysToDelete.push(key);
      }
    }

    for (const key of keysToDelete) {
      this.cache.delete(key);
      this.removeFromAccessOrder(key);
    }

    return keysToDelete;
  }

  public async exportCache(): Promise<any> {
    const exported: any = {};

    for (const [key, cached] of this.cache.entries()) {
      exported[key] = {
        result: cached.result,
        timestamp: cached.timestamp,
        ttl: cached.ttl,
        url: cached.url,
        hash: cached.hash,
        metadata: cached.metadata,
      };
    }

    return exported;
  }

  public async importCache(data: any): Promise<void> {
    this.clear();

    for (const [key, cached] of Object.entries(data)) {
      this.cache.set(key, cached as CachedResult);
      this.updateAccessOrder(key);
    }
  }

  public shutdown(): void {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
    this.clear();
    this.removeAllListeners();
  }
}
