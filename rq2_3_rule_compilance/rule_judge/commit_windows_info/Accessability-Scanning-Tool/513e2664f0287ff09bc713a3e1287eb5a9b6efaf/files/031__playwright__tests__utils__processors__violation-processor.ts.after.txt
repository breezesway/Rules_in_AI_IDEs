import { Page } from '@playwright/test';
import { AxeResults, Result as AxeViolation } from 'axe-core';
import { Pa11yResult } from '../runners/pa11y-test-runner';
import { WaveResult } from '../runners/wave-test-runner';
import { TenonResult } from '../runners/tenon-test-runner';
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService, ServiceResult } from '../services/error-handler-service';

export interface ProcessedViolation {
  id: string;
  impact: 'minor' | 'moderate' | 'serious' | 'critical';
  description: string;
  help: string;
  helpUrl: string;
  wcagTags: string[];
  wcagLevel: 'A' | 'AA' | 'AAA' | 'Unknown';
  occurrences: number;
  browsers?: string[];
  tools: string[];
  elements: Array<{
    html: string;
    target: any;
    failureSummary: string;
    screenshot?: string;
    selector: string;
    xpath?: string;
    boundingRect?: { x: number; y: number; width: number; height: number };
    relatedNodes?: Array<{
      html: string;
      target: any;
    }>;
  }>;
  scenarioRelevance: string[];
  remediation: {
    priority: 'High' | 'Medium' | 'Low';
    effort: 'Low' | 'Medium' | 'High';
    suggestions: string[];
    codeExample?: string;
  };
}

export interface MultiToolResults {
  axe: AxeResults | null;
  pa11y: Pa11yResult | null;
  lighthouse: any;
  wave: WaveResult | null;
  tenon: TenonResult | null;
}

export class ViolationProcessor {
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();

  constructor(private page: Page) {}

  /**
   * Processes violations from multiple tools
   */
  async processMultiToolViolations(
    results: MultiToolResults,
    captureScreenshots: boolean = true
  ): Promise<ServiceResult<ProcessedViolation[]>> {
    return this.errorHandler.executeWithErrorHandling(async () => {
      const allViolations: ProcessedViolation[] = [];

      // Process axe violations
      if (results.axe?.violations) {
        const axeViolations = await this.processAxeViolations(
          results.axe.violations,
          captureScreenshots
        );
        allViolations.push(...axeViolations);
      }

      // Process Pa11y issues
      if (results.pa11y?.issues) {
        const pa11yViolations = await this.processPa11yIssues(
          results.pa11y.issues,
          captureScreenshots
        );
        allViolations.push(...pa11yViolations);
      }

      // Process Lighthouse audits
      if (results.lighthouse) {
        const lighthouseViolations = await this.processLighthouseAudits(
          results.lighthouse,
          captureScreenshots
        );
        allViolations.push(...lighthouseViolations);
      }

      // Process Wave results
      if (results.wave) {
        const waveViolations = await this.processWaveResults(results.wave, captureScreenshots);
        allViolations.push(...waveViolations);
      }

      // Process Tenon results
      if (results.tenon) {
        const tenonViolations = await this.processTenonResults(results.tenon, captureScreenshots);
        allViolations.push(...tenonViolations);
      }

      // Merge violations from multiple tools
      const mergedViolations = this.mergeViolationsFromMultipleTools(allViolations);

      return mergedViolations;
    }, 'processMultiToolViolations');
  }

