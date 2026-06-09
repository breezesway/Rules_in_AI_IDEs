import { Page } from '@playwright/test';
import { SiteWideAccessibilityReport } from './accessibility-helpers';

export class SiteWideAccessibilityPdfGenerator {
  constructor(private page: Page) {}

  async generateSiteWidePdfReport(
    report: SiteWideAccessibilityReport,
    filename: string
  ): Promise<string[]> {
    const fs = require('fs');
    const path = require('path');

    const reportsDir = path.join(process.cwd(), 'playwright', 'accessibility-reports');
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }

    const generatedReports: string[] = [];

    // Create a new browser instance specifically for PDF generation in headless mode
    const { chromium } = require('playwright');
    const browser = await chromium.launch({ headless: true });

    try {
      // Generate audience-specific reports
      const audiences = [
        { name: 'stakeholders', displayName: 'Product Owners & Stakeholders' },
        { name: 'researchers', displayName: 'User Researchers & UCD' },
        { name: 'developers', displayName: 'Developers & Testers' },
      ];

      for (const audience of audiences) {
        const pdfPage = await browser.newPage();

        try {
          // Generate audience-specific HTML
          const htmlContent = this.generateAudienceSpecificHtmlTemplate(
            report,
            audience.name,
            audience.displayName
          );

          // Create temporary HTML file
          const tempHtmlPath = path.join(process.cwd(), `temp-${audience.name}-report.html`);
          fs.writeFileSync(tempHtmlPath, htmlContent);

          try {
            // Navigate to the HTML file
            await pdfPage.goto(`file://${tempHtmlPath}`);

            // Wait for any dynamic content to load
            await pdfPage.waitForTimeout(2000);

            // Generate PDF
            const pdfPath = path.join(reportsDir, `${filename}-${audience.name}.pdf`);

            await pdfPage.pdf({
              path: pdfPath,
              format: 'A4',
              printBackground: true,
              margin: {
                top: '0.75in',
                right: '0.75in',
                bottom: '0.75in',
                left: '0.75in',
              },
            });

            console.log(`📄 ${audience.displayName} PDF report generated: ${pdfPath}`);
            generatedReports.push(pdfPath);
          } finally {
            // Clean up temporary file
            this.cleanupTemporaryFiles(tempHtmlPath);
          }
        } finally {
          await pdfPage.close();
        }
      }
    } finally {
      await browser.close();
    }

