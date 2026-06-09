#!/usr/bin/env node

/**
 * Development Setup Script
 * 
 * This script handles the initial build and then starts the development server
 * with hot reloading enabled. It also provides options for local MongoDB setup.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 Setting up development environment...');

// Check if user wants to start MongoDB
const startMongoDB = process.argv.includes('--mongodb') || process.argv.includes('-m');
const skipMongoDB = process.argv.includes('--no-mongodb');

if (startMongoDB && !skipMongoDB) {
    console.log('🗄️  Setting up local MongoDB instance...');
    try {
        // Check if MongoDB is already running
        const mongoStatus = spawn('node', ['scripts/mongodb-setup.js', 'status'], {
            stdio: 'pipe'
        });
        
        // If not running, start it
        console.log('📦 Starting local MongoDB...');
        execSync('node scripts/mongodb-setup.js start', { stdio: 'inherit' });
        console.log('✅ Local MongoDB is ready');
    } catch (error) {
        console.log('⚠️  MongoDB setup failed, continuing without it...');
        console.log('   You can start it manually with: node scripts/mongodb-setup.js start');
    }
}

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

// Check for .env.local file
const envLocalPath = path.join(__dirname, '..', '.env.local');
const envExamplePath = path.join(__dirname, '..', 'env.local.example');

if (!fs.existsSync(envLocalPath) && fs.existsSync(envExamplePath)) {
    console.log('📝 Creating .env.local from template...');
    try {
        fs.copyFileSync(envExamplePath, envLocalPath);
        console.log('✅ .env.local created');
    } catch (error) {
        console.error('❌ Failed to create .env.local:', error.message);
    }
}

console.log('🔄 Starting development server with hot reload...');
console.log('📝 TypeScript compiler will watch for changes and rebuild automatically');
console.log('🔄 Nodemon will restart the server when dist files change');
console.log('🌐 Web interface will be available at: http://localhost:3000');

if (startMongoDB && !skipMongoDB) {
    console.log('🗄️  Local Mongo Express: http://localhost:8081');
    console.log('🗄️  Local MongoDB: localhost:27017');
}

console.log('');
console.log('💡 Development Tips:');
console.log('   - Use Ctrl+C to stop the development server');
console.log('   - MongoDB commands:');
console.log('     • node scripts/mongodb-setup.js start   - Start MongoDB');
console.log('     • node scripts/mongodb-setup.js stop    - Stop MongoDB');
console.log('     • node scripts/mongodb-setup.js reset   - Reset database');
console.log('     • node scripts/mongodb-setup.js status  - Check status');
console.log('     • node scripts/mongodb-setup.js logs    - View logs');
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