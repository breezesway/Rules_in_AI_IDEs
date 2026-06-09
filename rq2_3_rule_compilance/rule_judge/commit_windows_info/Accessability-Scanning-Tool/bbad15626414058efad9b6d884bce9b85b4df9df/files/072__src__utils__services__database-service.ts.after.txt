import { MongoClient, Db, Collection, ObjectId } from 'mongodb';
import { ConfigurationService } from './configuration-service';
import { ErrorHandlerService } from './error-handler-service';
import { ServiceResult, SiteWideAccessibilityReport, AccessibilityReport } from '@/core/types/common';

/**
 * Interface for database operation results
 */
export interface DatabaseResult<T = unknown> extends ServiceResult<T> {
    /** Optional database record ID */
    recordId?: string;
    /** Optional metadata about the operation */
    metadata?: {
        collectionName?: string;
        operation?: string;
        timestamp?: string;
        filtersApplied?: number;
    };
}

/**
 * Interface for stored reports in MongoDB
 */
export interface StoredReport {
    _id: ObjectId;
    siteUrl: string;
    reportType: 'site-wide' | 'single-page';
    reportData: SiteWideAccessibilityReport | AccessibilityReport;
    metadata?: {
        // Basic scan information
        totalPages?: number;
        totalViolations?: number;
        compliancePercentage?: number;
        wcagLevel?: string;

        // Violation breakdown
        criticalViolations?: number;
        seriousViolations?: number;
        moderateViolations?: number;
        minorViolations?: number;

        // Browser and viewport information
        browser?: string;
        viewport?: string;

        // Scan configuration
        scanConfiguration?: {
            maxPages?: number;
            maxDepth?: number;
            maxConcurrency?: number;
            retryFailedPages?: boolean;
            generateReports?: boolean;
            wcagLevel?: string;
        };

        // Performance metrics
        performanceMetrics?: {
            totalScanTime?: number;
            averageTimePerPage?: number;
            successRate?: number;
            pagesAnalyzed?: number;
            pagesWithViolations?: number;
        };

        // Tool information
        toolsUsed?: string[];

        // Timestamps
        scanStartedAt?: Date;
        scanCompletedAt?: Date;

        // Additional metadata
        scanId?: string;
        scanType?: 'full-site' | 'single-page' | 'quick';
        userAgent?: string;
        crawlDepth?: number;
        excludedPatterns?: string[];
    };
    createdAt: Date;
    updatedAt: Date;
}

/**
 * Interface for report query options
 */
export interface ReportQueryOptions {
    reportType?: 'site-wide' | 'single-page';
    siteUrl?: string;
    orderBy?: string;
    orderDirection?: 'asc' | 'desc';
    limit?: number;
    offset?: number;
}

/**
 * Interface for report statistics
 */
export interface ReportStatistics {
    totalReports: number;
    siteWideReports: number;
    singlePageReports: number;
    uniqueSites: number;
    oldestReport: string;
    newestReport: string;
}

/**
 * Singleton service for MongoDB database operations
 * Handles storage and retrieval of accessibility reports
 */
export class DatabaseService {
    private static instance: DatabaseService;
    private config = ConfigurationService.getInstance();
    private errorHandler = ErrorHandlerService.getInstance();
    private client: MongoClient | null = null;
    private db: Db | null = null;
    private collection: Collection<Omit<StoredReport, '_id'>> | null = null;

    private constructor() {
        // Private constructor to enforce singleton pattern
        if (DatabaseService.instance) {
            throw new Error(
                'Cannot instantiate DatabaseService directly. Use getInstance() instead.'
            );
        }
    }

    /**
     * Gets the singleton instance of DatabaseService
     * @returns DatabaseService instance
     */
    static getInstance(): DatabaseService {
        if (!DatabaseService.instance) {
            DatabaseService.instance = new DatabaseService();
        }
        return DatabaseService.instance;
    }

