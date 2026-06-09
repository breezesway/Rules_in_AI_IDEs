import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { ErrorHandlerService } from '../../playwright/tests/utils/services/error-handler-service';

describe('ErrorHandlerService', () => {
  let errorHandler: ErrorHandlerService;
  let consoleSpy: jest.SpyInstance;

  beforeEach(() => {
    // Reset singleton instance before each test
    (ErrorHandlerService as any).instance = undefined;
    errorHandler = ErrorHandlerService.getInstance();

    // Mock console methods
    consoleSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    // Clean up singleton instance after each test
    (ErrorHandlerService as any).instance = undefined;
    consoleSpy.mockRestore();
  });

  describe('Singleton Pattern', () => {
    it('should return the same instance on multiple calls', () => {
      const instance1 = ErrorHandlerService.getInstance();
      const instance2 = ErrorHandlerService.getInstance();

      expect(instance1).toBe(instance2);
    });

    it('should not allow direct instantiation', () => {
      expect(() => new (ErrorHandlerService as any)()).toThrow();
    });
  });

  describe('Error Handling', () => {
    it('should handle Error objects correctly', () => {
      const testError = new Error('Test error message');
      const context = 'test-context';

      const result = errorHandler.handleError(testError, context);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Test error message');
      expect(result.originalError).toBe(testError);
      expect(result.context).toBe(context);
      expect(result.timestamp).toBeDefined();
      expect(typeof result.timestamp).toBe('string');
    });

    it('should handle string errors correctly', () => {
      const errorMessage = 'String error message';
      const context = 'string-context';

      const result = errorHandler.handleError(errorMessage, context);

      expect(result.success).toBe(false);
      expect(result.error).toBe(errorMessage);
      expect(result.originalError).toBeUndefined();
      expect(result.context).toBe(context);
      expect(result.timestamp).toBeDefined();
    });

    it('should handle unknown error types', () => {
      const unknownError = { someProperty: 'value' };
      const context = 'unknown-context';

      const result = errorHandler.handleError(unknownError, context);

      expect(result.success).toBe(false);
      expect(result.error).toBe('[object Object]');
      expect(result.context).toBe(context);
      expect(result.timestamp).toBeDefined();
    });

    it('should handle null and undefined errors', () => {
      const nullResult = errorHandler.handleError(null, 'null-context');
      const undefinedResult = errorHandler.handleError(undefined, 'undefined-context');

      expect(nullResult.success).toBe(false);
      expect(nullResult.error).toBe('null');

      expect(undefinedResult.success).toBe(false);
      expect(undefinedResult.error).toBe('undefined');
    });

    it('should handle errors without context', () => {
      const testError = new Error('Test error');

      const result = errorHandler.handleError(testError);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Test error');
      expect(result.context).toBeUndefined();
    });

    it('should log errors to console', () => {
      const testError = new Error('Test error');
      const context = 'test-context';

      errorHandler.handleError(testError, context);

      expect(consoleSpy).toHaveBeenCalledWith('❌ Error in test-context:', 'Test error');
    });

    it('should log stack trace for Error objects', () => {
      const testError = new Error('Test error');
      testError.stack = 'Test stack trace';

      errorHandler.handleError(testError, 'test-context');

      expect(consoleSpy).toHaveBeenCalledWith('   Stack: Test stack trace');
    });
  });

  describe('Service Result Creation', () => {
    it('should create success results correctly', () => {
      const testData = { key: 'value', number: 42 };

      const result = errorHandler.createSuccess(testData);

      expect(result.success).toBe(true);
      expect(result.data).toEqual(testData);
      expect(result.timestamp).toBeDefined();
      expect(typeof result.timestamp).toBe('string');
    });

    it('should create success results with null data', () => {
      const result = errorHandler.createSuccess(null);

      expect(result.success).toBe(true);
      expect(result.data).toBeNull();
      expect(result.timestamp).toBeDefined();
    });

    it('should create success results with undefined data', () => {
      const result = errorHandler.createSuccess(undefined);

      expect(result.success).toBe(true);
      expect(result.data).toBeUndefined();
      expect(result.timestamp).toBeDefined();
    });
  });

  describe('Service Result Type Guards', () => {
    it('should correctly identify success results', () => {
      const successResult = errorHandler.createSuccess('test data');
      const errorResult = errorHandler.handleError(new Error('test error'));

      expect(errorHandler.isSuccess(successResult)).toBe(true);
      expect(errorHandler.isSuccess(errorResult)).toBe(false);
    });

    it('should correctly identify error results', () => {
      const successResult = errorHandler.createSuccess('test data');
      const errorResult = errorHandler.handleError(new Error('test error'));

      expect(errorHandler.isError(successResult)).toBe(false);
      expect(errorHandler.isError(errorResult)).toBe(true);
    });
  });

  describe('Execute with Error Handling', () => {
    it('should execute successful async functions', async () => {
      const testData = { result: 'success' };
      const asyncFunction = jest.fn().mockResolvedValue(testData);

      const result = await errorHandler.executeWithErrorHandling(asyncFunction, 'test-context');

      expect(asyncFunction).toHaveBeenCalledTimes(1);
      expect(result.success).toBe(true);
      expect(result.data).toEqual(testData);
    });

    it('should handle async function errors', async () => {
      const testError = new Error('Async error');
      const asyncFunction = jest.fn().mockRejectedValue(testError);

      const result = await errorHandler.executeWithErrorHandling(asyncFunction, 'test-context');

      expect(asyncFunction).toHaveBeenCalledTimes(1);
      expect(result.success).toBe(false);
      expect(result.error).toBe('Async error');
      expect(result.context).toBe('test-context');
    });

    it('should handle synchronous errors in async functions', async () => {
      const asyncFunction = jest.fn().mockImplementation(() => {
        throw new Error('Sync error in async function');
      });

      const result = await errorHandler.executeWithErrorHandling(asyncFunction, 'test-context');

      expect(result.success).toBe(false);
      expect(result.error).toBe('Sync error in async function');
    });

    it('should handle functions that return promises', async () => {
      const testData = 'promise result';
      const asyncFunction = jest.fn().mockImplementation(() => Promise.resolve(testData));

      const result = await errorHandler.executeWithErrorHandling(asyncFunction, 'test-context');

      expect(result.success).toBe(true);
      expect(result.data).toBe(testData);
    });
  });

  describe('Logging Methods', () => {
    let infoSpy: jest.SpyInstance;
    let successSpy: jest.SpyInstance;
    let warnSpy: jest.SpyInstance;

    beforeEach(() => {
      infoSpy = jest.spyOn(console, 'log').mockImplementation();
      successSpy = jest.spyOn(console, 'log').mockImplementation();
      warnSpy = jest.spyOn(console, 'warn').mockImplementation();
    });

    afterEach(() => {
      infoSpy.mockRestore();
      successSpy.mockRestore();
      warnSpy.mockRestore();
    });

    it('should log info messages', () => {
      const message = 'Info message';

      errorHandler.logInfo(message);

      expect(infoSpy).toHaveBeenCalledWith('ℹ️ Info:', message);
    });

    it('should log success messages', () => {
      const message = 'Success message';

      errorHandler.logSuccess(message);

      expect(successSpy).toHaveBeenCalledWith('✅ Success:', message);
    });

    it('should log warning messages', () => {
      const message = 'Warning message';

      errorHandler.logWarning(message);

      expect(warnSpy).toHaveBeenCalledWith('⚠️ Warning:', message);
    });
  });

  describe('Retry Logic', () => {
    it('should retry failed operations with exponential backoff', async () => {
      let attemptCount = 0;
      const maxRetries = 3;
      const failingFunction = jest.fn().mockImplementation(async () => {
        attemptCount++;
        if (attemptCount < maxRetries) {
          throw new Error(`Attempt ${attemptCount} failed`);
        }
        return 'success';
      });

      const result = await errorHandler.executeWithRetry(
        failingFunction,
        'test-context',
        maxRetries,
        1000
      );

      expect(failingFunction).toHaveBeenCalledTimes(maxRetries);
      expect(result.success).toBe(true);
      expect(result.data).toBe('success');
    });

    it('should fail after maximum retries', async () => {
      const maxRetries = 3;
      const alwaysFailingFunction = jest.fn().mockRejectedValue(new Error('Always fails'));

      const result = await errorHandler.executeWithRetry(
        alwaysFailingFunction,
        'test-context',
        maxRetries,
        100
      );

      expect(alwaysFailingFunction).toHaveBeenCalledTimes(maxRetries);
      expect(result.success).toBe(false);
      expect(result.error).toBe('Always fails');
    });

    it('should succeed on first attempt without retries', async () => {
      const successFunction = jest.fn().mockResolvedValue('immediate success');

      const result = await errorHandler.executeWithRetry(successFunction, 'test-context', 3, 1000);

      expect(successFunction).toHaveBeenCalledTimes(1);
      expect(result.success).toBe(true);
      expect(result.data).toBe('immediate success');
    });

    it('should use exponential backoff delay', async () => {
      const startTime = Date.now();
      const attemptTimes: number[] = [];

      const failingFunction = jest.fn().mockImplementation(async () => {
        attemptTimes.push(Date.now() - startTime);
        throw new Error('Always fails');
      });

      await errorHandler.executeWithRetry(failingFunction, 'test-context', 3, 100);

      expect(attemptTimes).toHaveLength(3);
      // Check that delays are increasing (exponential backoff)
      expect(attemptTimes[1] - attemptTimes[0]).toBeGreaterThan(50);
      expect(attemptTimes[2] - attemptTimes[1]).toBeGreaterThan(attemptTimes[1] - attemptTimes[0]);
    });
  });

  describe('Error Result Validation', () => {
    it('should validate error result structure', () => {
      const error = new Error('Test error');
      const context = 'test-context';

      const result = errorHandler.handleError(error, context);

      expect(result).toHaveProperty('success', false);
      expect(result).toHaveProperty('error', 'Test error');
      expect(result).toHaveProperty('originalError', error);
      expect(result).toHaveProperty('timestamp');
      expect(result).toHaveProperty('context', context);
    });

    it('should validate success result structure', () => {
      const testData = { key: 'value' };

      const result = errorHandler.createSuccess(testData);

      expect(result).toHaveProperty('success', true);
      expect(result).toHaveProperty('data', testData);
      expect(result).toHaveProperty('timestamp');
      expect(result).not.toHaveProperty('error');
      expect(result).not.toHaveProperty('originalError');
      expect(result).not.toHaveProperty('context');
    });

    it('should validate timestamp format', () => {
      const result = errorHandler.createSuccess('test');

      expect(result.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
    });
  });

  describe('Edge Cases', () => {
    it('should handle circular reference errors', () => {
      const circularObj: any = { prop: 'value' };
      circularObj.self = circularObj;

      const result = errorHandler.handleError(circularObj, 'circular-context');

      expect(result.success).toBe(false);
      expect(result.error).toBe('[object Object]');
      expect(result.context).toBe('circular-context');
    });

    it('should handle very long error messages', () => {
      const longMessage = 'A'.repeat(10000);
      const error = new Error(longMessage);

      const result = errorHandler.handleError(error, 'long-message-context');

      expect(result.success).toBe(false);
      expect(result.error).toBe(longMessage);
      expect(result.context).toBe('long-message-context');
    });

    it('should handle functions that throw non-error objects', async () => {
      const throwingFunction = jest.fn().mockImplementation(() => {
        // eslint-disable-next-line no-throw-literal
        throw 'String error';
      });

      const result = await errorHandler.executeWithErrorHandling(throwingFunction, 'test-context');

      expect(result.success).toBe(false);
      expect(result.error).toBe('String error');
    });
  });
});
