import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

// Global setup for integration tests
beforeAll(async () => {
    // Initialize services
    const errorHandler = ErrorHandlerService.getInstance();
    const configService = ConfigurationService.getInstance();

    // Set test configuration
    configService.set('test.integration', true);
    configService.set('test.timeout', 30000);

    // Suppress error logging during tests
    errorHandler.setLogLevel('error');

    // Set up test database environment
    (global as any).testUtils.database.setupTestEnvironment();

    // Clean up any existing test data before running integration tests
    try {
        await (global as any).testUtils.database.cleanupTestData();
        console.log('Integration test database cleanup completed');
    } catch (error) {
        console.warn('Integration test database cleanup failed:', error);
    }

    console.log('Integration test environment initialized');
});

// Global teardown for integration tests
afterAll(async () => {
    // Clean up any remaining test data
    try {
        await (global as any).testUtils.database.cleanupTestData();
        console.log('Integration test final database cleanup completed');
    } catch (error) {
        console.warn('Integration test final database cleanup failed:', error);
    }

    // Clean up any remaining resources
    console.log('Integration test environment cleaned up');
});

// Increase timeout for integration tests
jest.setTimeout(30000);

// Suppress console output during tests unless there's an error
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

beforeEach(() => {
    console.log = jest.fn();
    console.error = jest.fn();
});

afterEach(() => {
    console.log = originalConsoleLog;
    console.error = originalConsoleError;
}); 