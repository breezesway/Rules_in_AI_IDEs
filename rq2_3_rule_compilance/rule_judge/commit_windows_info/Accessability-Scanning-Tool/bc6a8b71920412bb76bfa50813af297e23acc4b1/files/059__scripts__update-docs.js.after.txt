#!/usr/bin/env node

/**
 * Documentation Update Script
 * 
 * This script helps maintain the reference documentation files when changes are made to the codebase.
 * It can scan for changes and suggest updates to the relevant documentation files.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI color codes for better CLI experience
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

// Reference files that need to be maintained
const REFERENCE_FILES = {
  'docs/AI_DEVELOPMENT_GUIDE.md': 'AI-specific development guidelines',
  'docs/DEPENDENCY_MAP.md': 'Complete dependency relationships',
  'docs/ARCHITECTURE_DIAGRAM.md': 'Visual system architecture',
  'docs/QUICK_REFERENCE.md': 'Fast reference for common operations',
  'docs/PROJECT_OVERVIEW.md': 'High-level project understanding',
  'README.md': 'User-facing documentation',
  'CHANGELOG.md': 'Change tracking'
};

// Critical files that should never be broken
const CRITICAL_FILES = [
  'src/core/types/common.ts',
  'src/utils/services/error-handler-service.ts',
  'src/utils/services/configuration-service.ts',
  'src/web/server.ts'
];

// Service files pattern
const SERVICE_FILES_PATTERN = /src\/utils\/services\/.*\.ts$/;

// Type files pattern
const TYPE_FILES_PATTERN = /src\/core\/types\/.*\.ts$/;

/**
 * Log a message with color
 */
function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * Check if a file exists
 */
function fileExists(filePath) {
  return fs.existsSync(filePath);
}

/**
 * Get git status of files
 */
function getGitStatus() {
  try {
    const status = execSync('git status --porcelain', { encoding: 'utf8' });
    return status.split('\n').filter(line => line.trim());
  } catch (error) {
    log('Warning: Could not get git status. Make sure you are in a git repository.', 'yellow');
    return [];
  }
}

/**
 * Check for modified TypeScript files
 */
function getModifiedTsFiles() {
  const status = getGitStatus();
  return status
    .filter(line => line.match(/^[AM]\s+.*\.ts$/))
    .map(line => line.substring(3))
    .filter(file => file.startsWith('src/'));
}

/**
 * Check for new service files
 */
function getNewServiceFiles() {
  const status = getGitStatus();
  return status
    .filter(line => line.match(/^A\s+.*\.ts$/))
    .map(line => line.substring(3))
    .filter(file => SERVICE_FILES_PATTERN.test(file));
}

/**
 * Check for new type files
 */
function getNewTypeFiles() {
  const status = getGitStatus();
  return status
    .filter(line => line.match(/^A\s+.*\.ts$/))
    .map(line => line.substring(3))
    .filter(file => TYPE_FILES_PATTERN.test(file));
}

/**
 * Check for modified critical files
 */
function getModifiedCriticalFiles() {
  const status = getGitStatus();
  return status
    .filter(line => line.match(/^[AM]\s+.*\.ts$/))
    .map(line => line.substring(3))
    .filter(file => CRITICAL_FILES.includes(file));
}

/**
 * Generate documentation update suggestions
 */
