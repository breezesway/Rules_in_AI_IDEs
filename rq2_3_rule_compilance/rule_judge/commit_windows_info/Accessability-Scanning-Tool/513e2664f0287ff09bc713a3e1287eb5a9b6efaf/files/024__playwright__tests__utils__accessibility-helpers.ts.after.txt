import { Page } from '@playwright/test';
import { AxeResults, Result as AxeViolation } from 'axe-core';
import AxeBuilder from '@axe-core/playwright';

export interface AccessibilityReport {
  url: string;
  timestamp: string;
  testSuite: string;
  browser?: string;
  viewport?: string;
  summary: {
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    wcagAAViolations: number;
    wcagAAAViolations: number;
  };
  violations: ProcessedViolation[];
  pageAnalysis: {
    title: string;
    headingStructure: Array<{ level: number; text: string; tagName: string }>;
    landmarks: { main: boolean; nav: boolean; footer: boolean };
    skipLink: { exists: boolean; isVisible: boolean; targetExists: boolean };
    images: Array<{ src: string; alt: string; hasAlt: boolean; ariaLabel?: string }>;
    links: Array<{ text: string; href: string; hasAriaLabel: boolean; ariaLabel?: string }>;
    forms: Array<{
      hasLabel: boolean;
      labelText: string;
      inputType: string;
      isRequired: boolean;
      hasAriaLabel: boolean;
    }>;
    keyboardNavigation: Array<{ element: string; canFocus: boolean; hasVisibleFocus: boolean }>;
    responsive?: { mobile: boolean; tablet: boolean; desktop: boolean };
  };
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
  browsers?: string[]; // List of browsers where this violation was found
  tools: string[]; // List of tools that found this violation (axe, pa11y, lighthouse)
  elements: Array<{
    html: string;
    target: any;
    failureSummary: string;
    screenshot?: string; // Base64 encoded screenshot
    selector: string; // CSS selector for the element
    xpath?: string; // XPath for the element
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

export interface SiteWideAccessibilityReport {
  siteUrl: string;
  timestamp: string;
  testSuite: string;
  summary: {
    totalPages: number;
    pagesWithViolations: number;
    totalViolations: number;
    criticalViolations: number;
    seriousViolations: number;
    moderateViolations: number;
    minorViolations: number;
    compliancePercentage: number;
    mostCommonViolations: Array<{
      id: string;
      affectedPages: number;
      totalOccurrences: number;
      impact: string;
      description: string;
    }>;
  };
  pageReports: AccessibilityReport[];
  violationsByType: Record<
    string,
    {
      count: number;
      pages: string[];
      impact: string;
      description: string;
      totalOccurrences: number;
      browsers: string[]; // List of browsers where this violation was found
      tools: string[]; // List of tools that detected this violation
    }
  >;
}

export class AccessibilityTestUtils {
  private page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * Creates a clickable terminal link using ANSI escape codes
   * @param text - The text to display
   * @param url - The URL or file path to link to
   * @param color - The color to apply to the link (default: magenta)
   * @returns Formatted clickable link
   */
  private createClickableLink(text: string, url: string, color: string = '\x1b[35m'): string {
    const reset = '\x1b[0m';
    // Convert file path to file:// URL for better compatibility
    const linkUrl = url.startsWith('/') ? `file://${url}` : url;

    // OSC 8 hyperlink format: \x1b]8;;URL\x1b\\TEXT\x1b]8;;\x1b\\
    return `${color}\x1b]8;;${linkUrl}\x1b\\${text}\x1b]8;;\x1b\\${reset}`;
  }

  async injectAxe(): Promise<void> {
    // AxeBuilder automatically injects axe, no separate injection needed
  }

  async runAxeAnalysis(options?: {
    include?: string[];
    exclude?: string[];
    tags?: string[];
    rules?: Record<string, { enabled: boolean }>;
  }): Promise<AxeResults> {
    let axeBuilder = new AxeBuilder({ page: this.page });

    if (options?.tags) {
      axeBuilder = axeBuilder.withTags(options.tags);
    } else {
      // Comprehensive tag set for maximum coverage
      axeBuilder = axeBuilder.withTags([
        'wcag2a',
        'wcag2aa',
        'wcag21aa',
        'wcag22aa', // WCAG standards
        'best-practice', // Best practices
        'experimental', // Include experimental rules for comprehensive coverage
      ]);
    }

    if (options?.include) {
      axeBuilder = axeBuilder.include(options.include);
    }

    if (options?.exclude) {
      axeBuilder = axeBuilder.exclude(options.exclude);
    }

    if (options?.rules) {
      Object.entries(options.rules).forEach(([ruleId, config]) => {
        if (config.enabled) {
          axeBuilder = axeBuilder.withRules([ruleId]);
        } else {
          axeBuilder = axeBuilder.disableRules([ruleId]);
        }
      });
    }

    return await axeBuilder.analyze();
  }

  async runPa11yAnalysis(): Promise<any> {
    console.log('🔍 Starting Pa11y analysis...');

    const startTime = Date.now();
    let pa11yResults = null;

    try {
      // Get current page URL for context
      const currentUrl = this.page.url();
      console.log(`   📄 Analyzing: ${currentUrl}`);

      // Configure Pa11y with optimised settings
      const pa11y = require('pa11y');

      // Create a more robust Pa11y configuration
      const pa11yOptions = {
        standard: 'WCAG2AA',
        includeNotices: true,
        includeWarnings: true,
        timeout: 30000, // 30 second timeout
        wait: 2000, // Wait 2 seconds for page to settle
        chromeLaunchConfig: {
          args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-translate',
            '--memory-pressure-off',
            '--max_old_space_size=2048',
            '--single-process',
          ],
        },
        // Let Pa11y manage its own browser instance instead of reusing Playwright page
        actions: [],
        hideElements: '',
        ignore: [],
        ignoreUrl: false,
        rootElement: null,
        rules: [],
        runners: ['htmlcs'],
        userAgent: 'pa11y/accessibility-audit',
        viewport: {
          width: 1280,
          height: 720,
        },
      };

      // Run Pa11y analysis with timeout protection
      pa11yResults = await Promise.race([
        pa11y(currentUrl, pa11yOptions),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Pa11y analysis timeout')), 60000)
        ),
      ]);

      const duration = Date.now() - startTime;
      console.log(`   ⏱️  Pa11y analysis completed in ${duration}ms`);

      if (pa11yResults && pa11yResults.issues) {
        console.log(`   📋 Pa11y found ${pa11yResults.issues.length} issues`);

        // Filter out notices if we have too many issues to keep output focused
        if (pa11yResults.issues.length > 500) {
          const originalCount = pa11yResults.issues.length;
          pa11yResults.issues = pa11yResults.issues.filter((issue: any) => issue.type !== 'notice');
          console.log(
            `   🔧 Filtered ${originalCount - pa11yResults.issues.length} notices to focus on actionable issues`
          );
        }

        // Log issue breakdown
        const issuesByType = pa11yResults.issues.reduce((acc: any, issue: any) => {
          acc[issue.type] = (acc[issue.type] || 0) + 1;
          return acc;
        }, {});

        console.log('   📊 Issue breakdown:', issuesByType);
      } else {
        console.log('   ✅ Pa11y completed with no issues');
      }
    } catch (error) {
      const duration = Date.now() - startTime;
      const errorMessage = error instanceof Error ? error.message : String(error);

      console.error(`   ❌ Pa11y analysis failed after ${duration}ms:`, errorMessage);

      // Return a safe error result instead of throwing
      return {
        issues: [],
        documentTitle: '',
        pageUrl: this.page.url(),
        error: errorMessage,
        duration,
      };
    }

    return (
      pa11yResults || {
        issues: [],
        documentTitle: '',
        pageUrl: this.page.url(),
      }
    );
  }