    /**
     * Initializes the MongoDB client and connection
     * @returns DatabaseResult indicating success or failure
     */
    async initialize(): Promise<DatabaseResult> {
        try {
            const mongoUrl = this.config.get('MONGODB_URL', 'mongodb://localhost:27017');
            const dbName = this.config.get('MONGODB_DB_NAME', 'accessibility_testing');

            if (!mongoUrl) {
                throw new Error('MongoDB configuration missing. Please set MONGODB_URL environment variable.');
            }

            this.client = new MongoClient(mongoUrl);
            await this.client.connect();

            // Test authentication with admin database
            try {
                await this.client.db('admin').command({ ping: 1 });
            } catch (authError) {
                const errorMessage = authError instanceof Error ? authError.message : 'Unknown authentication error';
                throw new Error(`MongoDB authentication failed. Please check your connection string and credentials. Error: ${errorMessage}`);
            }

            // Connect to the target database
            this.db = this.client.db(dbName);
            this.collection = this.db.collection<Omit<StoredReport, '_id'>>('accessibility_reports');

            // Create indexes for better query performance
            try {
                await this.collection.createIndex({ siteUrl: 1 });
                await this.collection.createIndex({ reportType: 1 });
                await this.collection.createIndex({ createdAt: -1 });
                await this.collection.createIndex({ updatedAt: -1 });
                await this.collection.createIndex({ siteUrl: 1, reportType: 1, createdAt: -1 });
            } catch (error) {
                // Log index creation error but don't fail initialization
                const errorMessage = error instanceof Error ? error.message : 'Unknown error';
                this.errorHandler.logWarning('Failed to create database indexes', { error: errorMessage });
            }

            // Test the connection
            await this.collection.findOne({});

            this.errorHandler.logSuccess('Database service initialized successfully');
            return {
                success: true,
                message: 'Database service initialized successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'initialization',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.initialize') as DatabaseResult;
        }
    }

    /**
     * Stores a site-wide accessibility report in the database
     * @param report The site-wide accessibility report to store
     * @param scanMetadata Optional additional scan metadata
     * @returns DatabaseResult with the stored record ID
     */
    async storeSiteWideReport(
        report: SiteWideAccessibilityReport,
        scanMetadata?: {
            scanConfiguration?: {
                maxPages?: number;
                maxDepth?: number;
                maxConcurrency?: number;
                retryFailedPages?: boolean;
                generateReports?: boolean;
                wcagLevel?: string;
            };
            performanceMetrics?: {
                totalScanTime?: number;
                averageTimePerPage?: number;
                successRate?: number;
                pagesAnalyzed?: number;
                pagesWithViolations?: number;
            };
            toolsUsed?: string[];
            scanId?: string;
            scanType?: 'full-site' | 'single-page' | 'quick';
            userAgent?: string;
            crawlDepth?: number;
            excludedPatterns?: string[];
        }
    ): Promise<DatabaseResult<string>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const now = new Date();

            // Extract tools used from violations
            const toolsUsed = new Set<string>();
            if (report.pageReports) {
                report.pageReports.forEach(pageReport => {
                    pageReport.violations?.forEach(violation => {
                        violation.tools?.forEach(tool => toolsUsed.add(tool));
                    });
                });
            }

            const document = {
                siteUrl: report.siteUrl,
                reportType: 'site-wide' as const,
                reportData: report,
                metadata: {
                    // Basic scan information
                    totalPages: report.summary?.totalPages || 0,
                    totalViolations: report.summary?.totalViolations || 0,
                    compliancePercentage: report.summary?.compliancePercentage || 0,
                    wcagLevel: report.wcagLevel || 'WCAG2AA',

                    // Violation breakdown
                    criticalViolations: report.summary?.criticalViolations || 0,
                    seriousViolations: report.summary?.seriousViolations || 0,
                    moderateViolations: report.summary?.moderateViolations || 0,
                    minorViolations: report.summary?.minorViolations || 0,

                    // Scan configuration
                    scanConfiguration: scanMetadata?.scanConfiguration || {},

                    // Performance metrics
                    performanceMetrics: scanMetadata?.performanceMetrics || {},

                    // Tool information
                    toolsUsed: Array.from(toolsUsed),

                    // Timestamps
                    scanStartedAt: scanMetadata?.scanId ? new Date(parseInt(scanMetadata.scanId)) : now,
                    scanCompletedAt: now,

                    // Additional metadata
                    ...(scanMetadata?.scanId && { scanId: scanMetadata.scanId }),
                    scanType: scanMetadata?.scanType || 'full-site',
                    ...(scanMetadata?.userAgent && { userAgent: scanMetadata.userAgent }),
                    ...(scanMetadata?.crawlDepth !== undefined && { crawlDepth: scanMetadata.crawlDepth }),
                    excludedPatterns: scanMetadata?.excludedPatterns || []
                },
                createdAt: now,
                updatedAt: now
            };

