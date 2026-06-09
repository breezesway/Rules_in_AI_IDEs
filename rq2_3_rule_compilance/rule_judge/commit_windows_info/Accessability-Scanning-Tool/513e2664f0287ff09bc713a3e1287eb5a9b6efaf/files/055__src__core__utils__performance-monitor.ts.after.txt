import {
  CachePerformance,
  MemoryTrend,
  Metric,
  PerformanceReport,
  ProcessingTimeMetrics,
  SystemHealthMetrics,
  ThroughputMetrics,
  Timer,
  WorkerUtilizationMetrics,
} from '../types/common.js';
import { ErrorHandlerService } from '../../../playwright/tests/utils/services/error-handler-service';
import { EventEmitter } from 'events';
import * as os from 'os';

export class PerformanceTimer implements Timer {
  private startTime: number = 0;
  private endTime: number = 0;
  private isRunning: boolean = false;

  constructor(
    private operationName: string,
    private monitor: PerformanceMonitor
  ) {}

  start(): void {
    if (this.isRunning) {
      throw new Error(`Timer for ${this.operationName} is already running`);
    }

    this.startTime = Date.now();
    this.isRunning = true;
  }

  end(): number {
    if (!this.isRunning) {
      throw new Error(`Timer for ${this.operationName} was not started`);
    }

    this.endTime = Date.now();
    this.isRunning = false;

    const duration = this.endTime - this.startTime;

    // Record the metric with enhanced context
    this.monitor.recordMetric(`processing_time_${this.operationName}`, {
      timestamp: this.endTime,
      value: duration,
      unit: 'milliseconds',
      context: this.operationName,
      tags: {
        operation: this.operationName,
        type: 'processing_time',
        status: 'completed',
      },
    });

    return duration;
  }

  stop(): number {
    return this.end();
  }

  getDuration(): number {
    if (this.isRunning) {
      return Date.now() - this.startTime;
    }
    return this.endTime - this.startTime;
  }
}

export class PerformanceMonitor extends EventEmitter {
  private static instance: PerformanceMonitor;
  private metrics: Map<string, Metric[]> = new Map();
  private errorHandler = ErrorHandlerService.getInstance();
  private maxMetricsPerKey = 1000; // Prevent memory leaks
  private monitoringInterval: NodeJS.Timeout | null = null;
  private systemHealthInterval: NodeJS.Timeout | null = null;
  private alertThresholds = {
    memoryUsage: 0.8, // 80% of heap
    cpuUsage: 0.9, // 90% CPU
    errorRate: 0.1, // 10% error rate
    responseTime: 30000, // 30 seconds
  };
  private alerts: Array<{
    timestamp: number;
    type: string;
    message: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    resolved: boolean;
  }> = [];
  private startTime: number = Date.now();
  private processedOperations: Map<string, number> = new Map();
  private errorCounts: Map<string, number> = new Map();

  private constructor() {
    super();
    this.startSystemHealthMonitoring();
  }

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  startTimer(operationName: string): PerformanceTimer {
    return new PerformanceTimer(operationName, this);
  }

  recordMetric(key: string, metric: Metric): void {
    if (!this.metrics.has(key)) {
      this.metrics.set(key, []);
    }

    const metrics = this.metrics.get(key)!;
    metrics.push(metric);

    // Prevent memory leaks by limiting metrics per key
    if (metrics.length > this.maxMetricsPerKey) {
      metrics.shift();
    }

    // Emit metric event for real-time monitoring
    this.emit('metricRecorded', { key, metric });

    // Check for alert conditions
    this.checkAlertConditions(key, metric);
  }

