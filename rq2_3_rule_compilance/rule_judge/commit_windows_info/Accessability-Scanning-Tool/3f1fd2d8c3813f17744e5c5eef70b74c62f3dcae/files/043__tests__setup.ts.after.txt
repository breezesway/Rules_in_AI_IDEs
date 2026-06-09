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
    }
}; 