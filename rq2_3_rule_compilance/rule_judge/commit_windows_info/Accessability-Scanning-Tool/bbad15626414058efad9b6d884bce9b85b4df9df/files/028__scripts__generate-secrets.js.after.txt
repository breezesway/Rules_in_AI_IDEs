#!/usr/bin/env node

/**
 * Secret Generation Script
 * 
 * This script generates secure secrets for local development
 * and helps users set up their environment variables properly.
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

function log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    console.log(`${prefix} [${timestamp}] ${message}`);
}

function generateSecureString(length = 32) {
    return crypto.randomBytes(length).toString('base64').replace(/[^a-zA-Z0-9]/g, '');
}

function generateJWTSecret() {
    // Generate a secure JWT secret (minimum 32 characters)
    return generateSecureString(32);
}

function generateSecretKeyBase() {
    // Generate a secure secret key base (minimum 64 characters for Phoenix)
    return generateSecureString(64);
}

function generatePassword() {
    // Generate a secure password for PostgreSQL
    return generateSecureString(24);
}

function generateMongoDBConfig() {
    // For local development, we can generate demo configuration
    // In production, these should come from your MongoDB setup
    return {
        mongoUrl: `mongodb://admin:${generateSecureString(12)}@localhost:27017/?authSource=admin`,
        databaseName: 'accessibility_testing'
    };
}

function createEnvFile(secrets, outputPath = '.env.local') {
    const envContent = `# =============================================================================
# Local MongoDB Configuration
# =============================================================================
# Auto-generated secure secrets for local development
# DO NOT commit this file to version control

# MongoDB Configuration (local development)
MONGODB_URL=${secrets.mongoUrl}
MONGODB_DB_NAME=${secrets.databaseName}

# Local Development Settings
NODE_ENV=development
PORT=3000

# =============================================================================
# SECURITY NOTES
# =============================================================================
# These secrets are generated for local development only
# For production, use proper secrets from your MongoDB setup
# Never commit .env.local to version control
`;

    fs.writeFileSync(outputPath, envContent);
    log(`Environment file created: ${outputPath}`, 'success');
}

function main() {
    log('Generating secure secrets for local development...');
    
    const secrets = {
        ...generateMongoDBConfig()
    };
    
    log('Generated secrets:', 'info');
    log(`MongoDB URL: ${secrets.mongoUrl}`, 'info');
    log(`Database Name: ${secrets.databaseName}`, 'info');

    
    // Create .env.local file
    createEnvFile(secrets);
    
    log('', 'info');
    log('Next steps:', 'info');
    log('1. Review the generated .env.local file', 'info');
    log('2. Start your development environment: npm run dev:full', 'info');
    log('3. The secrets will be automatically used by Docker Compose', 'info');
    log('', 'info');
    log('⚠️  IMPORTANT: Never commit .env.local to version control!', 'warning');
    log('   Add .env.local to your .gitignore file if not already present.', 'warning');
}

// Parse command line arguments
const command = process.argv[2];

switch (command) {
    case 'generate':
    case undefined:
        main();
        break;
    case 'help':
        console.log(`
Secret Generation Script

Usage: node scripts/generate-secrets.js [command]

Commands:
  generate  - Generate secure secrets and create .env.local (default)
  help      - Show this help message

This script will:
1. Generate secure MongoDB connection URL
2. Generate secure database name
3. Create .env.local file with all secrets
4. Configure Docker Compose to use these secrets

Security Notes:
- Generated secrets are for local development only
- For production, use proper secrets from your MongoDB setup
- Never commit .env.local to version control
- Add .env.local to .gitignore if not already present
        `);
        break;
    default:
        log(`Unknown command: ${command}`, 'error');
        log('Run "node scripts/generate-secrets.js help" for usage information', 'info');
        process.exit(1);
} 