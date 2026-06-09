#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function getCurrentVersion() {
  try {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    return packageJson.version;
  } catch (error) {
    log(`❌ Cannot read package.json: ${error.message}`, 'red');
    return null;
  }
}

function validateVersionConsistency() {
  log(`🔍 Validating version consistency across all files...`, 'cyan');

  const currentVersion = getCurrentVersion();
  if (!currentVersion) {
    return false;
  }

  log(`📦 Current version: ${currentVersion}`, 'blue');

  const issues = [];
  const warnings = [];

  // Check package-lock.json
  try {
    if (fs.existsSync('package-lock.json')) {
      const packageLock = JSON.parse(fs.readFileSync('package-lock.json', 'utf8'));

      if (packageLock.version !== currentVersion) {
        issues.push(
          `package-lock.json version mismatch: expected ${currentVersion}, got ${packageLock.version}`
        );
      }

      if (
        packageLock.packages &&
        packageLock.packages[''] &&
        packageLock.packages[''].version !== currentVersion
      ) {
        issues.push(
          `package-lock.json packages[""] version mismatch: expected ${currentVersion}, got ${packageLock.packages[''].version}`
        );
      }
    } else {
      warnings.push('package-lock.json not found');
    }
  } catch (error) {
    issues.push(`Cannot read package-lock.json: ${error.message}`);
  }

  // Check scripts/README.md for outdated examples
  try {
    if (fs.existsSync('scripts/README.md')) {
      const content = fs.readFileSync('scripts/README.md', 'utf8');
      const [major, minor, patch] = currentVersion.split('.').map(Number);

      // Check if version examples are consistent
      const expectedPatchExample = `${major}.${minor}.${patch + 1}`;
      const expectedMinorExample = `${major}.${minor + 1}.0`;

      const patchMatch = content.match(/npm run version:patch\s+#\s+([\d.]+)\s+→\s+([\d.]+)/);
      const minorMatch = content.match(/npm run version:minor\s+#\s+([\d.]+)\s+→\s+([\d.]+)/);

      if (patchMatch && patchMatch[1] !== currentVersion) {
        issues.push(
          `scripts/README.md patch example uses wrong base version: expected ${currentVersion}, got ${patchMatch[1]}`
        );
      }

      if (minorMatch && minorMatch[1] !== currentVersion) {
        issues.push(
          `scripts/README.md minor example uses wrong base version: expected ${currentVersion}, got ${minorMatch[1]}`
        );
      }

      if (patchMatch && patchMatch[2] !== expectedPatchExample) {
        issues.push(
          `scripts/README.md patch example shows wrong target version: expected ${expectedPatchExample}, got ${patchMatch[2]}`
        );
      }
    }
  } catch (error) {
    warnings.push(`Cannot check scripts/README.md: ${error.message}`);
  }

  return { issues, warnings, currentVersion };
}

function findPotentialVersionReferences() {
  log(`🔍 Searching for potential hardcoded version references...`, 'cyan');

  const currentVersion = getCurrentVersion();
  if (!currentVersion) {
    return [];
  }

  const potentialFiles = [];

  // List of files and directories to check
  const searchPaths = ['README.md', 'src', 'playwright/tests', 'scripts', '*.ts', '*.js'];

  // Use ripgrep or grep to find version-like patterns
  const versionPatterns = [
    // Current version
    currentVersion,
    // Previous likely versions
    `${currentVersion.split('.')[0]}.${parseInt(currentVersion.split('.')[1]) - 1}.0`,
    `${currentVersion.split('.')[0]}.${currentVersion.split('.')[1]}.${parseInt(currentVersion.split('.')[2]) - 1}`,
    // Version patterns
    '\\d+\\.\\d+\\.\\d+',
    'version.*\\d+\\.\\d+\\.\\d+',
    'v\\d+\\.\\d+\\.\\d+',
  ];

  // Try to use ripgrep (rg) first, fall back to grep
  const searchCommand =
    fs.existsSync('/usr/local/bin/rg') || fs.existsSync('/usr/bin/rg') ? 'rg' : 'grep';

  for (const pattern of versionPatterns) {
    try {
      const cmd =
        searchCommand === 'rg'
          ? `rg -n --type-not=json --type-not=lock "${pattern}" . || true`
          : `grep -r -n --exclude="*.json" --exclude="*.lock" --exclude-dir=node_modules --exclude-dir=.git "${pattern}" . || true`;

      const result = execSync(cmd, { encoding: 'utf8', stdio: 'pipe' });

      if (result.trim()) {
        const lines = result.trim().split('\n');
        lines.forEach(line => {
          if (
            line &&
            !line.includes('CHANGELOG.md') &&
            !line.includes('package.json') &&
            !line.includes('package-lock.json')
          ) {
            potentialFiles.push(line);
          }
        });
      }
    } catch (error) {
      // Command failed, but that's okay
    }
  }

  return [...new Set(potentialFiles)]; // Remove duplicates
}

function generateVersionReport() {
  log(`\n📋 Version Consistency Report`, 'bright');
  log(`=================================`, 'bright');

  const validation = validateVersionConsistency();

  if (!validation) {
    log(`❌ Cannot generate report - package.json unreadable`, 'red');
    return false;
  }

  const { issues, warnings, currentVersion } = validation;

  // Show current version
  log(`\n📦 Current Version: ${currentVersion}`, 'blue');

  // Show issues
  if (issues.length > 0) {
    log(`\n❌ Issues Found (${issues.length}):`, 'red');
    issues.forEach((issue, index) => {
      log(`  ${index + 1}. ${issue}`, 'red');
    });
  } else {
    log(`\n✅ No version consistency issues found`, 'green');
  }

  // Show warnings
  if (warnings.length > 0) {
    log(`\n⚠️  Warnings (${warnings.length}):`, 'yellow');
    warnings.forEach((warning, index) => {
      log(`  ${index + 1}. ${warning}`, 'yellow');
    });
  }

  // Show potential version references
  const potentialRefs = findPotentialVersionReferences();
  if (potentialRefs.length > 0) {
    log(`\n🔍 Potential Version References Found (${potentialRefs.length}):`, 'cyan');
    log(`   (Review these to ensure they're intentional)`, 'cyan');
    potentialRefs.slice(0, 20).forEach((ref, index) => {
      // Limit to first 20 results
      log(`  ${index + 1}. ${ref}`, 'cyan');
    });

    if (potentialRefs.length > 20) {
      log(`  ... and ${potentialRefs.length - 20} more results`, 'cyan');
    }
  }

  // Summary
  log(`\n📊 Summary:`, 'bright');
  log(
    `  ✅ Version consistency: ${issues.length === 0 ? 'PASS' : 'FAIL'}`,
    issues.length === 0 ? 'green' : 'red'
  );
  log(`  ⚠️  Warnings: ${warnings.length}`, warnings.length > 0 ? 'yellow' : 'green');
  log(`  🔍 Potential refs: ${potentialRefs.length}`, potentialRefs.length > 0 ? 'cyan' : 'green');

  return issues.length === 0;
}

function main() {
  const action = process.argv[2];

  if (action === '--fix') {
    log(`🔧 Running version-bump with validation...`, 'cyan');
    try {
      execSync('node scripts/version-bump.js patch', { stdio: 'inherit' });
    } catch (error) {
      log(`❌ Version bump failed: ${error.message}`, 'red');
      process.exit(1);
    }
  } else if (action === '--help') {
    log(`Version Validation Tool`, 'bright');
    log(`========================`, 'bright');
    log(`Usage: node scripts/validate-versions.js [options]`, 'cyan');
    log(`Options:`, 'cyan');
    log(`  (none)    Generate version consistency report`, 'cyan');
    log(`  --fix     Run version bump with validation`, 'cyan');
    log(`  --help    Show this help message`, 'cyan');
  } else {
    // Default: generate report
    const success = generateVersionReport();

    if (!success) {
      log(`\n❌ Version validation failed`, 'red');
      process.exit(1);
    } else {
      log(`\n✅ Version validation passed`, 'green');
    }
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  validateVersionConsistency,
  findPotentialVersionReferences,
  generateVersionReport,
};