  async runLighthouseAccessibilityAnalysis(): Promise<any> {
    try {
      const { playAudit } = await import('playwright-lighthouse');

      console.log('🔍 Running Lighthouse accessibility audit...');

      const config = this.configService.getLighthouseConfiguration();

      // Use playwright-lighthouse for seamless integration
      const lighthouseResults = await playAudit({
        page: this.page,
        thresholds: {
          accessibility: 90, // WCAG 2.1 AAA compliance threshold
          'best-practices': 85,
          performance: 70,
          seo: 80,
        },
        config: {
          extends: 'lighthouse:default',
          settings: {
            onlyCategories: ['accessibility', 'best-practices'],
            emulatedFormFactor: 'desktop',
            throttling: {
              rttMs: 40,
              throughputKbps: 10240,
              cpuSlowdownMultiplier: 1,
            },
          },
        },
        port: config.port,
        // Don't fail the test if thresholds aren't met - we'll handle results ourselves
        ignoreError: true,
      });

      console.log('✅ Lighthouse accessibility audit completed');
      return lighthouseResults;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      console.warn('⚠️  Lighthouse accessibility analysis failed:', errorMessage);
      console.warn('   Continuing with axe-core and Pa11y analysis...');
      return {};
    }
  }

  async runComprehensiveAnalysis(): Promise<{
    axe: AxeResults | null;
    pa11y: any;
    lighthouse: any;
  }> {
    console.log('🔍 Running comprehensive accessibility analysis with multiple tools...');

    // Run all tools in parallel for efficiency
    const [axeResults, pa11yResults, lighthouseResults] = await Promise.all([
      this.runAxeAnalysis().catch(error => {
        console.warn('Axe analysis failed:', error.message);
        return null;
      }),
      this.runPa11yAnalysis(),
      this.runLighthouseAccessibilityAnalysis(),
    ]);

    console.log(`✅ Axe: ${axeResults?.violations?.length || 0} violations`);
    console.log(`✅ Pa11y: ${pa11yResults.issues?.length || 0} issues`);
    console.log(`✅ Lighthouse: ${Object.keys(lighthouseResults).length} audits`);

    return {
      axe: axeResults,
      pa11y: pa11yResults,
      lighthouse: lighthouseResults,
    };
  }

