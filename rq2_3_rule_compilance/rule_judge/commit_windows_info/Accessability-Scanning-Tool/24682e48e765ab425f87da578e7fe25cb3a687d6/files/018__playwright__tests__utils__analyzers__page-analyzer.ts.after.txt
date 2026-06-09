import { Page } from '@playwright/test';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';

export interface PageAnalysisResult {
    title: string;
    headingStructure: Array<{ level: number; text: string; tagName: string }>;
    landmarks: { main: boolean; nav: boolean; footer: boolean };
    skipLink: { exists: boolean; isVisible: boolean; targetExists: boolean };
    images: Array<{ src: string; alt: string; hasAlt: boolean; ariaLabel?: string }>;
    links: Array<{ text: string; href: string; hasAriaLabel: boolean; ariaLabel?: string }>;
    forms: Array<{
        hasLabel: boolean;
        labelText: string;
        inputType: string;
        isRequired: boolean;
        hasAriaLabel: boolean;
    }>;
    keyboardNavigation: Array<{ element: string; canFocus: boolean; hasVisibleFocus: boolean }>;
    responsive?: { mobile: boolean; tablet: boolean; desktop: boolean };
}

export class PageAnalyzer {
    private errorHandler = ErrorHandlerService.getInstance();

    constructor(private page: Page) { }

    /**
     * Performs comprehensive page analysis
     */
    async analyzeCurrentPage(): Promise<ServiceResult<PageAnalysisResult>> {
        return this.errorHandler.executeWithErrorHandling(async () => {
            const [
                title,
                headingStructure,
                landmarks,
                skipLink,
                images,
                links,
                forms,
                keyboardNavigation,
                responsive,
            ] = await Promise.all([
                this.analyzeTitle(),
                this.analyzeHeadingStructure(),
                this.analyzeLandmarks(),
                this.analyzeSkipLink(),
                this.analyzeImages(),
                this.analyzeLinks(),
                this.analyzeForms(),
                this.analyzeKeyboardNavigation(),
                this.analyzeResponsiveness(),
            ]);

            return {
                title,
                headingStructure,
                landmarks,
                skipLink,
                images,
                links,
                forms,
                keyboardNavigation,
                responsive,
            };
        }, 'analyzeCurrentPage');
    }

    /**
     * Analyzes page title
     */
    private async analyzeTitle(): Promise<string> {
        try {
            return await this.page.title();
        } catch (error) {
            return 'Unable to retrieve page title';
        }
    }

    /**
     * Analyzes heading structure
     */
    private async analyzeHeadingStructure(): Promise<PageAnalysisResult['headingStructure']> {
        return await this.page.evaluate(() => {
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            return Array.from(headings).map(heading => ({
                level: parseInt(heading.tagName.charAt(1), 10),
                text: heading.textContent?.trim() || '',
                tagName: heading.tagName.toLowerCase(),
            }));
        });
    }

    /**
     * Analyzes landmarks
     */
    private async analyzeLandmarks(): Promise<PageAnalysisResult['landmarks']> {
        return await this.page.evaluate(() => {
            return {
                main: document.querySelector('main, [role="main"]') !== null,
                nav: document.querySelector('nav, [role="navigation"]') !== null,
                footer: document.querySelector('footer, [role="contentinfo"]') !== null,
            };
        });
    }

    /**
     * Analyzes skip link
     */
    private async analyzeSkipLink(): Promise<PageAnalysisResult['skipLink']> {
        return await this.page.evaluate(() => {
            const skipLink = document.querySelector('a[href^="#"]');

            if (!skipLink) {
                return { exists: false, isVisible: false, targetExists: false };
            }

            const href = skipLink.getAttribute('href');
            const target = href ? document.querySelector(href) : null;

            const computedStyle = window.getComputedStyle(skipLink);
            const isVisible = computedStyle.display !== 'none' &&
                computedStyle.visibility !== 'hidden' &&
                computedStyle.opacity !== '0';

            return {
                exists: true,
                isVisible,
                targetExists: target !== null,
            };
        });
    }

