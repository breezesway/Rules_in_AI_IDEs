#!/usr/bin/env node

/**
 * Test Database Cleanup Verification Script
 * 
 * This script verifies that all test files are properly using the database cleanup utilities
 * to ensure test data is cleaned up after each test run.
 */

const fs = require('fs');
const path = require('path');

// ANSI color codes for console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function logSuccess(message) {
    log(`✅ ${message}`, 'green');
}

function logWarning(message) {
    log(`⚠️  ${message}`, 'yellow');
}

function logError(message) {
    log(`❌ ${message}`, 'red');
}

function logInfo(message) {
    log(`ℹ️  ${message}`, 'blue');
}

function logHeader(message) {
    log(`\n${colors.bright}${colors.cyan}${message}${colors.reset}`);
}

/**
 * Check if a test file has proper database cleanup
 */
function checkTestFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const fileName = path.basename(filePath);
    
    // Helper function to check for method calls in various formats
    const hasMethodCall = (methodName) => {
        const patterns = [
            `testUtils.database.${methodName}`,
            `(global as any).testUtils.database.${methodName}`,
            `testUtils.database.${methodName}(`,
            `(global as any).testUtils.database.${methodName}(`
        ];
        return patterns.some(pattern => content.includes(pattern));
    };
    
    const checks = {
        hasBeforeEach: content.includes('beforeEach') && hasMethodCall('setupTestEnvironment'),
        hasAfterEach: content.includes('afterEach') && hasMethodCall('cleanupTestData'),
        hasAfterAll: content.includes('afterAll') && hasMethodCall('cleanupTestData'),
        hasSetupEnvironment: hasMethodCall('setupTestEnvironment'),
        hasCleanupData: hasMethodCall('cleanupTestData'),
        hasVerifyCleanup: hasMethodCall('verifyCleanup'),
        hasDatabaseImport: content.includes('DatabaseCleanupService') || content.includes('database-cleanup-service'),
        hasTestUtils: content.includes('testUtils.database') || content.includes('(global as any).testUtils.database'),
        isIntegrationTest: filePath.includes('integration'),
        isUnitTest: filePath.includes('unit'),
        isE2ETest: filePath.includes('e2e')
    };

    const issues = [];
    
    // Integration tests should have comprehensive cleanup
    if (checks.isIntegrationTest) {
        if (!checks.hasBeforeEach) {
            issues.push('Missing beforeEach with database setup');
        }
        if (!checks.hasAfterEach) {
            issues.push('Missing afterEach with database cleanup');
        }
        if (!checks.hasVerifyCleanup) {
            issues.push('Missing cleanup verification');
        }
    }
    
    // Unit tests should have basic cleanup if they use database
    if (checks.isUnitTest && checks.hasDatabaseImport) {
        if (!checks.hasAfterEach && !checks.hasAfterAll) {
            issues.push('Database unit test missing cleanup hooks');
        }
    }
    
    // E2E tests should have cleanup if they use database
    if (checks.isE2ETest && checks.hasDatabaseImport) {
        if (!checks.hasAfterAll) {
            issues.push('E2E test missing afterAll cleanup');
        }
    }

    return {
        fileName,
        filePath,
        checks,
        issues,
        hasIssues: issues.length > 0
    };
}

/**
 * Find all test files in the project
 */
function findTestFiles() {
    const testDirs = [
        'tests/unit',
        'tests/integration', 
        'tests/e2e'
    ];
    
    const testFiles = [];
    
    testDirs.forEach(dir => {
        if (fs.existsSync(dir)) {
            const files = fs.readdirSync(dir, { recursive: true });
            files.forEach(file => {
                if (typeof file === 'string' && file.endsWith('.test.ts')) {
                    testFiles.push(path.join(dir, file));
                }
            });
        }
    });
    
    return testFiles;
}

/**
 * Check the global test setup file
 */
function checkGlobalSetup() {
    const setupFile = 'tests/setup.ts';
    
    if (!fs.existsSync(setupFile)) {
        logError('Global test setup file not found: tests/setup.ts');
        return false;
    }
    
    const content = fs.readFileSync(setupFile, 'utf8');
    
    // Check for method definitions within the database object
    const requiredMethods = [
        'setupTestEnvironment',
        'cleanupTestData',
        'resetTestDatabase', 
        'getTestDatabaseStats',
        'verifyCleanup',
        'createTestData'
    ];
    
    const missingMethods = requiredMethods.filter(method => {
        // Look for method definitions in various formats
        const patterns = [
            `${method}: () => {`,
            `${method}: async () => {`,
            `${method}: function() {`,
            `${method}: async function() {`,
            `${method}: () => {`,
            `${method}: async () => {`
        ];
        
        // Special case for createTestData - it can be either a function or an object
        if (method === 'createTestData') {
            const functionPatterns = patterns;
            const objectPattern = `${method}: {`;
            return !functionPatterns.some(pattern => content.includes(pattern)) && 
                   !content.includes(objectPattern);
        }
        
        return !patterns.some(pattern => content.includes(pattern));
    });
    
    if (missingMethods.length > 0) {
        logError('Global test setup missing required database method definitions:');
        missingMethods.forEach(method => {
            logError(`  - ${method}`);
        });
        return false;
    }
    
    // Also check that the database object is properly defined
    if (!content.includes('database: {')) {
        logError('Global test setup missing database object definition');
        return false;
    }
    
    logSuccess('Global test setup has all required database utilities');
    return true;
}

