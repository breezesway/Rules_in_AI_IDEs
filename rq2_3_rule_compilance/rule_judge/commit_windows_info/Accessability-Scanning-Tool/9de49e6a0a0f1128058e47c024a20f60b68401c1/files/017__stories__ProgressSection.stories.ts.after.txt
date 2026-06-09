import { Meta, StoryObj } from '@storybook/html';
import { renderProgressSection, ProgressSectionProps } from '../src/components/ProgressSection';

const meta: Meta<ProgressSectionProps> = {
    title: 'Components/ProgressSection',
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
                        id: 'progressbar-name',
                        enabled: true,
                    },
                    {
                        id: 'aria-progressbar-name',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        currentStage: {
            control: 'select',
            options: ['initializing', 'crawling', 'analyzing', 'generating', 'complete'],
            description: 'Current stage of the scan process'
        },
        progress: {
            control: { type: 'range', min: 0, max: 100, step: 1 },
            description: 'Progress percentage (0-100)'
        },
        totalPages: {
            control: { type: 'number', min: 0 },
            description: 'Total number of pages to scan'
        },
        scannedPages: {
            control: { type: 'number', min: 0 },
            description: 'Number of pages already scanned'
        },
        currentUrl: {
            control: 'text',
            description: 'Current URL being processed'
        },
        isVisible: {
            control: 'boolean',
            description: 'Whether the progress section is visible'
        }
    }
};

export default meta;

export const Default: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'initializing',
        progress: 0,
        totalPages: 0,
        scannedPages: 0,
        currentUrl: '',
        isVisible: true
    }
};

export const Crawling: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'crawling',
        progress: 25,
        totalPages: 10,
        scannedPages: 2,
        currentUrl: 'https://example.com/page1',
        isVisible: true
    }
};

export const Analyzing: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'analyzing',
        progress: 60,
        totalPages: 10,
        scannedPages: 6,
        currentUrl: 'https://example.com/page6',
        isVisible: true
    }
};

export const Generating: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'generating',
        progress: 90,
        totalPages: 10,
        scannedPages: 10,
        currentUrl: '',
        isVisible: true
    }
};

export const Complete: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'complete',
        progress: 100,
        totalPages: 10,
        scannedPages: 10,
        currentUrl: '',
        isVisible: true
    }
};

export const Hidden: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'initializing',
        progress: 0,
        totalPages: 0,
        scannedPages: 0,
        currentUrl: '',
        isVisible: false
    }
};

export const LargeSite: StoryObj<ProgressSectionProps> = {
    render: (args) => renderProgressSection(args),
    args: {
        currentStage: 'crawling',
        progress: 15,
        totalPages: 50,
        scannedPages: 7,
        currentUrl: 'https://example.com/deep/nested/page',
        isVisible: true
    }
}; 