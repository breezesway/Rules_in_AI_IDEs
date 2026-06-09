#!/usr/bin/env npx ts-node

import { spawn } from 'child_process';
import * as path from 'path';

// ANSI color codes for better CLI experience - Company Branded Colors
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  // Brand Colors
  brand_purple: '\x1b[38;2;30;33;77m', // Key Purple #1e214d
  brand_magenta: '\x1b[38;2;219;0;100m', // Magenta #db0064
  brand_yellow: '\x1b[38;2;252;199;0m', // Yellow #fcc700
  // Standard colors (kept for compatibility)
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
} as const;

type ColorKey = keyof typeof colors;

function log(message: string, color: ColorKey = 'reset'): void {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

async function main(): Promise<void> {
  console.clear();
  log('🚀 Accessibility Testing Tool - Phase 2 Architecture', 'brand_magenta');
  log('='.repeat(55), 'brand_magenta');
  log('');
  log('⚡ This tool has been upgraded to Phase 2 architecture!', 'brand_yellow');
  log('');
  log('🔧 New Features:', 'brand_purple');
  log('  • Queue-based processing with auto-scaling worker pools');
  log('  • Intelligent caching with compression and TTL');
  log('  • Enhanced performance monitoring and real-time metrics');
  log('  • Service-based architecture for better scalability');
  log('  • Improved PDF report generation with brand compliance');
  log('');
  log('📄 Starting the new Phase 2 CLI...', 'green');
  log('');

  // Launch the new Phase 2 CLI
  const newCliPath = path.join(process.cwd(), 'src', 'cli', 'accessibility-test-cli.ts');

  try {
    const child = spawn('npx', ['ts-node', newCliPath], {
      stdio: 'inherit',
      env: process.env,
    });

    child.on('close', code => {
      if (code !== 0) {
        log(`❌ Phase 2 CLI exited with code ${code}`, 'red');
        process.exit(code || 1);
      }
    });

    child.on('error', error => {
      log(`❌ Failed to start Phase 2 CLI: ${error.message}`, 'red');
      log('');
      log('🔧 Manual startup instructions:', 'brand_yellow');
      log(`   npx ts-node ${newCliPath}`, 'cyan');
      log('');
      log('💡 Or use the package.json scripts:', 'brand_yellow');
      log('   npm run cli', 'cyan');
      log('   npm run test:accessibility', 'cyan');
      log('');
      process.exit(1);
    });
  } catch (error) {
    log(`❌ Error launching Phase 2 CLI: ${(error as Error).message}`, 'red');
    process.exit(1);
  }
}

// If this file is run directly, execute the main function
if (require.main === module) {
  main().catch(error => {
    log(`❌ Unexpected error: ${error.message}`, 'red');
    process.exit(1);
  });
}

export default main;
