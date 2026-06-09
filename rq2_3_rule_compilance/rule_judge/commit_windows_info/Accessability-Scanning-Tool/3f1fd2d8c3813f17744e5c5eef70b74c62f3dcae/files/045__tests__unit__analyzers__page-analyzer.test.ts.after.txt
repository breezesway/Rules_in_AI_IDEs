import { PageAnalyzer, PageAnalysisResult } from '@/utils/analyzers/page-analyzer';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { Page } from '@playwright/test';

// Mock the services
jest.mock('@/utils/services/error-handler-service');

describe('PageAnalyzer', () => {
    let pageAnalyzer: PageAnalyzer;
    let mockPage: jest.Mocked<Page>;
    let mockErrorHandler: jest.Mocked<ErrorHandlerService>;

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

        // Mock the static getInstance method
        (ErrorHandlerService.getInstance as jest.Mock).mockReturnValue(mockErrorHandler);

        // Mock Playwright Page
        mockPage = {
            title: jest.fn(),
            evaluate: jest.fn(),
            viewportSize: jest.fn(),
            setViewportSize: jest.fn(),
        } as any;

        // Create the analyzer instance
        pageAnalyzer = new PageAnalyzer(mockPage);
    });

    describe('Constructor', () => {
        test('should create instance with page', () => {
            expect(pageAnalyzer).toBeInstanceOf(PageAnalyzer);
        });
    });

    describe('analyzeCurrentPage', () => {
        test('should perform comprehensive page analysis successfully', async () => {
            const mockAnalysisResult: PageAnalysisResult = {
                title: 'Test Page',
                headingStructure: [
                    { level: 1, text: 'Main Heading', tagName: 'h1' },
                    { level: 2, text: 'Sub Heading', tagName: 'h2' },
                ],
                landmarks: { main: true, nav: true, footer: false },
                skipLink: { exists: true, isVisible: true, targetExists: true },
                images: [
                    { src: 'test.jpg', alt: 'Test Image', hasAlt: true },
                ],
                links: [
                    { text: 'Test Link', href: '/test', hasAriaLabel: false },
                ],
                forms: [
                    {
                        hasLabel: true,
                        labelText: 'Test Input',
                        inputType: 'text',
                        isRequired: false,
                        hasAriaLabel: false,
                    },
                ],
                keyboardNavigation: [
                    { element: 'button', canFocus: true, hasVisibleFocus: true },
                ],
                responsive: { mobile: true, tablet: true, desktop: true },
            };

            // Mock the error handler to return success
            mockErrorHandler.executeWithErrorHandling.mockResolvedValue({
                success: true,
                data: mockAnalysisResult,
            });

            // Mock individual analysis methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce(mockAnalysisResult.headingStructure)
                .mockResolvedValueOnce(mockAnalysisResult.landmarks)
                .mockResolvedValueOnce(mockAnalysisResult.skipLink)
                .mockResolvedValueOnce(mockAnalysisResult.images)
                .mockResolvedValueOnce(mockAnalysisResult.links)
                .mockResolvedValueOnce(mockAnalysisResult.forms)
                .mockResolvedValueOnce(mockAnalysisResult.keyboardNavigation)
                .mockResolvedValueOnce(mockAnalysisResult.responsive);

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data).toEqual(mockAnalysisResult);
            expect(mockErrorHandler.executeWithErrorHandling).toHaveBeenCalledWith(
                expect.any(Function),
                'analyzeCurrentPage'
            );
        });

        test('should handle analysis errors gracefully', async () => {
            // Mock the error handler to return error
            mockErrorHandler.executeWithErrorHandling.mockResolvedValue({
                success: false,
                error: new Error('Analysis failed'),
            });

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Analysis failed');
        });

        test('should handle page title errors', async () => {
            // Mock page.title to throw an error
            mockPage.title.mockRejectedValue(new Error('Title error'));

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                try {
                    const result = await fn();
                    return { success: true, data: result };
                } catch (error) {
                    return { success: false, error: new Error('Analysis failed') };
                }
            });

            // Mock other analysis methods to succeed
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.title).toBe('Unable to retrieve page title');
        });

        test('should handle responsive analysis errors', async () => {
            // Mock viewportSize to return null
            mockPage.viewportSize.mockReturnValue(null);
            mockPage.setViewportSize.mockRejectedValue(new Error('Viewport error'));

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                try {
                    const result = await fn();
                    return { success: true, data: result };
                } catch (error) {
                    return { success: false, error: new Error('Analysis failed') };
                }
            });

            // Mock other analysis methods to succeed
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]); // keyboardNavigation

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.responsive).toEqual({ mobile: false, tablet: false, desktop: false });
        });
    });

    describe('Heading Structure Analysis', () => {
        test('should analyze heading structure correctly', async () => {
            const mockHeadings = [
                { level: 1, text: 'Main Title', tagName: 'h1' },
                { level: 2, text: 'Section 1', tagName: 'h2' },
                { level: 3, text: 'Subsection', tagName: 'h3' },
            ];

            mockPage.evaluate.mockResolvedValue(mockHeadings);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce(mockHeadings) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.headingStructure).toEqual(mockHeadings);
        });

        test('should handle empty heading structure', async () => {
            mockPage.evaluate.mockResolvedValue([]);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.headingStructure).toEqual([]);
        });
    });

    describe('Landmarks Analysis', () => {
        test('should analyze landmarks correctly', async () => {
            const mockLandmarks = { main: true, nav: true, footer: true };

            mockPage.evaluate.mockResolvedValue(mockLandmarks);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce(mockLandmarks) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.landmarks).toEqual(mockLandmarks);
        });
    });

    describe('Skip Link Analysis', () => {
        test('should analyze skip link when it exists', async () => {
            const mockSkipLink = { exists: true, isVisible: true, targetExists: true };

            mockPage.evaluate.mockResolvedValue(mockSkipLink);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce(mockSkipLink) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.skipLink).toEqual(mockSkipLink);
        });

        test('should handle missing skip link', async () => {
            const mockSkipLink = { exists: false, isVisible: false, targetExists: false };

            mockPage.evaluate.mockResolvedValue(mockSkipLink);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce(mockSkipLink) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.skipLink).toEqual(mockSkipLink);
        });
    });

    describe('Images Analysis', () => {
        test('should analyze images correctly', async () => {
            const mockImages = [
                { src: 'image1.jpg', alt: 'Image 1', hasAlt: true },
                { src: 'image2.jpg', alt: '', hasAlt: false },
                { src: 'image3.jpg', alt: 'Image 3', hasAlt: true, ariaLabel: 'Aria Label' },
            ];

            mockPage.evaluate.mockResolvedValue(mockImages);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce(mockImages) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.images).toEqual(mockImages);
        });
    });

    describe('Links Analysis', () => {
        test('should analyze links correctly', async () => {
            const mockLinks = [
                { text: 'Home', href: '/', hasAriaLabel: false },
                { text: 'About', href: '/about', hasAriaLabel: true, ariaLabel: 'About Us' },
                { text: '', href: '/contact', hasAriaLabel: false },
            ];

            mockPage.evaluate.mockResolvedValue(mockLinks);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce(mockLinks) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.links).toEqual(mockLinks);
        });
    });

    describe('Forms Analysis', () => {
        test('should analyze forms correctly', async () => {
            const mockForms = [
                {
                    hasLabel: true,
                    labelText: 'Username',
                    inputType: 'text',
                    isRequired: true,
                    hasAriaLabel: false,
                },
                {
                    hasLabel: false,
                    labelText: '',
                    inputType: 'password',
                    isRequired: false,
                    hasAriaLabel: true,
                },
            ];

            mockPage.evaluate.mockResolvedValue(mockForms);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce(mockForms) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.forms).toEqual(mockForms);
        });
    });

    describe('Keyboard Navigation Analysis', () => {
        test('should analyze keyboard navigation correctly', async () => {
            const mockKeyboardNav = [
                { element: 'button', canFocus: true, hasVisibleFocus: true },
                { element: 'input', canFocus: true, hasVisibleFocus: false },
            ];

            mockPage.evaluate.mockResolvedValue(mockKeyboardNav);

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce(mockKeyboardNav) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.keyboardNavigation).toEqual(mockKeyboardNav);
        });
    });

    describe('Responsive Analysis', () => {
        test('should analyze responsiveness correctly', async () => {
            const mockResponsive = { mobile: true, tablet: true, desktop: true };

            // Mock viewport methods
            mockPage.viewportSize.mockReturnValue({ width: 1920, height: 1080 });
            mockPage.setViewportSize.mockResolvedValue();
            mockPage.evaluate.mockResolvedValue(true); // checkViewportUsability

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce(true) // mobile checkViewportUsability
                .mockResolvedValueOnce(true) // tablet checkViewportUsability
                .mockResolvedValueOnce(true); // desktop checkViewportUsability

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.responsive).toEqual(mockResponsive);
        });

        test('should handle responsive analysis errors', async () => {
            // Mock viewport methods to throw errors
            mockPage.viewportSize.mockReturnValue(null);
            mockPage.setViewportSize.mockRejectedValue(new Error('Viewport error'));

            // Mock the error handler to execute the function
            mockErrorHandler.executeWithErrorHandling.mockImplementation(async (fn) => {
                const result = await fn();
                return { success: true, data: result };
            });

            // Mock other methods
            mockPage.title.mockResolvedValue('Test Page');
            mockPage.evaluate
                .mockResolvedValueOnce([]) // headingStructure
                .mockResolvedValueOnce({ main: false, nav: false, footer: false }) // landmarks
                .mockResolvedValueOnce({ exists: false, isVisible: false, targetExists: false }) // skipLink
                .mockResolvedValueOnce([]) // images
                .mockResolvedValueOnce([]) // links
                .mockResolvedValueOnce([]) // forms
                .mockResolvedValueOnce([]) // keyboardNavigation
                .mockResolvedValueOnce({ mobile: false, tablet: false, desktop: false }); // responsive

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(true);
            expect(result.data?.responsive).toEqual({ mobile: false, tablet: false, desktop: false });
        });
    });

    describe('Error Handling', () => {
        test('should handle page.evaluate errors', async () => {
            // Mock page.evaluate to throw an error
            mockPage.evaluate.mockRejectedValue(new Error('Evaluate error'));

            // Mock the error handler to return error
            mockErrorHandler.executeWithErrorHandling.mockResolvedValue({
                success: false,
                error: new Error('Page analysis failed'),
            });

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Page analysis failed');
        });

        test('should handle multiple analysis failures', async () => {
            // Mock multiple methods to fail
            mockPage.title.mockRejectedValue(new Error('Title error'));
            mockPage.evaluate.mockRejectedValue(new Error('Evaluate error'));

            // Mock the error handler to return error
            mockErrorHandler.executeWithErrorHandling.mockResolvedValue({
                success: false,
                error: new Error('Multiple analysis failures'),
            });

            const result = await pageAnalyzer.analyzeCurrentPage();

            expect(result.success).toBe(false);
            expect(result.error?.message).toBe('Multiple analysis failures');
        });
    });
}); 