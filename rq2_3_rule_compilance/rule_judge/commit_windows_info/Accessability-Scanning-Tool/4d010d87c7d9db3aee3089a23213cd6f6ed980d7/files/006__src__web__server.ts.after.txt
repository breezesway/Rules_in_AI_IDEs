import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import path from 'path';
import { WorkflowOrchestrator } from '../utils/orchestration/workflow-orchestrator';
import { ErrorHandlerService } from '../utils/services/error-handler-service';
import { ConfigurationService } from '../utils/services/configuration-service';
import { createServer } from 'http';
import { Server as SocketIOServer } from 'socket.io';

export class WebServer {
    private app: express.Application;
    private server: any;
    private io: SocketIOServer;
    private orchestrator: WorkflowOrchestrator;
    private errorHandler: ErrorHandlerService;
    private config: ConfigurationService;
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
        this.setupMiddleware();
        this.setupRoutes(); // Setup API routes first
        this.setupStaticFiles(); // Setup static files after API routes
        this.setupWebSocket();
    }

    private setupMiddleware(): void {
        this.app.use(cors());
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
        // Serve static files from the public directory
        this.app.use(express.static(path.join(__dirname, '../public')));

        // Serve the main HTML file for all non-API routes (SPA)
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
                const { url, options = {} } = req.body;

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
                    ...options
                };

                // Store scan info
                this.activeScans.set(scanId, {
                    url,
                    startTime: new Date(),
                    status: 'starting',
                    type: 'full-site'
                });

                // Return scan ID immediately for real-time tracking
                res.json({
                    success: true,
                    data: {
                        scanId,
                        message: 'Full site scan started. Use the scan ID to track progress via WebSocket.'
                    }
                });

                // Start the scan in background with progress tracking
                this.runFullSiteScanWithProgress(scanId, url, scanOptions);

                return;

            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Full site scan failed');
                return res.status(500).json(errorResult);
            }
        });

        // Single page scan endpoint
        this.app.post('/api/scan/single-page', async (req, res) => {
            try {
                const { url } = req.body;

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

                // Generate scan ID for tracking
                const scanId = this.generateScanId();

                // Store scan info
                this.activeScans.set(scanId, {
                    url,
                    startTime: new Date(),
                    status: 'starting',
                    type: 'single-page'
                });

                // Return scan ID immediately for real-time tracking
                res.json({
                    success: true,
                    data: {
                        scanId,
                        message: 'Single page scan started. Use the scan ID to track progress via WebSocket.'
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

        // Regenerate reports endpoint
        this.app.post('/api/reports/regenerate', async (req, res) => {
            try {
                const reportsDir = path.join(process.cwd(), 'accessibility-reports');
                const historyDir = path.join(process.cwd(), 'accessibility-reports', 'history');
                const fs = require('fs');

                if (!fs.existsSync(reportsDir)) {
                    return res.status(404).json({
                        success: false,
                        error: 'No reports directory found'
                    });
                }

                // Look for JSON files in both reports directory and history directory
                const allReportFiles: Array<{ filename: string; path: string; mtime: Date }> = [];

                // Check main reports directory
                if (fs.existsSync(reportsDir)) {
                    const reportFiles = fs.readdirSync(reportsDir).filter((file: string) =>
                        file.endsWith('.json') && file.includes('accessibility-report')
                    );

                    reportFiles.forEach((file: string) => {
                        const filePath = path.join(reportsDir, file);
                        const stats = fs.statSync(filePath);
                        allReportFiles.push({
                            filename: file,
                            path: filePath,
                            mtime: stats.mtime
                        });
                    });
                }

                // Check history directory
                if (fs.existsSync(historyDir)) {
                    const historyFiles = fs.readdirSync(historyDir).filter((file: string) =>
                        file.endsWith('.json') && file.includes('accessibility-report')
                    );

                    historyFiles.forEach((file: string) => {
                        const filePath = path.join(historyDir, file);
                        const stats = fs.statSync(filePath);
                        allReportFiles.push({
                            filename: file,
                            path: filePath,
                            mtime: stats.mtime
                        });
                    });
                }

                if (allReportFiles.length === 0) {
                    return res.status(404).json({
                        success: false,
                        error: 'No accessibility reports found in reports or history directories'
                    });
                }

                // Sort by modification time to get the most recent first
                allReportFiles.sort((a, b) => b.mtime.getTime() - a.mtime.getTime());

                const reports = [];
                for (const reportFile of allReportFiles) {
                    try {
                        const reportData = JSON.parse(fs.readFileSync(reportFile.path, 'utf8'));
                        reports.push({
                            filename: reportFile.filename,
                            path: reportFile.path,
                            data: reportData,
                            lastModified: reportFile.mtime.toISOString()
                        });
                    } catch (error) {
                        this.errorHandler.handleError(error, `Failed to read ${reportFile.filename}`);
                    }
                }

                return res.json({
                    success: true,
                    data: {
                        reports,
                        count: reports.length
                    }
                });
            } catch (error) {
                const errorResult = this.errorHandler.handleError(error, 'Report regeneration failed');
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
    }

    private async runFullSiteScanWithProgress(scanId: string, url: string, options: any): Promise<void> {
        try {
            // Update scan status
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'running'
            });

            // Phase 0: Cleanup old reports (0-5%)
            this.emitProgressUpdate(scanId, 'cleanup', 0, 'Cleaning up old reports...');
            await this.orchestrator['cleanupReportsDirectory']();
            this.emitProgressUpdate(scanId, 'cleanup', 5, 'Cleanup completed');

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

            // Phase 4: Report Generation (80-100%)
            this.emitProgressUpdate(scanId, 'reporting', 85, 'Generating reports...');
            const reportPaths = await this.orchestrator.generateReports(analysisResults, url);
            this.emitProgressUpdate(scanId, 'reporting', 100, 'Reports generated successfully');

            // Update scan status to completed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'completed',
                results: {
                    crawlResults,
                    analysisResults,
                    reportPaths
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
                    reportPaths
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

            // Phase 0: Cleanup old reports (0-5%)
            this.emitProgressUpdate(scanId, 'cleanup', 0, 'Cleaning up old reports...');
            await this.orchestrator['cleanupReportsDirectory']();
            this.emitProgressUpdate(scanId, 'cleanup', 5, 'Cleanup completed');

            // Phase 1: Browser Initialization (5-15%)
            this.emitProgressUpdate(scanId, 'browser-init', 5, 'Initializing browser...');
            await this.orchestrator.browserManager.initialize();
            this.emitProgressUpdate(scanId, 'browser-init', 15, 'Browser initialized successfully');

            // Phase 2: Single Page Analysis (15-80%)
            this.emitProgressUpdate(scanId, 'analysis', 15, 'Starting single page analysis...');
            const analysisResults = await this.orchestrator.testSinglePage(url);
            this.emitProgressUpdate(scanId, 'analysis', 80, 'Single page analysis completed');

            // Phase 3: Report Generation (80-100%)
            this.emitProgressUpdate(scanId, 'reporting', 85, 'Generating reports...');
            const reportPaths = await this.orchestrator.generateReports(analysisResults, url);
            this.emitProgressUpdate(scanId, 'reporting', 100, 'Reports generated successfully');

            // Update scan status to completed
            this.activeScans.set(scanId, {
                ...this.activeScans.get(scanId),
                status: 'completed',
                results: {
                    analysisResults,
                    reportPaths
                },
                completedAt: new Date()
            });

            // Emit completion event
            this.io.to(scanId).emit('scan-completed', {
                scanId,
                success: true,
                data: {
                    analysisResults,
                    reportPaths
                }
            });

        } catch (error) {
            this.errorHandler.handleError(error, 'Single page scan failed');

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
            console.log(`🌐 Web interface available at: http://localhost:${this.port}`);
        });
    }
}

// Start the server if this file is run directly
if (require.main === module) {
    const server = new WebServer();
    server.start();
} 