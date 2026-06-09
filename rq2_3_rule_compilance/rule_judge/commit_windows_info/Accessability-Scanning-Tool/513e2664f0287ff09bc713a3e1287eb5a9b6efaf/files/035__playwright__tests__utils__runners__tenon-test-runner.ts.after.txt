import { Page } from '@playwright/test';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';
import fetch from 'node-fetch';

export interface TenonResult {
  status: number;
  message: string;
  code: string;
  moreInfo: string;
  responseExecTime: string;
  responseTime: string;
  request: {
    url: string;
    projectID: string;
    level: string;
    certainty: number;
    priority: number;
    docID: string;
    reportID: string;
    store: number;
    importance: number;
    ref: boolean;
    fragment: boolean;
    viewport: {
      height: number;
      width: number;
    };
    uaString: string;
  };
  resultSet: TenonIssue[];
  resultSetSize: number;
  totalResults: number;
  documentSize: number;
  apiUsage: {
    cost: number;
    remaining: number;
  };
  projectStats: {
    totalIssues: number;
    issuesByLevel: {
      A: number;
      AA: number;
      AAA: number;
    };
    density: number;
  };
}

export interface TenonIssue {
  bpID: number;
  certainty: number;
  errorDescription: string;
  errorSnippet: string;
  errorTitle: string;
  issueID: string;
  position: {
    line: number;
    column: number;
  };
  priority: number;
  ref: string;
  resultTitle: string;
  signature: string;
  snippet: string;
  tID: number;
  xpath: string;
  wcag: string[];
  severity: 'low' | 'medium' | 'high' | 'critical';
  tags: string[];
}

export interface TenonTestOptions {
  level?: 'A' | 'AA' | 'AAA';
  certainty?: number; // 0-100, higher = more certain
  priority?: number; // 0-100, higher = more important
  docID?: string;
  reportID?: string;
  projectID?: string;
  store?: boolean;
  importance?: number;
  ref?: boolean;
  fragment?: boolean;
  viewport?: {
    height: number;
    width: number;
  };
  uaString?: string;
}

export class TenonTestRunner {
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();
  private apiKey: string;
  private baseUrl = 'https://tenon.io/api/';

  constructor(
    private page: Page,
    apiKey?: string
  ) {
    this.apiKey = apiKey || this.getTenonApiKey();
  }

  /**
   * Runs Tenon API analysis
   */
  async runAnalysis(options: TenonTestOptions = {}): Promise<ServiceResult<TenonResult>> {
    const config = this.config.getTenonConfiguration();
    const currentUrl = this.page.url();

    this.errorHandler.logInfo(`Running Tenon API analysis for: ${currentUrl}`);

    return this.errorHandler.withTimeout(
      this.performTenonAnalysis(currentUrl, options),
      config.timeout,
      'Tenon API analysis'
    );
  }

  /**
   * Runs Tenon analysis for WCAG 2.1 AA compliance
   */
  async runWCAGAAAnalysis(): Promise<ServiceResult<TenonResult>> {
    return this.runAnalysis({
      level: 'AA',
      certainty: 80,
      priority: 60,
      store: true,
    });
  }

  /**
   * Runs Tenon analysis for WCAG 2.1 AAA compliance
   */
  async runWCAGAAAAnalysis(): Promise<ServiceResult<TenonResult>> {
    return this.runAnalysis({
      level: 'AAA',
      certainty: 90,
      priority: 80,
      store: true,
    });
  }

  /**
   * Runs Tenon analysis focusing on high-priority issues
   */
  async runHighPriorityAnalysis(): Promise<ServiceResult<TenonResult>> {
    return this.runAnalysis({
      level: 'AA',
      certainty: 95,
      priority: 90,
      store: true,
    });
  }

  /**
   * Runs Tenon analysis focusing on critical issues
   */
  async runCriticalAnalysis(): Promise<ServiceResult<TenonResult>> {
    const result = await this.runAnalysis({
      level: 'AA',
      certainty: 100,
      priority: 100,
      store: true,
    });

    if (result.success && result.data) {
      // Filter to only critical and high severity issues
      const criticalFilteredResult = {
        ...result.data,
        resultSet: result.data.resultSet.filter(
          issue => issue.severity === 'critical' || issue.severity === 'high'
        ),
        resultSetSize: result.data.resultSet.filter(
          issue => issue.severity === 'critical' || issue.severity === 'high'
        ).length,
      };

      return { success: true, data: criticalFilteredResult };
    }

    return result;
  }

  /**
   * Runs Tenon analysis for specific WCAG guidelines
   */
  async runWCAGGuidelineAnalysis(guideline: string): Promise<ServiceResult<TenonResult>> {
    const result = await this.runAnalysis({
      level: 'AA',
      certainty: 85,
      priority: 75,
      store: true,
    });

    if (result.success && result.data) {
      // Filter results to focus on specific WCAG guideline
      const guidelineFilteredResult = {
        ...result.data,
        resultSet: result.data.resultSet.filter(issue =>
          issue.wcag.some(wcagRef => wcagRef.includes(guideline))
        ),
        resultSetSize: result.data.resultSet.filter(issue =>
          issue.wcag.some(wcagRef => wcagRef.includes(guideline))
        ).length,
      };

      return { success: true, data: guidelineFilteredResult };
    }

    return result;
  }

  /**
   * Runs Tenon analysis with custom viewport
   */
  async runViewportAnalysis(viewport: {
    width: number;
    height: number;
  }): Promise<ServiceResult<TenonResult>> {
    // Set viewport on page first
    await this.page.setViewportSize(viewport);

    return this.runAnalysis({
      level: 'AA',
      certainty: 85,
      priority: 70,
      viewport,
      store: true,
    });
  }

