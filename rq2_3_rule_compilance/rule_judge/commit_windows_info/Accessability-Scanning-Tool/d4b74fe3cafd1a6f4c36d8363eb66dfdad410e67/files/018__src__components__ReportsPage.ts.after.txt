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
                            <h3>Advanced Search</h3>
                            <form class="search-form" id="searchReportsForm">
                                <div class="form-row">
                                    <div class="form-group">
                                        <label for="siteUrl" class="form-label">Site URL</label>
                                        <input type="url" id="siteUrl" name="siteUrl" class="form-input"
                                            placeholder="https://example.com" aria-describedby="siteUrlHelp">
                                        <div id="siteUrlHelp" class="form-help">Filter by specific website URL (optional)</div>
                                    </div>
                                    <div class="form-group">
                                        <label for="reportType" class="form-label">Report Type</label>
                                        <select id="reportType" name="reportType" class="form-select" aria-describedby="reportTypeHelp">
                                            <option value="">All Types</option>
                                            <option value="site-wide">Site-wide Reports</option>
                                            <option value="single-page">Single Page Reports</option>
                                        </select>
                                        <div id="reportTypeHelp" class="form-help">Filter by report type (optional)</div>
                                    </div>
                                </div>
                                
                                <div class="form-row">
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
                                    <div class="form-group">
                                        <label for="wcagLevel" class="form-label">WCAG Level</label>
                                        <select id="wcagLevel" name="wcagLevel" class="form-select" aria-describedby="wcagLevelHelp">
                                            <option value="">All Levels</option>
                                            <option value="A">WCAG A</option>
                                            <option value="AA">WCAG AA</option>
                                            <option value="AAA">WCAG AAA</option>
                                        </select>
                                        <div id="wcagLevelHelp" class="form-help">Filter by WCAG compliance level (optional)</div>
                                    </div>
                                </div>

                                <div class="form-actions">
                                    <button type="submit" class="btn btn-primary">
                                        <span class="btn-icon">🔍</span>
                                        Search Reports
                                    </button>
                                    <button type="button" class="btn btn-secondary" id="clearSearchBtn">
                                        <span class="btn-icon">🗑️</span>
                                        Clear Search
                                    </button>
                                </div>
                            </form>
                        </div>

                        <div class="results-section" id="searchResults" style="display: none;">
                            <h3>Search Results</h3>
                            <div class="results-header">
                                <div class="results-count" id="resultsCount"></div>
                            </div>
                            <div id="reportsList" class="reports-list">
                                <!-- Search results will be populated here -->
                            </div>
                        </div>

                        <div class="loading-section" id="loadingSection" style="display: none;">
                            <div class="loading-spinner"></div>
                            <p id="loadingMessage">Searching reports...</p>
                        </div>

                        <div class="error-section" id="errorSection" style="display: none;">
                            <div class="error-message" id="errorMessage"></div>
                        </div>

                        <div class="success-section" id="successSection" style="display: none;">
                            <div class="success-message" id="successMessage"></div>
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
                    const clearSearchBtn = document.getElementById('clearSearchBtn');
                    const searchResults = document.getElementById('searchResults');
                    const loadingSection = document.getElementById('loadingSection');
                    const errorSection = document.getElementById('errorSection');
                    const successSection = document.getElementById('successSection');
                    const reportsList = document.getElementById('reportsList');
                    const resultsCount = document.getElementById('resultsCount');
                    const loadingMessage = document.getElementById('loadingMessage');

                    let currentReports = [];

                    // Search reports functionality
                    if (searchForm) {
                        searchForm.addEventListener('submit', function(e) {
                            e.preventDefault();
                            performSearch();
                        });
                    }

                    // Clear search functionality
                    if (clearSearchBtn) {
                        clearSearchBtn.addEventListener('click', function() {
                            searchForm.reset();
                            hideResults();
                        });
                    }

                    function performSearch() {
                        const formData = new FormData(searchForm);
                        const searchData = {
                            siteUrl: formData.get('siteUrl'),
                            reportType: formData.get('reportType'),
                            dateFrom: formData.get('dateFrom'),
                            dateTo: formData.get('dateTo'),
                            wcagLevel: formData.get('wcagLevel')
                        };

                        // Show loading
                        showLoading('Searching reports...');
                        hideResults();
                        hideMessages();

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
                            hideLoading();
                            
                            if (data.success) {
                                currentReports = data.data.reports || [];
                                displaySearchResults(currentReports);
                                showResults();
                            } else {
                                showError(data.error || 'Search failed');
                            }
                        })
                        .catch(error => {
                            hideLoading();
                            showError('Search failed: ' + error.message);
                        });
                    }

                    function displaySearchResults(reports) {
                        if (reports.length === 0) {
                            reportsList.innerHTML = '<p class="no-results">No reports found matching your search criteria.</p>';
                            resultsCount.textContent = '0 reports found';
                            return;
                        }

                        resultsCount.textContent = \`\${reports.length} report\${reports.length === 1 ? '' : 's'} found\`;

                        const reportsHtml = reports.map(report => \`
                            <div class="report-item">
                                <div class="report-info">
                                    <h4>\${report.siteUrl || 'Unknown Site'}</h4>
                                    <div class="report-details">
                                        <span class="report-type \${report.reportType}">\${report.reportType || 'Unknown'}</span>
                                        <span class="report-date">\${new Date(report.createdAt || report.lastModified).toLocaleDateString('en-GB')}</span>
                                        <span class="report-violations">\${report.metadata?.totalViolations || 0} violations</span>
                                        <span class="report-compliance">\${report.metadata?.compliancePercentage || 0}% compliant</span>
                                    </div>
                                    <div class="report-metadata">
                                        <span class="wcag-level">WCAG \${report.metadata?.wcagLevel || 'Unknown'}</span>
                                        <span class="scan-type">\${report.metadata?.scanType || 'Unknown'} scan</span>
                                        <span class="tools-used">\${(report.metadata?.toolsUsed || []).join(', ')}</span>
                                    </div>
                                </div>
                                <div class="report-actions">
                                    <button class="btn btn-small" onclick="generateReportFromId('\${report._id || report.id}')">
                                        Generate PDF
                                    </button>
                                    <button class="btn btn-small btn-outline" onclick="viewReportDetails('\${report._id || report.id}')">
                                        View Details
                                    </button>
                                </div>
                            </div>
                        \`).join('');

                        reportsList.innerHTML = reportsHtml;
                    }

                    function showLoading(message) {
                        loadingMessage.textContent = message;
                        loadingSection.style.display = 'block';
                    }

                    function hideLoading() {
                        loadingSection.style.display = 'none';
                    }

                    function showResults() {
                        searchResults.style.display = 'block';
                    }

                    function hideResults() {
                        searchResults.style.display = 'none';
                        currentReports = [];
                    }

                    function showError(message) {
                        document.getElementById('errorMessage').textContent = message;
                        errorSection.style.display = 'block';
                    }

                    function showSuccess(message) {
                        document.getElementById('successMessage').textContent = message;
                        successSection.style.display = 'block';
                    }

                    function hideMessages() {
                        errorSection.style.display = 'none';
                        successSection.style.display = 'none';
                    }

                    // Make functions globally available
                    window.generateReportFromId = function(reportId) {
                        showLoading('Generating PDF report...');
                        hideMessages();

                        fetch('/api/reports/generate-pdf', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ reportId })
                        })
                        .then(response => response.json())
                        .then(data => {
                            hideLoading();
                            
                            if (data.success) {
                                showSuccess('PDF report generated successfully');
                                // Optionally trigger download
                                if (data.data?.downloadUrl) {
                                    window.open(data.data.downloadUrl, '_blank');
                                }
                            } else {
                                showError(data.error || 'PDF generation failed');
                            }
                        })
                        .catch(error => {
                            hideLoading();
                            showError('PDF generation failed: ' + error.message);
                        });
                    };

                    window.viewReportDetails = function(reportId) {
                        // Navigate to report details page or show modal
                        window.location.href = \`/reports/\${reportId}\`;
                    };
                });
            </script>
        </body>
        </html>
    `;
} 