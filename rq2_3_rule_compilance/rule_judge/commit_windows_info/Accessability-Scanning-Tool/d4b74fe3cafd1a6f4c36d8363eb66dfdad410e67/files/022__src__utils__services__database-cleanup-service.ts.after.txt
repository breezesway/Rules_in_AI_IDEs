import { DatabaseService } from './database-service';
import { ErrorHandlerService } from './error-handler-service';
import { ConfigurationService } from './configuration-service';
import { ServiceResult } from '@/core/types/common';

/**
 * Interface for cleanup operation results
 */
export interface CleanupResult extends ServiceResult {
    /** Number of records cleaned up */
    recordsCleaned?: number;
    /** Type of cleanup performed */
    cleanupType?: 'test-data' | 'orphaned-reports' | 'expired-reports' | 'all';
    /** Timestamp of cleanup operation */
    cleanupTimestamp?: string;
    /** Additional metadata about the cleanup */
    metadata?: {
        collectionsCleaned?: string[];
        spaceFreed?: number;
        errorsEncountered?: string[];
    };
}

/**
 * Interface for cleanup options
 */
export interface CleanupOptions {
    /** Clean up test data (default: true) */
    testData?: boolean;
    /** Clean up orphaned reports (default: true) */
    orphanedReports?: boolean;
    /** Clean up expired reports older than specified days (default: 30) */
    expiredReports?: boolean;
    /** Number of days after which reports are considered expired */
    expirationDays?: number;
    /** Clean up all data (use with caution) */
    allData?: boolean;
    /** Dry run mode - don't actually delete anything */
    dryRun?: boolean;
}

/**
 * Database Cleanup Service
 * 
 * Handles cleanup of test data, orphaned reports, and database maintenance
 * operations. This service is critical for maintaining database integrity
 * and preventing test data accumulation.
 */
export class DatabaseCleanupService {
    private static instance: DatabaseCleanupService;
    private databaseService = DatabaseService.getInstance();
    private errorHandler = ErrorHandlerService.getInstance();
    private configService = ConfigurationService.getInstance();

    private constructor() {
        // Private constructor for singleton pattern
    }

    /**
     * Get singleton instance
     */
    static getInstance(): DatabaseCleanupService {
        if (!DatabaseCleanupService.instance) {
            DatabaseCleanupService.instance = new DatabaseCleanupService();
        }
        return DatabaseCleanupService.instance;
    }

    /**
     * Perform comprehensive database cleanup
     */
    async performCleanup(options: CleanupOptions = {}): Promise<CleanupResult> {
        const errorHandler = this.errorHandler;

        try {
            // Initialize database service if not already initialized
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    return errorHandler.handleError(
                        new Error('Failed to initialize database service for cleanup'),
                        'Database cleanup initialization failed'
                    );
                }
            }

            const {
                testData = true,
                orphanedReports = true,
                expiredReports = true,
                expirationDays = 30,
                allData = false,
                dryRun = false
            } = options;

            let totalRecordsCleaned = 0;
            const errorsEncountered: string[] = [];
            const collectionsCleaned: string[] = [];

            // If allData is true, perform complete database cleanup
            if (allData) {
                try {
                    const allDataResult = await this.cleanupAllData(dryRun);
                    if (allDataResult.success && allDataResult.recordsCleaned) {
                        totalRecordsCleaned = allDataResult.recordsCleaned;
                        collectionsCleaned.push('all_data');
                    }
                    if (allDataResult.metadata?.errorsEncountered) {
                        errorsEncountered.push(...allDataResult.metadata.errorsEncountered);
                    }
                } catch (error) {
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    errorsEncountered.push(`All data cleanup failed: ${errorMessage}`);
                }
            } else {
                // Clean up test data
                if (testData) {
                    try {
                        const testDataResult = await this.cleanupTestData(dryRun);
                        if (testDataResult.success && testDataResult.recordsCleaned) {
                            totalRecordsCleaned += testDataResult.recordsCleaned;
                            collectionsCleaned.push('test_data');
                        }
                        if (testDataResult.metadata?.errorsEncountered) {
                            errorsEncountered.push(...testDataResult.metadata.errorsEncountered);
                        }
                    } catch (error) {
                        const errorMessage = error instanceof Error ? error.message : String(error);
                        errorsEncountered.push(`Test data cleanup failed: ${errorMessage}`);
                    }
                }

                // Clean up orphaned reports
                if (orphanedReports) {
                    try {
                        const orphanedResult = await this.cleanupOrphanedReports(dryRun);
                        if (orphanedResult.success && orphanedResult.recordsCleaned) {
                            totalRecordsCleaned += orphanedResult.recordsCleaned;
                            collectionsCleaned.push('orphaned_reports');
                        }
                        if (orphanedResult.metadata?.errorsEncountered) {
                            errorsEncountered.push(...orphanedResult.metadata.errorsEncountered);
                        }
                    } catch (error) {
                        const errorMessage = error instanceof Error ? error.message : String(error);
                        errorsEncountered.push(`Orphaned reports cleanup failed: ${errorMessage}`);
                    }
                }

                // Clean up expired reports
                if (expiredReports) {
                    try {
                        const expiredResult = await this.cleanupExpiredReports(expirationDays, dryRun);
                        if (expiredResult.success && expiredResult.recordsCleaned) {
                            totalRecordsCleaned += expiredResult.recordsCleaned;
                            collectionsCleaned.push('expired_reports');
                        }
                        if (expiredResult.metadata?.errorsEncountered) {
                            errorsEncountered.push(...expiredResult.metadata.errorsEncountered);
                        }
                    } catch (error) {
                        const errorMessage = error instanceof Error ? error.message : String(error);
                        errorsEncountered.push(`Expired reports cleanup failed: ${errorMessage}`);
                    }
                }
            }

