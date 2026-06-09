#!/usr/bin/env node

/**
 * MongoDB Setup Script
 * Manages local MongoDB development environment
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Colored console output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function log(message, type = 'info') {
    const timestamp = new Date().toLocaleTimeString();
    const colorMap = {
        info: colors.blue,
        success: colors.green,
        warning: colors.yellow,
        error: colors.red
    };
    const color = colorMap[type] || colors.reset;
    console.log(`${color}[${timestamp}] ${message}${colors.reset}`);
}

function checkDocker() {
    try {
        execSync('docker --version', { stdio: 'ignore' });
        execSync('docker-compose --version', { stdio: 'ignore' });
        return true;
    } catch (error) {
        return false;
    }
}

function waitForService(url, serviceName, maxAttempts = 30) {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        
        const checkService = () => {
            attempts++;
            
            try {
                // For MongoDB, we'll just check if the container is running
                execSync(`docker-compose ps ${serviceName}`, { stdio: 'ignore' });
                log(`${serviceName} is ready!`, 'success');
                resolve();
            } catch (error) {
                if (attempts >= maxAttempts) {
                    reject(new Error(`${serviceName} failed to start after ${maxAttempts} attempts`));
                    return;
                }
                
                log(`Waiting for ${serviceName}... (attempt ${attempts}/${maxAttempts})`, 'info');
                setTimeout(checkService, 2000);
            }
        };
        
        checkService();
    });
}

function populateEnvFile() {
    const envPath = path.join(process.cwd(), '.env.local');
    const envExamplePath = path.join(process.cwd(), 'env.local.example');
    
    // Check if .env.local already exists
    if (fs.existsSync(envPath)) {
        log('.env.local already exists, skipping creation', 'info');
        return;
    }
    
    // Copy from example if it exists
    if (fs.existsSync(envExamplePath)) {
        fs.copyFileSync(envExamplePath, envPath);
        log('Created .env.local from env.local.example', 'success');
    } else {
        // Create basic .env.local
        const envContent = `# MongoDB Configuration (local development)
MONGODB_URL=mongodb://admin:password123@localhost:27017/?authSource=admin
MONGODB_DB_NAME=accessibility_testing

# Local Development Settings
NODE_ENV=development
PORT=3000
`;
        fs.writeFileSync(envPath, envContent);
        log('Created .env.local with default MongoDB configuration', 'success');
    }
}

async function startMongoDB() {
    log('Starting MongoDB services...');
    
    if (!checkDocker()) {
        log('Docker and Docker Compose are required. Please install them first.', 'error');
        process.exit(1);
    }

    try {
        // Start MongoDB services
        execSync('docker-compose up -d', { stdio: 'inherit' });
        
        log('Waiting for MongoDB services to be ready...');
        
        // Wait for MongoDB
        await waitForService('mongodb://localhost:27017', 'mongodb');

        log('MongoDB stack is ready!', 'success');
        log('Mongo Express: http://localhost:8081', 'info');
        log('MongoDB: localhost:27017', 'info');
        
        // Auto-populate .env.local
        populateEnvFile();

    } catch (error) {
        log(`Failed to start MongoDB: ${error.message}`, 'error');
        process.exit(1);
    }
}

function stopMongoDB() {
    log('Stopping MongoDB services...');
    try {
        execSync('docker-compose down', { stdio: 'inherit' });
        log('MongoDB services stopped successfully', 'success');
    } catch (error) {
        log(`Failed to stop MongoDB: ${error.message}`, 'error');
        process.exit(1);
    }
}

function resetMongoDB() {
    log('Resetting MongoDB (this will delete all data)...');
    try {
        execSync('docker-compose down -v', { stdio: 'inherit' });
        execSync('docker-compose up -d', { stdio: 'inherit' });
        log('MongoDB reset successfully', 'success');
    } catch (error) {
        log(`Failed to reset MongoDB: ${error.message}`, 'error');
        process.exit(1);
    }
}

function showStatus() {
    log('MongoDB service status:');
    try {
        execSync('docker-compose ps', { stdio: 'inherit' });
    } catch (error) {
        log('Failed to get service status', 'error');
        process.exit(1);
    }
}

function showLogs() {
    log('MongoDB service logs:');
    try {
        execSync('docker-compose logs', { stdio: 'inherit' });
    } catch (error) {
        log('Failed to get service logs', 'error');
        process.exit(1);
    }
}

function showEnv() {
    log('Environment configuration:');
    populateEnvFile();
    
    const envPath = path.join(process.cwd(), '.env.local');
    if (fs.existsSync(envPath)) {
        const content = fs.readFileSync(envPath, 'utf8');
        console.log(content);
    } else {
        log('No .env.local file found', 'warning');
    }
}

// Main execution
const command = process.argv[2];

switch (command) {
    case 'start':
        startMongoDB();
        break;
    case 'stop':
        stopMongoDB();
        break;
    case 'reset':
        resetMongoDB();
        break;
    case 'status':
        showStatus();
        break;
    case 'logs':
        showLogs();
        break;
    case 'env':
        showEnv();
        break;
    default:
        log('MongoDB Setup Script', 'info');
        log('Usage: node scripts/mongodb-setup.js <command>', 'info');
        log('', 'info');
        log('Commands:', 'info');
        log('  start   - Start MongoDB services', 'info');
        log('  stop    - Stop MongoDB services', 'info');
        log('  reset   - Reset MongoDB (delete all data)', 'info');
        log('  status  - Show service status', 'info');
        log('  logs    - Show service logs', 'info');
        log('  env     - Show environment configuration', 'info');
        break;
} 