  async processMultiToolViolations(
    results: {
      axe: AxeResults | null;
      pa11y: any;
      lighthouse: any;
    },
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const allViolations: ProcessedViolation[] = [];

    // Process Axe violations
    if (results.axe?.violations) {
      const axeViolations = await this.processViolations(
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

    // Merge violations with the same ID from different tools
    return this.mergeViolationsFromMultipleTools(allViolations);
  }

  async processPa11yIssues(
    issues: any[],
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    // Process ALL Pa11y issues for comprehensive coverage (prioritize completeness over speed)
    const filteredIssues = issues.filter(
      issue => issue.type === 'error' || issue.type === 'warning' || issue.type === 'notice'
    ); // Keep all issue types

    console.log(
      `🔍 Pa11y: Processing ${filteredIssues.length} issues for comprehensive coverage (${issues.length} total found, including notices)`
    );

    return Promise.all(
      filteredIssues.map(async issue => {
        // Convert Pa11y issue to our format
        const wcagLevel = this.extractWcagLevelFromPa11y(issue.code);
        const impact = this.mapPa11yTypeToImpact(issue.type);

        // Create element information
        const selector = issue.selector || 'unknown';
        let screenshot: string | undefined;
        let boundingRect: { x: number; y: number; width: number; height: number } | undefined;

        // Capture screenshots for ALL violations to provide comprehensive visual context
        if (captureScreenshots && selector !== 'unknown') {
          try {
            const element = await this.page.locator(selector).first();
            const box = await element.boundingBox().catch(() => null);
            if (box) {
              boundingRect = box;
              const screenshotBuffer = await element
                .screenshot({
                  type: 'png',
                  timeout: 10000, // Increased timeout for comprehensive coverage
                })
                .catch(() => null);
              if (screenshotBuffer) {
                screenshot = screenshotBuffer.toString('base64');
              }
            }
          } catch {
            // Screenshot failed, continue without it
          }
        }

        return {
          id: issue.code,
          impact,
          description: issue.message,
          help: issue.message,
          helpUrl: `https://webaim.org/standards/wcag/checklist`,
          wcagTags: this.extractWcagTagsFromPa11y(issue.code),
          wcagLevel,
          occurrences: 1,
          tools: ['pa11y'],
          elements: [
            {
              html: issue.context || '',
              target: selector,
              failureSummary: issue.message,
              selector,
              screenshot,
              boundingRect,
              relatedNodes: [],
            },
          ],
          scenarioRelevance: this.getScenarioRelevance(issue.code, []),
          remediation: this.getRemediationGuidanceForPa11y(issue),
        };
      })
    );
  }

  private async processLighthouseAudits(
    audits: any,
    _captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    const violations: ProcessedViolation[] = [];

    for (const [auditId, audit] of Object.entries(audits as Record<string, any>)) {
      if (audit.score !== null && audit.score < 1) {
        // This is a failing audit
        const violation: ProcessedViolation = {
          id: auditId,
          impact: audit.score === 0 ? 'serious' : 'moderate',
          description: audit.title || auditId,
          help: audit.description || audit.title || auditId,
          helpUrl: audit.helpText || 'https://web.dev/lighthouse-accessibility/',
          wcagTags: [],
          wcagLevel: 'AA',
          occurrences: 1,
          tools: ['lighthouse'],
          elements: [
            {
              html: '',
              target: 'page',
              failureSummary: audit.description || 'Lighthouse accessibility audit failed',
              selector: 'html',
              relatedNodes: [],
            },
          ],
          scenarioRelevance: [],
          remediation: {
            priority: audit.score === 0 ? 'High' : 'Medium',
            effort: 'Medium',
            suggestions: [audit.description || 'See Lighthouse documentation'],
            codeExample: '',
          },
        };

        violations.push(violation);
      }
    }

    return violations;
  }

  private mergeViolationsFromMultipleTools(violations: ProcessedViolation[]): ProcessedViolation[] {
    const violationMap = new Map<string, ProcessedViolation>();

    violations.forEach(violation => {
      if (violationMap.has(violation.id)) {
        const existing = violationMap.get(violation.id)!;
        // Merge tools
        existing.tools = [...new Set([...existing.tools, ...violation.tools])];
        // Merge elements
        existing.elements.push(...violation.elements);
        // Update occurrences
        existing.occurrences += violation.occurrences;
      } else {
        violationMap.set(violation.id, violation);
      }
    });

    return Array.from(violationMap.values());
  }

  private extractWcagLevelFromPa11y(code: string): 'A' | 'AA' | 'AAA' | 'Unknown' {
    if (code.includes('WCAG2A')) return 'A';
    if (code.includes('WCAG2AA')) return 'AA';
    if (code.includes('WCAG2AAA')) return 'AAA';
    return 'AA'; // Default assumption
  }

  private mapPa11yTypeToImpact(type: string): 'minor' | 'moderate' | 'serious' | 'critical' {
    switch (type) {
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

  private extractWcagTagsFromPa11y(code: string): string[] {
    // Extract WCAG references from Pa11y codes
    const wcagMatches = code.match(/WCAG2A{1,3}/g) || [];
    return wcagMatches;
  }

  private getRemediationGuidanceForPa11y(issue: any): ProcessedViolation['remediation'] {
    return {
      priority: issue.type === 'error' ? 'High' : 'Medium',
      effort: 'Medium',
      suggestions: [issue.message || 'See Pa11y documentation for details'],
      codeExample: '',
    };
  }

  async checkColorContrast(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.color'],
      rules: {
        'color-contrast': { enabled: true },
        'color-contrast-enhanced': { enabled: true },
      },
    });
  }

  async checkKeyboardAccessibility(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.keyboard'],
      rules: {
        'focusable-content': { enabled: true },
        'focus-order-semantics': { enabled: true },
        tabindex: { enabled: true },
      },
    });
  }

