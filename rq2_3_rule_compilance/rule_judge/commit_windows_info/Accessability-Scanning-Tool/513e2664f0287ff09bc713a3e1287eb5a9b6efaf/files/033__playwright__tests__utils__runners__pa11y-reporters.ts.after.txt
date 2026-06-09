import { Pa11yResult } from './pa11y-test-runner';

export interface Pa11yReporter {
  results(results: Pa11yResult): string;
  error(error: string): string;
  begin?(): string;
  debug?(message: string): string;
}

/**
 * WCAG-focused reporter for Pa11y
 */
export class WCAGReporter implements Pa11yReporter {
  results(results: Pa11yResult): string {
    const wcagGrouped = this.groupByWCAG(results.issues);
    let output = '';

    output += `\n# WCAG 2.1 Compliance Report\n`;
    output += `URL: ${results.pageUrl}\n`;
    output += `Page Title: ${results.documentTitle}\n`;
    output += `Total Issues: ${results.issues.length}\n\n`;

    // Group by WCAG level
    const levels = ['A', 'AA', 'AAA'];
    levels.forEach(level => {
      const levelIssues = wcagGrouped[level] || [];
      if (levelIssues.length > 0) {
        output += `## WCAG 2.1 Level ${level} Issues (${levelIssues.length})\n\n`;

        levelIssues.forEach((issue, index) => {
          output += `### ${index + 1}. ${issue.message}\n`;
          output += `**Type:** ${issue.type}\n`;
          output += `**Code:** ${issue.code}\n`;
          output += `**Context:** \`${issue.context}\`\n`;
          output += `**Selector:** \`${issue.selector}\`\n\n`;
        });
      }
    });

    return output;
  }

  error(error: string): string {
    return `\n❌ **ERROR:** ${error}\n`;
  }

  begin(): string {
    return `\n🔍 **Starting WCAG 2.1 Analysis...**\n`;
  }

  debug(message: string): string {
    return `🐛 **DEBUG:** ${message}\n`;
  }

  private groupByWCAG(issues: any[]): Record<string, any[]> {
    const grouped: Record<string, any[]> = { A: [], AA: [], AAA: [] };

    issues.forEach(issue => {
      // Extract WCAG level from code or context
      const code = issue.code.toLowerCase();
      if (code.includes('aaa') || code.includes('level-aaa')) {
        grouped.AAA.push(issue);
      } else if (code.includes('aa') || code.includes('level-aa')) {
        grouped.AA.push(issue);
      } else {
        grouped.A.push(issue);
      }
    });

    return grouped;
  }
}

/**
 * JSON-structured reporter for Pa11y
 */
export class JSONStructuredReporter implements Pa11yReporter {
  results(results: Pa11yResult): string {
    const structuredOutput = {
      summary: {
        url: results.pageUrl,
        title: results.documentTitle,
        totalIssues: results.issues.length,
        issueTypes: this.getIssueTypeCounts(results.issues),
        severity: this.getSeverityCounts(results.issues),
        timestamp: new Date().toISOString(),
      },
      issues: results.issues.map(issue => ({
        id: this.generateIssueId(issue),
        type: issue.type,
        severity: this.mapTypeToSeverity(issue.type),
        message: issue.message,
        code: issue.code,
        context: issue.context,
        selector: issue.selector,
        runner: issue.runner,
        wcagLevel: this.extractWCAGLevel(issue.code),
        category: this.categorizeIssue(issue),
        fixes: this.suggestFixes(issue),
      })),
      statistics: {
        errorRate: (
          (results.issues.filter(i => i.type === 'error').length / results.issues.length) *
          100
        ).toFixed(2),
        warningRate: (
          (results.issues.filter(i => i.type === 'warning').length / results.issues.length) *
          100
        ).toFixed(2),
        noticeRate: (
          (results.issues.filter(i => i.type === 'notice').length / results.issues.length) *
          100
        ).toFixed(2),
      },
    };

    return JSON.stringify(structuredOutput, null, 2);
  }

  error(error: string): string {
    return JSON.stringify(
      {
        error: true,
        message: error,
        timestamp: new Date().toISOString(),
      },
      null,
      2
    );
  }

  begin(): string {
    return JSON.stringify(
      {
        status: 'started',
        timestamp: new Date().toISOString(),
      },
      null,
      2
    );
  }

  debug(message: string): string {
    return JSON.stringify(
      {
        debug: true,
        message,
        timestamp: new Date().toISOString(),
      },
      null,
      2
    );
  }

  private getIssueTypeCounts(issues: any[]): Record<string, number> {
    return issues.reduce((acc, issue) => {
      acc[issue.type] = (acc[issue.type] || 0) + 1;
      return acc;
    }, {});
  }

  private getSeverityCounts(issues: any[]): Record<string, number> {
    return issues.reduce((acc, issue) => {
      const severity = this.mapTypeToSeverity(issue.type);
      acc[severity] = (acc[severity] || 0) + 1;
      return acc;
    }, {});
  }

