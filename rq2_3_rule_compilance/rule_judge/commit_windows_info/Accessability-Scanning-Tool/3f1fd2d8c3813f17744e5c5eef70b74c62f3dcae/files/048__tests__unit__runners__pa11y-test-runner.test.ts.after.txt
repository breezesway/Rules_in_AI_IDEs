import { Pa11yTestRunner, Pa11yResult, Pa11yIssue } from '@/utils/runners/pa11y-test-runner';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { Page } from '@playwright/test';
import pa11y from 'pa11y';

// Mock the services
jest.mock('@/utils/services/error-handler-service');
jest.mock('@/utils/services/configuration-service');
jest.mock('pa11y');

describe('Pa11yTestRunner', () => {
    let pa11yTestRunner: Pa11yTestRunner;
    let mockPage: jest.Mocked<Page>;
    let mockErrorHandler: jest.Mocked<ErrorHandlerService>;
    let mockConfigService: jest.Mocked<ConfigurationService>;

    beforeEach(() => {
        // Reset all mocks
        jest.clearAllMocks();

        // Mock ErrorHandlerService
        mockErrorHandler = {
            executeWithErrorHandling: jest.fn(),
            handleError: jest.fn(),
            createSuccess: jest.fn(),
            executeWithErrorHandlingSync: jest.fn(),
            withTimeout: jest.fn(),
            retryWithBackoff: jest.fn(),
            logDebug: jest.fn(),
            logInfo: jest.fn(),
            logWarning: jest.fn(),
            logSuccess: jest.fn(),
            isErrorResult: jest.fn(),
            isSuccessResult: jest.fn(),
            executeWithRetry: jest.fn(),
        } as any;

        // Mock ConfigurationService
        mockConfigService = {
            getPa11yConfiguration: jest.fn(),
            getConfiguration: jest.fn(),
            updateConfiguration: jest.fn(),
        } as any;

        // Mock the static getInstance methods
        (ErrorHandlerService.getInstance as jest.Mock).mockReturnValue(mockErrorHandler);
        (ConfigurationService.getInstance as jest.Mock).mockReturnValue(mockConfigService);

        // Mock Playwright Page
        mockPage = {
            url: jest.fn().mockReturnValue('https://example.com'),
        } as any;

        // Default: withTimeout and retryWithBackoff call the function argument
        mockErrorHandler.withTimeout.mockImplementation(async (fn: any, ...args) => {
            if (typeof fn === 'function') {
                const result = await fn();
                return { success: true, data: result };
            }
            return { success: true, data: fn };
        });
        mockErrorHandler.retryWithBackoff.mockImplementation(async (fn: any, ...args) => {
            if (typeof fn === 'function') {
                const result = await fn();
                return { success: true, data: result };
            }
            return { success: true, data: fn };
        });

        // Create the runner instance
        pa11yTestRunner = new Pa11yTestRunner(mockPage);
    });

    describe('Constructor', () => {
        test('should create instance with page', () => {
            expect(pa11yTestRunner).toBeInstanceOf(Pa11yTestRunner);
        });
    });

    describe('runAnalysis', () => {
        test('should run analysis successfully', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [
                    {
                        code: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                        type: 'error',
                        message: 'Images must have alternate text',
                        context: '<img src="test.jpg">',
                        selector: 'img',
                        runner: 'pa11y',
                        runnerExtras: {},
                    },
                ],
            };

            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock pa11y to return results
            (pa11y as unknown as jest.Mock).mockResolvedValue(mockPa11yResult);

            // Mock the error handler to return success
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: true,
                data: mockPa11yResult,
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(true);
            expect(result.data).toEqual(mockPa11yResult);
            expect(mockErrorHandler.withTimeout).toHaveBeenCalledWith(
                expect.anything(),
                30000,
                'Pa11y analysis'
            );
            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith('Analyzing: https://example.com');
        });

        test('should handle analysis timeout', async () => {
            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 5000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return timeout error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Pa11y analysis timed out'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Pa11y analysis timed out');
        });

        test('should handle pa11y errors', async () => {
            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Pa11y analysis failed'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Pa11y analysis failed');
        });
    });

    describe('runAnalysisWithRetry', () => {
        test('should run analysis with retry successfully', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [],
            };

            // Mock the error handler to return success
            mockErrorHandler.retryWithBackoff.mockResolvedValue({
                success: true,
                data: mockPa11yResult,
            });

            const result = await pa11yTestRunner.runAnalysisWithRetry(3);

            expect(result.success).toBe(true);
            expect(result.data).toEqual(mockPa11yResult);
            expect(mockErrorHandler.retryWithBackoff).toHaveBeenCalledWith(
                expect.any(Function),
                3,
                'Pa11y analysis with retry'
            );
        });

        test('should handle retry failures', async () => {
            // Mock the error handler to return error after retries
            mockErrorHandler.retryWithBackoff.mockResolvedValue({
                success: false,
                error: new Error('All retries failed'),
            });

            const result = await pa11yTestRunner.runAnalysisWithRetry(2);

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('All retries failed');
        });

        test('should use default max retries', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [],
            };

            // Mock the error handler to return success
            mockErrorHandler.retryWithBackoff.mockResolvedValue({
                success: true,
                data: mockPa11yResult,
            });

            await pa11yTestRunner.runAnalysisWithRetry();

            expect(mockErrorHandler.retryWithBackoff).toHaveBeenCalledWith(
                expect.any(Function),
                3, // Default max retries
                'Pa11y analysis with retry'
            );
        });
    });

    describe('run', () => {
        test('should run successfully and return formatted results', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [
                    {
                        code: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                        type: 'error',
                        message: 'Images must have alternate text',
                        context: '<img src="test.jpg">',
                        selector: 'img',
                        runner: 'pa11y',
                        runnerExtras: {},
                    },
                    {
                        code: 'WCAG2AA.Principle2.Guideline2_1.2_1_1',
                        type: 'warning',
                        message: 'Keyboard navigation issue',
                        context: '<button>Click me</button>',
                        selector: 'button',
                        runner: 'pa11y',
                        runnerExtras: {},
                    },
                ],
            };

            // Mock the runAnalysis method
            jest.spyOn(pa11yTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockPa11yResult,
            });

            const result = await pa11yTestRunner.run();

            expect(result.status).toBe('success');
            expect(result.data).toEqual({
                tool: 'pa11y',
                violations: [
                    {
                        id: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                        code: 'WCAG2AA.Principle1.Guideline1_1.1_1_1',
                        description: 'Images must have alternate text',
                        impact: 'critical',
                        tags: ['WCAG2AA.Principle1.Guideline1_1.1_1_1'],
                        helpUrl: 'https://www.w3.org/TR/WCAG21/#1_1_1',
                        nodes: [{
                            html: '<img src="test.jpg">',
                            target: ['img'],
                            failureSummary: 'Images must have alternate text',
                        }],
                    },
                    {
                        id: 'WCAG2AA.Principle2.Guideline2_1.2_1_1',
                        code: 'WCAG2AA.Principle2.Guideline2_1.2_1_1',
                        description: 'Keyboard navigation issue',
                        impact: 'moderate',
                        tags: ['WCAG2AA.Principle2.Guideline2_1.2_1_1'],
                        helpUrl: 'https://www.w3.org/TR/WCAG21/#2_1_1',
                        nodes: [{
                            html: '<button>Click me</button>',
                            target: ['button'],
                            failureSummary: 'Keyboard navigation issue',
                        }],
                    },
                ],
                timestamp: expect.any(String),
            });
            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith('Starting Pa11y analysis');
            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith('Pa11y analysis completed successfully', {
                issues: 2,
            });
        });

        test('should handle analysis errors', async () => {
            // Mock the runAnalysis method to return error
            jest.spyOn(pa11yTestRunner, 'runAnalysis').mockResolvedValue({
                success: false,
                error: new Error('Pa11y analysis failed'),
            });

            const result = await pa11yTestRunner.run();

            expect(result.status).toBe('error');
            expect(result.error).toBe('Pa11y analysis failed');
            expect(mockErrorHandler.handleError).toHaveBeenCalled();
        });

        test('should handle unexpected errors', async () => {
            // Mock the runAnalysis method to throw an error
            jest.spyOn(pa11yTestRunner, 'runAnalysis').mockRejectedValue(new Error('Unexpected error'));

            const result = await pa11yTestRunner.run();

            expect(result.status).toBe('error');
            expect(result.error).toBe('Unexpected error');
            expect(mockErrorHandler.handleError).toHaveBeenCalled();
        });

        test('should handle null/undefined results', async () => {
            // Mock the runAnalysis method to return success with null data
            jest.spyOn(pa11yTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: {
                    documentTitle: 'Test Page',
                    pageUrl: 'https://example.com',
                    issues: undefined,
                } as unknown as Pa11yResult,
            });

            const result = await pa11yTestRunner.run();

            expect(result.status).toBe('success');
            expect(result.data).toEqual({
                tool: 'pa11y',
                violations: [],
                timestamp: expect.any(String),
            });
        });

        test('should handle empty issues array', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [],
            };

            // Mock the runAnalysis method
            jest.spyOn(pa11yTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockPa11yResult,
            });

            const result = await pa11yTestRunner.run();

            expect(result.status).toBe('success');
            expect(result.data.violations).toEqual([]);
        });
    });

    describe('performPa11yAnalysis (private method)', () => {
        test('should configure pa11y with correct options', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [],
            };

            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: { args: ['--no-sandbox'] },
            });

            // Mock pa11y to return results
            (pa11y as unknown as jest.Mock).mockResolvedValue(mockPa11yResult);

            // Mock the error handler to execute the function
            mockErrorHandler.withTimeout.mockImplementation(async (fn: any) => {
                if (typeof fn === 'function') {
                    const result = await fn();
                    return { success: true, data: result };
                }
                return { success: true, data: fn };
            });

            await pa11yTestRunner.runAnalysis();

            expect(pa11y).toHaveBeenCalledWith('https://example.com', {
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                timeout: 30000,
                wait: 1000,
                chromeLaunchConfig: { args: ['--no-sandbox'] },
                actions: [],
                hideElements: '',
                ignore: [],
            });
        });

        test('should handle pa11y timeout', async () => {
            // Mock configuration to prevent errors
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 5000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return timeout error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Pa11y analysis timed out'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Pa11y analysis timed out');
        });

        test('should handle invalid pa11y results', async () => {
            // Mock configuration to prevent errors
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Pa11y returned invalid results'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Pa11y returned invalid results');
        });

        test('should filter notices when too many issues', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: Array.from({ length: 600 }, (_, i) => ({
                    code: `WCAG2AA.${i}`,
                    type: i < 100 ? 'error' : 'notice',
                    message: `Issue ${i}`,
                    context: `<div>Issue ${i}</div>`,
                    selector: `div:nth-child(${i})`,
                    runner: 'pa11y',
                    runnerExtras: {},
                })),
            };

            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock pa11y to return results
            (pa11y as unknown as jest.Mock).mockResolvedValue(mockPa11yResult);

            // Mock the error handler to execute the function
            mockErrorHandler.withTimeout.mockImplementation(async (fn: any) => {
                if (typeof fn === 'function') {
                    const result = await fn();
                    return { success: true, data: result };
                }
                return { success: true, data: fn };
            });

            await pa11yTestRunner.runAnalysis();

            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith(
                'Filtered 500 notices to focus on actionable issues'
            );
        });

        test('should log analysis progress', async () => {
            const mockPa11yResult: Pa11yResult = {
                documentTitle: 'Test Page',
                pageUrl: 'https://example.com',
                issues: [],
            };

            // Mock configuration
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock pa11y to return results
            (pa11y as unknown as jest.Mock).mockResolvedValue(mockPa11yResult);

            // Mock the error handler to execute the function
            mockErrorHandler.withTimeout.mockImplementation(async (fn: any) => {
                if (typeof fn === 'function') {
                    const result = await fn();
                    return { success: true, data: result };
                }
                return { success: true, data: fn };
            });

            await pa11yTestRunner.runAnalysis();

            expect(mockErrorHandler.logSuccess).toHaveBeenCalledWith(
                expect.stringMatching(/Pa11y analysis completed in \d+ms: 0 issues found/)
            );
        });
    });

    describe('mapPa11yTypeToImpact (private method)', () => {
        test('should map error type to critical impact', () => {
            // Access the private method through the class instance
            const result = (pa11yTestRunner as any).mapPa11yTypeToImpact('error');
            expect(result).toBe('critical');
        });

        test('should map warning type to moderate impact', () => {
            const result = (pa11yTestRunner as any).mapPa11yTypeToImpact('warning');
            expect(result).toBe('moderate');
        });

        test('should map notice type to minor impact', () => {
            const result = (pa11yTestRunner as any).mapPa11yTypeToImpact('notice');
            expect(result).toBe('minor');
        });

        test('should map unknown type to moderate impact', () => {
            const result = (pa11yTestRunner as any).mapPa11yTypeToImpact('unknown');
            expect(result).toBe('moderate');
        });

        test('should handle case insensitive mapping', () => {
            expect((pa11yTestRunner as any).mapPa11yTypeToImpact('ERROR')).toBe('critical');
            expect((pa11yTestRunner as any).mapPa11yTypeToImpact('Warning')).toBe('moderate');
            expect((pa11yTestRunner as any).mapPa11yTypeToImpact('NOTICE')).toBe('minor');
        });
    });

    describe('Error Handling', () => {
        test('should handle pa11y promise rejection', async () => {
            // Mock configuration to prevent errors
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Pa11y promise rejected'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Pa11y promise rejected');
        });

        test('should handle configuration errors', async () => {
            // Mock configuration to prevent errors
            mockConfigService.getPa11yConfiguration.mockReturnValue({
                timeout: 30000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                wait: 1000,
                chromeLaunchConfig: {},
            });

            // Mock the error handler to return error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Configuration error'),
            });

            const result = await pa11yTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Configuration error');
        });
    });
}); 