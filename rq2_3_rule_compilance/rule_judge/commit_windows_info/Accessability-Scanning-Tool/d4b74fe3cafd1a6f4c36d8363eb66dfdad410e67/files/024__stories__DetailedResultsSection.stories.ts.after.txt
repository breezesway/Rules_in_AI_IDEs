import { renderDetailedResultsSection, DetailedResultsSectionProps } from '@/components/DetailedResultsSection';
import { SiteWideAccessibilityReport, ProcessedViolation } from '@/core/types/common';

// Mock data for testing
const createMockViolation = (id: string, impact: 'minor' | 'moderate' | 'serious' | 'critical'): ProcessedViolation => ({
    id,
    impact,
    description: `${id} issue description`,
    help: `Help text for ${id}`,
    helpUrl: 'https://example.com/help',
    wcagTags: ['1.1.1'],
    wcagLevel: 'A',
    occurrences: 1,
    tools: ['axe-core'],
    elements: [{
        html: `<div>${id} element</div>`,
        target: { selector: 'div' },
        failureSummary: `${id} failure summary`,
        selector: 'div'
    }],
    scenarioRelevance: ['All users'],
    remediation: {
        priority: 'High',
        effort: 'Medium',
        suggestions: [`Fix ${id} issue`]
    }
});

const createMockReport = (): SiteWideAccessibilityReport => ({
    siteUrl: 'https://example.com',
    reportType: 'site-wide',
    timestamp: new Date().toISOString(),
    wcagLevel: 'AA',
    metadata: {
        toolsUsed: ['axe-core', 'pa11y'],
        scanId: 'test-scan-123'
    },
    summary: {
        totalPages: 5,
        totalViolations: 12,
        compliancePercentage: 85,
        criticalViolations: 2,
        seriousViolations: 3,
        moderateViolations: 4,
        minorViolations: 3
    },
    violations: [
        createMockViolation('color-contrast', 'serious'),
        createMockViolation('missing-alt-text', 'critical'),
        createMockViolation('empty-heading', 'moderate')
    ],
    pageReports: [
        {
            url: 'https://example.com',
            violations: [createMockViolation('color-contrast', 'serious')],
            summary: {
                criticalViolations: 0,
                seriousViolations: 1,
                moderateViolations: 0,
                minorViolations: 0
            }
        },
        {
            url: 'https://example.com/about',
            violations: [createMockViolation('missing-alt-text', 'critical')],
            summary: {
                criticalViolations: 1,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0
            }
        }
    ],
    mostCommonViolations: [
        {
            id: 'color-contrast',
            impact: 'serious',
            description: 'Color contrast issue',
            affectedPages: 3,
            totalOccurrences: 5
        }
    ]
});

export default {
    title: 'Components/DetailedResultsSection',
    parameters: {
        layout: 'fullscreen',
        docs: {
            description: {
                component: 'A shared component for displaying detailed accessibility scan results with comprehensive violation analysis, summary statistics, and remediation suggestions.'
            }
        }
    },
    argTypes: {
        report: {
            control: 'object',
            description: 'The accessibility report data to display'
        },
        visible: {
            control: 'boolean',
            description: 'Whether the component should be visible'
        },
        showHeader: {
            control: 'boolean',
            description: 'Whether to show the report header section'
        },
        showBackButton: {
            control: 'boolean',
            description: 'Whether to show the back button'
        }
    }
};