  private mapTypeToSeverity(type: string): string {
    switch (type) {
      case 'error':
        return 'high';
      case 'warning':
        return 'medium';
      case 'notice':
        return 'low';
      default:
        return 'unknown';
    }
  }

  private generateIssueId(issue: any): string {
    return `pa11y-${issue.code}-${issue.selector.replace(/[^a-zA-Z0-9]/g, '-')}`;
  }

  private extractWCAGLevel(code: string): string {
    const lowerCode = code.toLowerCase();
    if (lowerCode.includes('aaa')) return 'AAA';
    if (lowerCode.includes('aa')) return 'AA';
    if (lowerCode.includes('a')) return 'A';
    return 'Unknown';
  }

  private categorizeIssue(issue: any): string {
    const message = issue.message.toLowerCase();
    const context = issue.context.toLowerCase();

    if (message.includes('color') || message.includes('contrast')) return 'color-contrast';
    if (message.includes('aria') || context.includes('aria')) return 'aria';
    if (message.includes('form') || message.includes('input') || message.includes('label'))
      return 'forms';
    if (message.includes('image') || message.includes('alt')) return 'images';
    if (message.includes('heading') || message.includes('landmark')) return 'structure';
    if (message.includes('keyboard') || message.includes('focus')) return 'keyboard';
    if (message.includes('link') || message.includes('anchor')) return 'links';

    return 'general';
  }

  private suggestFixes(issue: any): string[] {
    const fixes: string[] = [];
    const message = issue.message.toLowerCase();
    const context = issue.context.toLowerCase();

    if (message.includes('alt') && message.includes('missing')) {
      fixes.push('Add alt attribute to image element');
      fixes.push('Use empty alt="" for decorative images');
    }

    if (message.includes('label') && message.includes('missing')) {
      fixes.push('Add label element for form control');
      fixes.push('Use aria-label or aria-labelledby attribute');
    }

    if (message.includes('heading') && message.includes('order')) {
      fixes.push('Ensure heading levels are in logical order');
      fixes.push('Do not skip heading levels');
    }

    if (message.includes('color') && message.includes('contrast')) {
      fixes.push('Increase color contrast ratio to meet WCAG standards');
      fixes.push('Use a darker text color or lighter background');
    }

    if (message.includes('aria') && message.includes('invalid')) {
      fixes.push('Use valid ARIA attributes');
      fixes.push('Remove invalid ARIA attributes');
    }

    if (fixes.length === 0) {
      fixes.push('Review the issue and apply appropriate accessibility fixes');
    }

    return fixes;
  }
}

/**
 * Accessibility Category reporter for Pa11y
 */
export class CategoryReporter implements Pa11yReporter {
  results(results: Pa11yResult): string {
    const categories = this.groupByCategory(results.issues);
    let output = '';

    output += `\n# Accessibility Issues by Category\n`;
    output += `URL: ${results.pageUrl}\n`;
    output += `Page Title: ${results.documentTitle}\n`;
    output += `Total Issues: ${results.issues.length}\n\n`;

    // Sort categories by issue count
    const sortedCategories = Object.entries(categories).sort(([, a], [, b]) => b.length - a.length);

    sortedCategories.forEach(([category, issues]) => {
      output += `## ${this.formatCategoryName(category)} (${issues.length} issues)\n\n`;

      issues.forEach((issue, index) => {
        output += `${index + 1}. **${issue.type.toUpperCase()}**: ${issue.message}\n`;
        output += `   - Code: \`${issue.code}\`\n`;
        output += `   - Selector: \`${issue.selector}\`\n`;
        output += `   - Context: \`${issue.context.substring(0, 100)}...\`\n\n`;
      });
    });

    return output;
  }

  error(error: string): string {
    return `\n❌ **Category Analysis Error:** ${error}\n`;
  }

  begin(): string {
    return `\n📊 **Starting Category Analysis...**\n`;
  }

  debug(message: string): string {
    return `🏷️ **Category Debug:** ${message}\n`;
  }

  private groupByCategory(issues: any[]): Record<string, any[]> {
    const categories: Record<string, any[]> = {
      'color-contrast': [],
      aria: [],
      forms: [],
      images: [],
      structure: [],
      keyboard: [],
      links: [],
      general: [],
    };

    issues.forEach(issue => {
      const category = this.categorizeIssue(issue);
      categories[category].push(issue);
    });

    // Remove empty categories
    Object.keys(categories).forEach(key => {
      if (categories[key].length === 0) {
        delete categories[key];
      }
    });

    return categories;
  }

