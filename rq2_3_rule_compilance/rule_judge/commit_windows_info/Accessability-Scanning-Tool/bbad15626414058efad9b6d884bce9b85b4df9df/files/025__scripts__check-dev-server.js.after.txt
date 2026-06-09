#!/usr/bin/env node

/**
 * Development Server Check and Start Script
 * 
 * This script checks if the local development server is running on port 3000.
 * If not, it starts the development server using the existing dev:start script.
 * Used by E2E tests to ensure the local server is available.
 */

const { spawn, execSync } = require('child_process');
const http = require('http');
const path = require('path');

function log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    console.log(`${prefix} [${timestamp}] ${message}`);
}

/**
 * Check if a server is running on the specified port
 */
function checkServerRunning(port) {
    return new Promise((resolve) => {
        const req = http.get(`http://localhost:${port}`, (res) => {
            // Check if we get a valid response (status code 200-499)
            if (res.statusCode >= 200 && res.statusCode < 500) {
                resolve(true);
            } else {
                resolve(false);
            }
        });
        
        req.on('error', () => {
            resolve(false);
        });
        
        req.setTimeout(5000, () => {
            req.destroy();
            resolve(false);
        });
    });
}

/**
 * Wait for server to be ready with health check
 */
function waitForServerReady(port, maxAttempts = 30) {
    return new Promise((resolve, reject) => {
        let attempts = 0;
        const interval = setInterval(async () => {
            attempts++;
            try {
                const isRunning = await checkServerRunning(port);
                if (isRunning) {
                    clearInterval(interval);
                    log(`Server is ready at http://localhost:${port}`, 'success');
                    resolve();
                } else if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    log(`Server failed to start after ${maxAttempts} attempts`, 'error');
                    reject(new Error('Server startup timeout'));
                }
            } catch (error) {
                if (attempts >= maxAttempts) {
                    clearInterval(interval);
                    log(`Server health check failed after ${maxAttempts} attempts`, 'error');
                    reject(error);
                }
            }
        }, 2000);
    });
}

/**
 * Start the development server
 */
async function startDevServer() {
    log('Starting development server...');
    
    return new Promise((resolve, reject) => {
        const devProcess = spawn('node', ['scripts/start-dev.js', 'start'], {
            stdio: 'pipe',
            shell: true,
            cwd: path.join(__dirname, '..')
        });
        
        let output = '';
        
        devProcess.stdout.on('data', (data) => {
            const message = data.toString();
            output += message;
            process.stdout.write(message);
        });
        
        devProcess.stderr.on('data', (data) => {
            const message = data.toString();
            output += message;
            process.stderr.write(message);
        });
        
        devProcess.on('error', (error) => {
            log(`Failed to start development server: ${error.message}`, 'error');
            reject(error);
        });
        
        devProcess.on('exit', (code) => {
            if (code !== 0) {
                log(`Development server exited with code ${code}`, 'error');
                reject(new Error(`Development server exited with code ${code}`));
            }
        });
        
        // Wait for server to be ready
        waitForServerReady(3000)
            .then(() => {
                log('Development server started successfully!', 'success');
                resolve(devProcess);
            })
            .catch((error) => {
                devProcess.kill('SIGTERM');
                reject(error);
            });
    });
}

/**
 * Main function to check and start server if needed
 */
async function main() {
    log('Checking if development server is running...');
    
    try {
        // First check if server is already running
        const isRunning = await checkServerRunning(3000);
        
        if (isRunning) {
            log('Development server is already running on port 3000', 'success');
            // Wait a moment to ensure it's fully ready
            await new Promise(resolve => setTimeout(resolve, 2000));
            return;
        }
        
        log('Development server not running, starting it...', 'info');
        await startDevServer();
        
        // Wait for server to be fully ready
        log('Waiting for server to be fully ready...', 'info');
        await waitForServerReady(3000);
        
    } catch (error) {
        log(`Failed to check/start development server: ${error.message}`, 'error');
        process.exit(1);
    }
}

// Run the script
if (require.main === module) {
    main().catch((error) => {
        log(`Script failed: ${error.message}`, 'error');
        process.exit(1);
    });
}

module.exports = {
    checkServerRunning,
    waitForServerReady,
    startDevServer,
    main
}; 