// Jest setup file for accessibility testing application
import { jest } from '@jest/globals';
import * as fs from 'fs';
import * as path from 'path';

// Global test timeout
jest.setTimeout(10000);

// Track created test files and directories for cleanup
const createdTestPaths: string[] = [];

// Mock console methods to reduce noise in tests
global.console = {
    ...console,
    log: jest.fn(),
    debug: jest.fn(),
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
};

// Mock process.exit to prevent tests from actually exiting
const originalExit = process.exit;
beforeAll(() => {
    process.exit = jest.fn() as any;
});

afterAll(() => {
    process.exit = originalExit;
});

// Global cleanup after all tests
afterAll(async () => {
    // Clean up all tracked test files and directories
    createdTestPaths.forEach(testPath => {
        try {
            if (fs.existsSync(testPath)) {
                if (fs.statSync(testPath).isDirectory()) {
                    fs.rmSync(testPath, { recursive: true, force: true });
                } else {
                    fs.unlinkSync(testPath);
                }
            }
        } catch (error) {
            // Ignore cleanup errors
        }
    });

    // Clean up common test directories
    const commonTestDirs = [
        path.join(process.cwd(), 'test-temp'),
        path.join(process.cwd(), 'temp-test-*'),
        path.join(process.cwd(), 'accessibility-reports'),
        path.join(process.cwd(), 'test-results')
    ];

    commonTestDirs.forEach(dir => {
        try {
            if (fs.existsSync(dir)) {
                fs.rmSync(dir, { recursive: true, force: true });
            }
        } catch (error) {
            // Ignore cleanup errors
        }
    });

    // Clean up temporary HTML files created by PDF orchestrator
    try {
        const tempHtmlFiles = fs.readdirSync(process.cwd())
            .filter(file => file.startsWith('temp-') && file.endsWith('.html'));

        tempHtmlFiles.forEach(file => {
            try {
                fs.unlinkSync(path.join(process.cwd(), file));
            } catch (error) {
                // Ignore individual file cleanup errors
            }
        });

        if (tempHtmlFiles.length > 0) {
            console.log(`Cleaned up ${tempHtmlFiles.length} temporary HTML files`);
        }
    } catch (error) {
        // Ignore cleanup errors
    }

    // Force cleanup of any remaining timers
    jest.clearAllTimers();

    // Clear all timeouts and intervals
    const activeTimers = (global as any).__JEST_TIMERS__;
    if (activeTimers) {
        activeTimers.clearAllTimers();
    }

    // Give a small delay to allow any remaining async operations to complete
    await new Promise(resolve => setTimeout(resolve, 100));
});