  recordMemoryUsage(context: string): void {
    try {
      const memoryUsage = process.memoryUsage();
      const timestamp = Date.now();

      // Record detailed memory metrics
      this.recordMetric('memory_heap_used', {
        timestamp,
        value: memoryUsage.heapUsed,
        unit: 'bytes',
        context,
        tags: { type: 'memory', metric: 'heap_used', context },
      });

      this.recordMetric('memory_heap_total', {
        timestamp,
        value: memoryUsage.heapTotal,
        unit: 'bytes',
        context,
        tags: { type: 'memory', metric: 'heap_total', context },
      });

      this.recordMetric('memory_external', {
        timestamp,
        value: memoryUsage.external,
        unit: 'bytes',
        context,
        tags: { type: 'memory', metric: 'external', context },
      });

      this.recordMetric('memory_rss', {
        timestamp,
        value: memoryUsage.rss,
        unit: 'bytes',
        context,
        tags: { type: 'memory', metric: 'rss', context },
      });
    } catch (error) {
      this.errorHandler.handleError(error as Error, 'PerformanceMonitor.recordMemoryUsage');
    }
  }

  recordThroughput(operationName: string, itemsProcessed: number, duration: number): void {
    const throughput = itemsProcessed / (duration / 1000); // items per second

    this.recordMetric('throughput', {
      timestamp: Date.now(),
      value: throughput,
      unit: 'items/second',
      context: operationName,
      tags: {
        operation: operationName,
        type: 'throughput',
        items_processed: itemsProcessed.toString(),
        duration: duration.toString(),
      },
    });

    // Update processed operations counter
    this.processedOperations.set(
      operationName,
      (this.processedOperations.get(operationName) || 0) + itemsProcessed
    );
  }

  recordResourceUsage(context: string, additionalData?: Record<string, number>): void {
    try {
      const timestamp = Date.now();

      // CPU usage
      const cpuUsage = process.cpuUsage();
      this.recordMetric('cpu_user', {
        timestamp,
        value: cpuUsage.user,
        unit: 'microseconds',
        context,
        tags: { type: 'cpu', metric: 'user', context },
      });

      this.recordMetric('cpu_system', {
        timestamp,
        value: cpuUsage.system,
        unit: 'microseconds',
        context,
        tags: { type: 'cpu', metric: 'system', context },
      });

      // System load average
      const loadAvg = os.loadavg();
      this.recordMetric('load_average_1m', {
        timestamp,
        value: loadAvg[0],
        unit: 'load',
        context,
        tags: { type: 'system', metric: 'load_1m', context },
      });

      // Process uptime
      this.recordMetric('uptime', {
        timestamp,
        value: process.uptime(),
        unit: 'seconds',
        context,
        tags: { type: 'system', metric: 'uptime', context },
      });

      // Record additional data if provided
      if (additionalData) {
        Object.entries(additionalData).forEach(([key, value]) => {
          this.recordMetric(`resource_${key}`, {
            timestamp,
            value,
            unit: 'count',
            context,
            tags: { type: 'resource', metric: key, context },
          });
        });
      }
    } catch (error) {
      this.errorHandler.handleError(error as Error, 'PerformanceMonitor.recordResourceUsage');
    }
  }

  recordError(context: string, error: Error): void {
    const timestamp = Date.now();

    this.recordMetric('error_count', {
      timestamp,
      value: 1,
      unit: 'count',
      context,
      tags: {
        type: 'error',
        error_type: error.name,
        context,
      },
    });

    // Update error counts
    this.errorCounts.set(context, (this.errorCounts.get(context) || 0) + 1);
  }

  private checkAlertConditions(key: string, metric: Metric): void {
    const timestamp = Date.now();

    // Memory usage alerts
    if (key === 'memory_heap_used') {
      const memoryUsage = process.memoryUsage();
      const memoryPressure = memoryUsage.heapUsed / memoryUsage.heapTotal;

      if (memoryPressure > this.alertThresholds.memoryUsage) {
        this.createAlert(
          'memory_pressure',
          `High memory usage: ${Math.round(memoryPressure * 100)}%`,
          memoryPressure > 0.95 ? 'critical' : 'high'
        );
      }
    }

    // Processing time alerts
    if (key.startsWith('processing_time_') && metric.value > this.alertThresholds.responseTime) {
      this.createAlert(
        'slow_processing',
        `Slow processing time for ${metric.context}: ${metric.value}ms`,
        metric.value > 60000 ? 'critical' : 'medium'
      );
    }

    // Error rate alerts
    if (key === 'error_count') {
      const totalOps = this.processedOperations.get(metric.context) || 0;
      const errorCount = this.errorCounts.get(metric.context) || 0;
      const errorRate = totalOps > 0 ? errorCount / totalOps : 0;

      if (errorRate > this.alertThresholds.errorRate) {
        this.createAlert(
          'high_error_rate',
          `High error rate for ${metric.context}: ${Math.round(errorRate * 100)}%`,
          errorRate > 0.5 ? 'critical' : 'high'
        );
      }
    }
  }

