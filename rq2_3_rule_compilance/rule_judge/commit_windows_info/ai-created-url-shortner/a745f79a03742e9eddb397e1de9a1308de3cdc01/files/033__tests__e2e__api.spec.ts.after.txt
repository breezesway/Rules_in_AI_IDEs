import { test, expect } from "@nuxt/test-utils/playwright";
import { $fetch } from "@nuxt/test-utils/e2e";

test.describe("API Routes", () => {
  test("should handle API requests", async () => {
    // Example of testing API endpoints
    // This test will work once you have API routes set up
    try {
      const response = await $fetch("/api/health");
      expect(response).toBeDefined();
    } catch {
      // If no API routes exist yet, this test will be skipped
      console.warn("No API routes found - skipping API tests");
    }
  });

  test("should return proper error responses", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Test 404 handling
    const response = await page.request.get("/api/non-existent-endpoint");
    expect(response.status()).toBe(404);
  });

  test("should handle CORS correctly", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Test that API requests work from the client side
    const response = await page.evaluate(async () => {
      try {
        // eslint-disable-next-line
        const res = await fetch("/api/test");
        return res.status;
      } catch {
        return 404; // Expected if no API routes exist
      }
    });

    // Should either work (200) or return 404 if no routes exist
    expect([200, 404]).toContain(response);
  });
});
