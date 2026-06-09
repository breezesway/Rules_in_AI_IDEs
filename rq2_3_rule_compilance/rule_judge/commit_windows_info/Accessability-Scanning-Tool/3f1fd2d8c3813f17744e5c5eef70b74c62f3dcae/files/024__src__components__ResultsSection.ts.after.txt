export interface ScanResult {
    title: string;
    stats?: {
        issuesFound?: number;
        pagesScanned?: number;
        complianceScore?: string;
    };
    description?: string;
    actions?: {
        text: string;
        url?: string;
        class?: string;
    }[];
}

export interface ResultsSectionProps {
    result?: ScanResult;
    visible?: boolean;
}

export function renderResultsSection(props: ResultsSectionProps = {}): string {
    const {
        result = {
            title: 'Accessibility Analysis Complete',
            stats: {
                issuesFound: 23,
                pagesScanned: 12,
                complianceScore: '85%'
            },
            description: 'Comprehensive accessibility report generated successfully. Download the PDF report for detailed analysis.',
            actions: [
                {
                    text: 'Download PDF Report',
                    class: 'btn-primary'
                },
                {
                    text: 'View Detailed Results',
                    class: 'btn-secondary'
                }
            ]
        },
        visible = false
    } = props;

    const hidden = visible ? '' : 'hidden';

    const renderStats = (stats: any): string => {
        if (!stats) return '';

        return `
            <div class="result-stats">
                ${stats.issuesFound ? `
                    <div class="stat">
                        <div class="stat-value">${stats.issuesFound}</div>
                        <div class="stat-label">Issues Found</div>
                    </div>
                ` : ''}
                ${stats.pagesScanned ? `
                    <div class="stat">
                        <div class="stat-value">${stats.pagesScanned}</div>
                        <div class="stat-label">Pages Scanned</div>
                    </div>
                ` : ''}
                ${stats.complianceScore ? `
                    <div class="stat">
                        <div class="stat-value">${stats.complianceScore}</div>
                        <div class="stat-label">Compliance Score</div>
                    </div>
                ` : ''}
            </div>
        `;
    };

    const renderActions = (actions: any[]): string => {
        if (!actions || actions.length === 0) return '';

        return `
            <div class="result-actions">
                ${actions.map(action => `
                    <button type="button" class="btn ${action.class || 'btn-primary'}" ${action.url ? `onclick="window.open('${action.url}', '_blank')"` : ''}>
                        ${action.text}
                    </button>
                `).join('')}
            </div>
        `;
    };

    return `
        <section class="results-section" id="resultsSection" aria-labelledby="results-heading" ${hidden}>
            <h2 id="results-heading" class="section-heading">Scan Results</h2>
            <div class="results-container" id="resultsContainer">
                <div class="result-item">
                    <h3>${result.title}</h3>
                    ${renderStats(result.stats)}
                    ${result.description ? `<p>${result.description}</p>` : ''}
                    ${renderActions(result.actions || [])}
                </div>
            </div>
        </section>
    `;
} 