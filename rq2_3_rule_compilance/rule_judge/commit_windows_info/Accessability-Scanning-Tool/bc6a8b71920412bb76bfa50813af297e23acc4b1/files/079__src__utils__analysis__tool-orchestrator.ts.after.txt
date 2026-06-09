import { Page } from 'playwright';
import { AccessibilityTool, AccessibilityToolOptions } from './accessibility-tool';
import {
  AnalysisSummary,
  CombinedResult,
  ProcessedViolation,
  ToolResult,
} from '../../core/types/common';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ViolationProcessor } from '@/utils/processors/violation-processor';

export interface ToolOrchestrationOptions extends AccessibilityToolOptions {
  enabledTools?: string[];
  parallelExecution?: boolean;
  failOnFirstError?: boolean;
}

export class ToolOrchestrator {
  private tools: Map<string, AccessibilityTool> = new Map();
  private errorHandler = ErrorHandlerService.getInstance();
  private violationProcessor: ViolationProcessor;

  constructor(page: Page) {
    this.violationProcessor = new ViolationProcessor(page);
  }

  registerTool(tool: AccessibilityTool): void {
    this.tools.set(tool.name, tool);
    this.errorHandler.logInfo(`Registered accessibility tool: ${tool.name} v${tool.version}`);
  }

  unregisterTool(toolName: string): void {
    const tool = this.tools.get(toolName);
    if (tool) {
      this.tools.delete(toolName);
      this.errorHandler.logInfo(`Unregistered accessibility tool: ${toolName}`);
    }
  }

  getRegisteredTools(): string[] {
    return Array.from(this.tools.keys());
  }

  async runAnalysis(page: Page, options: ToolOrchestrationOptions = {}): Promise<CombinedResult> {
    const {
      enabledTools = this.getRegisteredTools(),
      parallelExecution = true,
      failOnFirstError = false,
      ...toolOptions
    } = options;

    this.errorHandler.logInfo('Starting tool orchestration analysis', {
      enabledTools,
      parallelExecution,
      toolCount: enabledTools.length,
    });

    const selectedTools = enabledTools
      .map(toolName => this.tools.get(toolName))
      .filter((tool): tool is AccessibilityTool => tool !== undefined);

    if (selectedTools.length === 0) {
      throw new Error('No valid accessibility tools found for analysis');
    }

    const startTime = Date.now();
    let results: ToolResult[];

    try {
      if (parallelExecution) {
        results = await this.runParallelAnalysis(
          selectedTools,
          page,
          toolOptions,
          failOnFirstError
        );
      } else {
        results = await this.runSequentialAnalysis(
          selectedTools,
          page,
          toolOptions,
          failOnFirstError
        );
      }

      const duration = Date.now() - startTime;

      // Process and combine results
      const combinedResult = await this.combineResults(results);

      this.errorHandler.logSuccess(`Tool orchestration completed in ${duration}ms`, {
        toolsRun: results.length,
        successfulTools: results.filter(r => r.success).length,
        totalViolations: combinedResult.violations.length,
      });

      return combinedResult;
    } catch (error) {
      const duration = Date.now() - startTime;
      this.errorHandler.handleError(error, `Tool orchestration failed after ${duration}ms`);
      throw error;
    }
  }

  private async runParallelAnalysis(
    tools: AccessibilityTool[],
    page: Page,
    options: AccessibilityToolOptions,
    failOnFirstError: boolean
  ): Promise<ToolResult[]> {
    this.errorHandler.logInfo(`Running parallel analysis with ${tools.length} tools`);

    const promises = tools.map(async tool => {
      try {
        return await tool.analyze(page, options);
      } catch (error) {
        if (failOnFirstError) {
          throw error;
        }

        this.errorHandler.handleError(error, `Tool ${tool.name} failed`);
        return {
          tool: tool.name,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
          duration: 0,
        };
      }
    });

    return await Promise.all(promises);
  }

  private async runSequentialAnalysis(
    tools: AccessibilityTool[],
    page: Page,
    options: AccessibilityToolOptions,
    failOnFirstError: boolean
  ): Promise<ToolResult[]> {
    this.errorHandler.logInfo(`Running sequential analysis with ${tools.length} tools`);

    const results: ToolResult[] = [];

    for (const tool of tools) {
      try {
        const result = await tool.analyze(page, options);
        results.push(result);
      } catch (error) {
        if (failOnFirstError) {
          throw error;
        }

        this.errorHandler.handleError(error, `Tool ${tool.name} failed`);
        results.push({
          tool: tool.name,
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
          duration: 0,
        });
      }
    }

    return results;
  }

  private async combineResults(results: ToolResult[]): Promise<CombinedResult> {
    const violations: ProcessedViolation[] = [];
    const successfulResults = results.filter(r => r.success);

    // Extract violations from successful results
    for (const result of successfulResults) {
      // TODO: Fix this type error
      if (result.data && (result.data as any).violations) {
        violations.push(...(result.data as any).violations);
      }
    }

    // Create combined summary
    const summary: AnalysisSummary = {
      totalViolations: violations.length,
      criticalViolations: violations.filter(v => v.impact === 'critical').length,
      seriousViolations: violations.filter(v => v.impact === 'serious').length,
      moderateViolations: violations.filter(v => v.impact === 'moderate').length,
      minorViolations: violations.filter(v => v.impact === 'minor').length,
    };

    return {
      results,
      violations: await this.deduplicateViolations(violations),
      summary,
    };
  }

  private async deduplicateViolations(
    violations: ProcessedViolation[]
  ): Promise<ProcessedViolation[]> {
    const violationMap = new Map<string, ProcessedViolation>();

    for (const violation of violations) {
      const key = `${violation.id}-${violation.elements[0]?.selector || 'unknown'}`;

      if (violationMap.has(key)) {
        const existing = violationMap.get(key)!;

        // Merge tools that found this violation
        existing.tools = [...new Set([...existing.tools, ...violation.tools])];

        // Use the highest impact level
        if (this.getImpactLevel(violation.impact) > this.getImpactLevel(existing.impact)) {
          existing.impact = violation.impact;
        }

        // Merge elements
        existing.elements = [...existing.elements, ...violation.elements];
        existing.occurrences += violation.occurrences;
      } else {
        violationMap.set(key, { ...violation });
      }
    }

    return Array.from(violationMap.values());
  }

  private getImpactLevel(impact: ProcessedViolation['impact']): number {
    const levels = { minor: 1, moderate: 2, serious: 3, critical: 4 };
    return levels[impact] || 0;
  }

  async cleanup(): Promise<void> {
    this.errorHandler.logInfo('Cleaning up tool orchestrator');

    const cleanupPromises = Array.from(this.tools.values()).map(tool =>
      tool
        .cleanup()
        .catch(error =>
          this.errorHandler.handleError(error, `Cleanup failed for tool: ${tool.name}`)
        )
    );

    await Promise.all(cleanupPromises);
    this.errorHandler.logSuccess('Tool orchestrator cleanup completed');
  }

  getToolStatus(): Record<string, { registered: boolean; version: string }> {
    const status: Record<string, { registered: boolean; version: string }> = {};

    for (const [name, tool] of this.tools) {
      status[name] = {
        registered: true,
        version: tool.version,
      };
    }

    return status;
  }
}
