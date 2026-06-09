import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ServiceResult, ErrorResult, SuccessResult } from '@/core/types/common';

// Mock console methods to reduce noise in tests
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation();
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation();
const mockConsoleWarn = jest.spyOn(console, 'warn').mockImplementation();

describe('ErrorHandlerService', () => {
    let errorHandler: ErrorHandlerService;

    beforeEach(() => {
        // Clear all mocks before each test
        jest.clearAllMocks();
        errorHandler = ErrorHandlerService.getInstance();
    });

    afterAll(() => {
        // Restore console methods
        mockConsoleError.mockRestore();
        mockConsoleLog.mockRestore();
        mockConsoleWarn.mockRestore();
    });

    describe('Singleton Pattern', () => {
        test('should return the same instance when called multiple times', () => {
            const instance1 = ErrorHandlerService.getInstance();
            const instance2 = ErrorHandlerService.getInstance();
            expect(instance1).toBe(instance2);
        });

        test('should throw error when trying to instantiate directly', () => {
            expect(() => {
                new (ErrorHandlerService as any)();
            }).toThrow('Use ErrorHandlerService.getInstance() instead of new.');
        });
    });

    describe('handleError', () => {
        test('should handle Error objects correctly', () => {
            const testError = new Error('Test error message');
            const result = errorHandler.handleError(testError, 'test context');

            expect(result.success).toBe(false);
            expect(result.error).toBe(testError);
            expect(result.context).toBe('test context');
            expect(mockConsoleError).toHaveBeenCalledWith(
                '❌ Error in test context:',
                'Test error message'
            );
        });

        test('should handle string errors correctly', () => {
            const result = errorHandler.handleError('String error', 'string context');

            expect(result.success).toBe(false);
            expect(result.error).toBeInstanceOf(Error);
            expect((result.error as Error).message).toBe('String error');
            expect(result.context).toBe('string context');
        });

        test('should handle unknown error types', () => {
            const unknownError = { custom: 'error' };
            const result = errorHandler.handleError(unknownError, 'unknown context');

            expect(result.success).toBe(false);
            expect(result.error).toBeInstanceOf(Error);
            expect((result.error as Error).message).toBe('[object Object]');
            expect(result.context).toBe('unknown context');
        });

        test('should use default context when none provided', () => {
            const result = errorHandler.handleError('Test error');
            expect(result.context).toBe('unknown context');
        });
    });

    describe('createSuccess', () => {
        test('should create success result with data', () => {
            const testData = { test: 'data' };
            const result = errorHandler.createSuccess(testData);

                  expect(result.success).toBe(true);
      expect(result.data).toEqual(testData);
      expect(result.timestamp).toBeDefined();
      expect(new Date(result.timestamp!).getTime()).toBeCloseTo(Date.now(), -2);
        });

        test('should handle different data types', () => {
            const stringResult = errorHandler.createSuccess('string data');
            const numberResult = errorHandler.createSuccess(42);
            const arrayResult = errorHandler.createSuccess([1, 2, 3]);

            expect(stringResult.data).toBe('string data');
            expect(numberResult.data).toBe(42);
            expect(arrayResult.data).toEqual([1, 2, 3]);
        });
    });

    describe('executeWithErrorHandling', () => {
        test('should return success result when function succeeds', async () => {
            const asyncFn = jest.fn().mockResolvedValue('success data');
            const result = await errorHandler.executeWithErrorHandling(asyncFn, 'test context');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('success data');
            expect(asyncFn).toHaveBeenCalledTimes(1);
        });

        test('should return error result when function throws', async () => {
            const asyncFn = jest.fn().mockRejectedValue(new Error('Async error'));
            const result = await errorHandler.executeWithErrorHandling(asyncFn, 'async context');

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
            expect((result as ErrorResult).context).toBe('async context');
        });
    });

    describe('executeWithErrorHandlingSync', () => {
        test('should return success result when function succeeds', () => {
            const syncFn = jest.fn().mockReturnValue('sync data');
            const result = errorHandler.executeWithErrorHandlingSync(syncFn, 'sync context');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('sync data');
            expect(syncFn).toHaveBeenCalledTimes(1);
        });

        test('should return error result when function throws', () => {
            const syncFn = jest.fn().mockImplementation(() => {
                throw new Error('Sync error');
            });
            const result = errorHandler.executeWithErrorHandlingSync(syncFn, 'sync error context');

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
            expect((result as ErrorResult).context).toBe('sync error context');
        });
    });

    describe('withTimeout', () => {
        test('should return success result when promise resolves before timeout', async () => {
            const fastPromise = Promise.resolve('fast result');
            const result = await errorHandler.withTimeout(fastPromise, 1000, 'timeout test');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('fast result');
        });

        test('should return error result when promise times out', async () => {
            const slowPromise = new Promise(resolve => setTimeout(() => resolve('slow'), 2000));
            const result = await errorHandler.withTimeout(slowPromise, 100, 'timeout error test');

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
            expect((result as ErrorResult).error.message).toContain('timed out after 100ms');
        });
    });

    describe('retryWithBackoff', () => {
        test('should return success result on first attempt', async () => {
            const fn = jest.fn().mockResolvedValue('first try success');
            const result = await errorHandler.retryWithBackoff(fn, 3, 'retry test');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('first try success');
            expect(fn).toHaveBeenCalledTimes(1);
        });

        test('should retry and eventually succeed', async () => {
            const fn = jest.fn()
                .mockRejectedValueOnce(new Error('First failure'))
                .mockRejectedValueOnce(new Error('Second failure'))
                .mockResolvedValue('Third try success');

            const result = await errorHandler.retryWithBackoff(fn, 3, 'retry success test');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('Third try success');
            expect(fn).toHaveBeenCalledTimes(3);
        });

        test('should return error result after max retries', async () => {
            const fn = jest.fn().mockRejectedValue(new Error('Persistent failure'));
            const result = await errorHandler.retryWithBackoff(fn, 2, 'retry failure test');

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
            expect(fn).toHaveBeenCalledTimes(2);
        });
    });

    describe('Logging Methods', () => {
        test('should log debug messages correctly', () => {
            errorHandler.logDebug('Debug message', { debug: 'data' });
            expect(mockConsoleLog).toHaveBeenCalledWith(
                '🔍 [DEBUG] Debug message',
                JSON.stringify({ debug: 'data' }, null, 2)
            );
        });

        test('should log info messages correctly', () => {
            errorHandler.logInfo('Info message', { info: 'data' });
            expect(mockConsoleLog).toHaveBeenCalledWith(
                'ℹ️ Info:',
                'Info message',
                JSON.stringify({ info: 'data' }, null, 2)
            );
        });

        test('should log warning messages correctly', () => {
            errorHandler.logWarning('Warning message', { warning: 'data' });
            expect(mockConsoleWarn).toHaveBeenCalledWith(
                '⚠️ Warning:',
                'Warning message',
                JSON.stringify({ warning: 'data' }, null, 2)
            );
        });

        test('should log success messages correctly', () => {
            errorHandler.logSuccess('Success message', { success: 'data' });
            expect(mockConsoleLog).toHaveBeenCalledWith(
                '✅ Success:',
                'Success message',
                JSON.stringify({ success: 'data' }, null, 2)
            );
        });
    });

    describe('Type Guards', () => {
        test('should correctly identify error results', () => {
            const errorResult = errorHandler.handleError('Test error');
            const successResult = errorHandler.createSuccess('Test data');

            expect(errorHandler.isError(errorResult)).toBe(true);
            expect(errorHandler.isError(successResult)).toBe(false);
        });

        test('should correctly identify success results', () => {
            const errorResult = errorHandler.handleError('Test error');
            const successResult = errorHandler.createSuccess('Test data');

            expect(errorHandler.isSuccess(successResult)).toBe(true);
            expect(errorHandler.isSuccess(errorResult)).toBe(false);
        });
    });

    describe('executeWithRetry', () => {
        test('should execute function with retry logic', async () => {
            const fn = jest.fn().mockResolvedValue('retry success');
            const result = await errorHandler.executeWithRetry(fn, 'retry context', 2);

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('retry success');
            expect(fn).toHaveBeenCalledTimes(1);
        });

        test('should handle retry failures', async () => {
            const fn = jest.fn().mockRejectedValue(new Error('Retry failure'));
            const result = await errorHandler.executeWithRetry(fn, 'retry failure context', 1);

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
        });
    });
}); 