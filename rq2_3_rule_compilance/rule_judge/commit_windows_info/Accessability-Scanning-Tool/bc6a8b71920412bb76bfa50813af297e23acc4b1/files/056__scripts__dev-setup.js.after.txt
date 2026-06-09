#!/usr/bin/env node

/**
 * Development Setup Script
 * 
 * This script handles the initial build and then starts the development server
 * with hot reloading enabled.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up development environment...');

// Check if dist directory exists and has content
const distExists = fs.existsSync(path.join(__dirname, '../dist'));
const distHasContent = distExists && fs.readdirSync(path.join(__dirname, '../dist')).length > 0;

if (!distExists || !distHasContent) {
    console.log('📦 Building project for the first time...');
    try {
        execSync('npm run build', { stdio: 'inherit' });
        console.log('✅ Initial build completed');
    } catch (error) {
        console.error('❌ Initial build failed:', error.message);
        process.exit(1);
    }
} else {
    console.log('✅ Build directory already exists, skipping initial build');
}

// Copy public files if they don't exist in dist
const publicSrc = path.join(__dirname, '../src/public');
const publicDist = path.join(__dirname, '../dist/public');

if (!fs.existsSync(publicDist)) {
    console.log('📁 Copying public files...');
    try {
        execSync('npm run copy-public', { stdio: 'inherit' });
        console.log('✅ Public files copied');
    } catch (error) {
        console.error('❌ Failed to copy public files:', error.message);
    }
}

console.log('🔄 Starting development server with hot reload...');
console.log('📝 TypeScript compiler will watch for changes and rebuild automatically');
console.log('🔄 Nodemon will restart the server when dist files change');
console.log('🌐 Web interface will be available at: http://localhost:3000');
console.log('');

// Start the development server
const devProcess = spawn('npm', ['run', 'dev'], {
    stdio: 'inherit',
    shell: true
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down development server...');
    devProcess.kill('SIGINT');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down development server...');
    devProcess.kill('SIGTERM');
    process.exit(0);
});

devProcess.on('close', (code) => {
    console.log(`\n🔚 Development server exited with code ${code}`);
    process.exit(code);
}); 