function generateUpdateSuggestions() {
  log('\n🔍 Analyzing codebase changes...', 'cyan');
  
  const modifiedTsFiles = getModifiedTsFiles();
  const newServiceFiles = getNewServiceFiles();
  const newTypeFiles = getNewTypeFiles();
  const modifiedCriticalFiles = getModifiedCriticalFiles();
  
  log('\n📊 Change Summary:', 'bright');
  
  if (modifiedTsFiles.length > 0) {
    log(`\n📝 Modified TypeScript files (${modifiedTsFiles.length}):`, 'yellow');
    modifiedTsFiles.forEach(file => log(`  - ${file}`, 'yellow'));
  }
  
  if (newServiceFiles.length > 0) {
    log(`\n🆕 New service files (${newServiceFiles.length}):`, 'green');
    newServiceFiles.forEach(file => log(`  - ${file}`, 'green'));
  }
  
  if (newTypeFiles.length > 0) {
    log(`\n🆕 New type files (${newTypeFiles.length}):`, 'green');
    newTypeFiles.forEach(file => log(`  - ${file}`, 'green'));
  }
  
  if (modifiedCriticalFiles.length > 0) {
    log(`\n⚠️  Modified critical files (${modifiedCriticalFiles.length}):`, 'red');
    modifiedCriticalFiles.forEach(file => log(`  - ${file}`, 'red'));
    log('\n🚨 WARNING: Critical files have been modified!', 'red');
    log('   Please ensure these changes are safe and update documentation accordingly.', 'red');
  }
  
  // Generate update suggestions
  log('\n📚 Documentation Update Suggestions:', 'bright');
  
  if (newServiceFiles.length > 0) {
    log('\n🔄 For new services, update:', 'cyan');
    log('  • docs/DEPENDENCY_MAP.md - Add to service dependencies section', 'cyan');
    log('  • docs/ARCHITECTURE_DIAGRAM.md - Update service layer diagram', 'cyan');
    log('  • docs/QUICK_REFERENCE.md - Add to common patterns section', 'cyan');
  }
  
  if (newTypeFiles.length > 0) {
    log('\n🔄 For new types, update:', 'cyan');
    log('  • docs/DEPENDENCY_MAP.md - Add to core dependencies section', 'cyan');
    log('  • docs/QUICK_REFERENCE.md - Add type definition patterns', 'cyan');
  }
  
  if (modifiedTsFiles.length > 0) {
    log('\n🔄 For modified files, check:', 'cyan');
    log('  • docs/DEPENDENCY_MAP.md - Update import patterns if needed', 'cyan');
    log('  • docs/QUICK_REFERENCE.md - Update common patterns if needed', 'cyan');
  }
  
  if (modifiedCriticalFiles.length > 0) {
    log('\n🔄 For critical file changes, update:', 'cyan');
    log('  • docs/AI_DEVELOPMENT_GUIDE.md - Update critical rules if needed', 'cyan');
    log('  • docs/DEPENDENCY_MAP.md - Update breaking change prevention rules', 'cyan');
    log('  • docs/QUICK_REFERENCE.md - Update common issues section', 'cyan');
  }
  
  // Always suggest CHANGELOG update
  log('\n🔄 Always update:', 'cyan');
  log('  • CHANGELOG.md - Add entry for this change', 'cyan');
}

/**
 * Check if reference files exist
 */
function checkReferenceFiles() {
  log('\n📋 Reference File Status:', 'bright');
  
  let allExist = true;
  
  Object.entries(REFERENCE_FILES).forEach(([filename, description]) => {
    if (fileExists(filename)) {
      log(`  ✅ ${filename} - ${description}`, 'green');
    } else {
      log(`  ❌ ${filename} - ${description} (MISSING)`, 'red');
      allExist = false;
    }
  });
  
  if (!allExist) {
    log('\n⚠️  Some reference files are missing!', 'yellow');
    log('   Please ensure all reference files are present before making changes.', 'yellow');
  }
  
  return allExist;
}

/**
 * Validate critical files
 */
function validateCriticalFiles() {
  log('\n🔒 Critical File Validation:', 'bright');
  
  let allExist = true;
  
  CRITICAL_FILES.forEach(file => {
    if (fileExists(file)) {
      log(`  ✅ ${file}`, 'green');
    } else {
      log(`  ❌ ${file} (MISSING)`, 'red');
      allExist = false;
    }
  });
  
  if (!allExist) {
    log('\n🚨 CRITICAL ERROR: Some critical files are missing!', 'red');
    log('   The application may not function correctly.', 'red');
  }
  
  return allExist;
}

/**
 * Show usage information
 */
function showUsage() {
  log('\n📖 Usage:', 'bright');
  log('  node scripts/update-docs.js [command]', 'cyan');
  log('\nCommands:', 'bright');
  log('  analyze    - Analyze changes and suggest documentation updates', 'cyan');
  log('  check      - Check if all reference files exist', 'cyan');
  log('  validate   - Validate critical files exist', 'cyan');
  log('  all        - Run all checks and analysis', 'cyan');
  log('  help       - Show this help message', 'cyan');
}

/**
 * Main function
 */
function main() {
  const command = process.argv[2] || 'all';
  
  log('🤖 Documentation Update Script', 'bright');
  log('==============================', 'bright');
  
  switch (command) {
    case 'analyze':
      generateUpdateSuggestions();
      break;
      
    case 'check':
      checkReferenceFiles();
      break;
      
    case 'validate':
      validateCriticalFiles();
      break;
      
    case 'all':
      checkReferenceFiles();
      validateCriticalFiles();
      generateUpdateSuggestions();
      break;
      
    case 'help':
    default:
      showUsage();
      break;
  }
  
  log('\n✨ Documentation maintenance complete!', 'green');
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = {
  checkReferenceFiles,
  validateCriticalFiles,
  generateUpdateSuggestions,
  REFERENCE_FILES,
  CRITICAL_FILES
}; 