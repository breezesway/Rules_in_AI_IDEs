import { Page, test, expect } from '@playwright/test';
import { AccessibilityTestUtils } from './utils/accessibility-helpers';

test.describe('Pre-Crawl Health Check', (): void => {
  let accessibilityTestUtils: AccessibilityTestUtils;

  test.beforeEach(async ({ page }: { page: Page }): Promise<void> => {
    accessibilityTestUtils = new AccessibilityTestUtils(page);
  });

  test('should have a valid sitemap', async ({ page }: { page: Page }): Promise<void> => {
    const sitemapUrl = new URL('sitemap.xml', page.url()).toString();
    const response = await page.goto(sitemapUrl, { waitUntil: 'domcontentloaded' });
    expect(response?.status()).toBe(200);
  });

  test('should have a valid robots.txt', async ({ page }: { page: Page }): Promise<void> => {
    const robotsUrl = new URL('robots.txt', page.url()).toString();
    const response = await page.goto(robotsUrl, { waitUntil: 'domcontentloaded' });
    expect(response?.status()).toBe(200);
  });

  test('should have a main landmark', async ({ page }: { page: Page }): Promise<void> => {
    await accessibilityTestUtils.checkLandmarks(page);
  });

  test('should have a descriptive page title', async ({ page }: { page: Page }): Promise<void> => {
    await accessibilityTestUtils.checkPageTitle(page);
  });

  test('should have no broken links', async ({ page }: { page: Page }): Promise<void> => {
    await accessibilityTestUtils.checkBrokenLinks(page);
  });
});