  /**
   * Processes axe-core violations
   */
  private async processAxeViolations(
    violations: AxeViolation[],
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const processedViolations: ProcessedViolation[] = [];

    for (const violation of violations) {
      const elements = [];

      for (const node of violation.nodes) {
        const element: ProcessedViolation['elements'][0] = {
          html: node.html,
          target: node.target,
          failureSummary: node.failureSummary || violation.description,
          selector: Array.isArray(node.target) ? node.target.join(', ') : String(node.target),
          relatedNodes: (node as any).relatedNodes?.map((relatedNode: any) => ({
            html: relatedNode.html,
            target: relatedNode.target,
          })),
        };

        // Add XPath if available
        if (node.target && Array.isArray(node.target) && node.target.length > 0) {
          try {
            const targetElement = await this.page.locator(element.selector).first();
            if (targetElement) {
              element.xpath = await this.generateXPath(targetElement);
            }
          } catch (error) {
            // XPath generation failed, continue without it
          }
        }

        // Add bounding rectangle
        try {
          const boundingRect = await this.page.locator(element.selector).first().boundingBox();
          if (boundingRect) {
            element.boundingRect = boundingRect;
          }
        } catch (error) {
          // Bounding rect failed, continue without it
        }

        // Capture screenshot if requested
        if (captureScreenshots) {
          try {
            const screenshot = await this.captureElementScreenshot(element.selector);
            if (screenshot) {
              element.screenshot = screenshot;
            }
          } catch (error) {
            // Screenshot failed, continue without it
          }
        }

        elements.push(element);
      }

      processedViolations.push({
        id: violation.id,
        impact: violation.impact as ProcessedViolation['impact'],
        description: violation.description,
        help: violation.help,
        helpUrl: violation.helpUrl,
        wcagTags: violation.tags.filter(tag => tag.startsWith('wcag')),
        wcagLevel: this.getWcagLevel(violation.tags),
        occurrences: violation.nodes.length,
        tools: ['axe-core'],
        elements,
        scenarioRelevance: this.getScenarioRelevance(violation.id, violation.tags),
        remediation: this.getRemediationGuidance(violation),
      });
    }

    return processedViolations;
  }

  /**
   * Processes Pa11y issues
   */
  private async processPa11yIssues(
    issues: Pa11yResult['issues'],
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const processedViolations: ProcessedViolation[] = [];

    for (const issue of issues) {
      const element: ProcessedViolation['elements'][0] = {
        html: issue.context,
        target: issue.selector,
        failureSummary: issue.message,
        selector: issue.selector,
      };

      // Capture screenshot if requested
      if (captureScreenshots) {
        try {
          const screenshot = await this.captureElementScreenshot(issue.selector);
          if (screenshot) {
            element.screenshot = screenshot;
          }
        } catch (error) {
          // Screenshot failed, continue without it
        }
      }

      processedViolations.push({
        id: issue.code,
        impact: this.mapPa11yTypeToImpact(issue.type),
        description: issue.message,
        help: issue.message,
        helpUrl: `https://www.w3.org/WAI/WCAG21/Understanding/`,
        wcagTags: this.extractWcagTagsFromPa11y(issue.code),
        wcagLevel: this.extractWcagLevelFromPa11y(issue.code),
        occurrences: 1,
        tools: ['pa11y'],
        elements: [element],
        scenarioRelevance: this.getScenarioRelevance(issue.code, []),
        remediation: this.getRemediationGuidanceForPa11y(issue),
      });
    }

    return processedViolations;
  }

  /**
   * Processes Lighthouse audits
   */
  private async processLighthouseAudits(
    audits: any,
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const processedViolations: ProcessedViolation[] = [];

    // Process accessibility audits from Lighthouse
    const accessibilityAudits = [
      'color-contrast',
      'image-alt',
      'label',
      'link-name',
      'button-name',
      'document-title',
      'html-has-lang',
      'html-lang-valid',
      'meta-viewport',
      'heading-order',
    ];

    for (const auditId of accessibilityAudits) {
      const audit = audits[auditId];
      if (audit && audit.score < 1) {
        // This audit failed
        processedViolations.push({
          id: auditId,
          impact: 'moderate',
          description: audit.title || audit.description,
          help: audit.description,
          helpUrl: audit.details?.helpUrl || 'https://web.dev/lighthouse-accessibility/',
          wcagTags: ['wcag2aa'],
          wcagLevel: 'AA',
          occurrences: 1,
          tools: ['lighthouse'],
          elements: [],
          scenarioRelevance: ['general'],
          remediation: {
            priority: 'Medium',
            effort: 'Medium',
            suggestions:
              audit.details?.items?.map((item: any) => item.snippet || item.node?.snippet) || [],
          },
        });
      }
    }

    return processedViolations;
  }

