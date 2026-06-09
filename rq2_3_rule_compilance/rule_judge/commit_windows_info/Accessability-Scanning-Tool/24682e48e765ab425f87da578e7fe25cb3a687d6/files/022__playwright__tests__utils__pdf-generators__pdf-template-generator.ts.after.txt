import { SiteWideAccessibilityReport } from '../accessibility-test-orchestrator';

export class PdfTemplateGenerator {
    /**
     * Generates audience-specific HTML template
     */
    generateAudienceSpecificTemplate(
        report: SiteWideAccessibilityReport,
        audience: string,
        displayName: string
    ): string {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Report - ${displayName}</title>
    <style>
        ${this.getPdfStyles()}
    </style>
</head>
<body>
    ${this.generateHeader(report, audience, displayName)}
    ${this.generateContent(report, audience)}
    ${this.generateFooter()}
</body>
</html>`;
    }

    /**
     * Generates PDF-specific CSS styles
     */
    private getPdfStyles(): string {
        return `
        @page {
            size: A4;
            margin: 0.75in;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            font-size: 11pt;
            margin: 0;
            padding: 0;
        }

        .header {
            background: linear-gradient(135deg, #1e214d 0%, #db0064 100%);
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }

        .header h1 {
            margin: 0;
            font-size: 24pt;
            font-weight: 700;
        }

        .header .subtitle {
            margin: 5px 0 0 0;
            font-size: 14pt;
            opacity: 0.9;
        }

        .header .meta {
            margin-top: 10px;
            font-size: 10pt;
            opacity: 0.8;
        }

        .section {
            margin-bottom: 30px;
            page-break-inside: avoid;
        }

        .section h2 {
            color: #1e214d;
            border-bottom: 2px solid #db0064;
            padding-bottom: 5px;
            margin-bottom: 15px;
            font-size: 16pt;
        }

        .section h3 {
            color: #1e214d;
            margin-top: 20px;
            margin-bottom: 10px;
            font-size: 14pt;
        }

        .summary-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .summary-item {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }

        .summary-item .value {
            font-size: 24pt;
            font-weight: 700;
            color: #1e214d;
            display: block;
        }

        .summary-item .label {
            font-size: 10pt;
            color: #6c757d;
            margin-top: 5px;
        }

        .violation-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 10pt;
        }

        .violation-table th,
        .violation-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }

