/**
 * Global Setup for E2E Tests
 * 
 * This file runs before all E2E tests to ensure the database is clean
 * and ready for testing.
 */

import { DatabaseCleanupService } from '@/utils/services/database-cleanup-service';

async function globalSetup() {
    console.log('🧹 Starting global E2E test setup...');

    try {
        // Set up test environment variables
        process.env['NODE_ENV'] = 'test';
        process.env['MONGODB_URL'] = 'mongodb://localhost:27017';
        process.env['MONGODB_DB_NAME'] = 'test_accessibility_db';

        // Clean up any existing test data
        const cleanupService = DatabaseCleanupService.getInstance();

        console.log('🧹 Cleaning up existing test data...');
        const result = await cleanupService.performCleanup({
            testData: true,
            orphanedReports: true,
            expiredReports: false, // Don't clean up expired reports in tests
            dryRun: false
        });

        if (result.success) {
            console.log(`✅ Global setup completed: ${result.recordsCleaned || 0} test records cleaned`);
        } else {
            console.warn('⚠️ Global setup cleanup failed:', result.message);
        }

    } catch (error) {
        console.warn('⚠️ Global setup error:', error);
        // Don't fail the setup - tests can still run
    }
}

export default globalSetup; 