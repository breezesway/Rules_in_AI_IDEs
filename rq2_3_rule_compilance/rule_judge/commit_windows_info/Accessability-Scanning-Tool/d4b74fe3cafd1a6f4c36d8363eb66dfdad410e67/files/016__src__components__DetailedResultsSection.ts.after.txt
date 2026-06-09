import { SiteWideAccessibilityReport, ProcessedViolation } from '@/core/types/common';

export interface DetailedResultsSectionProps {
    report?: SiteWideAccessibilityReport | any;
    visible?: boolean;
    showHeader?: boolean;
    showBackButton?: boolean;
}

export function renderDetailedResultsSection(props: DetailedResultsSectionProps = {}): string {
    const {
        report = null,
        visible = false,
        showHeader = true,
        showBackButton = false
    } = props;

    if (!report) {
        return `
            <div class="results-section" ${visible ? '' : 'hidden'}>
                <h2 class="section-heading">No Report Data Available</h2>
                <p>No detailed results to display.</p>
            </div>
        `;
    }

    const data = report.data || report;
    const summary = data.summary || {};
    const violations = data.violations || [];
    const pageReports = data.pageReports || [];
    const mostCommonViolations = data.mostCommonViolations || [];

    const compliancePercentage = summary.compliancePercentage || 0;
    const complianceClass = compliancePercentage >= 90 ? 'good' :
        compliancePercentage >= 70 ? 'moderate' :
            compliancePercentage >= 50 ? 'serious' : 'critical';

    function formatDate(dateString: string): string {
        return new Date(dateString).toLocaleDateString('en-GB', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function renderViolationCard(violation: ProcessedViolation): string {
        const impactClass = `impact-${violation.impact || 'moderate'}`;
        const elements = violation.elements || [];

        return `
            <div class="violation-card">
                <div class="violation-header">
                    <div class="violation-title">
                        <code>${violation.id}</code>
                        <span class="wcag-level">WCAG ${violation.wcagLevel || 'Unknown'}</span>
                    </div>
                    <span class="violation-impact ${impactClass}">${violation.impact || 'moderate'}</span>
                </div>
                
                <div class="violation-details">
                    <div class="violation-description">${violation.description || 'No description available'}</div>
                    <div class="violation-help">${violation.help || 'No help information available'}</div>
                </div>
                
                <div class="violation-stats">
                    <div class="stat-item">
                        <div class="stat-value">${violation.occurrences || 1}</div>
                        <div class="stat-label">Occurrences</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${elements.length}</div>
                        <div class="stat-label">Elements</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${violation.tools?.join(', ') || 'Unknown'}</div>
                        <div class="stat-label">Tools</div>
                    </div>
                </div>
                
                ${elements.length > 0 ? `
                    <div class="violation-elements">
                        <h4>Affected Elements (${elements.length})</h4>
                        ${elements.map(element => `
                            <div class="element-item">
                                <div class="element-html">${element.html || 'No HTML available'}</div>
                                <div class="element-selector">Selector: ${element.selector || 'No selector available'}</div>
                                ${element.failureSummary ? `
                                    <div class="element-failure">Failure: ${element.failureSummary}</div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                ` : ''}
                
                ${violation.remediation ? `
                    <div class="remediation-info">
                        <h4>Remediation</h4>
                        <p><strong>Priority:</strong> ${violation.remediation.priority}</p>
                        <p><strong>Effort:</strong> ${violation.remediation.effort}</p>
                        ${violation.remediation.suggestions?.length > 0 ? `
                            <div>
                                <strong>Suggestions:</strong>
                                <ul>
                                    ${violation.remediation.suggestions.map(suggestion => `
                                        <li>${suggestion}</li>
                                    `).join('')}
                                </ul>
                            </div>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }

    function renderPageItem(page: any): string {
        const violations = page.violations || [];
        const pageSummary = page.summary || {};

        return `
            <div class="page-item">
                <div class="page-url">${page.url}</div>
                <div class="page-stats">
                    <span>${violations.length} violations</span>
                    <span>${pageSummary.criticalViolations || 0} critical</span>
                    <span>${pageSummary.seriousViolations || 0} serious</span>
                    <span>${pageSummary.moderateViolations || 0} moderate</span>
                    <span>${pageSummary.minorViolations || 0} minor</span>
                </div>
            </div>
        `;
    }

    return `
        <div class="detailed-results-container" ${visible ? '' : 'hidden'}>
            ${showBackButton ? `
                <a href="/reports" class="back-button">
                    ← Back to Reports
                </a>
            ` : ''}
            
            ${showHeader ? `
                <div class="report-header">
                    <h1>Accessibility Report</h1>
                    <p>${data.siteUrl || 'Unknown Site'}</p>
                    <div class="report-meta">
                        <div class="meta-item">
                            <div class="meta-label">Report Type</div>
                            <div class="meta-value">${data.reportType || 'Unknown'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Scan Date</div>
                            <div class="meta-value">${formatDate(data.timestamp || data.createdAt)}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">WCAG Level</div>
                            <div class="meta-value">${data.wcagLevel || 'Unknown'}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-label">Tools Used</div>
                            <div class="meta-value">${(data.metadata?.toolsUsed || []).join(', ') || 'Unknown'}</div>
                        </div>
                    </div>
                </div>
            ` : ''}

            <div class="results-section">
                <h2 class="section-heading">Summary</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="summary-value ${complianceClass}">${compliancePercentage}%</div>
                        <div class="summary-label">Compliance Score</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value">${summary.totalPages || 0}</div>
                        <div class="summary-label">Pages Scanned</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value">${summary.totalViolations || 0}</div>
                        <div class="summary-label">Total Violations</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value critical">${summary.criticalViolations || 0}</div>
                        <div class="summary-label">Critical</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value serious">${summary.seriousViolations || 0}</div>
                        <div class="summary-label">Serious</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value moderate">${summary.moderateViolations || 0}</div>
                        <div class="summary-label">Moderate</div>
                    </div>
                    <div class="summary-card">
                        <div class="summary-value minor">${summary.minorViolations || 0}</div>
                        <div class="summary-label">Minor</div>
                    </div>
                </div>
            </div>

            ${violations.length > 0 ? `
                <div class="results-section">
                    <h2 class="section-heading">Violations (${violations.length})</h2>
                    ${violations.map((violation: ProcessedViolation) => renderViolationCard(violation)).join('')}
                </div>
            ` : ''}

            ${pageReports.length > 0 ? `
                <div class="results-section">
                    <h2 class="section-heading">Pages Analyzed (${pageReports.length})</h2>
                    ${pageReports.map((page: any) => renderPageItem(page)).join('')}
                </div>
            ` : ''}

            ${mostCommonViolations.length > 0 ? `
                <div class="results-section">
                    <h2 class="section-heading">Most Common Violations</h2>
                    ${mostCommonViolations.map((violation: any) => `
                        <div class="violation-card">
                            <div class="violation-header">
                                <div class="violation-title">
                                    <code>${violation.id}</code>
                                </div>
                                <span class="violation-impact impact-${violation.impact || 'moderate'}">${violation.impact || 'moderate'}</span>
                            </div>
                            <div class="violation-details">
                                <div class="violation-description">${violation.description || 'No description available'}</div>
                            </div>
                            <div class="violation-stats">
                                <div class="stat-item">
                                    <div class="stat-value">${violation.affectedPages || 0}</div>
                                    <div class="stat-label">Pages Affected</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value">${violation.totalOccurrences || 0}</div>
                                    <div class="stat-label">Total Occurrences</div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `;
} 