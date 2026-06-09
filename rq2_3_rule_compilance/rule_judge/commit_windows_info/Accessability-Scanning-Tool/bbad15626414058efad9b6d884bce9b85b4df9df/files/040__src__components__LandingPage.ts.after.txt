import { renderHeader, HeaderProps } from './Header';
import { renderFooter, FooterProps } from './Footer';

export interface LandingPageProps {
    header?: HeaderProps;
    footer?: FooterProps;
}

export function renderLandingPage(props: LandingPageProps = {}): string {
    const {
        header = {},
        footer = {}
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
            ${renderHeader({ ...header, currentPage: 'home' })}
            
            <main class="main">
                <div class="container">
                    <section class="hero-section" aria-labelledby="hero-heading">
                        <h1 id="hero-heading" class="hero-heading">Professional Accessibility Testing</h1>
                        <p class="hero-description">Comprehensive WCAG 2.1 AAA compliance testing with detailed reporting and analysis</p>
                    </section>

                    <section class="features-section" aria-labelledby="features-heading">
                        <h2 id="features-heading" class="section-heading">Choose Your Testing Approach</h2>
                        <div class="features-grid">
                            <div class="feature-card">
                                <div class="feature-icon">📄</div>
                                <h3>Single Page Scan</h3>
                                <p>Test one specific page for accessibility issues. Perfect for testing new pages, forms, or individual components.</p>
                                <ul class="feature-list">
                                    <li>Test any single URL</li>
                                    <li>Quick results in minutes</li>
                                    <li>Detailed page-specific analysis</li>
                                    <li>Perfect for development testing</li>
                                </ul>
                                <a href="/single-page" class="btn btn-primary">
                                    <span class="btn-icon">📄</span>
                                    Start Single Page Scan
                                </a>
                            </div>

                            <div class="feature-card">
                                <div class="feature-icon">🌐</div>
                                <h3>Full Site Scan</h3>
                                <p>Automatically discover and test multiple pages across your entire website. Ideal for comprehensive site audits.</p>
                                <ul class="feature-list">
                                    <li>Automatic page discovery</li>
                                    <li>Configurable crawl depth (1-10 levels)</li>
                                    <li>Up to 100 pages per scan</li>
                                    <li>Site-wide compliance overview</li>
                                </ul>
                                <a href="/full-site" class="btn btn-primary">
                                    <span class="btn-icon">🌐</span>
                                    Start Full Site Scan
                                </a>
                            </div>

                            <div class="feature-card">
                                <div class="feature-icon">📊</div>
                                <h3>Search & Generate Reports</h3>
                                <p>Search through past scan results and generate comprehensive PDF reports from stored data.</p>
                                <ul class="feature-list">
                                    <li>Advanced search filters</li>
                                    <li>Date range filtering</li>
                                    <li>Multiple report formats</li>
                                    <li>Historical data access</li>
                                </ul>
                                <a href="/reports" class="btn btn-primary">
                                    <span class="btn-icon">📊</span>
                                    Search Reports
                                </a>
                            </div>
                        </div>
                    </section>

                    <section class="info-section" aria-labelledby="info-heading">
                        <h2 id="info-heading" class="section-heading">Why Choose Our Tool?</h2>
                        <div class="info-grid">
                            <div class="info-item">
                                <h3>WCAG 2.1 AAA Compliance</h3>
                                <p>Test against the highest accessibility standards with comprehensive WCAG 2.1 AAA compliance checking.</p>
                            </div>
                            <div class="info-item">
                                <h3>Multiple Testing Tools</h3>
                                <p>Combines axe-core and Pa11y for comprehensive accessibility analysis with detailed violation reporting.</p>
                            </div>
                            <div class="info-item">
                                <h3>Real-time Progress</h3>
                                <p>Track scan progress in real-time with detailed stage information and estimated completion times.</p>
                            </div>
                            <div class="info-item">
                                <h3>Professional Reports</h3>
                                <p>Generate detailed PDF reports suitable for stakeholders, developers, and compliance documentation.</p>
                            </div>
                        </div>
                    </section>
                </div>
            </main>

            ${renderFooter(footer)}

            <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
            <script src="app.js"></script>
        </body>
        </html>
    `;
} 