export const Default = {
    args: {
        report: createMockReport(),
        visible: true,
        showHeader: true,
        showBackButton: true
    },
    render: (args: DetailedResultsSectionProps) => `
        <!DOCTYPE html>
        <html lang="en-GB">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Detailed Results Section - Storybook</title>
            <link rel="stylesheet" href="styles.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <style>
                /* Additional styles for detailed results */
                .detailed-results-container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 var(--spacing-md);
                }
                
                .report-header {
                    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
                    color: var(--white);
                    padding: var(--spacing-xl);
                    border-radius: var(--border-radius-lg);
                    margin-bottom: var(--spacing-xl);
                }
                
                .report-header h1 {
                    margin: 0 0 var(--spacing-md) 0;
                    font-size: 2rem;
                    font-weight: 600;
                }
                
                .report-meta {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: var(--spacing-md);
                    margin-top: var(--spacing-lg);
                }
                
                .meta-item {
                    background: rgba(255, 255, 255, 0.1);
                    padding: var(--spacing-md);
                    border-radius: var(--border-radius);
                }
                
                .meta-label {
                    font-size: var(--font-size-small);
                    opacity: 0.8;
                    margin-bottom: var(--spacing-xs);
                }
                
                .meta-value {
                    font-size: var(--font-size-large);
                    font-weight: 600;
                }
                
                .summary-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: var(--spacing-lg);
                    margin-top: var(--spacing-lg);
                }
                
                .summary-card {
                    text-align: center;
                    padding: var(--spacing-lg);
                    border-radius: var(--border-radius);
                    background: var(--light-grey);
                    border: 1px solid var(--light-grey);
                }
                
                .summary-value {
                    font-size: 2rem;
                    font-weight: 700;
                    margin-bottom: var(--spacing-xs);
                }
                
                .summary-label {
                    font-size: var(--font-size-small);
                    color: var(--grey);
                    font-weight: 500;
                }
                
                .critical { color: var(--error); }
                .serious { color: #ea580c; }
                .moderate { color: #d97706; }
                .minor { color: var(--success); }
                .good { color: var(--success); }
                
                .violation-card {
                    border: 1px solid var(--light-grey);
                    border-radius: var(--border-radius);
                    padding: var(--spacing-lg);
                    margin-bottom: var(--spacing-md);
                    background: var(--light-grey);
                }
                
                .violation-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: var(--spacing-md);
                }
                
                .violation-title {
                    font-weight: 600;
                    font-size: var(--font-size-large);
                    color: var(--dark-grey);
                }
                
                .violation-impact {
                    padding: var(--spacing-xs) var(--spacing-md);
                    border-radius: 20px;
                    font-size: 0.75rem;
                    font-weight: 600;
                    text-transform: uppercase;
                }
                
                .impact-critical { background: #fef2f2; color: var(--error); }
                .impact-serious { background: #fff7ed; color: #ea580c; }
                .impact-moderate { background: #fffbeb; color: #d97706; }
                .impact-minor { background: #f0fdf4; color: var(--success); }
                
                .violation-details {
                    margin-bottom: var(--spacing-md);
                }
                
                .violation-description {
                    color: var(--grey);
                    margin-bottom: var(--spacing-xs);
                }
                
                .violation-help {
                    color: var(--grey);
                    font-size: var(--font-size-small);
                }
                
                .violation-stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                    gap: var(--spacing-md);
                    margin-bottom: var(--spacing-md);
                }
                
                .stat-item {
                    text-align: center;
                    padding: var(--spacing-md);
                    background: var(--white);
                    border-radius: var(--border-radius);
                    border: 1px solid var(--light-grey);
                }
                
                .stat-value {
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: var(--dark-grey);
                }
                
                .stat-label {
                    font-size: 0.75rem;
                    color: var(--grey);
                    text-transform: uppercase;
                }
                
                .violation-elements {
                    margin-top: var(--spacing-md);
                }
                
                .element-item {
                    background: var(--white);
                    border: 1px solid var(--light-grey);
                    border-radius: var(--border-radius);
                    padding: var(--spacing-md);
                    margin-bottom: var(--spacing-xs);
                }
                
                .element-html {
                    font-family: 'Courier New', monospace;
                    font-size: var(--font-size-small);
                    background: var(--light-grey);
                    padding: var(--spacing-xs);
                    border-radius: 4px;
                    margin-bottom: var(--spacing-xs);
                    overflow-x: auto;
                }
                
                .element-selector {
                    font-size: 0.75rem;
                    color: var(--grey);
                    font-family: 'Courier New', monospace;
                }
                
                .element-failure {
                    color: var(--error);
                    font-size: var(--font-size-small);
                    margin-top: var(--spacing-xs);
                }
                
                .page-item {
                    border: 1px solid var(--light-grey);
                    border-radius: var(--border-radius);
                    padding: var(--spacing-md);
                    margin-bottom: var(--spacing-md);
                    background: var(--light-grey);
                }
                
                .page-url {
                    font-weight: 600;
                    color: var(--dark-grey);
                    margin-bottom: var(--spacing-xs);
                }
                
                .page-stats {
                    display: flex;
                    gap: var(--spacing-md);
                    font-size: var(--font-size-small);
                    color: var(--grey);
                }
                
                .back-button {
                    display: inline-flex;
                    align-items: center;
                    gap: var(--spacing-xs);
                    padding: var(--spacing-md) var(--spacing-lg);
                    background: var(--primary);
                    color: var(--white);
                    text-decoration: none;
                    border-radius: var(--border-radius);
                    font-weight: 500;
                    margin-bottom: var(--spacing-xl);
                    transition: var(--transition);
                }
                
                .back-button:hover {
                    background: var(--secondary);
                    color: var(--white);
                    text-decoration: none;
                }
                
                .remediation-info {
                    margin-top: var(--spacing-md);
                    padding: var(--spacing-md);
                    background: var(--white);
                    border-radius: var(--border-radius);
                    border: 1px solid var(--light-grey);
                }
                
                .remediation-info h4 {
                    margin: 0 0 var(--spacing-md) 0;
                    color: var(--primary);
                }
                
                .remediation-info ul {
                    margin: var(--spacing-xs) 0;
                    padding-left: var(--spacing-lg);
                }
                
                .remediation-info li {
                    margin-bottom: var(--spacing-xs);
                }
                
                @media (max-width: 768px) {
                    .detailed-results-container {
                        padding: 0 var(--spacing-sm);
                    }
                    
                    .report-meta {
                        grid-template-columns: 1fr;
                    }
                    
                    .summary-grid {
                        grid-template-columns: repeat(2, 1fr);
                    }
                    
                    .violation-stats {
                        grid-template-columns: repeat(2, 1fr);
                    }
                    
                    .violation-header {
                        flex-direction: column;
                        align-items: flex-start;
                        gap: var(--spacing-xs);
                    }
                }
            </style>
        </head>
        <body>
            <main class="main">
                ${renderDetailedResultsSection(args)}
            </main>
        </body>
        </html>
    `
};

