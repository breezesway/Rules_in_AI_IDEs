import type { Meta, StoryObj } from '@storybook/react';
import { LandingPage } from '@/components/LandingPage';

const meta: Meta<typeof LandingPage> = {
    title: 'Pages/LandingPage',
    component: LandingPage,
    parameters: {
        layout: 'fullscreen',
        a11y: {
            config: {
                rules: [
                    { id: 'color-contrast', enabled: true },
                    { id: 'heading-order', enabled: true },
                    { id: 'landmark-one-main', enabled: true },
                    { id: 'button-name', enabled: true },
                    { id: 'link-name', enabled: true },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        onGetStarted: { action: 'get-started' },
        onLearnMore: { action: 'learn-more' },
    },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
    args: {},
};

export const WithHeroContent: Story = {
    args: {
        heroTitle: 'Accessibility Testing Made Simple',
        heroSubtitle: 'Comprehensive WCAG 2.1 AA/AAA compliance testing for your website',
        ctaText: 'Start Your Free Scan',
    },
};

export const WithFeatures: Story = {
    args: {
        features: [
            {
                title: 'WCAG 2.1 Compliance',
                description: 'Full support for WCAG 2.1 AA and AAA standards',
                icon: 'check-circle',
            },
            {
                title: 'Automated Testing',
                description: 'Comprehensive automated accessibility testing',
                icon: 'robot',
            },
            {
                title: 'Detailed Reports',
                description: 'Generate detailed PDF and web reports',
                icon: 'file-text',
            },
        ],
    },
};

export const WithTestimonials: Story = {
    args: {
        testimonials: [
            {
                name: 'Sarah Johnson',
                role: 'UX Designer',
                company: 'TechCorp',
                content: 'This tool has transformed our accessibility testing process.',
                rating: 5,
            },
            {
                name: 'Mike Chen',
                role: 'Frontend Developer',
                company: 'WebSolutions',
                content: 'Comprehensive and easy to use. Highly recommended!',
                rating: 5,
            },
        ],
    },
};

export const DarkTheme: Story = {
    args: {},
    parameters: {
        backgrounds: {
            default: 'dark',
        },
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