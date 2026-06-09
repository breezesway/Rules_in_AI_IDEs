#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
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

// Configuration for files that need version updates
const VERSION_FILES = [
  {
    file: 'package.json',
    handler: 'updatePackageJson',
    description: 'Main package.json version',
  },
  {
    file: 'package-lock.json',
    handler: 'updatePackageLockJson',
    description: 'Package-lock.json version synchronization',
  },
  {
    file: 'scripts/README.md',
    handler: 'updateScriptsReadme',
    description: 'Version examples in scripts documentation',
  },
];

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function getCurrentVersion() {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  return packageJson.version;
}

function updatePackageJson(newVersion) {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  packageJson.version = newVersion;
  fs.writeFileSync('package.json', `${JSON.stringify(packageJson, null, 2)}\n`);
  log(`✅ Updated package.json to version ${newVersion}`, 'green');
}

function updatePackageLockJson(newVersion) {
  const packageLockPath = 'package-lock.json';

  if (!fs.existsSync(packageLockPath)) {
    log('⚠️  package-lock.json not found, skipping', 'yellow');
    return;
  }

  const packageLock = JSON.parse(fs.readFileSync(packageLockPath, 'utf8'));

  // Update both root version and packages[""] version
  packageLock.version = newVersion;
  if (packageLock.packages && packageLock.packages['']) {
    packageLock.packages[''].version = newVersion;
  }

  fs.writeFileSync(packageLockPath, `${JSON.stringify(packageLock, null, 2)}\n`);
  log(`✅ Updated package-lock.json to version ${newVersion}`, 'green');
}

function updateScriptsReadme(newVersion) {
  const readmePath = 'scripts/README.md';

  if (!fs.existsSync(readmePath)) {
    log('⚠️  scripts/README.md not found, skipping', 'yellow');
    return;
  }

  let content = fs.readFileSync(readmePath, 'utf8');

  // Update version examples based on the new version
  const [major, minor, patch] = newVersion.split('.').map(Number);

  const patchExample = `${major}.${minor}.${patch + 1}`;
  const minorExample = `${major}.${minor + 1}.0`;
  const majorExample = `${major + 1}.0.0`;

  // Update version examples in usage section
  const usageRegex =
    /npm run version:patch\s+#\s+[\d.]+\s+→\s+[\d.]+\nnpm run version:minor\s+#\s+[\d.]+\s+→\s+[\d.]+\s+\nnpm run version:major\s+#\s+[\d.]+\s+→\s+[\d.]+/;
  const newUsageText = `npm run version:patch   # ${newVersion} → ${patchExample}
npm run version:minor   # ${newVersion} → ${minorExample}  
npm run version:major   # ${newVersion} → ${majorExample}`;

  content = content.replace(usageRegex, newUsageText);

  // Update git tag example
  const gitTagRegex = /git tag v[\d.]+/;
  content = content.replace(gitTagRegex, `git tag v${patchExample}`);

  // Update commit message example
  const commitRegex = /git commit -m "chore: bump version to [\d.]+"/;
  content = content.replace(commitRegex, `git commit -m "chore: bump version to ${patchExample}"`);

  fs.writeFileSync(readmePath, content);
  log(`✅ Updated scripts/README.md version examples`, 'green');
}

function bumpVersion(currentVersion, type) {
  const [major, minor, patch] = currentVersion.split('.').map(Number);

  switch (type) {
    case 'major':
      return `${major + 1}.0.0`;
    case 'minor':
      return `${major}.${minor + 1}.0`;
    case 'patch':
      return `${major}.${minor}.${patch + 1}`;
    default:
      throw new Error(`Invalid version type: ${type}`);
  }
}

function updateChangelog(version, type) {
  const changelogPath = 'CHANGELOG.md';
  const date = new Date().toISOString().split('T')[0];

  if (!fs.existsSync(changelogPath)) {
    log('⚠️  CHANGELOG.md not found, creating new one', 'yellow');
    fs.writeFileSync(
      changelogPath,
      `# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n## [Unreleased]\n\n### Added\n- Initial release\n\n`
    );
  }

  let changelog = fs.readFileSync(changelogPath, 'utf8');

  // Create new version section
  const versionHeader = `## [${version}] - ${date}`;
  const changeTemplate =
    type === 'major'
      ? `\n### Added\n- Major feature update\n\n### Changed\n- Breaking changes\n\n### Fixed\n- Bug fixes\n\n`
      : type === 'minor'
        ? `\n### Added\n- New features\n\n### Changed\n- Enhancements\n\n### Fixed\n- Bug fixes\n\n`
        : `\n### Fixed\n- Bug fixes and improvements\n\n`;

  // Insert new version after [Unreleased]
  const unreleasedIndex = changelog.indexOf('## [Unreleased]');
  if (unreleasedIndex !== -1) {
    const nextSectionIndex = changelog.indexOf('\n## [', unreleasedIndex + 1);
    const insertionPoint = nextSectionIndex !== -1 ? nextSectionIndex : changelog.length;

    const newSection = `${versionHeader}${changeTemplate}`;
    changelog = changelog.slice(0, insertionPoint) + newSection + changelog.slice(insertionPoint);
  } else {
    // Add after the header
    const headerEnd = changelog.indexOf('\n\n') + 2;
    const newSection = `## [Unreleased]\n\n### Added\n- Future changes\n\n${versionHeader}${changeTemplate}`;
    changelog = changelog.slice(0, headerEnd) + newSection + changelog.slice(headerEnd);
  }

  fs.writeFileSync(changelogPath, changelog);
  log(`✅ Updated CHANGELOG.md with version ${version}`, 'green');
}

