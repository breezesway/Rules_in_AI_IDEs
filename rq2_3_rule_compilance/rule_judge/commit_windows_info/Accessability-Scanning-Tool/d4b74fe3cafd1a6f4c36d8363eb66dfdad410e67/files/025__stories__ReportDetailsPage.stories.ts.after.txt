import type { Meta, StoryObj } from '@storybook/html';
import { renderReportDetailsPage } from '../src/components/ReportDetailsPage';

const meta: Meta = {
    title: 'Pages/ReportDetailsPage',
    parameters: {
        layout: 'fullscreen',
        docs: {
            description: {
                component: 'Detailed report view page that displays comprehensive accessibility scan results with violations, pages analyzed, and remediation information.'
            }
        }
    },
    argTypes: {
        reportId: {
            control: 'text',
            description: 'The ID of the report to display'
        },
        header: {
            control: 'object',
            description: 'Header component props'
        },
        footer: {
            control: 'object',
            description: 'Footer component props'
        }
    }
};

export default meta;
type Story = StoryObj;

// Default story with a sample report ID
export const Default: Story = {
    args: {
        reportId: 'sample-report-123',
        header: {
            currentPage: 'reports'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
};

// Story with a different report ID
export const WithDifferentReportId: Story = {
    args: {
        reportId: 'test-report-456',
        header: {
            currentPage: 'reports'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
};

// Story with custom header
export const WithCustomHeader: Story = {
    args: {
        reportId: 'custom-report-789',
        header: {
            currentPage: 'reports',
            title: 'Custom Report Details'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
};

// Story with empty report ID (error state)
export const EmptyReportId: Story = {
    args: {
        reportId: '',
        header: {
            currentPage: 'reports'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
};

// Story with very long report ID
export const LongReportId: Story = {
    args: {
        reportId: 'very-long-report-id-that-might-cause-layout-issues-123456789012345678901234567890',
        header: {
            currentPage: 'reports'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
};

// Story with special characters in report ID
export const SpecialCharactersReportId: Story = {
    args: {
        reportId: 'report-with-special-chars-!@#$%^&*()',
        header: {
            currentPage: 'reports'
        },
        footer: {}
    },
    render: (args) => renderReportDetailsPage(args)
}; 