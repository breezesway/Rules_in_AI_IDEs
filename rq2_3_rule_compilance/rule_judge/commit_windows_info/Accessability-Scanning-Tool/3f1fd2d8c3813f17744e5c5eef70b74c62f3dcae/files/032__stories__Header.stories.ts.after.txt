import { Meta, StoryObj } from '@storybook/html';
import { renderHeader, HeaderProps } from '../src/components/Header';

const meta: Meta<HeaderProps> = {
    title: 'Components/Header',
    parameters: {
        layout: 'fullscreen',
        a11y: {
            config: {
                rules: [
                    {
                        id: 'color-contrast',
                        enabled: true,
                    },
                    {
                        id: 'heading-order',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        title: {
            control: 'text',
            description: 'Main title text'
        },
        subtitle: {
            control: 'text',
            description: 'Subtitle text'
        },
        version: {
            control: 'text',
            description: 'Version number'
        }
    }
};

export default meta;

export const Default: StoryObj<HeaderProps> = {
    render: (args) => renderHeader(args),
    args: {
        title: 'Accessibility Testing Tool',
        subtitle: 'Professional WCAG 2.1 AAA compliance testing with comprehensive reporting',
        version: 'v2.1.1'
    }
};

export const CustomTitle: StoryObj<HeaderProps> = {
    render: (args) => renderHeader(args),
    args: {
        title: 'Custom Accessibility Tool',
        subtitle: 'Custom subtitle for testing',
        version: 'v1.0.0'
    }
};

export const LongTitle: StoryObj<HeaderProps> = {
    render: (args) => renderHeader(args),
    args: {
        title: 'Very Long Accessibility Testing Tool Title That Might Wrap',
        subtitle: 'A comprehensive tool for testing web accessibility compliance with detailed reporting',
        version: 'v2.1.1'
    }
}; 