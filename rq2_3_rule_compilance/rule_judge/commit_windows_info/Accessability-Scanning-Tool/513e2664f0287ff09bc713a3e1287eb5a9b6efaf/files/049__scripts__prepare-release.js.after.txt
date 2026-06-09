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

function checkGitStatus() {
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf8' });
    return status.trim().length === 0;
  } catch (error) {
    return false;
  }
}

function validateChangelog() {
  const changelogPath = 'CHANGELOG.md';

  if (!fs.existsSync(changelogPath)) {
    log('❌ CHANGELOG.md not found', 'red');
    return false;
  }

  const changelog = fs.readFileSync(changelogPath, 'utf8');
  const version = getCurrentVersion();

  // Check if current version is in changelog
  if (!changelog.includes(`## [${version}]`)) {
    log(`❌ Version ${version} not found in CHANGELOG.md`, 'red');
    return false;
  }

  // Check for [Unreleased] section
  if (!changelog.includes('## [Unreleased]')) {
    log('❌ [Unreleased] section not found in CHANGELOG.md', 'red');
    return false;
  }

  return true;
}

function runTests() {
  log('🧪 Running tests...', 'cyan');
  try {
    execSync('npm test', { stdio: 'inherit' });
    return true;
  } catch (error) {
    log('❌ Tests failed', 'red');
    return false;
  }
}

function runLinting() {
  log('🔍 Running linting...', 'cyan');
  try {
    execSync('npm run lint', { stdio: 'inherit' });
    return true;
  } catch (error) {
    log('❌ Linting failed', 'red');
    return false;
  }
}

function runTypeChecking() {
  log('🔧 Running type checking...', 'cyan');
  try {
    execSync('npm run typecheck', { stdio: 'inherit' });
    return true;
  } catch (error) {
    log('❌ Type checking failed', 'red');
    return false;
  }
}

function buildProject() {
  log('🏗️  Building project...', 'cyan');
  try {
    // Add build command if it exists
    if (fs.existsSync('package.json')) {
      const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
      if (packageJson.scripts && packageJson.scripts.build) {
        execSync('npm run build', { stdio: 'inherit' });
      }
    }
    return true;
  } catch (error) {
    log('❌ Build failed', 'red');
    return false;
  }
}

function generateReleaseNotes() {
  const changelogPath = 'CHANGELOG.md';
  const version = getCurrentVersion();

  if (!fs.existsSync(changelogPath)) {
    return null;
  }

  const changelog = fs.readFileSync(changelogPath, 'utf8');
  const versionStart = changelog.indexOf(`## [${version}]`);

  if (versionStart === -1) {
    return null;
  }

  const nextVersionStart = changelog.indexOf('\n## [', versionStart + 1);
  const versionEnd = nextVersionStart !== -1 ? nextVersionStart : changelog.length;

  return changelog.slice(versionStart, versionEnd).trim();
}

function main() {
  log('🚀 Preparing release...', 'cyan');

  const version = getCurrentVersion();
  log(`📦 Current version: ${version}`, 'blue');

  let allChecksPass = true;

  // Check git status
  if (!checkGitStatus()) {
    log('⚠️  Git working directory is not clean', 'yellow');
    allChecksPass = false;
  } else {
    log('✅ Git working directory is clean', 'green');
  }

  // Validate changelog
  if (!validateChangelog()) {
    allChecksPass = false;
  } else {
    log('✅ Changelog is valid', 'green');
  }

  // Run type checking
  if (!runTypeChecking()) {
    allChecksPass = false;
  } else {
    log('✅ Type checking passed', 'green');
  }

  // Run linting
  if (!runLinting()) {
    allChecksPass = false;
  } else {
    log('✅ Linting passed', 'green');
  }

  // Run tests
  if (!runTests()) {
    allChecksPass = false;
  } else {
    log('✅ Tests passed', 'green');
  }

  // Build project
  if (!buildProject()) {
    allChecksPass = false;
  } else {
    log('✅ Build completed', 'green');
  }

  if (allChecksPass) {
    log('\n🎉 Release preparation completed successfully!', 'green');

    const releaseNotes = generateReleaseNotes();
    if (releaseNotes) {
      log('\n📋 Release Notes:', 'cyan');
      log(releaseNotes, 'bright');
    }

    log('\n📝 Next steps:', 'cyan');
    log('1. Review the release notes above', 'yellow');
    log('2. Push to repository: git push origin main --tags', 'yellow');
    log('3. Create GitHub release with the generated notes', 'yellow');
    log('4. Publish to npm: npm publish', 'yellow');
  } else {
    log('\n❌ Release preparation failed', 'red');
    log('Please fix the issues above before proceeding with the release', 'yellow');
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { validateChangelog, generateReleaseNotes };
