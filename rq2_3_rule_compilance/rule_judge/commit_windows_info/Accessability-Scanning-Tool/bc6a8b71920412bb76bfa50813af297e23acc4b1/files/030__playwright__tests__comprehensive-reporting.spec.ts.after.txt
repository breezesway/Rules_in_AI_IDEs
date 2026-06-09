import { expect, test } from '@playwright/test';
import { AccessibilityTestUtils } from './utils/accessibility-helpers';
import { existsSync, readdirSync, readFileSync } from 'fs';
import path from 'path';

function getViewportInfo(page: any): string {
    const viewport = page.viewportSize();
    if (!viewport) return 'Desktop Chrome (1280x720)';
    return `Desktop Chrome (${viewport.width}x${viewport.height})`;
}

function createClickableLink(text: string, url: string, color: string = '\x1b[35m'): string {
    const reset = '\x1b[0m';
    const linkUrl = url.startsWith('/') ? `file://${url}` : url;
    return `${color}\x1b]8;;${linkUrl}\x1b\\${text}\x1b]8;;\x1b\\${reset}`;
}

function mergeViolationsFromMultipleTools(violations: any[]): any[] {
    const violationMap = new Map<string, any>();

    violations.forEach(violation => {
        if (violationMap.has(violation.id)) {
            const existing = violationMap.get(violation.id)!;
            existing.tools = [...new Set([...existing.tools, ...violation.tools])];
            existing.elements.push(...violation.elements);
            existing.occurrences += violation.occurrences;
        } else {
            violationMap.set(violation.id, violation);
        }
    });

    return Array.from(violationMap.values());
}

test.describe('Comprehensive Accessibility Reporting', () => {
    let accessibilityUtils: AccessibilityTestUtils;

    test.beforeEach(async ({ page, browserName }) => {
        accessibilityUtils = new AccessibilityTestUtils(page);
        (page as any).browserName = browserName;
        (page as any).viewportInfo = getViewportInfo(page);
    });

    test('@accessibility @reporting @parallel Combine all parallel analysis results into comprehensive reports', async ({
        page,
        browserName,
    }) => {
        console.log('📄 Starting comprehensive accessibility reporting...');
        const resultsDir = path.join(
            process.cwd(),
            'playwright',
            'accessibility-reports',
            'parallel-analysis'
        );

        if (!existsSync(resultsDir)) {
            console.log('⚠️ No parallel analysis results found.');
            return;
        }

        const files = readdirSync(resultsDir).filter(f => f.endsWith('.json'));
        const axeResultFile = files.find(f => f.startsWith('axe-core-results-'));
        const pa11yResultFile = files.find(f => f.startsWith('pa11y-results-'));

        let axeResults: any[] | null = null;
        if (axeResultFile) {
            axeResults = JSON.parse(readFileSync(path.join(resultsDir, axeResultFile), 'utf8')).results;
        }

        let pa11yResults: any[] | null = null;
        if (pa11yResultFile) {
            pa11yResults = JSON.parse(readFileSync(path.join(resultsDir, pa11yResultFile), 'utf8')).results;
        }

        const combinedReports: any[] = [];
        const allUrls = new Set<string>();

        if (axeResults) axeResults.forEach(r => allUrls.add(r.url));
        if (pa11yResults) pa11yResults.forEach(r => allUrls.add(r.url));

        for (const url of allUrls) {
            const axeResult = axeResults?.find(r => r.url === url);
            const pa11yResult = pa11yResults?.find(r => r.url === url);
            const allViolations: any[] = [];
            const toolsUsed: string[] = [];

            if (axeResult?.violations) {
                allViolations.push(...axeResult.violations);
                toolsUsed.push('axe-core');
            }

            if (pa11yResult?.violations) {
                allViolations.push(...pa11yResult.violations);
                toolsUsed.push('pa11y');
            }

            const mergedViolations = mergeViolationsFromMultipleTools(allViolations);

            const comprehensiveReport = {
                url,
                timestamp: new Date().toISOString(),
                testSuite: 'Comprehensive Parallel Accessibility Analysis',
                browser: browserName,
                viewport: getViewportInfo(page),
                summary: {
                    totalViolations: mergedViolations.length,
                    criticalViolations: mergedViolations.filter(v => v.impact === 'critical').length,
                    seriousViolations: mergedViolations.filter(v => v.impact === 'serious').length,
                    moderateViolations: mergedViolations.filter(v => v.impact === 'moderate').length,
                    minorViolations: mergedViolations.filter(v => v.impact === 'minor').length,
                },
                violations: mergedViolations,
                toolsUsed,
                rawResults: {
                    axe: axeResult || null,
                    pa11y: pa11yResult || null,
                },
            };

            combinedReports.push(comprehensiveReport);
        }
    });
}); 