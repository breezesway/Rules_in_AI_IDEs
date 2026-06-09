import { expect, test } from "@nuxt/test-utils/playwright";

test.describe("Homepage", () => {
  test("displays the homepage correctly", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Check that the page loads and displays the expected content
    await expect(
      page.getByRole("heading", { name: "Hello World" })
    ).toBeVisible();

    // Check that the page title is set correctly
    await expect(page).toHaveTitle(/home/i);
  });

  test("navigates to playground page", async ({ page, goto }) => {
    await goto("/", { waitUntil: "hydration" });

    // Navigate to playground if there's a link
    if ((await page.locator('a[href="/playground"]').count()) > 0) {
      await page.click('a[href="/playground"]');
      await expect(page).toHaveURL(/.*playground.*/);
    }
  });

  test("page is responsive", async ({ page, goto }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await goto("/", { waitUntil: "hydration" });

    await expect(
      page.getByRole("heading", { name: "Hello World" })
    ).toBeVisible();

    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(
      page.getByRole("heading", { name: "Hello World" })
    ).toBeVisible();
  });
});
