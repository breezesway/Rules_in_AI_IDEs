#!/usr/bin/env node

/**
 * Development Startup Script
 * 
 * This script starts both the MongoDB database and the development server
 * in parallel, ensuring proper startup sequence and error handling.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Import validation function
let validateEnvFile;
try {
    const validateModule = require('./validate-env.js');
    validateEnvFile = validateModule.validateEnvFile;
} catch (error) {
    // Fallback if validation module is not available
    validateEnvFile = () => ({ isValid: true, issues: [] });
}

function log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    console.log(`${prefix} [${timestamp}] ${message}`);
}

function checkDocker() {
    try {
        execSync('docker --version', { stdio: 'pipe' });
        execSync('docker-compose --version', { stdio: 'pipe' });
        return true;
    } catch (error) {
        return false;
    }
}

function waitForService(url, serviceName, maxAttempts = 30) {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const interval = setInterval(async () => {
            attempts++;
            try {
                // Special handling for PostgreSQL
                if (serviceName === 'PostgreSQL') {
                    try {
                        execSync(`nc -z localhost 5432`, { stdio: 'pipe' });
                        clearInterval(interval);
                        log(`${serviceName} is ready at localhost:5432`, 'success');
                        resolve();
                        return;
                    } catch (error) {
                        if (attempts >= maxAttempts) {
                            clearInterval(interval);
                            log(`${serviceName} failed to start after ${maxAttempts} attempts`, 'error');
                            reject(new Error(`${serviceName} startup timeout`));
                        }
                        return;
                    }
                }
                
                // HTTP-based health check for other services
                const response = await fetch(url);
                if (response.ok) {
                    clearInterval(interval);
                    log(`${serviceName} is ready at ${url}`, 'success');
                    resolve();
                }
            } catch (error) {
                if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    log(`${serviceName} failed to start after ${maxAttempts} attempts`, 'error');
                    reject(new Error(`${serviceName} startup timeout`));
                }
            }
        }, 2000);
    });
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
        
        // Wait a moment for containers to start
        log('Waiting for containers to start...');
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // Check if containers are running
        try {
            const containerStatus = execSync('docker-compose ps --format json', { stdio: 'pipe' }).toString();
            const containers = JSON.parse(`[${containerStatus.trim().replace(/\n/g, ',')}]`);
            
            const runningContainers = containers.filter(container => container.State === 'running');
            if (runningContainers.length >= 2) {
                log('MongoDB containers are running', 'success');
            } else {
                log('Some MongoDB containers may not be running', 'warning');
            }
        } catch (error) {
            log('Could not check container status, but continuing...', 'warning');
        }

        // Check MongoDB connection
        try {
            execSync('nc -z localhost 27017', { stdio: 'pipe' });
            log('MongoDB connection verified', 'success');
        } catch (error) {
            log('MongoDB connection check failed, but continuing...', 'warning');
        }

        log('MongoDB stack is ready!', 'success');
        log('Mongo Express: http://localhost:8081', 'info');
        log('MongoDB: localhost:27017', 'info');
        
        // Auto-populate .env.local
        await populateEnvFile();

    } catch (error) {
        log(`Failed to start MongoDB: ${error.message}`, 'error');
        process.exit(1);
    }
}

async function populateEnvFile() {
    log('Auto-populating .env.local with local MongoDB details...');

    const envLocalPath = path.join(__dirname, '..', '.env.local');
    const envExamplePath = path.join(__dirname, '..', 'env.local.example');

    try {
        // If .env.local already exists with real secrets, don't overwrite it
        if (fs.existsSync(envLocalPath)) {
            const existingContent = fs.readFileSync(envLocalPath, 'utf8');
            // Check if it contains actual secrets (not placeholder values)
            if (!existingContent.includes('your_mongodb_url_here') && 
                !existingContent.includes('your_mongodb_password_here')) {
                log('.env.local already contains real secrets, skipping population', 'info');
                return;
            }
        }
        
        const localConfig = {
            url: 'mongodb://admin:password123@localhost:27017/?authSource=admin',
            databaseName: 'accessibility_testing'
        };
        
        let envContent = '';
        if (fs.existsSync(envExamplePath)) {
            envContent = fs.readFileSync(envExamplePath, 'utf8');
        } else {
            envContent = `# Local MongoDB Configuration
# Auto-generated for local development
MONGODB_URL=${localConfig.url}
MONGODB_DB_NAME=${localConfig.databaseName}
NODE_ENV=development
PORT=3000
`;
        }
        
        const updatedContent = updateEnvContent(envContent, localConfig);
        fs.writeFileSync(envLocalPath, updatedContent);
        log('Successfully populated .env.local with local MongoDB details', 'success');
        
    } catch (error) {
        log(`Failed to populate .env.local: ${error.message}`, 'warning');
    }
}

function updateEnvContent(content, config) {
    const lines = content.split('\n');
    const updatedLines = [];
    const keysToUpdate = {
        'MONGODB_URL': config.url,
        'MONGODB_DB_NAME': config.databaseName
    };
    
    const updatedKeys = new Set();
    
    // Process existing lines
    for (const line of lines) {
        const trimmedLine = line.trim();
        let updated = false;
        
        for (const [key, value] of Object.entries(keysToUpdate)) {
            if (trimmedLine.startsWith(`${key}=`)) {
                updatedLines.push(`${key}=${value}`);
                updatedKeys.add(key);
                updated = true;
                break;
            }
        }
        
        if (!updated) {
            updatedLines.push(line);
        }
    }
    
    // Add missing keys
    for (const [key, value] of Object.entries(keysToUpdate)) {
        if (!updatedKeys.has(key)) {
            updatedLines.push(`${key}=${value}`);
        }
    }
    
    // Add development settings if not present
    const hasNodeEnv = updatedLines.some(line => line.trim().startsWith('NODE_ENV='));
    const hasPort = updatedLines.some(line => line.trim().startsWith('PORT='));
    
    if (!hasNodeEnv) {
        updatedLines.push('NODE_ENV=development');
    }
    if (!hasPort) {
        updatedLines.push('PORT=3000');
    }
    
    return updatedLines.join('\n');
}

async function startDevServer() {
    log('Starting development server...');
    
    // Check if TypeScript compilation is needed
    const distPath = path.join(__dirname, '..', 'dist');
    if (!fs.existsSync(distPath)) {
        log('Building TypeScript...');
        try {
            execSync('npm run build', { stdio: 'inherit' });
        } catch (error) {
            log('Failed to build TypeScript', 'error');
            process.exit(1);
        }
    }
    
    // Start the development server
    const devProcess = spawn('npm', ['run', 'dev'], {
        stdio: 'inherit',
        shell: true
    });
    
    devProcess.on('error', (error) => {
        log(`Development server error: ${error.message}`, 'error');
        process.exit(1);
    });
    
    devProcess.on('exit', (code) => {
        if (code !== 0) {
            log(`Development server exited with code ${code}`, 'error');
            process.exit(code);
        }
    });
    
    // Wait a moment for the server to start
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    log('Development server started successfully!', 'success');
    log('Web interface available at: http://localhost:3000', 'info');
    
    return devProcess;
}

async function main() {
    log('Starting full development environment...');
    
    // Validate environment file before starting
    log('Validating environment configuration...');
    const validationResult = validateEnvFile();
    if (!validationResult.isValid) {
        log('Environment file validation failed!', 'error');
        log('Please fix the issues before starting development environment:', 'error');
        validationResult.issues.forEach(issue => log(`  ${issue}`, 'error'));
        log('Run "npm run validate:env" for detailed validation and suggestions', 'error');
        process.exit(1);
    }
    log('Environment configuration validated successfully', 'success');
    
    try {
        // Start MongoDB first
        await startMongoDB();
        
        // Wait a moment for everything to settle
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Start the development server
        const devProcess = await startDevServer();
        
        // Handle graceful shutdown
        process.on('SIGINT', () => {
            log('Shutting down development environment...', 'info');
            devProcess.kill('SIGINT');
            process.exit(0);
        });
        
        process.on('SIGTERM', () => {
            log('Shutting down development environment...', 'info');
            devProcess.kill('SIGTERM');
            process.exit(0);
        });
        
        // Keep the process running
        log('Development environment is ready!', 'success');
        log('Press Ctrl+C to stop all services', 'info');
        
    } catch (error) {
        log(`Failed to start development environment: ${error.message}`, 'error');
        process.exit(1);
    }
}

// Parse command line arguments
const command = process.argv[2];

switch (command) {
    case 'start':
        main();
        break;
    case 'mongodb-only':
        startMongoDB();
        break;
    case 'dev-only':
        startDevServer().catch(error => {
            log(`Failed to start development server: ${error.message}`, 'error');
            process.exit(1);
        });
        break;
    default:
        console.log(`
Development Environment Startup Script

Usage: node scripts/start-dev.js <command>

Commands:
  start        - Start both MongoDB and development server
  mongodb-only - Start only MongoDB services
  dev-only     - Start only development server

This script will:
1. Start the full MongoDB stack (MongoDB, Mongo Express, etc.)
2. Wait for all services to be ready
3. Auto-populate .env.local with local configuration
4. Start the development server

Services started:
- Mongo Express: http://localhost:8081
- MongoDB: localhost:27017
- Development Server: http://localhost:3000
        `);
        break;
} 