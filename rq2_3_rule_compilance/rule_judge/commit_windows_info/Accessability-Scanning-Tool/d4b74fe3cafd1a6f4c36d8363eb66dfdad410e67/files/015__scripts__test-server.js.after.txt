#!/usr/bin/env node

/**
 * Test Server for E2E Testing
 * 
 * This script starts the web server specifically for E2E testing.
 * It includes proper error handling, logging, and cleanup.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const PORT = process.env.TEST_PORT || 3000;
const HOST = process.env.TEST_HOST || 'localhost';
const BUILD_DIR = path.join(__dirname, '..', 'dist');
const SERVER_FILE = path.join(BUILD_DIR, 'web', 'server.js');

// Colors for console output
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

function log(message, color = 'reset') {
  console.log(`${colors[color]}[TEST-SERVER]${colors.reset} ${message}`);
}

function logError(message) {
  console.error(`${colors.red}[TEST-SERVER ERROR]${colors.reset} ${message}`);
}

function logSuccess(message) {
  console.log(`${colors.green}[TEST-SERVER SUCCESS]${colors.reset} ${message}`);
}

function logWarning(message) {
  console.log(`${colors.yellow}[TEST-SERVER WARNING]${colors.reset} ${message}`);
}

// Check if build exists
function checkBuild() {
  if (!fs.existsSync(SERVER_FILE)) {
    logError(`Server file not found: ${SERVER_FILE}`);
    logWarning('Building application...');
    
    return new Promise((resolve, reject) => {
      const buildProcess = spawn('npm', ['run', 'build'], {
        stdio: 'inherit',
        shell: true
      });
      
      buildProcess.on('close', (code) => {
        if (code === 0) {
          logSuccess('Build completed successfully');
          resolve();
        } else {
          logError(`Build failed with code ${code}`);
          reject(new Error(`Build failed with code ${code}`));
        }
      });
      
      buildProcess.on('error', (error) => {
        logError(`Build process error: ${error.message}`);
        reject(error);
      });
    });
  }
  
  return Promise.resolve();
}

// Start the server
function startServer() {
  return new Promise((resolve, reject) => {
    log(`Starting test server on http://${HOST}:${PORT}`);
    
    // Set environment variables for testing
    const env = {
      ...process.env,
      NODE_ENV: 'test',
      PORT: PORT.toString(),
      TEST_MODE: 'true'
    };
    
    const serverProcess = spawn('node', [SERVER_FILE], {
      env,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let serverReady = false;
    let startupTimeout;
    
    // Handle server output
    serverProcess.stdout.on('data', (data) => {
      const output = data.toString();
      log(output.trim(), 'cyan');
      
      // Check if server is ready
      if (output.includes('Server running on port') || output.includes('Listening on port')) {
        if (!serverReady) {
          serverReady = true;
          clearTimeout(startupTimeout);
          logSuccess(`Test server is ready on http://${HOST}:${PORT}`);
          resolve(serverProcess);
        }
      }
    });
    
    serverProcess.stderr.on('data', (data) => {
      const output = data.toString();
      // Only log errors that aren't expected startup messages
      if (!output.includes('Server running') && !output.includes('Listening on')) {
        logError(output.trim());
      }
    });
    
    // Handle server process events
    serverProcess.on('error', (error) => {
      logError(`Server process error: ${error.message}`);
      reject(error);
    });
    
    serverProcess.on('close', (code) => {
      if (code !== 0) {
        logError(`Server process exited with code ${code}`);
      } else {
        logSuccess('Server process closed normally');
      }
    });
    
    // Set startup timeout
    startupTimeout = setTimeout(() => {
      if (!serverReady) {
        logError('Server startup timeout - killing process');
        serverProcess.kill('SIGTERM');
        reject(new Error('Server startup timeout'));
      }
    }, 30000); // 30 seconds timeout
  });
}

// Graceful shutdown
function gracefulShutdown(serverProcess) {
  return new Promise((resolve) => {
    log('Shutting down test server...');
    
    const shutdownTimeout = setTimeout(() => {
      logWarning('Force killing server process');
      serverProcess.kill('SIGKILL');
      resolve();
    }, 5000); // 5 seconds grace period
    
    serverProcess.on('close', () => {
      clearTimeout(shutdownTimeout);
      logSuccess('Test server shutdown complete');
      resolve();
    });
    
    serverProcess.kill('SIGTERM');
  });
}

// Main execution
async function main() {
  try {
    // Check and build if necessary
    await checkBuild();
    
    // Start server
    const serverProcess = await startServer();
    
    // Handle process signals
    process.on('SIGINT', async () => {
      await gracefulShutdown(serverProcess);
      process.exit(0);
    });
    
    process.on('SIGTERM', async () => {
      await gracefulShutdown(serverProcess);
      process.exit(0);
    });
    
    // Keep the process alive
    process.stdin.resume();
    
  } catch (error) {
    logError(`Failed to start test server: ${error.message}`);
    process.exit(1);
  }
}

// Run if this script is executed directly
if (require.main === module) {
  main();
}

module.exports = {
  startServer,
  gracefulShutdown,
  checkBuild
}; 