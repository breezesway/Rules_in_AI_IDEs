import { renderHeader, HeaderProps } from './Header';
import { renderFooter, FooterProps } from './Footer';
import { renderDetailedResultsSection, DetailedResultsSectionProps } from './DetailedResultsSection';
import { SiteWideAccessibilityReport, AccessibilityReport, ProcessedViolation } from '@/core/types/common';

export interface ReportDetailsPageProps {
    header?: HeaderProps;
    footer?: FooterProps;
    reportId?: string;
}

export function renderReportDetailsPage(props: ReportDetailsPageProps = {}): string {
    const {
        header = {},
        footer = {},
        reportId = ''
    } = props;

    return `
        <!DOCTYPE html>
        <html lang="en-GB">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Report Details - Accessibility Testing Tool</title>
            <meta name="description" content="Detailed breakdown of accessibility scan results">
            <link rel="stylesheet" href="/styles.css?v=20250125">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            ${renderHeader({ ...header, currentPage: 'reports' })}
            
            <main class="main">
                <div class="report-details-container">
                    <div id="loadingSection" class="loading-section" style="display: block;">
                        <div class="loading-spinner"></div>
                        <p>Loading report details...</p>
                    </div>
                    
                    <div id="errorSection" class="error-section" style="display: none;">
                        <h3>Error Loading Report</h3>
                        <p id="errorMessage"></p>
                    </div>
                    
                    <div id="reportContent" style="display: none;">
                        <!-- Report content will be populated here -->
                    </div>
                </div>
            </main>

            ${renderFooter(footer)}

            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    const reportId = '${reportId}' || getReportIdFromUrl();
                    const loadingSection = document.getElementById('loadingSection');
                    const errorSection = document.getElementById('errorSection');
                    const reportContent = document.getElementById('reportContent');
                    const errorMessage = document.getElementById('errorMessage');

                    function getReportIdFromUrl() {
                        const pathParts = window.location.pathname.split('/');
                        return pathParts[pathParts.length - 1];
                    }

                    function showLoading() {
                        loadingSection.style.display = 'block';
                        errorSection.style.display = 'none';
                        reportContent.style.display = 'none';
                    }

                    // Show loading state initially
                    showLoading();

                    function showError(message) {
                        errorMessage.textContent = message;
                        loadingSection.style.display = 'none';
                        errorSection.style.display = 'block';
                        reportContent.style.display = 'none';
                    }

                    function showContent() {
                        loadingSection.style.display = 'none';
                        errorSection.style.display = 'none';
                        reportContent.style.display = 'block';
                    }

                    // Load report data
                    if (reportId) {
                        showLoading();
                        
                        fetch(\`/api/reports/\${reportId}\`)
                            .then(response => {
                                if (!response.ok) {
                                    throw new Error(\`HTTP \${response.status}: \${response.statusText}\`);
                                }
                                return response.json();
                            })
                            .then(data => {
                                if (data.success) {
                                    // Use the shared component to render the detailed results
                                    const detailedResultsProps = {
                                        report: data.data,
                                        visible: true,
                                        showHeader: true,
                                        showBackButton: true
                                    };
                                    
                                    // For now, we'll render the content directly since we can't call the component function
                                    // In a real implementation, this would be handled by the server-side rendering
                                    reportContent.innerHTML = renderDetailedResultsContent(data.data);
                                    showContent();
                                } else {
                                    showError(data.error || 'Failed to load report data');
                                }
                            })
                            .catch(error => {
                                showError('Failed to load report: ' + error.message);
                            });
                    } else {
                        showError('No report ID provided');
                    }

                    // Client-side rendering function for detailed results
                    function renderDetailedResultsContent(report) {
                        const data = report.data || report;
                        const summary = data.summary || {};
                        const violations = data.violations || [];
                        const pageReports = data.pageReports || [];
                        const mostCommonViolations = data.mostCommonViolations || [];
                        
                        const compliancePercentage = summary.compliancePercentage || 0;
                        const complianceClass = compliancePercentage >= 90 ? 'good' : 
                                               compliancePercentage >= 70 ? 'moderate' : 
                                               compliancePercentage >= 50 ? 'serious' : 'critical';

                        function formatDate(dateString) {
                            return new Date(dateString).toLocaleDateString('en-GB', {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                            });
                        }

                        function renderViolationCard(violation) {
                            const impactClass = \`impact-\${violation.impact || 'moderate'}\`;
                            const elements = violation.elements || [];
                            
                            return \`
                                <div class="violation-card">
                                    <div class="violation-header">
                                        <div class="violation-title">
                                            <code>\${violation.id}</code>
                                            <span class="wcag-level">WCAG \${violation.wcagLevel || 'Unknown'}</span>
                                        </div>
                                        <span class="violation-impact \${impactClass}">\${violation.impact || 'moderate'}</span>
                                    </div>
                                    
                                    <div class="violation-details">
                                        <div class="violation-description">\${violation.description || 'No description available'}</div>
                                        <div class="violation-help">\${violation.help || 'No help information available'}</div>
                                    </div>
                                    
                                    <div class="violation-stats">
                                        <div class="stat-item">
                                            <div class="stat-value">\${violation.occurrences || 1}</div>
                                            <div class="stat-label">Occurrences</div>
                                        </div>
                                        <div class="stat-item">
                                            <div class="stat-value">\${elements.length}</div>
                                            <div class="stat-label">Elements</div>
                                        </div>
                                        <div class="stat-item">
                                            <div class="stat-value">\${violation.tools?.join(', ') || 'Unknown'}</div>
                                            <div class="stat-label">Tools</div>
                                        </div>
                                    </div>
                                    
                                    \${elements.length > 0 ? \`
                                        <div class="violation-elements">
                                            <h4>Affected Elements (\${elements.length})</h4>
                                            \${elements.map(element => \`
                                                <div class="element-item">
                                                    <div class="element-html">\${element.html || 'No HTML available'}</div>
                                                    <div class="element-selector">Selector: \${element.selector || 'No selector available'}</div>
                                                    \${element.failureSummary ? \`
                                                        <div class="element-failure">Failure: \${element.failureSummary}</div>
                                                    \` : ''}
                                                </div>
                                            \`).join('')}
                                        </div>
                                    \` : ''}
                                    
                                    \${violation.remediation ? \`
                                        <div class="remediation-info">
                                            <h4>Remediation</h4>
                                            <p><strong>Priority:</strong> \${violation.remediation.priority}</p>
                                            <p><strong>Effort:</strong> \${violation.remediation.effort}</p>
                                            \${violation.remediation.suggestions?.length > 0 ? \`
                                                <div>
                                                    <strong>Suggestions:</strong>
                                                    <ul>
                                                        \${violation.remediation.suggestions.map(suggestion => \`
                                                            <li>\${suggestion}</li>
                                                        \`).join('')}
                                                    </ul>
                                                </div>
                                            \` : ''}
                                        </div>
                                    \` : ''}
                                </div>
                            \`;
                        }

                        function renderPageItem(page) {
                            const violations = page.violations || [];
                            const pageSummary = page.summary || {};
                            
                            return \`
                                <div class="page-item">
                                    <div class="page-url">\${page.url}</div>
                                    <div class="page-stats">
                                        <span>\${violations.length} violations</span>
                                        <span>\${pageSummary.criticalViolations || 0} critical</span>
                                        <span>\${pageSummary.seriousViolations || 0} serious</span>
                                        <span>\${pageSummary.moderateViolations || 0} moderate</span>
                                        <span>\${pageSummary.minorViolations || 0} minor</span>
                                    </div>
                                </div>
                            \`;
                        }

                        return \`
                            <a href="/reports" class="back-button">
                                ← Back to Reports
                            </a>
                            
                            <div class="report-header">
                                <h1>Accessibility Report</h1>
                                <p>\${data.siteUrl || 'Unknown Site'}</p>
                                <div class="report-meta">
                                    <div class="meta-item">
                                        <div class="meta-label">Report Type</div>
                                        <div class="meta-value">\${data.reportType || 'Unknown'}</div>
                                    </div>
                                    <div class="meta-item">
                                        <div class="meta-label">Scan Date</div>
                                        <div class="meta-value">\${formatDate(data.timestamp || data.createdAt)}</div>
                                    </div>
                                    <div class="meta-item">
                                        <div class="meta-label">WCAG Level</div>
                                        <div class="meta-value">\${data.wcagLevel || 'Unknown'}</div>
                                    </div>
                                    <div class="meta-item">
                                        <div class="meta-label">Tools Used</div>
                                        <div class="meta-value">\${(data.metadata?.toolsUsed || []).join(', ') || 'Unknown'}</div>
                                    </div>
                                </div>
                            </div>

                            <div class="results-section">
                                <h2 class="section-heading">Summary</h2>
                                <div class="summary-grid">
                                    <div class="summary-card">
                                        <div class="summary-value \${complianceClass}">\${compliancePercentage}%</div>
                                        <div class="summary-label">Compliance Score</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value">\${summary.totalPages || 0}</div>
                                        <div class="summary-label">Pages Scanned</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value">\${summary.totalViolations || 0}</div>
                                        <div class="summary-label">Total Violations</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value critical">\${summary.criticalViolations || 0}</div>
                                        <div class="summary-label">Critical</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value serious">\${summary.seriousViolations || 0}</div>
                                        <div class="summary-label">Serious</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value moderate">\${summary.moderateViolations || 0}</div>
                                        <div class="summary-label">Moderate</div>
                                    </div>
                                    <div class="summary-card">
                                        <div class="summary-value minor">\${summary.minorViolations || 0}</div>
                                        <div class="summary-label">Minor</div>
                                    </div>
                                </div>
                            </div>

                            \${violations.length > 0 ? \`
                                <div class="results-section">
                                    <h2 class="section-heading">Violations (\${violations.length})</h2>
                                    \${violations.map(violation => renderViolationCard(violation)).join('')}
                                </div>
                            \` : ''}

                            \${pageReports.length > 0 ? \`
                                <div class="results-section">
                                    <h2 class="section-heading">Pages Analyzed (\${pageReports.length})</h2>
                                    \${pageReports.map(page => renderPageItem(page)).join('')}
                                </div>
                            \` : ''}

                            \${mostCommonViolations.length > 0 ? \`
                                <div class="results-section">
                                    <h2 class="section-heading">Most Common Violations</h2>
                                    \${mostCommonViolations.map(violation => \`
                                        <div class="violation-card">
                                            <div class="violation-header">
                                                <div class="violation-title">
                                                    <code>\${violation.id}</code>
                                                </div>
                                                <span class="violation-impact impact-\${violation.impact || 'moderate'}">\${violation.impact || 'moderate'}</span>
                                            </div>
                                            <div class="violation-details">
                                                <div class="violation-description">\${violation.description || 'No description available'}</div>
                                            </div>
                                            <div class="violation-stats">
                                                <div class="stat-item">
                                                    <div class="stat-value">\${violation.affectedPages || 0}</div>
                                                    <div class="stat-label">Pages Affected</div>
                                                </div>
                                                <div class="stat-item">
                                                    <div class="stat-value">\${violation.totalOccurrences || 0}</div>
                                                    <div class="stat-label">Total Occurrences</div>
                                                </div>
                                            </div>
                                        </div>
                                    \`).join('')}
                                </div>
                            \` : ''}
                        \`;
                    }
                });
            </script>
        </body>
        </html>
    `;
} 