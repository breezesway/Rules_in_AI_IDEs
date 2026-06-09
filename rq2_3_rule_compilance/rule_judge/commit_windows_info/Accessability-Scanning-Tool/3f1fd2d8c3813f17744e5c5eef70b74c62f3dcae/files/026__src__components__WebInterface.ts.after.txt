import { renderHeader, HeaderProps } from './Header';
import { renderScanOptions, ScanOptionsProps } from './ScanOptions';
import { renderProgressSection, ProgressSectionProps } from './ProgressSection';
import { renderResultsSection, ResultsSectionProps } from './ResultsSection';
import { renderErrorSection, ErrorSectionProps } from './ErrorSection';
import { renderFooter, FooterProps } from './Footer';

export interface WebInterfaceProps {
    header?: HeaderProps;
    scanOptions?: ScanOptionsProps;
    progress?: ProgressSectionProps;
    results?: ResultsSectionProps;
    error?: ErrorSectionProps;
    footer?: FooterProps;
    showProgress?: boolean;
    showResults?: boolean;
    showError?: boolean;
}

export function renderWebInterface(props: WebInterfaceProps = {}): string {
    const {
        header = {},
        scanOptions = {},
        progress = {},
        results = {},
        error = {},
        footer = {},
        showProgress = false,
        showResults = false,
        showError = false
    } = props;

    return `
        <!DOCTYPE html>
        <html lang="en-GB">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Accessibility Testing Tool - Professional WCAG 2.1 AAA Compliance</title>
            <meta name="description" content="Professional automated accessibility testing solution with comprehensive WCAG 2.1 AAA compliance reports">
            <link rel="stylesheet" href="styles.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            ${renderHeader(header)}
            
            <main class="main">
                <div class="container">
                    ${renderScanOptions(scanOptions)}
                    ${renderProgressSection({ ...progress, visible: showProgress })}
                    ${renderResultsSection({ ...results, visible: showResults })}
                    ${renderErrorSection({ ...error, visible: showError })}
                </div>
            </main>

            ${renderFooter(footer)}

            <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
            <script src="app.js"></script>
        </body>
        </html>
    `;
}

// Export individual components for use in Storybook
export { renderHeader } from './Header';
export { renderScanOptions } from './ScanOptions';
export { renderProgressSection } from './ProgressSection';
export { renderResultsSection } from './ResultsSection';
export { renderErrorSection } from './ErrorSection';
export { renderFooter } from './Footer'; 