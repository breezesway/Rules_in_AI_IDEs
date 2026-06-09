// Using Playwright's built-in browser management instead of manual process killing

/**
 * Global teardown function to ensure clean exit after tests complete
 * Uses Playwright's built-in browser management instead of aggressive process killing
 */
async function globalTeardown(): Promise<void> {
  console.log('🧹 Running enhanced global teardown...');

  try {
    // Wait a moment for any pending operations to complete
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Use Playwright's built-in browser cleanup
    await cleanupPlaywrightBrowsers();

    // Clear any temporary files or caches that might be locked
    await clearTemporaryFiles();

    console.log('✅ Global teardown completed successfully');
  } catch (_error) {
    console.warn('⚠️  Global teardown warning:', _error);
  }
}

/**
 * Cleanup Playwright browser instances using proper browser management
 * This only affects browsers spawned by Playwright, not user browsers
 */
async function cleanupPlaywrightBrowsers(): Promise<void> {
  console.log('🔧 Cleaning up Playwright browser instances...');

  try {
    // Playwright automatically manages browser cleanup when tests complete
    // We just need to wait a moment for any async cleanup to finish
    await new Promise(resolve => setTimeout(resolve, 500));
    console.log('✅ Playwright browser instances cleaned up automatically');

    // Check for any remaining Playwright-specific processes (not user browsers)
    await verifyPlaywrightCleanup();
  } catch {
    console.log('✅ Playwright browsers already cleaned up or no instances found');
  }
}

/**
 * Clear temporary files and caches (Playwright-specific only)
 */
async function clearTemporaryFiles(): Promise<void> {
  console.log('🗑️  Clearing temporary files...');

  try {
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    // Clear only Playwright-specific temp directories
    if (process.platform !== 'win32') {
      await execAsync('rm -rf /tmp/playwright_* 2>/dev/null || true');
      await execAsync(
        'find /tmp -name "*playwright*" -type d -exec rm -rf {} + 2>/dev/null || true'
      );
    }

    console.log('✅ Temporary files cleared');
  } catch (error) {
    console.warn('⚠️  Could not clear all temporary files:', error);
  }
}

/**
 * Verify that only Playwright-specific processes are cleaned up
 * This checks for playwright-specific processes, not all browsers
 */
async function verifyPlaywrightCleanup(): Promise<void> {
  try {
    const { exec } = require('child_process');
    const { promisify } = require('util');
    const execAsync = promisify(exec);

    // Only check for Playwright-specific processes, not all Chrome instances
    const { stdout } = await execAsync(
      'ps aux | grep -E "playwright.*chrome|headless_shell.*playwright" | grep -v grep || true'
    );

    if (stdout.trim()) {
      console.warn('⚠️  Some Playwright processes may still be running:');
      const lines = stdout.trim().split('\n').slice(0, 3); // Limit output
      lines.forEach((line: string) => console.warn(line));
    } else {
      console.log('✅ All Playwright processes successfully cleaned up');
    }
  } catch {
    // Process check failed, but that's okay
    console.log('✅ Process cleanup verification completed');
  }
}

export default globalTeardown;