// Global test utilities
(global as any).testUtils = {
    // Helper to create mock PageInfo objects
    createMockPageInfo: (overrides: Partial<any> = {}): any => ({
        url: 'https://example.com',
        title: 'Test Page',
        depth: 0,
        foundOn: 'https://example.com',
        status: 200,
        loadTime: 1000,
        ...overrides
    }),

    // Helper to create mock AnalysisResult objects
    createMockAnalysisResult: (overrides: Partial<any> = {}): any => ({
        url: 'https://example.com',
        timestamp: new Date().toISOString(),
        tool: 'axe-core',
        violations: [],
        summary: {
            totalViolations: 0,
            criticalViolations: 0,
            seriousViolations: 0,
            moderateViolations: 0,
            minorViolations: 0
        },
        ...overrides
    }),

    // Helper to create mock ServiceResult objects
    createMockServiceResult: <T>(data: T, success = true, message = 'Test result'): any => ({
        success,
        data,
        message,
        metadata: {}
    }),

    // Helper to wait for async operations
    wait: (ms: number) => new Promise(resolve => setTimeout(resolve, ms)),

    // Helper to create temporary test directories with tracking
    createTempDir: () => {
        const tempDir = path.join(process.cwd(), 'test-temp-' + Date.now());
        fs.mkdirSync(tempDir, { recursive: true });
        createdTestPaths.push(tempDir);
        return tempDir;
    },

    // Helper to clean up temporary directories
    cleanupTempDir: (dir: string) => {
        if (fs.existsSync(dir)) {
            fs.rmSync(dir, { recursive: true, force: true });
            // Remove from tracking array
            const index = createdTestPaths.indexOf(dir);
            if (index > -1) {
                createdTestPaths.splice(index, 1);
            }
        }
    },

    // Helper to create test files with tracking
    createTestFile: (filePath: string, content: string = 'test content') => {
        const dir = path.dirname(filePath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
            createdTestPaths.push(dir);
        }
        fs.writeFileSync(filePath, content);
        createdTestPaths.push(filePath);
        return filePath;
    },

    // Helper to clean up test files
    cleanupTestFile: (filePath: string) => {
        try {
            if (fs.existsSync(filePath)) {
                fs.unlinkSync(filePath);
                // Remove from tracking array
                const index = createdTestPaths.indexOf(filePath);
                if (index > -1) {
                    createdTestPaths.splice(index, 1);
                }
            }
        } catch (error) {
            // Ignore cleanup errors
        }
    },

    // Helper to create test reports directory with tracking
    createTestReportsDir: () => {
        const reportsDir = path.join(process.cwd(), 'accessibility-reports');
        if (!fs.existsSync(reportsDir)) {
            fs.mkdirSync(reportsDir, { recursive: true });
            createdTestPaths.push(reportsDir);
        }
        return reportsDir;
    },

    // Helper to clean up test reports directory
    cleanupTestReportsDir: () => {
        const reportsDir = path.join(process.cwd(), 'accessibility-reports');
        try {
            if (fs.existsSync(reportsDir)) {
                fs.rmSync(reportsDir, { recursive: true, force: true });
                // Remove from tracking array
                const index = createdTestPaths.indexOf(reportsDir);
                if (index > -1) {
                    createdTestPaths.splice(index, 1);
                }
            }
        } catch (error) {
            // Ignore cleanup errors
        }
    },

    // Helper to clean up temporary HTML files
    cleanupTempHtmlFiles: () => {
        try {
            const tempHtmlFiles = fs.readdirSync(process.cwd())
                .filter(file => file.startsWith('temp-') && file.endsWith('.html'));

            tempHtmlFiles.forEach(file => {
                try {
                    fs.unlinkSync(path.join(process.cwd(), file));
                } catch (error) {
                    // Ignore individual file cleanup errors
                }
            });

            return tempHtmlFiles.length;
        } catch (error) {
            return 0;
        }
    },

    // Database cleanup utilities
    database: {
        // Helper to set up test database environment
        setupTestEnvironment: () => {
            // Set test-specific environment variables
            process.env['NODE_ENV'] = 'test';
            process.env['MONGODB_URL'] = 'mongodb://localhost:27017';
            process.env['MONGODB_DB_NAME'] = 'test_accessibility_db';

            // Ensure test database name is used
            if (!process.env['MONGODB_DB_NAME']?.includes('test')) {
                process.env['MONGODB_DB_NAME'] = 'test_accessibility_db';
            }
        },

        // Helper to clean up test database data
        cleanupTestData: async () => {
            try {
                // Import the cleanup service dynamically to avoid circular dependencies
                const { DatabaseCleanupService } = await import('@/utils/services/database-cleanup-service');
                const cleanupService = DatabaseCleanupService.getInstance();

                // Perform test data cleanup
                const result = await cleanupService.performCleanup({
                    testData: true,
                    orphanedReports: true,
                    expiredReports: false, // Don't clean up expired reports in tests
                    dryRun: false
                });

                if (result.success) {
                    console.log(`Database cleanup completed: ${result.recordsCleaned || 0} records cleaned`);
                } else {
                    console.warn('Database cleanup failed:', result.message);
                }

                return result;
            } catch (error) {
                console.warn('Database cleanup error:', error);
                return {
                    success: false,
                    message: 'Database cleanup failed',
                    data: null
                };
            }
        },

        // Helper to reset test database
        resetTestDatabase: async () => {
            try {
                const { DatabaseCleanupService } = await import('@/utils/services/database-cleanup-service');
                const cleanupService = DatabaseCleanupService.getInstance();

                const result = await cleanupService.resetDatabase();

                if (result.success) {
                    console.log('Test database reset completed');
                } else {
                    console.warn('Test database reset failed:', result.message);
                }

                return result;
            } catch (error) {
                console.warn('Test database reset error:', error);
                return {
                    success: false,
                    message: 'Test database reset failed',
                    data: null
                };
            }
        },

        // Helper to get database statistics
        getTestDatabaseStats: async () => {
            try {
                const { DatabaseCleanupService } = await import('@/utils/services/database-cleanup-service');
                const cleanupService = DatabaseCleanupService.getInstance();

                return await cleanupService.getDatabaseStatistics();
            } catch (error) {
                console.warn('Database statistics error:', error);
                return {
                    success: false,
                    message: 'Database statistics failed',
                    data: null
                };
            }
        },

        // Helper to create test data in database
        createTestData: async (testData: any) => {
            try {
                const { DatabaseService } = await import('@/utils/services/database-service');
                const databaseService = DatabaseService.getInstance();

                // Initialize database if needed
                if (!databaseService.isInitialized()) {
                    await databaseService.initialize();
                }

                // Store test data
                if (testData.siteUrl) {
                    // Site-wide report
                    return await databaseService.storeSiteWideReport(testData);
                } else {
                    // Single page report
                    return await databaseService.storeSinglePageReport(testData);
                }
            } catch (error) {
                console.warn('Test data creation error:', error);
                return {
                    success: false,
                    message: 'Test data creation failed',
                    data: null
                };
            }
        },

        // Helper to verify test data was cleaned up
        verifyCleanup: async () => {
            try {
                const stats = await (global as any).testUtils.database.getTestDatabaseStats();
                if (stats.success && stats.data) {
                    const totalReports = stats.data.totalReports || 0;
                    if (totalReports > 0) {
                        console.warn(`Warning: ${totalReports} reports still exist in test database`);
                        return false;
                    }
                    return true;
                }
                return true; // Assume clean if we can't verify
            } catch (error) {
                console.warn('Cleanup verification error:', error);
                return true; // Assume clean if we can't verify
            }
        }
    },

    // Test data creation helpers
    createTestData: {
        // Create mock site-wide report for testing
        createMockSiteWideReport: (overrides: Partial<any> = {}): any => ({
            siteUrl: 'https://test-example.com',
            pages: [
                {
                    url: 'https://test-example.com',
                    title: 'Test Page',
                    violations: [],
                    summary: {
                        totalViolations: 0,
                        criticalViolations: 0,
                        seriousViolations: 0,
                        moderateViolations: 0,
                        minorViolations: 0
                    }
                }
            ],
            summary: {
                totalPages: 1,
                totalViolations: 0,
                compliancePercentage: 100,
                wcagLevel: 'AA'
            },
            metadata: {
                scanId: 'test-scan-' + Date.now(),
                scanType: 'test',
                scanStartedAt: new Date(),
                scanCompletedAt: new Date(),
                toolsUsed: ['axe-core'],
                ...overrides['metadata']
            },
            ...overrides
        }),

        // Create mock single page report for testing
        createMockSinglePageReport: (overrides: Partial<any> = {}): any => ({
            url: 'https://test-example.com',
            title: 'Test Page',
            violations: [],
            summary: {
                totalViolations: 0,
                criticalViolations: 0,
                seriousViolations: 0,
                moderateViolations: 0,
                minorViolations: 0
            },
            metadata: {
                scanId: 'test-scan-' + Date.now(),
                scanType: 'test',
                scanStartedAt: new Date(),
                scanCompletedAt: new Date(),
                toolsUsed: ['axe-core'],
                ...overrides['metadata']
            },
            ...overrides
        })
    }
}; 