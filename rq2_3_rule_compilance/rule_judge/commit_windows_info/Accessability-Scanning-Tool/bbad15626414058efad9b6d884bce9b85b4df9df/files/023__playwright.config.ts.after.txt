import { defineConfig, devices } from '@playwright/test';

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: './tests/e2e',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 1,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 4 : 4,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [['html', { open: 'never' }], ['list']],

  // E2E test timeout settings
  timeout: 20_000, // 20 seconds per test
  expect: {
    // Default timeout for assertions
    timeout: 10_000, // 10 seconds
  },

  /* Global timeout for entire test run */
  globalTimeout: 600_000, // 10 minutes for entire test suite

  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:3000',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    // E2E testing settings
    headless: true,

    // Navigation timeout for E2E tests
    navigationTimeout: 30_000, // 30 seconds

    // Action timeout
    actionTimeout: 10_000, // 10 seconds

    // Disable resource-heavy features for better performance
    video: 'off',
    screenshot: 'only-on-failure',

    // E2E testing optimisations
    ignoreHTTPSErrors: true,

  },

  /* Configure projects for multiple browsers */
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        headless: true,
        viewport: { width: 1280, height: 720 },
      },
    },
    // {
    //   name: 'firefox',
    //   use: {
    //     ...devices['Desktop Firefox'],
    //     headless: true,
    //     viewport: { width: 1280, height: 720 },
    //   },
    // },
    // {
    //   name: 'webkit',
    //   use: {
    //     ...devices['Desktop Safari'],
    //     headless: true,
    //     viewport: { width: 1280, height: 720 },
    //   },
    // },
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    command: 'node scripts/check-dev-server.js',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 180_000, // 3 minutes to start server (includes MongoDB startup)
  },
});
