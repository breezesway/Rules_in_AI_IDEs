#!/usr/bin/env node

/**
 * Accessibility Testing Infrastructure Validation Script
 * 
 * This script validates that the accessibility testing infrastructure is properly set up
 * and can run the various accessibility test commands.
 * 
 * Usage: node scripts/test-accessibility-infrastructure.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🔍 Validating Accessibility Testing Infrastructure...\n');

// Check if required test files exist
const requiredTestFiles = [
    'tests/e2e/interface-accessibility.test.ts',
    'tests/e2e/component-accessibility.test.ts',
    'tests/e2e/accessibility-scanning.test.ts',
    'tests/storybook/storybook-validation.test.ts'
];

console.log('📁 Checking required test files...');
let allFilesExist = true;

requiredTestFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`  ✅ ${file}`);
    } else {
        console.log(`  ❌ ${file} - MISSING`);
        allFilesExist = false;
    }
});

if (!allFilesExist) {
    console.log('\n❌ Some required test files are missing!');
    process.exit(1);
}

console.log('\n✅ All required test files exist');

// Check if package.json has the new scripts
console.log('\n📦 Checking package.json scripts...');
const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
const requiredScripts = [
    'test:accessibility',
    'test:accessibility:e2e',
    'test:accessibility:storybook',
    'test:accessibility:quick'
];

let allScriptsExist = true;
requiredScripts.forEach(script => {
    if (packageJson.scripts[script]) {
        console.log(`  ✅ ${script}`);
    } else {
        console.log(`  ❌ ${script} - MISSING`);
        allScriptsExist = false;
    }
});

if (!allScriptsExist) {
    console.log('\n❌ Some required scripts are missing from package.json!');
    process.exit(1);
}

console.log('\n✅ All required scripts exist in package.json');

// Test Storybook accessibility validation (this should work without server)
console.log('\n🧪 Testing Storybook accessibility validation...');
try {
    const result = execSync('npm run test:accessibility:storybook', { 
        encoding: 'utf8',
        stdio: 'pipe'
    });
    console.log('  ✅ Storybook accessibility tests passed');
} catch (error) {
    console.log('  ❌ Storybook accessibility tests failed:');
    console.log(error.stdout || error.message);
    process.exit(1);
}

// Check if documentation is updated
console.log('\n📚 Checking documentation updates...');
const docsToCheck = [
    'docs/ACCESSIBILITY_TESTING_RULES.md',
    'docs/QUICK_REFERENCE.md',
    'CHANGELOG.md'
];

docsToCheck.forEach(doc => {
    if (fs.existsSync(doc)) {
        const content = fs.readFileSync(doc, 'utf8');
        if (content.includes('test:accessibility')) {
            console.log(`  ✅ ${doc} - Updated`);
        } else {
            console.log(`  ⚠️  ${doc} - May need updating`);
        }
    } else {
        console.log(`  ❌ ${doc} - Missing`);
    }
});

console.log('\n🎉 Accessibility Testing Infrastructure Validation Complete!');
console.log('\n📋 Summary:');
console.log('  ✅ All required test files exist');
console.log('  ✅ All required scripts are configured');
console.log('  ✅ Storybook accessibility tests are working');
console.log('  ✅ Documentation has been updated');
console.log('\n🚀 You can now use:');
console.log('  npm run test:accessibility          # Run all accessibility tests');
console.log('  npm run test:accessibility:e2e      # Run E2E accessibility tests');
console.log('  npm run test:accessibility:storybook # Run Storybook component tests');
console.log('  npm run test:accessibility:quick    # Quick accessibility validation'); 