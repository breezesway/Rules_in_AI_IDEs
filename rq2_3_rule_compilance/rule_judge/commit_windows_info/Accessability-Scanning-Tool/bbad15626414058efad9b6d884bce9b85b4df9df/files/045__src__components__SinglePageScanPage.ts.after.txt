import { renderHeader, HeaderProps } from './Header';
import { renderProgressSection, ProgressSectionProps } from './ProgressSection';
import { renderResultsSection, ResultsSectionProps } from './ResultsSection';
import { renderErrorSection, ErrorSectionProps } from './ErrorSection';
import { renderFooter, FooterProps } from './Footer';

export interface SinglePageScanPageProps {
    header?: HeaderProps;
    progress?: ProgressSectionProps;
    results?: ResultsSectionProps;
    error?: ErrorSectionProps;
    footer?: FooterProps;
    showProgress?: boolean;
    showResults?: boolean;
    showError?: boolean;
}

export function renderSinglePageScanPage(props: SinglePageScanPageProps = {}): string {
    const {
        header = {},
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
            <title>Single Page Scan - Accessibility Testing Tool</title>
            <meta name="description" content="Quick accessibility analysis of a single web page with detailed reporting">
            <link rel="stylesheet" href="styles.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            ${renderHeader({ ...header, currentPage: 'single-page' })}
            
            <main class="main">
                <div class="container">
                    <section class="scan-section" aria-labelledby="single-page-scan-heading">
                        <h2 id="single-page-scan-heading" class="section-heading">Single Page Accessibility Scan</h2>
                        <p class="section-description">Quick accessibility analysis of a single web page with detailed reporting</p>
                        
                        <div class="scan-option">
                            <div class="scan-option-header">
                                <span class="scan-icon">📄</span>
                                <h3>Single Page Scan</h3>
                            </div>
                            <p>Analyse the accessibility of a single web page with comprehensive WCAG 2.1 AAA compliance reporting.</p>
                                                            <form class="scan-form" id="singlePageForm" novalidate>
                                    <div class="form-group">
                                        <label for="singlePageUrl" class="form-label">Page URL <span class="required" aria-label="required">*</span></label>
                                        <input type="url" id="singlePageUrl" name="url" class="form-input"
                                            placeholder="https://example.com/page" required aria-describedby="singlePageUrlHelp singlePageUrlError" aria-invalid="false">
                                        <div id="singlePageUrlHelp" class="form-help">Enter the full URL of the page to test</div>
                                        <div id="singlePageUrlError" class="form-error" role="alert" aria-live="polite" hidden></div>
                                    </div>
                                    <div class="form-group">
                                        <label for="singlePageWcagLevel" class="form-label">WCAG Standard <span class="required" aria-label="required">*</span></label>
                                        <select id="singlePageWcagLevel" name="wcagLevel" class="form-select" required aria-describedby="singlePageWcagLevelHelp">
                                            <option value="WCAG2A">WCAG 2.1 Level A</option>
                                            <option value="WCAG2AA" selected>WCAG 2.1 Level AA</option>
                                            <option value="WCAG2AAA">WCAG 2.1 Level AAA</option>
                                            <option value="WCAG22A">WCAG 2.2 Level A</option>
                                            <option value="WCAG22AA">WCAG 2.2 Level AA</option>
                                            <option value="WCAG22AAA">WCAG 2.2 Level AAA</option>
                                        </select>
                                        <div id="singlePageWcagLevelHelp" class="form-help">Choose the WCAG compliance level to test against</div>
                                    </div>
                                    <button type="submit" class="btn btn-primary">
                                        <span class="btn-icon" aria-hidden="true">📊</span>
                                        Start Single Page Scan
                                    </button>
                                </form>
                        </div>
                    </section>
                    
                    ${renderProgressSection({ ...progress })}
                    ${renderResultsSection({ ...results })}
                    ${renderErrorSection({ ...error })}
                </div>
            </main>

            ${renderFooter(footer)}

            <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
            <script src="app.js"></script>

        </body>
        </html>
    `;
} 