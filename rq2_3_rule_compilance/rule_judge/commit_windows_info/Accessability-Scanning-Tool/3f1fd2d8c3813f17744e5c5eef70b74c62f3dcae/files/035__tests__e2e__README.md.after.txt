# End-to-End (E2E) Tests

This directory contains Playwright E2E tests for the accessibility testing web interface.

## Overview

These tests verify that the web interface works correctly from a user's perspective, testing complete workflows and user interactions.

## Test Structure

```
tests/e2e/
├── README.md                    # This file
├── web-interface.test.ts        # Basic web interface functionality tests
├── accessibility-scanning.test.ts # Accessibility scanning workflow tests (planned)
├── report-generation.test.ts    # Report generation workflow tests (planned)
├── user-journey.test.ts         # Complete user journey tests (planned)
├── interface-accessibility.test.ts # Interface accessibility compliance tests (planned)
└── wcag-compliance.test.ts      # WCAG compliance verification tests (planned)
```

## Running E2E Tests

### Prerequisites

1. **Install Playwright browsers** (if not already installed):
   ```bash
   npx playwright install
   ```

2. **Build the application**:
   ```bash
   npm run build
   ```

### Test Commands

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI (interactive)
npm run test:e2e:ui

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed

# Run E2E tests in debug mode
npm run test:e2e:debug

# Run specific test file
npx playwright test tests/e2e/web-interface.test.ts

# Run tests for specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

## Test Configuration

The Playwright configuration (`playwright.config.ts`) is set up to:

- **Auto-start the web server** before running tests
- **Test multiple browsers** (Chrome, Firefox, Safari)
- **Use appropriate timeouts** for E2E testing
- **Capture screenshots** on test failures
- **Run tests in parallel** for efficiency

## Test Categories

### 1. Web Interface Tests (`web-interface.test.ts`)
- Page loading and basic functionality
- Form validation and user input
- Accessibility features (ARIA, keyboard navigation)
- Responsive design testing

### 2. Accessibility Scanning Tests (planned)
- Complete accessibility scanning workflows
- URL input and validation
- Real-time progress tracking
- Error handling and recovery

### 3. Report Generation Tests (planned)
- Report generation workflows
- PDF and JSON report creation
- Historical data management
- Report regeneration functionality

### 4. User Journey Tests (planned)
- Complete end-to-end user workflows
- Multi-step processes
- Cross-browser compatibility
- Performance testing

### 5. Interface Accessibility Tests (planned)
- WCAG 2.1 AA compliance verification
- Color contrast testing
- Screen reader compatibility
- Keyboard navigation testing

## Best Practices

1. **Test Real User Scenarios**: Focus on actual user workflows
2. **Cross-Browser Testing**: Ensure compatibility across browsers
3. **Accessibility Testing**: Verify the interface itself is accessible
4. **Error Handling**: Test error scenarios and recovery
5. **Performance**: Monitor test execution time and performance

## Integration with Testing Pyramid

E2E tests represent the **top 5%** of the testing pyramid:

- **Unit Tests (70%)**: Individual functions and methods
- **Integration Tests (20%)**: Service interactions
- **Component Tests (5%)**: UI components in isolation
- **E2E Tests (5%)**: Complete user workflows ← **This layer**

## Future Enhancements

- [ ] Add axe-core integration for interface accessibility testing
- [ ] Implement visual regression testing
- [ ] Add performance benchmarking
- [ ] Create test data fixtures
- [ ] Add parallel test execution optimization 