  /**
   * Processes Wave results
   */
  private async processWaveResults(
    waveResult: WaveResult,
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const processedViolations: ProcessedViolation[] = [];

    // Process Wave errors
    for (const error of waveResult.categories.error.items) {
      const elements = [];
      for (const selector of error.selectors) {
        const element: ProcessedViolation['elements'][0] = {
          html: selector,
          target: selector,
          failureSummary: error.description,
          selector: selector,
        };

        if (captureScreenshots) {
          try {
            const screenshot = await this.captureElementScreenshot(selector);
            if (screenshot) {
              element.screenshot = screenshot;
            }
          } catch (error) {
            // Screenshot failed, continue without it
          }
        }

        elements.push(element);
      }

      processedViolations.push({
        id: error.id,
        impact: 'serious',
        description: error.description,
        help: error.description,
        helpUrl: `https://wave.webaim.org/help#${error.id}`,
        wcagTags: error.wcag.map(w => w.toLowerCase()),
        wcagLevel: this.getWcagLevelFromWcagRefs(error.wcag),
        occurrences: error.count,
        tools: ['wave'],
        elements,
        scenarioRelevance: this.getScenarioRelevance(error.id, error.wcag),
        remediation: this.getWaveRemediationGuidance(error),
      });
    }

    // Process Wave alerts
    for (const alert of waveResult.categories.alert.items) {
      const elements = [];
      for (const selector of alert.selectors) {
        const element: ProcessedViolation['elements'][0] = {
          html: selector,
          target: selector,
          failureSummary: alert.description,
          selector: selector,
        };

        if (captureScreenshots) {
          try {
            const screenshot = await this.captureElementScreenshot(selector);
            if (screenshot) {
              element.screenshot = screenshot;
            }
          } catch (error) {
            // Screenshot failed, continue without it
          }
        }

        elements.push(element);
      }

      processedViolations.push({
        id: alert.id,
        impact: 'moderate',
        description: alert.description,
        help: alert.description,
        helpUrl: `https://wave.webaim.org/help#${alert.id}`,
        wcagTags: alert.wcag.map(w => w.toLowerCase()),
        wcagLevel: this.getWcagLevelFromWcagRefs(alert.wcag),
        occurrences: alert.count,
        tools: ['wave'],
        elements,
        scenarioRelevance: this.getScenarioRelevance(alert.id, alert.wcag),
        remediation: this.getWaveRemediationGuidance(alert),
      });
    }

    // Process Wave contrast issues
    for (const contrast of waveResult.categories.contrast.items) {
      const elements = [];
      for (const selector of contrast.selectors) {
        const element: ProcessedViolation['elements'][0] = {
          html: selector,
          target: selector,
          failureSummary: contrast.description,
          selector: selector,
        };

        if (captureScreenshots) {
          try {
            const screenshot = await this.captureElementScreenshot(selector);
            if (screenshot) {
              element.screenshot = screenshot;
            }
          } catch (error) {
            // Screenshot failed, continue without it
          }
        }

        elements.push(element);
      }

      processedViolations.push({
        id: contrast.id,
        impact: 'serious',
        description: contrast.description,
        help: contrast.description,
        helpUrl: `https://wave.webaim.org/help#${contrast.id}`,
        wcagTags: contrast.wcag.map(w => w.toLowerCase()),
        wcagLevel: this.getWcagLevelFromWcagRefs(contrast.wcag),
        occurrences: contrast.count,
        tools: ['wave'],
        elements,
        scenarioRelevance: ['visual-impairment', 'color-blind'],
        remediation: this.getWaveRemediationGuidance(contrast),
      });
    }

    return processedViolations;
  }

  /**
   * Processes Tenon results
   */
  private async processTenonResults(
    tenonResult: TenonResult,
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const processedViolations: ProcessedViolation[] = [];

    for (const issue of tenonResult.resultSet) {
      const element: ProcessedViolation['elements'][0] = {
        html: issue.snippet,
        target: issue.xpath,
        failureSummary: issue.errorDescription,
        selector: issue.xpath,
        xpath: issue.xpath,
      };

      if (captureScreenshots) {
        try {
          const screenshot = await this.captureElementScreenshot(issue.xpath);
          if (screenshot) {
            element.screenshot = screenshot;
          }
        } catch (error) {
          // Screenshot failed, continue without it
        }
      }

      processedViolations.push({
        id: `tenon-${issue.bpID}`,
        impact: this.mapTenonSeverityToImpact(issue.severity),
        description: issue.errorDescription,
        help: issue.errorTitle,
        helpUrl: issue.ref,
        wcagTags: issue.wcag.map(w => w.toLowerCase()),
        wcagLevel: this.getWcagLevelFromWcagRefs(issue.wcag),
        occurrences: 1,
        tools: ['tenon'],
        elements: [element],
        scenarioRelevance: this.getScenarioRelevanceFromTags(issue.tags),
        remediation: this.getTenonRemediationGuidance(issue),
      });
    }

    return processedViolations;
  }

