import fs from 'fs';
import path from 'path';

describe('Storybook Setup Validation', () => {
    const storiesDir = path.join(process.cwd(), 'stories');
    const storybookDir = path.join(process.cwd(), '.storybook');
    const componentsDir = path.join(process.cwd(), 'src/components');

    test('should have Storybook configuration files', () => {
        expect(fs.existsSync(path.join(storybookDir, 'main.mjs'))).toBe(true);
        expect(fs.existsSync(path.join(storybookDir, 'preview.mjs'))).toBe(true);
    });

    test('should have component stories', () => {
        const storyFiles = fs.readdirSync(storiesDir);
        expect(storyFiles).toContain('Header.stories.ts');
        expect(storyFiles).toContain('ScanOptions.stories.ts');
        expect(storyFiles).toContain('ProgressSection.stories.ts');
        expect(storyFiles).toContain('ResultsSection.stories.ts');
        expect(storyFiles).toContain('ErrorSection.stories.ts');
        expect(storyFiles).toContain('Footer.stories.ts');
    });

    test('should have shared component files', () => {
        const componentFiles = fs.readdirSync(componentsDir);
        expect(componentFiles).toContain('Header.ts');
        expect(componentFiles).toContain('ScanOptions.ts');
        expect(componentFiles).toContain('ProgressSection.ts');
        expect(componentFiles).toContain('ResultsSection.ts');
        expect(componentFiles).toContain('ErrorSection.ts');
        expect(componentFiles).toContain('Footer.ts');
        expect(componentFiles).toContain('WebInterface.ts');
        expect(componentFiles).toContain('LandingPage.ts');
        expect(componentFiles).toContain('FullSiteScanPage.ts');
        expect(componentFiles).toContain('SinglePageScanPage.ts');
        expect(componentFiles).toContain('ReportsPage.ts');
        expect(componentFiles).toContain('index.ts');
    });

    test('should have CSS styles for stories', () => {
        // Check if the shared CSS file exists
        const cssPath = path.join(process.cwd(), 'src/public/styles.css');
        expect(fs.existsSync(cssPath)).toBe(true);

        if (fs.existsSync(cssPath)) {
            const cssContent = fs.readFileSync(cssPath, 'utf8');
            expect(cssContent.length).toBeGreaterThan(0);
        }
    });

    test('should have accessibility testing configuration in stories', () => {
        const headerContent = fs.readFileSync(path.join(storiesDir, 'Header.stories.ts'), 'utf8');
        expect(headerContent).toContain('a11y');
        expect(headerContent).toContain('color-contrast');
        expect(headerContent).toContain('heading-order');

        const progressContent = fs.readFileSync(path.join(storiesDir, 'ProgressSection.stories.ts'), 'utf8');
        expect(progressContent).toContain('a11y');
        expect(progressContent).toContain('progressbar-name');
        expect(progressContent).toContain('aria-progressbar-name');

        const resultsContent = fs.readFileSync(path.join(storiesDir, 'ResultsSection.stories.ts'), 'utf8');
        expect(resultsContent).toContain('a11y');
        expect(resultsContent).toContain('table-fake-caption');
        expect(resultsContent).toContain('table-structure');

        const errorContent = fs.readFileSync(path.join(storiesDir, 'ErrorSection.stories.ts'), 'utf8');
        expect(errorContent).toContain('a11y');
        expect(errorContent).toContain('alert');
        expect(errorContent).toContain('aria-alert');

        const footerContent = fs.readFileSync(path.join(storiesDir, 'Footer.stories.ts'), 'utf8');
        expect(footerContent).toContain('a11y');
        expect(footerContent).toContain('link-name');
        expect(footerContent).toContain('landmark-one-main');

        const webInterfaceContent = fs.readFileSync(path.join(storiesDir, 'WebInterface.stories.ts'), 'utf8');
        expect(webInterfaceContent).toContain('a11y');
        expect(webInterfaceContent).toContain('landmark-one-main');
        expect(webInterfaceContent).toContain('region');

        const landingPageContent = fs.readFileSync(path.join(storiesDir, 'LandingPage.stories.ts'), 'utf8');
        expect(landingPageContent).toContain('a11y');
        expect(landingPageContent).toContain('button-name');
        expect(landingPageContent).toContain('link-name');

        const fullSiteScanContent = fs.readFileSync(path.join(storiesDir, 'FullSiteScanPage.stories.ts'), 'utf8');
        expect(fullSiteScanContent).toContain('a11y');
        expect(fullSiteScanContent).toContain('form-field-multiple-labels');
        expect(fullSiteScanContent).toContain('progressbar-name');

        const singlePageScanContent = fs.readFileSync(path.join(storiesDir, 'SinglePageScanPage.stories.ts'), 'utf8');
        expect(singlePageScanContent).toContain('a11y');
        expect(singlePageScanContent).toContain('form-field-multiple-labels');
        expect(singlePageScanContent).toContain('progressbar-name');

        const reportsPageContent = fs.readFileSync(path.join(storiesDir, 'ReportsPage.stories.ts'), 'utf8');
        expect(reportsPageContent).toContain('a11y');
        expect(reportsPageContent).toContain('table-fake-caption');
        expect(reportsPageContent).toContain('table-structure');
    });

    test('should have responsive viewport configurations', () => {
        const previewContent = fs.readFileSync(path.join(storybookDir, 'preview.mjs'), 'utf8');
        expect(previewContent).toContain('viewport');
        expect(previewContent).toContain('mobile');
        expect(previewContent).toContain('tablet');
        expect(previewContent).toContain('desktop');
    });

    test('should have component-based architecture', () => {
        const headerContent = fs.readFileSync(path.join(storiesDir, 'Header.stories.ts'), 'utf8');
        expect(headerContent).toContain('renderHeader');
        expect(headerContent).toContain('HeaderProps');
        expect(headerContent).toContain('from \'../src/components/Header\'');
    });

    test('should have proper TypeScript imports', () => {
        const scanOptionsContent = fs.readFileSync(path.join(storiesDir, 'ScanOptions.stories.ts'), 'utf8');
        expect(scanOptionsContent).toContain('renderScanOptions');
        expect(scanOptionsContent).toContain('ScanOptionsProps');
        expect(scanOptionsContent).toContain('from \'../src/components/ScanOptions\'');
    });

    test('should have ES module configuration', () => {
        const mainContent = fs.readFileSync(path.join(storybookDir, 'main.mjs'), 'utf8');
        expect(mainContent).toContain('export default config');
        expect(mainContent).toContain('ts-loader');
        expect(mainContent).toContain('.ts');
        expect(mainContent).toContain('.tsx');
    });

    test('should have shared CSS import', () => {
        const previewContent = fs.readFileSync(path.join(storybookDir, 'preview.mjs'), 'utf8');
        expect(previewContent).toContain('import \'../src/public/styles.css\'');
    });

    test('should have accessibility attributes in components', () => {
        const headerComponentContent = fs.readFileSync(path.join(componentsDir, 'Header.ts'), 'utf8');
        expect(headerComponentContent).toContain('class="header"');
        expect(headerComponentContent).toContain('class="logo"');
        expect(headerComponentContent).toContain('class="tagline"');
    });

    test('should have form accessibility in scan options', () => {
        const scanOptionsComponentContent = fs.readFileSync(path.join(componentsDir, 'ScanOptions.ts'), 'utf8');
        expect(scanOptionsComponentContent).toContain('aria-labelledby');
        expect(scanOptionsComponentContent).toContain('aria-describedby');
        expect(scanOptionsComponentContent).toContain('required');
        expect(scanOptionsComponentContent).toContain('form-label');
    });
}); 