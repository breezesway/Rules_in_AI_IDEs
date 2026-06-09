import { ServiceResult, ErrorResult, SuccessResult } from '@/core/types/common';

/**
 * Singleton service for consistent error handling across the application
 * Provides standardized error handling, logging, and retry logic
 */
export class ErrorHandlerService {
  private static instance: ErrorHandlerService;

  private constructor() {
    if (ErrorHandlerService.instance) {
      throw new Error('Use ErrorHandlerService.getInstance() instead of new.');
    }
  }

  /**
   * Gets the singleton instance of ErrorHandlerService
   * @returns The singleton ErrorHandlerService instance
   */
  static getInstance(): ErrorHandlerService {
    if (!ErrorHandlerService.instance) {
      ErrorHandlerService.instance = new ErrorHandlerService();
    }
    return ErrorHandlerService.instance;
  }

  /**
   * Handles errors consistently across the application
   * @param error The error to handle (Error object, string, or unknown)
   * @param context Optional context describing where the error occurred
   * @returns Standardized error result object
   */
  handleError(error: unknown, context?: string): ErrorResult {
    const timestamp = new Date().toISOString();

    if (error instanceof Error) {
      console.error(`❌ Error in ${context || 'unknown context'}:`, error.message);
      console.error(`   Stack: ${error.stack}`);

      return {
        success: false,
        error: error,
        context: context || 'unknown context',
      };
    }

    const errorMessage = typeof error === 'string' ? error : String(error);
    const errorObj = new Error(errorMessage);
    console.error(`❌ Error in ${context || 'unknown context'}:`, errorMessage);

    return {
      success: false,
      error: errorObj,
      context: context || 'unknown context',
    };
  }

