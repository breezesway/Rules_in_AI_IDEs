import type { Meta, StoryObj } from '@storybook/react';
import { FullSiteScanPage } from '@/components/FullSiteScanPage';

const meta: Meta<typeof FullSiteScanPage> = {
    title: 'Pages/FullSiteScanPage',
    component: FullSiteScanPage,
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
            maxPages: 50,
            maxDepth: 3,
            excludePatterns: ['/admin/*', '/private/*'],
            includePatterns: ['/*'],
            respectRobotsTxt: true,
            delayBetweenRequests: 1000,
        },
    },
};

export const Scanning: Story = {
    args: {
        isScanning: true,
        scanProgress: {
            currentPage: 15,
            totalPages: 50,
            currentUrl: 'https://example.com/about',
            status: 'crawling',
        },
    },
};

export const Analyzing: Story = {
    args: {
        isScanning: true,
        scanProgress: {
            currentPage: 50,
            totalPages: 50,
            currentUrl: 'https://example.com/contact',
            status: 'analyzing',
        },
    },
};

export const WithResults: Story = {
    args: {
        scanResults: {
            siteUrl: 'https://example.com',
            timestamp: new Date().toISOString(),
            summary: {
                totalPages: 50,
                pagesWithViolations: 12,
                totalViolations: 45,
                compliancePercentage: 76,
            },
        },
    },
};

export const WithError: Story = {
    args: {
        error: 'Failed to scan website. Please check the URL and try again.',
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