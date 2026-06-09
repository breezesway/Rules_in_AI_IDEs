import { renderHeader, HeaderProps } from './Header';
import { renderFooter, FooterProps } from './Footer';

export interface ReportsPageProps {
    header?: HeaderProps;
    footer?: FooterProps;
}

export function renderReportsPage(props: ReportsPageProps = {}): string {
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
            <title>Search Reports - Accessibility Testing Tool</title>
            <meta name="description" content="Search and generate PDF reports from past accessibility scan results">
            <link rel="stylesheet" href="styles.css">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            ${renderHeader({ ...header, currentPage: 'reports' })}
            
            <main class="main">
                <div class="container">
                    <section class="reports-section" aria-labelledby="reports-heading">
                        <h2 id="reports-heading" class="section-heading">Search & Generate Reports</h2>
                        <p class="section-description">Search through past scan results and generate PDF reports from stored data</p>
                        
                        <div class="search-section">
                            <h3>Search Reports</h3>
                            <form class="search-form" id="searchReportsForm">
                                <div class="form-row">
                                    <div class="form-group">
                                        <label for="siteUrl" class="form-label">Site URL</label>
                                        <input type="url" id="siteUrl" name="siteUrl" class="form-input"
                                            placeholder="https://example.com" aria-describedby="siteUrlHelp">
                                        <div id="siteUrlHelp" class="form-help">Filter by specific website URL (optional)</div>
                                    </div>
                                    <div class="form-group">
                                        <label for="dateFrom" class="form-label">From Date</label>
                                        <input type="date" id="dateFrom" name="dateFrom" class="form-input"
                                            aria-describedby="dateFromHelp">
                                        <div id="dateFromHelp" class="form-help">Start date for search (optional)</div>
                                    </div>
                                    <div class="form-group">
                                        <label for="dateTo" class="form-label">To Date</label>
                                        <input type="date" id="dateTo" name="dateTo" class="form-input"
                                            aria-describedby="dateToHelp">
                                        <div id="dateToHelp" class="form-help">End date for search (optional)</div>
                                    </div>
                                </div>
                                <button type="submit" class="btn btn-primary">
                                    <span class="btn-icon">🔍</span>
                                    Search Reports
                                </button>
                            </form>
                        </div>

                        <div class="generate-section">
                            <h3>Generate PDF Reports</h3>
                            <p>Generate comprehensive PDF reports from past scan results stored in the database.</p>
                            <button type="button" class="btn btn-secondary" id="generateReportsBtn">
                                <span class="btn-icon">📄</span>
                                Generate Reports
                            </button>
                        </div>

                        <div class="results-section" id="searchResults" style="display: none;">
                            <h3>Search Results</h3>
                            <div id="reportsList" class="reports-list">
                                <!-- Search results will be populated here -->
                            </div>
                        </div>

                        <div class="loading-section" id="loadingSection" style="display: none;">
                            <div class="loading-spinner"></div>
                            <p>Searching reports...</p>
                        </div>

                        <div class="error-section" id="errorSection" style="display: none;">
                            <div class="error-message" id="errorMessage"></div>
                        </div>
                    </section>
                </div>
            </main>

            ${renderFooter(footer)}

            <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
            <script src="app.js"></script>
            <script>
                // Page-specific JavaScript for reports page
                document.addEventListener('DOMContentLoaded', function() {
                    const searchForm = document.getElementById('searchReportsForm');
                    const generateBtn = document.getElementById('generateReportsBtn');
                    const searchResults = document.getElementById('searchResults');
                    const loadingSection = document.getElementById('loadingSection');
                    const errorSection = document.getElementById('errorSection');
                    const reportsList = document.getElementById('reportsList');

                    // Search reports functionality
                    if (searchForm) {
                        searchForm.addEventListener('submit', function(e) {
                            e.preventDefault();
                            const formData = new FormData(searchForm);
                            const searchData = {
                                siteUrl: formData.get('siteUrl'),
                                dateFrom: formData.get('dateFrom'),
                                dateTo: formData.get('dateTo')
                            };

                            // Show loading
                            loadingSection.style.display = 'block';
                            searchResults.style.display = 'none';
                            errorSection.style.display = 'none';

                            // Call search API
                            fetch('/api/reports/search', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(searchData)
                            })
                            .then(response => response.json())
                            .then(data => {
                                loadingSection.style.display = 'none';
                                
                                if (data.success) {
                                    displaySearchResults(data.data.reports);
                                    searchResults.style.display = 'block';
                                } else {
                                    showError(data.error || 'Search failed');
                                }
                            })
                            .catch(error => {
                                loadingSection.style.display = 'none';
                                showError('Search failed: ' + error.message);
                            });
                        });
                    }

                    // Generate reports functionality
                    if (generateBtn) {
                        generateBtn.addEventListener('click', function() {
                            // Call the existing generate reports functionality
                            if (window.generateReports) {
                                window.generateReports();
                            }
                        });
                    }

                    function displaySearchResults(reports) {
                        if (reports.length === 0) {
                            reportsList.innerHTML = '<p>No reports found matching your search criteria.</p>';
                            return;
                        }

                        const reportsHtml = reports.map(report => \`
                            <div class="report-item">
                                <div class="report-info">
                                    <h4>\${report.siteUrl || 'Unknown Site'}</h4>
                                    <p>Type: \${report.reportType || 'Unknown'}</p>
                                    <p>Date: \${new Date(report.lastModified).toLocaleDateString('en-GB')}</p>
                                </div>
                                <div class="report-actions">
                                    <button class="btn btn-small" onclick="generateReportFromId('\${report.id}')">
                                        Generate PDF
                                    </button>
                                </div>
                            </div>
                        \`).join('');

                        reportsList.innerHTML = reportsHtml;
                    }

                    function showError(message) {
                        document.getElementById('errorMessage').textContent = message;
                        errorSection.style.display = 'block';
                    }

                    // Make functions globally available
                    window.generateReportFromId = function(reportId) {
                        // Call the existing PDF generation functionality
                        if (window.generatePdfFromReportId) {
                            window.generatePdfFromReportId(reportId);
                        }
                    };
                });
            </script>
        </body>
        </html>
    `;
} 