  /**
   * Creates a success result with the provided data
   * @template T Type of the data to wrap
   * @param data The data to wrap in a success result
   * @returns Standardized success result object
   */
  createSuccess<T>(data: T): SuccessResult<T> {
    return {
      success: true,
      data,
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Executes an async function with error handling
   * @template T Type of the data returned by the function
   * @param fn The async function to execute
   * @param context Context description for error reporting
   * @returns Promise resolving to ServiceResult
   */
  async executeWithErrorHandling<T>(
    fn: () => Promise<T>,
    context: string
  ): Promise<ServiceResult<T>> {
    try {
      const result = await fn();
      return this.createSuccess(result);
    } catch (error) {
      return this.handleError(error, context);
    }
  }

  /**
   * Executes a synchronous function with error handling
   * @template T Type of the data returned by the function
   * @param fn The synchronous function to execute
   * @param context Context description for error reporting
   * @returns ServiceResult
   */
  executeWithErrorHandlingSync<T>(fn: () => T, context: string): ServiceResult<T> {
    try {
      const result = fn();
      return this.createSuccess(result);
    } catch (error) {
      return this.handleError(error, context);
    }
  }

  /**
   * Wraps a timeout around a promise
   * @template T Type of the data returned by the promise
   * @param promise The promise to wrap with timeout
   * @param timeoutMs Timeout in milliseconds
   * @param context Context description for error reporting
   * @returns Promise resolving to ServiceResult
   */
  async withTimeout<T>(
    promise: Promise<T>,
    timeoutMs: number,
    context: string
  ): Promise<ServiceResult<T>> {
    let timeoutId: NodeJS.Timeout | undefined;
    const timeoutPromise = new Promise<never>((_, reject) => {
      timeoutId = setTimeout(() => {
        reject(new Error(`Operation timed out after ${timeoutMs}ms`));
      }, timeoutMs);
    });

    try {
      const result = await Promise.race([promise, timeoutPromise]);
      // Clear the timeout if the promise resolves
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      return this.createSuccess(result);
    } catch (error) {
      // Clear the timeout if there's an error
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      return this.handleError(error, context);
    }
  }

  /**
   * Retries a function with exponential backoff
   * @template T Type of the data returned by the function
   * @param fn The async function to retry
   * @param maxRetries Maximum number of retry attempts
   * @param context Context description for error reporting
   * @param baseDelayMs Base delay in milliseconds for exponential backoff
   * @returns Promise resolving to ServiceResult
   */
  async retryWithBackoff<T>(
    fn: () => Promise<T>,
    maxRetries: number,
    context: string,
    baseDelayMs: number = 1000
  ): Promise<ServiceResult<T>> {
    let lastError: unknown;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        const result = await fn();
        return this.createSuccess(result);
      } catch (error) {
        lastError = error;

        if (attempt === maxRetries - 1) {
          // Last attempt failed
          break;
        }

        // Calculate delay with exponential backoff
        const delay = baseDelayMs * Math.pow(2, attempt);
        console.log(
          `   🔄 Retrying ${context} (attempt ${attempt + 1}/${maxRetries}) in ${delay}ms...`
        );

        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    return this.handleError(lastError, `${context} (after ${maxRetries} attempts)`);
  }

  /**
   * Logs debug information in a consistent format
   * @param message Debug message to log
   * @param data Optional data to include in the log
   */
  logDebug(message: string, data?: any): void {
    console.log(`🔍 [DEBUG] ${message}`, data ? JSON.stringify(data, null, 2) : '');
  }

  /**
   * Logs info in a consistent format
   * @param message Info message to log
   * @param data Optional data to include in the log
   */
  logInfo(message: string, data?: any): void {
    if (data) {
      console.log('ℹ️ Info:', message, JSON.stringify(data, null, 2));
    } else {
      console.log('ℹ️ Info:', message);
    }
  }

  /**
   * Logs warning in a consistent format
   * @param message Warning message to log
   * @param data Optional data to include in the log
   */
  logWarning(message: string, data?: any): void {
    if (data) {
      console.warn('⚠️ Warning:', message, JSON.stringify(data, null, 2));
    } else {
      console.warn('⚠️ Warning:', message);
    }
  }

  /**
   * Logs error in a consistent format
   * @param message Error message to log
   * @param data Optional data to include in the log
   */
  logError(message: string, data?: any): void {
    if (data) {
      console.error('❌ Error:', message, JSON.stringify(data, null, 2));
    } else {
      console.error('❌ Error:', message);
    }
  }

  /**
   * Logs success in a consistent format
   * @param message Success message to log
   * @param data Optional data to include in the log
   */
  logSuccess(message: string, data?: any): void {
    if (data) {
      console.log('✅ Success:', message, JSON.stringify(data, null, 2));
    } else {
      console.log('✅ Success:', message);
    }
  }

  /**
   * Type guard to check if a result is an error
   * @param result The ServiceResult to check
   * @returns True if the result is an error, false otherwise
   */
  isError(result: ServiceResult): result is ErrorResult {
    return !result.success;
  }

  /**
   * Type guard to check if a result is successful
   * @template T Type of the data in the success result
   * @param result The ServiceResult to check
   * @returns True if the result is successful, false otherwise
   */
  isSuccess<T>(result: ServiceResult<T>): result is SuccessResult<T> {
    return result.success;
  }

  /**
   * Executes a function with retry logic and exponential backoff
   * @template T Type of the data returned by the function
   * @param fn The async function to retry
   * @param context Context description for error reporting
   * @param maxRetries Maximum number of retry attempts
   * @param baseDelayMs Base delay in milliseconds for exponential backoff
   * @returns Promise resolving to ServiceResult
   */
  async executeWithRetry<T>(
    fn: () => Promise<T>,
    context: string,
    maxRetries: number,
    baseDelayMs: number = 1000
  ): Promise<ServiceResult<T>> {
    let lastError: unknown;

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        this.logInfo(`Executing ${context} (attempt ${attempt + 1}/${maxRetries})`);
        const result = await fn();

        if (attempt > 0) {
          this.logSuccess(`${context} succeeded after ${attempt + 1} attempts`);
        }

        return this.createSuccess(result);
      } catch (error) {
        lastError = error;

        if (attempt === maxRetries - 1) {
          // Last attempt failed
          this.logWarning(`${context} failed after ${maxRetries} attempts`);
          break;
        }

        // Calculate delay with exponential backoff
        const delay = baseDelayMs * Math.pow(2, attempt);
        this.logWarning(
          `${context} failed on attempt ${attempt + 1}/${maxRetries}, retrying in ${delay}ms...`
        );

        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    return this.handleError(lastError, `${context} (after ${maxRetries} attempts)`);
  }
}