  private createAlert(
    type: string,
    message: string,
    severity: 'low' | 'medium' | 'high' | 'critical'
  ): void {
    const alert = {
      timestamp: Date.now(),
      type,
      message,
      severity,
      resolved: false,
    };

    this.alerts.push(alert);
    this.emit('alert', alert);

    // Keep only last 100 alerts
    if (this.alerts.length > 100) {
      this.alerts.shift();
    }
  }

  private startSystemHealthMonitoring(): void {
    this.systemHealthInterval = setInterval(() => {
      this.recordMemoryUsage('system_health');
      this.recordResourceUsage('system_health');
    }, 30000); // Every 30 seconds
  }

  getMetrics(key: string): Metric[] {
    return this.metrics.get(key) || [];
  }

  getAllMetrics(): Map<string, Metric[]> {
    return new Map(this.metrics);
  }

  getReport(): PerformanceReport {
    return {
      memoryUsage: this.getEnhancedMemoryTrend(),
      processingTimes: this.getProcessingTimeMetrics(),
      throughput: this.getThroughputMetrics(),
      cachePerformance: this.getCachePerformanceMetrics(),
      workerUtilization: this.getWorkerUtilizationMetrics(),
      systemHealth: this.getSystemHealthMetrics(),
    };
  }

  private getEnhancedMemoryTrend(): MemoryTrend {
    const heapUsedMetrics = this.getMetrics('memory_heap_used');

    if (heapUsedMetrics.length === 0) {
      return {
        current: 0,
        peak: 0,
        average: 0,
        trend: 'stable',
        history: [],
      };
    }

    const values = heapUsedMetrics.map(m => m.value);
    const current = values[values.length - 1];
    const peak = Math.max(...values);
    const average = values.reduce((a, b) => a + b, 0) / values.length;

    // Calculate trend
    const recentValues = values.slice(-10);
    const trend =
      recentValues.length > 1
        ? recentValues[recentValues.length - 1] > recentValues[0]
          ? 'increasing'
          : recentValues[recentValues.length - 1] < recentValues[0]
            ? 'decreasing'
            : 'stable'
        : 'stable';

    return {
      current,
      peak,
      average,
      trend,
      history: heapUsedMetrics.map(m => ({ timestamp: m.timestamp, value: m.value })),
    };
  }

  private getProcessingTimeMetrics(): ProcessingTimeMetrics {
    const processingMetrics = Array.from(this.metrics.entries())
      .filter(([key]) => key.startsWith('processing_time_'))
      .flatMap(([, metrics]) => metrics);

    if (processingMetrics.length === 0) {
      return {
        averageTime: 0,
        medianTime: 0,
        p95Time: 0,
        p99Time: 0,
        totalTime: 0,
      };
    }

    const times = processingMetrics.map(m => m.value).sort((a, b) => a - b);
    const totalTime = times.reduce((a, b) => a + b, 0);
    const averageTime = totalTime / times.length;
    const medianTime = times[Math.floor(times.length / 2)];
    const p95Time = times[Math.floor(times.length * 0.95)];
    const p99Time = times[Math.floor(times.length * 0.99)];

    return {
      averageTime,
      medianTime,
      p95Time,
      p99Time,
      totalTime,
    };
  }

