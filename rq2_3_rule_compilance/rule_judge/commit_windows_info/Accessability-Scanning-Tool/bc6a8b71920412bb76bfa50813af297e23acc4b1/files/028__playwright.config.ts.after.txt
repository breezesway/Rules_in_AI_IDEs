import { defineConfig, devices } from '@playwright/test';

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './playwright/tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [['html', { open: 'never' }]],

  // Universal timeout settings optimised for any website
  timeout: 900_000, // 15 minutes per test (increased back for large sites)
  expect: {
    // Default timeout for assertions
    timeout: 30_000, // 30 seconds
  },

  /* Global timeout for entire test run - scales with site size */
  globalTimeout: 3_600_000, // 1 hour for entire test suite (restored for large sites)



  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    // baseURL: 'http://localhost:3000',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    // Universal browser settings optimised for any website
    headless: true,

    // Universal navigation timeout - will be overridden by adaptive logic
    navigationTimeout: 45_000, // 45 seconds (increased for slower sites)

    // Universal action timeout
    actionTimeout: 30_000, // 30 seconds (increased for complex interactions)

    // Disable resource-heavy features for better performance
    video: 'off',
    screenshot: 'off',

    // Universal optimisation for any website
    ignoreHTTPSErrors: true,

    // Universal Chrome optimisation flags (a11y-safe)
    launchOptions: {
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-extensions',
        '--disable-default-apps',
        '--disable-sync',
        '--disable-background-timer-throttling',
        '--disable-backgrounding-occluded-windows',
        '--disable-renderer-backgrounding',
        '--disable-ipc-flooding-protection',
        '--memory-pressure-off',
        '--max_old_space_size=4096',
        '--enable-automation',
        '--disable-blink-features=AutomationControlled',
        '--disable-background-networking',
        '--disable-component-update',
        '--disable-domain-reliability',
        '--disable-hang-monitor',
        '--disable-prompt-on-repost',
        '--metrics-recording-only',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
        '--use-mock-keychain',
      ],
    },
  },

  /* Configure projects for Chrome only (universal optimisation) */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Universal settings for any website
        headless: true,
        viewport: { width: 1280, height: 720 },
        // Universal Chrome-specific optimisations (a11y-safe)
        launchOptions: {
          args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-extensions',
            '--disable-default-apps',
            '--disable-sync',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-ipc-flooding-protection',
            '--memory-pressure-off',
            '--max_old_space_size=4096',
            '--enable-automation',
            '--disable-blink-features=AutomationControlled',
            '--disable-background-networking',
            '--disable-component-update',
            '--disable-domain-reliability',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--use-mock-keychain',
          ],
        },
      },
    },
  ],

  /* Run your local dev server before starting the tests */
  // webServer: {
  //   command: 'npm run start',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
