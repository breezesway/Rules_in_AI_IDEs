#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Optimizing npm installation...');

const startTime = Date.now();

try {
  // Check if package-lock.json exists
  if (!fs.existsSync('package-lock.json')) {
    console.log('⚠️  No package-lock.json found, generating...');
    execSync('npm install --package-lock-only', { stdio: 'inherit' });
  }

  // Install production dependencies and essential dev dependencies
  console.log('📦 Installing production dependencies and essential dev dependencies...');
  execSync('npm ci --omit=dev && npm install --no-save typescript tsc-alias @types/pa11y', { stdio: 'inherit' });

  const endTime = Date.now();
  const duration = (endTime - startTime) / 1000;

  console.log(`✅ Installation completed in ${duration.toFixed(2)} seconds`);
  
  // Show dependency count
  const nodeModulesPath = path.join(process.cwd(), 'node_modules');
  if (fs.existsSync(nodeModulesPath)) {
    const packages = fs.readdirSync(nodeModulesPath).filter(name => 
      !name.startsWith('.') && !name.startsWith('@')
    );
    const scopedPackages = fs.readdirSync(nodeModulesPath).filter(name => 
      name.startsWith('@')
    );
    
    console.log(`📊 Installed packages: ${packages.length} direct + ${scopedPackages.length} scoped`);
  }

} catch (error) {
  console.error('❌ Installation failed:', error.message);
  process.exit(1);
} 