  /**
   * Performs the actual Tenon API analysis
   */
  private async performTenonAnalysis(url: string, options: TenonTestOptions): Promise<TenonResult> {
    if (!this.apiKey) {
      throw new Error(
        'Tenon API key is required. Set TENON_API_KEY environment variable or provide it in configuration.'
      );
    }

    const requestBody = {
      key: this.apiKey,
      url: url,
      level: options.level || 'AA',
      certainty: options.certainty || 80,
      priority: options.priority || 60,
      docID: options.docID || '',
      reportID: options.reportID || '',
      projectID: options.projectID || '',
      store: options.store ? 1 : 0,
      importance: options.importance || 60,
      ref: options.ref ? 1 : 0,
      fragment: options.fragment ? 1 : 0,
      viewport: options.viewport || { width: 1200, height: 800 },
      uaString: options.uaString || 'Mozilla/5.0 (compatible; Tenon/1.0)',
    };

    this.errorHandler.logInfo(`Making Tenon API request for URL: ${url}`);

    const startTime = Date.now();
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    const duration = Date.now() - startTime;

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `Tenon API request failed: ${response.status} ${response.statusText} - ${errorText}`
      );
    }

    const result = (await response.json()) as TenonResult;

    if (!result || result.status !== 200) {
      throw new Error(`Tenon API returned error: ${result.message || 'Unknown error'}`);
    }

    // Add severity levels to issues based on priority and certainty
    result.resultSet = result.resultSet.map(issue => ({
      ...issue,
      severity: this.calculateSeverity(issue.priority, issue.certainty),
      tags: this.generateTags(issue),
    }));

    this.errorHandler.logSuccess(
      `Tenon API analysis completed in ${duration}ms: ${result.resultSetSize} issues found, ${result.apiUsage.remaining} API calls remaining`
    );

    return result;
  }

  /**
   * Calculates severity level based on priority and certainty
   */
  private calculateSeverity(
    priority: number,
    certainty: number
  ): 'low' | 'medium' | 'high' | 'critical' {
    const score = priority * 0.6 + certainty * 0.4;

    if (score >= 90) return 'critical';
    if (score >= 70) return 'high';
    if (score >= 50) return 'medium';
    return 'low';
  }

  /**
   * Generates tags for issue categorization
   */
  private generateTags(issue: TenonIssue): string[] {
    const tags: string[] = ['tenon'];

    // Add WCAG tags
    issue.wcag.forEach(wcagRef => {
      tags.push(wcagRef.toLowerCase());
    });

    // Add category tags based on error title
    const title = issue.errorTitle.toLowerCase();
    if (title.includes('color') || title.includes('contrast')) {
      tags.push('color', 'contrast');
    }
    if (title.includes('aria')) {
      tags.push('aria');
    }
    if (title.includes('form') || title.includes('input')) {
      tags.push('forms');
    }
    if (title.includes('image') || title.includes('alt')) {
      tags.push('images');
    }
    if (title.includes('heading') || title.includes('landmark')) {
      tags.push('structure');
    }
    if (title.includes('keyboard') || title.includes('focus')) {
      tags.push('keyboard');
    }

    return tags;
  }

  /**
   * Gets Tenon API key from environment or configuration
   */
  private getTenonApiKey(): string {
    // Try environment variable first
    const envKey = process.env.TENON_API_KEY;
    if (envKey) {
      return envKey;
    }

    // Try configuration service
    const config = this.config.getTenonConfiguration();
    if (config.apiKey) {
      return config.apiKey;
    }

    // Return empty string - will be handled by performTenonAnalysis
    return '';
  }

  /**
   * Runs Tenon analysis with retry logic
   */
  async runAnalysisWithRetry(
    options: TenonTestOptions = {},
    maxRetries: number = 3
  ): Promise<ServiceResult<TenonResult>> {
    return this.errorHandler.retryWithBackoff(
      () => this.performTenonAnalysis(this.page.url(), options),
      maxRetries,
      1000,
      'Tenon API analysis'
    );
  }

  /**
   * Converts Tenon results to standardized format for integration
   */
  convertToStandardFormat(tenonResult: TenonResult): any[] {
    return tenonResult.resultSet.map(issue => ({
      id: `tenon-${issue.bpID}`,
      impact: this.mapSeverityToImpact(issue.severity),
      description: issue.errorDescription,
      help: issue.errorTitle,
      helpUrl: issue.ref,
      tags: issue.tags,
      nodes: [
        {
          target: [issue.xpath],
          html: issue.snippet,
          impact: this.mapSeverityToImpact(issue.severity),
          any: [],
          all: [],
          none: [],
        },
      ],
      wcag: issue.wcag,
      tool: 'tenon',
      tenonData: {
        bpID: issue.bpID,
        certainty: issue.certainty,
        priority: issue.priority,
        position: issue.position,
        signature: issue.signature,
        tID: issue.tID,
      },
    }));
  }

  /**
   * Maps Tenon severity to standard impact levels
   */
  private mapSeverityToImpact(severity: 'low' | 'medium' | 'high' | 'critical'): string {
    switch (severity) {
      case 'critical':
        return 'critical';
      case 'high':
        return 'serious';
      case 'medium':
        return 'moderate';
      case 'low':
        return 'minor';
      default:
        return 'moderate';
    }
  }

  /**
   * Gets project statistics from Tenon
   */
  async getProjectStats(projectID: string): Promise<ServiceResult<any>> {
    if (!this.apiKey) {
      return { success: false, error: 'Tenon API key is required' };
    }

    const requestBody = {
      key: this.apiKey,
      projectID: projectID,
    };

    try {
      const response = await fetch(`${this.baseUrl}/stats`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Tenon stats request failed: ${response.status}`);
      }

      const result = await response.json();
      return { success: true, data: result };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}
