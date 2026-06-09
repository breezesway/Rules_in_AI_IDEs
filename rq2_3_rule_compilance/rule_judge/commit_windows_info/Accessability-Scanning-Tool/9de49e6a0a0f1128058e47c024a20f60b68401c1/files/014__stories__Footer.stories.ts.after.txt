import { Meta, StoryObj } from '@storybook/html';
import { renderFooter, FooterProps } from '../src/components/Footer';

const meta: Meta<FooterProps> = {
    title: 'Components/Footer',
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
                        id: 'link-name',
                        enabled: true,
                    },
                    {
                        id: 'landmark-one-main',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        copyrightText: {
            control: 'text',
            description: 'Copyright text to display'
        },
        links: {
            control: 'object',
            description: 'Footer links array'
        },
        showLinks: {
            control: 'boolean',
            description: 'Whether to show footer links'
        }
    }
};

export default meta;

export const Default: StoryObj<FooterProps> = {
    render: (args) => renderFooter(args),
    args: {
        copyrightText: '© 2025 Accessibility Testing Tool. All rights reserved.',
        links: [
            { href: '/privacy', text: 'Privacy Policy' },
            { href: '/terms', text: 'Terms of Service' },
            { href: '/contact', text: 'Contact Us' }
        ],
        showLinks: true
    }
};

export const NoLinks: StoryObj<FooterProps> = {
    render: (args) => renderFooter(args),
    args: {
        copyrightText: '© 2025 Accessibility Testing Tool. All rights reserved.',
        links: [],
        showLinks: false
    }
};

export const CustomCopyright: StoryObj<FooterProps> = {
    render: (args) => renderFooter(args),
    args: {
        copyrightText: '© 2025 Brad Reaney. Built with accessibility in mind.',
        links: [
            { href: '/about', text: 'About' },
            { href: '/help', text: 'Help & Support' },
            { href: '/github', text: 'GitHub Repository' }
        ],
        showLinks: true
    }
};

export const ManyLinks: StoryObj<FooterProps> = {
    render: (args) => renderFooter(args),
    args: {
        copyrightText: '© 2025 Accessibility Testing Tool. All rights reserved.',
        links: [
            { href: '/privacy', text: 'Privacy Policy' },
            { href: '/terms', text: 'Terms of Service' },
            { href: '/contact', text: 'Contact Us' },
            { href: '/about', text: 'About' },
            { href: '/help', text: 'Help & Support' },
            { href: '/github', text: 'GitHub Repository' },
            { href: '/docs', text: 'Documentation' },
            { href: '/api', text: 'API Reference' }
        ],
        showLinks: true
    }
};

export const Minimal: StoryObj<FooterProps> = {
    render: (args) => renderFooter(args),
    args: {
        copyrightText: '© 2025',
        links: [],
        showLinks: false
    }
}; 