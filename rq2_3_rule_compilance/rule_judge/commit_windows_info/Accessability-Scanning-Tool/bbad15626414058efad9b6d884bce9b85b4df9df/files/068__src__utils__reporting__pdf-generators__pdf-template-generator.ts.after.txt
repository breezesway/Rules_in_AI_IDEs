import { SiteWideAccessibilityReport } from '@/core/types/common';
import * as fs from 'fs';
import * as path from 'path';

interface ViolationItem {
    id: string;
    // Add other properties as needed
}

interface PriorityMatrix {
    'high-low': ViolationItem[];
    'high-medium': ViolationItem[];
    'high-high': ViolationItem[];
    'medium-low': ViolationItem[];
    'medium-medium': ViolationItem[];
    'medium-high': ViolationItem[];
    'low-low': ViolationItem[];
    'low-medium': ViolationItem[];
    'low-high': ViolationItem[];
}

interface ScanMetadata {
    totalPages?: number;
    totalViolations?: number;
    compliancePercentage?: number;
    wcagLevel?: string;
    criticalViolations?: number;
    seriousViolations?: number;
    moderateViolations?: number;
    minorViolations?: number;
    browser?: string;
    viewport?: string;
    scanConfiguration?: {
        maxPages?: number;
        maxDepth?: number;
        maxConcurrency?: number;
        retryFailedPages?: boolean;
        generateReports?: boolean;
        wcagLevel?: string;
    };
    performanceMetrics?: {
        totalScanTime?: number;
        averageTimePerPage?: number;
        successRate?: number;
        pagesAnalyzed?: number;
        pagesWithViolations?: number;
    };
    toolsUsed?: string[];
    scanStartedAt?: Date;
    scanCompletedAt?: Date;
    scanId?: string;
    scanType?: 'full-site' | 'single-page' | 'quick';
    userAgent?: string;
    crawlDepth?: number;
    excludedPatterns?: string[];
}

