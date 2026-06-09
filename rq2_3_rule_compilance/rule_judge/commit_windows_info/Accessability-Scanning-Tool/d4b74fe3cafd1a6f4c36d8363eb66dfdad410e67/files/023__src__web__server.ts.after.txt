import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env.local
dotenv.config({ path: path.resolve(process.cwd(), '.env.local') });
import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import { WorkflowOrchestrator } from '@/utils/orchestration/workflow-orchestrator';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { DatabaseService } from '@/utils/services/database-service';
import { DatabaseCleanupService } from '@/utils/services/database-cleanup-service';
import { SiteWideAccessibilityReport } from '@/core/types/common';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';

export class WebServer {
    private app: express.Application;
    private server: any;
    private io: SocketIOServer;
    private orchestrator: WorkflowOrchestrator;
    private errorHandler: ErrorHandlerService;
    private config: ConfigurationService;
    private databaseService: DatabaseService;
    private databaseCleanupService: DatabaseCleanupService;
    private activeScans: Map<string, any> = new Map();

    constructor(private port: number = 3000) {
        this.app = express();
        this.server = createServer(this.app);
        this.io = new SocketIOServer(this.server, {
            cors: {
                origin: "*",
                methods: ["GET", "POST"]
            }
        });
        this.orchestrator = new WorkflowOrchestrator();
        this.errorHandler = ErrorHandlerService.getInstance();
        this.config = ConfigurationService.getInstance();
        this.databaseService = DatabaseService.getInstance();
        this.databaseCleanupService = DatabaseCleanupService.getInstance();
        this.setupMiddleware();
        this.setupRoutes(); // Setup API routes first
        this.setupStaticFiles(); // Setup static files after API routes
        this.setupWebSocket();
    }

    private setupMiddleware(): void {
        this.app.use(cors({
            origin: "*",
            methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allowedHeaders: ["Content-Type", "Authorization", "X-Requested-With"],
            credentials: true
        }));
        this.app.use(bodyParser.json());
    }

    private setupWebSocket(): void {
        this.io.on('connection', (socket) => {
            this.errorHandler.logInfo('Client connected to WebSocket', { socketId: socket.id });

            socket.on('disconnect', () => {
                this.errorHandler.logInfo('Client disconnected from WebSocket', { socketId: socket.id });
            });

            socket.on('join-scan', (scanId: string) => {
                socket.join(scanId);
                this.errorHandler.logInfo('Client joined scan room', { socketId: socket.id, scanId });
            });
        });
    }

    private emitProgressUpdate(scanId: string, stage: string, progress: number, message: string, details?: any): void {
        this.io.to(scanId).emit('progress-update', {
            scanId,
            stage,
            progress,
            message,
            details,
            timestamp: new Date().toISOString()
        });
    }

