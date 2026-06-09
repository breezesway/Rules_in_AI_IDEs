import { Meta, StoryObj } from '@storybook/html';
import { renderErrorSection, ErrorSectionProps } from '../src/components/ErrorSection';

const meta: Meta<ErrorSectionProps> = {
    title: 'Components/ErrorSection',
    parameters: {
        layout: 'padded',
        a11y: {
            config: {
                rules: [
                    {
                        id: 'color-contrast',
                        enabled: true,
                    },
                    {
                        id: 'alert',
                        enabled: true,
                    },
                    {
                        id: 'aria-alert',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        error: {
            control: 'object',
            description: 'Error information to display'
        },
        isVisible: {
            control: 'boolean',
            description: 'Whether the error section is visible'
        },
        showDetails: {
            control: 'boolean',
            description: 'Whether to show detailed error information'
        }
    }
};

export default meta;

export const Default: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'An error occurred during the scan',
            type: 'scan_error',
            details: 'The scan failed due to network connectivity issues',
            timestamp: new Date().toISOString(),
            code: 'NETWORK_ERROR'
        },
        isVisible: true,
        showDetails: false
    }
};

export const NetworkError: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'Network connection failed',
            type: 'network_error',
            details: 'Unable to connect to the target website. Please check your internet connection and try again.',
            timestamp: new Date().toISOString(),
            code: 'CONNECTION_TIMEOUT'
        },
        isVisible: true,
        showDetails: true
    }
};

export const ValidationError: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'Invalid URL provided',
            type: 'validation_error',
            details: 'The URL "invalid-url" is not a valid web address. Please enter a valid URL starting with http:// or https://',
            timestamp: new Date().toISOString(),
            code: 'INVALID_URL'
        },
        isVisible: true,
        showDetails: true
    }
};

export const ServerError: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'Server error occurred',
            type: 'server_error',
            details: 'The server encountered an internal error while processing your request. Please try again later.',
            timestamp: new Date().toISOString(),
            code: 'INTERNAL_SERVER_ERROR'
        },
        isVisible: true,
        showDetails: true
    }
};

export const TimeoutError: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'Scan timed out',
            type: 'timeout_error',
            details: 'The scan took longer than expected and timed out. This may be due to a large website or slow network connection.',
            timestamp: new Date().toISOString(),
            code: 'SCAN_TIMEOUT'
        },
        isVisible: true,
        showDetails: true
    }
};

export const Hidden: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'An error occurred',
            type: 'generic_error',
            details: 'Something went wrong',
            timestamp: new Date().toISOString(),
            code: 'GENERIC_ERROR'
        },
        isVisible: false,
        showDetails: false
    }
};

export const CriticalError: StoryObj<ErrorSectionProps> = {
    render: (args) => renderErrorSection(args),
    args: {
        error: {
            message: 'Critical system error',
            type: 'critical_error',
            details: 'A critical error has occurred that requires immediate attention. Please contact support if this error persists.',
            timestamp: new Date().toISOString(),
            code: 'CRITICAL_ERROR'
        },
        isVisible: true,
        showDetails: true
    }
}; 