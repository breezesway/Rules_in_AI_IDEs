export interface ErrorResult {
    success: false;
    error: string;
    originalError?: Error;
    timestamp: string;
    context?: string;
}

export interface SuccessResult<T = any> {
    success: true;
    data: T;
    timestamp: string;
}

export type ServiceResult<T = any> = ErrorResult | SuccessResult<T>;

export class ErrorHandlerService {
    private static instance: ErrorHandlerService;

    private constructor() { }

    static getInstance(): ErrorHandlerService {
        if (!ErrorHandlerService.instance) {
            ErrorHandlerService.instance = new ErrorHandlerService();
        }
        return ErrorHandlerService.instance;
    }

    /**
     * Handles errors consistently across the application
     */
    handleError(error: unknown, context?: string): ErrorResult {
        const timestamp = new Date().toISOString();

        if (error instanceof Error) {
            console.error(`❌ Error in ${context || 'unknown context'}:`, error.message);
            console.error(`   Stack: ${error.stack}`);

            return {
                success: false,
                error: error.message,
                originalError: error,
                timestamp,
                context,
            };
        }

        const errorMessage = typeof error === 'string' ? error : String(error);
        console.error(`❌ Error in ${context || 'unknown context'}:`, errorMessage);

        return {
            success: false,
            error: errorMessage,
            timestamp,
            context,
        };
    }

    /**
     * Creates a success result
     */
    createSuccess<T>(data: T): SuccessResult<T> {
        return {
            success: true,
            data,
            timestamp: new Date().toISOString(),
        };
    }

    /**
     * Executes a function with error handling
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
     */
    executeWithErrorHandlingSync<T>(
        fn: () => T,
        context: string
    ): ServiceResult<T> {
        try {
            const result = fn();
            return this.createSuccess(result);
        } catch (error) {
            return this.handleError(error, context);
        }
    }

    /**
     * Wraps a timeout around a promise
     */
    async withTimeout<T>(
        promise: Promise<T>,
        timeoutMs: number,
        context: string
    ): Promise<ServiceResult<T>> {
        const timeoutPromise = new Promise<never>((_, reject) => {
            setTimeout(() => {
                reject(new Error(`Operation timed out after ${timeoutMs}ms`));
            }, timeoutMs);
        });

        try {
            const result = await Promise.race([promise, timeoutPromise]);
            return this.createSuccess(result);
        } catch (error) {
            return this.handleError(error, context);
        }
    }

    /**
     * Retries a function with exponential backoff
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
                console.log(`   🔄 Retrying ${context} (attempt ${attempt + 1}/${maxRetries}) in ${delay}ms...`);

                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }

        return this.handleError(lastError, `${context} (after ${maxRetries} attempts)`);
    }

    /**
     * Logs debug information in a consistent format
     */
    logDebug(message: string, data?: any): void {
        console.log(`🔍 [DEBUG] ${message}`, data ? JSON.stringify(data, null, 2) : '');
    }

    /**
     * Logs info in a consistent format
     */
    logInfo(message: string, data?: any): void {
        console.log(`ℹ️  ${message}`, data ? JSON.stringify(data, null, 2) : '');
    }

    /**
     * Logs warning in a consistent format
     */
    logWarning(message: string, data?: any): void {
        console.warn(`⚠️  ${message}`, data ? JSON.stringify(data, null, 2) : '');
    }

    /**
     * Logs success in a consistent format
     */
    logSuccess(message: string, data?: any): void {
        console.log(`✅ ${message}`, data ? JSON.stringify(data, null, 2) : '');
    }

    /**
     * Checks if a result is an error
     */
    isError(result: ServiceResult): result is ErrorResult {
        return !result.success;
    }

    /**
     * Checks if a result is successful
     */
    isSuccess<T>(result: ServiceResult<T>): result is SuccessResult<T> {
        return result.success;
    }
} 