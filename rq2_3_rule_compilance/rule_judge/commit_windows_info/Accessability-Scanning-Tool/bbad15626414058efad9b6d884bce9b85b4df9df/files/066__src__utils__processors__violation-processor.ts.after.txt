import { Page } from '@playwright/test';
import { AxeResults, Result as AxeViolation, NodeResult } from 'axe-core';
import { Pa11yResult } from '@/utils/runners/pa11y-test-runner';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ServiceResult, ViolationTarget } from '@/core/types/common';

// Extend NodeResult to include relatedNodes property
interface ExtendedNodeResult extends NodeResult {
  relatedNodes?: Array<{
    html: string;
    target: ViolationTarget;
  }>;
}

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
    target: ViolationTarget;
    failureSummary: string;
    screenshot?: string;
    selector: string;
    xpath?: string;
    boundingRect?: { x: number; y: number; width: number; height: number };
    relatedNodes?: Array<{
      html: string;
      target: ViolationTarget;
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
}

export class ViolationProcessor {
  private config = ConfigurationService.getInstance();
  private errorHandler = ErrorHandlerService.getInstance();

  constructor(private page: Page) { }

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
        if (!node) continue;
        const element: ProcessedViolation['elements'][0] = {
          html: node.html,
          // Fixed: Properly type the target based on axe-core NodeResult
          target: {
            selector: Array.isArray(node.target) ? node.target.join(', ') : String(node.target),
          },
          failureSummary: node.failureSummary || violation.description,
          selector: Array.isArray(node.target) ? node.target.join(', ') : String(node.target),
          relatedNodes: (node as ExtendedNodeResult).relatedNodes ?? [],
        };

        // Add XPath if available
        if (node.target && Array.isArray(node.target) && node.target.length > 0) {
          try {
            const targetElement = await this.page.locator(element.selector).first();
            if (targetElement) {
              element.xpath = await this.generateXPath(targetElement);
            }
          } catch (_error) {
            // XPath generation failed, continue without it
          }
        }

        // Add bounding rectangle
        try {
          const boundingRect = await this.page.locator(element.selector).first().boundingBox();
          if (boundingRect) {
            element.boundingRect = boundingRect;
          }
        } catch (_error) {
          // Bounding rect failed, continue without it
        }

