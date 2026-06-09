import { AxeTestRunner, AxeTestOptions } from '@/utils/runners/axe-test-runner';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { Page } from '@playwright/test';
import { AxeResults } from 'axe-core';

// Mock the services
jest.mock('@/utils/services/error-handler-service');
jest.mock('@/utils/services/configuration-service');
jest.mock('@axe-core/playwright');

describe('AxeTestRunner', () => {
    let axeTestRunner: AxeTestRunner;
    let mockPage: jest.Mocked<Page>;
    let mockErrorHandler: jest.Mocked<ErrorHandlerService>;
    let mockConfigService: jest.Mocked<ConfigurationService>;
    let mockAxeBuilder: any;

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

        // Default: withTimeout and executeWithErrorHandling call the function argument
        mockErrorHandler.withTimeout.mockImplementation(async (fn: any, ...args) => {
            if (typeof fn === 'function') {
                const result = await fn();
                return { success: true, data: result };
            }
            return { success: true, data: fn };
        });
        mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn: any, ...args) => {
            if (typeof fn === 'function') {
                const result = await fn();
                return { success: true, data: result };
            }
            return { success: true, data: fn };
        });

        // Mock ConfigurationService
        mockConfigService = {
            getAxeConfiguration: jest.fn(),
            getConfiguration: jest.fn(),
            updateConfiguration: jest.fn(),
        } as any;

        // Mock the static getInstance methods
        (ErrorHandlerService.getInstance as jest.Mock).mockReturnValue(mockErrorHandler);
        (ConfigurationService.getInstance as jest.Mock).mockReturnValue(mockConfigService);

        // Mock Playwright Page
        mockPage = {
            addScriptTag: jest.fn(),
        } as any;

        // Mock AxeBuilder
        mockAxeBuilder = {
            include: jest.fn().mockReturnThis(),
            exclude: jest.fn().mockReturnThis(),
            withTags: jest.fn().mockReturnThis(),
            withRules: jest.fn().mockReturnThis(),
            disableRules: jest.fn().mockReturnThis(),
            analyze: jest.fn().mockResolvedValue({
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            }),
        };

        // Mock the AxeBuilder constructor
        const { AxeBuilder } = require('@axe-core/playwright');
        AxeBuilder.mockImplementation(() => mockAxeBuilder);

        // Create the runner instance
        axeTestRunner = new AxeTestRunner(mockPage);
    });

    describe('Constructor', () => {
        test('should create instance with page', () => {
            expect(axeTestRunner).toBeInstanceOf(AxeTestRunner);
        });
    });

    describe('injectAxe', () => {
        test('should inject axe-core successfully', async () => {
            // Override the error handler to call the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn: any, ...args) => {
                if (typeof fn === 'function') {
                    const result = await fn();
                    return { success: true, data: result };
                }
                return { success: true, data: fn };
            });

            // Mock page.addScriptTag to resolve
            mockPage.addScriptTag.mockResolvedValue({} as any);

            const result = await axeTestRunner.injectAxe();

            expect(result.success).toBe(true);
            expect(mockPage.addScriptTag).toHaveBeenCalledWith({
                url: 'https://unpkg.com/axe-core@4.8.2/axe.min.js',
            });
            expect(mockErrorHandler.executeWithErrorHandling).toHaveBeenCalledWith(
                expect.any(Function),
                'injectAxe'
            );
        });

        test('should handle injection errors', async () => {
            // Mock the error handler to return error
            mockErrorHandler.executeWithErrorHandling.mockResolvedValue({
                success: false,
                error: new Error('Injection failed'),
            });

            const result = await axeTestRunner.injectAxe();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Injection failed');
        });
    });

    describe('runAnalysis', () => {
        test('should run analysis with default options successfully', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock configuration
            mockConfigService.getAxeConfiguration.mockReturnValue({
                timeout: 30000,
            });

            // Mock the error handler to return success
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runAnalysis();

            expect(result.success).toBe(true);
            expect(result.data).toEqual(mockResults);
            expect(mockErrorHandler.withTimeout).toHaveBeenCalledWith(
                expect.anything(),
                30000,
                'axe-core analysis'
            );
        });

        test('should run analysis with custom options', async () => {
            const options: AxeTestOptions = {
                tags: ['wcag2a', 'wcag2aa'],
                rules: {
                    'color-contrast': { enabled: true },
                },
            };

            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock configuration
            mockConfigService.getAxeConfiguration.mockReturnValue({
                timeout: 30000,
            });

            // Mock the error handler to return success
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runAnalysis(options);

            expect(result.success).toBe(true);
            expect(result.data).toEqual(mockResults);
        });

        test('should handle analysis timeout', async () => {
            // Mock configuration
            mockConfigService.getAxeConfiguration.mockReturnValue({
                timeout: 5000,
            });

            // Mock the error handler to return timeout error
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Analysis timed out'),
            });

            const result = await axeTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Analysis timed out');
        });

        test('should use default timeout when config is null', async () => {
            // Mock configuration to return null
            mockConfigService.getAxeConfiguration.mockReturnValue(null);

            // Mock the error handler to return success
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: true,
                data: {} as AxeResults,
            });

            await axeTestRunner.runAnalysis();

            expect(mockErrorHandler.withTimeout).toHaveBeenCalledWith(
                expect.anything(), // changed from expect.any(Function)
                30000, // Default timeout
                'axe-core analysis'
            );
        });
    });

    describe('Specialized Analysis Methods', () => {
        test('should run color contrast analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runColorContrastAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.color'],
                rules: {
                    'color-contrast': { enabled: true },
                    'color-contrast-enhanced': { enabled: true },
                },
            });
        });

        test('should run keyboard accessibility analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runKeyboardAccessibilityAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.keyboard'],
                rules: {
                    'focus-order-semantics': { enabled: true },
                    'focusable-content': { enabled: true },
                    tabindex: { enabled: true },
                },
            });
        });

        test('should run ARIA analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runAriaAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.aria'],
                rules: {
                    'aria-valid-attr': { enabled: true },
                    'aria-valid-attr-value': { enabled: true },
                    'aria-required-attr': { enabled: true },
                },
            });
        });

        test('should run form accessibility analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runFormAccessibilityAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.forms'],
                rules: {
                    label: { enabled: true },
                    'label-title-only': { enabled: true },
                    'form-field-multiple-labels': { enabled: true },
                },
            });
        });

        test('should run image accessibility analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runImageAccessibilityAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.text-alternatives'],
                rules: {
                    'image-alt': { enabled: true },
                    'image-redundant-alt': { enabled: true },
                    'input-image-alt': { enabled: true },
                },
            });
        });

        test('should run landmarks and headings analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runLandmarksAndHeadingsAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                tags: ['cat.structure'],
                rules: {
                    'landmark-one-main': { enabled: true },
                    'landmark-no-duplicate-banner': { enabled: true },
                    'landmark-no-duplicate-contentinfo': { enabled: true },
                    'heading-order': { enabled: true },
                    'page-has-heading-one': { enabled: true },
                },
            });
        });
    });

    describe('DevTools Analysis Methods', () => {
        test('should run DevTools analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runDevToolsAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                devtools: true,
                shadow: true,
                iframes: true,
                reporter: 'v2',
                tags: ['wcag2a', 'wcag2aa', 'wcag21aa'],
                rules: expect.objectContaining({
                    'color-contrast': { enabled: true },
                    'aria-valid-attr': { enabled: true },
                }),
            });
        });

        test('should run shadow DOM analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runShadowDOMAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                devtools: true,
                shadow: true,
                reporter: 'v2',
                tags: ['wcag2a', 'wcag2aa'],
            });
        });

        test('should run iframe analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runIframeAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                devtools: true,
                iframes: true,
                reporter: 'v2',
                tags: ['wcag2a', 'wcag2aa'],
                allowedOrigins: ['*'],
            });
        });

        test('should run experimental analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runExperimentalAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                devtools: true,
                shadow: true,
                iframes: true,
                reporter: 'v2',
                tags: ['experimental'],
                rules: expect.objectContaining({
                    'autocomplete-valid': { enabled: true },
                    'target-size': { enabled: true },
                }),
            });
        });

        test('should run comprehensive DevTools analysis', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runComprehensiveDevToolsAnalysis();

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith({
                devtools: true,
                shadow: true,
                iframes: true,
                reporter: 'v2',
                tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag21aaa', 'best-practice', 'experimental'],
                allowedOrigins: ['*'],
            });
        });

        test('should run custom DevTools analysis', async () => {
            const customConfig: Partial<AxeTestOptions> = {
                tags: ['wcag2a'],
                rules: {
                    'color-contrast': { enabled: true },
                },
            };

            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runCustomDevToolsAnalysis(customConfig);

            expect(result.success).toBe(true);
            expect(axeTestRunner.runAnalysis).toHaveBeenCalledWith(customConfig);
        });
    });

    describe('runAxeAnalysis', () => {
        test('should return results when analysis succeeds', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.runAxeAnalysis();

            expect(result).toEqual(mockResults);
        });

        test('should throw error when analysis fails', async () => {
            // Mock the runAnalysis method to return error
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: false,
                error: new Error('Analysis failed'),
            });

            await expect(axeTestRunner.runAxeAnalysis()).rejects.toThrow('Analysis failed');
        });
    });

    describe('run', () => {
        test('should run successfully and return formatted results', async () => {
            const mockResults: AxeResults = {
                violations: [
                    {
                        id: 'color-contrast',
                        impact: 'serious',
                        tags: ['wcag2aa'],
                        description: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                        help: 'Elements must meet minimum color contrast ratio requirements',
                        helpUrl: 'https://dequeuniversity.com/rules/axe/4.8/color-contrast',
                        nodes: [],
                    },
                ],
                passes: [
                    {
                        id: 'html-has-lang',
                        impact: null,
                        tags: ['wcag2a'],
                        description: 'Ensures every HTML document has a lang attribute',
                        help: 'html element must have a lang attribute',
                        helpUrl: 'https://dequeuniversity.com/rules/axe/4.8/html-has-lang',
                        nodes: [],
                    },
                ],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock the runAnalysis method
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: mockResults,
            });

            const result = await axeTestRunner.run();

            expect(result.status).toBe('success');
            expect(result.data).toEqual({
                tool: 'axe-core',
                violations: mockResults.violations,
                passes: mockResults.passes,
                timestamp: expect.any(String),
            });
            expect(mockErrorHandler.logSuccess).toHaveBeenCalledWith(
                'Axe-core analysis completed successfully',
                {
                    violations: 1,
                    passes: 1,
                }
            );
        });

        test('should handle analysis errors', async () => {
            // Mock the runAnalysis method to return error
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: false,
                error: new Error('Analysis failed'),
            });

            const result = await axeTestRunner.run();

            expect(result.status).toBe('error');
            expect(result.error).toBe('Analysis failed');
            expect(mockErrorHandler.handleError).toHaveBeenCalled();
        });

        test('should handle unexpected errors', async () => {
            // Mock the runAnalysis method to throw an error
            jest.spyOn(axeTestRunner, 'runAnalysis').mockRejectedValue(new Error('Unexpected error'));

            const result = await axeTestRunner.run();

            expect(result.status).toBe('error');
            expect(result.error).toBe('Unexpected error');
            expect(mockErrorHandler.handleError).toHaveBeenCalled();
        });

        test('should handle null/undefined results', async () => {
            // Mock the runAnalysis method to return success with empty data
            jest.spyOn(axeTestRunner, 'runAnalysis').mockResolvedValue({
                success: true,
                data: {
                    violations: [],
                    passes: [],
                    incomplete: [],
                    inapplicable: [],
                    timestamp: new Date().toISOString(),
                    url: 'test-url',
                    testEngine: { name: 'axe-core', version: '4.8.2' },
                    testRunner: { name: 'axe' },
                    testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                    toolOptions: {},
                } as AxeResults,
            });

            const result = await axeTestRunner.run();

            expect(result.status).toBe('success');
            expect(result.data).toEqual({
                tool: 'axe-core',
                violations: [],
                passes: [],
                timestamp: expect.any(String),
            });
        });
    });

    describe('performAxeAnalysis (private method)', () => {
        test('should configure AxeBuilder with options correctly', async () => {
            const options: AxeTestOptions = {
                include: ['#main'],
                exclude: ['#sidebar'],
                tags: ['wcag2a'],
                rules: {
                    'color-contrast': { enabled: true },
                    'html-has-lang': { enabled: false },
                },
            };

            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock configuration
            mockConfigService.getAxeConfiguration.mockReturnValue({
                devtools: true,
            });

            // Mock AxeBuilder methods
            mockAxeBuilder.analyze.mockResolvedValue(mockResults);

            // Use default withTimeout mock from beforeEach
            await axeTestRunner.runAnalysis(options);

            expect(mockAxeBuilder.include).toHaveBeenCalledWith(['#main']);
            expect(mockAxeBuilder.exclude).toHaveBeenCalledWith(['#sidebar']);
            expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['wcag2a']);
            expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(['color-contrast', 'html-has-lang']);
            expect(mockAxeBuilder.disableRules).toHaveBeenCalledWith(['html-has-lang']);
            expect(mockAxeBuilder.analyze).toHaveBeenCalled();
        });

        test('should handle AxeBuilder errors', async () => {
            // Mock the error handler to return error directly
            mockErrorHandler.withTimeout.mockResolvedValue({
                success: false,
                error: new Error('Analysis failed'),
            });

            const result = await axeTestRunner.runAnalysis();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Analysis failed');
        });

        test('should log analysis progress', async () => {
            const mockResults: AxeResults = {
                violations: [],
                passes: [],
                incomplete: [],
                inapplicable: [],
                timestamp: new Date().toISOString(),
                url: 'test-url',
                testEngine: { name: 'axe-core', version: '4.8.2' },
                testRunner: { name: 'axe' },
                testEnvironment: { userAgent: 'test', windowWidth: 1920, windowHeight: 1080 },
                toolOptions: {},
            };

            // Mock configuration
            mockConfigService.getAxeConfiguration.mockReturnValue({});

            // Mock AxeBuilder methods
            mockAxeBuilder.analyze.mockResolvedValue(mockResults);

            // Use default withTimeout mock from beforeEach
            await axeTestRunner.runAnalysis();

            expect(mockErrorHandler.logInfo).toHaveBeenCalledWith(
                'Starting axe-core analysis with options',
                { options: {} }
            );
            expect(mockErrorHandler.logSuccess).toHaveBeenCalledWith(
                'Axe-core analysis completed',
                {
                    violations: 0,
                    passes: 0,
                }
            );
        });
    });
}); 