export interface PageInfo {
  url: string;
  title: string;
  depth: number;
  foundOn: string;
  status: number;
  loadTime: number; // Make loadTime required
}

export interface AnalysisResult {
  url: string;
  timestamp: string;
  tool: string;
  violations: ProcessedViolation[];
  passes: ProcessedViolation[];
  warnings: ProcessedViolation[];
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
  browsers?: string[]; // List of browsers where this violation was found
  tools: string[]; // List of tools that found this violation (axe, pa11y)
  elements: Array<{
    html: string;
    target: ViolationTarget;
    failureSummary: string;
    screenshot?: string; // Base64 encoded screenshot
    selector: string; // CSS selector for the element
    xpath?: string; // XPath for the element
    boundingRect?: { x: number; y: number; width: number; height: number };
    relatedNodes?: Array<{
      html: string;
      target: ViolationTarget;
    }>;
  }>;
  scenarioRelevance: string[];
  remediation: {
    priority: 'High' | 'Medium' | 'Low';
    effort: 'Low' | 'Medium' | 'High';
    suggestions: string[];
    codeExample?: string;
  };
}

export interface AccessibilityReport {
  url: string;
  timestamp: string;
  testSuite: string;
  browser?: string;
  viewport?: string;
  summary: {
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    wcagAAViolations: number;
    wcagAAAViolations: number;
  };
  violations: ProcessedViolation[];
  pageAnalysis: {
    title: string;
    headingStructure: Array<{ level: number; text: string; tagName: string }>;
    landmarks: { main: boolean; nav: boolean; footer: boolean };
    skipLink: { exists: boolean; isVisible: boolean; targetExists: boolean };
    images: Array<{ src: string; alt: string; hasAlt: boolean; ariaLabel?: string }>;
    links: Array<{ text: string; href: string; hasAriaLabel: boolean; ariaLabel?: string }>;
    forms: Array<{
      hasLabel: boolean;
      labelText: string;
      inputType: string;
      isRequired: boolean;
      hasAriaLabel: boolean;
    }>;
    keyboardNavigation: Array<{ element: string; canFocus: boolean; hasVisibleFocus: boolean }>;
    responsive?: { mobile: boolean; tablet: boolean; desktop: boolean };
  };
}

export interface SiteWideAccessibilityReport {
  siteUrl: string;
  timestamp: string;
  testSuite: string;
  wcagLevel?: string; // WCAG level used for the scan
  summary: {
    totalPages: number;
    pagesWithViolations: number;
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    compliancePercentage: number;
    mostCommonViolations: Array<{
      id: string;
      affectedPages: number;
      totalOccurrences: number;
      impact: string;
      description: string;
    }>;
  };
  pageReports: AccessibilityReport[];
  violationsByType: Record<
    string,
    {
      count: number;
      pages: string[];
      impact: string;
      description: string;
      totalOccurrences: number;
      browsers: string[]; // List of browsers where this violation was found
      tools: string[]; // List of tools that detected this violation
    }
  >;
}

// Type for accessibility tool target selectors
export interface ViolationTarget {
  selector?: string;
  xpath?: string;
  element?: Element;
  [key: string]: unknown;
}

export interface ViolationElement {
  html: string;
  target: ViolationTarget;
  failureSummary: string;
  screenshot?: string;
  selector: string;
  xpath?: string;
  boundingRect?: { x: number; y: number; width: number; height: number };
}

export interface AnalysisSummary {
  totalViolations: number;
  totalPasses: number;
  totalWarnings: number;
  criticalViolations: number;
  seriousViolations: number;
  moderateViolations: number;
  minorViolations: number;
}

export interface ToolResult<T = unknown> {
  tool: string;
  success: boolean;
  data?: T;
  error?: string;
  duration: number;
}

export interface CombinedResult {
  results: ToolResult[];
  violations: ProcessedViolation[];
  passes: ProcessedViolation[];
  warnings: ProcessedViolation[];
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

export interface ServiceResult<T = unknown> {
  success: boolean;
  data?: T;
  error?: Error;
  message?: string;
  metadata?: Record<string, unknown>;
}

export interface SuccessResult<T> extends ServiceResult<T> {
  success: true;
  data: T;
  timestamp?: string;
}

export interface ErrorResult extends ServiceResult<never> {
  success: false;
  error: Error;
  context?: string;
}

export interface Task {
  id: string;
  type: 'crawl' | 'analyze' | 'report';
  url: string;
  options: AccessibilityTestOptions;
  priority: number;
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

export interface TaskResult<T = ServiceResult> {
  taskId: string;
  success: boolean;
  result?: T;
  error?: Error;
  duration: number;
  memoryUsage: number;
  workerMetrics: WorkerMetrics;
}

export interface Worker {
  id: string;
  isAvailable: boolean;
  currentTask: AnalysisTask | null;
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
export interface CachedResult<T = AnalysisResult> {
  result: T;
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

export interface CachePerformance {
  hitRate: number;
  missRate: number;
  evictionRate: number;
  memoryUsage: number;
  entryCount: number;
}

export interface CacheConfig {
  maxSize: number;
  defaultTTL: number;
  cleanupInterval: number;
  compressionEnabled: boolean;
}



// Phase 2: API Service Layer Types
export interface TestRequest {
  url: string;
  type: 'quick' | 'comprehensive' | 'single-page';
  options: AccessibilityTestOptions;
  priority: 'low' | 'medium' | 'high';
  callback?: string;
  metadata?: Record<string, unknown>;
}

export interface TestResponse<T = ServiceResult> {
  requestId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  results?: T;
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

export interface StoredResult<T = AnalysisResult> {
  id: string;
  url: string;
  testType: string;
  results: T;
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
  expiresAt?: Date;
}

export interface CrawlOptions {
  maxPages?: number;
  maxDepth?: number;
  allowedDomains?: string[];
  excludePatterns?: RegExp[];
  includePatterns?: RegExp[];
  delayBetweenRequests?: number;
  respectRobotsTxt?: boolean;
  maxRetries?: number;
  retryDelay?: number;
  timeoutMs?: number;
  timeout?: number;
  userAgent?: string;
}

export interface AccessibilityTestOptions {
  generateReports?: boolean;
  outputPath?: string;
  includeCharts?: boolean;
  includeScreenshots?: boolean;
  includeBrandColors?: boolean;
  timeout?: number;
  retries?: number;
  [key: string]: unknown;
}
