#!/usr/bin/env node

/**
 * Environment File Validation Script
 * 
 * This script validates that an existing .env.local file contains
 * the correct details and is properly formatted for local development.
 */

const fs = require('fs');
const path = require('path');

function log(message, type = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = type === 'error' ? '❌' : type === 'success' ? '✅' : type === 'warning' ? '⚠️' : 'ℹ️';
    console.log(`${prefix} [${timestamp}] ${message}`);
}

function validateEnvFile(envFilePath = '.env.local') {
    log('Validating environment file...');
    
    const fullPath = path.resolve(envFilePath);
    
    // Check if file exists
    if (!fs.existsSync(fullPath)) {
        log(`Environment file not found: ${envFilePath}`, 'error');
        return { isValid: false, issues: [`File not found: ${envFilePath}`] };
    }
    
    const issues = [];
    const warnings = [];
    const content = fs.readFileSync(fullPath, 'utf8');
    const lines = content.split('\n');
    
    // Required variables for local MongoDB development
    const requiredVars = {
        'MONGODB_URL': {
            required: true,
            pattern: /^mongodb:\/\/[^@]+@localhost:\d+\/?\?authSource=admin$/,
            description: 'MongoDB connection URL with authentication (e.g., mongodb://admin:password123@localhost:27017/?authSource=admin)'
        },
        'MONGODB_DB_NAME': {
            required: true,
            pattern: /^[a-zA-Z0-9_]+$/,
            description: 'MongoDB database name'
        },
        'NODE_ENV': {
            required: true,
            pattern: /^(development|production|test)$/,
            description: 'Node environment'
        },
        'PORT': {
            required: true,
            pattern: /^\d+$/,
            description: 'Application port number'
        }
    };
    
    // Optional variables for MongoDB development
    const optionalVars = {
        'NODE_ENV': {
            pattern: /^(development|production|test)$/,
            description: 'Node environment'
        },
        'PORT': {
            pattern: /^\d+$/,
            description: 'Application port number'
        }
    };
    
    const foundVars = {};
    
    // Parse the file
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        // Skip empty lines and comments
        if (!line || line.startsWith('#')) {
            continue;
        }
        
        // Check for valid variable assignment
        if (line.includes('=')) {
            const [key, ...valueParts] = line.split('=');
            const value = valueParts.join('='); // Handle values that might contain '='
            
            if (key && value !== undefined) {
                foundVars[key.trim()] = value.trim();
            } else {
                issues.push(`Invalid variable assignment on line ${i + 1}: ${line}`);
            }
        } else {
            issues.push(`Invalid line format on line ${i + 1}: ${line}`);
        }
    }
    
    // Validate required variables
    for (const [varName, config] of Object.entries(requiredVars)) {
        if (!foundVars[varName]) {
            if (config.required) {
                issues.push(`Missing required variable: ${varName} - ${config.description}`);
            }
        } else {
            // Check pattern if specified
            if (config.pattern && !config.pattern.test(foundVars[varName])) {
                issues.push(`Invalid value for ${varName}: "${foundVars[varName]}" - ${config.description}`);
            }
        }
    }
    
    // Validate optional variables (if present)
    for (const [varName, config] of Object.entries(optionalVars)) {
        if (foundVars[varName]) {
            if (config.pattern && !config.pattern.test(foundVars[varName])) {
                warnings.push(`Invalid value for ${varName}: "${foundVars[varName]}" - ${config.description}`);
            }
        }
    }
    
    // Check for duplicate variables
    const duplicates = Object.keys(foundVars).filter((key, index, arr) => arr.indexOf(key) !== index);
    if (duplicates.length > 0) {
        issues.push(`Duplicate variables found: ${duplicates.join(', ')}`);
    }
    
    // Check for unknown variables
    const allKnownVars = { ...requiredVars, ...optionalVars };
    const unknownVars = Object.keys(foundVars).filter(key => !allKnownVars[key]);
    if (unknownVars.length > 0) {
        warnings.push(`Unknown variables found: ${unknownVars.join(', ')}`);
    }
    
    // Validate database URL consistency
    if (foundVars['DATABASE_URL'] && foundVars['POSTGRES_PASSWORD']) {
        const dbUrl = foundVars['DATABASE_URL'];
        const password = foundVars['POSTGRES_PASSWORD'];
        
        if (!dbUrl.includes(password)) {
            issues.push('DATABASE_URL password does not match POSTGRES_PASSWORD');
        }
    }
    
    // Validate MongoDB URL consistency
    if (foundVars['MONGODB_URL']) {
        const mongoUrl = foundVars['MONGODB_URL'];
        
        // Check if MongoDB URL includes authentication
        if (!mongoUrl.includes('authSource=admin')) {
            warnings.push(`MongoDB URL should include authSource=admin parameter for proper authentication`);
        }
        
        // Check if MongoDB URL includes credentials
        if (!mongoUrl.includes('@localhost')) {
            warnings.push(`MongoDB URL should include authentication credentials (username:password@localhost)`);
        }
    }
    
    const isValid = issues.length === 0;
    
    // Report results
    if (isValid) {
        log('Environment file validation passed!', 'success');
        log(`Found ${Object.keys(foundVars).length} variables`, 'info');
        
        if (warnings.length > 0) {
            log('Warnings found:', 'warning');
            warnings.forEach(warning => log(`  ${warning}`, 'warning'));
        }
    } else {
        log('Environment file validation failed!', 'error');
        log('Issues found:', 'error');
        issues.forEach(issue => log(`  ${issue}`, 'error'));
        
        if (warnings.length > 0) {
            log('Warnings found:', 'warning');
            warnings.forEach(warning => log(`  ${warning}`, 'warning'));
        }
    }
    
    return {
        isValid,
        issues,
        warnings,
        variables: foundVars,
        totalVariables: Object.keys(foundVars).length
    };
}

