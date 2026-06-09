export interface PageInfo {
  url: string;
  title: string;
  depth: number;
  foundOn: string;
  status: number;
  loadTime?: number;
}

export interface AnalysisResult {
  url: string;
  timestamp: string;
  tool: string;
  violations: ProcessedViolation[];
  summary: AnalysisSummary;
}

export interface ProcessedViolation {
  id: string;
  impact: 'minor' | 'moderate' | 'serious' | 'critical';
  description: string;
  help: string;
  helpUrl: string;
  wcagTags: string[];
  wcagLevel: 'A' | 'AA' | 'AAA' | 'Unknown';
  occurrences: number;
  tools: string[];
  elements: ViolationElement[];
  remediation: {
    priority: 'High' | 'Medium' | 'Low';
    effort: 'Low' | 'Medium' | 'High';
    suggestions: string[];
    codeExample?: string;
  };
}

export interface ViolationElement {
  html: string;
  target: any;
  failureSummary: string;
  screenshot?: string;
  selector: string;
  xpath?: string;
  boundingRect?: { x: number; y: number; width: number; height: number };
}

export interface AnalysisSummary {
  totalViolations: number;
  criticalViolations: number;
  seriousViolations: number;
  moderateViolations: number;
  minorViolations: number;
}

export interface ToolResult {
  tool: string;
  success: boolean;
  data?: any;
  error?: string;
  duration: number;
}

export interface CombinedResult {
  results: ToolResult[];
  violations: ProcessedViolation[];
  summary: AnalysisSummary;
}

export interface BatchResult {
  successful: AnalysisResult[];
  failed: Array<{ page: PageInfo; error: string }>;
  metrics: {
    totalTime: number;
    averageTimePerPage: number;
    successRate: number;
  };
}

export interface ServiceResult<T> {
  success: boolean;
  data?: T;
  error?: Error;
  message?: string;
  metadata?: any;
}

export interface Task {
  id: string;
  type: 'crawl' | 'analyze' | 'report';
  url: string;
  options: any;
  priority: number;
}

export interface CachedResult {
  result: AnalysisResult;
  timestamp: number;
  ttl: number;
}

export interface Metric {
  timestamp: number;
  value: number;
  unit: string;
}

export interface Timer {
  start(): void;
  end(): number;
}

// Phase 2: Queue-based Processing Types
export interface AnalysisTask {
  id: string;
  url: string;
  type: 'single-page' | 'batch' | 'full-site';
  priority: 'low' | 'medium' | 'high';
  options: AccessibilityTestOptions;
  retryCount: number;
  maxRetries: number;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
}

export interface TaskResult {
  taskId: string;
  success: boolean;
  result?: ServiceResult<any>;
  error?: Error;
  duration: number;
  memoryUsage: number;
  workerMetrics: WorkerMetrics;
}

export interface Worker {
  id: string;
  isAvailable: boolean;
  currentTask?: AnalysisTask;
  processedTasks: number;
  totalProcessingTime: number;
  lastActivity: Date;
  metrics: WorkerMetrics;
}

export interface WorkerMetrics {
  tasksProcessed: number;
  averageProcessingTime: number;
  memoryUsage: number;
  errorRate: number;
  uptime: number;
}

export interface TaskQueue {
  pending: AnalysisTask[];
  processing: AnalysisTask[];
  completed: AnalysisTask[];
  failed: AnalysisTask[];
}

// Phase 2: Caching Types
export interface CachedResult {
  result: any;
  timestamp: number;
  ttl: number;
  url: string;
  hash: string;
  metadata: CacheMetadata;
}

export interface CacheMetadata {
  size: number;
  accessCount: number;
  lastAccessed: Date;
  cacheKey: string;
  domain: string;
}

export interface CacheConfig {
  maxSize: number;
  defaultTTL: number;
  cleanupInterval: number;
  compressionEnabled: boolean;
}

// Phase 2: Enhanced Monitoring Types
export interface Metric {
  timestamp: number;
  value: number;
  unit: string;
  context: string;
  tags: Record<string, string>;
}

export interface PerformanceReport {
  memoryUsage: MemoryTrend;
  processingTimes: ProcessingTimeMetrics;
  throughput: ThroughputMetrics;
  cachePerformance: CachePerformance;
  workerUtilization: WorkerUtilizationMetrics;
  systemHealth: SystemHealthMetrics;
}

export interface MemoryTrend {
  current: number;
  peak: number;
  average: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  history: Array<{ timestamp: number; value: number }>;
}

export interface ProcessingTimeMetrics {
  averageTime: number;
  medianTime: number;
  p95Time: number;
  p99Time: number;
  totalTime: number;
}

export interface ThroughputMetrics {
  pagesPerSecond: number;
  pagesPerMinute: number;
  tasksPerSecond: number;
  peakThroughput: number;
}

export interface CachePerformance {
  hitRate: number;
  missRate: number;
  evictionRate: number;
  memoryUsage: number;
  entryCount: number;
}

export interface WorkerUtilizationMetrics {
  activeWorkers: number;
  totalWorkers: number;
  utilizationRate: number;
  averageTaskTime: number;
  queueLength: number;
}

export interface SystemHealthMetrics {
  cpuUsage: number;
  memoryUsage: number;
  diskUsage: number;
  networkLatency: number;
  uptime: number;
  errorRate: number;
}

// Phase 2: API Service Layer Types
export interface TestRequest {
  url: string;
  type: 'quick' | 'comprehensive' | 'single-page';
  options: AccessibilityTestOptions;
  priority: 'low' | 'medium' | 'high';
  callback?: string;
  metadata?: Record<string, any>;
}

export interface TestResponse {
  requestId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  results?: ServiceResult<any>;
  error?: string;
  metrics: ProcessingMetrics;
  estimatedCompletion?: Date;
}

export interface ProcessingMetrics {
  startTime: Date;
  endTime?: Date;
  duration?: number;
  pagesProcessed: number;
  totalPages: number;
  memoryUsage: number;
  cacheHits: number;
  cacheMisses: number;
}

// Phase 2: Database Integration Types
export interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
  pool: {
    min: number;
    max: number;
    idleTimeoutMillis: number;
  };
}

export interface StoredResult {
  id: string;
  url: string;
  testType: string;
  results: any;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
  expiresAt?: Date;
}

export interface AccessibilityTestOptions {
  generateReports?: boolean;
  outputPath?: string;
  includeCharts?: boolean;
  includeScreenshots?: boolean;
  includeBrandColors?: boolean;
  timeout?: number;
  retries?: number;
  [key: string]: any;
}
