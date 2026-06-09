#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Starting robust npm installation...');

const startTime = Date.now();

try {
  // Step 1: Validate or regenerate package-lock.json
  console.log('🔍 Validating package-lock.json...');
  
  if (!fs.existsSync('package-lock.json')) {
    console.log('⚠️  No package-lock.json found, generating...');
    execSync('npm install --package-lock-only', { stdio: 'inherit' });
  } else {
    // Try to validate package-lock.json with a dry run
    try {
      execSync('npm ci --dry-run --omit=dev', { stdio: 'pipe', timeout: 30000 });
      console.log('✅ Package-lock.json is valid');
    } catch (error) {
      console.log('⚠️  Package-lock.json appears corrupted, regenerating...');
      try {
        fs.unlinkSync('package-lock.json');
      } catch (unlinkError) {
        console.log('⚠️  Could not delete package-lock.json, continuing...');
      }
      execSync('npm install --package-lock-only', { stdio: 'inherit' });
    }
  }

  // Step 2: Clean install with fallback
  console.log('📦 Installing dependencies...');
  
  try {
    // Try optimized installation first
    execSync('npm ci --omit=dev', { stdio: 'inherit', timeout: 120000 });
    console.log('✅ Production dependencies installed successfully');
  } catch (error) {
    console.log('⚠️  Optimized installation failed, trying fallback...');
    
    // Fallback: Clean install
    try {
      execSync('rm -rf node_modules', { stdio: 'inherit' });
      execSync('npm install --omit=dev', { stdio: 'inherit', timeout: 180000 });
      console.log('✅ Fallback installation successful');
    } catch (fallbackError) {
      console.log('❌ Fallback installation also failed, trying full install...');
      execSync('npm install', { stdio: 'inherit', timeout: 300000 });
      console.log('✅ Full installation successful');
    }
  }

  // Step 3: Install essential dev dependencies for build
  console.log('🔧 Installing essential dev dependencies...');
  try {
    execSync('npm install --no-save typescript tsc-alias @types/pa11y', { stdio: 'inherit' });
    console.log('✅ Essential dev dependencies installed');
  } catch (error) {
    console.log('⚠️  Could not install essential dev dependencies, continuing...');
  }

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