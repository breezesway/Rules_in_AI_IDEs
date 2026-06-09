import type { Meta, StoryObj } from '@storybook/react';
import { WebInterface } from '@/components/WebInterface';

const meta: Meta<typeof WebInterface> = {
    title: 'Components/WebInterface',
    component: WebInterface,
    parameters: {
        layout: 'fullscreen',
        a11y: {
            config: {
                rules: [
                    { id: 'color-contrast', enabled: true },
                    { id: 'heading-order', enabled: true },
                    { id: 'landmark-one-main', enabled: true },
                    { id: 'region', enabled: true },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        onScanComplete: { action: 'scan-complete' },
        onError: { action: 'error' },
    },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {},
};

export const WithInitialData: Story = {
    args: {
        initialScanResults: {
            siteUrl: 'https://example.com',
            timestamp: new Date().toISOString(),
            summary: {
                totalPages: 5,
                pagesWithViolations: 2,
                totalViolations: 8,
                compliancePercentage: 60,
            },
        },
    },
};

export const Loading: Story = {
    args: {
        isLoading: true,
    },
};

export const WithError: Story = {
    args: {
        error: 'Failed to load accessibility data',
    },
};

export const EmptyState: Story = {
    args: {
        isEmpty: true,
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

export const TabletView: Story = {
    args: {},
    parameters: {
        viewport: {
            defaultViewport: 'tablet',
        },
    },
}; 