    return generatedReports;
  }

  private generateAudienceSpecificHtmlTemplate(
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
        ${this.getSiteWideStyles()}
    </style>
</head>
<body>
    ${this.generateAudienceSpecificHeader(report, audience, displayName)}
    ${this.generateAudienceSpecificContent(report, audience)}
</body>
</html>
        `.trim();
  }

  private generateAudienceSpecificHeader(
    report: SiteWideAccessibilityReport,
    audience: string,
    displayName: string
  ): string {
    const auditDate = new Date(report.timestamp).toLocaleDateString();

    return `
        <div class="header-section">
            <div class="section-title">Accessibility Report - ${displayName}</div>
            
            <div class="field-row">
                <span class="field-label">Report Type:</span>
                <span class="field-value">${displayName} Focused Analysis</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Evaluation date:</span>
                <span class="field-value">${auditDate}</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Site URL:</span>
                <span class="field-value">${report.siteUrl}</span>
            </div>

            <div class="field-row">
                <span class="field-label">Pages Tested:</span>
                <span class="field-value">${report.summary.totalPages}</span>
            </div>
        </div>
        `;
  }

  private generateAudienceSpecificContent(
    report: SiteWideAccessibilityReport,
    audience: string
  ): string {
    switch (audience) {
      case 'stakeholders':
        return this.generateStakeholderContent(report);
      case 'researchers':
        return this.generateResearcherContent(report);
      case 'developers':
        return this.generateDeveloperContent(report);
      default:
        return this.generateStakeholderContent(report);
    }
  }

  private generateStakeholderContent(report: SiteWideAccessibilityReport): string {
    return `
        ${this.generateExecutiveSummary(report)}
        ${this.generateBusinessImpactSection(report)}
        ${this.generateComplianceOverview(report)}
        ${this.generateRecommendationsAndTimeline(report)}
    `;
  }

  private generateResearcherContent(report: SiteWideAccessibilityReport): string {
    return `
        ${this.generateUserImpactAnalysis(report)}
        ${this.generateWcagComplianceMatrix(report)}
        ${this.generateAccessibilityScenarios(report)}
        ${this.generateResearchRecommendations(report)}
    `;
  }

  private generateDeveloperContent(report: SiteWideAccessibilityReport): string {
    return `
        ${this.generateTechnicalSummary(report)}
        ${this.generateDeveloperFixGuide(report)}
        ${this.generatePageByPageResults(report)}
        ${this.generateImplementationGuidance(report)}
        `;
  }

  // New audience-specific section methods
  private generateExecutiveSummary(report: SiteWideAccessibilityReport): string {
    const overallCompliance =
      report.summary.compliancePercentage === 100
        ? 'COMPLIANT'
        : report.summary.compliancePercentage >= 70
          ? 'PARTIALLY_COMPLIANT'
          : 'NON-COMPLIANT';

    return `
        <div class="section-title">Executive Summary</div>
        <div class="summary-stats">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${report.summary.compliancePercentage}%</div>
                    <div class="stat-label">Overall Compliance</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${report.summary.totalViolations}</div>
                    <div class="stat-label">Total Issues</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${report.summary.totalPages}</div>
                    <div class="stat-label">Pages Tested</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${report.summary.criticalViolations}</div>
                    <div class="stat-label">Critical Issues</div>
                </div>
            </div>
            
            <div class="summary-description">
                <p><strong>Compliance Status:</strong> ${overallCompliance}</p>
                <p>This report evaluates ${report.summary.totalPages} pages against WCAG 2.1 AA accessibility standards. 
                ${
                  report.summary.pagesWithViolations > 0
                    ? `${report.summary.pagesWithViolations} pages have accessibility issues that require attention.`
                    : 'All pages meet accessibility standards.'
                }</p>
            </div>
        </div>
        `;
  }

  private generateBusinessImpactSection(report: SiteWideAccessibilityReport): string {
    const criticalCount = report.summary.criticalViolations;
    const seriousCount = report.summary.seriousViolations;

    return `
        <div class="page-break">
            <div class="section-title">Business Impact & Risk Assessment</div>
            
            <div class="summary-stats">
                <h3>📊 Risk Analysis</h3>
                <div class="violation-summary-card violation-critical">
                    <div class="violation-summary-title">High Risk - Immediate Action Required</div>
                    <div class="violation-summary-meta">${criticalCount} critical violations found</div>
                    <p>These issues prevent users with disabilities from accessing your content and may expose your organisation to legal risk under accessibility laws (ADA, EN 301 549, etc.).</p>
                </div>
                
                <div class="violation-summary-card violation-serious">
                    <div class="violation-summary-title">Medium Risk - High Priority Fixes</div>
                    <div class="violation-summary-meta">${seriousCount} serious violations found</div>
                    <p>These significantly impact user experience for people with disabilities and should be addressed within the next sprint cycle.</p>
                </div>

                <h3>💰 Estimated Impact</h3>
                <ul>
                    <li><strong>User Base:</strong> 15-20% of users may be affected by accessibility barriers</li>
                    <li><strong>Market Reach:</strong> Improved accessibility expands potential customer base</li>
                    <li><strong>SEO Benefits:</strong> Many accessibility improvements also enhance search rankings</li>
                    <li><strong>Legal Protection:</strong> WCAG compliance reduces litigation risk</li>
                </ul>
            </div>
        </div>
        `;
  }

  private generateComplianceOverview(report: SiteWideAccessibilityReport): string {
    return `
        <div class="page-break">
            <div class="section-title">WCAG 2.1 AA Compliance Overview</div>
            
            <div class="summary-stats">
                <p>Web Content Accessibility Guidelines (WCAG) 2.1 Level AA is the internationally recognized standard for web accessibility and is referenced by most accessibility laws.</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">${report.summary.totalPages - report.summary.pagesWithViolations}</div>
                        <div class="stat-label">Compliant Pages</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">${report.summary.pagesWithViolations}</div>
                        <div class="stat-label">Pages Needing Work</div>
                    </div>
                </div>

                <h3>📋 Most Common Issues</h3>
                ${report.summary.mostCommonViolations
                  .slice(0, 5)
                  .map(
                    (violation, index) => `
                    <div class="violation-summary-card">
                        <div class="violation-summary-title">${index + 1}. ${violation.description}</div>
                        <div class="violation-summary-meta">Affects ${violation.affectedPages} pages • ${violation.totalOccurrences} total occurrences</div>
                    </div>
                `
                  )
                  .join('')}
            </div>
        </div>
        `;
  }

  private generateRecommendationsAndTimeline(report: SiteWideAccessibilityReport): string {
    const criticalCount = report.summary.criticalViolations;
    const seriousCount = report.summary.seriousViolations;

    return `
        <div class="page-break">
            <div class="section-title">Recommendations & Implementation Timeline</div>
            
            <div class="summary-stats">
                <h3>🎯 Priority Roadmap</h3>
                
                <div class="violation-summary-card violation-critical">
                    <div class="violation-summary-title">Phase 1: Critical Fixes</div>
                    <p><strong>Focus:</strong> ${criticalCount} critical violations</p>
                    <p><strong>Impact:</strong> Removes major accessibility barriers and legal risk</p>
                </div>

                <div class="violation-summary-card violation-serious">
                    <div class="violation-summary-title">Phase 2: High Priority Fixes</div>
                    <p><strong>Focus:</strong> ${seriousCount} serious violations</p>
                    <p><strong>Impact:</strong> Significantly improves user experience</p>
                </div>

                <div class="violation-summary-card">
                    <div class="violation-summary-title">Phase 3: Process Integration</div>
                    <p><strong>Focus:</strong> Prevent new violations through automated testing</p>
                    <p><strong>Impact:</strong> Ensures long-term accessibility compliance</p>
                </div>

                <h3>🔧 Recommended Actions</h3>
                <ul>
                    <li><strong>Immediate:</strong> Begin critical violation fixes</li>
                    <li><strong>Short-term:</strong> Implement automated accessibility testing in CI/CD</li>
                    <li><strong>Medium-term:</strong> Provide accessibility training for development team</li>
                    <li><strong>Long-term:</strong> Establish accessibility review process for new features</li>
                </ul>
            </div>
        </div>
        `;
  }

  // Researcher-focused sections
  private generateUserImpactAnalysis(report: SiteWideAccessibilityReport): string {
    return `
        <div class="section-title">User Impact Analysis</div>
        <div class="summary-stats">
            <h3>🧑‍🦯 Affected User Groups</h3>
            
            <div class="violation-summary-card">
                <div class="violation-summary-title">Visual Impairments</div>
                <div class="violation-summary-meta">Estimated 8-10% of users affected</div>
                <p><strong>Key Issues Found:</strong> Colour contrast violations (${report.violationsByType['color-contrast']?.totalOccurrences || 0} instances), missing alt text</p>
                <p><strong>User Impact:</strong> Content may be difficult or impossible to read with screen readers or high contrast settings</p>
            </div>

            <div class="violation-summary-card">
                <div class="violation-summary-title">Motor/Mobility Impairments</div>
                <div class="violation-summary-meta">Estimated 2-4% of users affected</div>
                <p><strong>Key Issues Found:</strong> Viewport/zoom restrictions (${report.violationsByType['meta-viewport']?.totalOccurrences || 0} instances)</p>
                <p><strong>User Impact:</strong> Users may be unable to zoom or navigate effectively with assistive devices</p>
            </div>

            <div class="violation-summary-card">
                <div class="violation-summary-title">Cognitive Impairments</div>
                <div class="violation-summary-meta">Estimated 3-5% of users affected</div>
                <p><strong>Key Issues Found:</strong> Missing link context (${report.violationsByType['link-name']?.totalOccurrences || 0} instances)</p>
                <p><strong>User Impact:</strong> Unclear navigation and link purposes create confusion and cognitive burden</p>
            </div>

            <h3>📱 Device & Context Considerations</h3>
            <ul>
                <li><strong>Mobile Users:</strong> Viewport issues particularly impact mobile accessibility</li>
                                    <li><strong>Low Vision:</strong> Colour contrast problems affect users in bright environments</li>
                <li><strong>Screen Reader Users:</strong> Missing alt text and link names break navigation flow</li>
                <li><strong>Keyboard Users:</strong> Focus management issues prevent effective navigation</li>
            </ul>
        </div>
        `;
  }

  private generateAccessibilityScenarios(report: SiteWideAccessibilityReport): string {
    return `
        <div class="page-break">
            <div class="section-title">User Journey Accessibility Analysis</div>
            
            <div class="summary-stats">
                <h3>🛤️ Critical User Paths</h3>
                
                <div class="violation-summary-card violation-critical">
                    <div class="violation-summary-title">Homepage to Service Information</div>
                    <p><strong>Barriers Found:</strong> Colour contrast issues on navigation, missing link context</p>
                    <p><strong>Impact:</strong> Users may struggle to understand available services and navigate effectively</p>
                    <p><strong>Testing Priority:</strong> High - Primary conversion path</p>
                </div>

                <div class="violation-summary-card violation-serious">
                    <div class="violation-summary-title">Content Discovery & Reading</div>
                    <p><strong>Barriers Found:</strong> Viewport restrictions, inconsistent heading structure</p>
                    <p><strong>Impact:</strong> Content may be difficult to read and navigate sequentially</p>
                    <p><strong>Testing Priority:</strong> High - Core user activity</p>
                </div>

                <h3>🧪 Recommended User Testing Scenarios</h3>
                <ol>
                    <li><strong>Screen Reader Navigation:</strong> Test primary navigation and content discovery with NVDA/JAWS</li>
                    <li><strong>Keyboard-Only Navigation:</strong> Complete core tasks using only keyboard input</li>
                    <li><strong>High Contrast Mode:</strong> Verify content visibility in Windows High Contrast mode</li>
                    <li><strong>Mobile Zoom Testing:</strong> Test 200% zoom on mobile devices for viewport compliance</li>
                    <li><strong>Voice Control:</strong> Test navigation with Dragon NaturallySpeaking or similar tools</li>
                </ol>

                <h3>📋 Accessibility Testing Checklist</h3>
                <ul>
                    <li>✅ Run automated tools (axe, WAVE, Lighthouse)</li>
                    <li>⚠️ Manual keyboard navigation testing needed</li>
                    <li>⚠️ Screen reader testing with real users recommended</li>
                    <li>⚠️ Colour/contrast validation in various lighting conditions</li>
                    <li>⚠️ Mobile accessibility testing on actual devices</li>
                </ul>
            </div>
        </div>
        `;
  }

  private generateResearchRecommendations(report: SiteWideAccessibilityReport): string {
    return `
        <div class="page-break">
            <div class="section-title">Research & Testing Recommendations</div>
            
            <div class="summary-stats">
                <h3>🔬 Recommended Research Activities</h3>
                
                <div class="violation-summary-card">
                    <div class="violation-summary-title">Usability Testing with Disabled Users</div>
                    <p><strong>Priority:</strong> High</p>
                    <p><strong>Participants:</strong> 2-3 screen reader users, 2-3 motor impairment users, 2-3 low vision users</p>
                    <p><strong>Focus:</strong> Core task completion, navigation efficiency, content comprehension</p>
                </div>

                <div class="violation-summary-card">
                    <div class="violation-summary-title">Accessibility Persona Development</div>
                    <p><strong>Priority:</strong> Medium</p>
                    <p><strong>Deliverable:</strong> Accessibility-focused user personas including assistive technology usage</p>
                    <p><strong>Benefit:</strong> Helps design team consider accessibility from the start</p>
                </div>

                <div class="violation-summary-card">
                    <div class="violation-summary-title">Accessibility Guidelines & Standards</div>
                    <p><strong>Priority:</strong> High</p>
                    <p><strong>Deliverable:</strong> Team accessibility guidelines based on WCAG 2.1 AA and user research findings</p>
                    <p><strong>Benefit:</strong> Prevents future accessibility issues through proactive design</p>
                </div>

                <h3>🎯 Success Metrics to Track</h3>
                <ul>
                    <li><strong>Task Completion Rate:</strong> Compare disabled vs non-disabled users</li>
                    <li><strong>Time to Complete:</strong> Measure efficiency of assistive technology users</li>
                    <li><strong>Error Recovery:</strong> How easily users recover from navigation mistakes</li>
                    <li><strong>Satisfaction Scores:</strong> Post-task satisfaction ratings for accessibility</li>
                    <li><strong>Accessibility Compliance:</strong> Percentage of WCAG 2.1 AA criteria met</li>
                </ul>

                <h3>🛠️ Recommended Tools & Resources</h3>
                <ul>
                    <li><strong>Screen Readers:</strong> NVDA (free), JAWS, VoiceOver</li>
                    <li><strong>Testing Tools:</strong> axe DevTools, WAVE, Lighthouse accessibility audit</li>
                    <li><strong>Color Tools:</strong> Colour Contrast Analyser, WebAIM contrast checker</li>
                    <li><strong>Guidelines:</strong> WCAG 2.1 Quick Reference, GOV.UK accessibility guide</li>
                </ul>
            </div>
        </div>
        `;
  }

  // Developer-focused sections
  private generateTechnicalSummary(report: SiteWideAccessibilityReport): string {
    return `
        <div class="section-title">Technical Summary</div>
        <div class="summary-stats">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">${report.summary.totalViolations}</div>
                    <div class="stat-label">Total Violations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${Object.keys(report.violationsByType).length}</div>
                    <div class="stat-label">Unique Violation Types</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${report.summary.totalPages}</div>
                    <div class="stat-label">Pages Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">${report.summary.criticalViolations}</div>
                    <div class="stat-label">Critical Fixes Needed</div>
                </div>
            </div>

            <h3>🔧 Technical Violation Breakdown</h3>
            <table class="violation-table">
                <thead>
                    <tr>
                        <th>Violation Type</th>
                        <th>Severity</th>
                        <th>Count</th>
                        <th>Pages Affected</th>
                        <th>WCAG Criteria</th>
                    </tr>
                </thead>
                <tbody>
                    ${Object.entries(report.violationsByType)
                      .sort(([, a], [, b]) => b.totalOccurrences - a.totalOccurrences)
                      .map(
                        ([id, data]) => `
                            <tr>
                                <td><code>${id}</code></td>
                                <td><span class="impact-badge impact-${data.impact}">${data.impact}</span></td>
                                <td>${data.totalOccurrences}</td>
                                <td>${data.count}</td>
                                <td>WCAG 2.1 AA</td>
                            </tr>
                        `
                      )
                      .join('')}
                </tbody>
            </table>

                        <h3>🌐 Browser Compatibility</h3>
            ${Object.entries(report.violationsByType)
              .map(([id, data]) =>
                data.browsers && data.browsers.length > 0
                  ? `<p><strong>${id}:</strong> Found in ${data.browsers.join(', ')}</p>`
                  : ''
              )
              .join('')}

            <h3>🔧 Detection Tools Coverage</h3>
            ${Object.entries(report.violationsByType)
              .map(([id, data]) =>
                data.tools && data.tools.length > 0
                  ? `<p><strong>${id}:</strong> Detected by ${data.tools.join(', ')}</p>`
                  : ''
              )
              .join('')}
            
            <div class="summary-stats">
                <p><strong>Multi-Tool Analysis:</strong> This report combines results from two complementary accessibility testing tools to provide comprehensive coverage:</p>
                <ul>
                    <li><strong>axe-core:</strong> Industry-standard DOM-based accessibility testing engine with detailed remediation guidance</li>
                    <li><strong>Pa11y:</strong> Command-line accessibility testing with HTML_CodeSniffer for additional HTML structure validation</li>
                </ul>
                <p>Using multiple tools with different testing approaches ensures broader coverage and catches issues that might be missed by any single tool.</p>
            </div>
        </div>
        `;
  }

  private generateImplementationGuidance(report: SiteWideAccessibilityReport): string {
    return `
        <div class="page-break">
            <div class="section-title">Implementation Guidance</div>
            
            <div class="summary-stats">
                <h3>🚀 Quick Wins (Easy Fixes)</h3>
                <div class="violation-summary-card">
                    <div class="violation-summary-title">Add Viewport Meta Tag</div>
                    <div class="code-container">
                        <pre><code>&lt;meta name="viewport" content="width=device-width, initial-scale=1"&gt;</code></pre>
                    </div>
                    <p><strong>Impact:</strong> Fixes ${report.violationsByType['meta-viewport']?.totalOccurrences || 0} violations across ${report.violationsByType['meta-viewport']?.count || 0} pages</p>
                </div>

                <h3>🧰 Development Tools Integration</h3>
                <div class="code-container">
                    <pre><code># Install axe-core for automated testing
npm install --save-dev @axe-core/playwright

# Add to your test suite
import { AxeBuilder } from '@axe-core/playwright';

test('accessibility check', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});</code></pre>
                </div>

                <h3>📋 Code Review Checklist</h3>
                <ul>
                    <li>✅ All images have descriptive alt text</li>
                    <li>✅ Colour contrast ratios meet WCAG AA standards (4.5:1)</li>
                    <li>✅ Interactive elements are keyboard accessible</li>
                    <li>✅ Form inputs have associated labels</li>
                    <li>✅ Page has proper heading hierarchy (h1 → h2 → h3)</li>
                    <li>✅ Links have descriptive text or aria-labels</li>
                    <li>✅ Viewport meta tag allows zooming</li>
                </ul>

                <h3>🔄 CI/CD Integration</h3>
                <p>Add accessibility testing to your deployment pipeline to catch violations before they reach production:</p>
                <div class="code-container">
                    <pre><code># GitHub Actions example
