# Page Object Model (POM) Implementation

This document describes the Page Object Model (POM) implementation for the E2E tests in the accessibility testing application.

## Overview

The Page Object Model is a design pattern that creates an object repository for storing web elements. This pattern helps to:

- **Reduce code duplication**: Common selectors and actions are centralized
- **Improve maintainability**: UI changes only require updates in page objects
- **Enhance readability**: Tests focus on business logic rather than implementation details
- **Increase reusability**: Page objects can be used across multiple test files

## Architecture

```
tests/e2e/
├── pages/                    # Page Object classes
│   ├── BasePage.ts          # Base class with common functionality
│   ├── HomePage.ts          # Main interface page object
│   ├── ProgressPage.ts      # Progress tracking page object
│   ├── ResultsPage.ts       # Results display page object
│   └── index.ts             # Export all page objects
├── utils/                   # Test utilities
│   └── TestUtils.ts         # Common test helper methods
├── web-interface.test.ts    # Refactored tests using POM
├── accessibility-scanning.test.ts
├── interface-accessibility.test.ts
├── performance.test.ts
└── README.md               # Original E2E test documentation
```

## Page Objects

### BasePage.ts

The foundation class that provides common functionality for all page objects.

**Key Features:**
- Common selectors and element getters
- Standardized action methods (click, fill, focus, etc.)
- Validation methods (expectElementVisible, expectElementFocused, etc.)
- Navigation methods (goto, reload, goBack, goForward)
- Utility methods (waitForTimeout, setViewportSize, etc.)

**Usage:**
```typescript
import { BasePage } from './pages/BasePage';

export class MyPage extends BasePage {
    // Page-specific implementation
}
```

### HomePage.ts

Represents the main accessibility testing interface.

**Key Elements:**
- URL input fields (`#fullSiteUrl`, `#singlePageUrl`)
- Form submission buttons
- Scan option headings
- Progress, results, and error sections

**Key Methods:**
- `startFullSiteScan(url: string)` - Complete scan workflow
- `startSinglePageScan(url: string)` - Single page scan workflow
- `expectPageLoaded()` - Validate page load
- `expectScanOptionsVisible()` - Check scan options
- `testKeyboardNavigation()` - Test accessibility
- `testResponsiveDesign()` - Test responsiveness

**Usage:**
```typescript
const homePage = new HomePage(page);
await homePage.goto();
await homePage.startFullSiteScan('https://example.com');
```

### ProgressPage.ts

Handles real-time progress tracking and scan status.

**Key Elements:**
- Progress bar and text
- Stage indicators (browser, navigation, axe, pa11y, etc.)
- Progress details and updates

**Key Methods:**
- `waitForScanCompletion()` - Wait for scan to finish
- `waitForProcessingStart()` - Wait for processing to begin
- `getProgressPercentage()` - Get current progress
- `isScanInProgress()` - Check scan status
- `getActiveStage()` - Get current stage

**Usage:**
```typescript
const progressPage = new ProgressPage(page);
await progressPage.waitForScanCompletion();
const isComplete = await progressPage.isScanCompleted();
```

### ResultsPage.ts

Manages scan results display and report generation.

**Key Elements:**
- Results container and sections
- Error display
- Download buttons
- Navigation options

**Key Methods:**
- `validateScanResults()` - Check results structure
- `downloadPDF()` - Download PDF report
- `downloadJSON()` - Download JSON data
- `isScanSuccessful()` - Check success status
- `hasViolations()` - Check for violations

**Usage:**
```typescript
const resultsPage = new ResultsPage(page);
await resultsPage.waitForResultsSection();
const isSuccessful = await resultsPage.isScanSuccessful();
```

## Test Utilities

### TestUtils.ts

Provides common helper methods for E2E tests.

**Key Features:**
- Wait methods (waitForNetworkIdle, waitForElementVisible, etc.)
- Element interaction (clickIfExists, fillIfExists, etc.)
- Validation helpers (elementExists, elementIsVisible, etc.)
- Browser utilities (setViewportSize, pressKey, etc.)
- Accessibility checks (checkBasicAccessibility, checkMetaTags, etc.)
- Data generation (generateRandomString, generateRandomEmail, etc.)

**Usage:**
```typescript
const testUtils = new TestUtils(page);
await testUtils.waitForNetworkIdle();
await testUtils.setViewportSize(375, 667);
const randomUrl = testUtils.generateRandomURL();
```

## Best Practices

### 1. Page Object Design

**✅ Good:**
```typescript
// Encapsulate selectors
private readonly urlInputSelector = '#fullSiteUrl';

// Provide meaningful methods
async startFullSiteScan(url: string) {
    await this.fillFullSiteUrl(url);
    await this.submitFullSiteScan();
}

// Use descriptive validation methods
async expectPageLoaded() {
    await this.expectTitle(/Accessibility Testing/);
    await this.expectElementVisible(this.fullSiteUrlInput);
}
```