  private getThroughputMetrics(): ThroughputMetrics {
    const throughputMetrics = this.getMetrics('throughput');

    if (throughputMetrics.length === 0) {
      return {
        pagesPerSecond: 0,
        pagesPerMinute: 0,
        tasksPerSecond: 0,
        peakThroughput: 0,
      };
    }

    const values = throughputMetrics.map(m => m.value);
    const currentThroughput = values[values.length - 1] || 0;
    const peakThroughput = Math.max(...values);

    return {
      pagesPerSecond: currentThroughput,
      pagesPerMinute: currentThroughput * 60,
      tasksPerSecond: currentThroughput, // Assuming 1 task per page
      peakThroughput,
    };
  }

  private getCachePerformanceMetrics(): CachePerformance {
    const cacheHits = this.getMetrics('cache_hit');
    const cacheMisses = this.getMetrics('cache_miss');
    const cacheStores = this.getMetrics('cache_store');

    const totalRequests = cacheHits.length + cacheMisses.length;
    const hitRate = totalRequests > 0 ? cacheHits.length / totalRequests : 0;
    const missRate = totalRequests > 0 ? cacheMisses.length / totalRequests : 0;

    return {
      hitRate,
      missRate,
      evictionRate: 0, // Would need eviction metrics
      memoryUsage: 0, // Would need cache memory metrics
      entryCount: cacheStores.length,
    };
  }

  private getWorkerUtilizationMetrics(): WorkerUtilizationMetrics {
    // This would integrate with the TaskQueue to get worker metrics
    return {
      activeWorkers: 0,
      totalWorkers: 0,
      utilizationRate: 0,
      averageTaskTime: 0,
      queueLength: 0,
    };
  }

  private getSystemHealthMetrics(): SystemHealthMetrics {
    const cpuUserMetrics = this.getMetrics('cpu_user');
    const cpuSystemMetrics = this.getMetrics('cpu_system');
    const loadMetrics = this.getMetrics('load_average_1m');
    const uptimeMetrics = this.getMetrics('uptime');
    const memoryMetrics = this.getMetrics('memory_heap_used');
    const errorMetrics = this.getMetrics('error_count');

    const totalErrors = errorMetrics.reduce((sum, m) => sum + m.value, 0);
    const totalOperations = Array.from(this.processedOperations.values()).reduce(
      (sum, count) => sum + count,
      0
    );

    return {
      cpuUsage: cpuUserMetrics.length > 0 ? cpuUserMetrics[cpuUserMetrics.length - 1].value : 0,
      memoryUsage: memoryMetrics.length > 0 ? memoryMetrics[memoryMetrics.length - 1].value : 0,
      diskUsage: 0, // Would need disk metrics
      networkLatency: 0, // Would need network metrics
      uptime: uptimeMetrics.length > 0 ? uptimeMetrics[uptimeMetrics.length - 1].value : 0,
      errorRate: totalOperations > 0 ? totalErrors / totalOperations : 0,
    };
  }

  getMemoryTrend(): Metric[] {
    return this.getMetrics('memory_heap_used');
  }

  getProcessingTimes(): Metric[] {
    return Array.from(this.metrics.entries())
      .filter(([key]) => key.startsWith('processing_time_'))
      .flatMap(([, metrics]) => metrics);
  }

  getThroughput(): Metric[] {
    return this.getMetrics('throughput');
  }

  getAverageProcessingTime(operationName: string): number {
    const metrics = this.getMetrics(`processing_time_${operationName}`);
    if (metrics.length === 0) return 0;
    return metrics.reduce((sum, m) => sum + m.value, 0) / metrics.length;
  }

  getMemoryPeakUsage(context: string): number {
    const metrics = this.getMetrics('memory_heap_used');
    return metrics.length > 0 ? Math.max(...metrics.map(m => m.value)) : 0;
  }

  getAlerts(unresolved?: boolean): Array<{
    timestamp: number;
    type: string;
    message: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    resolved: boolean;
  }> {
    return unresolved ? this.alerts.filter(a => !a.resolved) : this.alerts;
  }