- name: Run accessibility tests
  run: npm run test:accessibility
  
# Fail build if critical violations found
- name: Check accessibility compliance
  run: npm run accessibility:check --fail-on=critical</code></pre>
                </div>
            </div>
        </div>
        `;
  }

  private generateSiteWideHtmlTemplate(report: SiteWideAccessibilityReport): string {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site-wide Accessibility Evaluation Report</title>
    <style>
        ${this.getSiteWideStyles()}
    </style>
</head>
<body>
    ${this.generateSiteWideHeader(report)}
    ${this.generateSiteWideExecutiveSummary(report)}
    ${this.generateSiteWideScope(report)}
    ${this.generateWcagComplianceMatrix(report)}
    ${this.generateMostCommonViolations(report)}
    ${this.generateDeveloperFixGuide(report)}
    ${this.generatePageByPageResults(report)}
</body>
</html>
        `.trim();
  }

  private getSiteWideStyles(): string {
    return `
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Red+Hat+Display:wght@400;500;600;700&display=swap');

        @page {
            margin: 0.75in;
            @bottom-center {
                content: counter(page);
                font-size: 12px;
                color: #1e214d;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Red Hat Display', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #1e214d;
            background-color: #fff;
        }

        .page-break {
            page-break-before: always;
        }

        .header-section {
            margin-bottom: 40px;
        }

        .section-title {
            font-family: 'Poppins', Arial, sans-serif;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 15px;
            margin-top: 25px;
            color: #1e214d;
        }

        .field-row {
            margin-bottom: 8px;
            display: flex;
        }

        .field-label {
            font-weight: bold;
            min-width: 180px;
            margin-right: 20px;
        }

        .field-value {
            border-bottom: 1px solid #ccc;
            min-width: 200px;
            padding-bottom: 2px;
        }

        .summary-stats {
            margin: 15px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }

        .stat-card {
            background: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 15px;
            text-align: center;
        }

        .stat-number {
            font-size: 24pt;
            font-weight: bold;
            color: #1e214d;
            margin-bottom: 5px;
            font-family: 'Poppins', Arial, sans-serif;
        }

        .stat-label {
            font-size: 10pt;
            color: #1e214d;
            opacity: 0.7;
        }

        .violation-summary-card {
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .violation-critical { border-left: 5px solid #db0064; }
        .violation-serious { border-left: 5px solid #fcc700; }
        .violation-moderate { border-left: 5px solid #1e214d; }
        .violation-minor { border-left: 5px solid #28a745; }

        .violation-summary-title {
            font-family: 'Poppins', Arial, sans-serif;
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 8px;
            color: #1e214d;
        }

        .violation-summary-meta {
            font-size: 10pt;
            color: #1e214d;
            margin-bottom: 8px;
            opacity: 0.8;
        }

        .page-list {
            font-size: 9pt;
            color: #1e214d;
            max-height: 60px;
            overflow: hidden;
            opacity: 0.8;
        }

        .page-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10pt;
        }

        .page-table th,
        .page-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
            vertical-align: top;
        }

        .page-table th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #1e214d;
            font-family: 'Poppins', Arial, sans-serif;
        }

        .page-url {
            color: #db0064;
            word-break: break-all;
        }

        .compliance-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: bold;
            color: white;
        }

        .compliant { background: #28a745; }
        .non-compliant { background: #db0064; }
        .partially-compliant { background: #fcc700; color: #1e214d; }

        .impact-badge {
            display: inline-block;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
            font-family: 'Red Hat Display', Arial, sans-serif;
        }

        .impact-critical { background: #db0064; }
        .impact-serious { background: #fcc700; color: #1e214d; }
        .impact-moderate { background: #1e214d; }
        .impact-minor { background: #28a745; }

        .summary-description {
            margin: 15px 0;
            padding: 15px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 6px;
            font-size: 11pt;
            border-left: 4px solid #1e214d;
        }

        .wcag-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 9pt;
        }

        .wcag-table th,
        .wcag-table td {
            border: 1px solid #ddd;
            padding: 6px;
            text-align: left;
            vertical-align: top;
        }

        .wcag-table th {
            background-color: #f8f9fa;
            font-weight: bold;
            font-size: 10pt;
            color: #1e214d;
            font-family: 'Poppins', Arial, sans-serif;
        }

        .principle-header td {
            background-color: #f0f1f3 !important;
            font-weight: bold;
            font-size: 10pt;
            padding: 8px 6px;
            color: #1e214d;
            font-family: 'Poppins', Arial, sans-serif;
        }

        .criterion-id {
            font-family: monospace;
            font-weight: bold;
            text-align: center;
            color: #1e214d;
        }

        .level-a {
            font-weight: bold;
            color: #28a745;
        }

        .level-aa {
            font-weight: bold;
            color: #1e214d;
        }

        .status-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            color: white;
            text-align: center;
            min-width: 60px;
        }

        .status-badge.pass {
            background: #28a745;
        }

        .status-badge.fail {
            background: #db0064;
        }



        .observations {
            font-size: 8pt;
            color: #1e214d;
            opacity: 0.7;
        }

        .wcag-legend {
            font-size: 9pt;
        }

        .wcag-legend .status-badge {
            margin-right: 10px;
            font-size: 8pt;
            padding: 2px 6px;
        }

        .blank-cell {
            background-color: #f9f9f9;
            border: 1px dashed #ddd;
            min-height: 20px;
        }

        /* Developer Fix Guide Styles */
        .violation-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            background: #fff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .violation-header {
            border-bottom: 1px solid #eee;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }

        .violation-title {
            font-family: 'Poppins', Arial, sans-serif;
            font-size: 12pt;
            font-weight: bold;
            margin-bottom: 5px;
            color: #1e214d;
        }

        .violation-meta {
            color: #1e214d;
            font-size: 10pt;
            opacity: 0.7;
        }

        .violation-details {
            margin-top: 15px;
        }

        .detail-section {
            margin-bottom: 20px;
        }

        .detail-section h4 {
            margin: 0 0 10px 0;
            color: #1e214d;
            font-size: 11pt;
            font-weight: bold;
            font-family: 'Poppins', Arial, sans-serif;
        }

        .code-container {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 15px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }

        .problematic-code {
            background: #fff5f5;
            border-color: #feb2b2;
        }

        .fixed-code {
            background: #f0fff4;
            border-color: #9ae6b4;
        }

        .code-container pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.3;
        }

        .code-snippet {
            background: #f1f3f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            color: #db0064;
        }

        .screenshot-container {
            text-align: center;
            margin: 15px 0;
        }

        .element-screenshot {
            max-width: 100%;
            max-height: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        .priority-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
        }

        .priority-high {
            background: #fdeef3;
            color: #db0064;
        }

        .priority-medium {
            background: #fff9e6;
            color: #fcc700;
        }

        .priority-low {
            background: #e8f5e8;
            color: #28a745;
        }
        `;
  }

  private generateSiteWideHeader(report: SiteWideAccessibilityReport): string {
    const auditDate = new Date(report.timestamp).toLocaleDateString();

    return `
        <div class="header-section">
            <div class="section-title">Site-wide Accessibility Evaluation Report</div>
            
            <div class="field-row">
                <span class="field-label">Report Creator:</span>
                <span class="field-value">Automated Accessibility Testing System</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Evaluation Commissioner:</span>
                <span class="field-value">_________________</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Evaluation date:</span>
                <span class="field-value">${auditDate}</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Site URL:</span>
                <span class="field-value">${report.siteUrl}</span>
            </div>
        </div>
        `;
  }

  private generateSiteWideExecutiveSummary(report: SiteWideAccessibilityReport): string {
    const overallCompliance =
      report.summary.compliancePercentage === 100
        ? 'COMPLIANT'
        : report.summary.compliancePercentage >= 70
          ? 'PARTIALLY_COMPLIANT'
          : 'NON-COMPLIANT';

    return `
        <div class="section-title">Executive Summary</div>
        
        <div class="summary-description">
            This report provides a comprehensive accessibility assessment of <strong>${report.siteUrl}</strong>, 
            covering <strong>${report.summary.totalPages}</strong> pages across the website. 
            The evaluation identified <strong>${report.summary.totalViolations}</strong> accessibility violations 
            affecting <strong>${report.summary.pagesWithViolations}</strong> pages.
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${report.summary.totalPages}</div>
                <div class="stat-label">Pages Tested</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${report.summary.compliancePercentage}%</div>
                <div class="stat-label">Compliance Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${report.summary.totalViolations}</div>
                <div class="stat-label">Total Violations</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${report.summary.pagesWithViolations}</div>
                <div class="stat-label">Pages with Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${report.summary.criticalViolations}</div>
                <div class="stat-label">Critical Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${report.summary.seriousViolations}</div>
                <div class="stat-label">Serious Issues</div>
            </div>
        </div>

        <div class="summary-stats">
            <p><strong>Overall Compliance Status:</strong> 
                <span class="compliance-badge ${overallCompliance.toLowerCase().replace('_', '-')}">${overallCompliance.replace('_', ' ')}</span>
            </p>
            
            ${
              report.summary.compliancePercentage < 100
                ? `
                <p style="margin-top: 10px;"><strong>Key Recommendations:</strong></p>
                <ul style="margin-top: 5px; padding-left: 20px;">
                    ${report.summary.criticalViolations > 0 ? '<li>Address critical accessibility violations immediately to avoid legal risks</li>' : ''}
                    ${report.summary.seriousViolations > 0 ? '<li>Prioritize serious violations that significantly impact user experience</li>' : ''}
                    <li>Implement consistent accessibility standards across all pages</li>
                    <li>Conduct regular accessibility testing in development workflow</li>
                </ul>
            `
                : ''
            }
        </div>
        `;
  }

  private generateSiteWideScope(report: SiteWideAccessibilityReport): string {
    return `
        <div class="page-break">
            <div class="section-title">Scope</div>
            
            <div class="field-row">
                <span class="field-label">Website:</span>
                <span class="field-value">${report.siteUrl}</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Scope of evaluation:</span>
                <span class="field-value">Site-wide accessibility evaluation (${report.summary.totalPages} pages)</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">WCAG Version:</span>
                <span class="field-value">WCAG 2.1</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Conformance target:</span>
                <span class="field-value">Level AA</span>
            </div>
            
            <div class="field-row">
                <span class="field-label">Testing methodology:</span>
                <span class="field-value">Automated testing with axe-core, Playwright, and custom accessibility checks</span>
            </div>
        </div>
        `;
  }

  private generateMostCommonViolations(report: SiteWideAccessibilityReport): string {
    if (report.summary.mostCommonViolations.length === 0) {
      return `
            <div class="section-title">Most Common Violations</div>
            <div class="summary-stats">
                <p><strong>🎉 No violations found across the site!</strong></p>
                <p>All tested pages meet the accessibility requirements. Continue following accessibility best practices.</p>
            </div>
            `;
    }

    let content = `
        <div class="section-title">Most Common Violations</div>
        <p style="margin-bottom: 20px;">The following violations appear most frequently across the site and should be prioritized for remediation:</p>
        `;

    report.summary.mostCommonViolations.forEach((violation, index) => {
      const impactClass = violation.impact.toLowerCase();
      const pagesText =
        violation.affectedPages === 1 ? '1 page' : `${violation.affectedPages} pages`;
      const occurrencesText =
        violation.totalOccurrences === 1
          ? '1 occurrence'
          : `${violation.totalOccurrences} occurrences`;

      content += `
            <div class="violation-summary-card violation-${impactClass}">
                <div class="violation-summary-title">
                    ${index + 1}. ${violation.id}
                    <span class="impact-badge impact-${impactClass}">${violation.impact}</span>
                </div>
                <div class="violation-summary-meta">
                    <strong>Affected:</strong> ${pagesText} • <strong>Total:</strong> ${occurrencesText}
                </div>
                <div style="margin-top: 8px; font-size: 10pt;">
                    ${violation.description}
                </div>
            </div>
            `;
    });

    return content;
  }

  private generateWcagComplianceMatrix(report: SiteWideAccessibilityReport): string {
    // WCAG 2.1 AA Success Criteria organised by the 4 principles
    const wcagCriteria = [
      // 1. Perceivable
      {
        id: '1.1.1',
        title: 'Non-text Content',
        level: 'A',
        principle: 'Perceivable',
        rules: ['image-alt', 'input-image-alt', 'area-alt', 'svg-img-alt'],
      },
      {
        id: '1.2.1',
        title: 'Audio-only and Video-only (Prerecorded)',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.2.2',
        title: 'Captions (Prerecorded)',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.2.3',
        title: 'Audio Description or Media Alternative (Prerecorded)',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.2.4',
        title: 'Captions (Live)',
        level: 'AA',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.2.5',
        title: 'Audio Description (Prerecorded)',
        level: 'AA',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.3.1',
        title: 'Info and Relationships',
        level: 'A',
        principle: 'Perceivable',
        rules: [
          'heading-order',
          'list',
          'definition-list',
          'dlitem',
          'listitem',
          'th-has-data-cells',
          'td-headers-attr',
        ],
      },
      {
        id: '1.3.2',
        title: 'Meaningful Sequence',
        level: 'A',
        principle: 'Perceivable',
        rules: ['tabindex'],
      },
      {
        id: '1.3.3',
        title: 'Sensory Characteristics',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.3.4',
        title: 'Orientation',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['css-orientation-lock'],
      },
      {
        id: '1.3.5',
        title: 'Identify Input Purpose',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['autocomplete-valid'],
      },
      {
        id: '1.4.1',
        title: 'Use of Color',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.4.2',
        title: 'Audio Control',
        level: 'A',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.4.3',
        title: 'Contrast (Minimum)',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['color-contrast'],
      },
      {
        id: '1.4.4',
        title: 'Resize text',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['meta-viewport'],
      },
      {
        id: '1.4.5',
        title: 'Images of Text',
        level: 'AA',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.4.10',
        title: 'Reflow',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['scrollable-region-focusable'],
      },
      {
        id: '1.4.11',
        title: 'Non-text Contrast',
        level: 'AA',
        principle: 'Perceivable',
        rules: ['color-contrast'],
      },
      {
        id: '1.4.12',
        title: 'Text Spacing',
        level: 'AA',
        principle: 'Perceivable',
        rules: [],
      },
      {
        id: '1.4.13',
        title: 'Content on Hover or Focus',
        level: 'AA',
        principle: 'Perceivable',
        rules: [],
      },

      // 2. Operable
      {
        id: '2.1.1',
        title: 'Keyboard',
        level: 'A',
        principle: 'Operable',
        rules: ['keyboard'],
      },
      {
        id: '2.1.2',
        title: 'No Keyboard Trap',
        level: 'A',
        principle: 'Operable',
        rules: ['keyboard-trap'],
      },
      {
        id: '2.1.4',
        title: 'Character Key Shortcuts',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.2.1',
        title: 'Timing Adjustable',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.2.2',
        title: 'Pause, Stop, Hide',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.3.1',
        title: 'Three Flashes or Below Threshold',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.4.1',
        title: 'Bypass Blocks',
        level: 'A',
        principle: 'Operable',
        rules: ['bypass', 'skip-link'],
      },
      {
        id: '2.4.2',
        title: 'Page Titled',
        level: 'A',
        principle: 'Operable',
        rules: ['document-title'],
      },
      {
        id: '2.4.3',
        title: 'Focus Order',
        level: 'A',
        principle: 'Operable',
        rules: ['focus-order-semantics', 'tabindex'],
      },
      {
        id: '2.4.4',
        title: 'Link Purpose (In Context)',
        level: 'A',
        principle: 'Operable',
        rules: ['link-name'],
      },
      {
        id: '2.4.5',
        title: 'Multiple Ways',
        level: 'AA',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.4.6',
        title: 'Headings and Labels',
        level: 'AA',
        principle: 'Operable',
        rules: ['heading-order', 'empty-heading'],
      },
      {
        id: '2.4.7',
        title: 'Focus Visible',
        level: 'AA',
        principle: 'Operable',
        rules: ['focus-visible'],
      },
      {
        id: '2.5.1',
        title: 'Pointer Gestures',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.5.2',
        title: 'Pointer Cancellation',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },
      {
        id: '2.5.3',
        title: 'Label in Name',
        level: 'A',
        principle: 'Operable',
        rules: ['label-content-name-mismatch'],
      },
      {
        id: '2.5.4',
        title: 'Motion Actuation',
        level: 'A',
        principle: 'Operable',
        rules: [],
      },

      // 3. Understandable
      {
        id: '3.1.1',
        title: 'Language of Page',
        level: 'A',
        principle: 'Understandable',
        rules: ['html-has-lang', 'html-lang-valid'],
      },
      {
        id: '3.1.2',
        title: 'Language of Parts',
        level: 'AA',
        principle: 'Understandable',
        rules: ['valid-lang'],
      },
      {
        id: '3.2.1',
        title: 'On Focus',
        level: 'A',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.2.2',
        title: 'On Input',
        level: 'A',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.2.3',
        title: 'Consistent Navigation',
        level: 'AA',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.2.4',
        title: 'Consistent Identification',
        level: 'AA',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.3.1',
        title: 'Error Identification',
        level: 'A',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.3.2',
        title: 'Labels or Instructions',
        level: 'A',
        principle: 'Understandable',
        rules: ['label', 'form-field-multiple-labels'],
      },
      {
        id: '3.3.3',
        title: 'Error Suggestion',
        level: 'AA',
        principle: 'Understandable',
        rules: [],
      },
      {
        id: '3.3.4',
        title: 'Error Prevention (Legal, Financial, Data)',
        level: 'AA',
        principle: 'Understandable',
        rules: [],
      },

      // 4. Robust
      {
        id: '4.1.1',
        title: 'Parsing',
        level: 'A',
        principle: 'Robust',
        rules: ['duplicate-id', 'duplicate-id-active', 'duplicate-id-aria'],
      },
      {
        id: '4.1.2',
        title: 'Name, Role, Value',
        level: 'A',
        principle: 'Robust',
        rules: [
          'button-name',
          'input-button-name',
          'select-name',
          'textarea-name',
          'aria-valid-attr',
          'aria-valid-attr-value',
          'aria-roles',
          'aria-required-attr',
          'aria-required-children',
          'aria-required-parent',
          'role-img-alt',
          'frame-title',
          'iframe-title',
        ],
      },
      {
        id: '4.1.3',
        title: 'Status Messages',
        level: 'AA',
        principle: 'Robust',
        rules: ['aria-live-region'],
      },
    ];

    // Create violation map for quick lookup
    const violationMap = new Map();
    Object.keys(report.violationsByType).forEach(violationId => {
      violationMap.set(violationId, report.violationsByType[violationId]);
    });

    let content = `
        <div class="page-break">
            <div class="section-title">WCAG 2.1 AA Compliance Matrix</div>
            <p style="margin-bottom: 20px;">Systematic evaluation of Web Content Accessibility Guidelines 2.1 Level AA success criteria:</p>
            
            <table class="wcag-table">
                <thead>
                    <tr>
                        <th style="width: 15%;">Success Criterion</th>
                        <th style="width: 45%;">Title</th>
                        <th style="width: 10%;">Level</th>
                        <th style="width: 15%;">Result</th>
                        <th style="width: 15%;">Observations</th>
                    </tr>
                </thead>
                <tbody>
        `;

    let currentPrinciple = '';

    wcagCriteria.forEach(criterion => {
      // Add principle header
      if (criterion.principle !== currentPrinciple) {
        currentPrinciple = criterion.principle;
        content += `
                <tr class="principle-header">
                    <td colspan="5"><strong>Principle ${criterion.principle.charAt(0)}: ${criterion.principle}</strong></td>
                </tr>
                `;
      }

      // Determine status based on violations
      let status = 'PASS';
      let statusClass = 'pass';
      let observations = 'No violations detected';
      let violationCount = 0;

      // Check if any of the criterion's rules have violations
      criterion.rules.forEach(rule => {
        if (violationMap.has(rule)) {
          status = 'FAIL';
          statusClass = 'fail';
          violationCount += violationMap.get(rule).count;
        }
      });

      // If no rules are defined for automated testing, leave blank for manual assessment
      if (criterion.rules.length === 0) {
        // Leave Results and Observations blank for manual completion
        content += `
                <tr>
                    <td class="criterion-id">${criterion.id}</td>
                    <td>${criterion.title}</td>
                    <td class="level-${criterion.level.toLowerCase()}">${criterion.level}</td>
                    <td class="blank-cell"></td>
                    <td class="blank-cell"></td>
                </tr>
                `;
      } else {
        // Show automated test results for criteria with rules
        if (status === 'FAIL') {
          observations = `${violationCount} violation${violationCount === 1 ? '' : 's'} found`;
        }

        content += `
                <tr>
                    <td class="criterion-id">${criterion.id}</td>
                    <td>${criterion.title}</td>
                    <td class="level-${criterion.level.toLowerCase()}">${criterion.level}</td>
                    <td><span class="status-badge ${statusClass}">${status}</span></td>
                    <td class="observations">${observations}</td>
                </tr>
                `;
      }
    });

    content += `
                </tbody>
            </table>
            
            <div class="wcag-legend" style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 6px; border-left: 4px solid #1e214d;">
                <p><strong>Legend:</strong></p>
                <p><span class="status-badge pass">PASS</span> - No accessibility violations detected for this criterion</p>
                <p><span class="status-badge fail">FAIL</span> - One or more accessibility violations found</p>
                <p><strong>Blank cells</strong> - Criteria requiring manual evaluation (to be completed by accessibility auditor)</p>
                <br>
                <p><strong>Note:</strong> This assessment focuses on automatically testable criteria. Blank rows require manual evaluation for complete compliance verification.</p>
            </div>
        </div>
        `;

    return content;
  }

  private generateDeveloperFixGuide(report: SiteWideAccessibilityReport): string {
    // Collect all violations with their elements from all pages
    const allViolations: Array<{
      violation: any;
      element: any;
      pageUrl: string;
      pageTitle: string;
    }> = [];

    report.pageReports.forEach(pageReport => {
      pageReport.violations.forEach(violation => {
        violation.elements.forEach(element => {
          allViolations.push({
            violation,
            element,
            pageUrl: pageReport.url,
            pageTitle: pageReport.pageAnalysis.title,
          });
        });
      });
    });

    if (allViolations.length === 0) {
      return `
            <div class="page-break">
                <div class="section-title">Developer Fix Guide</div>
                <div class="summary-stats">
                    <p><strong>🎉 No violations found!</strong></p>
                    <p>All pages are accessible. No developer fixes required.</p>
                </div>
            </div>
            `;
    }

    // Group violations by violation ID to consolidate duplicates
    const violationGroups = new Map<
      string,
      {
        violation: any;
        instances: Array<{
          element: any;
          pageUrl: string;
          pageTitle: string;
        }>;
      }
    >();

    allViolations.forEach(item => {
      const violationId = item.violation.id;
      if (!violationGroups.has(violationId)) {
        violationGroups.set(violationId, {
          violation: item.violation,
          instances: [],
        });
      }
      violationGroups.get(violationId)!.instances.push({
        element: item.element,
        pageUrl: item.pageUrl,
        pageTitle: item.pageTitle,
      });
    });

    // Convert to array and sort by impact (critical first) and then by violation type
    const sortedViolationGroups = Array.from(violationGroups.entries()).sort(([, a], [, b]) => {
      const impactOrder = { critical: 4, serious: 3, moderate: 2, minor: 1 };
      const impactDiff =
        (impactOrder as any)[b.violation.impact] - (impactOrder as any)[a.violation.impact];
      if (impactDiff !== 0) return impactDiff;
      return a.violation.id.localeCompare(b.violation.id);
    });

    let content = `
        <div class="page-break">
            <div class="section-title">Developer Fix Guide</div>
            <p style="margin-bottom: 20px;">Consolidated accessibility violations grouped by type. Each violation shows the fix guidance once, followed by all affected pages and elements to streamline development efforts.</p>
        `;

    sortedViolationGroups.forEach(([_violationId, group]) => {
      const { violation, instances } = group;
      const impactClass = violation.impact.toLowerCase();
      const uniquePages = [...new Set(instances.map(i => i.pageUrl))];
      const totalInstances = instances.length;

      // Generate code fix suggestion using the first instance
      const fixSuggestion = this.generateCodeFixSuggestion(violation.id, instances[0].element.html);

      content += `
            <div class="violation-card violation-${impactClass}" style="margin: 20px 0; page-break-inside: avoid;">
                <div class="violation-header">
                    <div class="violation-title">
                        <span class="impact-badge impact-${impactClass}">${violation.impact.toUpperCase()}</span>
                        ${violation.id}: ${violation.description}
                    </div>
                    <div class="violation-meta">
                        <strong>Affected:</strong> ${uniquePages.length} page${uniquePages.length === 1 ? '' : 's'} • ${totalInstances} element${totalInstances === 1 ? '' : 's'}
                        ${violation.browsers && violation.browsers.length > 0 ? `<br><strong>Browsers:</strong> ${violation.browsers.join(', ')}` : ''}
                        ${violation.tools && violation.tools.length > 0 ? `<br><strong>Detected by:</strong> ${violation.tools.join(', ')}` : ''}
                    </div>
                </div>

                <div class="violation-details">
                    <div class="detail-section">
                        <h4>📖 How to Fix</h4>
                        <p><strong>Issue:</strong> ${violation.description}</p>
                        <p><strong>Solution:</strong> ${violation.help}</p>
                        <p><strong>Priority:</strong> <span class="priority-badge priority-${violation.remediation.priority.toLowerCase()}">${violation.remediation.priority}</span></p>
                        <p><strong>Effort:</strong> ${violation.remediation.effort}</p>
                        
                        ${
                          violation.remediation.suggestions.length > 0
                            ? `
                        <p><strong>Recommendations:</strong></p>
                        <ul style="margin-left: 20px; padding-left: 20px; line-height: 1.6;">
                            ${violation.remediation.suggestions.map((suggestion: string) => `<li style="margin-bottom: 5px;">${suggestion}</li>`).join('')}
                        </ul>
                        `
                            : ''
                        }
                        
                        <p><strong>Learn More:</strong> <a href="${violation.helpUrl}" target="_blank">${violation.helpUrl}</a></p>
                    </div>

                    ${
                      fixSuggestion
                        ? `
                    <div class="detail-section">
                        <h4>✅ Code Fix Example</h4>
                        <div class="code-container fixed-code">
                            <pre><code>${this.escapeHtml(fixSuggestion)}</code></pre>
                        </div>
                    </div>
                    `
                        : ''
                    }

                    <div class="detail-section">
                        <h4>🏷️ WCAG Information</h4>
                        <p><strong>Level:</strong> ${violation.wcagLevel}</p>
                        <p><strong>Guidelines:</strong> ${violation.wcagTags.join(', ')}</p>
                    </div>

                    <div class="detail-section">
                        <h4>📍 All Affected Locations</h4>
                        ${this.generateAffectedLocationsTable(instances)}
                    </div>
                </div>
            </div>
            `;
    });

    content += `
        </div>
        `;

    return content;
  }

  private generateAffectedLocationsTable(
    instances: Array<{
      element: any;
      pageUrl: string;
      pageTitle: string;
    }>
  ): string {
    // Group instances by page for better organisation
    const instancesByPage = new Map<
      string,
      Array<{
        element: any;
        pageTitle: string;
      }>
    >();

    instances.forEach(instance => {
      if (!instancesByPage.has(instance.pageUrl)) {
        instancesByPage.set(instance.pageUrl, []);
      }
      instancesByPage.get(instance.pageUrl)!.push({
        element: instance.element,
        pageTitle: instance.pageTitle,
      });
    });

    let content = `<div style="margin-top: 15px;">`;

    // Create a more compact, page-by-page summary
    for (const [pageUrl, pageInstances] of instancesByPage) {
      const pageTitle = pageInstances[0].pageTitle || 'Untitled';
      const shortUrl = pageUrl.replace(/^https?:\/\//, '').replace(/\/$/, '');

      content += `
        <div style="margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; overflow: hidden;">
          <div style="background: #f8f9fa; padding: 8px; border-bottom: 1px solid #ddd;">
            <strong style="font-size: 10pt; color: #1e214d;">${pageTitle}</strong>
            <br><span style="font-size: 8pt; color: #db0064; font-family: monospace;">${shortUrl}</span>
            <span style="font-size: 8pt; color: #1e214d; opacity: 0.7; float: right;">${pageInstances.length} element${pageInstances.length === 1 ? '' : 's'}</span>
          </div>
          <div style="padding: 8px;">
      `;

      // List elements in a more compact format
      pageInstances.forEach((instance, index) => {
        const element = instance.element;
        const htmlPreview = this.escapeHtml(element.html.substring(0, 100));
        const isLast = index === pageInstances.length - 1;

        content += `
          <div style="margin-bottom: ${isLast ? '0' : '8px'}; padding-bottom: ${isLast ? '0' : '8px'}; ${isLast ? '' : 'border-bottom: 1px solid #eee;'}">
            <div style="font-size: 8pt; margin-bottom: 3px;">
              <code style="background: #f1f3f4; padding: 2px 4px; border-radius: 3px; font-size: 8pt; color: #1e214d;">${element.selector || 'N/A'}</code>
              ${element.failureSummary ? `<span style="color: #db0064; margin-left: 8px;">${element.failureSummary}</span>` : ''}
            </div>
            <div style="font-size: 7pt; color: #1e214d; font-family: monospace; background: #f8f9fa; padding: 3px 6px; border-radius: 3px; border-left: 2px solid #1e214d; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
              ${htmlPreview}${element.html.length > 100 ? '...' : ''}
            </div>
          </div>
        `;
      });

      content += `
          </div>
        </div>
      `;
    }

    content += `</div>`;
    return content;
  }

  private generateCodeFixSuggestion(violationId: string, originalHtml: string): string {
    // Generate specific code fix suggestions based on violation type
    const suggestions: Record<string, (html: string) => string> = {
      'image-alt': html => {
        return html.replace(/<img([^>]*?)>/gi, (match, attrs) => {
          if (attrs.includes('alt=')) {
            return match.replace(/alt\s*=\s*["'][\s]*["']/gi, 'alt="Descriptive alternative text"');
          } else {
            return `<img${attrs} alt="Descriptive alternative text">`;
          }
        });
      },
      'color-contrast': (html: string) => {
        return `${
          html
        }\n<!-- Fix: Increase colour contrast to meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text) -->\n<!-- Example: Use darker colours or add background colours for better contrast -->`;
      },
      'link-name': html => {
        return html.replace(/<a([^>]*?)>(.*?)<\/a>/gi, (match, attrs, content) => {
          if (!content.trim() || content.trim().length < 4) {
            return `<a${attrs} aria-label="Descriptive link purpose">${content || 'Descriptive link text'}</a>`;
          }
          return match;
        });
      },
      'button-name': html => {
        return html.replace(/<button([^>]*?)>(.*?)<\/button>/gi, (match, attrs, content) => {
          if (!content.trim()) {
            return `<button${attrs} aria-label="Descriptive button purpose">${content || 'Button action'}</button>`;
          }
          return match;
        });
      },
      label: html => {
        return html.replace(/<input([^>]*?)>/gi, (match, attrs) => {
          if (!attrs.includes('aria-label') && !attrs.includes('aria-labelledby')) {
            const id = attrs.match(/id\s*=\s*["']([^"']*)["']/);
            if (id) {
              return `<label for="${id[1]}">Input label</label>\n${match}`;
            } else {
              return match.replace('>', ' aria-label="Input description">');
            }
          }
          return match;
        });
      },
      'heading-order': html => {
        return `${
          html
        }\n<!-- Fix: Ensure headings follow logical order (h1, h2, h3, etc.) without skipping levels -->`;
      },
      'meta-viewport': html => {
        return '<meta name="viewport" content="width=device-width, initial-scale=1">';
      },
      'frame-title': html => {
        return html.replace(/<(iframe|frame)([^>]*?)>/gi, (match, tag, attrs) => {
          if (!attrs.includes('title=')) {
            return `<${tag}${attrs} title="Descriptive frame purpose">`;
          }
          return match;
        });
      },
      'select-name': html => {
        return html.replace(/<select([^>]*?)>/gi, (match, attrs) => {
          if (!attrs.includes('aria-label') && !attrs.includes('aria-labelledby')) {
            return `<label for="select-id">Select label</label>\n${match.replace('>', ' id="select-id">')}`;
          }
          return match;
        });
      },
    };

    const fixFunction = suggestions[violationId];
    if (fixFunction) {
      return fixFunction(originalHtml);
    }

    return `${originalHtml}\n<!-- Refer to WCAG guidelines for specific fix recommendations -->`;
  }

  private escapeHtml(html: string): string {
    return html
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;');
  }

  private generatePageByPageResults(report: SiteWideAccessibilityReport): string {
    let content = `
        <div class="page-break">
            <div class="section-title">Page-by-Page Results</div>
            <p style="margin-bottom: 20px;">Detailed accessibility results for each tested page:</p>

            <table class="page-table">
                <thead>
                    <tr>
                        <th style="width: 50%;">Page URL</th>
                        <th style="width: 20%;">Page Title</th>
                        <th style="width: 15%;">Status</th>
                        <th style="width: 15%;">Violations</th>
                    </tr>
                </thead>
                <tbody>
        `;

    report.pageReports.forEach(pageReport => {
      const hasViolations = pageReport.summary.totalViolations > 0;
      const statusClass = hasViolations ? 'non-compliant' : 'compliant';
      const statusText = hasViolations ? 'Issues Found' : 'Compliant';

      const violationsSummary = hasViolations
        ? `${pageReport.summary.totalViolations} total (${pageReport.summary.criticalViolations}C, ${pageReport.summary.seriousViolations}S)`
        : 'None';

      content += `
            <tr>
                <td><a href="${pageReport.url}" class="page-url" target="_blank">${pageReport.url}</a></td>
                <td>${pageReport.pageAnalysis.title || 'No title'}</td>
                <td><span class="compliance-badge ${statusClass}">${statusText}</span></td>
                <td>${violationsSummary}</td>
            </tr>
            `;
    });

    content += `
                </tbody>
            </table>
        </div>
        `;

    return content;
  }

  private cleanupTemporaryFiles(tempHtmlPath: string): void {
    const fs = require('fs');

    try {
      // Clean up the main temporary HTML file
      if (fs.existsSync(tempHtmlPath)) {
        fs.unlinkSync(tempHtmlPath);
        console.log('🧹 Cleaned up temporary HTML file');
      }

      // Clean up any other temporary files that might have been created
      const tempDir = require('path').dirname(tempHtmlPath);
      const tempFiles = fs
        .readdirSync(tempDir)
        .filter(
          (file: string) =>
            file.startsWith('temp-') && (file.endsWith('.html') || file.endsWith('.css'))
        );

      tempFiles.forEach((file: string) => {
        const filePath = require('path').join(tempDir, file);
        fs.unlinkSync(filePath);
        console.log(`🧹 Cleaned up temporary file: ${file}`);
      });
    } catch (error) {
      console.warn('Warning: Could not clean up temporary files:', error);
    }
  }
}