export const WithoutHeader = {
    args: {
        report: createMockReport(),
        visible: true,
        showHeader: false,
        showBackButton: true
    },
    render: Default.render
};

export const WithoutBackButton = {
    args: {
        report: createMockReport(),
        visible: true,
        showHeader: true,
        showBackButton: false
    },
    render: Default.render
};

export const Hidden = {
    args: {
        report: createMockReport(),
        visible: false,
        showHeader: true,
        showBackButton: true
    },
    render: Default.render
};

export const NoReportData = {
    args: {
        report: null,
        visible: true,
        showHeader: true,
        showBackButton: true
    },
    render: Default.render
};

export const HighComplianceScore = {
    args: {
        report: {
            ...createMockReport(),
            summary: {
                ...createMockReport().summary,
                compliancePercentage: 95,
                criticalViolations: 0,
                seriousViolations: 1,
                moderateViolations: 2,
                minorViolations: 1
            }
        },
        visible: true,
        showHeader: true,
        showBackButton: true
    },
    render: Default.render
};

export const LowComplianceScore = {
    args: {
        report: {
            ...createMockReport(),
            summary: {
                ...createMockReport().summary,
                compliancePercentage: 45,
                criticalViolations: 5,
                seriousViolations: 8,
                moderateViolations: 10,
                minorViolations: 3
            }
        },
        visible: true,
        showHeader: true,
        showBackButton: true
    },
    render: Default.render
}; 