  resolveAlert(timestamp: number): void {
    const alert = this.alerts.find(a => a.timestamp === timestamp);
    if (alert) {
      alert.resolved = true;
      this.emit('alertResolved', alert);
    }
  }

  startContinuousMonitoring(intervalMs: number = 5000): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }

    this.monitoringInterval = setInterval(() => {
      this.recordMemoryUsage('continuous_monitoring');
      this.recordResourceUsage('continuous_monitoring');
    }, intervalMs);
  }

  stopContinuousMonitoring(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
      this.monitoringInterval = null;
    }
  }

  clearMetrics(key?: string): void {
    if (key) {
      this.metrics.delete(key);
    } else {
      this.metrics.clear();
      this.processedOperations.clear();
      this.errorCounts.clear();
      this.alerts.length = 0;
    }
  }

  exportMetrics(format: 'json' | 'csv' = 'json'): string {
    const allMetrics = Array.from(this.metrics.entries()).map(([key, metrics]) => ({
      key,
      metrics,
    }));

    if (format === 'json') {
      return JSON.stringify(allMetrics, null, 2);
    }

    // CSV format
    const csvHeaders = 'key,timestamp,value,unit,context,tags\n';
    const csvRows = allMetrics
      .flatMap(({ key, metrics }) =>
        metrics.map(
          metric =>
            `${key},${metric.timestamp},${metric.value},${metric.unit},${metric.context},${JSON.stringify(metric.tags)}`
        )
      )
      .join('\n');

    return csvHeaders + csvRows;
  }

  getSummary(): {
    totalMetrics: number;
    memoryPeakMB: number;
    averageProcessingTime: number;
    activeOperations: string[];
    systemHealth: 'healthy' | 'warning' | 'critical';
    unresolvedAlerts: number;
  } {
    const totalMetrics = Array.from(this.metrics.values()).reduce(
      (sum, metrics) => sum + metrics.length,
      0
    );
    const memoryPeakMB = this.getMemoryPeakUsage('') / (1024 * 1024);
    const averageProcessingTime =
      this.getProcessingTimes().reduce((sum, m) => sum + m.value, 0) /
      Math.max(1, this.getProcessingTimes().length);
    const activeOperations = Array.from(this.processedOperations.keys());
    const unresolvedAlerts = this.getAlerts(true).length;

    let systemHealth: 'healthy' | 'warning' | 'critical' = 'healthy';
    const criticalAlerts = this.getAlerts(true).filter(a => a.severity === 'critical').length;
    const highAlerts = this.getAlerts(true).filter(a => a.severity === 'high').length;

    if (criticalAlerts > 0) {
      systemHealth = 'critical';
    } else if (highAlerts > 0 || unresolvedAlerts > 5) {
      systemHealth = 'warning';
    }

    return {
      totalMetrics,
      memoryPeakMB,
      averageProcessingTime,
      activeOperations,
      systemHealth,
      unresolvedAlerts,
    };
  }

  async measureAsyncOperation<T>(operationName: string, operation: () => Promise<T>): Promise<T> {
    const timer = this.startTimer(operationName);
    const startMemory = process.memoryUsage().heapUsed;

    try {
      const result = await operation();
      const duration = timer.end();
      const endMemory = process.memoryUsage().heapUsed;

      // Record additional metrics
      this.recordMetric(`operation_memory_delta_${operationName}`, {
        timestamp: Date.now(),
        value: endMemory - startMemory,
        unit: 'bytes',
        context: operationName,
        tags: { type: 'memory_delta', operation: operationName },
      });

      return result;
    } catch (error) {
      timer.end();
      this.recordError(operationName, error as Error);
      throw error;
    }
  }

  shutdown(): void {
    if (this.monitoringInterval) {
      clearInterval(this.monitoringInterval);
    }
    if (this.systemHealthInterval) {
      clearInterval(this.systemHealthInterval);
    }
    this.removeAllListeners();
  }
}
