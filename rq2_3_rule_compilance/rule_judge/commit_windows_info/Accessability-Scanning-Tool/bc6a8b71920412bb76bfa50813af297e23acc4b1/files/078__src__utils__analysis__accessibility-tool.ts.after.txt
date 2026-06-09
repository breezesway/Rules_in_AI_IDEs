import { Page } from 'playwright';
import { ToolResult } from '../../core/types/common';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';

export interface AccessibilityToolOptions {
  timeout?: number;
  includeScreenshots?: boolean;
  excludePatterns?: string[];
  includePatterns?: string[];
}

export interface AccessibilityTool {
  name: string;
  version: string;
  analyze(page: Page, options?: AccessibilityToolOptions): Promise<ToolResult>;
  cleanup(): Promise<void>;
}

export abstract class BaseAccessibilityTool implements AccessibilityTool {
  protected errorHandler = ErrorHandlerService.getInstance();

  abstract name: string;
  abstract version: string;

  abstract analyze(page: Page, options?: AccessibilityToolOptions): Promise<ToolResult>;

  async cleanup(): Promise<void> {
    // Default implementation - can be overridden
    this.errorHandler.logInfo(`Cleaning up ${this.name} tool`);
  }

  protected async measureExecutionTime<T>(
    operation: () => Promise<T>,
    operationName: string
  ): Promise<{ result: T; duration: number }> {
    const startTime = Date.now();

    try {
      const result = await operation();
      const duration = Date.now() - startTime;

      this.errorHandler.logInfo(`${this.name} ${operationName} completed in ${duration}ms`);

      return { result, duration };
    } catch (error) {
      const duration = Date.now() - startTime;
      this.errorHandler.handleError(
        error,
        `${this.name} ${operationName} failed after ${duration}ms`
      );
      throw error;
    }
  }

  protected createSuccessResult(data: any, duration: number): ToolResult {
    return {
      tool: this.name,
      success: true,
      data,
      duration,
    };
  }

  protected createErrorResult(error: Error, duration: number): ToolResult {
    return {
      tool: this.name,
      success: false,
      error: error.message,
      duration,
    };
  }
}