  private categorizeIssue(issue: any): string {
    const message = issue.message.toLowerCase();
    const context = issue.context.toLowerCase();

    if (message.includes('color') || message.includes('contrast')) return 'color-contrast';
    if (message.includes('aria') || context.includes('aria')) return 'aria';
    if (message.includes('form') || message.includes('input') || message.includes('label'))
      return 'forms';
    if (message.includes('image') || message.includes('alt')) return 'images';
    if (message.includes('heading') || message.includes('landmark')) return 'structure';
    if (message.includes('keyboard') || message.includes('focus')) return 'keyboard';
    if (message.includes('link') || message.includes('anchor')) return 'links';

    return 'general';
  }

  private formatCategoryName(category: string): string {
    return category
      .split('-')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
}

/**
 * Executive Summary reporter for Pa11y
 */
export class ExecutiveSummaryReporter implements Pa11yReporter {
  results(results: Pa11yResult): string {
    const summary = this.generateSummary(results);
    let output = '';

    output += `\n# Executive Accessibility Summary\n`;
    output += `**URL:** ${results.pageUrl}\n`;
    output += `**Page Title:** ${results.documentTitle}\n`;
    output += `**Assessment Date:** ${new Date().toLocaleDateString()}\n\n`;

    output += `## Overall Compliance Status\n`;
    output += `- **Total Issues Found:** ${summary.totalIssues}\n`;
    output += `- **Critical Issues:** ${summary.criticalIssues}\n`;
    output += `- **Compliance Score:** ${summary.complianceScore}%\n`;
    output += `- **WCAG 2.1 Level:** ${summary.wcagLevel}\n\n`;

    output += `## Issue Breakdown\n`;
    output += `- **Errors:** ${summary.errors} (${summary.errorPercentage}%)\n`;
    output += `- **Warnings:** ${summary.warnings} (${summary.warningPercentage}%)\n`;
    output += `- **Notices:** ${summary.notices} (${summary.noticePercentage}%)\n\n`;

    output += `## Priority Actions Required\n`;
    summary.priorityActions.forEach((action, index) => {
      output += `${index + 1}. ${action}\n`;
    });

    output += `\n## Compliance Recommendations\n`;
    summary.recommendations.forEach((rec, index) => {
      output += `${index + 1}. ${rec}\n`;
    });

    return output;
  }

  error(error: string): string {
    return `\n🚨 **Executive Summary Error:** ${error}\n`;
  }

  begin(): string {
    return `\n📋 **Generating Executive Summary...**\n`;
  }

  debug(message: string): string {
    return `📊 **Executive Debug:** ${message}\n`;
  }

  private generateSummary(results: Pa11yResult): any {
    const totalIssues = results.issues.length;
    const errors = results.issues.filter(i => i.type === 'error').length;
    const warnings = results.issues.filter(i => i.type === 'warning').length;
    const notices = results.issues.filter(i => i.type === 'notice').length;

    // Calculate compliance score (simplified)
    const complianceScore = Math.max(0, 100 - errors * 10 - warnings * 5 - notices * 1);

    // Determine WCAG level based on errors
    let wcagLevel = 'AAA';
    if (errors > 0) wcagLevel = 'Non-compliant';
    else if (warnings > 5) wcagLevel = 'AA';

    // Generate priority actions
    const priorityActions: string[] = [];
    if (errors > 0)
      priorityActions.push(`Address ${errors} critical accessibility errors immediately`);
    if (warnings > 10) priorityActions.push(`Review and fix ${warnings} accessibility warnings`);
    if (notices > 20)
      priorityActions.push(
        `Consider addressing ${notices} accessibility notices for enhanced compliance`
      );

    // Generate recommendations
    const recommendations: string[] = [];
    if (complianceScore < 70) {
      recommendations.push('Implement comprehensive accessibility audit and remediation plan');
    }
    if (errors > 0) {
      recommendations.push('Prioritize fixing all accessibility errors before launch');
    }
    if (warnings > 5) {
      recommendations.push('Establish accessibility testing in development workflow');
    }
    recommendations.push('Conduct regular accessibility testing and monitoring');

    return {
      totalIssues,
      criticalIssues: errors,
      complianceScore: Math.round(complianceScore),
      wcagLevel,
      errors,
      warnings,
      notices,
      errorPercentage: totalIssues > 0 ? Math.round((errors / totalIssues) * 100) : 0,
      warningPercentage: totalIssues > 0 ? Math.round((warnings / totalIssues) * 100) : 0,
      noticePercentage: totalIssues > 0 ? Math.round((notices / totalIssues) * 100) : 0,
      priorityActions,
      recommendations,
    };
  }
}

/**
 * Factory for creating Pa11y reporters
 */
export class Pa11yReporterFactory {
  static create(type: string): Pa11yReporter {
    switch (type) {
      case 'wcag':
        return new WCAGReporter();
      case 'json-structured':
        return new JSONStructuredReporter();
      case 'category':
        return new CategoryReporter();
      case 'executive':
        return new ExecutiveSummaryReporter();
      default:
        throw new Error(`Unknown Pa11y reporter type: ${type}`);
    }
  }

  static getAvailableReporters(): string[] {
    return ['wcag', 'json-structured', 'category', 'executive'];
  }
}