**❌ Avoid:**
```typescript
// Don't expose raw selectors
public urlInput = '#fullSiteUrl';

// Don't create overly specific methods
async fillUrlAndClickSubmit(url: string) {
    // Too specific, not reusable
}
```

### 2. Test Structure

**✅ Good:**
```typescript
test.describe('User Experience', () => {
    test('should provide clear feedback', async ({ page }) => {
        const homePage = new HomePage(page);
        await homePage.goto();
        await homePage.startFullSiteScan('https://example.com');
        // Test focuses on business logic
    });
});
```

**❌ Avoid:**
```typescript
test('should work', async ({ page }) => {
    await page.goto('/');
    await page.locator('#fullSiteUrl').fill('https://example.com');
    await page.locator('#fullSiteForm button[type="submit"]').click();
    // Too much implementation detail in test
});
```

### 3. Selector Strategy

**✅ Good:**
```typescript
// Use stable, semantic selectors
private readonly fullSiteUrlSelector = '#fullSiteUrl';
private readonly submitButtonSelector = '#fullSiteForm button[type="submit"]';

// Use data attributes for dynamic content
private readonly stageItemSelector = '[data-stage]';
```

**❌ Avoid:**
```typescript
// Don't use fragile selectors
private readonly buttonSelector = 'button:nth-child(2)';
private readonly textSelector = 'text=Some Text';
```

### 4. Error Handling

**✅ Good:**
```typescript
async clickElementIfExists(locator: Locator) {
    if (await locator.count() > 0) {
        await this.clickElement(locator);
    }
}

async waitForElementWithTimeout(locator: Locator, timeout: number = 10000) {
    await expect(locator).toBeVisible({ timeout });
}
```

### 5. Focus Management

**✅ Good (Direct Focus):**
```typescript
// Use direct focus for reliable element focusing
async focusFullSiteUrl() {
    await this.focusElement(this.fullSiteUrlInput);
    await this.expectElementFocused(this.fullSiteUrlInput);
}

// Test keyboard navigation with direct focus
async testKeyboardNavigation() {
    await this.focusFullSiteUrl();
    await this.focusFullSiteSubmitBtn();
    await this.focusFullSiteUrl();
    await this.expectElementFocused(this.fullSiteUrlInput);
}
```

**❌ Avoid (Tab Navigation):**
```typescript
// Don't rely on predicting exact tab order
async focusWithTab() {
    await this.pressKey('Tab'); // h1
    await this.pressKey('Tab'); // h2
    await this.pressKey('Tab'); // h3
    await this.pressKey('Tab'); // input - fragile!
    await this.expectElementFocused(this.fullSiteUrlInput);
}
```

**Why Direct Focus is Better:**
- **Reliable**: Not dependent on page structure or tab order
- **Cross-browser**: Works consistently across all browsers
- **Maintainable**: Less fragile when UI changes
- **Testable**: Easier to verify focus behavior

## Migration Guide

### From Old Tests to POM

**Before (Old Pattern):**
```typescript
test('should load interface', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('#fullSiteUrl')).toBeVisible();
    await expect(page.locator('#fullSiteForm button[type="submit"]')).toBeVisible();
});
```

**After (POM Pattern):**
```typescript
test('should load interface', async ({ page }) => {
    const homePage = new HomePage(page);
    await homePage.goto();
    await homePage.expectPageLoaded();
});
```

### Benefits of Migration

1. **Reduced Code Duplication**: Common selectors and actions are centralized
2. **Improved Maintainability**: UI changes only require updates in page objects
3. **Enhanced Readability**: Tests focus on business logic
4. **Increased Reusability**: Page objects can be used across multiple test files
5. **Better Error Messages**: Centralized error handling and validation
6. **Easier Debugging**: Clear separation of concerns

## Future Enhancements

### 1. Component Objects

For complex UI components, consider creating component objects:

```typescript
export class FormComponent {
    constructor(private page: Page) {}
    
    async fillAndSubmit(url: string) {
        // Component-specific logic
    }
}
```

### 2. Data Objects

Create data objects for test data:

```typescript
export class TestData {
    static readonly validUrls = [
        'https://example.com',
        'https://www.example.com',
        'https://example.com/path'
    ];
    
    static readonly invalidUrls = [
        'not-a-url',
        'ftp://example.com',
        'http://'
    ];
}
```

### 3. Configuration Objects

Create configuration objects for test settings:

```typescript
export class TestConfig {
    static readonly timeouts = {
        short: 5000,
        medium: 10000,
        long: 30000
    };
    
    static readonly viewports = {
        mobile: { width: 375, height: 667 },
        tablet: { width: 768, height: 1024 },
        desktop: { width: 1280, height: 720 }
    };
}
```

## Conclusion

The Page Object Model implementation provides a solid foundation for maintainable and scalable E2E tests. By following the established patterns and best practices, tests become more readable, maintainable, and reliable.

The modular design allows for easy extension and modification as the application evolves, while the centralized selectors and actions reduce the impact of UI changes on test code. 