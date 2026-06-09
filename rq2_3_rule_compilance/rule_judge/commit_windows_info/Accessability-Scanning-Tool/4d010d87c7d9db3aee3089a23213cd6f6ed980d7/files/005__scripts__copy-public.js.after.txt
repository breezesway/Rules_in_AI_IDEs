#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, '..', 'src', 'public');
const destDir = path.join(__dirname, '..', 'dist', 'public');

console.log('🔧 Copying public files...');
console.log(`Source: ${srcDir}`);
console.log(`Destination: ${destDir}`);

function copyFileSync(source, dest) {
  const destFile = path.join(dest, path.basename(source));
  fs.copyFileSync(source, destFile);
  console.log(`📄 Copied: ${path.basename(source)}`);
}

function copyDirectorySync(source, dest) {
  // Create destination directory if it doesn't exist
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
    console.log('📁 Created destination directory');
  }

  // Read source directory
  const files = fs.readdirSync(source);
  
  files.forEach(file => {
    const sourcePath = path.join(source, file);
    const destPath = path.join(dest, file);
    
    const stat = fs.statSync(sourcePath);
    
    if (stat.isDirectory()) {
      // Recursively copy subdirectories
      copyDirectorySync(sourcePath, destPath);
    } else {
      // Copy file
      copyFileSync(sourcePath, dest);
    }
  });
}

try {
  // Check if source directory exists
  if (!fs.existsSync(srcDir)) {
    console.log('⚠️  Warning: src/public directory not found, skipping copy');
    process.exit(0);
  }

  // Copy directory using pure Node.js
  copyDirectorySync(srcDir, destDir);
  
  console.log('✅ Public files copied successfully');
} catch (error) {
  console.error('❌ Error copying public files:', error.message);
  process.exit(1);
} 