import { jest } from '@jest/globals';

// Global test configuration
beforeEach(() => {
  // Clear all mocks before each test
  jest.clearAllMocks();

  // Reset environment variables for each test
  process.env.NODE_ENV = 'test';
  delete process.env.TARGET_SITE_URL;
  delete process.env.WAVE_API_KEY;
  delete process.env.TENON_API_KEY;
});

// Global test utilities
global.testUtils = {
  createMockPage: () => ({
    url: jest.fn().mockReturnValue('https://example.com'),
    goto: jest.fn(),
    screenshot: jest.fn(),
    addScriptTag: jest.fn(),
    locator: jest.fn(),
    waitForSelector: jest.fn(),
    evaluate: jest.fn(),
    content: jest.fn(),
    title: jest.fn(),
    context: jest.fn(),
    close: jest.fn(),
    isClosed: jest.fn().mockReturnValue(false),
    on: jest.fn(),
    off: jest.fn(),
    browserName: 'chromium',
    viewportInfo: '1200x800',
  }),

  createMockServiceResult: <T>(data: T) => ({
    success: true,
    data,
    timestamp: new Date().toISOString(),
  }),

  createMockErrorResult: (error: string) => ({
    success: false,
    error,
    timestamp: new Date().toISOString(),
  }),

  mockFileSystem: {
    existsSync: jest.fn(),
    readFileSync: jest.fn(),
    writeFileSync: jest.fn(),
    mkdirSync: jest.fn(),
    unlinkSync: jest.fn(),
    readdirSync: jest.fn(),
    statSync: jest.fn(),
  },
};

// Global type definitions for TypeScript
declare global {
  namespace globalThis {
    // eslint-disable-next-line no-var
    var testUtils: {
      createMockPage: () => any;
      createMockServiceResult: <T>(data: T) => any;
      createMockErrorResult: (error: string) => any;
      mockFileSystem: {
        existsSync: jest.Mock;
        readFileSync: jest.Mock;
        writeFileSync: jest.Mock;
        mkdirSync: jest.Mock;
        unlinkSync: jest.Mock;
        readdirSync: jest.Mock;
        statSync: jest.Mock;
      };
    };
  }
}

// Mock external dependencies that require special handling
jest.mock('fs', () => ({
  existsSync: jest.fn(),
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
  mkdirSync: jest.fn(),
  unlinkSync: jest.fn(),
  readdirSync: jest.fn(),
  statSync: jest.fn(),
  promises: {
    readFile: jest.fn(),
    writeFile: jest.fn(),
    mkdir: jest.fn(),
    unlink: jest.fn(),
    readdir: jest.fn(),
    stat: jest.fn(),
  },
}));

jest.mock('path', () => ({
  resolve: jest.fn((...args: string[]) => args.join('/')),
  dirname: jest.fn((path: string) => path.split('/').slice(0, -1).join('/')),
  basename: jest.fn((path: string) => path.split('/').pop()),
  extname: jest.fn((path: string) => {
    const parts = path.split('.');
    return parts.length > 1 ? `.${parts.pop()}` : '';
  }),
  join: jest.fn((...args: string[]) => args.join('/')),
}));

jest.mock('node-fetch', () => ({
  default: jest.fn(),
}));

// Increase default timeout for all tests
jest.setTimeout(30000);