    private generateScanId(): string {
        return `scan-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    private setupStaticFiles(): void {
        // Import page components
        const { renderLandingPage } = require('../components/LandingPage');
        const { renderSinglePageScanPage } = require('../components/SinglePageScanPage');
        const { renderFullSiteScanPage } = require('../components/FullSiteScanPage');
        const { renderReportsPage } = require('../components/ReportsPage');
        const { renderReportDetailsPage } = require('../components/ReportDetailsPage');

        // Handle specific page routes BEFORE static files
        this.app.get('/', (req, res) => {
            res.send(renderLandingPage());
        });

        this.app.get('/single-page', (req, res) => {
            res.send(renderSinglePageScanPage());
        });

        this.app.get('/full-site', (req, res) => {
            res.send(renderFullSiteScanPage());
        });

        this.app.get('/reports', (req, res) => {
            res.send(renderReportsPage());
        });

        // Report details page route
        this.app.get('/reports/:reportId', (req, res) => {
            const { reportId } = req.params;
            res.send(renderReportDetailsPage({ reportId }));
        });

        // Serve static files from the public directory (CSS, JS, images)
        this.app.use(express.static(path.join(__dirname, '../public')));

        // Serve the main HTML file for all other non-API routes (SPA)
        this.app.get('*', (req, res) => {
            // Skip API routes - let them be handled by the API route handlers
            if (req.path.startsWith('/api/')) {
                return res.status(404).json({
                    success: false,
                    error: 'API endpoint not found'
                });
            }
            return res.sendFile(path.join(__dirname, '../public/index.html'));
        });
    }

    private setupRoutes(): void {
        // Health check endpoint
        this.app.get('/api/health', (req, res) => {
            res.json({
                status: 'healthy',
                timestamp: new Date().toISOString(),
                version: '2.1.1'
            });
        });

        // Full site scan endpoint
        this.app.post('/api/scan/full-site', async (req, res) => {
            try {
                const { url, wcagLevel = 'WCAG2AA', options = {} } = req.body;

                if (!url) {
                    return res.status(400).json({
                        success: false,
                        error: 'URL is required'
                    });
                }

                // Validate URL
                try {
                    new URL(url);
                } catch {
                    return res.status(400).json({
                        success: false,
                        error: 'Invalid URL format'
                    });
                }

                // Validate WCAG level
                const validWcagLevels = ['WCAG2A', 'WCAG2AA', 'WCAG2AAA', 'WCAG22A', 'WCAG22AA', 'WCAG22AAA'];
                if (!validWcagLevels.includes(wcagLevel)) {
                    return res.status(400).json({
                        success: false,
                        error: 'Invalid WCAG level. Must be one of: WCAG2A, WCAG2AA, WCAG2AAA, WCAG22A, WCAG22AA, WCAG22AAA'
                    });
                }

                // Generate scan ID for tracking
                const scanId = this.generateScanId();

                // Default options for full site scan
                const scanOptions = {
                    maxPages: 50,
                    maxDepth: 4,
                    maxConcurrency: 5,
                    enablePerformanceMonitoring: false,
                    retryFailedPages: true,
                    generateReports: true,
                    wcagLevel,
                    ...options
                };

                // Store scan info
                this.activeScans.set(scanId, {
                    url,
                    wcagLevel,
                    startTime: new Date(),
                    status: 'starting',
                    type: 'full-site'
                });

                // Return scan ID immediately for real-time tracking
                res.json({
                    success: true,
                    data: {
                        scanId,
                        message: `Full site scan started with ${wcagLevel} compliance. Use the scan ID to track progress via WebSocket.`
                    }
                });

                // Start the scan in background with progress tracking
                this.runFullSiteScanWithProgress(scanId, url, { wcagLevel });

                return;

            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Full site scan failed');
                return res.status(500).json(errorResult);
            }
        });

        // Single page scan endpoint
        this.app.post('/api/scan/single-page', async (req, res) => {
            try {
                const { url, wcagLevel = 'WCAG2AA' } = req.body;

                if (!url) {
                    return res.status(400).json({
                        success: false,
                        error: 'URL is required'
                    });
                }

                // Validate URL
                try {
                    new URL(url);
                } catch {
                    return res.status(400).json({
                        success: false,
                        error: 'Invalid URL format'
                    });
                }

                // Validate WCAG level
                const validWcagLevels = ['WCAG2A', 'WCAG2AA', 'WCAG2AAA', 'WCAG22A', 'WCAG22AA', 'WCAG22AAA'];
                if (!validWcagLevels.includes(wcagLevel)) {
                    return res.status(400).json({
                        success: false,
                        error: 'Invalid WCAG level. Must be one of: WCAG2A, WCAG2AA, WCAG2AAA, WCAG22A, WCAG22AA, WCAG22AAA'
                    });
                }

                // Generate scan ID for tracking
                const scanId = this.generateScanId();

                // Store scan info
                this.activeScans.set(scanId, {
                    url,
                    wcagLevel,
                    startTime: new Date(),
                    status: 'starting',
                    type: 'single-page'
                });

                // Return scan ID immediately for real-time tracking
                res.json({
                    success: true,
                    data: {
                        scanId,
                        message: `Single page scan started with ${wcagLevel} compliance. Use the scan ID to track progress via WebSocket.`
                    }
                });

                // Start the scan in background with progress tracking
                this.runSinglePageScanWithProgress(scanId, url);

                return;

            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Single page scan failed');
                return res.status(500).json(errorResult);
            }
        });





        // Generate reports endpoint - list available reports (kept for backward compatibility)
        this.app.post('/api/reports/generate', async (req, res) => {
            try {
                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to initialize database service: ${initResult.message}`
                        });
                    }
                }

                // Get reports from database
                const dbResult = await this.databaseService.getReports({
                    limit: 50,
                    orderBy: 'createdAt',
                    orderDirection: 'desc'
                });

                if (!dbResult.success) {
                    return res.status(500).json({
                        success: false,
                        error: `Failed to retrieve reports from database: ${dbResult.message}`
                    });
                }

                const dbReports = dbResult.data || [];

                if (dbReports.length === 0) {
                    return res.status(404).json({
                        success: false,
                        error: 'No reports found in database. Please run a scan first.'
                    });
                }

                // Convert database reports to the expected format
                const reports = dbReports.map(report => {
                    if (!report) return null;
                    return {
                        id: report._id.toString(),
                        filename: `accessibility-report-${report._id.toString()}.json`,
                        path: `db://${report._id.toString()}`,
                        data: report.reportData,
                        lastModified: report.createdAt,
                        source: 'database',
                        reportType: report.reportType,
                        siteUrl: report.siteUrl
                    };
                }).filter(Boolean);

                return res.json({
                    success: true,
                    data: {
                        reports,
                        count: reports.length,
                        source: 'database'
                    }
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to retrieve reports for generation');
                return res.status(500).json(errorResult);
            }
        });

        // Download PDF reports endpoint
        this.app.get('/api/reports/download/:filename', (req, res) => {
            try {
                const { filename } = req.params;

                if (!filename) {
                    return res.status(400).json({
                        success: false,
                        error: 'Filename is required'
                    });
                }

                const reportsDir = path.join(process.cwd(), 'accessibility-reports');
                const filePath = path.join(reportsDir, filename);

                // Check if file exists
                if (!require('fs').existsSync(filePath)) {
                    return res.status(404).json({
                        success: false,
                        error: 'PDF file not found'
                    });
                }

                // Set headers for file download
                res.setHeader('Content-Type', 'application/pdf');
                res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);

                // Stream the file
                const fileStream = require('fs').createReadStream(filePath);
                fileStream.pipe(res);

                // Delete the file after download
                fileStream.on('end', () => {
                    try {
                        require('fs').unlinkSync(filePath);
                        this.errorHandler.logInfo(`PDF file deleted after download: ${filename}`);
                    } catch (error) {
                        this.errorHandler.logWarning(`Failed to delete PDF file after download: ${filename}`, { error });
                    }
                });

                return; // Explicit return for TypeScript

            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'PDF download failed');
                return res.status(500).json(errorResult);
            }
        });

        // Generate PDF reports endpoint
        this.app.post('/api/reports/generate-pdf', async (req, res) => {
            try {
                const { reportId, audience, generateAll } = req.body;

                if (!reportId) {
                    return res.status(400).json({
                        success: false,
                        error: 'Report ID is required'
                    });
                }

                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to initialize database service: ${initResult.message}`
                        });
                    }
                }

                // Get report from database
                const dbResult = await this.databaseService.getReportById(reportId);

                if (!dbResult.success) {
                    return res.status(404).json({
                        success: false,
                        error: `Report not found: ${dbResult.message}`
                    });
                }

                const report = dbResult.data;

                if (!report) {
                    return res.status(404).json({
                        success: false,
                        error: 'Report data not found'
                    });
                }

                // Initialize browser manager for PDF generation
                await this.orchestrator.browserManager.initialize();

                // Check if the report data is a SiteWideAccessibilityReport
                if (report.reportType === 'site-wide') {
                    // Generate PDF reports with scan metadata from database
                    const pdfResults = await this.orchestrator.generatePdfReportsFromStoredData(
                        report.reportData as SiteWideAccessibilityReport,
                        {
                            reportId,
                            audience,
                            generateAll,
                            ...(report.metadata && { scanMetadata: report.metadata })
                        }
                    );

                    if (!pdfResults.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to generate PDF reports: ${pdfResults.message}`
                        });
                    }

                    return res.json({
                        success: true,
                        data: {
                            reportId,
                            pdfFiles: pdfResults.data || [],
                            count: pdfResults.data?.length || 0
                        }
                    });
                } else {
                    return res.status(400).json({
                        success: false,
                        error: 'Only site-wide reports can be used to generate PDF reports'
                    });
                }
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'PDF generation failed');
                return res.status(500).json(errorResult);
            }
        });

        // Download PDF endpoint
        this.app.get('/api/reports/download/:filename', async (req, res) => {
            try {
                const { filename } = req.params;

                if (!filename) {
                    return res.status(400).json({
                        success: false,
                        error: 'Filename is required'
                    });
                }

                const filePath = path.join(process.cwd(), 'accessibility-reports', filename);

                if (!require('fs').existsSync(filePath)) {
                    return res.status(404).json({
                        success: false,
                        error: 'PDF file not found'
                    });
                }

                res.download(filePath, filename, (err) => {
                    if (err) {
                        this.errorHandler.handleError(err, 'PDF download failed');
                    } else {
                        // Delete the file after successful download
                        require('fs').unlinkSync(filePath);
                        this.errorHandler.logInfo(`PDF file deleted after download: ${filename}`);
                    }
                });
                return;
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'PDF download failed');
                return res.status(500).json(errorResult);
            }
        });

        // Get report by ID endpoint
        this.app.get('/api/reports/:reportId', async (req, res) => {
            try {
                const { reportId } = req.params;

                if (!reportId) {
                    return res.status(400).json({
                        success: false,
                        error: 'Report ID is required'
                    });
                }

                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to initialize database service: ${initResult.message}`
                        });
                    }
                }

                // Get report from database
                const dbResult = await this.databaseService.getReportById(reportId);

                if (!dbResult.success) {
                    return res.status(404).json({
                        success: false,
                        error: `Report not found: ${dbResult.message}`
                    });
                }

                const report = dbResult.data;

                if (!report) {
                    return res.status(404).json({
                        success: false,
                        error: 'Report data not found'
                    });
                }

                return res.json({
                    success: true,
                    data: {
                        id: report._id.toString(),
                        filename: `accessibility-report-${report._id.toString()}.json`,
                        path: `db://${report._id.toString()}`,
                        data: report.reportData,
                        lastModified: report.createdAt,
                        source: 'database',
                        reportType: report.reportType,
                        siteUrl: report.siteUrl,
                        metadata: report.metadata
                    }
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to retrieve report');
                return res.status(500).json(errorResult);
            }
        });

        // Get report statistics endpoint
        this.app.get('/api/reports/stats', async (req, res) => {
            try {
                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to initialize database service: ${initResult.message}`
                        });
                    }
                }

                // Get report statistics from database
                const statsResult = await this.databaseService.getReportStatistics();

                if (!statsResult.success) {
                    return res.status(500).json({
                        success: false,
                        error: `Failed to retrieve report statistics: ${statsResult.message}`
                    });
                }

                return res.json({
                    success: true,
                    data: statsResult.data
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to retrieve report statistics');
                return res.status(500).json(errorResult);
            }
        });



        // Enhanced search reports endpoint with advanced filters
        this.app.post('/api/reports/search', async (req, res) => {
            try {
                const {
                    siteUrl,
                    dateFrom,
                    dateTo,
                    reportType,
                    wcagLevel,
                    minViolations,
                    maxViolations,
                    minCompliance,
                    scanType
                } = req.body;

                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        return res.status(500).json({
                            success: false,
                            error: `Failed to initialize database service: ${initResult.message}`
                        });
                    }
                }

                // Build search options
                const searchOptions: any = {
                    limit: 100,
                    orderBy: 'createdAt',
                    orderDirection: 'desc'
                };

                // Add filters if provided
                if (siteUrl && siteUrl.trim()) {
                    searchOptions.siteUrl = siteUrl.trim();
                }

                if (dateFrom) {
                    try {
                        searchOptions.dateFrom = new Date(dateFrom);
                    } catch (error) {
                        return res.status(400).json({
                            success: false,
                            error: 'Invalid dateFrom format. Use ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)'
                        });
                    }
                }

                if (dateTo) {
                    try {
                        searchOptions.dateTo = new Date(dateTo);
                    } catch (error) {
                        return res.status(400).json({
                            success: false,
                            error: 'Invalid dateTo format. Use ISO 8601 format (YYYY-MM-DDTHH:mm:ss.sssZ)'
                        });
                    }
                }

                if (reportType) {
                    searchOptions.reportType = reportType;
                }

                if (wcagLevel) {
                    searchOptions.wcagLevel = wcagLevel;
                }

                if (scanType) {
                    searchOptions.scanType = scanType;
                }

                if (minViolations !== undefined) {
                    searchOptions.minViolations = parseInt(minViolations);
                }

                if (maxViolations !== undefined) {
                    searchOptions.maxViolations = parseInt(maxViolations);
                }

                if (minCompliance !== undefined) {
                    searchOptions.minCompliance = parseFloat(minCompliance);
                }

                // Get reports from database with filters
                const dbResult = await this.databaseService.getReportsWithMetadata(searchOptions);

                if (!dbResult.success) {
                    return res.status(500).json({
                        success: false,
                        error: `Failed to search reports in database: ${dbResult.message}`
                    });
                }

                const dbReports = dbResult.data || [];

                if (dbReports.length === 0) {
                    return res.status(404).json({
                        success: false,
                        error: 'No reports found matching your search criteria.'
                    });
                }

                // Convert database reports to the expected format
                const reports = dbReports.map(report => {
                    if (!report) return null;
                    return {
                        id: report._id.toString(),
                        filename: `accessibility-report-${report._id.toString()}.json`,
                        path: `db://${report._id.toString()}`,
                        data: report.reportData,
                        lastModified: report.createdAt,
                        source: 'database',
                        reportType: report.reportType,
                        siteUrl: report.siteUrl,
                        metadata: report.metadata
                    };
                }).filter(Boolean);

                return res.json({
                    success: true,
                    data: {
                        reports,
                        count: reports.length,
                        source: 'database',
                        searchCriteria: {
                            siteUrl: siteUrl || null,
                            dateFrom: dateFrom || null,
                            dateTo: dateTo || null,
                            reportType: reportType || null,
                            wcagLevel: wcagLevel || null,
                            minViolations: minViolations || null,
                            maxViolations: maxViolations || null,
                            minCompliance: minCompliance || null,
                            scanType: scanType || null
                        }
                    }
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to search reports');
                return res.status(500).json(errorResult);
            }
        });



        // Database statistics endpoint
        this.app.get('/api/database/statistics', async (req, res) => {
            try {
                const statsResult = await this.databaseCleanupService.getDatabaseStatistics();

                if (!statsResult.success) {
                    return res.status(500).json({
                        success: false,
                        error: `Failed to retrieve database statistics: ${statsResult.message}`
                    });
                }

                return res.json({
                    success: true,
                    data: statsResult.data
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to retrieve database statistics');
                return res.status(500).json(errorResult);
            }
        });

        // Database cleanup endpoint
        this.app.post('/api/database/cleanup', async (req, res) => {
            try {
                const {
                    testData = true,
                    orphanedReports = true,
                    expiredReports = false,
                    expirationDays = 30,
                    dryRun = false
                } = req.body;

                const cleanupOptions = {
                    testData,
                    orphanedReports,
                    expiredReports,
                    expirationDays,
                    dryRun
                };

                const cleanupResult = await this.databaseCleanupService.performCleanup(cleanupOptions);

                if (!cleanupResult.success) {
                    return res.status(500).json({
                        success: false,
                        error: `Failed to perform database cleanup: ${cleanupResult.message}`
                    });
                }

                return res.json({
                    success: true,
                    message: cleanupResult.message,
                    data: cleanupResult.data
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Failed to perform database cleanup');
                return res.status(500).json(errorResult);
            }
        });

        // Get scan status endpoint
        this.app.get('/api/scan/status', (req, res) => {
            const { scanId } = req.query;

            if (scanId && typeof scanId === 'string') {
                const scan = this.activeScans.get(scanId);
                if (scan) {
                    return res.json({
                        success: true,
                        data: scan
                    });
                } else {
                    return res.status(404).json({
                        success: false,
                        error: 'Scan not found'
                    });
                }
            }

            // Return all active scans
            const activeScans = Array.from(this.activeScans.entries()).map(([id, scan]) => ({
                scanId: id,
                ...scan
            }));

            return res.json({
                success: true,
                data: {
                    activeScans: activeScans.length,
                    scans: activeScans
                }
            });
        });

        // Cancel scan endpoint
        this.app.post('/api/scan/cancel', async (req, res) => {
            try {
                const { scanId } = req.body;

                if (!scanId) {
                    return res.status(400).json({
                        success: false,
                        error: 'Scan ID is required'
                    });
                }

                const scan = this.activeScans.get(scanId);
                if (!scan) {
                    return res.status(404).json({
                        success: false,
                        error: 'Scan not found'
                    });
                }

                // Update scan status to cancelled
                this.activeScans.set(scanId, {
                    ...scan,
                    status: 'cancelled',
                    cancelledAt: new Date()
                });

                // Emit cancellation event
                this.io.to(scanId).emit('scan-cancelled', {
                    scanId,
                    message: 'Scan cancelled by user'
                });

                return res.json({
                    success: true,
                    data: {
                        message: 'Scan cancelled successfully'
                    }
                });

            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Cancel scan failed');
                return res.status(500).json(errorResult);
            }
        });
    }

    private async runFullSiteScanWithProgress(scanId: string, url: string, options: any): Promise<void> {
        try {
            // Update scan status
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'running'
            });

            // Phase 0: Initialization (0-5%)
            this.emitProgressUpdate(scanId, 'init', 0, 'Initializing scan...');
            this.emitProgressUpdate(scanId, 'init', 5, 'Initialization completed');

            // Phase 1: Browser Initialization (5-15%)
            this.emitProgressUpdate(scanId, 'browser-init', 5, 'Initializing browser...');
            await this.orchestrator.browserManager.initialize();
            this.emitProgressUpdate(scanId, 'browser-init', 15, 'Browser initialized successfully');

            // Phase 2: Site Crawling (15-35%)
            this.emitProgressUpdate(scanId, 'crawling', 15, 'Starting site crawling...');
            const crawlResults = await this.orchestrator.performSiteCrawling(url, {
                maxPages: options.maxPages,
                maxDepth: options.maxDepth,
                excludePatterns: options.excludePatterns
            });
            this.emitProgressUpdate(scanId, 'crawling', 35, `Site crawling completed. Found ${crawlResults.length} pages.`);

            // Phase 3: Accessibility Analysis (35-80%)
            this.emitProgressUpdate(scanId, 'analysis', 35, 'Starting accessibility analysis...');
            const analysisResults = await this.orchestrator.performAccessibilityAnalysis(crawlResults, {
                maxConcurrency: options.maxConcurrency,
                retryFailedPages: options.retryFailedPages
            });
            this.emitProgressUpdate(scanId, 'analysis', 80, `Accessibility analysis completed. Analyzed ${analysisResults.length} pages.`);

            // Phase 4: Store Results (80-100%)
            this.emitProgressUpdate(scanId, 'storing', 85, 'Storing results in database...');

            // Store results in database using the workflow orchestrator's database storage logic
            const scanStartTime = Date.now();
            const scanIdForMetadata = scanStartTime.toString();

            // Calculate performance metrics for database storage
            const totalScanTime = Date.now() - scanStartTime;
            const pagesWithViolations = analysisResults.filter(result => result.summary.totalViolations > 0).length;
            const successRate = analysisResults.length > 0 ? (analysisResults.length / crawlResults.length) * 100 : 0;
            const averageTimePerPage = analysisResults.length > 0 ? totalScanTime / analysisResults.length : 0;

            // Extract tools used from analysis results
            const toolsUsed = new Set<string>();
            analysisResults.forEach(result => {
                result.violations?.forEach(violation => {
                    violation.tools?.forEach(tool => toolsUsed.add(tool));
                });
            });

            // Prepare scan metadata for database storage
            const scanMetadata = {
                scanConfiguration: {
                    maxPages: options.maxPages,
                    maxDepth: options.maxDepth,
                    maxConcurrency: options.maxConcurrency,
                    retryFailedPages: options.retryFailedPages,
                    generateReports: false, // PDF generation is now separate
                    wcagLevel: options.wcagLevel || 'WCAG2AA'
                },
                performanceMetrics: {
                    totalScanTime,
                    averageTimePerPage,
                    successRate,
                    pagesAnalyzed: analysisResults.length,
                    pagesWithViolations
                },
                toolsUsed: Array.from(toolsUsed),
                scanId: scanIdForMetadata,
                scanType: 'full-site' as const,
                userAgent: await this.orchestrator.browserManager.getUserAgent(),
                crawlDepth: options.maxDepth,
                excludedPatterns: options.excludePatterns?.map((pattern: RegExp) => pattern.toString()) || []
            };

            // Store results in database
            const siteWideReport = this.orchestrator.convertAnalysisResultsToSiteWideReport(
                analysisResults,
                url,
                options.wcagLevel || 'WCAG2AA'
            );

            try {
                // Initialize database service if not already initialized
                if (!this.databaseService.isInitialized()) {
                    const initResult = await this.databaseService.initialize();
                    if (!initResult.success) {
                        this.errorHandler.logWarning('Failed to initialize database service for report storage', {
                            error: initResult.message
                        });
                    }
                }

                if (this.databaseService.isInitialized()) {
                    const storeResult = await this.databaseService.storeSiteWideReport(siteWideReport, scanMetadata);
                    if (storeResult.success) {
                        this.errorHandler.logSuccess('Scan results stored in database successfully', {
                            reportId: storeResult.data,
                            scanId: scanIdForMetadata
                        });
                    } else {
                        this.errorHandler.logWarning('Failed to store scan results in database', {
                            error: storeResult.message
                        });
                    }
                }
            } catch (error) {
                this.errorHandler.logWarning('Error storing scan results in database', { error });
            }

            this.emitProgressUpdate(scanId, 'storing', 100, 'Results stored successfully');

            // Update scan status to completed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'completed',
                results: {
                    crawlResults,
                    analysisResults,
                    reportPaths: [] // No PDF generation - reports stored in database
                },
                completedAt: new Date()
            });

            // Emit completion event
            this.io.to(scanId).emit('scan-completed', {
                scanId,
                success: true,
                data: {
                    crawlResults,
                    analysisResults,
                    reportPaths: [], // No PDF generation - reports stored in database
                    wcagLevel: options.wcagLevel || 'WCAG2AA' // Include WCAG level in results
                }
            });

        } catch (error) {
            this.errorHandler.handleError(error, 'Full site scan failed');

            // Update scan status to failed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'failed',
                error: error instanceof Error ? error.message : 'Unknown error',
                completedAt: new Date()
            });

            // Emit error event
            this.io.to(scanId).emit('scan-failed', {
                scanId,
                error: error instanceof Error ? error.message : 'Unknown error'
            });
        }
    }

    private async runSinglePageScanWithProgress(scanId: string, url: string): Promise<void> {
        try {
            // Update scan status
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'running'
            });

            // Phase 0: Initialization (0-5%)
            this.emitProgressUpdate(scanId, 'init', 0, 'Initializing scan...');
            this.emitProgressUpdate(scanId, 'init', 5, 'Initialization completed');

            // Phase 1: Browser Initialization (5-15%)
            this.emitProgressUpdate(scanId, 'browser-init', 5, 'Initializing browser...');
            await this.orchestrator.browserManager.initialize();
            this.emitProgressUpdate(scanId, 'browser-init', 15, 'Browser initialized successfully');

            // Phase 2: Single Page Analysis (15-80%)
            this.emitProgressUpdate(scanId, 'analysis', 15, 'Starting single page analysis...');

            // Prepare scan metadata
            const scanMetadata = {
                scanConfiguration: {
                    maxPages: 1,
                    maxDepth: 0,
                    maxConcurrency: 1,
                    retryFailedPages: false,
                    generateReports: false, // PDF generation is now separate
                    wcagLevel: this.activeScans.get(scanId)?.wcagLevel || 'WCAG2AA'
                },
                scanId,
                scanType: 'single-page' as const
            };

            const { analysisResults, reportPaths } = await this.orchestrator.testSinglePageWithReports(
                url,
                this.activeScans.get(scanId)?.wcagLevel || 'WCAG2AA',
                scanMetadata
            );

            this.emitProgressUpdate(scanId, 'analysis', 80, 'Single page analysis completed');
            this.emitProgressUpdate(scanId, 'storing', 100, 'Results stored successfully');

            // Update scan status to completed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'completed',
                results: {
                    analysisResults,
                    reportPaths
                }
            });

            // Emit completion event
            this.io.to(scanId).emit('scan-completed', {
                scanId,
                success: true,
                data: {
                    analysisResults,
                    reportPaths,
                    wcagLevel: this.activeScans.get(scanId)?.wcagLevel || 'WCAG2AA' // Include WCAG level in results
                }
            });

        } catch (error) {
            // Update scan status to failed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'failed',
                error: error instanceof Error ? error.message : 'Unknown error'
            });

            // Emit error event
            this.io.to(scanId).emit('scan-failed', {
                scanId,
                error: error instanceof Error ? error.message : 'Unknown error'
            });

            this.errorHandler.handleError(error, 'Single page scan failed');
        }
    }

    // Mock scan completion for testing purposes
    private async runMockScanWithProgress(scanId: string, url: string, isFullSite: boolean = false, wcagLevel?: string): Promise<void> {
        try {
            // Update scan status
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'running'
            });

            // Simulate scan progress for testing
            const stages = isFullSite ?
                ['cleanup', 'browser-init', 'crawling', 'analysis', 'reporting'] :
                ['cleanup', 'browser-init', 'analysis', 'reporting'];

            for (let i = 0; i < stages.length; i++) {
                const stage = stages[i];
                if (stage) {
                    const progress = (i / (stages.length - 1)) * 100;

                    this.emitProgressUpdate(scanId, stage, progress, `${stage}...`);

                    // Wait a bit between stages for realistic progress
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }

            // Mock results
            const mockResults = {
                url: url,
                wcagLevel: wcagLevel || 'WCAG2AA',
                violations: [],
                warnings: [],
                passes: [],
                summary: {
                    totalViolations: 0,
                    totalWarnings: 0,
                    totalPasses: 10,
                    complianceScore: 100
                }
            };

            // Update scan status to completed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'completed',
                results: mockResults,
                completedAt: new Date()
            });

            // Emit completion event
            this.io.to(scanId).emit('scan-completed', {
                scanId,
                success: true,
                data: mockResults
            });

        } catch (error) {
            this.errorHandler.handleError(error, 'Mock scan failed');

            // Update scan status to failed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'failed',
                error: error instanceof Error ? error.message : 'Unknown error',
                completedAt: new Date()
            });

            // Emit error event
            this.io.to(scanId).emit('scan-failed', {
                scanId,
                error: error instanceof Error ? error.message : 'Unknown error'
            });
        }
    }

    public start(): void {
        this.server.listen(this.port, () => {
            this.errorHandler.logInfo(`Web server started on port ${this.port}`);
            this.errorHandler.logInfo(`🌐 Web interface available at: http://localhost:${this.port}`);
        });
    }
}

// Start the server if this file is run directly
if (require.main === module) {
    const server = new WebServer();
    server.start();
} 