export class PdfTemplateGenerator {
    /**
     * Generates audience-specific HTML template with enhanced metadata
     */
    generateAudienceSpecificTemplate(
        report: SiteWideAccessibilityReport,
        audience: string,
        displayName: string,
        scanMetadata?: ScanMetadata
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
    <main class="content-wrapper">
      ${this.generateEnhancedHeader(report, audience, displayName, scanMetadata)}
      ${this.generateContent(report, audience, scanMetadata)}
      ${this.generateFooter()}
    </main>
</body>
</html>`;
    }

    /**
     * Generates enhanced header with scan metadata
     */
    private generateEnhancedHeader(
        report: SiteWideAccessibilityReport,
        audience: string,
        displayName: string,
        scanMetadata?: ScanMetadata
    ): string {
        // Get WCAG level display name
        const wcagLevel = report.wcagLevel || 'WCAG2AA';
        const wcagDisplayName = {
            'WCAG2A': 'WCAG 2.1 Level A',
            'WCAG2AA': 'WCAG 2.1 Level AA',
            'WCAG2AAA': 'WCAG 2.1 Level AAA',
            'WCAG22A': 'WCAG 2.2 Level A',
            'WCAG22AA': 'WCAG 2.2 Level AA',
            'WCAG22AAA': 'WCAG 2.2 Level AAA'
        }[wcagLevel] || 'WCAG 2.1 Level AA';

        // Format scan duration
        const scanDuration = scanMetadata?.performanceMetrics?.totalScanTime
            ? this.formatDuration(scanMetadata.performanceMetrics.totalScanTime)
            : 'N/A';

        // Format scan dates
        const scanStartDate = scanMetadata?.scanStartedAt
            ? new Date(scanMetadata.scanStartedAt).toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })
            : new Date(report.timestamp).toLocaleDateString('en-GB');

        const scanEndDate = scanMetadata?.scanCompletedAt
            ? new Date(scanMetadata.scanCompletedAt).toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })
            : 'N/A';

        return `
      <div class="header">
        <div class="header-content">
            <h1>${report.siteUrl} - ${displayName} Report</h1>
            <div class="subtitle">Accessibility Testing Report - ${wcagDisplayName}</div>
            <div class="meta">
                <span>Scan Date: ${scanStartDate}</span>
                <span>WCAG Standard: ${wcagDisplayName}</span>
                <span>Total Violations: ${report.summary.totalViolations}</span>
                ${scanMetadata?.scanId ? `<span>Scan ID: ${scanMetadata.scanId}</span>` : ''}
            </div>
            ${scanMetadata ? this.generateScanMetadataSection(scanMetadata) : ''}
        </div>
      </div>`;
    }

    /**
     * Generates scan metadata section for enhanced reports
     */
    private generateScanMetadataSection(scanMetadata: ScanMetadata): string {
        const toolsUsed = scanMetadata.toolsUsed?.join(', ') || 'axe-core, Pa11y';
        const scanType = scanMetadata.scanType || 'full-site';
        const scanTypeDisplay = {
            'full-site': 'Full Site Scan',
            'single-page': 'Single Page Scan',
            'quick': 'Quick Scan'
        }[scanType] || 'Full Site Scan';

        return `
        <div class="scan-metadata">
            <div class="metadata-grid">
                <div class="metadata-item">
                    <strong>Scan Type:</strong> ${scanTypeDisplay}
                </div>
                <div class="metadata-item">
                    <strong>Scan Duration:</strong> ${this.formatDuration(scanMetadata.performanceMetrics?.totalScanTime || 0)}
                </div>
                <div class="metadata-item">
                    <strong>Pages Analyzed:</strong> ${scanMetadata.performanceMetrics?.pagesAnalyzed || scanMetadata.totalPages || 'N/A'}
                </div>
                <div class="metadata-item">
                    <strong>Success Rate:</strong> ${scanMetadata.performanceMetrics?.successRate ? `${Math.round(scanMetadata.performanceMetrics.successRate)}%` : 'N/A'}
                </div>
                <div class="metadata-item">
                    <strong>Tools Used:</strong> ${toolsUsed}
                </div>
                <div class="metadata-item">
                    <strong>Browser:</strong> ${scanMetadata.browser || scanMetadata.userAgent ? 'Chrome (Playwright)' : 'N/A'}
                </div>
                <div class="metadata-item">
                    <strong>Crawl Depth:</strong> ${scanMetadata.crawlDepth !== undefined ? scanMetadata.crawlDepth : 'N/A'}
                </div>
                <div class="metadata-item">
                    <strong>Max Concurrency:</strong> ${scanMetadata.scanConfiguration?.maxConcurrency || 'N/A'}
                </div>
            </div>
            ${scanMetadata.excludedPatterns && scanMetadata.excludedPatterns.length > 0
                ? `<div class="excluded-patterns">
                    <strong>Excluded Patterns:</strong> ${scanMetadata.excludedPatterns.join(', ')}
                   </div>`
                : ''
            }
        </div>`;
    }

    /**
     * Formats duration in milliseconds to human readable format
     */
    private formatDuration(milliseconds: number): string {
        if (milliseconds < 1000) {
            return `${milliseconds}ms`;
        }

        const seconds = Math.floor(milliseconds / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);

        if (hours > 0) {
            const remainingMinutes = minutes % 60;
            return `${hours}h ${remainingMinutes}m`;
        } else if (minutes > 0) {
            const remainingSeconds = seconds % 60;
            return `${minutes}m ${remainingSeconds}s`;
        } else {
            return `${seconds}s`;
        }
    }

    /**
     * Generates PDF-specific CSS styles
     */
    private getPdfStyles(): string {
        return `
        @page content {
            size: A4 landscape;
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

        .content-wrapper {
          page: content;
        }

        .header {
            background: linear-gradient(135deg, #1e214d 0%, #db0064 100%);
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }

        .header-content {
            position: relative;
            z-index: 2;
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

        .alert-critical {
            background-color: #f8d7da;
            color: #721c24;
            padding: 10px;
            border: 1px solid #f5c6cb;
            border-radius: 4px;
            margin-top: 15px;
            font-weight: 600;
        }

        .priority-matrix {
            border-collapse: collapse;
            margin-top: 20px;
            margin-bottom: 20px;
            width: 100%;
        }

        .matrix-header {
            background-color: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            font-weight: 600;
            color: #1e214d;
        }

        .matrix-header .header {
            text-align: center;
            padding: 10px 0;
        }

        .matrix-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr; /* Adjust as needed */
            gap: 10px;
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .matrix-row:last-child {
            border-bottom: none;
        }

        .matrix-cell {
            padding: 10px;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            text-align: center;
            background-color: #f8f9fa;
        }

        .matrix-cell.header {
            background-color: #e9ecef;
            font-weight: 600;
            color: #1e214d;
        }

        .matrix-cell.impact-label {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #1e214d;
            padding: 10px 0;
        }

        .matrix-item {
            background-color: #e9ecef;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 9pt;
            font-weight: 500;
            color: #1e214d;
            margin-bottom: 5px;
        }

        .priority-matrix .quick-wins { background-color: #d4edda; }
        .priority-matrix .major-projects { background-color: #fff3cd; }
        .priority-matrix .fill-ins { background-color: #e2e3e5; }
        .priority-matrix .thankless { background-color: #f8d7da; }

        .priority-legend {
            display: flex;
            justify-content: space-around;
            margin-top: 15px;
            font-size: 9pt;
            color: #6c757d;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .testing-guide h3 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #1e214d;
        }

        .testing-checklist {
            list-style: none;
            padding-left: 20px;
            line-height: 1.6;
        }

        .testing-checklist li {
            margin-bottom: 5px;
        }

        .tool-list {
            list-style: none;
            padding-left: 20px;
            line-height: 1.6;
        }

        .tool-list li {
            margin-bottom: 5px;
        }

        .resources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .resource-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }

        .resource-card h3 {
            margin-top: 0;
            margin-bottom: 15px;
            color: #1e214d;
        }

        .resource-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .resource-card ul li {
            margin-bottom: 10px;
        }

        .resource-card ul li a {
            color: #db0064;
            text-decoration: none;
        }

        .resource-card ul li a:hover {
            text-decoration: underline;
        }

        .workflow-section h3 {
            margin-top: 20px;
            margin-bottom: 10px;
            color: #1e214d;
        }

        .workflow-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .workflow-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }

        .workflow-card h4 {
            margin-top: 0;
            margin-bottom: 15px;
            color: #1e214d;
        }

        .workflow-card ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .workflow-card ul li {
            margin-bottom: 10px;
        }

        .violation-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .violation-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .violation-title {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 14pt;
            font-weight: 600;
            color: #1e214d;
        }

        .violation-title .wcag-level {
            font-size: 9pt;
            padding: 2px 6px;
            border-radius: 3px;
        }

                          .violation-title .priority-high { background-color: #fcc700; }
         .violation-title .priority-medium { background-color: #ffc107; }
         .violation-title .priority-low { background-color: #28a745; }

        .violation-stats {
            display: flex;
            gap: 15px;
            font-size: 9pt;
            color: #6c757d;
        }

        .violation-description p {
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .violation-pages strong {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #1e214d;
        }

        .violation-pages ul {
            list-style: none;
            padding-left: 20px;
            margin: 0;
        }

        .violation-pages ul li {
            margin-bottom: 5px;
        }

        .violation-pages ul li code {
            background-color: #e9ecef;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .remediation-section h4 {
            margin-top: 15px;
            margin-bottom: 10px;
            color: #1e214d;
        }

        .remediation-steps ol {
            list-style: none;
            padding-left: 20px;
            margin: 0;
        }

        .remediation-steps ol li {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .remediation-steps ol li strong {
            font-weight: 600;
            color: #1e214d;
        }

        .code-snippet pre {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
            font-size: 9pt;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .testing-instructions ul {
            list-style: none;
            padding-left: 20px;
            margin: 0;
        }

        .testing-instructions ul li {
            margin-bottom: 10px;
            line-height: 1.6;
        }

        .testing-instructions ul li strong {
            font-weight: 600;
            color: #1e214d;
        }

        .violations-detailed {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .scan-metadata {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 15px;
            margin-top: 15px;
            font-size: 10pt;
        }

        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 10px;
        }

        .metadata-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .metadata-item strong {
            color: #fcc700;
            font-weight: 600;
        }

        .excluded-patterns {
            background: rgba(255, 255, 255, 0.1);
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 9pt;
        }

        .excluded-patterns strong {
            color: #fcc700;
            font-weight: 600;
        }

        .performance-metrics {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .performance-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }

        .performance-item {
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }

        .performance-item .value {
            font-size: 18pt;
            font-weight: 700;
            color: #1e214d;
            display: block;
        }

        .performance-item .label {
            font-size: 9pt;
            color: #6c757d;
            margin-top: 5px;
        }

        .technical-details {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .technical-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .technical-item {
            padding: 10px;
            background: white;
            border-radius: 6px;
            border: 1px solid #e9ecef;
        }

        .technical-item strong {
            color: #1e214d;
            font-weight: 600;
            display: block;
            margin-bottom: 5px;
        }

        .scan-timeline {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .timeline-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e9ecef;
        }

        .timeline-item:last-child {
            border-bottom: none;
        }

        .timeline-label {
            font-weight: 600;
            color: #1e214d;
        }

        .timeline-value {
            color: #6c757d;
        }
    `;
    }

    /**
     * Generates content based on audience
     */
    private generateContent(report: SiteWideAccessibilityReport, audience: string, scanMetadata?: ScanMetadata): string {
        switch (audience) {
            case 'stakeholders':
                return this.generateStakeholderContent(report, scanMetadata);
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
    private generateStakeholderContent(report: SiteWideAccessibilityReport, scanMetadata?: ScanMetadata): string {
        const complianceScore = Math.round(report.summary?.compliancePercentage || 0);
        const totalIssues = report.summary?.totalViolations || 0;
        const criticalIssues = report.summary?.criticalViolations || 0;
        const totalPages = report.summary?.totalPages || 0;
        const pagesWithViolations = report.summary?.pagesWithViolations || 0;
        const mostCommonViolations = report.summary?.mostCommonViolations || [];

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
                        <span class="value">${totalPages}</span>
                        <div class="label">Pages Tested</div>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${complianceScore}%"></div>
                </div>
                <div class="text-center text-muted">Overall Accessibility Compliance</div>
            </div>
        </div>

        ${scanMetadata ? this.generatePerformanceMetricsSection(scanMetadata) : ''}

        <div class="section">
            <h2>Business Impact</h2>
            <p><strong>Risk Level:</strong> ${criticalIssues > 10 ? 'High' : criticalIssues > 5 ? 'Medium' : 'Low'}</p>
            <p><strong>Potential User Impact:</strong> ${pagesWithViolations} out of ${totalPages} pages have accessibility barriers that could prevent users from accessing your content.</p>
            <p><strong>Legal Compliance:</strong> ${complianceScore > 80 ? 'Good progress towards' : 'Requires significant work to achieve'} ${report.wcagLevel ? report.wcagLevel.replace('WCAG', 'WCAG ').replace('2', '2.').replace('22', '2.2') : 'WCAG 2.1 AA'} compliance.</p>
        </div>

        <div class="section">
            <h2>Priority Actions</h2>
            <h3>Immediate Actions (High Priority)</h3>
            <ul>
                ${mostCommonViolations.length > 0
                ? mostCommonViolations
                    .slice(0, 3)
                    .map(
                        violation =>
                            `<li>Address <strong>${violation.id || 'Unknown Issue'}</strong> issues across ${violation.affectedPages || 0} pages</li>`
                    )
                    .join('')
                : '<li>No specific violations identified in this scan</li>'
            }
            </ul>
            
            <h3>Recommended Timeline</h3>
            <ul>
                <li><strong>Week 1-2:</strong> Fix critical accessibility issues</li>
                <li><strong>Week 3-4:</strong> Address serious violations</li>
                <li><strong>Month 2:</strong> Implement comprehensive accessibility testing</li>
            </ul>
        </div>

        ${scanMetadata ? this.generateTechnicalDetailsSection(scanMetadata) : ''}
    `;
    }

    /**
     * Generates content for researchers
     */
    private generateResearcherContent(report: SiteWideAccessibilityReport): string {
        const mostCommonViolations = report.summary?.mostCommonViolations || [];

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
            ${mostCommonViolations.length > 0 ? `
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
                    ${mostCommonViolations
                    .map(
                        violation => `
                                <tr>
                                    <td>${violation.id || 'Unknown Issue'}</td>
                                    <td>${violation.affectedPages || 0}</td>
                                    <td>${violation.totalOccurrences || 0}</td>
                                    <td><span class="impact-${violation.impact || 'medium'}">${violation.impact || 'Medium'}</span></td>
                                    <td>${this.getUserGroupsAffected(violation.id || '')}</td>
                                </tr>
                            `
                    )
                    .join('')}
                </tbody>
            </table>
            ` : '<p>No specific violation patterns identified in this scan.</p>'}
        </div>
    `;
    }

    /**
     * Generates content for developers
     */
    private generateDeveloperContent(report: SiteWideAccessibilityReport): string {
        const priorityMatrix = this.generatePriorityMatrix(report);
        const mostCommonViolations = report.summary?.mostCommonViolations || [];
        const topViolations = mostCommonViolations.slice(0, 8);
        const criticalViolations = report.summary?.criticalViolations || 0;
        const seriousViolations = report.summary?.seriousViolations || 0;
        const pagesWithViolations = report.summary?.pagesWithViolations || 0;
        const compliancePercentage = report.summary?.compliancePercentage || 0;

        return `
        <div class="section">
            <h2>🚨 Critical Issues - Fix Immediately</h2>
            <div class="summary-card">
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="value">${criticalViolations}</span>
                        <div class="label">Critical Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${seriousViolations}</span>
                        <div class="label">Serious Issues</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${pagesWithViolations}</span>
                        <div class="label">Pages Affected</div>
                    </div>
                    <div class="summary-item">
                        <span class="value">${Math.round(compliancePercentage)}%</span>
                        <div class="label">Compliance Score</div>
                    </div>
                </div>
                ${criticalViolations > 0
                ? `
                    <div class="alert-critical">
                        <strong>⚠️ Action Required:</strong> ${criticalViolations} critical issues must be fixed before deployment.
                    </div>
                `
                : ''
            }
            </div>
        </div>

        <div class="section">
            <h2>📋 Priority Matrix - Development Roadmap</h2>
            <div class="priority-matrix">
                <div class="matrix-header">
                    <div class="matrix-cell header">Impact vs Effort</div>
                    <div class="matrix-cell header">Low Effort</div>
                    <div class="matrix-cell header">Medium Effort</div>
                    <div class="matrix-cell header">High Effort</div>
                </div>
                ${priorityMatrix}
            </div>
            <div class="priority-legend">
                <div class="legend-item quick-wins">🟢 Quick Wins - High Impact, Low Effort</div>
                <div class="legend-item major-projects">🟡 Major Projects - High Impact, High Effort</div>
                <div class="legend-item fill-ins">🔵 Fill-ins - Low Impact, Low Effort</div>
                <div class="legend-item thankless">🔴 Avoid - Low Impact, High Effort</div>
            </div>
        </div>

        <div class="section">
            <h2>🔧 Detailed Violation Analysis</h2>
            ${topViolations.length > 0 ? `
            <div class="violations-detailed">
                ${topViolations.map(violation => this.generateDetailedViolationCard(violation, report)).join('')}
            </div>
            ` : '<p>No specific violations identified in this scan.</p>'}
        </div>

        <div class="section">
            <h2>🧪 Testing & Validation Guide</h2>
            <div class="testing-guide">
                <h3>Automated Testing Integration</h3>
                <div class="code-snippet">
// Add to your CI/CD pipeline
npm run test:accessibility
npm run test:wcag-compliance
                </div>
                
                <h3>Manual Testing Checklist</h3>
                <ul class="testing-checklist">
                    <li><strong>Keyboard Navigation:</strong> Tab through all interactive elements</li>
                    <li><strong>Screen Reader:</strong> Test with VoiceOver (Mac) or NVDA (Windows)</li>
                    <li><strong>Color Contrast:</strong> Use axe DevTools browser extension</li>
                    <li><strong>Mobile Accessibility:</strong> Test on actual mobile devices</li>
                    <li><strong>Focus Management:</strong> Ensure visible focus indicators</li>
                </ul>

                <h3>Browser Testing Tools</h3>
                <ul class="tool-list">
                    <li><strong>axe DevTools:</strong> <code>chrome://extensions/</code> - Install axe browser extension</li>
                    <li><strong>Colour Contrast Analyser:</strong> <code>https://www.colour-contrast-analyser.org/</code></li>
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>📚 Developer Resources</h2>
            <div class="resources-grid">
                <div class="resource-card">
                    <h3>WCAG Quick Reference</h3>
                    <ul>
                        <li><a href="https://www.w3.org/WAI/WCAG21/quickref/">WCAG 2.1 Quick Reference</a></li>
                        <li><a href="https://webaim.org/standards/wcag/checklist">WebAIM WCAG Checklist</a></li>
                        <li><a href="https://www.w3.org/WAI/WCAG21/Understanding/">Understanding WCAG 2.1</a></li>
                    </ul>
                </div>
                <div class="resource-card">
                    <h3>Development Tools</h3>
                    <ul>
                        <li><a href="https://github.com/dequelabs/axe-core">axe-core GitHub</a></li>
                        <li><a href="https://pa11y.org/">Pa11y Command Line Tool</a></li>
                        <li><a href="https://github.com/jsx-eslint/eslint-plugin-jsx-a11y">ESLint jsx-a11y</a></li>
                    </ul>
                </div>
                <div class="resource-card">
                    <h3>Design System Integration</h3>
                    <ul>
                        <li>Ensure all components meet AA standards</li>
                        <li>Document accessibility requirements</li>
                        <li>Include keyboard interaction patterns</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🔄 Development Workflow Integration</h2>
            <div class="workflow-section">
                <h3>Prevention Strategy</h3>
                <div class="workflow-grid">
                    <div class="workflow-card">
                        <h4>🎨 Design Phase</h4>
                        <ul>
                            <li>Use accessibility-first design system</li>
                            <li>Ensure 4.5:1 color contrast ratios</li>
                            <li>Design focus states for all interactive elements</li>
                        </ul>
                    </div>
                    <div class="workflow-card">
                        <h4>⌨️ Development Phase</h4>
                        <ul>
                            <li>Use semantic HTML elements</li>
                            <li>Add ESLint accessibility rules</li>
                            <li>Test with keyboard navigation</li>
                        </ul>
                    </div>
                    <div class="workflow-card">
                        <h4>✅ Testing Phase</h4>
                        <ul>
                            <li>Run automated accessibility tests</li>
                            <li>Conduct manual keyboard testing</li>
                            <li>Validate with screen readers</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `;
    }

    /**
     * Generates detailed violation card with actionable information
     */
    private generateDetailedViolationCard(
        violation: any,
        report: SiteWideAccessibilityReport
    ): string {
        const violationData = report.violationsByType[violation.id];
        const impactIcon = this.getImpactIcon(violation.impact);
        const wcagLevel = this.getWcagLevelFromViolationId(violation.id);
        const effort = this.estimateFixEffort(violation.id);
        const priority = this.calculatePriority(violation.impact, effort, violation.affectedPages);

        return `
        <div class="violation-card">
            <div class="violation-header">
                <div class="violation-title">
                    ${impactIcon} <code>${violation.id}</code>
                    <span class="wcag-level wcag-${wcagLevel.toLowerCase()}">${wcagLevel}</span>
                    <span class="priority-${priority.toLowerCase()}">${priority} Priority</span>
                </div>
                <div class="violation-stats">
                    <span class="stat">${violation.affectedPages} pages</span>
                    <span class="stat">${violation.totalOccurrences} occurrences</span>
                    <span class="stat">${effort} effort</span>
                </div>
            </div>
            
            <div class="violation-description">
                <p><strong>Issue:</strong> ${violation.description || this.getViolationDescription(violation.id)}</p>
                <p><strong>User Impact:</strong> ${this.getUserImpactDescription(violation.id)}</p>
            </div>

            <div class="violation-pages">
                <strong>Most Affected Pages:</strong>
                <ul>
                    ${violationData?.pages
                ?.slice(0, 3)
                .map(page => `<li><code>${page}</code></li>`)
                .join('') || '<li>Page details not available</li>'
            }
                </ul>
            </div>

            <div class="remediation-section">
                <h4>🔧 How to Fix:</h4>
                <div class="remediation-steps">
                    ${this.getRemediationSteps(violation.id)}
                </div>
                
                <h4>�� Code Example:</h4>
                <div class="code-snippet">
                    ${this.getCodeExample(violation.id)}
                </div>
                
                <h4>🧪 Testing:</h4>
                <div class="testing-instructions">
                    ${this.getTestingInstructions(violation.id)}
                </div>
            </div>
        </div>
    `;
    }

    /**
     * Generates priority matrix for visual impact vs effort analysis
     */
    private generatePriorityMatrix(report: SiteWideAccessibilityReport): string {
        const violations = report.summary?.mostCommonViolations || [];
        const matrix: PriorityMatrix = {
            'high-low': [],
            'high-medium': [],
            'high-high': [],
            'medium-low': [],
            'medium-medium': [],
            'medium-high': [],
            'low-low': [],
            'low-medium': [],
            'low-high': [],
        };

        violations.forEach(violation => {
            const impact = this.getBusinessImpact(violation.impact || 'moderate', violation.affectedPages || 0);
            const effort = this.estimateFixEffort(violation.id || '');
            const key = `${impact}-${effort}` as keyof PriorityMatrix;
            if (matrix[key]) {
                matrix[key].push(violation as ViolationItem);
            }
        });

        return `
        <div class="matrix-row">
            <div class="matrix-cell impact-label">High Impact</div>
            <div class="matrix-cell quick-wins">${matrix['high-low']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell major-projects">${matrix['high-medium']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell major-projects">${matrix['high-high']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
        </div>
        <div class="matrix-row">
            <div class="matrix-cell impact-label">Medium Impact</div>
            <div class="matrix-cell fill-ins">${matrix['medium-low']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell fill-ins">${matrix['medium-medium']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell thankless">${matrix['medium-high']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
        </div>
        <div class="matrix-row">
            <div class="matrix-cell impact-label">Low Impact</div>
            <div class="matrix-cell fill-ins">${matrix['low-low']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell thankless">${matrix['low-medium']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
            <div class="matrix-cell thankless">${matrix['low-high']?.map(v => `<div class="matrix-item">${v.id || 'Unknown Issue'}</div>`).join('') || ''}</div>
        </div>`;
    }

    /**
     * Gets violations by impact level
     */
    private getViolationsByImpact(report: SiteWideAccessibilityReport, impact: string): any[] {
        const violations = report.summary?.mostCommonViolations || [];
        return violations.filter(v => v.impact === impact);
    }

    /**
     * Gets impact icon for visualization
     */
    private getImpactIcon(impact: string): string {
        switch (impact) {
            case 'critical':
                return '🚨';
            case 'serious':
                return '⚠️';
            case 'moderate':
                return '🟡';
            case 'minor':
                return '🔵';
            default:
                return '⚪';
        }
    }

    /**
     * Estimates fix effort based on violation type
     */
    private estimateFixEffort(violationId: string): 'low' | 'medium' | 'high' {
        const lowEffort = ['image-alt', 'label', 'link-name', 'button-name', 'document-title'];
        const highEffort = [
            'color-contrast',
            'keyboard-navigation',
            'focus-management',
            'aria-complex',
        ];

        if (lowEffort.some(id => violationId.includes(id))) return 'low';
        if (highEffort.some(id => violationId.includes(id))) return 'high';
        return 'medium';
    }

    /**
     * Gets business impact level
     */
    private getBusinessImpact(impact: string, affectedPages: number): 'low' | 'medium' | 'high' {
        if (impact === 'critical' || (impact === 'serious' && affectedPages > 5)) return 'high';
        if (impact === 'serious' || (impact === 'moderate' && affectedPages > 10)) return 'medium';
        return 'low';
    }

    /**
     * Calculates overall priority
     */
    private calculatePriority(
        impact: string,
        effort: string,
        affectedPages: number
    ): 'High' | 'Medium' | 'Low' {
        if (impact === 'critical') return 'High';
        if (impact === 'serious' && effort === 'low') return 'High';
        if (impact === 'serious' && affectedPages > 5) return 'High';
        if (impact === 'moderate' && effort === 'low' && affectedPages > 10) return 'Medium';
        return 'Low';
    }

    /**
     * Gets WCAG level from violation ID
     */
    private getWcagLevelFromViolationId(violationId: string): 'A' | 'AA' | 'AAA' {
        // This would ideally use the actual WCAG data from the violation
        const aaaViolations = ['color-contrast-enhanced', 'focus-visible'];
        const aViolations = ['image-alt', 'form-label', 'keyboard-navigation'];

        if (aaaViolations.some(id => violationId.includes(id))) return 'AAA';
        if (aViolations.some(id => violationId.includes(id))) return 'A';
        return 'AA';
    }

    /**
     * Gets detailed violation description
     */
    private getViolationDescription(violationId: string): string {
        const descriptions: Record<string, string> = {
            'color-contrast': 'Text lacks sufficient color contrast against background',
            'image-alt': 'Images missing alternative text descriptions',
            label: 'Form elements lack proper labels',
            'link-name': 'Links lack descriptive text',
            'button-name': 'Buttons lack accessible names',
            'keyboard-navigation': 'Elements not keyboard accessible',
            'focus-management': 'Focus indicators not visible',
            'aria-label': 'ARIA labels missing or incorrect',
            'heading-order': 'Headings not in logical order',
            'landmark-navigation': 'Page lacks navigation landmarks',
        };

        return descriptions[violationId] || 'Accessibility violation detected';
    }

    /**
     * Gets user impact description
     */
    private getUserImpactDescription(violationId: string): string {
        const impacts: Record<string, string> = {
            'color-contrast': 'Creates barriers for users with visual impairments',
            'image-alt': 'Screen reader users cannot access image content',
            label: 'Form completion impossible without visual cues',
            'link-name': 'Navigation unclear for screen reader users',
            'button-name': 'Actions unclear for assistive technology users',
            'keyboard-navigation': 'Excludes users who cannot use mouse',
            'focus-management': 'Keyboard users cannot track current position',
            'aria-label': 'Screen readers provide incorrect information',
            'heading-order': 'Document structure unclear to screen readers',
            'landmark-navigation': 'Page navigation inefficient for screen readers',
        };

        return impacts[violationId] || 'Creates barriers for users with disabilities';
    }

    /**
     * Gets specific remediation steps
     */
    private getRemediationSteps(violationId: string): string {
        const steps: Record<string, string> = {
            'color-contrast': `
        <ol>
          <li>Check current contrast ratio using browser dev tools</li>
          <li>Ensure minimum 4.5:1 ratio for normal text, 3:1 for large text</li>
          <li>Adjust text or background colors to meet requirements</li>
          <li>Test with automated tools to verify compliance</li>
        </ol>
      `,
            'image-alt': `
        <ol>
          <li>Add descriptive alt text to all informative images</li>
          <li>Use alt="" for decorative images</li>
          <li>Ensure alt text conveys the image's purpose and context</li>
          <li>Test with screen reader to verify effectiveness</li>
        </ol>
      `,
            label: `
        <ol>
          <li>Add proper label elements associated with form controls</li>
          <li>Use for/id attributes to create explicit associations</li>
          <li>Consider placeholder text as supplementary, not primary labels</li>
          <li>Test with screen reader to verify label announcements</li>
        </ol>
      `,
        };

        return (
            steps[violationId] ||
            `
      <ol>
        <li>Review WCAG documentation for specific requirements</li>
        <li>Implement necessary changes following best practices</li>
        <li>Test with assistive technologies</li>
        <li>Validate with automated accessibility tools</li>
      </ol>
    `
        );
    }

    /**
     * Gets code example for fixing violation
     */
    private getCodeExample(violationId: string): string {
        const examples: Record<string, string> = {
            'color-contrast': `
<!-- Bad: Insufficient contrast -->
<p style="color: #999; background: #fff;">Text content</p>

<!-- Good: Sufficient contrast -->
<p style="color: #333; background: #fff;">Text content</p>
      `,
            'image-alt': `
<!-- Bad: Missing alt text -->
<img src="chart.png">

<!-- Good: Descriptive alt text -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2">
      `,
            label: `
<!-- Bad: Missing label -->
<input type="email" placeholder="Enter email">

<!-- Good: Proper label -->
<label for="email">Email address</label>
<input type="email" id="email" placeholder="Enter email">
      `,
        };

        return (
            examples[violationId] ||
            `
<!-- Review violation-specific documentation -->
<!-- Implement following WCAG guidelines -->
<!-- Test with assistive technologies -->
    `
        );
    }

    /**
     * Gets testing instructions
     */
    private getTestingInstructions(violationId: string): string {
        const instructions: Record<string, string> = {
            'color-contrast': `
        <ul>
          <li>Use axe DevTools browser extension</li>
          <li>Install axe DevTools browser extension</li>
          <li>Test with Colour Contrast Analyser tool</li>
          <li>Verify with users who have visual impairments</li>
        </ul>
      `,
            'image-alt': `
        <ul>
          <li>Use screen reader (VoiceOver on Mac, NVDA on Windows)</li>
          <li>Test with axe DevTools to check for missing alt text</li>
          <li>Verify images are properly described in context</li>
          <li>Check that decorative images are marked appropriately</li>
        </ul>
      `,
            label: `
        <ul>
          <li>Test with screen reader to verify label announcements</li>
          <li>Use keyboard navigation to ensure proper focus</li>
          <li>Check form validation messages are accessible</li>
          <li>Verify labels are programmatically associated</li>
        </ul>
      `,
        };

        return (
            instructions[violationId] ||
            `
      <ul>
        <li>Test with keyboard navigation only</li>
        <li>Use screen reader to verify accessibility</li>
        <li>Run automated accessibility tests</li>
        <li>Validate with real users when possible</li>
      </ul>
    `
        );
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

    /**
     * Generates performance metrics section
     */
    private generatePerformanceMetricsSection(scanMetadata: ScanMetadata): string {
        if (!scanMetadata.performanceMetrics) {
            return '';
        }

        const metrics = scanMetadata.performanceMetrics;
        const avgTimePerPage = metrics.averageTimePerPage ? this.formatDuration(metrics.averageTimePerPage) : 'N/A';
        const totalScanTime = metrics.totalScanTime ? this.formatDuration(metrics.totalScanTime) : 'N/A';
        const successRate = metrics.successRate ? `${Math.round(metrics.successRate)}%` : 'N/A';

        return `
        <div class="section">
            <h2>Performance Metrics</h2>
            <div class="performance-metrics">
                <div class="performance-grid">
                    <div class="performance-item">
                        <span class="value">${totalScanTime}</span>
                        <div class="label">Total Scan Time</div>
                    </div>
                    <div class="performance-item">
                        <span class="value">${avgTimePerPage}</span>
                        <div class="label">Average Time Per Page</div>
                    </div>
                    <div class="performance-item">
                        <span class="value">${successRate}</span>
                        <div class="label">Success Rate</div>
                    </div>
                    <div class="performance-item">
                        <span class="value">${metrics.pagesAnalyzed || 'N/A'}</span>
                        <div class="label">Pages Analyzed</div>
                    </div>
                    <div class="performance-item">
                        <span class="value">${metrics.pagesWithViolations || 'N/A'}</span>
                        <div class="label">Pages With Violations</div>
                    </div>
                </div>
            </div>
        </div>`;
    }

    /**
     * Generates technical details section
     */
    private generateTechnicalDetailsSection(scanMetadata: ScanMetadata): string {
        const toolsUsed = scanMetadata.toolsUsed?.join(', ') || 'axe-core, Pa11y';
        const scanType = scanMetadata.scanType || 'full-site';
        const scanTypeDisplay = {
            'full-site': 'Full Site Scan',
            'single-page': 'Single Page Scan',
            'quick': 'Quick Scan'
        }[scanType] || 'Full Site Scan';

        return `
        <div class="section">
            <h2>Technical Details</h2>
            <div class="technical-details">
                <div class="technical-grid">
                    <div class="technical-item">
                        <strong>Scan Type</strong>
                        ${scanTypeDisplay}
                    </div>
                    <div class="technical-item">
                        <strong>Tools Used</strong>
                        ${toolsUsed}
                    </div>
                    <div class="technical-item">
                        <strong>Browser</strong>
                        ${scanMetadata.browser || scanMetadata.userAgent ? 'Chrome (Playwright)' : 'N/A'}
                    </div>
                    <div class="technical-item">
                        <strong>Crawl Depth</strong>
                        ${scanMetadata.crawlDepth !== undefined ? scanMetadata.crawlDepth : 'N/A'}
                    </div>
                    <div class="technical-item">
                        <strong>Max Concurrency</strong>
                        ${scanMetadata.scanConfiguration?.maxConcurrency || 'N/A'}
                    </div>
                    <div class="technical-item">
                        <strong>Max Pages</strong>
                        ${scanMetadata.scanConfiguration?.maxPages || 'N/A'}
                    </div>
                    ${scanMetadata.excludedPatterns && scanMetadata.excludedPatterns.length > 0
                ? `<div class="technical-item">
                            <strong>Excluded Patterns</strong>
                            ${scanMetadata.excludedPatterns.join(', ')}
                           </div>`
                : ''
            }
                </div>
            </div>
        </div>

        ${scanMetadata.scanStartedAt || scanMetadata.scanCompletedAt ? this.generateScanTimelineSection(scanMetadata) : ''}`;
    }

    /**
     * Generates scan timeline section
     */
    private generateScanTimelineSection(scanMetadata: ScanMetadata): string {
        const startDate = scanMetadata.scanStartedAt
            ? new Date(scanMetadata.scanStartedAt).toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            })
            : 'N/A';

        const endDate = scanMetadata.scanCompletedAt
            ? new Date(scanMetadata.scanCompletedAt).toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            })
            : 'N/A';

        const duration = scanMetadata.performanceMetrics?.totalScanTime
            ? this.formatDuration(scanMetadata.performanceMetrics.totalScanTime)
            : 'N/A';

        return `
        <div class="section">
            <h2>Scan Timeline</h2>
            <div class="scan-timeline">
                <div class="timeline-item">
                    <span class="timeline-label">Scan Started</span>
                    <span class="timeline-value">${startDate}</span>
                </div>
                <div class="timeline-item">
                    <span class="timeline-label">Scan Completed</span>
                    <span class="timeline-value">${endDate}</span>
                </div>
                <div class="timeline-item">
                    <span class="timeline-label">Total Duration</span>
                    <span class="timeline-value">${duration}</span>
                </div>
                ${scanMetadata.scanId ? `
                <div class="timeline-item">
                    <span class="timeline-label">Scan ID</span>
                    <span class="timeline-value">${scanMetadata.scanId}</span>
                </div>` : ''}
            </div>
        </div>`;
    }
}