        // Capture screenshot if requested
        if (captureScreenshots) {
          try {
            const screenshot = await this.captureElementScreenshot(element.selector);
            if (screenshot) {
              element.screenshot = screenshot;
            }
          } catch (_error) {
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
        // Fixed: Properly type the target for pa11y selector
        target: {
          selector: typeof issue.selector === 'string' ? issue.selector : '',
        },
        failureSummary: issue.message,
        selector: typeof issue.selector === 'string' ? issue.selector : '',
      };

      // Capture screenshot if requested
      if (captureScreenshots) {
        try {
          const screenshot = await this.captureElementScreenshot(issue.selector);
          if (screenshot) {
            element.screenshot = screenshot;
          }
        } catch (_error) {
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
   * Merges violations from multiple tools
   */
  private mergeViolationsFromMultipleTools(violations: ProcessedViolation[]): ProcessedViolation[] {
    const violationMap = new Map<string, ProcessedViolation>();

    for (const violation of violations) {
      const key = violation.id;

      const existing = violationMap.get(key);

      if (existing) {
        // Merge tools and browsers
        existing.tools = [...new Set([...existing.tools, ...violation.tools])];
        existing.browsers = [
          ...new Set([...(existing.browsers ?? []), ...(violation.browsers ?? [])]),
        ];

        // Increase occurrences
        existing.occurrences += violation.occurrences;

        // Merge elements if they are distinct
        for (const newElement of violation.elements) {
          if (!existing.elements.some(e => e.selector === newElement.selector)) {
            existing.elements.push(newElement);
          }
        }
      } else {
        violationMap.set(key, { ...violation });
      }
    }

    return Array.from(violationMap.values());
  }

  /**
   * Captures screenshot of an element
   */
  private async captureElementScreenshot(selector: string): Promise<string | null> {
    try {
      const element = this.page.locator(selector).first();
      const buffer = await element.screenshot();
      return buffer.toString('base64');
    } catch (_error) {
      this.errorHandler.logWarning(`Could not capture screenshot for selector: ${selector}`);
      return null;
    }
  }

  /**
   * Generates XPath for an element
   */
  private async generateXPath(element: {
    evaluate: (fn: (el: Element) => string) => Promise<string>;
  }): Promise<string> {
    try {
      const getXPath = (element: Element): string => {
        if (element.id) {
          return `id("${element.id}")`;
        }
        if (element.parentElement) {
          const siblings = Array.from(element.parentElement.children).filter(
            child => child.tagName === element.tagName
          );
          if (siblings.length > 1) {
            const index = siblings.indexOf(element) + 1;
            return `${getXPath(element.parentElement)}/${element.tagName.toLowerCase()}[${index}]`;
          }
          return `${getXPath(element.parentElement)}/${element.tagName.toLowerCase()}`;
        }
        return `/${element.tagName.toLowerCase()}`;
      };

      return await element.evaluate(getXPath);
    } catch (_error) {
      this.errorHandler.logWarning('Failed to generate XPath');
      return '';
    }
  }

  /**
   * Maps Pa11y type to impact level
   */
  private mapPa11yTypeToImpact(type: string): ProcessedViolation['impact'] {
    switch (type) {
      case 'error':
        return 'critical';
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
    const match = code.match(/WCAG2AA\.Principle\d\./);
    if (match) {
      return 'AA';
    }
    return 'Unknown';
  }

  /**
   * Extracts WCAG tags from Pa11y code
   */
  private extractWcagTagsFromPa11y(code: string): string[] {
    // Basic extraction, can be improved
    const parts = code.split('.');
    if (parts.length > 2 && parts[2]) {
      return [parts[2]];
    }
    return [];
  }

  /**
   * Gets WCAG level from tags
   */
  private getWcagLevel(tags: string[]): ProcessedViolation['wcagLevel'] {
    if (tags.includes('wcag21aaa') || tags.includes('wcag2aaa')) return 'AAA';
    if (tags.includes('wcag21aa') || tags.includes('wcag2aa')) return 'AA';
    if (tags.includes('wcag21a') || tags.includes('wcag2a')) return 'A';
    return 'Unknown';
  }

  /**
   * Gets scenario relevance for violations
   */
  private getScenarioRelevance(violationId: string, tags: string[]): string[] {
    const relevance: string[] = [];
    if (tags.includes('cat.keyboard')) relevance.push('Keyboard Navigation');
    if (tags.includes('cat.forms')) relevance.push('Forms');
    if (tags.includes('cat.color')) relevance.push('Color Contrast');
    if (violationId.startsWith('aria-')) relevance.push('ARIA Implementation');
    return relevance;
  }

  /**
   * Gets remediation guidance for axe violations
   */
  private getRemediationGuidance(violation: AxeViolation): ProcessedViolation['remediation'] {
    const priority =
      violation.impact === 'critical' || violation.impact === 'serious'
        ? 'High'
        : violation.impact === 'moderate'
          ? 'Medium'
          : 'Low';

    const effort = priority === 'High' ? 'High' : priority === 'Medium' ? 'Medium' : 'Low';

    const codeExample = this.generateCodeExample(violation);
    return {
      priority,
      effort,
      suggestions: [violation.help],
      ...(codeExample && { codeExample }),
    };
  }

  /**
   * Gets remediation guidance for Pa11y issues
   */
  private getRemediationGuidanceForPa11y(
    issue: Pa11yResult['issues'][0]
  ): ProcessedViolation['remediation'] {
    const priority = issue.type === 'error' ? 'High' : issue.type === 'warning' ? 'Medium' : 'Low';
    const effort = priority === 'High' ? 'High' : 'Medium';
    return {
      priority,
      effort,
      suggestions: [issue.message],
    };
  }

  /**
   * Generates code example for violations
   */
  private generateCodeExample(violation: AxeViolation): string | undefined {
    if (violation.id === 'color-contrast' && violation.nodes.length > 0) {
      const node = violation.nodes[0];
      if (node) {
        const failureSummary = node.failureSummary || '';
        const matches = failureSummary.match(/#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})/g);
        if (matches && matches.length >= 2) {
          return `/* Example CSS */\n.element {\n  color: ${matches[0]};\n  background-color: ${matches[1]};\n}`;
        }
      }
    }
    return undefined;
  }

  /**
   * Gets WCAG level from WCAG references
   */
  private getWcagLevelFromWcagRefs(wcagRefs: string[]): ProcessedViolation['wcagLevel'] {
    if (wcagRefs.some(ref => ref.includes('AAA'))) return 'AAA';
    if (wcagRefs.some(ref => ref.includes('AA'))) return 'AA';
    if (wcagRefs.some(ref => ref.includes('A'))) return 'A';
    return 'Unknown';
  }

  /**
   * Gets scenario relevance from tags
   */
  private getScenarioRelevanceFromTags(tags: string[]): string[] {
    const relevance: string[] = [];
    if (tags.includes('keyboard')) relevance.push('Keyboard Navigation');
    if (tags.includes('forms')) relevance.push('Forms');
    if (tags.includes('color')) relevance.push('Color Contrast');
    if (tags.includes('aria')) relevance.push('ARIA Implementation');
    return relevance;
  }
}