function validateVersionConsistency(expectedVersion) {
  log(`🔍 Validating version consistency...`, 'cyan');

  const issues = [];

  // Check package.json
  try {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    if (packageJson.version !== expectedVersion) {
      issues.push(
        `package.json version mismatch: expected ${expectedVersion}, got ${packageJson.version}`
      );
    }
  } catch (error) {
    issues.push(`Cannot read package.json: ${error.message}`);
  }

  // Check package-lock.json
  try {
    if (fs.existsSync('package-lock.json')) {
      const packageLock = JSON.parse(fs.readFileSync('package-lock.json', 'utf8'));
      if (packageLock.version !== expectedVersion) {
        issues.push(
          `package-lock.json version mismatch: expected ${expectedVersion}, got ${packageLock.version}`
        );
      }
      if (
        packageLock.packages &&
        packageLock.packages[''] &&
        packageLock.packages[''].version !== expectedVersion
      ) {
        issues.push(
          `package-lock.json packages[""] version mismatch: expected ${expectedVersion}, got ${packageLock.packages[''].version}`
        );
      }
    }
  } catch (error) {
    issues.push(`Cannot read package-lock.json: ${error.message}`);
  }

  // Check for any remaining old version references (excluding historical changelog entries)
  const previousVersion = getCurrentVersion();
  if (previousVersion !== expectedVersion) {
    const filesToCheck = ['scripts/README.md', 'README.md', 'src/**/*.ts', 'src/**/*.js'];

    // This is a simplified check - in a real implementation, you might want to use glob patterns
    log(
      `⚠️  Consider checking these files for hardcoded version references: ${filesToCheck.join(', ')}`,
      'yellow'
    );
  }

  if (issues.length > 0) {
    log(`❌ Version consistency issues found:`, 'red');
    issues.forEach(issue => log(`  - ${issue}`, 'red'));
    return false;
  }

  log(`✅ Version consistency validated`, 'green');
  return true;
}

function updateAllVersionFiles(newVersion) {
  log(`📝 Updating all version references to ${newVersion}...`, 'blue');

  for (const versionFile of VERSION_FILES) {
    try {
      if (fs.existsSync(versionFile.file)) {
        switch (versionFile.handler) {
          case 'updatePackageJson':
            updatePackageJson(newVersion);
            break;
          case 'updatePackageLockJson':
            updatePackageLockJson(newVersion);
            break;
          case 'updateScriptsReadme':
            updateScriptsReadme(newVersion);
            break;
          default:
            log(`⚠️  Unknown handler: ${versionFile.handler}`, 'yellow');
        }
      } else {
        log(`⚠️  File not found: ${versionFile.file}`, 'yellow');
      }
    } catch (error) {
      log(`❌ Failed to update ${versionFile.file}: ${error.message}`, 'red');
    }
  }
}

function createGitTag(version) {
  try {
    const filesToAdd = VERSION_FILES.map(f => f.file).filter(f => fs.existsSync(f));
    filesToAdd.push('CHANGELOG.md');

    execSync(`git add ${filesToAdd.join(' ')}`, { stdio: 'inherit' });
    execSync(`git commit -m "chore: bump version to ${version}"`, { stdio: 'inherit' });
    execSync(`git tag -a v${version} -m "Release version ${version}"`, { stdio: 'inherit' });
    log(`✅ Created git tag v${version}`, 'green');
  } catch (error) {
    log(`⚠️  Git operations failed: ${error.message}`, 'yellow');
  }
}

function main() {
  const versionType = process.argv[2];

  if (!versionType || !['major', 'minor', 'patch'].includes(versionType)) {
    log('❌ Usage: npm run version:bump <major|minor|patch>', 'red');
    process.exit(1);
  }

  try {
    log(`🚀 Starting ${versionType} version bump...`, 'cyan');

    const currentVersion = getCurrentVersion();
    const newVersion = bumpVersion(currentVersion, versionType);

    log(`📝 Bumping version from ${currentVersion} to ${newVersion}`, 'blue');

    // Update all version references
    updateAllVersionFiles(newVersion);

    // Update changelog
    updateChangelog(newVersion, versionType);

    // Validate consistency
    if (!validateVersionConsistency(newVersion)) {
      log(`❌ Version consistency validation failed`, 'red');
      process.exit(1);
    }

    // Create git tag
    createGitTag(newVersion);

    log(`\n🎉 Version bump completed successfully!`, 'green');
    log(`📦 New version: ${newVersion}`, 'bright');
    log(`📝 Please edit CHANGELOG.md to add specific changes before release`, 'yellow');

    // Show summary of updated files
    log(`\n📋 Files updated:`, 'cyan');
    VERSION_FILES.forEach(vf => {
      if (fs.existsSync(vf.file)) {
        log(`  ✅ ${vf.file} - ${vf.description}`, 'green');
      }
    });
    log(`  ✅ CHANGELOG.md - Version entry added`, 'green');
  } catch (error) {
    log(`❌ Version bump failed: ${error.message}`, 'red');
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  bumpVersion,
  updateChangelog,
  updatePackageJson,
  updatePackageLockJson,
  updateScriptsReadme,
  validateVersionConsistency,
};