            return {
                success: true,
                message: `Database cleanup completed successfully${dryRun ? ' (dry run)' : ''}`,
                data: {
                    recordsCleaned: totalRecordsCleaned,
                    cleanupType: allData ? 'all' : 'selective',
                    cleanupTimestamp: new Date().toISOString()
                },
                metadata: {
                    collectionsCleaned,
                    errorsEncountered: errorsEncountered.length > 0 ? errorsEncountered : []
                }
            };

        } catch (error) {
            return errorHandler.handleError(error, 'Database cleanup operation failed');
        }
    }

    /**
     * Clean up test data based on patterns
     */
    private async cleanupTestData(dryRun: boolean = false): Promise<CleanupResult> {
        try {
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    throw new Error('Failed to initialize database service for cleanup');
                }
            }

            // Identify test data patterns
            const testPatterns = [
                { siteUrl: { $regex: /test|example\.com|localhost/i } },
                { siteUrl: { $regex: /invalid-domain-that-does-not-exist-12345\.com/i } },
                { 'metadata.scanId': { $regex: /test|mock|fake/i } },
                { 'metadata.scanType': 'test' },
                { siteUrl: { $regex: /127\.0\.0\.1|localhost/i } }
            ];

            const query = { $or: testPatterns };

            if (dryRun) {
                // Count test records without deleting
                const testRecords = await this.databaseService.getReportsWithMetadata({
                    siteUrl: 'test',
                    limit: 1000
                });

                return {
                    success: true,
                    message: `Found ${testRecords.data?.length || 0} test records (dry run)`,
                    recordsCleaned: testRecords.data?.length || 0,
                    cleanupType: 'test-data',
                    cleanupTimestamp: new Date().toISOString()
                };
            }

            // Perform actual deletion using MongoDB collection
            const collection = (this.databaseService as any).collection;
            if (!collection) {
                throw new Error('Database collection not available for cleanup');
            }

            const deleteResult = await collection.deleteMany(query);
            const deletedCount = deleteResult.deletedCount || 0;

            this.errorHandler.logSuccess(`Test data cleanup completed: ${deletedCount} records deleted`);

            return {
                success: true,
                message: `Test data cleanup completed: ${deletedCount} records deleted`,
                recordsCleaned: deletedCount,
                cleanupType: 'test-data',
                cleanupTimestamp: new Date().toISOString(),
                metadata: {
                    collectionsCleaned: ['accessibility_reports'],
                    spaceFreed: 0, // Could calculate this if needed
                    errorsEncountered: []
                }
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'Test data cleanup failed');
        }
    }

    /**
     * Clean up orphaned reports (reports without proper metadata)
     */
    private async cleanupOrphanedReports(dryRun: boolean = false): Promise<CleanupResult> {
        try {
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    throw new Error('Failed to initialize database service for cleanup');
                }
            }

            // Identify orphaned reports (missing required metadata)
            const orphanedQuery = {
                $or: [
                    { 'metadata.scanId': { $exists: false } },
                    { 'metadata.scanType': { $exists: false } },
                    { 'metadata.scanStartedAt': { $exists: false } },
                    { siteUrl: { $exists: false } }
                ]
            };

            if (dryRun) {
                // Count orphaned records without deleting
                const collection = (this.databaseService as any).collection;
                if (!collection) {
                    throw new Error('Database collection not available for cleanup');
                }

                const orphanedCount = await collection.countDocuments(orphanedQuery);

                return {
                    success: true,
                    message: `Found ${orphanedCount} orphaned records (dry run)`,
                    recordsCleaned: orphanedCount,
                    cleanupType: 'orphaned-reports',
                    cleanupTimestamp: new Date().toISOString()
                };
            }

            // Perform actual deletion
            const collection = (this.databaseService as any).collection;
            if (!collection) {
                throw new Error('Database collection not available for cleanup');
            }

            const deleteResult = await collection.deleteMany(orphanedQuery);
            const deletedCount = deleteResult.deletedCount || 0;

            this.errorHandler.logSuccess(`Orphaned reports cleanup completed: ${deletedCount} records deleted`);

            return {
                success: true,
                message: `Orphaned reports cleanup completed: ${deletedCount} records deleted`,
                recordsCleaned: deletedCount,
                cleanupType: 'orphaned-reports',
                cleanupTimestamp: new Date().toISOString(),
                metadata: {
                    collectionsCleaned: ['accessibility_reports'],
                    spaceFreed: 0,
                    errorsEncountered: []
                }
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'Orphaned reports cleanup failed');
        }
    }

    /**
     * Clean up expired reports older than specified days
     */
    private async cleanupExpiredReports(expirationDays: number, dryRun: boolean = false): Promise<CleanupResult> {
        try {
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    throw new Error('Failed to initialize database service for cleanup');
                }
            }

            const expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() - expirationDays);

            const expiredQuery = {
                createdAt: { $lt: expirationDate }
            };

            if (dryRun) {
                // Count expired records without deleting
                const collection = (this.databaseService as any).collection;
                if (!collection) {
                    throw new Error('Database collection not available for cleanup');
                }

                const expiredCount = await collection.countDocuments(expiredQuery);

                return {
                    success: true,
                    message: `Found ${expiredCount} expired records (older than ${expirationDays} days) (dry run)`,
                    recordsCleaned: expiredCount,
                    cleanupType: 'expired-reports',
                    cleanupTimestamp: new Date().toISOString()
                };
            }

            // Perform actual deletion
            const collection = (this.databaseService as any).collection;
            if (!collection) {
                throw new Error('Database collection not available for cleanup');
            }

            const deleteResult = await collection.deleteMany(expiredQuery);
            const deletedCount = deleteResult.deletedCount || 0;

            this.errorHandler.logSuccess(`Expired reports cleanup completed: ${deletedCount} records deleted`);

            return {
                success: true,
                message: `Expired reports cleanup completed: ${deletedCount} records deleted (older than ${expirationDays} days)`,
                recordsCleaned: deletedCount,
                cleanupType: 'expired-reports',
                cleanupTimestamp: new Date().toISOString(),
                metadata: {
                    collectionsCleaned: ['accessibility_reports'],
                    spaceFreed: 0,
                    errorsEncountered: []
                }
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'Expired reports cleanup failed');
        }
    }

    /**
     * Clean up all data from the database (use with extreme caution)
     */
    private async cleanupAllData(dryRun: boolean = false): Promise<CleanupResult> {
        try {
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    throw new Error('Failed to initialize database service for cleanup');
                }
            }

            const collection = (this.databaseService as any).collection;
            if (!collection) {
                throw new Error('Database collection not available for cleanup');
            }

            if (dryRun) {
                // Count all records without deleting
                const totalCount = await collection.countDocuments({});

                return {
                    success: true,
                    message: `Found ${totalCount} total records (dry run)`,
                    recordsCleaned: totalCount,
                    cleanupType: 'all',
                    cleanupTimestamp: new Date().toISOString()
                };
            }

            // Perform actual deletion of all records
            const deleteResult = await collection.deleteMany({});
            const deletedCount = deleteResult.deletedCount || 0;

            this.errorHandler.logSuccess(`All data cleanup completed: ${deletedCount} records deleted`);

            return {
                success: true,
                message: `All data cleanup completed: ${deletedCount} records deleted`,
                recordsCleaned: deletedCount,
                cleanupType: 'all',
                cleanupTimestamp: new Date().toISOString(),
                metadata: {
                    collectionsCleaned: ['accessibility_reports'],
                    spaceFreed: 0,
                    errorsEncountered: []
                }
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'All data cleanup failed');
        }
    }

    /**
     * Get database statistics for monitoring
     */
    async getDatabaseStatistics(): Promise<ServiceResult> {
        try {
            if (!this.databaseService.isInitialized()) {
                const initResult = await this.databaseService.initialize();
                if (!initResult.success) {
                    return this.errorHandler.handleError(
                        new Error('Failed to initialize database service for statistics'),
                        'Database statistics initialization failed'
                    );
                }
            }

            const statsResult = await this.databaseService.getReportStatistics();

            if (!statsResult.success) {
                return this.errorHandler.handleError(
                    new Error('Failed to retrieve database statistics'),
                    'Database statistics retrieval failed'
                );
            }

            return {
                success: true,
                message: 'Database statistics retrieved successfully',
                data: statsResult.data,
                metadata: {
                    timestamp: new Date().toISOString(),
                    operation: 'statistics_retrieval'
                }
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'Database statistics retrieval failed');
        }
    }

    /**
     * Reset database (use with extreme caution)
     */
    async resetDatabase(): Promise<CleanupResult> {
        try {
            const resetResult = await this.performCleanup({
                allData: true,
                dryRun: false
            });

            return {
                ...resetResult,
                message: 'Database reset completed successfully',
                cleanupType: 'all'
            };

        } catch (error) {
            return this.errorHandler.handleError(error, 'Database reset failed');
        }
    }
}