    /**
     * Analyzes images
     */
    private async analyzeImages(): Promise<PageAnalysisResult['images']> {
        return await this.page.evaluate(() => {
            const images = document.querySelectorAll('img');
            return Array.from(images).map(img => {
                const alt = img.getAttribute('alt') || '';
                const ariaLabel = img.getAttribute('aria-label') || '';

                return {
                    src: img.src,
                    alt,
                    hasAlt: alt !== '',
                    ariaLabel: ariaLabel || undefined,
                };
            });
        });
    }

    /**
     * Analyzes links
     */
    private async analyzeLinks(): Promise<PageAnalysisResult['links']> {
        return await this.page.evaluate(() => {
            const links = document.querySelectorAll('a[href]');
            return Array.from(links).map(link => {
                const text = link.textContent?.trim() || '';
                const href = link.getAttribute('href') || '';
                const ariaLabel = link.getAttribute('aria-label') || '';

                return {
                    text,
                    href,
                    hasAriaLabel: ariaLabel !== '',
                    ariaLabel: ariaLabel || undefined,
                };
            });
        });
    }

    /**
     * Analyzes forms
     */
    private async analyzeForms(): Promise<PageAnalysisResult['forms']> {
        return await this.page.evaluate(() => {
            const inputs = document.querySelectorAll('input, select, textarea');
            return Array.from(inputs).map(input => {
                const id = input.getAttribute('id') || '';
                const label = id ? document.querySelector(`label[for="${id}"]`) : null;
                const ariaLabel = input.getAttribute('aria-label') || '';
                const type = input.getAttribute('type') || input.tagName.toLowerCase();
                const required = input.hasAttribute('required');

                return {
                    hasLabel: label !== null,
                    labelText: label?.textContent?.trim() || '',
                    inputType: type,
                    isRequired: required,
                    hasAriaLabel: ariaLabel !== '',
                };
            });
        });
    }

    /**
     * Analyzes keyboard navigation
     */
    private async analyzeKeyboardNavigation(): Promise<PageAnalysisResult['keyboardNavigation']> {
        return await this.page.evaluate(() => {
            const focusableElements = document.querySelectorAll(
                'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );

            return Array.from(focusableElements).map(element => {
                const tagName = element.tagName.toLowerCase();
                const canFocus = element.tabIndex >= 0;

                // Check if element has visible focus styles
                const computedStyle = window.getComputedStyle(element);
                const hasVisibleFocus = computedStyle.outline !== 'none' ||
                    computedStyle.outlineWidth !== '0px' ||
                    computedStyle.boxShadow !== 'none';

                return {
                    element: tagName,
                    canFocus,
                    hasVisibleFocus,
                };
            });
        });
    }

    /**
     * Analyzes responsive design
     */
    private async analyzeResponsiveness(): Promise<PageAnalysisResult['responsive']> {
        const originalViewport = this.page.viewportSize();

        try {
            // Test mobile viewport
            await this.page.setViewportSize({ width: 375, height: 667 });
            const mobile = await this.checkViewportUsability();

            // Test tablet viewport
            await this.page.setViewportSize({ width: 768, height: 1024 });
            const tablet = await this.checkViewportUsability();

            // Test desktop viewport
            await this.page.setViewportSize({ width: 1920, height: 1080 });
            const desktop = await this.checkViewportUsability();

            return { mobile, tablet, desktop };
        } catch (error) {
            return { mobile: false, tablet: false, desktop: false };
        } finally {
            // Restore original viewport
            if (originalViewport) {
                await this.page.setViewportSize(originalViewport);
            }
        }
    }

    /**
     * Checks if current viewport is usable
     */
    private async checkViewportUsability(): Promise<boolean> {
        return await this.page.evaluate(() => {
            // Check if content is readable and clickable
            const body = document.body;
            const hasHorizontalScroll = body.scrollWidth > window.innerWidth;
            const hasOverflowingText = document.querySelector('*:is(h1, h2, h3, h4, h5, h6, p, li)')
                ? Array.from(document.querySelectorAll('*:is(h1, h2, h3, h4, h5, h6, p, li)'))
                    .some(el => el.scrollWidth > el.clientWidth)
                : false;

            return !hasHorizontalScroll && !hasOverflowingText;
        });
    }
} 