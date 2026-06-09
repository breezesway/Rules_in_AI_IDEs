#!/usr/bin/env node

import * as fs from 'fs';
import { execSync } from 'child_process';

// ANSI color codes for better output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    red: '\x1b[31m',
} as const;

type ColorName = keyof typeof colors;

interface PackageJson {
    version: string;
    [key: string]: unknown;
}

function log(message: string, color: ColorName = 'reset'): void {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function getCurrentVersion(): string {
    const packageJson: PackageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    return packageJson.version;
}

function checkVersionInChangelog(): boolean {
    const changelogPath = 'CHANGELOG.md';

    if (!fs.existsSync(changelogPath)) {
        log('⚠️  CHANGELOG.md not found', 'yellow');
        return false;
    }

    const changelog = fs.readFileSync(changelogPath, 'utf8');
    const version = getCurrentVersion();

    // Check if current version is in changelog
    if (!changelog.includes(`## [${version}]`)) {
        log(`⚠️  Version ${version} not found in CHANGELOG.md`, 'yellow');
        log('💡 Run: npm run changelog:add to add changelog entries', 'cyan');
        return false;
    }

    return true;
}

function getStagedFiles(): string[] {
    try {
        const output = execSync('git diff --cached --name-only', { encoding: 'utf8' });
        return output.trim().split('\n').filter(file => file.length > 0);
    } catch (error) {
        log('Error getting staged files', 'red');
        return [];
    }
}

function runCommand(command: string, description: string): boolean {
    try {
        log(`🔧 ${description}...`, 'blue');
        execSync(command, { stdio: 'inherit' });
        log(`✅ ${description} completed`, 'green');
        return true;
    } catch (error) {
        log(`❌ ${description} failed`, 'red');
        return false;
    }
}

function main(): void {
    log('🚀 Running pre-commit checks...', 'bright');

    const stagedFiles = getStagedFiles();
    if (stagedFiles.length === 0) {
        log('No staged files found', 'yellow');
        return;
    }

    // Check if version is in changelog
    if (!checkVersionInChangelog()) {
        log('❌ Pre-commit check failed: Version not in changelog', 'red');
        process.exit(1);
    }

    // Run linting
    if (!runCommand('npm run lint:fix', 'Linting and fixing')) {
        log('❌ Pre-commit check failed: Linting issues', 'red');
        process.exit(1);
    }

    // Run formatting
    if (!runCommand('npm run format', 'Formatting code')) {
        log('❌ Pre-commit check failed: Formatting issues', 'red');
        process.exit(1);
    }

    // Run type checking
    if (!runCommand('npm run typecheck', 'Type checking')) {
        log('❌ Pre-commit check failed: Type errors', 'red');
        process.exit(1);
    }

    // Stage any fixes that were applied
    try {
        execSync('git add .', { stdio: 'inherit' });
    } catch (error) {
        log('Warning: Could not stage automatic fixes', 'yellow');
    }

    log('✅ All pre-commit checks passed!', 'green');
}

if (require.main === module) {
    main();
} 