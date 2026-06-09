// Jest setup file for accessibility testing application
import { jest } from '@jest/globals';

// Global test timeout
jest.setTimeout(10000);

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

    // Helper to create temporary test directories
    createTempDir: () => {
        const fs = require('fs');
        const path = require('path');
        const tempDir = path.join(__dirname, '../temp-test-' + Date.now());
        fs.mkdirSync(tempDir, { recursive: true });
        return tempDir;
    },

    // Helper to clean up temporary directories
    cleanupTempDir: (dir: string) => {
        const fs = require('fs');
        const path = require('path');
        if (fs.existsSync(dir)) {
            fs.rmSync(dir, { recursive: true, force: true });
        }
    }
}; 