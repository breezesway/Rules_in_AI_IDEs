/** @type {import('jest').Config} */
module.exports = {
  // Basic configuration
  preset: 'ts-jest',
  testEnvironment: 'node',

  // Test file patterns
  testMatch: [
    '**/__tests__/**/*.test.ts',
    '**/__tests__/**/*.spec.ts',
    '**/tests/**/*.test.ts',
    '**/tests/**/*.spec.ts',
  ],

  // Ignore patterns
  testPathIgnorePatterns: ['/node_modules/', '/playwright/', '/build/', '/dist/', '/coverage/'],

  // TypeScript configuration
  transform: {
    '^.+\.ts$': 'ts-jest',
  },

  // Module resolution
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/playwright/tests/utils/$1',
  },

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'],

  // Coverage configuration
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  collectCoverageFrom: [
    'playwright/tests/utils/**/*.ts',
    '!playwright/tests/utils/**/*.spec.ts',
    '!playwright/tests/utils/**/*.test.ts',
    '!playwright/tests/utils/**/*.d.ts',
    '!**/node_modules/**',
    '!**/dist/**',
  ],

  // Coverage thresholds (initially relaxed for setup)
  coverageThreshold: {
    global: {
      branches: 20,
      functions: 20,
      lines: 20,
      statements: 20,
    },
    'playwright/tests/utils/services/': {
      branches: 20,
      functions: 20,
      lines: 20,
      statements: 20,
    },
  },

  // Test timeout
  testTimeout: 30000,

  // Clear mocks between tests
  clearMocks: true,

  // Verbose output
  verbose: true,

  // Error handling
  bail: false,

  // Module file extensions
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Transform configuration
  transform: {
    '^.+\\.ts$': [
      'ts-jest',
      {
        tsconfig: 'tsconfig.json',
      },
    ],
  },
};
