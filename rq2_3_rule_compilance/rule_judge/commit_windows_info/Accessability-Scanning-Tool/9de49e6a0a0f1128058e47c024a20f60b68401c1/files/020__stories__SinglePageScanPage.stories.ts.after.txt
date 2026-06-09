import type { Meta, StoryObj } from '@storybook/react';
import { SinglePageScanPage } from '@/components/SinglePageScanPage';

const meta: Meta<typeof SinglePageScanPage> = {
    title: 'Pages/SinglePageScanPage',
    component: SinglePageScanPage,
    parameters: {
        layout: 'fullscreen',
        a11y: {
            config: {
                rules: [
                    { id: 'color-contrast', enabled: true },
                    { id: 'heading-order', enabled: true },
                    { id: 'form-field-multiple-labels', enabled: true },
                    { id: 'button-name', enabled: true },
                    { id: 'progressbar-name', enabled: true },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        onScanStart: { action: 'scan-start' },
        onScanComplete: { action: 'scan-complete' },
        onError: { action: 'error' },
    },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {},
};

export const WithInitialUrl: Story = {
    args: {
        initialUrl: 'https://example.com',
    },
};

export const WithScanOptions: Story = {
    args: {
        initialUrl: 'https://example.com',
        scanOptions: {
            tools: ['axe-core', 'pa11y'],
            wcagLevel: 'WCAG2AA',
            includePasses: true,
            includeWarnings: true,
            timeout: 30000,
        },
    },
};

export const Scanning: Story = {
    args: {
        isScanning: true,
        scanProgress: {
            currentStep: 'analyzing',
            totalSteps: 3,
            currentUrl: 'https://example.com',
            status: 'Running accessibility tests...',
        },
    },
};

export const WithResults: Story = {
    args: {
        scanResults: {
            url: 'https://example.com',
            timestamp: new Date().toISOString(),
            tool: 'axe-core',
            violations: [
                {
                    id: 'color-contrast',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    impact: 'serious',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/color-contrast',
                    wcagTags: ['wcag2aa', 'wcag143'],
                    wcagLevel: 'AA',
                    nodes: [
                        {
                            html: '<button class="btn-primary">Submit</button>',
                            target: ['button.btn-primary'],
                            failureSummary: 'Fix any of the following:\n  Element has insufficient color contrast of 2.51 (foreground color: #ffffff, background color: #f0f0f0, font size: 14.0pt (18.6667px), font weight: 400). Expected contrast ratio of 4.5:1',
                        },
                    ],
                },
            ],
            passes: [],
            warnings: [],
            summary: {
                totalViolations: 1,
                totalPasses: 45,
                totalWarnings: 0,
            },
        },
    },
};

export const WithManyViolations: Story = {
    args: {
        scanResults: {
            url: 'https://example.com',
            timestamp: new Date().toISOString(),
            tool: 'axe-core',
            violations: [
                {
                    id: 'color-contrast',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    impact: 'serious',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/color-contrast',
                    wcagTags: ['wcag2aa', 'wcag143'],
                    wcagLevel: 'AA',
                    nodes: [],
                },
                {
                    id: 'heading-order',
                    description: 'Heading levels should only increase by one',
                    impact: 'moderate',
                    help: 'Ensures the order of headings is semantically correct',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/heading-order',
                    wcagTags: ['wcag2aa', 'wcag131'],
                    wcagLevel: 'AA',
                    nodes: [],
                },
                {
                    id: 'button-name',
                    description: 'Buttons must have discernible text',
                    impact: 'critical',
                    help: 'Ensures buttons have accessible names',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.7/button-name',
                    wcagTags: ['wcag2aa', 'wcag412'],
                    wcagLevel: 'AA',
                    nodes: [],
                },
            ],
            passes: [],
            warnings: [],
            summary: {
                totalViolations: 3,
                totalPasses: 42,
                totalWarnings: 0,
            },
        },
    },
};

export const WithError: Story = {
    args: {
        error: 'Failed to scan page. Please check the URL and try again.',
    },
};

export const MobileView: Story = {
    args: {},
    parameters: {
        viewport: {
            defaultViewport: 'mobile1',
        },
    },
}; 