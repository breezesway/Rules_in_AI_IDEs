#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const srcDir = path.join(__dirname, '..', 'src', 'public');
const destDir = path.join(__dirname, '..', 'dist', 'public');

console.log('🔧 Copying public files...');
console.log(`Source: ${srcDir}`);
console.log(`Destination: ${destDir}`);

try {
  // Check if source directory exists
  if (!fs.existsSync(srcDir)) {
    console.log('⚠️  Warning: src/public directory not found, skipping copy');
    process.exit(0);
  }

  // Create destination directory if it doesn't exist
  if (!fs.existsSync(destDir)) {
    fs.mkdirSync(destDir, { recursive: true });
    console.log('📁 Created destination directory');
  }

  // Copy files using cross-platform method
  if (process.platform === 'win32') {
    // Windows
    execSync(`xcopy "${srcDir}" "${destDir}" /E /I /Y`, { stdio: 'inherit' });
  } else {
    // Unix-like systems (Linux, macOS)
    execSync(`cp -r "${srcDir}"/* "${destDir}/"`, { stdio: 'inherit' });
  }

  console.log('✅ Public files copied successfully');
} catch (error) {
  console.error('❌ Error copying public files:', error.message);
  process.exit(1);
} 