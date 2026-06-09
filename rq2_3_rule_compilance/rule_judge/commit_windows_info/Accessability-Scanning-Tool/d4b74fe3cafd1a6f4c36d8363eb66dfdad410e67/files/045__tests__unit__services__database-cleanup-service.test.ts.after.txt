import { DatabaseCleanupService, CleanupResult, CleanupOptions } from '@/utils/services/database-cleanup-service';
import { DatabaseService } from '@/utils/services/database-service';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

// Mock the DatabaseService
jest.mock('@/utils/services/database-service');

describe('DatabaseCleanupService', () => {
    let cleanupService: DatabaseCleanupService;
    let mockDatabaseService: jest.Mocked<DatabaseService>;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;

    beforeEach(() => {
        // Setup test environment and database cleanup
        (global as any).testUtils.database.setupTestEnvironment();

        // Clear all mocks
        jest.clearAllMocks();

        // Reset singleton instances
        (ConfigurationService as any).instance = undefined;
        (ErrorHandlerService as any).instance = undefined;
        (DatabaseCleanupService as any).instance = undefined;

        // Create mock database service
        mockDatabaseService = {
            isInitialized: jest.fn(),
            initialize: jest.fn(),
            getReportsWithMetadata: jest.fn(),
            getReportStatistics: jest.fn(),
            close: jest.fn(),
            collection: {
                deleteMany: jest.fn(),
                countDocuments: jest.fn()
            }
        } as any;

        // Mock the DatabaseService.getInstance to return our mock
        (DatabaseService.getInstance as jest.Mock) = jest.fn().mockReturnValue(mockDatabaseService);

        cleanupService = DatabaseCleanupService.getInstance();
        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();
    });

    afterEach(async () => {
        // Clean up test data and verify cleanup
        await (global as any).testUtils.database.cleanupTestData();
        await (global as any).testUtils.database.verifyCleanup();
        jest.clearAllMocks();
    });

    describe('Singleton Pattern', () => {
        test('should return the same instance when called multiple times', () => {
            const instance1 = DatabaseCleanupService.getInstance();
            const instance2 = DatabaseCleanupService.getInstance();
            expect(instance1).toBe(instance2);
        });

        test('should not allow direct instantiation', () => {
            // The constructor is private, so this should not be possible
            expect(() => {
                const Constructor = DatabaseCleanupService as any;
                return new Constructor();
            }).toThrow();
        });
    });

    describe('performCleanup', () => {
        beforeEach(() => {
            mockDatabaseService.isInitialized.mockReturnValue(true);
            mockDatabaseService.getReportsWithMetadata.mockResolvedValue({
                success: true,
                data: [],
                message: 'Reports retrieved successfully'
            });

            // Mock collection methods using Object.defineProperty to access private property
            Object.defineProperty(mockDatabaseService, 'collection', {
                value: {
                    deleteMany: jest.fn().mockResolvedValue({ deletedCount: 5 }),
                    countDocuments: jest.fn().mockResolvedValue(10)
                },
                writable: true
            });
        });

        test('should perform cleanup with default options', async () => {
            const result = await cleanupService.performCleanup();

            expect(result.success).toBe(true);
            expect(result.message).toContain('Database cleanup completed successfully');
            expect(result.data).toBeDefined();
            expect((result.data as any)?.cleanupType).toBe('selective');
            expect((result.data as any)?.cleanupTimestamp).toBeDefined();
        });

        test('should perform cleanup with custom options', async () => {
            const options: CleanupOptions = {
                testData: true,
                orphanedReports: false,
                expiredReports: true,
                expirationDays: 60,
                dryRun: true
            };

            const result = await cleanupService.performCleanup(options);

            expect(result.success).toBe(true);
            expect(result.message).toContain('(dry run)');
            expect((result.data as any)?.cleanupType).toBe('selective');
        });

        test('should perform full cleanup when allData is true', async () => {
            const options: CleanupOptions = {
                allData: true,
                dryRun: false
            };

            const result = await cleanupService.performCleanup(options);

            expect(result.success).toBe(true);
            expect((result.data as any)?.cleanupType).toBe('all');
        });

        test('should handle database initialization failure', async () => {
            mockDatabaseService.isInitialized.mockReturnValue(false);
            mockDatabaseService.initialize.mockResolvedValue({
                success: false,
                message: 'Database initialization failed',
                data: null
            });

            const result = await cleanupService.performCleanup();

            expect(result.success).toBe(false);
            expect(result.message).toContain('Database cleanup initialization failed');
        });

        test('should handle cleanup errors gracefully', async () => {
            mockDatabaseService.getReportsWithMetadata.mockRejectedValue(new Error('Database error'));

            const result = await cleanupService.performCleanup();

            expect(result.success).toBe(true); // Overall operation succeeds
            expect(result.metadata?.errorsEncountered).toBeDefined();
            expect(result.metadata?.errorsEncountered?.length).toBeGreaterThan(0);
        });
    });

    describe('getDatabaseStatistics', () => {
        beforeEach(() => {
            mockDatabaseService.isInitialized.mockReturnValue(true);
            mockDatabaseService.getReportStatistics.mockResolvedValue({
                success: true,
                data: {
                    totalReports: 10,
                    siteWideReports: 5,
                    singlePageReports: 5,
                    uniqueSites: 2,
                    oldestReport: '2024-01-01T00:00:00.000Z',
                    newestReport: '2024-01-15T00:00:00.000Z'
                },
                message: 'Statistics retrieved successfully'
            });
        });

        test('should retrieve database statistics successfully', async () => {
            const result = await cleanupService.getDatabaseStatistics();

            expect(result.success).toBe(true);
            expect(result.message).toBe('Database statistics retrieved successfully');
            expect(result.data).toBeDefined();
            expect((result.data as any)?.totalReports).toBe(10);
            expect(result.metadata?.['operation']).toBe('statistics_retrieval');
        });

        test('should handle database initialization for statistics', async () => {
            mockDatabaseService.isInitialized.mockReturnValue(false);
            mockDatabaseService.initialize.mockResolvedValue({
                success: true,
                message: 'Database initialized successfully',
                data: null
            });

            const result = await cleanupService.getDatabaseStatistics();

            expect(result.success).toBe(true);
            expect(mockDatabaseService.initialize).toHaveBeenCalled();
        });

        test('should handle statistics retrieval failure', async () => {
            mockDatabaseService.getReportStatistics.mockResolvedValue({
                success: false,
                message: 'Statistics retrieval failed',
                data: undefined,
                metadata: {
                    collectionName: 'accessibility_reports',
                    operation: 'statistics_retrieval',
                    timestamp: new Date().toISOString()
                }
            } as any);

            const result = await cleanupService.getDatabaseStatistics();

            expect(result.success).toBe(false);
            expect(result.message).toContain('Database statistics retrieval failed');
        });
    });

    describe('resetDatabase', () => {
        test('should reset database successfully', async () => {
            mockDatabaseService.isInitialized.mockReturnValue(true);

            const result = await cleanupService.resetDatabase();

            expect(result.success).toBe(true);
            expect(result.message).toBe('Database reset completed successfully');
            expect((result.data as any)?.cleanupType).toBe('all');
        });

        test('should handle reset errors', async () => {
            mockDatabaseService.isInitialized.mockReturnValue(false);
            mockDatabaseService.initialize.mockRejectedValue(new Error('Reset failed'));

            const result = await cleanupService.resetDatabase();

            expect(result.success).toBe(false);
            expect(result.message).toContain('Database reset failed');
        });
    });

    describe('Error Handling', () => {
        test('should handle unexpected errors in cleanup', async () => {
            mockDatabaseService.isInitialized.mockImplementation(() => {
                throw new Error('Unexpected error');
            });

            const result = await cleanupService.performCleanup();

            expect(result.success).toBe(false);
            expect(result.message).toContain('Database cleanup operation failed');
        });

        test('should handle errors in statistics retrieval', async () => {
            mockDatabaseService.getReportStatistics.mockRejectedValue(new Error('Statistics error'));

            const result = await cleanupService.getDatabaseStatistics();

            expect(result.success).toBe(false);
            expect(result.message).toContain('Database statistics retrieval failed');
        });
    });

    describe('Integration with ErrorHandlerService', () => {
        test('should use ErrorHandlerService for error handling', async () => {
            const mockHandleError = jest.fn().mockReturnValue({
                success: false,
                message: 'Handled error',
                data: null
            });

            // Mock the error handler
            (ErrorHandlerService.getInstance as jest.Mock) = jest.fn().mockReturnValue({
                handleError: mockHandleError
            });

            mockDatabaseService.isInitialized.mockImplementation(() => {
                throw new Error('Test error');
            });

            const newCleanupService = DatabaseCleanupService.getInstance();
            const result = await newCleanupService.performCleanup();

            expect(mockHandleError).toHaveBeenCalled();
            expect(result.success).toBe(false);
        });
    });
}); 