        .violation-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #1e214d;
        }

        .violation-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }

        .impact-critical { color: #dc3545; font-weight: 600; }
        .impact-serious { color: #fd7e14; font-weight: 600; }
        .impact-moderate { color: #ffc107; font-weight: 600; }
        .impact-minor { color: #28a745; font-weight: 600; }

        .code-snippet {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 8px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            word-break: break-all;
            margin: 5px 0;
        }

        .recommendation-list {
            margin-left: 20px;
            padding-left: 20px;
            line-height: 1.6;
        }

        .recommendation-list li {
            margin-bottom: 5px;
        }

        .footer {
            margin-top: 40px;
            padding: 20px;
            border-top: 1px solid #e9ecef;
            font-size: 9pt;
            color: #6c757d;
            text-align: center;
        }

        .page-break {
            page-break-before: always;
        }

        .no-break {
            page-break-inside: avoid;
        }

        .wcag-level {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: 600;
            color: white;
        }

        .wcag-a { background-color: #28a745; }
        .wcag-aa { background-color: #ffc107; color: #212529; }
        .wcag-aaa { background-color: #dc3545; }

        .chart-container {
            margin: 20px 0;
            text-align: center;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1e214d 0%, #db0064 100%);
            transition: width 0.3s ease;
        }

        .highlight {
            background-color: #fcc700;
            padding: 2px 4px;
            border-radius: 3px;
            font-weight: 600;
        }

        .brand-accent {
            color: #db0064;
        }

        .text-muted {
            color: #6c757d;
        }

        .text-center {
            text-align: center;
        }

        .mb-3 {
            margin-bottom: 1rem;
        }

        .mt-3 {
            margin-top: 1rem;
        }
    `;
    }

    /**
     * Generates header section
     */
    private generateHeader(
        report: SiteWideAccessibilityReport,
        audience: string,
        displayName: string
    ): string {
        const date = new Date(report.timestamp).toLocaleDateString('en-GB', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });

        return `
        <div class="header">
            <h1>Accessibility Report</h1>
            <div class="subtitle">For ${displayName}</div>
            <div class="meta">
                <strong>Site:</strong> ${report.siteUrl} | 
                <strong>Date:</strong> ${date} | 
                <strong>Test Suite:</strong> ${report.testSuite}
            </div>
        </div>
    `;
    }

    /**
     * Generates content based on audience
     */
    private generateContent(report: SiteWideAccessibilityReport, audience: string): string {
        switch (audience) {
            case 'stakeholders':
                return this.generateStakeholderContent(report);
            case 'researchers':
                return this.generateResearcherContent(report);
            case 'developers':
                return this.generateDeveloperContent(report);
            default:
                return this.generateGenericContent(report);
        }
    }

    /**
     * Generates content for stakeholders
     */
    private generateStakeholderContent(report: SiteWideAccessibilityReport): string {
        const complianceScore = Math.round(report.summary.compliancePercentage);
        const totalIssues = report.summary.totalViolations;
        const criticalIssues = report.summary.criticalViolations;

        return `
        <div class="section">
            <h2>Executive Summary</h2>
            <div class="summary-card">
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="value">${complianceScore}%</span>
                        <div class="label">Compliance Score</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${totalIssues}</span>
                        <div class="label">Total Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${criticalIssues}</span>
                        <div class="label">Critical Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${report.summary.totalPages}</span>
                        <div class="label">Pages Tested</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${complianceScore}%"></div>
                </div>
                <div class="text-center text-muted">Overall Accessibility Compliance</div>
            </div>
        </div>

        <div class="section">
            <h2>Business Impact</h2>
            <p><strong>Risk Level:</strong> ${criticalIssues > 10 ? 'High' : criticalIssues > 5 ? 'Medium' : 'Low'}</p>
            <p><strong>Potential User Impact:</strong> ${report.summary.pagesWithViolations} out of ${report.summary.totalPages} pages have accessibility barriers that could prevent users from accessing your content.</p>
            <p><strong>Legal Compliance:</strong> ${complianceScore > 80 ? 'Good progress towards' : 'Requires significant work to achieve'} WCAG 2.1 AA compliance.</p>
        </div>

        <div class="section">
            <h2>Priority Actions</h2>
            <h3>Immediate Actions (High Priority)</h3>
            <ul>
                ${report.summary.mostCommonViolations.slice(0, 3).map(violation =>
            `<li>Address <strong>${violation.id}</strong> issues across ${violation.affectedPages} pages</li>`
        ).join('')}
            </ul>
            
            <h3>Recommended Timeline</h3>
            <ul>
                <li><strong>Week 1-2:</strong> Fix critical accessibility issues</li>
                <li><strong>Week 3-4:</strong> Address serious violations</li>
                <li><strong>Month 2:</strong> Implement comprehensive accessibility testing</li>
            </ul>
        </div>
    `;
    }

    /**
     * Generates content for researchers
     */
    private generateResearcherContent(report: SiteWideAccessibilityReport): string {
        return `
        <div class="section">
            <h2>User Experience Impact Analysis</h2>
            <div class="summary-card">
                <h3>Accessibility Scenarios Affected</h3>
                <ul>
                    <li><strong>Screen Reader Users:</strong> ${this.countViolationType(report, 'aria|label|heading')} issues detected</li>
                    <li><strong>Keyboard Navigation:</strong> ${this.countViolationType(report, 'keyboard|focus')} issues detected</li>
                    <li><strong>Visual Impairments:</strong> ${this.countViolationType(report, 'color|contrast')} issues detected</li>
                    <li><strong>Motor Impairments:</strong> ${this.countViolationType(report, 'target|click')} issues detected</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>Common Violation Patterns</h2>
            <table class="violation-table">
                <thead>
                    <tr>
                        <th>Issue Type</th>
                        <th>Pages Affected</th>
                        <th>Total Occurrences</th>
                        <th>Impact Level</th>
                        <th>User Groups Affected</th>
                    </tr>
                </thead>
                <tbody>
                    ${report.summary.mostCommonViolations.map(violation => `
                        <tr>
                            <td>${violation.id}</td>
                            <td>${violation.affectedPages}</td>
                            <td>${violation.totalOccurrences}</td>
                            <td><span class="impact-${violation.impact}">${violation.impact}</span></td>
                            <td>${this.getUserGroupsAffected(violation.id)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Testing Recommendations</h2>
            <h3>Usability Testing Focus Areas</h3>
            <ul>
                <li>Test with screen reader users on pages with high violation counts</li>
                <li>Conduct keyboard-only navigation testing</li>
                <li>Test with users who have visual impairments</li>
                <li>Validate colour contrast with colour-blind users</li>
            </ul>
        </div>
    `;
    }

    /**
     * Generates content for developers
     */
    private generateDeveloperContent(report: SiteWideAccessibilityReport): string {
        return `
        <div class="section">
            <h2>Technical Summary</h2>
            <div class="summary-card">
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="value">${report.summary.criticalViolations}</span>
                        <div class="label">Critical Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${report.summary.seriousViolations}</span>
                        <div class="label">Serious Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${report.summary.moderateViolations}</span>
                        <div class="label">Moderate Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${report.summary.minorViolations}</span>
                        <div class="label">Minor Issues</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Most Common Violations</h2>
            <table class="violation-table">
                <thead>
                    <tr>
                        <th>Violation ID</th>
                        <th>Pages</th>
                        <th>Count</th>
                        <th>Impact</th>
                        <th>WCAG Level</th>
                        <th>Tools</th>
                    </tr>
                </thead>
                <tbody>
                    ${report.summary.mostCommonViolations.map(violation => `
                        <tr>
                            <td><code>${violation.id}</code></td>
                            <td>${violation.affectedPages}</td>
                            <td>${violation.totalOccurrences}</td>
                            <td><span class="impact-${violation.impact}">${violation.impact}</span></td>
                            <td><span class="wcag-level wcag-aa">AA</span></td>
                            <td>axe-core, pa11y</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>Implementation Priority</h2>
            <h3>High Priority (Fix First)</h3>
            <ul>
                ${report.summary.mostCommonViolations
                .filter(v => v.totalOccurrences > 5)
                .slice(0, 5)
                .map(violation => `<li><code>${violation.id}</code> - ${violation.totalOccurrences} occurrences</li>`)
                .join('')}
            </ul>
        </div>
    `;
    }

    /**
     * Generates generic content
     */
    private generateGenericContent(report: SiteWideAccessibilityReport): string {
        return `
        <div class="section">
            <h2>Accessibility Overview</h2>
            <p>This report provides a comprehensive analysis of accessibility issues found across ${report.summary.totalPages} pages.</p>
            
            <div class="summary-card">
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="value">${report.summary.totalViolations}</span>
                        <div class="label">Total Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${Math.round(report.summary.compliancePercentage)}%</span>
                        <div class="label">Compliance Score</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    }

    /**
     * Generates footer
     */
    private generateFooter(): string {
        return `
        <div class="footer">
            <p>Generated by Nimble Accessibility Testing Suite | Report created on ${new Date().toLocaleDateString('en-GB')}</p>
            <p>For questions about this report, please contact your accessibility team.</p>
        </div>
    `;
    }

    /**
     * Counts violations by type pattern
     */
    private countViolationType(report: SiteWideAccessibilityReport, pattern: string): number {
        const regex = new RegExp(pattern, 'i');
        return Object.keys(report.violationsByType).filter(id => regex.test(id)).length;
    }

    /**
     * Gets user groups affected by violation type
     */
    private getUserGroupsAffected(violationId: string): string {
        if (violationId.includes('color') || violationId.includes('contrast')) {
            return 'Visually impaired, colour blind';
        }
        if (violationId.includes('aria') || violationId.includes('label')) {
            return 'Screen reader users';
        }
        if (violationId.includes('keyboard') || violationId.includes('focus')) {
            return 'Keyboard users, motor impaired';
        }
        return 'All users';
    }
} 