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