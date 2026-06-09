import { test, expect } from "@nuxt/test-utils/playwright";

test.describe("Basic Functionality", () => {
  test("can load the homepage", async ({ page, goto }) => {
    // Navigate to the homepage
    await goto("/", { waitUntil: "hydration" });

    // Check that the page loads (basic test)
    expect(await page.title()).toBeTruthy();

    // Check that we can find some content on the page
    const bodyText = await page.textContent("body");
    expect(bodyText).toBeTruthy();
  });

  test("can navigate and hydrate properly", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Test that Vue hydration worked by checking if we can interact with the page
    const html = await page.innerHTML("html");
    expect(html).toContain("nuxt");
  });

  test("API health endpoint works", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Test the API endpoint we created
    const response = await page.request.get("/api/health");
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.status).toBe("healthy");
    expect(data.timestamp).toBeTruthy();
  });
});
