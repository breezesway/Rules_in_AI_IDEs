import type { Meta, StoryObj } from '@storybook/react';
import { ReportsPage } from '@/components/ReportsPage';

const meta: Meta<typeof ReportsPage> = {
    title: 'Pages/ReportsPage',
    component: ReportsPage,
    parameters: {
        layout: 'fullscreen',
        a11y: {
            config: {
                rules: [
                    { id: 'color-contrast', enabled: true },
                    { id: 'heading-order', enabled: true },
                    { id: 'table-fake-caption', enabled: true },
                    { id: 'table-structure', enabled: true },
                    { id: 'button-name', enabled: true },
                    { id: 'link-name', enabled: true },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        onReportDownload: { action: 'report-download' },
    },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {},
};

export const WithReports: Story = {
    args: {
        reports: [
            {
                id: '1',
                siteUrl: 'https://example.com',
                timestamp: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
                summary: {
                    totalPages: 25,
                    pagesWithViolations: 8,
                    totalViolations: 32,
                    compliancePercentage: 68,
                },
                status: 'completed',
            },
            {
                id: '2',
                siteUrl: 'https://test-site.com',
                timestamp: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
                summary: {
                    totalPages: 15,
                    pagesWithViolations: 3,
                    totalViolations: 12,
                    compliancePercentage: 80,
                },
                status: 'completed',
            },
            {
                id: '3',
                siteUrl: 'https://demo-app.com',
                timestamp: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
                summary: {
                    totalPages: 40,
                    pagesWithViolations: 15,
                    totalViolations: 67,
                    compliancePercentage: 62,
                },
                status: 'completed',
            },
        ],
    },
};

export const WithManyReports: Story = {
    args: {
        reports: Array.from({ length: 20 }, (_, i) => ({
            id: `${i + 1}`,
            siteUrl: `https://site-${i + 1}.com`,
            timestamp: new Date(Date.now() - (i + 1) * 86400000).toISOString(),
            summary: {
                totalPages: Math.floor(Math.random() * 50) + 10,
                pagesWithViolations: Math.floor(Math.random() * 20) + 1,
                totalViolations: Math.floor(Math.random() * 100) + 5,
                compliancePercentage: Math.floor(Math.random() * 40) + 60,
            },
            status: 'completed' as const,
        })),
    },
};

export const WithFiltering: Story = {
    args: {
        reports: [
            {
                id: '1',
                siteUrl: 'https://example.com',
                timestamp: new Date(Date.now() - 86400000).toISOString(),
                summary: {
                    totalPages: 25,
                    pagesWithViolations: 8,
                    totalViolations: 32,
                    compliancePercentage: 68,
                },
                status: 'completed',
            },
            {
                id: '2',
                siteUrl: 'https://test-site.com',
                timestamp: new Date(Date.now() - 172800000).toISOString(),
                summary: {
                    totalPages: 15,
                    pagesWithViolations: 3,
                    totalViolations: 12,
                    compliancePercentage: 80,
                },
                status: 'completed',
            },
        ],
        filters: {
            dateRange: 'last7days',
            complianceThreshold: 70,
            searchTerm: 'example',
        },
    },
};

export const WithPagination: Story = {
    args: {
        reports: Array.from({ length: 50 }, (_, i) => ({
            id: `${i + 1}`,
            siteUrl: `https://site-${i + 1}.com`,
            timestamp: new Date(Date.now() - (i + 1) * 86400000).toISOString(),
            summary: {
                totalPages: Math.floor(Math.random() * 50) + 10,
                pagesWithViolations: Math.floor(Math.random() * 20) + 1,
                totalViolations: Math.floor(Math.random() * 100) + 5,
                compliancePercentage: Math.floor(Math.random() * 40) + 60,
            },
            status: 'completed' as const,
        })),
        pagination: {
            currentPage: 1,
            totalPages: 5,
            itemsPerPage: 10,
            totalItems: 50,
        },
    },
};

export const EmptyState: Story = {
    args: {
        reports: [],
    },
};

export const Loading: Story = {
    args: {
        isLoading: true,
    },
};

export const WithError: Story = {
    args: {
        error: 'Failed to load reports. Please try again.',
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