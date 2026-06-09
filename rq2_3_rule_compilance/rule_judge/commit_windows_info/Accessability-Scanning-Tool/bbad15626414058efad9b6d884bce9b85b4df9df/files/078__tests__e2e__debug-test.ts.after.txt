import { test, expect } from '@playwright/test';

test('Debug page content', async ({ page }) => {
    // Navigate to the page
    await page.goto('http://localhost:3000');

    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Check if the element exists
    const fullSiteUrlExists = await page.locator('#fullSiteUrl').count();
    console.log('fullSiteUrl elements found:', fullSiteUrlExists);

    // Get page content
    const pageContent = await page.content();
    console.log('Page title:', await page.title());

    // Check if the element is in the HTML
    if (pageContent.includes('fullSiteUrl')) {
        console.log('fullSiteUrl found in page content');
    } else {
        console.log('fullSiteUrl NOT found in page content');
    }

    // Take a screenshot
    await page.screenshot({ path: 'debug-screenshot.png' });
}); 