#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔧 Setting up build environment...');

const requiredDirs = [
  'src/public',
  'dist',
  'accessibility-reports'
];

const requiredFiles = [
  'src/public/index.html',
  'src/public/app.js',
  'src/public/styles.css'
];

try {
  // Create required directories
  for (const dir of requiredDirs) {
    const fullPath = path.join(__dirname, '..', dir);
    if (!fs.existsSync(fullPath)) {
      fs.mkdirSync(fullPath, { recursive: true });
      console.log(`📁 Created directory: ${dir}`);
    } else {
      console.log(`✅ Directory exists: ${dir}`);
    }
  }

  // Check required files
  for (const file of requiredFiles) {
    const fullPath = path.join(__dirname, '..', file);
    if (!fs.existsSync(fullPath)) {
      console.log(`⚠️  Warning: Required file not found: ${file}`);
    } else {
      console.log(`✅ File exists: ${file}`);
    }
  }

  console.log('✅ Build environment setup complete');
} catch (error) {
  console.error('❌ Error setting up build environment:', error.message);
  process.exit(1);
} 