            const result = await this.collection.insertOne(document);

            this.errorHandler.logSuccess(`Site-wide report stored with ID: ${result.insertedId}`);
            return {
                success: true,
                data: result.insertedId.toString(),
                recordId: result.insertedId.toString(),
                message: 'Site-wide report stored successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'insert',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.storeSiteWideReport') as DatabaseResult<string>;
        }
    }

    /**
     * Stores a single-page accessibility report in the database
     * @param report The single-page accessibility report to store
     * @param scanMetadata Optional additional scan metadata
     * @returns DatabaseResult with the stored record ID
     */
    async storeSinglePageReport(
        report: AccessibilityReport,
        scanMetadata?: {
            scanConfiguration?: {
                maxPages?: number;
                maxDepth?: number;
                maxConcurrency?: number;
                retryFailedPages?: boolean;
                generateReports?: boolean;
                wcagLevel?: string;
            };
            performanceMetrics?: {
                totalScanTime?: number;
                averageTimePerPage?: number;
                successRate?: number;
                pagesAnalyzed?: number;
                pagesWithViolations?: number;
            };
            toolsUsed?: string[];
            scanId?: string;
            scanType?: 'full-site' | 'single-page' | 'quick';
            userAgent?: string;
            crawlDepth?: number;
            excludedPatterns?: string[];
        }
    ): Promise<DatabaseResult<string>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const now = new Date();

            // Extract tools used from violations
            const toolsUsed = new Set<string>();
            report.violations?.forEach(violation => {
                violation.tools?.forEach(tool => toolsUsed.add(tool));
            });

            const document = {
                siteUrl: report.url,
                reportType: 'single-page' as const,
                reportData: report,
                metadata: {
                    // Basic scan information
                    totalViolations: report.summary?.totalViolations || 0,
                    criticalViolations: report.summary?.criticalViolations || 0,
                    seriousViolations: report.summary?.seriousViolations || 0,
                    moderateViolations: report.summary?.moderateViolations || 0,
                    minorViolations: report.summary?.minorViolations || 0,

                    // Browser and viewport information
                    ...(report.browser && { browser: report.browser }),
                    ...(report.viewport && { viewport: report.viewport }),

                    // Scan configuration
                    scanConfiguration: scanMetadata?.scanConfiguration || {},

                    // Performance metrics
                    performanceMetrics: scanMetadata?.performanceMetrics || {},

                    // Tool information
                    toolsUsed: Array.from(toolsUsed),

                    // Timestamps
                    scanStartedAt: scanMetadata?.scanId ? new Date(parseInt(scanMetadata.scanId)) : now,
                    scanCompletedAt: now,

                    // Additional metadata
                    ...(scanMetadata?.scanId && { scanId: scanMetadata.scanId }),
                    scanType: scanMetadata?.scanType || 'single-page',
                    ...(scanMetadata?.userAgent && { userAgent: scanMetadata.userAgent }),
                    ...(scanMetadata?.crawlDepth !== undefined && { crawlDepth: scanMetadata.crawlDepth }),
                    excludedPatterns: scanMetadata?.excludedPatterns || []
                },
                createdAt: now,
                updatedAt: now
            };

            const result = await this.collection.insertOne(document);

            this.errorHandler.logSuccess(`Single-page report stored with ID: ${result.insertedId}`);
            return {
                success: true,
                data: result.insertedId.toString(),
                recordId: result.insertedId.toString(),
                message: 'Single-page report stored successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'insert',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.storeSinglePageReport') as DatabaseResult<string>;
        }
    }

    /**
     * Retrieves a specific report by ID
     * @param reportId The ID of the report to retrieve
     * @returns DatabaseResult with the stored report
     */
    async getReportById(reportId: string): Promise<DatabaseResult<StoredReport>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const objectId = new ObjectId(reportId);
            const report = await this.collection.findOne({ _id: objectId });

            if (!report) {
                throw new Error(`Report not found with ID: ${reportId}`);
            }

            return {
                success: true,
                data: report,
                recordId: report._id.toString(),
                message: 'Report retrieved successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'select',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.getReportById') as DatabaseResult<StoredReport>;
        }
    }

    /**
     * Retrieves reports with optional filtering and pagination
     * @param options Query options for filtering and pagination
     * @returns DatabaseResult with array of stored reports
     */
    async getReports(options: ReportQueryOptions = {}): Promise<DatabaseResult<StoredReport[]>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const filter: any = {};

            // Apply filters
            if (options.reportType) {
                filter.reportType = options.reportType;
            }

            if (options.siteUrl) {
                // Use case-insensitive regex for partial URL matching
                filter.siteUrl = {
                    $regex: options.siteUrl,
                    $options: 'i'
                };
            }

            // Build sort object
            const sort: any = {};
            const orderBy = options.orderBy || 'createdAt';
            const orderDirection = options.orderDirection || 'desc';
            sort[orderBy] = orderDirection === 'asc' ? 1 : -1;

            // Build query
            let query = this.collection.find(filter).sort(sort);

            // Apply pagination
            if (options.offset) {
                query = query.skip(options.offset);
            }

            if (options.limit) {
                query = query.limit(options.limit);
            }

            const reports = await query.toArray();

            return {
                success: true,
                data: reports,
                message: `Retrieved ${reports.length} reports`,
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'select',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.getReports') as DatabaseResult<StoredReport[]>;
        }
    }

    /**
     * Retrieves reports with enhanced filtering and metadata search
     * @param options Enhanced query options for filtering and pagination
     * @returns DatabaseResult with array of stored reports
     */
    async getReportsWithMetadata(options: {
        reportType?: 'site-wide' | 'single-page';
        siteUrl?: string;
        orderBy?: string;
        orderDirection?: 'asc' | 'desc';
        limit?: number;
        offset?: number;
        wcagLevel?: string;
        scanType?: 'full-site' | 'single-page' | 'quick';
        toolsUsed?: string[];
        minViolations?: number;
        maxViolations?: number;
        minCompliancePercentage?: number;
        maxCompliancePercentage?: number;
        dateFrom?: Date;
        dateTo?: Date;
        scanId?: string;
    } = {}): Promise<DatabaseResult<StoredReport[]>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const filter: any = {};

            // Apply basic filters
            if (options.reportType) {
                filter.reportType = options.reportType;
            }

            if (options.siteUrl) {
                // Use case-insensitive regex for partial URL matching
                filter.siteUrl = {
                    $regex: options.siteUrl,
                    $options: 'i'
                };
            }

            if (options.scanId) {
                filter['metadata.scanId'] = options.scanId;
            }

            // Apply metadata filters
            if (options.wcagLevel) {
                filter['metadata.wcagLevel'] = options.wcagLevel;
            }

            if (options.scanType) {
                filter['metadata.scanType'] = options.scanType;
            }

            if (options.toolsUsed && options.toolsUsed.length > 0) {
                filter['metadata.toolsUsed'] = { $in: options.toolsUsed };
            }

            if (options.minViolations !== undefined || options.maxViolations !== undefined) {
                filter['metadata.totalViolations'] = {};
                if (options.minViolations !== undefined) {
                    filter['metadata.totalViolations'].$gte = options.minViolations;
                }
                if (options.maxViolations !== undefined) {
                    filter['metadata.totalViolations'].$lte = options.maxViolations;
                }
            }

            if (options.minCompliancePercentage !== undefined || options.maxCompliancePercentage !== undefined) {
                filter['metadata.compliancePercentage'] = {};
                if (options.minCompliancePercentage !== undefined) {
                    filter['metadata.compliancePercentage'].$gte = options.minCompliancePercentage;
                }
                if (options.maxCompliancePercentage !== undefined) {
                    filter['metadata.compliancePercentage'].$lte = options.maxCompliancePercentage;
                }
            }

            // Apply date range filters
            if (options.dateFrom || options.dateTo) {
                filter.createdAt = {};
                if (options.dateFrom) {
                    filter.createdAt.$gte = options.dateFrom;
                }
                if (options.dateTo) {
                    filter.createdAt.$lte = options.dateTo;
                }
            }

            // Build sort object
            const sort: any = {};
            const orderBy = options.orderBy || 'createdAt';
            const orderDirection = options.orderDirection || 'desc';
            sort[orderBy] = orderDirection === 'asc' ? 1 : -1;

            // Build query
            let query = this.collection.find(filter).sort(sort);

            // Apply pagination
            if (options.offset) {
                query = query.skip(options.offset);
            }

            if (options.limit) {
                query = query.limit(options.limit);
            }

            const reports = await query.toArray();

            return {
                success: true,
                data: reports,
                message: `Retrieved ${reports.length} reports with metadata filtering`,
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'select_with_metadata',
                    timestamp: new Date().toISOString(),
                    filtersApplied: Object.keys(filter).length
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.getReportsWithMetadata') as DatabaseResult<StoredReport[]>;
        }
    }

    /**
     * Retrieves the most recent report for a given site URL
     * @param siteUrl The site URL to get the most recent report for
     * @param reportType Optional report type filter
     * @returns DatabaseResult with the most recent report
     */
    async getMostRecentReport(siteUrl: string, reportType?: 'site-wide' | 'single-page'): Promise<DatabaseResult<StoredReport>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const filter: any = { siteUrl };

            if (reportType) {
                filter.reportType = reportType;
            }

            const report = await this.collection.findOne(filter, {
                sort: { createdAt: -1 }
            });

            if (!report) {
                throw new Error(`No reports found for site: ${siteUrl}`);
            }

            return {
                success: true,
                data: report,
                recordId: report._id.toString(),
                message: 'Most recent report retrieved successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'select',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.getMostRecentReport') as DatabaseResult<StoredReport>;
        }
    }

    /**
     * Deletes a report by ID
     * @param reportId The ID of the report to delete
     * @returns DatabaseResult indicating success or failure
     */
    async deleteReport(reportId: string): Promise<DatabaseResult> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            const objectId = new ObjectId(reportId);
            const result = await this.collection.deleteOne({ _id: objectId });

            if (result.deletedCount === 0) {
                throw new Error(`Report not found with ID: ${reportId}`);
            }

            this.errorHandler.logSuccess(`Report deleted with ID: ${reportId}`);
            return {
                success: true,
                message: 'Report deleted successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'delete',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.deleteReport') as DatabaseResult;
        }
    }

    /**
     * Gets statistics about stored reports
     * @returns DatabaseResult with report statistics
     */
    async getReportStatistics(): Promise<DatabaseResult<ReportStatistics>> {
        try {
            if (!this.collection) {
                throw new Error('Database service not initialized. Call initialize() first.');
            }

            // Get total count
            const totalReports = await this.collection.countDocuments();

            // Get site-wide count
            const siteWideReports = await this.collection.countDocuments({ reportType: 'site-wide' });

            // Get single-page count
            const singlePageReports = await this.collection.countDocuments({ reportType: 'single-page' });

            // Get unique sites count
            const uniqueSites = await this.collection.distinct('siteUrl').then(urls => urls.length);

            // Get date range
            const dateRange = await this.collection.aggregate([
                {
                    $group: {
                        _id: null,
                        oldestReport: { $min: '$createdAt' },
                        newestReport: { $max: '$createdAt' }
                    }
                }
            ]).toArray();

            const oldestReport = dateRange[0]?.['oldestReport']?.toISOString() || '';
            const newestReport = dateRange[0]?.['newestReport']?.toISOString() || '';

            const statistics: ReportStatistics = {
                totalReports,
                siteWideReports,
                singlePageReports,
                uniqueSites,
                oldestReport,
                newestReport
            };

            return {
                success: true,
                data: statistics,
                message: 'Report statistics retrieved successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'aggregate',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.getReportStatistics') as DatabaseResult<ReportStatistics>;
        }
    }

    /**
     * Closes the database connection
     * @returns DatabaseResult indicating success or failure
     */
    async close(): Promise<DatabaseResult> {
        try {
            if (this.client) {
                await this.client.close();
                this.client = null;
                this.db = null;
                this.collection = null;
            }

            this.errorHandler.logSuccess('Database connection closed successfully');
            return {
                success: true,
                message: 'Database connection closed successfully',
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'close',
                    timestamp: new Date().toISOString()
                }
            };
        } catch (error) {
            return this.errorHandler.handleError(error, 'DatabaseService.close') as DatabaseResult;
        }
    }

    /**
     * Checks if the database service is properly initialized
     * @returns True if initialized, false otherwise
     */
    isInitialized(): boolean {
        return this.client !== null && this.db !== null && this.collection !== null;
    }
} 