  /**
   * Merges violations from multiple tools
   */
  private mergeViolationsFromMultipleTools(violations: ProcessedViolation[]): ProcessedViolation[] {
    const merged = new Map<string, ProcessedViolation>();

    for (const violation of violations) {
      const key = violation.id;

      if (merged.has(key)) {
        const existing = merged.get(key)!;
        existing.tools = [...new Set([...existing.tools, ...violation.tools])];
        existing.occurrences += violation.occurrences;
        existing.elements.push(...violation.elements);
      } else {
        merged.set(key, { ...violation });
      }
    }

    return Array.from(merged.values());
  }

  /**
   * Captures screenshot of an element
   */
  private async captureElementScreenshot(selector: string): Promise<string | null> {
    const config = this.config.getReportingConfiguration();

    try {
      const element = this.page.locator(selector).first();
      const screenshot = await element.screenshot({
        timeout: config.screenshotTimeout,
      });
      return screenshot.toString('base64');
    } catch (error) {
      return null;
    }
  }

  /**
   * Generates XPath for an element
   */
  private async generateXPath(element: any): Promise<string> {
    return await this.page.evaluate((el: Element) => {
      const getXPath = (element: Element): string => {
        if (element.id) {
          return `//*[@id='${element.id}']`;
        }

        if (element === document.body) {
          return '/html/body';
        }

        let ix = 0;
        const siblings = element.parentNode?.children || [];
        for (let i = 0; i < siblings.length; i++) {
          const sibling = siblings[i];
          if (sibling === element) {
            return `${getXPath(element.parentElement!)}/${element.tagName.toLowerCase()}[${ix + 1}]`;
          }
          if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
            ix++;
          }
        }
        return '';
      };

      return getXPath(el);
    }, element);
  }

  /**
   * Maps Pa11y type to impact level
   */
  private mapPa11yTypeToImpact(type: string): ProcessedViolation['impact'] {
    switch (type.toLowerCase()) {
      case 'error':
        return 'serious';
      case 'warning':
        return 'moderate';
      case 'notice':
        return 'minor';
      default:
        return 'moderate';
    }
  }

  /**
   * Extracts WCAG level from Pa11y code
   */
  private extractWcagLevelFromPa11y(code: string): ProcessedViolation['wcagLevel'] {
    if (code.includes('WCAG2AAA')) return 'AAA';
    if (code.includes('WCAG2AA')) return 'AA';
    if (code.includes('WCAG2A')) return 'A';
    return 'Unknown';
  }

  /**
   * Extracts WCAG tags from Pa11y code
   */
  private extractWcagTagsFromPa11y(code: string): string[] {
    const tags = [];
    if (code.includes('WCAG2A')) tags.push('wcag2a');
    if (code.includes('WCAG2AA')) tags.push('wcag2aa');
    if (code.includes('WCAG2AAA')) tags.push('wcag2aaa');
    return tags;
  }

  /**
   * Gets WCAG level from tags
   */
  private getWcagLevel(tags: string[]): ProcessedViolation['wcagLevel'] {
    if (tags.some(tag => tag.includes('wcag2aaa'))) return 'AAA';
    if (tags.some(tag => tag.includes('wcag2aa'))) return 'AA';
    if (tags.some(tag => tag.includes('wcag2a'))) return 'A';
    return 'Unknown';
  }

  /**
   * Gets scenario relevance for violations
   */
  private getScenarioRelevance(violationId: string, tags: string[]): string[] {
    const relevance = ['general'];

    if (violationId.includes('color') || tags.some(tag => tag.includes('color'))) {
      relevance.push('visual-impairment', 'color-blind');
    }

    if (violationId.includes('keyboard') || violationId.includes('focus')) {
      relevance.push('motor-impairment', 'keyboard-only');
    }

    if (violationId.includes('aria') || violationId.includes('label')) {
      relevance.push('screen-reader', 'cognitive-impairment');
    }

    return relevance;
  }

  /**
   * Gets remediation guidance for axe violations
   */
  private getRemediationGuidance(violation: AxeViolation): ProcessedViolation['remediation'] {
    const suggestions = [];

    // Add specific suggestions based on violation type
    if (violation.help) {
      suggestions.push(violation.help);
    }

    if (violation.nodes?.[0]?.all?.[0]?.message) {
      suggestions.push(violation.nodes[0].all[0].message);
    }

    return {
      priority:
        violation.impact === 'critical' || violation.impact === 'serious'
          ? 'High'
          : violation.impact === 'moderate'
            ? 'Medium'
            : 'Low',
      effort: violation.impact === 'critical' ? 'High' : 'Medium',
      suggestions,
      codeExample: this.generateCodeExample(violation),
    };
  }

  /**
   * Gets remediation guidance for Pa11y issues
   */
  private getRemediationGuidanceForPa11y(
    issue: Pa11yResult['issues'][0]
  ): ProcessedViolation['remediation'] {
    return {
      priority: issue.type === 'error' ? 'High' : issue.type === 'warning' ? 'Medium' : 'Low',
      effort: issue.type === 'error' ? 'High' : 'Medium',
      suggestions: [issue.message],
    };
  }

  /**
   * Generates code example for violations
   */
  private generateCodeExample(violation: AxeViolation): string | undefined {
    if (!violation.nodes?.[0]?.html) return undefined;

    const html = violation.nodes[0].html;

    // Generate improved code example based on violation type
    if (violation.id === 'color-contrast') {
      return `<!-- Ensure sufficient colour contrast -->\n${html.replace(/style="[^"]*"/g, 'style="color: #333; background: #fff;"')}`;
    }

    if (violation.id === 'image-alt') {
      return `<!-- Add descriptive alt text -->\n${html.replace(/alt="[^"]*"/g, 'alt="Descriptive text about the image"')}`;
    }

    if (violation.id === 'label') {
      return `<!-- Add proper label -->\n<label for="input-id">Label text</label>\n${html.replace(/<input/g, '<input id="input-id"')}`;
    }

    return html;
  }

  /**
   * Maps Tenon severity to impact level
   */
  private mapTenonSeverityToImpact(
    severity: 'low' | 'medium' | 'high' | 'critical'
  ): ProcessedViolation['impact'] {
    switch (severity) {
      case 'critical':
        return 'critical';
      case 'high':
        return 'serious';
      case 'medium':
        return 'moderate';
      case 'low':
        return 'minor';
      default:
        return 'moderate';
    }
  }

  /**
   * Gets WCAG level from WCAG references
   */
  private getWcagLevelFromWcagRefs(wcagRefs: string[]): ProcessedViolation['wcagLevel'] {
    for (const ref of wcagRefs) {
      const lowerRef = ref.toLowerCase();
      if (lowerRef.includes('aaa')) return 'AAA';
      if (lowerRef.includes('aa')) return 'AA';
      if (lowerRef.includes('a')) return 'A';
    }
    return 'Unknown';
  }

  /**
   * Gets scenario relevance from tags
   */
  private getScenarioRelevanceFromTags(tags: string[]): string[] {
    const relevance = ['general'];

    for (const tag of tags) {
      const lowerTag = tag.toLowerCase();
      if (lowerTag.includes('color') || lowerTag.includes('contrast')) {
        relevance.push('visual-impairment', 'color-blind');
      }
      if (lowerTag.includes('keyboard')) {
        relevance.push('motor-impairment', 'keyboard-only');
      }
      if (lowerTag.includes('aria') || lowerTag.includes('forms')) {
        relevance.push('screen-reader', 'cognitive-impairment');
      }
    }

    return [...new Set(relevance)];
  }

  /**
   * Gets remediation guidance for Wave violations
   */
  private getWaveRemediationGuidance(waveItem: any): ProcessedViolation['remediation'] {
    const suggestions = [waveItem.description];

    // Add specific suggestions based on Wave item type
    if (waveItem.id.includes('alt')) {
      suggestions.push('Provide descriptive alternative text for images');
    }
    if (waveItem.id.includes('contrast')) {
      suggestions.push('Increase color contrast to meet WCAG requirements');
    }
    if (waveItem.id.includes('label')) {
      suggestions.push('Add proper labels to form controls');
    }

    return {
      priority: 'High',
      effort: 'Medium',
      suggestions,
    };
  }

  /**
   * Gets remediation guidance for Tenon violations
   */
  private getTenonRemediationGuidance(tenonIssue: any): ProcessedViolation['remediation'] {
    const suggestions = [tenonIssue.errorTitle];

    // Add specific suggestions based on Tenon issue type
    if (tenonIssue.errorTitle.toLowerCase().includes('alt')) {
      suggestions.push('Add alternative text to images');
    }
    if (tenonIssue.errorTitle.toLowerCase().includes('contrast')) {
      suggestions.push('Improve color contrast ratios');
    }
    if (tenonIssue.errorTitle.toLowerCase().includes('label')) {
      suggestions.push('Associate labels with form controls');
    }

    return {
      priority:
        tenonIssue.severity === 'critical' || tenonIssue.severity === 'high' ? 'High' : 'Medium',
      effort: tenonIssue.certainty > 90 ? 'Low' : 'Medium',
      suggestions,
    };
  }
}