/**
 * Check the DatabaseCleanupService implementation
 */
function checkDatabaseCleanupService() {
    const serviceFile = 'src/utils/services/database-cleanup-service.ts';
    
    if (!fs.existsSync(serviceFile)) {
        logError('DatabaseCleanupService not found');
        return false;
    }
    
    const content = fs.readFileSync(serviceFile, 'utf8');
    
    const requiredMethods = [
        'performCleanup',
        'getDatabaseStatistics',
        'resetDatabase',
        'cleanupTestData',
        'cleanupOrphanedReports',
        'cleanupExpiredReports'
    ];
    
    const missingMethods = requiredMethods.filter(method => !content.includes(method));
    
    if (missingMethods.length > 0) {
        logError('DatabaseCleanupService missing required methods:');
        missingMethods.forEach(method => {
            logError(`  - ${method}`);
        });
        return false;
    }
    
    logSuccess('DatabaseCleanupService has all required methods');
    return true;
}

/**
 * Check the unit tests for DatabaseCleanupService
 */
function checkDatabaseCleanupServiceTests() {
    const testFile = 'tests/unit/services/database-cleanup-service.test.ts';
    
    if (!fs.existsSync(testFile)) {
        logError('DatabaseCleanupService unit tests not found');
        return false;
    }
    
    const content = fs.readFileSync(testFile, 'utf8');
    
    const requiredTests = [
        'performCleanup',
        'getDatabaseStatistics',
        'resetDatabase',
        'Singleton Pattern',
        'Error Handling'
    ];
    
    const missingTests = requiredTests.filter(test => !content.includes(test));
    
    if (missingTests.length > 0) {
        logError('DatabaseCleanupService unit tests missing required test cases:');
        missingTests.forEach(test => {
            logError(`  - ${test}`);
        });
        return false;
    }
    
    logSuccess('DatabaseCleanupService has comprehensive unit tests');
    return true;
}

/**
 * Main verification function
 */
function verifyDatabaseCleanup() {
    logHeader('🔍 VERIFYING DATABASE CLEANUP IMPLEMENTATION');
    
    let allChecksPassed = true;
    
    // Check global setup
    logInfo('Checking global test setup...');
    if (!checkGlobalSetup()) {
        allChecksPassed = false;
    }
    
    // Check DatabaseCleanupService
    logInfo('Checking DatabaseCleanupService implementation...');
    if (!checkDatabaseCleanupService()) {
        allChecksPassed = false;
    }
    
    // Check DatabaseCleanupService tests
    logInfo('Checking DatabaseCleanupService unit tests...');
    if (!checkDatabaseCleanupServiceTests()) {
        allChecksPassed = false;
    }
    
    // Check all test files
    logInfo('Checking individual test files...');
    const testFiles = findTestFiles();
    
    if (testFiles.length === 0) {
        logWarning('No test files found');
    } else {
        logInfo(`Found ${testFiles.length} test files`);
        
        const filesWithIssues = [];
        const filesWithoutIssues = [];
        
        testFiles.forEach(filePath => {
            const result = checkTestFile(filePath);
            if (result.hasIssues) {
                filesWithIssues.push(result);
            } else {
                filesWithoutIssues.push(result);
            }
        });
        
        if (filesWithIssues.length > 0) {
            logError(`\n${filesWithIssues.length} test files have database cleanup issues:`);
            filesWithIssues.forEach(file => {
                logError(`\n  ${file.fileName}:`);
                file.issues.forEach(issue => {
                    logError(`    - ${issue}`);
                });
            });
            allChecksPassed = false;
        } else {
            logSuccess(`All ${testFiles.length} test files have proper database cleanup`);
        }
        
        // Summary
        logInfo(`\n📊 SUMMARY:`);
        logInfo(`  Total test files: ${testFiles.length}`);
        logInfo(`  Files with issues: ${filesWithIssues.length}`);
        logInfo(`  Files without issues: ${filesWithoutIssues.length}`);
        
        // Show files by category
        const integrationTests = testFiles.filter(f => f.includes('integration'));
        const unitTests = testFiles.filter(f => f.includes('unit'));
        const e2eTests = testFiles.filter(f => f.includes('e2e'));
        
        logInfo(`\n📁 TEST CATEGORIES:`);
        logInfo(`  Integration tests: ${integrationTests.length}`);
        logInfo(`  Unit tests: ${unitTests.length}`);
        logInfo(`  E2E tests: ${e2eTests.length}`);
    }
    
    // Final result
    logHeader('🎯 VERIFICATION RESULT');
    if (allChecksPassed) {
        logSuccess('All database cleanup checks passed! ✅');
        logInfo('Test data will be properly cleaned up after each test run.');
    } else {
        logError('Some database cleanup checks failed! ❌');
        logWarning('Please fix the issues above to ensure proper test data cleanup.');
        process.exit(1);
    }
}

// Run verification if this script is executed directly
if (require.main === module) {
    verifyDatabaseCleanup();
}

module.exports = {
    verifyDatabaseCleanup,
    checkTestFile,
    findTestFiles,
    checkGlobalSetup,
    checkDatabaseCleanupService,
    checkDatabaseCleanupServiceTests
}; 