  async checkAriaImplementation(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.aria'],
      rules: {
        'aria-valid-attr': { enabled: true },
        'aria-valid-attr-value': { enabled: true },
        'aria-required-attr': { enabled: true },
        'aria-roles': { enabled: true },
        'aria-labelledby': { enabled: true },
      },
    });
  }

  async checkFormAccessibility(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.forms'],
      rules: {
        label: { enabled: true },
        'form-field-multiple-labels': { enabled: true },
        fieldset: { enabled: true },
      },
    });
  }

  async checkImageAccessibility(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.text-alternatives'],
      rules: {
        'image-alt': { enabled: true },
        'image-redundant-alt': { enabled: true },
        'object-alt': { enabled: true },
      },
    });
  }

  async checkLandmarksAndHeadings(): Promise<AxeResults> {
    return await this.runAxeAnalysis({
      tags: ['cat.structure'],
      rules: {
        'landmark-one-main': { enabled: true },
        'landmark-main-is-top-level': { enabled: true },
        'landmark-no-duplicate-banner': { enabled: true },
        'landmark-no-duplicate-contentinfo': { enabled: true },
        'heading-order': { enabled: true },
        'empty-heading': { enabled: true },
      },
    });
  }

  async processViolations(
    violations: AxeViolation[],
    captureScreenshots: boolean = true
  ): Promise<ProcessedViolation[]> {
    return Promise.all(
      violations.map(async violation => {
        const wcagLevel = this.getWcagLevel(violation.tags);
        const scenarioRelevance = this.getScenarioRelevance(violation.id, violation.tags);
        const remediation = this.getRemediationGuidance(violation);

        // Process elements with enhanced information
        const elements = await Promise.all(
          violation.nodes.map(async node => {
            const selector = Array.isArray(node.target)
              ? node.target.join(' ')
              : String(node.target);

            // Enhanced element data
            let screenshot: string | undefined;
            let boundingRect: { x: number; y: number; width: number; height: number } | undefined;
            let xpath: string | undefined;

            if (captureScreenshots) {
              try {
                // Find element for additional information
                const element = await this.page.locator(selector).first();

                // Get bounding box
                const box = await element.boundingBox().catch(() => null);
                if (box) {
                  boundingRect = box;

                  // Capture screenshot of the element
                  const screenshotBuffer = await element
                    .screenshot({
                      type: 'png',
                      timeout: 5000,
                    })
                    .catch(() => null);

                  if (screenshotBuffer) {
                    screenshot = screenshotBuffer.toString('base64');
                  }
                }

                // Generate XPath
                xpath = await element
                  .evaluate(el => {
                    const getXPath = (element: Element): string => {
                      if (element.id !== '') {
                        return `//*[@id="${element.id}"]`;
                      }
                      if (element === document.body) {
                        return '/html/body';
                      }

                      let ix = 0;
                      const siblings = element.parentNode?.children || [];
                      for (let i = 0; i < siblings.length; i++) {
                        const sibling = siblings[i];
                        if (sibling === element) {
                          const tagName = element.tagName.toLowerCase();
                          return `${getXPath(element.parentElement!)}/${tagName}[${ix + 1}]`;
                        }
                        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                          ix++;
                        }
                      }
                      return '';
                    };
                    return getXPath(el);
                  })
                  .catch(() => undefined);
              } catch (error) {
                console.warn(`Could not capture enhanced data for element: ${selector}`, error);
              }
            }

            return {
              html: node.html,
              target: node.target,
              failureSummary: node.failureSummary || '',
              selector,
              screenshot,
              xpath,
              boundingRect,
              relatedNodes: (node as any).relatedNodes?.map((relatedNode: any) => ({
                html: relatedNode.html,
                target: relatedNode.target,
              })),
            };
          })
        );

        return {
          id: violation.id,
          impact: violation.impact as 'minor' | 'moderate' | 'serious' | 'critical',
          description: violation.description,
          help: violation.help,
          helpUrl: violation.helpUrl,
          wcagTags: violation.tags.filter(tag => tag.startsWith('wcag')),
          wcagLevel,
          occurrences: violation.nodes.length,
          tools: ['axe-core'], // Default to axe-core for existing violations
          elements,
          scenarioRelevance,
          remediation,
        };
      })
    );
  }

  private getWcagLevel(tags: string[]): 'A' | 'AA' | 'AAA' | 'Unknown' {
    if (tags.includes('wcag111') || tags.includes('wcag2a')) return 'A';
    if (tags.includes('wcag21aa') || tags.includes('wcag2aa')) return 'AA';
    if (tags.includes('wcag21aaa') || tags.includes('wcag2aaa')) return 'AAA';
    return 'Unknown';
  }

  private getScenarioRelevance(violationId: string, tags: string[]): string[] {
    const relevantScenarios: string[] = [];

    // Map violations to feature file scenarios
    const scenarioMap: Record<string, string[]> = {
      'color-contrast': ['Colour contrast meets WCAG AA standards'],
      'heading-order': ['Headings provide proper content structure'],
      'image-alt': ['Images have proper alternative text'],
      label: ['Forms are accessible and properly labeled'],
      'link-name': ['Links are accessible and descriptive'],
      'landmark-one-main': ['Page has proper document structure'],
      'focus-order-semantics': ['Navigation is keyboard accessible'],
      'aria-valid-attr': ['ARIA attributes are properly implemented'],
      'skip-link': ['Page has proper document structure'],
      tabindex: ['Navigation is keyboard accessible'],
      'form-field-multiple-labels': ['Forms are accessible and properly labeled'],
      'duplicate-id': ['Overall WCAG 2.1 AA compliance'],
      'html-has-lang': ['Overall WCAG 2.1 AA compliance'],
      'page-has-heading-one': ['Headings provide proper content structure'],
      region: ['Page has proper document structure'],
    };

    if (scenarioMap[violationId]) {
      relevantScenarios.push(...scenarioMap[violationId]);
    }

    // Add category-based scenarios
    if (tags.includes('cat.keyboard')) {
      relevantScenarios.push('Navigation is keyboard accessible');
    }
    if (tags.includes('cat.aria')) {
      relevantScenarios.push('ARIA attributes are properly implemented');
    }
    if (tags.includes('cat.forms')) {
      relevantScenarios.push('Forms are accessible and properly labeled');
    }
    if (tags.includes('cat.structure')) {
      relevantScenarios.push('Page has proper document structure');
    }
    if (tags.includes('cat.color')) {
      relevantScenarios.push('Colour contrast meets WCAG AA standards');
    }

    return [...new Set(relevantScenarios)]; // Remove duplicates
  }

  private getRemediationGuidance(violation: AxeViolation): ProcessedViolation['remediation'] {
    const remediationMap: Record<string, ProcessedViolation['remediation']> = {
      'color-contrast': {
        priority: 'High',
        effort: 'Low',
        suggestions: [
          'Increase colour contrast to meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)',
          'Use colour contrast checking tools to verify compliance',
          'Consider using darker colours for text or lighter background colours',
        ],
        codeExample: `/* Example: Improve text contrast with brand colours */
.text-element {
  color: #1e214d; /* Key Purple - brand colour */
  background-color: #ffffff; /* Light background */
  /* This provides approximately 8.5:1 contrast ratio - exceeds WCAG AA */
}

/* Alternative brand colour combinations */
.button-primary {
  color: #ffffff; /* White text */
  background-color: #db0064; /* Magenta - brand colour */
  /* Contrast ratio: 5.8:1 - exceeds WCAG AA */
}

.warning-text {
  color: #1e214d; /* Key Purple for readability */
  background-color: #fcc700; /* Yellow - brand colour */
  /* Contrast ratio: 6.2:1 - exceeds WCAG AA */
}`,
      },
      'heading-order': {
        priority: 'Medium',
        effort: 'Medium',
        suggestions: [
          'Ensure headings follow logical order (h1 → h2 → h3)',
          'Use only one h1 per page',
          'Do not skip heading levels',
          'Use headings to structure content, not for styling',
        ],
        codeExample: `<!-- Correct heading structure -->
<h1>Main Page Title</h1>
<h2>Section Title</h2>
<h3>Subsection Title</h3>
<h3>Another Subsection</h3>
<h2>Next Section</h2>`,
      },
      'image-alt': {
        priority: 'High',
        effort: 'Low',
        suggestions: [
          'Add descriptive alt text to all informative images',
          'Use empty alt="" for decorative images',
          'Ensure alt text conveys the same information as the image',
          'Avoid redundant phrases like "image of" or "picture of"',
        ],
        codeExample: `<!-- Good alt text examples -->
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2 2024">
<img src="decoration.png" alt="" role="presentation">
<img src="logo.png" alt="Company Name">`,
      },
      label: {
        priority: 'High',
        effort: 'Low',
        suggestions: [
          'Associate labels with form controls using "for" attribute',
          'Use aria-label for controls without visible labels',
          'Ensure labels are descriptive and clear',
          'Group related form fields with fieldset and legend',
        ],
        codeExample: `<!-- Proper form labeling -->
<label for="email">Email Address</label>
<input type="email" id="email" required>

<fieldset>
  <legend>Contact Preferences</legend>
  <input type="checkbox" id="newsletter">
  <label for="newsletter">Subscribe to newsletter</label>
</fieldset>`,
      },
      'link-name': {
        priority: 'Medium',
        effort: 'Low',
        suggestions: [
          'Ensure link text clearly describes the destination or purpose',
          'Avoid generic text like "click here" or "read more"',
          'Use aria-label for additional context when needed',
          'Make link text meaningful out of context',
        ],
        codeExample: `<!-- Good link examples -->
<a href="/services">Our Services</a>
<a href="/report.pdf">Download Annual Report (PDF, 2MB)</a>
<a href="/contact" aria-label="Contact us for more information">Contact Us</a>`,
      },
    };

    return (
      remediationMap[violation.id] || {
        priority: 'Medium',
        effort: 'Medium',
        suggestions: [
          'Review the violation details and WCAG guidelines',
          'Test with assistive technologies',
          'Consult accessibility documentation for specific guidance',
        ],
      }
    );
  }

  createSummary(violations: ProcessedViolation[]): AccessibilityReport['summary'] {
    const summary = {
      totalViolations: violations.length,
      criticalViolations: 0,
      seriousViolations: 0,
      moderateViolations: 0,
      minorViolations: 0,
      wcagAAViolations: 0,
      wcagAAAViolations: 0,
    };

    violations.forEach(violation => {
      switch (violation.impact) {
        case 'critical':
          summary.criticalViolations++;
          break;
        case 'serious':
          summary.seriousViolations++;
          break;
        case 'moderate':
          summary.moderateViolations++;
          break;
        case 'minor':
          summary.minorViolations++;
          break;
      }

      if (violation.wcagLevel === 'AA') {
        summary.wcagAAViolations++;
      } else if (violation.wcagLevel === 'AAA') {
        summary.wcagAAAViolations++;
      }
    });

    return summary;
  }

  async generateAccessibilityReport(
    url: string,
    testSuite: string,
    pageAnalysis: AccessibilityReport['pageAnalysis'],
    browser: string = 'chromium',
    viewport: string = 'Desktop'
  ): Promise<AccessibilityReport> {
    // Run comprehensive analysis with multiple tools
    const comprehensiveResults = await this.runComprehensiveAnalysis();
    const processedViolations = await this.processMultiToolViolations(comprehensiveResults);
    const summary = this.createSummary(processedViolations);

    return {
      url,
      timestamp: new Date().toISOString(),
      testSuite,
      browser,
      viewport,
      summary,
      violations: processedViolations,
      pageAnalysis,
    };
  }

  async saveReportToFile(report: AccessibilityReport, filename: string): Promise<void> {
    const fs = require('fs');
    const path = require('path');

    // Ensure reports directory exists
    const reportsDir = path.join(process.cwd(), 'playwright', 'accessibility-reports');
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }

    // Clean up old reports (keep only the latest)
    this.cleanupOldReports(reportsDir);

    // Only save Gemini JSON report (most useful format)
    const jsonPath = path.join(reportsDir, `${filename}.json`);

    // Create and save report (JSON only, no PDF generation here)
    const accessibilityReporter = new (require('./accessibility-reporter').AccessibilityReporter)(
      report
    );
    const reportData = accessibilityReporter.generateReport();
    fs.writeFileSync(jsonPath, JSON.stringify(reportData, null, 2));

    console.log(`JSON report saved to: ${jsonPath}`);
  }

  private cleanupOldReports(reportsDir: string): void {
    const fs = require('fs');
    const path = require('path');

    try {
      const files = fs.readdirSync(reportsDir);

      // Filter accessibility report files (both old and new naming conventions)
      const reportFiles = files.filter((file: string) => {
        // Keep the existing "Accessibility Report.pdf" but clean up generated reports
        if (file === 'Accessibility Report.pdf') {
          return false;
        }

        // Clean up both old and new report formats
        const isOldFormat =
          file.startsWith('nimble-approach-accessibility-') ||
          file.startsWith('specific-pages-accessibility-');

        const isPreviousFormat =
          file.startsWith('comprehensive-site-audit-') ||
          file.startsWith('site-wide-accessibility-') ||
          file.startsWith('parallel-comprehensive-audit-');

        const isNewFormat =
          file.includes('-accessibility-report-') &&
          (file.endsWith('.json') || file.endsWith('.pdf') || file.endsWith('.txt'));

        return (
          (isOldFormat || isPreviousFormat || isNewFormat) &&
          (file.endsWith('.json') || file.endsWith('.pdf') || file.endsWith('.txt'))
        );
      });

      // Remove old report files
      reportFiles.forEach((file: string) => {
        const filePath = path.join(reportsDir, file);
        fs.unlinkSync(filePath);
        console.log(`🧹 Cleaned up old report: ${file}`);
      });

      if (reportFiles.length > 0) {
        console.log(`🧹 Cleaned up ${reportFiles.length} old accessibility reports`);
      }
    } catch (error) {
      console.warn('Warning: Could not clean up old reports:', error);
    }
  }

  private generateReadableReport(report: AccessibilityReport): string {
    let content = `ACCESSIBILITY REPORT FOR ${report.url}\n`;
    content += `Generated: ${report.timestamp}\n`;
    content += `Test Suite: ${report.testSuite}\n`;
    content += `\n${'='.repeat(80)}\n\n`;

    // Summary
    content += `SUMMARY\n`;
    content += `${'='.repeat(80)}\n`;
    content += `Total Violations: ${report.summary.totalViolations}\n`;
    content += `Critical: ${report.summary.criticalViolations}\n`;
    content += `Serious: ${report.summary.seriousViolations}\n`;
    content += `Moderate: ${report.summary.moderateViolations}\n`;
    content += `Minor: ${report.summary.minorViolations}\n`;
    content += `WCAG AA Violations: ${report.summary.wcagAAViolations}\n`;
    content += `WCAG AAA Violations: ${report.summary.wcagAAAViolations}\n\n`;

    // Violations
    content += `VIOLATIONS\n`;
    content += `${'='.repeat(80)}\n`;

    report.violations.forEach((violation, index) => {
      content += `${index + 1}. ${violation.id.toUpperCase()} [${violation.impact.toUpperCase()}]\n`;
      content += `   Description: ${violation.description}\n`;
      content += `   Help: ${violation.help}\n`;
      content += `   WCAG Level: ${violation.wcagLevel}\n`;
      content += `   Occurrences: ${violation.occurrences}\n`;
      content += `   Priority: ${violation.remediation.priority}\n`;
      content += `   Effort: ${violation.remediation.effort}\n`;
      content += `   Scenarios: ${violation.scenarioRelevance.join(', ')}\n`;
      content += `   Suggestions:\n`;
      violation.remediation.suggestions.forEach(suggestion => {
        content += `     - ${suggestion}\n`;
      });
      content += `\n`;
    });

    return content;
  }

  async generateComprehensiveReports(
    url: string,
    testSuite: string,
    pageAnalysis: AccessibilityReport['pageAnalysis'],
    filename: string,
    generatePdf: boolean = true
  ): Promise<void> {
    const report = await this.generateAccessibilityReport(url, testSuite, pageAnalysis);

    // Generate all report formats including PDF
    const { AccessibilityReporter } = require('./accessibility-reporter');
    const accessibilityReporter = new AccessibilityReporter(report, this.page);

    await accessibilityReporter.saveReport(filename, generatePdf);

    if (generatePdf) {
      console.log(
        `\n📄 **PDF Report Available**: Check the accessibility-reports folder for the comprehensive PDF report.`
      );
      console.log(
        `   This report includes charts, graphs, and detailed formatting perfect for stakeholder presentations.`
      );
    }
  }

  // Multi-page testing support with smart redirect handling
  async testMultiplePagesWithRedirectHandling(
    urls: string[],
    testSuite: string,
    options: {
      maxConcurrency?: number;
      delayBetweenPages?: number;
      skipErrors?: boolean;
      handleRedirects?: boolean;
    } = {}
  ): Promise<AccessibilityReport[]> {
    const {
      maxConcurrency = 3,
      delayBetweenPages = 1000,
      skipErrors = true,
      handleRedirects = false,
    } = options;
    const reports: AccessibilityReport[] = [];
    const testedUrls = new Set<string>(); // Track which URLs have been tested

    console.log(`🧪 Testing ${urls.length} pages for accessibility...`);
    console.log(`⚙️  Max concurrency: ${maxConcurrency}, Delay: ${delayBetweenPages}ms`);
    if (handleRedirects) {
      console.log(`🔄 Smart redirect handling enabled - skipping duplicate URLs`);
    }

    // Process pages in batches to avoid overwhelming the server
    for (let i = 0; i < urls.length; i += maxConcurrency) {
      const batch = urls.slice(i, i + maxConcurrency);
      const batchPromises = batch.map(async (url, index) => {
        try {
          // Skip if this exact URL has already been tested
          if (handleRedirects && testedUrls.has(url)) {
            console.log(`⏭️  Skipping ${url} (already tested)`);
            return null;
          }

          console.log(`📄 Testing page ${i + index + 1}/${urls.length}: ${url}`);

          // Navigate to the page with better error handling
          await this.page.goto(url, {
            waitUntil: 'domcontentloaded', // Less strict than networkidle
            timeout: 30000, // Balanced timeout
          });

          // Wait for page to stabilize
          await this.page.waitForTimeout(500);

          // Check if we were redirected and update URL
          const finalUrl = this.page.url();
          if (finalUrl !== url) {
            console.log(`📍 Page redirected from ${url} to ${finalUrl}`);

            // If redirect handling is enabled, check if we've already tested the final URL
            if (handleRedirects && testedUrls.has(finalUrl)) {
              console.log(`⏭️  Skipping redirected URL ${finalUrl} (already tested)`);
              testedUrls.add(url); // Mark original URL as processed
              return null;
            }
          }

          // Mark both original and final URLs as tested
          if (handleRedirects) {
            testedUrls.add(url);
            testedUrls.add(finalUrl);
          }

          await this.injectAxe();

          // Gather page analysis with error handling
          let pageAnalysis;
          try {
            pageAnalysis = await this.gatherPageAnalysis();
          } catch {
            console.warn(`⚠️  Page analysis failed for ${finalUrl}, using minimal analysis`);
            pageAnalysis = {
              title: await this.page.title().catch(() => 'Unknown'),
              headingStructure: [],
              landmarks: { main: false, nav: false, footer: false },
              skipLink: { exists: false, isVisible: false, targetExists: false },
              images: [],
              links: [],
              forms: [],
              keyboardNavigation: [],
              responsive: { mobile: false, tablet: false, desktop: false },
            };
          }

          // Generate accessibility report (use final URL after any redirects)
          const report = await this.generateAccessibilityReport(finalUrl, testSuite, pageAnalysis);

          return report;
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : String(error);
          console.error(`❌ Error testing ${url}:`, errorMessage);

          if (!skipErrors) {
            throw error;
          }

          // Return minimal error report
          return {
            url,
            timestamp: new Date().toISOString(),
            testSuite,
            summary: {
              totalViolations: 0,
              criticalViolations: 0,
              seriousViolations: 0,
              moderateViolations: 0,
              minorViolations: 0,
              wcagAAViolations: 0,
              wcagAAAViolations: 0,
            },
            violations: [],
            pageAnalysis: {
              title: `Error loading page: ${errorMessage}`,
              headingStructure: [],
              landmarks: { main: false, nav: false, footer: false },
              skipLink: { exists: false, isVisible: false, targetExists: false },
              images: [],
              links: [],
              forms: [],
              keyboardNavigation: [],
              responsive: { mobile: false, tablet: false, desktop: false },
            },
          } as AccessibilityReport;
        }
      });

      const batchReports = await Promise.all(batchPromises);
      // Filter out null results from skipped pages
      const validReports = batchReports.filter(report => report !== null) as AccessibilityReport[];
      reports.push(...validReports);

      // Delay between batches to be respectful to the server
      if (i + maxConcurrency < urls.length && delayBetweenPages > 0) {
        await new Promise(resolve => setTimeout(resolve, delayBetweenPages));
      }
    }

    const uniqueTestedUrls = handleRedirects ? testedUrls.size : reports.length;
    console.log(`✅ Completed testing ${reports.length} pages (${uniqueTestedUrls} unique URLs)`);

    if (handleRedirects) {
      const skippedCount = urls.length - reports.length;
      if (skippedCount > 0) {
        console.log(`⏭️  Skipped ${skippedCount} pages due to redirects to already-tested URLs`);
      }
    }

    return reports;
  }

  // Multi-page testing support (legacy method for backward compatibility)
  async testMultiplePages(
    urls: string[],
    testSuite: string,
    options: {
      maxConcurrency?: number;
      delayBetweenPages?: number;
      skipErrors?: boolean;
    } = {}
  ): Promise<AccessibilityReport[]> {
    const { maxConcurrency = 3, delayBetweenPages = 1000, skipErrors = true } = options;
    const reports: AccessibilityReport[] = [];

    console.log(`🧪 Testing ${urls.length} pages for accessibility...`);
    console.log(`⚙️  Max concurrency: ${maxConcurrency}, Delay: ${delayBetweenPages}ms`);

    // Process pages in batches to avoid overwhelming the server
    for (let i = 0; i < urls.length; i += maxConcurrency) {
      const batch = urls.slice(i, i + maxConcurrency);
      const batchPromises = batch.map(async (url, index) => {
        try {
          console.log(`📄 Testing page ${i + index + 1}/${urls.length}: ${url}`);

          // Navigate to the page with better error handling
          await this.page.goto(url, {
            waitUntil: 'domcontentloaded', // Less strict than networkidle
            timeout: 60000, // Longer timeout
          });

          // Wait for page to stabilize
          await this.page.waitForTimeout(1000);

          // Check if we were redirected and update URL
          const finalUrl = this.page.url();
          if (finalUrl !== url) {
            console.log(`📍 Page redirected from ${url} to ${finalUrl}`);
          }

          await this.injectAxe();

          // Gather page analysis
          const pageAnalysis = await this.gatherPageAnalysis();

          // Generate accessibility report (use final URL after any redirects)
          const browserName = (this.page as any).browserName || 'chromium';
          const viewportInfo = (this.page as any).viewportInfo || 'Desktop';
          const report = await this.generateAccessibilityReport(
            finalUrl,
            testSuite,
            pageAnalysis,
            browserName,
            viewportInfo
          );

          return report;
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : String(error);
          console.error(`❌ Error testing ${url}:`, errorMessage);

          if (!skipErrors) {
            throw error;
          }

          // Return minimal error report
          return {
            url,
            timestamp: new Date().toISOString(),
            testSuite,
            summary: {
              totalViolations: 0,
              criticalViolations: 0,
              seriousViolations: 0,
              moderateViolations: 0,
              minorViolations: 0,
              wcagAAViolations: 0,
              wcagAAAViolations: 0,
            },
            violations: [],
            pageAnalysis: {
              title: `Error loading page: ${errorMessage}`,
              headingStructure: [],
              landmarks: { main: false, nav: false, footer: false },
              skipLink: { exists: false, isVisible: false, targetExists: false },
              images: [],
              links: [],
              forms: [],
              keyboardNavigation: [],
              responsive: { mobile: false, tablet: false, desktop: false },
            },
          } as AccessibilityReport;
        }
      });

      const batchReports = await Promise.all(batchPromises);
      reports.push(...batchReports);

      // Delay between batches to be respectful to the server
      if (i + maxConcurrency < urls.length && delayBetweenPages > 0) {
        await new Promise(resolve => setTimeout(resolve, delayBetweenPages));
      }
    }

    console.log(`✅ Completed testing ${reports.length} pages`);
    return reports;
  }

  async gatherPageAnalysis(): Promise<AccessibilityReport['pageAnalysis']> {
    try {
      // This should be implemented based on the existing page analysis methods
      // For now, using basic implementations that should work with most pages
      const title = await this.page.title();

      const headingStructure = await this.page.$$eval('h1, h2, h3, h4, h5, h6', headings => {
        return headings.map(heading => ({
          level: parseInt(heading.tagName.substring(1)),
          text: heading.textContent?.trim() || '',
          tagName: heading.tagName.toLowerCase(),
        }));
      });

      const landmarks = {
        main: (await this.page.locator('main, [role="main"]').count()) > 0,
        nav: (await this.page.locator('nav, [role="navigation"]').count()) > 0,
        footer: (await this.page.locator('footer, [role="contentinfo"]').count()) > 0,
      };

      const skipLink = {
        exists: await this.page
          .locator('a[href*="#"], a[href^="#"]')
          .first()
          .isVisible()
          .catch(() => false),
        isVisible: await this.page
          .locator('a[href*="#"], a[href^="#"]')
          .first()
          .isVisible()
          .catch(() => false),
        targetExists: true, // Basic assumption
      };

      const images = await this.page.$$eval('img', imgs => {
        return imgs.map(img => ({
          src: img.src,
          alt: img.alt,
          hasAlt: img.hasAttribute('alt'),
          ariaLabel: img.getAttribute('aria-label') || undefined,
        }));
      });

      const links = await this.page.$$eval('a[href]', anchors => {
        return anchors.map(anchor => ({
          text: anchor.textContent?.trim() || '',
          href: (anchor as HTMLAnchorElement).href,
          hasAriaLabel: anchor.hasAttribute('aria-label'),
          ariaLabel: anchor.getAttribute('aria-label') || undefined,
        }));
      });

      const forms = await this.page.$$eval('input, select, textarea', elements => {
        return elements.map(element => {
          const label = document.querySelector(`label[for="${element.id}"]`);
          return {
            hasLabel: !!label || element.hasAttribute('aria-label'),
            labelText: label?.textContent?.trim() || element.getAttribute('aria-label') || '',
            inputType: element.getAttribute('type') || element.tagName.toLowerCase(),
            isRequired: element.hasAttribute('required'),
            hasAriaLabel: element.hasAttribute('aria-label'),
          };
        });
      });

      const keyboardNavigation = await this.page.$$eval(
        'a, button, input, select, textarea, [tabindex]',
        elements => {
          return elements.map(element => ({
            element: element.tagName.toLowerCase(),
            canFocus: element.tabIndex >= 0,
            hasVisibleFocus: true, // Basic assumption, would need actual focus testing
          }));
        }
      );

      return {
        title,
        headingStructure,
        landmarks,
        skipLink,
        images,
        links,
        forms,
        keyboardNavigation,
      };
    } catch (error) {
      console.error('Error gathering page analysis:', error);

      // Return minimal analysis on error
      return {
        title: '',
        headingStructure: [],
        landmarks: { main: false, nav: false, footer: false },
        skipLink: { exists: false, isVisible: false, targetExists: false },
        images: [],
        links: [],
        forms: [],
        keyboardNavigation: [],
      };
    }
  }

  // Aggregate multiple reports into a site-wide report
  aggregateReports(reports: AccessibilityReport[]): SiteWideAccessibilityReport {
    const successfulReports = reports.filter(r => r.violations.length >= 0); // Include all reports

    const totalViolations = successfulReports.reduce(
      (sum, report) => sum + report.summary.totalViolations,
      0
    );
    const totalCritical = successfulReports.reduce(
      (sum, report) => sum + report.summary.criticalViolations,
      0
    );
    const totalSerious = successfulReports.reduce(
      (sum, report) => sum + report.summary.seriousViolations,
      0
    );
    const totalModerate = successfulReports.reduce(
      (sum, report) => sum + report.summary.moderateViolations,
      0
    );
    const totalMinor = successfulReports.reduce(
      (sum, report) => sum + report.summary.minorViolations,
      0
    );

    // Group violations by type across all pages
    const violationsByType: Record<
      string,
      {
        count: number;
        pages: string[];
        impact: string;
        description: string;
        totalOccurrences: number;
        browsers: string[];
        tools: string[];
      }
    > = {};

    successfulReports.forEach(report => {
      report.violations.forEach(violation => {
        if (!violationsByType[violation.id]) {
          violationsByType[violation.id] = {
            count: 0,
            pages: [],
            impact: violation.impact,
            description: violation.description,
            totalOccurrences: 0,
            browsers: [],
            tools: [],
          };
        }

        violationsByType[violation.id].count++;
        violationsByType[violation.id].pages.push(report.url);
        violationsByType[violation.id].totalOccurrences += violation.occurrences;

        // Add browser information if available
        if (report.browser && !violationsByType[violation.id].browsers.includes(report.browser)) {
          violationsByType[violation.id].browsers.push(report.browser);
        }

        // Add tools information if available
        if (violation.tools) {
          violation.tools.forEach(tool => {
            if (!violationsByType[violation.id].tools.includes(tool)) {
              violationsByType[violation.id].tools.push(tool);
            }
          });
        }
      });
    });

    // Calculate compliance percentage
    const pagesWithViolations = successfulReports.filter(r => r.summary.totalViolations > 0).length;
    const compliancePercentage =
      successfulReports.length > 0
        ? Math.round(
            ((successfulReports.length - pagesWithViolations) / successfulReports.length) * 100
          )
        : 100;

    return {
      siteUrl: reports[0]?.url ? new URL(reports[0].url).origin : '',
      timestamp: new Date().toISOString(),
      testSuite: reports[0]?.testSuite || 'Site-wide Accessibility Audit',
      summary: {
        totalPages: successfulReports.length,
        pagesWithViolations,
        totalViolations,
        criticalViolations: totalCritical,
        seriousViolations: totalSerious,
        moderateViolations: totalModerate,
        minorViolations: totalMinor,
        compliancePercentage,
        mostCommonViolations: Object.entries(violationsByType)
          .sort(([, a], [, b]) => b.count - a.count)
          .slice(0, 10)
          .map(([id, data]) => ({
            id,
            affectedPages: data.count,
            totalOccurrences: data.totalOccurrences,
            impact: data.impact,
            description: data.description,
          })),
      },
      pageReports: successfulReports,
      violationsByType,
    };
  }

  async generateSiteWideReport(
    reports: AccessibilityReport[],
    filename: string,
    generatePdf: boolean = true
  ): Promise<void> {
    const aggregatedReport = this.aggregateReports(reports);

    // Save JSON report
    const fs = require('fs');
    const path = require('path');

    const reportsDir = path.join(process.cwd(), 'playwright', 'accessibility-reports');
    if (!fs.existsSync(reportsDir)) {
      fs.mkdirSync(reportsDir, { recursive: true });
    }

    // Clean up old reports before generating new ones
    this.cleanupOldReports(reportsDir);

    const jsonPath = path.join(reportsDir, `${filename}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(aggregatedReport, null, 2));
    console.log(`📄 Site-wide JSON report saved to: ${jsonPath}`);

    // Generate PDF reports
    if (generatePdf) {
      try {
        const { SiteWideAccessibilityPdfGenerator } = require('./site-wide-pdf-generator');
        const pdfGenerator = new SiteWideAccessibilityPdfGenerator(this.page);
        const generatedReports = await pdfGenerator.generateSiteWidePdfReport(
          aggregatedReport,
          filename
        );

        console.log(
          `📄 Generated ${generatedReports.length} audience-specific PDF reports (click to open):`
        );
        generatedReports.forEach((reportPath: string) => {
          const reportType = reportPath.includes('-stakeholders')
            ? 'Product Owners & Stakeholders'
            : reportPath.includes('-researchers')
              ? 'User Researchers & UCD'
              : reportPath.includes('-developers')
                ? 'Developers & Testers'
                : 'Unknown';

          // Create clickable link for terminal display
          const displayName = `📄 ${reportType}`;
          const clickableLink = this.createClickableLink(displayName, reportPath);
          console.log(`   ${clickableLink}`);
        });
      } catch (error) {
        console.warn('Could not generate PDF reports:', error);
      }
    }
  }
}
