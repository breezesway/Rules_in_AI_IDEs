import { Meta, StoryObj } from '@storybook/html';
import { renderResultsSection, ResultsSectionProps } from '../src/components/ResultsSection';

const meta: Meta<ResultsSectionProps> = {
    title: 'Components/ResultsSection',
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
                        id: 'heading-order',
                        enabled: true,
                    },
                    {
                        id: 'table-fake-caption',
                        enabled: true,
                    },
                    {
                        id: 'table-structure',
                        enabled: true,
                    },
                ],
            },
        },
    },
    tags: ['autodocs'],
    argTypes: {
        results: {
            control: 'object',
            description: 'Accessibility scan results data'
        },
        isVisible: {
            control: 'boolean',
            description: 'Whether the results section is visible'
        },
        showDetails: {
            control: 'boolean',
            description: 'Whether to show detailed violation information'
        }
    }
};

export default meta;

export const Default: StoryObj<ResultsSectionProps> = {
    render: (args) => renderResultsSection(args),
    args: {
        results: {
            summary: {
                totalViolations: 5,
                criticalViolations: 1,
                seriousViolations: 2,
                moderateViolations: 1,
                minorViolations: 1,
                compliancePercentage: 85,
                mostCommonViolations: ['color-contrast', 'button-name']
            },
            violations: [
                {
                    id: 'color-contrast',
                    impact: 'serious',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/color-contrast',
                    wcagTags: ['WCAG2AA'],
                    wcagLevel: 'AA',
                    occurrences: 3,
                    tools: ['axe-core'],
                    elements: [
                        {
                            html: '<button class="btn-primary">Submit</button>',
                            target: { selector: 'button.btn-primary' },
                            failureSummary: 'Fix any of the following: Element has insufficient color contrast of 2.51 (foreground color: #ffffff, background color: #f0f0f0, font size: 12.0pt (16px), font weight: normal). Expected contrast ratio of 4.5:1',
                            selector: 'button.btn-primary'
                        }
                    ],
                    scenarioRelevance: ['All users'],
                    remediation: {
                        priority: 'High',
                        effort: 'Medium',
                        suggestions: ['Increase the contrast ratio to at least 4.5:1', 'Use a darker background color', 'Use a lighter text color']
                    }
                }
            ]
        },
        isVisible: true,
        showDetails: false
    }
};

export const NoViolations: StoryObj<ResultsSectionProps> = {
    render: (args) => renderResultsSection(args),
    args: {
        results: {
            summary: {
                totalViolations: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0,
                compliancePercentage: 100,
                mostCommonViolations: []
            },
            violations: []
        },
        isVisible: true,
        showDetails: false
    }
};

export const ManyViolations: StoryObj<ResultsSectionProps> = {
    render: (args) => renderResultsSection(args),
    args: {
        results: {
            summary: {
                totalViolations: 25,
                criticalViolations: 5,
                seriousViolations: 10,
                moderateViolations: 7,
                minorViolations: 3,
                compliancePercentage: 45,
                mostCommonViolations: ['color-contrast', 'button-name', 'image-alt', 'heading-order', 'form-field-multiple-labels']
            },
            violations: [
                {
                    id: 'color-contrast',
                    impact: 'serious',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/color-contrast',
                    wcagTags: ['WCAG2AA'],
                    wcagLevel: 'AA',
                    occurrences: 8,
                    tools: ['axe-core'],
                    elements: [],
                    scenarioRelevance: ['All users'],
                    remediation: {
                        priority: 'High',
                        effort: 'Medium',
                        suggestions: ['Increase the contrast ratio to at least 4.5:1']
                    }
                },
                {
                    id: 'button-name',
                    impact: 'critical',
                    description: 'Buttons must have discernible text',
                    help: 'Ensures buttons have accessible names',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/button-name',
                    wcagTags: ['WCAG2AA'],
                    wcagLevel: 'AA',
                    occurrences: 5,
                    tools: ['axe-core'],
                    elements: [],
                    scenarioRelevance: ['All users'],
                    remediation: {
                        priority: 'Critical',
                        effort: 'Low',
                        suggestions: ['Add accessible names to buttons using aria-label or text content']
                    }
                }
            ]
        },
        isVisible: true,
        showDetails: true
    }
};

export const Hidden: StoryObj<ResultsSectionProps> = {
    render: (args) => renderResultsSection(args),
    args: {
        results: {
            summary: {
                totalViolations: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0,
                compliancePercentage: 100,
                mostCommonViolations: []
            },
            violations: []
        },
        isVisible: false,
        showDetails: false
    }
};

export const WithDetails: StoryObj<ResultsSectionProps> = {
    render: (args) => renderResultsSection(args),
    args: {
        results: {
            summary: {
                totalViolations: 3,
                criticalViolations: 0,
                seriousViolations: 2,
                moderateViolations: 1,
                minorViolations: 0,
                compliancePercentage: 92,
                mostCommonViolations: ['color-contrast', 'heading-order']
            },
            violations: [
                {
                    id: 'color-contrast',
                    impact: 'serious',
                    description: 'Elements must meet minimum color contrast ratio requirements',
                    help: 'Ensures the contrast between foreground and background colors meets WCAG 2 AA contrast ratio thresholds',
                    helpUrl: 'https://dequeuniversity.com/rules/axe/4.9/color-contrast',
                    wcagTags: ['WCAG2AA'],
                    wcagLevel: 'AA',
                    occurrences: 2,
                    tools: ['axe-core'],
                    elements: [
                        {
                            html: '<span class="text-light">Light text</span>',
                            target: { selector: 'span.text-light' },
                            failureSummary: 'Element has insufficient color contrast',
                            selector: 'span.text-light'
                        }
                    ],
                    scenarioRelevance: ['All users'],
                    remediation: {
                        priority: 'High',
                        effort: 'Medium',
                        suggestions: ['Increase the contrast ratio to at least 4.5:1']
                    }
                }
            ]
        },
        isVisible: true,
        showDetails: true
    }
}; 