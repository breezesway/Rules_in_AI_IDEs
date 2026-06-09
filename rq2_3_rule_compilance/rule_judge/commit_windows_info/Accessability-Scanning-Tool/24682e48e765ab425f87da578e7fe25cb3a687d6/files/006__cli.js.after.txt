#!/usr/bin/env node

const readline = require('readline');
const fs = require('fs');
const { spawn } = require('child_process');
const path = require('path');

// ANSI color codes for better CLI experience - Company Branded Colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  // Brand Colors
  brand_purple: '\x1b[38;2;30;33;77m',    // Key Purple #1e214d
  brand_magenta: '\x1b[38;2;219;0;100m',  // Magenta #db0064
  brand_yellow: '\x1b[38;2;252;199;0m',   // Yellow #fcc700
  // Standard colors (kept for compatibility)
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

class AccessibilityTestCLI {
  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });
    this.config = {};
  }

  // Utility methods
  log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
  }

  async question(prompt, color = 'brand_magenta') {
    return new Promise((resolve) => {
      this.rl.question(`${colors[color]}${prompt}${colors.reset}`, resolve);
    });
  }

  async validateUrl(url) {
    try {
      const urlObj = new URL(url);
      // Ensure it has http or https protocol
      if (urlObj.protocol !== 'http:' && urlObj.protocol !== 'https:') {
        return false;
      }
      return true;
    } catch {
      return false;
    }
  }

  // Main CLI interface
  async start() {
    console.clear();
    this.log('🌐 Accessibility Testing Tool', 'brand_magenta');
    this.log('=' .repeat(35), 'brand_magenta');
    this.log('');
    this.log('Professional WCAG 2.1 AA compliance testing for any website.');
    this.log('Generate comprehensive accessibility reports with actionable insights.');
    this.log('');

    const action = await this.selectAction();
    
    switch (action) {
      case '1':
        await this.runAccessibilityAudit();
        // Exit after audit completes instead of looping back
        this.log('👋 Goodbye!', 'green');
        this.rl.close();
        return;
      case '2':
        await this.cleanupReports();
        break;
      case '3':
      default:
        this.log('👋 Goodbye!', 'green');
        this.rl.close();
        return;
    }

    // Only show menu again if we didn't exit above (cleanup case)
    if (action === '2') {
      await this.start();
    }
  }

  async selectAction() {
    this.log('What would you like to do?', 'brand_magenta');
    this.log('');
    this.log('1. 🧪 Run Accessibility Audit');
    this.log('2. 🧹 Clean Up Reports');
    this.log('3. 🚪 Exit');
    this.log('');

    const choice = await this.question('Enter your choice (1-3): ');
    return choice.trim();
  }

  async runAccessibilityAudit() {
    try {
      this.log('\n🧪 Accessibility Audit', 'brand_magenta');
      this.log('=' .repeat(25), 'brand_magenta');

      // Get website URL
      let websiteUrl;
      let attempts = 0;
      const maxAttempts = 3;
      
      while (attempts < maxAttempts) {
        websiteUrl = await this.question('\n📄 Enter the website URL to test (or "back" to return): ');
        
        if (websiteUrl.toLowerCase() === 'back') {
          this.log('Returning to main menu...', 'brand_yellow');
          return;
        }
        
        if (await this.validateUrl(websiteUrl)) {
          break;
        }
        
        attempts++;
        this.log(`❌ Invalid URL. Please enter a valid URL (e.g., https://example.com)`, 'red');
        this.log(`💡 Attempts remaining: ${maxAttempts - attempts}`, 'brand_yellow');
      }
      
      if (attempts >= maxAttempts) {
        this.log('❌ Too many invalid attempts. Returning to main menu.', 'red');
        return;
      }

      // Set up default configuration for comprehensive audit
      this.config = {
        targetSiteUrl: websiteUrl,
        pageTimeout: 20000,
        delayBetweenRequests: 300,
        maxRetries: 3,
        maxPages: 50,
        maxDepth: 4,
        description: 'Full accessibility audit'
      };

      this.log(`\n✅ Configuration set for: ${websiteUrl}`, 'green');
      this.log('📊 Running comprehensive accessibility audit...', 'brand_yellow');

      await this.saveConfig();
      await this.runFullAudit();
      
      this.log('\n🎉 Audit process completed!', 'green');
      
    } catch (error) {
      this.log(`\n❌ Audit failed: ${error.message}`, 'red');
    }
  }

  async cleanupReports() {
    this.log('\n🧹 Clean Up Reports', 'brand_magenta');
    this.log('=' .repeat(20), 'brand_magenta');

    try {
      await this.runCommand('npm run clean:all');
      this.log('✅ All reports and cache cleared', 'green');
    } catch (error) {
      this.log(`❌ Cleanup failed: ${error.message}`, 'red');
    }
  }

  async runFullAudit() {
    this.log('\n🚀 Launching comprehensive audit...', 'green');
    this.log('💡 You can press Ctrl+C to stop the tests at any time', 'brand_yellow');

    try {
      await this.executeTest('1'); // '1' = Fresh full audit
      this.log('\n🎉 Accessibility audit completed successfully!', 'brand_magenta');
      this.log('📊 Check the accessibility-reports folder for your results.', 'brand_magenta');
      this.log('📄 Multiple audience-specific PDF reports have been generated:', 'brand_yellow');
      this.log('   📊 Product Owners & Stakeholders report', 'brand_yellow');
      this.log('   🔬 User Researchers & UCD report', 'brand_yellow');
      this.log('   💻 Developers & Testers report', 'brand_yellow');
      this.log('   📋 Detailed JSON report for further analysis', 'brand_yellow');
    } catch (error) {
      this.log(`\n❌ Test execution failed: ${error.message}`, 'red');
      throw error; // Re-throw to ensure proper error handling
    }
  }

  // Legacy method - keeping for compatibility but not used in simplified interface
  async quickStart() {
    this.log('\n🚀 Quick Start Configuration', 'brand_magenta');
    this.log('=' .repeat(30), 'brand_magenta');

    // Get website URL
    let websiteUrl;
    while (true) {
      websiteUrl = await this.question('\n📄 Enter the website URL to test: ');
      if (await this.validateUrl(websiteUrl)) {
        break;
      }
      this.log('❌ Invalid URL. Please enter a valid URL (e.g., https://example.com)', 'red');
    }

    // Select website type
    this.log('\n🏗️  What type of website is this?', 'brand_magenta');
    this.log('1. 📄 Static website (blogs, marketing sites)');
    this.log('2. 🏪 Business website (WordPress, CMS)');
    this.log('3. 💻 Web application (complex, interactive)');
    this.log('4. 🏢 Large enterprise site (100+ pages)');

    const typeChoice = await this.question('Select type (1-4): ');

    // Generate configuration based on type
    const presets = {
      '1': { // Static website
        pageTimeout: 10000,
        delayBetweenRequests: 200,
        maxRetries: 2,
        maxPages: 30,
        maxDepth: 3,
        description: 'Fast static website'
      },
      '2': { // Business website
        pageTimeout: 20000,
        delayBetweenRequests: 300,
        maxRetries: 3,
        maxPages: 50,
        maxDepth: 4,
        description: 'Business website'
      },
      '3': { // Web application
        pageTimeout: 30000,
        delayBetweenRequests: 500,
        maxRetries: 3,
        maxPages: 75,
        maxDepth: 4,
        description: 'Complex web application'
      },
      '4': { // Enterprise site
        pageTimeout: 45000,
        delayBetweenRequests: 400,
        maxRetries: 4,
        maxPages: 100,
        maxDepth: 5,
        description: 'Large enterprise site'
      }
    };

    const preset = presets[typeChoice] || presets['2'];
    
    this.config = {
      targetSiteUrl: websiteUrl,
      ...preset
    };

    this.log(`\n✅ Configuration created for: ${preset.description}`, 'green');
    this.showConfigSummary();

    const runNow = await this.question('\n🧪 Run accessibility tests now? (y/n): ');
    if (runNow.toLowerCase() === 'y' || runNow.toLowerCase() === 'yes') {
      await this.saveConfigAndRunQuickStart();
    } else {
      await this.saveConfig();
    }
  }

  async advancedConfiguration() {
    this.log('\n⚙️  Advanced Configuration', 'brand_magenta');
    this.log('=' .repeat(25), 'brand_magenta');

    // Website URL
    let websiteUrl;
    while (true) {
      websiteUrl = await this.question('\n📄 Website URL: ');
      if (await this.validateUrl(websiteUrl)) {
        break;
      }
      this.log('❌ Invalid URL format', 'red');
    }

    // Advanced options
    const maxPages = await this.askNumber('📊 Maximum pages to test', 50, 1, 1000);
    const maxDepth = await this.askNumber('🕳️  Maximum crawl depth', 4, 1, 10);
    const pageTimeout = await this.askNumber('⏱️  Page timeout (seconds)', 20, 5, 120) * 1000;
    const delayBetweenRequests = await this.askNumber('⏳ Delay between requests (ms)', 300, 100, 5000);
    const maxRetries = await this.askNumber('🔄 Max retries per page', 3, 1, 10);

    this.config = {
      targetSiteUrl: websiteUrl,
      maxPages,
      maxDepth,
      pageTimeout,
      delayBetweenRequests,
      maxRetries,
      retryDelay: 1500,
      description: 'Custom configuration'
    };

    this.log('\n✅ Advanced configuration completed', 'green');
    this.showConfigSummary();

    const save = await this.question('\n💾 Save and run tests? (y/n): ');
    if (save.toLowerCase() === 'y' || save.toLowerCase() === 'yes') {
      await this.saveConfigAndRun();
    }
  }

  async askNumber(prompt, defaultValue, min, max) {
    while (true) {
      const answer = await this.question(`${prompt} (${min}-${max}, default: ${defaultValue}): `);
      
      if (answer.trim() === '') {
        return defaultValue;
      }
      
      const num = parseInt(answer);
      if (!isNaN(num) && num >= min && num <= max) {
        return num;
      }
      
      this.log(`❌ Please enter a number between ${min} and ${max}`, 'red');
    }
  }

  showConfigSummary() {
    this.log('\n📋 Configuration Summary:', 'brand_magenta');
    this.log(`🌐 Website: ${this.config.targetSiteUrl}`, 'brand_magenta');
    this.log(`📊 Max Pages: ${this.config.maxPages}`, 'brand_yellow');
    this.log(`🕳️  Max Depth: ${this.config.maxDepth}`, 'brand_yellow');
    this.log(`⏱️  Timeout: ${this.config.pageTimeout / 1000}s`, 'brand_yellow');
    this.log(`⏳ Delay: ${this.config.delayBetweenRequests}ms`, 'brand_yellow');
    this.log(`🔄 Retries: ${this.config.maxRetries}`, 'brand_yellow');
  }

  async saveConfig() {
    const envContent = this.generateEnvContent();
    fs.writeFileSync('.env', envContent);
    this.log('\n💾 Configuration saved to .env file', 'green');
  }

  async saveConfigAndRun() {
    await this.saveConfig();
    await this.runTests();
  }

  async saveConfigAndRunQuickStart() {
    await this.saveConfig();
    await this.runQuickStartTests();
  }

  generateEnvContent() {
    return `# Accessibility Testing Configuration
# Generated by CLI tool on ${new Date().toISOString()}

TARGET_SITE_URL=${this.config.targetSiteUrl}
MAX_PAGES=${this.config.maxPages}
MAX_DEPTH=${this.config.maxDepth}
PAGE_TIMEOUT=${this.config.pageTimeout}
DELAY_BETWEEN_REQUESTS=${this.config.delayBetweenRequests}
MAX_RETRIES=${this.config.maxRetries}
RETRY_DELAY=${this.config.retryDelay || 1500}
FAIL_ON_CRITICAL_VIOLATIONS=true
MINIMUM_COMPLIANCE_THRESHOLD=80
`;
  }

  async runTests() {
    this.log('\n🧪 Starting Accessibility Tests...', 'brand_magenta');
    this.log('=' .repeat(35), 'brand_magenta');

    // Check if config exists
    if (!fs.existsSync('.env') && Object.keys(this.config).length === 0) {
      this.log('❌ No configuration found. Please run configuration first.', 'red');
      return;
    }

    const testType = await this.selectTestType();
    
    this.log('\n🚀 Launching tests...', 'green');
          this.log('💡 You can press Ctrl+C to stop the tests at any time', 'brand_yellow');

    try {
      await this.executeTest(testType);
    } catch (error) {
      this.log(`\n❌ Test execution failed: ${error.message}`, 'red');
    }
  }

  async runQuickStartTests() {
    this.log('\n🧪 Starting Fresh Full Audit (Quick Start)...', 'brand_magenta');
    this.log('=' .repeat(45), 'brand_magenta');

    // Check if config exists
    if (!fs.existsSync('.env') && Object.keys(this.config).length === 0) {
      this.log('❌ No configuration found. Please run configuration first.', 'red');
      return;
    }

    this.log('\n🚀 Launching fresh full audit...', 'green');
    this.log('💡 You can press Ctrl+C to stop the tests at any time', 'brand_yellow');

    try {
      await this.executeTest('1'); // '1' = Fresh full audit
      this.log('\n🎉 Quick Start completed successfully!', 'brand_magenta');
      this.log('📊 Check the accessibility-reports folder for your results.', 'brand_magenta');
    } catch (error) {
      this.log(`\n❌ Test execution failed: ${error.message}`, 'red');
    }
  }

  async selectTestType() {
    this.log('\n🧪 Select test type:', 'brand_magenta');
    this.log('1. 🧹 Fresh full audit (recommended)');
    this.log('2. 🕷️  Pre-crawl only (discover pages)');
    this.log('3. 🔍 Debug mode (detailed logging)');

    const choice = await this.question('Select test type (1-3): ');
    return choice.trim();
  }

  async executeTest(testType) {
    const commands = {
      '1': 'npm run audit:fresh',
      '2': 'npm run audit:pre-crawl', 
      '3': 'npm run audit:debug'
    };

    const command = commands[testType] || commands['1'];
    
    // Pause the readline interface during command execution
    this.rl.pause();
    
    return new Promise((resolve, reject) => {
      const childProcess = spawn('npm', command.split(' ').slice(1), {
        stdio: 'inherit',
        env: { ...process.env, ...this.parseEnvFile() },
        shell: true
      });

      childProcess.on('close', (code) => {
        // Resume the readline interface after command completion
        this.rl.resume();
        
        if (code === 0) {
          this.log('\n✅ Tests completed successfully!', 'green');
          resolve();
        } else {
          reject(new Error(`Tests failed with exit code ${code}`));
        }
      });

      childProcess.on('error', (error) => {
        // Resume the readline interface on error
        this.rl.resume();
        reject(error);
      });
    });
  }

  parseEnvFile() {
    if (!fs.existsSync('.env')) return {};
    
    const content = fs.readFileSync('.env', 'utf8');
    const env = {};
    
    content.split('\n').forEach(line => {
      const [key, value] = line.split('=');
      if (key && value && !key.startsWith('#')) {
        env[key.trim()] = value.trim();
      }
    });
    
    return env;
  }

  async showStatus() {
    this.log('\n📊 System Status', 'brand_magenta');
    this.log('=' .repeat(15), 'brand_magenta');

    // Check configuration
    if (fs.existsSync('.env')) {
      this.log('✅ Configuration file exists', 'green');
      const env = this.parseEnvFile();
      if (env.TARGET_SITE_URL) {
        this.log(`🌐 Target site: ${env.TARGET_SITE_URL}`, 'brand_magenta');
      }
    } else {
      this.log('❌ No configuration found', 'red');
    }

    // Check for reports
    const reportsDir = path.join(process.cwd(), 'playwright', 'accessibility-reports');
    if (fs.existsSync(reportsDir)) {
      const files = fs.readdirSync(reportsDir, { recursive: true }).filter(f => f.endsWith('.json'));
      this.log(`📄 Found ${files.length} report files`, 'brand_yellow');
    }

    // Check running processes
          this.log('\n🔍 Checking for running browser processes...', 'brand_yellow');
    try {
      const { exec } = require('child_process');
      exec('ps aux | grep -E "(chrome|chromium|playwright)" | grep -v grep', (error, stdout) => {
        if (stdout.trim()) {
          this.log('⚠️  Found running browser processes:', 'brand_yellow');
          console.log(stdout);
        } else {
          this.log('✅ No browser processes running', 'green');
        }
      });
    } catch (error) {
              this.log('ℹ️  Could not check processes', 'brand_yellow');
    }

    await this.question('\nPress Enter to continue...');
  }

  async cleanup() {
    this.log('\n🧹 Cleanup & Reset', 'brand_magenta');
    this.log('=' .repeat(17), 'brand_magenta');

    this.log('\nWhat would you like to clean up?');
    this.log('1. 🗑️  Clear all reports and cache');
    this.log('2. 🔄 Kill hanging browser processes');
    this.log('3. 📝 Reset configuration');
    this.log('4. 🧽 Full cleanup (all of the above)');

    const choice = await this.question('Select cleanup option (1-4): ');

    try {
      switch (choice) {
        case '1':
          await this.runCommand('npm run clean:all');
          this.log('✅ Reports and cache cleared', 'green');
          break;
        case '2':
          await this.runCommand('npm run clean:browsers');
          this.log('✅ Browser processes cleaned', 'green');
          break;
        case '3':
          if (fs.existsSync('.env')) {
            fs.unlinkSync('.env');
            this.log('✅ Configuration reset', 'green');
          } else {
            this.log('ℹ️  No configuration to reset', 'brand_yellow');
          }
          break;
        case '4':
          await this.runCommand('npm run system:cleanup');
          if (fs.existsSync('.env')) {
            fs.unlinkSync('.env');
          }
          this.log('✅ Full cleanup completed', 'green');
          break;
        default:
          this.log('❌ Invalid choice', 'red');
      }
    } catch (error) {
      this.log(`❌ Cleanup failed: ${error.message}`, 'red');
    }

    await this.question('\nPress Enter to continue...');
  }

  async runCommand(command) {
    return new Promise((resolve, reject) => {
      const process = spawn('npm', command.split(' ').slice(1), {
        stdio: 'inherit'
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Command failed with exit code ${code}`));
        }
      });

      process.on('error', reject);
    });
  }

  close() {
    this.rl.close();
  }
}

// Handle CLI arguments
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
🌐 Accessibility Testing CLI Tool

Usage:
  node cli.js              Interactive mode
  node cli.js --help      Show this help
  node cli.js --version   Show version

Interactive Commands:
  🚀 Quick Start          - Easy setup for common website types
  ⚙️  Advanced Config     - Detailed configuration options  
  🧪 Run Tests           - Execute accessibility tests
  📊 Show Status         - Check system and configuration status
  🧹 Cleanup             - Clean up reports, processes, and config

Examples:
  node cli.js             # Start interactive mode
  npm run cli             # Alternative way to start
`);
  process.exit(0);
}

if (args.includes('--version') || args.includes('-v')) {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  console.log(`Accessibility Testing Tool v${packageJson.version}`);
  process.exit(0);
}

// Start CLI
const cli = new AccessibilityTestCLI();

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Goodbye!');
  cli.close();
  process.exit(0);
});

process.on('SIGTERM', () => {
  cli.close();
  process.exit(0);
});

// Start the CLI
cli.start().catch((error) => {
  console.error('CLI Error:', error);
  cli.close();
  process.exit(1);
}); 