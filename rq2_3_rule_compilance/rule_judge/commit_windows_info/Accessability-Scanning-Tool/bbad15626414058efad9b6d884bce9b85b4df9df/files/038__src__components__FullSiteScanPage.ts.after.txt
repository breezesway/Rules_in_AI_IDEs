import { renderHeader, HeaderProps } from './Header';
import { renderProgressSection, ProgressSectionProps } from './ProgressSection';
import { renderResultsSection, ResultsSectionProps } from './ResultsSection';
import { renderErrorSection, ErrorSectionProps } from './ErrorSection';
import { renderFooter, FooterProps } from './Footer';

export interface FullSiteScanPageProps {
    header?: HeaderProps;
    progress?: ProgressSectionProps;
    results?: ResultsSectionProps;
    error?: ErrorSectionProps;
    footer?: FooterProps;
    showProgress?: boolean;
    showResults?: boolean;
    showError?: boolean;
}

export function renderFullSiteScanPage(props: FullSiteScanPageProps = {}): string {
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
            <title>Full Site Scan - Accessibility Testing Tool</title>
            <meta name="description" content="Comprehensive accessibility audit across your entire website with detailed reporting">
            <link rel="stylesheet" href="styles.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            ${renderHeader({ ...header, currentPage: 'full-site' })}
            
            <main class="main">
                <div class="container">
                    <section class="scan-section" aria-labelledby="full-site-scan-heading">
                        <h2 id="full-site-scan-heading" class="section-heading">Full Site Accessibility Scan</h2>
                        <p class="section-description">Comprehensive accessibility audit across your entire website (50 pages, 4 levels deep)</p>
                        
                        <div class="scan-option">
                            <div class="scan-option-header">
                                <span class="scan-icon">🌐</span>
                                <h3>Full Site Scan</h3>
                            </div>
                            <p>Comprehensive accessibility audit across your entire website with intelligent crawling and detailed reporting.</p>
                            <form class="scan-form" id="fullSiteForm" novalidate>
                                <div class="form-group">
                                    <label for="fullSiteUrl" class="form-label">Website URL <span class="required" aria-label="required">*</span></label>
                                    <input type="url" id="fullSiteUrl" name="url" class="form-input"
                                        placeholder="https://example.com" required aria-describedby="fullSiteUrlHelp fullSiteUrlError" aria-invalid="false">
                                    <div id="fullSiteUrlHelp" class="form-help">Enter the full URL including http:// or https://</div>
                                    <div id="fullSiteUrlError" class="form-error" role="alert" aria-live="polite" hidden></div>
                                </div>
                                <div class="form-group">
                                    <label for="fullSiteWcagLevel" class="form-label">WCAG Standard <span class="required" aria-label="required">*</span></label>
                                    <select id="fullSiteWcagLevel" name="wcagLevel" class="form-select" required aria-describedby="fullSiteWcagLevelHelp">
                                        <option value="WCAG2A">WCAG 2.1 Level A</option>
                                        <option value="WCAG2AA" selected>WCAG 2.1 Level AA</option>
                                        <option value="WCAG2AAA">WCAG 2.1 Level AAA</option>
                                        <option value="WCAG22A">WCAG 2.2 Level A</option>
                                        <option value="WCAG22AA">WCAG 2.2 Level AA</option>
                                        <option value="WCAG22AAA">WCAG 2.2 Level AAA</option>
                                    </select>
                                    <div id="fullSiteWcagLevelHelp" class="form-help">Choose the WCAG compliance level to test against</div>
                                </div>
                                <button type="submit" class="btn btn-primary">
                                    <span class="btn-icon" aria-hidden="true">🚀</span>
                                    Start Full Site Scan
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