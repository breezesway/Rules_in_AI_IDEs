import { Meta, StoryObj } from '@storybook/html';
import { renderScanOptions, ScanOptionsProps } from '../src/components/ScanOptions';

const meta: Meta<ScanOptionsProps> = {
    title: 'Components/ScanOptions',
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
                        id: 'form-field-multiple-labels',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        options: {
            control: 'object',
            description: 'Custom scan options configuration'
        }
    }
};

export default meta;

export const Default: StoryObj<ScanOptionsProps> = {
    render: (args) => renderScanOptions(args),
    args: {}
};

export const CustomOptions: StoryObj<ScanOptionsProps> = {
    render: (args) => renderScanOptions(args),
    args: {
        options: [
            {
                id: 'custom-scan',
                icon: '🔧',
                title: 'Custom Scan',
                description: 'Custom accessibility scan with specific options',
                formId: 'customScanForm',
                inputId: 'customScanUrl',
                inputName: 'url',
                inputPlaceholder: 'https://example.com',
                inputHelp: 'Enter the URL for custom scan',
                buttonText: 'Start Custom Scan',
                buttonClass: 'btn-primary',
                buttonIcon: '🔧'
            }
        ]
    }
};

export const MinimalOptions: StoryObj<ScanOptionsProps> = {
    render: (args) => renderScanOptions(args),
    args: {
        options: [
            {
                id: 'simple-scan',
                icon: '📄',
                title: 'Simple Scan',
                description: 'Basic accessibility scan',
                formId: 'simpleScanForm',
                inputId: 'simpleScanUrl',
                inputName: 'url',
                inputPlaceholder: 'https://example.com',
                inputHelp: 'Enter URL to scan',
                buttonText: 'Scan',
                buttonClass: 'btn-primary',
                buttonIcon: '📄'
            }
        ]
    }
}; 