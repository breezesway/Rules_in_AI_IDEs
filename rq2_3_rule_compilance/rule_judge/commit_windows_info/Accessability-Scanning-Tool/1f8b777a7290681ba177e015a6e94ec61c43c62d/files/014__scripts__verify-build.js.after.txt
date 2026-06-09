#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying build output...');

const expectedDirs = [
  'dist',
  'dist/public',
  'dist/web',
  'dist/utils',
  'dist/core',
  'dist/components'
];

const expectedFiles = [
  'dist/public/index.html',
  'dist/public/app.js',
  'dist/public/styles.css',
  'dist/web/server.js'
];

try {
  let allGood = true;

  // Check directories
  for (const dir of expectedDirs) {
    const fullPath = path.join(__dirname, '..', dir);
    if (!fs.existsSync(fullPath)) {
      console.log(`❌ Missing directory: ${dir}`);
      allGood = false;
    } else {
      console.log(`✅ Directory exists: ${dir}`);
    }
  }

  // Check files
  for (const file of expectedFiles) {
    const fullPath = path.join(__dirname, '..', file);
    if (!fs.existsSync(fullPath)) {
      console.log(`❌ Missing file: ${file}`);
      allGood = false;
    } else {
      const stats = fs.statSync(fullPath);
      console.log(`✅ File exists: ${file} (${stats.size} bytes)`);
    }
  }

  if (allGood) {
    console.log('✅ Build verification passed');
  } else {
    console.log('❌ Build verification failed');
    process.exit(1);
  }
} catch (error) {
  console.error('❌ Error verifying build:', error.message);
  process.exit(1);
} 