function suggestFix(validationResult) {
    if (validationResult.isValid) {
        log('No fixes needed - environment file is valid!', 'success');
        return;
    }
    
    log('Suggested fixes:', 'info');
    
    if (validationResult.issues.includes('File not found')) {
        log('1. Generate a new environment file: npm run secrets:generate', 'info');
        return;
    }
    
    const missingVars = validationResult.issues
        .filter(issue => issue.includes('Missing required variable'))
        .map(issue => issue.split(': ')[1]);
    
    if (missingVars.length > 0) {
        log('1. Missing required variables detected', 'info');
        log('   Run: npm run secrets:generate', 'info');
    }
    
    const placeholderIssues = validationResult.issues
        .filter(issue => issue.includes('should not be placeholder'));
    
    if (placeholderIssues.length > 0) {
        log('2. Placeholder values detected', 'info');
        log('   Run: npm run secrets:generate', 'info');
    }
    
    const formatIssues = validationResult.issues
        .filter(issue => issue.includes('Invalid line format') || issue.includes('Invalid variable assignment'));
    
    if (formatIssues.length > 0) {
        log('3. Format issues detected', 'info');
        log('   Check the .env.local file for syntax errors', 'info');
        log('   Each line should be: VARIABLE_NAME=value', 'info');
    }
    
    log('4. After fixing, run validation again: npm run validate:env', 'info');
}

function main() {
    const command = process.argv[2];
    const envFile = process.argv[3] || '.env.local';
    
    switch (command) {
        case 'validate':
        case undefined:
            const result = validateEnvFile(envFile);
            suggestFix(result);
            process.exit(result.isValid ? 0 : 1);
            break;
            
        case 'help':
            console.log(`
Environment File Validation Script

Usage: node scripts/validate-env.js [command] [env-file]

Commands:
  validate  - Validate the environment file (default)
  help      - Show this help message

Arguments:
  env-file  - Path to environment file (default: .env.local)

Examples:
  node scripts/validate-env.js validate
  node scripts/validate-env.js validate .env.production
  node scripts/validate-env.js help

This script will:
1. Check if the environment file exists
2. Validate required variables are present
3. Check for placeholder values
4. Validate variable formats and patterns
5. Check for consistency between related variables
6. Suggest fixes for any issues found

Required variables for local development:
- MONGODB_URL
- MONGODB_DB_NAME
- NODE_ENV
- PORT
            `);
            break;
            
        default:
            log(`Unknown command: ${command}`, 'error');
            log('Run "node scripts/validate-env.js help" for usage information', 'info');
            process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { validateEnvFile, suggestFix }; 