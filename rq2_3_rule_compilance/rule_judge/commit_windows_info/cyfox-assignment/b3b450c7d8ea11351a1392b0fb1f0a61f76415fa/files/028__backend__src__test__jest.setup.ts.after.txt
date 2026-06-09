import dotenv from 'dotenv';
import { setupTestDatabase, teardownTestDatabase, clearTestData } from './setup';

// Load test environment variables
dotenv.config({ path: '.env.test' });

// Global test setup
beforeAll(async () => {
  await setupTestDatabase();
});

// Global test teardown
afterAll(async () => {
  await teardownTestDatabase();
});

// Clear data between tests
beforeEach(async () => {
  await clearTestData();
});

// Increase timeout for database operations
jest.setTimeout(30000);