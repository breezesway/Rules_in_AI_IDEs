import { defineVitestConfig } from "@nuxt/test-utils/config";

export default defineVitestConfig({
  test: {
    environment: "nuxt",
    // Enable globals for cleanup
    globals: true,
    // Include patterns for co-located tests
    include: [
      "**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
      "**/*.nuxt.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
      "**/tests/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}",
    ],
    // Exclude e2e tests and other non-test files
    exclude: [
      "**/tests/e2e/**",
      "**/node_modules/**",
      "**/dist/**",
      "**/.nuxt/**",
      "**/coverage/**",
      "**/cypress/**",
      "**/.nyc_output/**",
      "**/playwright-report/**",
      "**/test-results/**",
    ],
    // Environment options for Nuxt testing
    environmentOptions: {
      nuxt: {
        domEnvironment: "happy-dom",
        mock: {
          intersectionObserver: true,
          indexedDb: true,
        },
      },
    },
  },
});
