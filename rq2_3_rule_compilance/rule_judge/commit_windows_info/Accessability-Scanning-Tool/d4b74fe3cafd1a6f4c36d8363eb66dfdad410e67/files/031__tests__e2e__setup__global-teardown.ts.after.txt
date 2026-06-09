/**
 * Global Teardown for E2E Tests
 * 
 * This file runs after all E2E tests to clean up any remaining test data
 * and ensure the database is left in a clean state.
 */

import { DatabaseCleanupService } from '@/utils/services/database-cleanup-service';

async function globalTeardown() {
    console.log('🧹 Starting global E2E test teardown...');

    try {
        // Clean up any remaining test data
        const cleanupService = DatabaseCleanupService.getInstance();

        console.log('🧹 Cleaning up remaining test data...');
        const result = await cleanupService.performCleanup({
            testData: true,
            orphanedReports: true,
            expiredReports: false, // Don't clean up expired reports in tests
            dryRun: false
        });

        if (result.success) {
            console.log(`✅ Global teardown completed: ${result.recordsCleaned || 0} test records cleaned`);
        } else {
            console.warn('⚠️ Global teardown cleanup failed:', result.message);
        }

    } catch (error) {
        console.warn('⚠️ Global teardown error:', error);
        // Don't fail the teardown - tests have already completed
    }
}

export default globalTeardown; 