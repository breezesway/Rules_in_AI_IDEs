#!/usr/bin/env node

const fs = require('fs');
const { execSync } = require('child_process');

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
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function getCurrentVersion() {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  return packageJson.version;
}

function checkVersionInChangelog() {
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

function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only', { encoding: 'utf8' });
    return output
      .trim()
      .split('\n')
      .filter(file => file.length > 0);
  } catch (error) {
    return [];
  }
}

function runLintOnStagedFiles() {
  const stagedFiles = getStagedFiles();
  const tsFiles = stagedFiles.filter(file => file.endsWith('.ts') || file.endsWith('.js'));

  if (tsFiles.length === 0) {
    return true;
  }

  log('🔍 Running linting on staged files...', 'cyan');

  try {
    execSync(`npx eslint ${tsFiles.join(' ')}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    log('❌ Linting failed on staged files', 'red');
    log('💡 Run: npm run lint:fix to auto-fix issues', 'cyan');
    return false;
  }
}

function runPrettierOnStagedFiles() {
  const stagedFiles = getStagedFiles();
  const formatFiles = stagedFiles.filter(
    file =>
      file.endsWith('.ts') || file.endsWith('.js') || file.endsWith('.json') || file.endsWith('.md')
  );

  if (formatFiles.length === 0) {
    return true;
  }

  log('💅 Running prettier on staged files...', 'cyan');

  try {
    execSync(`npx prettier --write ${formatFiles.join(' ')}`, { stdio: 'inherit' });
    // Re-stage the formatted files
    execSync(`git add ${formatFiles.join(' ')}`, { stdio: 'inherit' });
    return true;
  } catch (error) {
    log('❌ Prettier formatting failed', 'red');
    return false;
  }
}

function checkVersionConsistency() {
  try {
    const { validateVersionConsistency } = require('./validate-versions.js');
    const validation = validateVersionConsistency();

    if (!validation || validation.issues.length > 0) {
      log('❌ Version consistency check failed', 'red');
      log('💡 Run: npm run version:validate to see detailed issues', 'cyan');
      return false;
    }

    log('✅ Version consistency check passed', 'green');
    return true;
  } catch (error) {
    log(`⚠️  Version consistency check failed: ${error.message}`, 'yellow');
    return true; // Don't block commit on validation script errors
  }
}

function checkPackageJsonVersion() {
  const stagedFiles = getStagedFiles();

  if (stagedFiles.includes('package.json')) {
    log('📦 package.json version change detected', 'blue');

    if (!checkVersionInChangelog()) {
      log('❌ Version change in package.json but not in CHANGELOG.md', 'red');
      return false;
    }

    log('✅ Version change properly documented in CHANGELOG.md', 'green');
  }

  return true;
}

function main() {
  log('🔍 Running pre-commit checks...', 'cyan');

  let allChecksPass = true;

  // Check version consistency
  if (!checkVersionConsistency()) {
    allChecksPass = false;
  }

  // Check if version changes are documented
  if (!checkPackageJsonVersion()) {
    allChecksPass = false;
  }

  // Run prettier formatting
  if (!runPrettierOnStagedFiles()) {
    allChecksPass = false;
  }

  // Run linting
  if (!runLintOnStagedFiles()) {
    allChecksPass = false;
  }

  if (allChecksPass) {
    log('✅ Pre-commit checks passed', 'green');
  } else {
    log('❌ Pre-commit checks failed', 'red');
    log('Please fix the issues above before committing', 'yellow');
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  checkVersionInChangelog,
  runLintOnStagedFiles,
  runPrettierOnStagedFiles,
  checkVersionConsistency,
};
