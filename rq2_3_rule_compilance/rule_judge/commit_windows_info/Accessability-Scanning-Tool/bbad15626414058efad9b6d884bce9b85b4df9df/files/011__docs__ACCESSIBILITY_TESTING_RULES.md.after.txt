# Accessibility Testing Rules

## 📋 **Overview**

This document defines the accessibility testing requirements and rules for all web UI components and interfaces in the accessibility testing application. All components must pass these tests before being deployed.

**Last Updated**: 23/01/2025 18:30 GMT  
**Status**: ✅ **ACTIVE** - All rules must be followed

---

## 🚨 **CRITICAL ACCESSIBILITY RULES** (MUST FOLLOW)

### **1. WCAG 2.1 AA Compliance**
- **ALL web components must pass WCAG 2.1 AA standards**
- **Testing Tools**: Axe-Core, Pa11y, and manual testing
- **Required Standards**: WCAG2AA (minimum), WCAG2AAA (preferred)
- **Testing Scope**: All user-facing interfaces, forms, and interactive elements

### **2. Automated Testing Requirements**

#### **Prerequisites**
```bash
# Start the web server before running accessibility tests
npm run dev:start

# In another terminal, start the Playwright test server
npx playwright test-server -c playwright.config.ts
```

#### **Running Accessibility Tests**
```bash
# Run all accessibility tests
npm run test:e2e -- --grep "accessibility"

# Run specific accessibility test suites
npm run test:e2e -- tests/e2e/interface-accessibility.test.ts
npm run test:e2e -- tests/e2e/web-interface.test.ts

# Run accessibility scanning tests
npm run test:e2e -- tests/e2e/accessibility-scanning.test.ts
```

#### **Troubleshooting**
- **Element Not Found Errors**: Ensure web server is running (`npm run dev:start`)
- **Timeout Errors**: Check if Playwright test server is running
- **Connection Errors**: Verify web server is accessible at `http://localhost:3000`

### **3. Manual Testing Checklist**
Before any UI changes are committed:
- [ ] **Keyboard Navigation**: All interactive elements accessible via keyboard
- [ ] **Screen Reader Compatibility**: Test with NVDA, JAWS, or VoiceOver
- [ ] **Colour Contrast**: Minimum 4.5:1 ratio for normal text, 3:1 for large text
- [ ] **Focus Indicators**: Visible focus indicators on all interactive elements
- [ ] **Semantic HTML**: Proper use of headings, landmarks, and ARIA labels
- [ ] **Form Accessibility**: Labels, error messages, and validation feedback

---

## 🧪 **Testing Patterns**

### **E2E Accessibility Testing**

```typescript
// ✅ CORRECT - Accessibility test pattern
test.describe('WCAG 2.1 AA Compliance', () => {
  test('should pass accessibility tests', async ({ page }) => {
    await page.goto('/');
    
    // Run axe-core tests
    const results = await page.evaluate(() => {
      return new Promise((resolve) => {
        axe.run((err, results) => {
          if (err) throw err;
          resolve(results);
        });
      });
    });
    
    expect(results.violations).toHaveLength(0);
  });
});
```

### **Component Accessibility Testing**

```typescript
// ✅ CORRECT - Component accessibility validation
test('should have proper ARIA labels', async ({ page }) => {
  await page.goto('/scan-options');
  
  // Check form labels
  const formLabels = await page.locator('label[for]').count();
  const formInputs = await page.locator('input[id]').count();
  expect(formLabels).toBe(formInputs);
  
  // Check heading structure
  const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
  expect(headings.length).toBeGreaterThan(0);
});
```

### **Keyboard Navigation Testing**

```typescript
// ✅ CORRECT - Keyboard navigation testing
test('should support keyboard navigation', async ({ page }) => {
  await page.goto('/');
  
  // Tab through all interactive elements
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toBeVisible();
  
  // Check focus indicators
  const focusStyles = await page.evaluate(() => {
    const focused = document.querySelector(':focus');
    return focused ? window.getComputedStyle(focused).outline : '';
  });
  
  expect(focusStyles).not.toBe('none');
});
```

---

## 🎯 **Component-Specific Requirements**

### **Web UI Components Requiring Accessibility Testing**

#### **Core Components** (`src/components/`)
- **LandingPage.ts** - Main landing page with scan options
- **FullSiteScanPage.ts** - Full site scanning interface
- **SinglePageScanPage.ts** - Single page scanning interface
- **ReportsPage.ts** - Report generation and viewing interface
- **Header.ts** - Navigation header component
- **Footer.ts** - Footer component
- **ScanOptions.ts** - Scan configuration options
- **ProgressSection.ts** - Real-time progress display
- **ResultsSection.ts** - Results display and navigation
- **ErrorSection.ts** - Error handling and display
- **WebInterface.ts** - Main web interface wrapper

#### **Public Assets** (`src/public/`)
- **index.html** - Main HTML template
- **app.js** - Client-side JavaScript
- **styles.css** - Styling and responsive design

#### **Server Components** (`src/web/`)
- **server.ts** - Express server with accessibility endpoints

### **Form Components**
- **Labels**: Every form control must have an associated label
- **Error Messages**: Clear, descriptive error messages with ARIA attributes
- **Validation**: Real-time validation with appropriate feedback
- **Required Fields**: Clear indication of required fields

```typescript
// ✅ CORRECT - Accessible form pattern
<form>
  <label for="url-input">Website URL</label>
  <input 
    id="url-input"
    type="url" 
    required
    aria-describedby="url-help url-error"
    aria-invalid="false"
  />
  <div id="url-help">Enter the full URL including https://</div>
  <div id="url-error" role="alert" aria-live="polite"></div>
</form>
```

### **Navigation Components**
- **Skip Links**: Provide skip navigation links for keyboard users
- **Landmarks**: Use semantic HTML5 landmarks (nav, main, aside, footer)
- **Breadcrumbs**: Implement accessible breadcrumb navigation
- **Menu Structure**: Proper heading hierarchy in navigation menus

### **Interactive Components**
- **Buttons**: Descriptive button text, proper ARIA labels
- **Links**: Clear link text that makes sense out of context
- **Modals**: Proper focus management, escape key handling
- **Tabs**: ARIA tabs pattern implementation

### **Data Display Components**
- **Tables**: Proper table headers, captions, and summaries
- **Lists**: Semantic list elements (ul, ol, dl)
- **Charts**: Alternative text descriptions for visual data
- **Status Messages**: ARIA live regions for dynamic content

---

## 🔧 **Testing Tools Configuration**

### **Axe-Core Configuration**
```typescript
// ✅ CORRECT - Axe-core test configuration
const axeConfig = {
  rules: {
    'color-contrast': { enabled: true },
    'heading-order': { enabled: true },
    'label': { enabled: true },
    'landmark-one-main': { enabled: true },
    'page-has-heading-one': { enabled: true },
    'region': { enabled: true }
  },
  runOnly: {
    type: 'tag',
    values: ['wcag2a', 'wcag2aa', 'wcag21aa']
  }
};
```

### **Pa11y Configuration**
```typescript
// ✅ CORRECT - Pa11y test configuration
const pa11yConfig = {
  standard: 'WCAG2AA',
  includeNotices: false,
  includeWarnings: true,
  timeout: 60000,
  wait: 1000,
  chromeLaunchConfig: {
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
};
```

---

## 📊 **Accessibility Metrics**

### **Current Test Status** (23/01/2025)
- **Total Accessibility Tests**: 42 tests across 3 test suites
- **Test Suites**:
  - `interface-accessibility.test.ts` - WCAG 2.1 AA compliance, keyboard navigation, screen reader compatibility
  - `web-interface.test.ts` - Form accessibility, responsive design, focus management
  - `accessibility-scanning.test.ts` - Scanning workflow accessibility
- **Status**: ⚠️ **Tests failing due to web server setup issues**
- **Required Action**: Fix web server configuration and element selectors
- **Progress Made**:
  - ✅ Fixed test selectors to match actual HTML structure
  - ✅ Updated test methods to handle hidden elements
  - ✅ Identified web server configuration issues
  - ✅ Created comprehensive accessibility testing framework

### **Required Test Coverage**
- **E2E Tests**: 100% of user-facing pages must have accessibility tests
- **Component Tests**: All interactive components must have accessibility validation
- **Manual Testing**: Regular manual testing with assistive technologies
- **Performance**: Accessibility tests must not significantly impact performance

### **Acceptance Criteria**
- **Zero Violations**: No WCAG 2.1 AA violations in automated tests
- **Keyboard Access**: All functionality accessible via keyboard
- **Screen Reader**: All content and functionality accessible to screen readers
- **Colour Independence**: All information conveyed through colour also available through other means
- **Responsive**: Accessibility maintained across all device sizes

---

## 🚨 **Emergency Stop Conditions**

### **Accessibility Failures**
- **Critical Violations**: Any WCAG 2.1 AA critical violations
- **Keyboard Blockers**: Any functionality not accessible via keyboard
- **Screen Reader Blockers**: Any content not accessible to screen readers
- **Colour Contrast Failures**: Text with insufficient contrast ratios
- **Missing Labels**: Form controls without proper labels

### **Required Actions**
1. **Immediate Fix**: Address accessibility violations before deployment
2. **Manual Verification**: Test fixes with assistive technologies
3. **Documentation**: Update accessibility testing documentation
4. **Review**: Code review with accessibility focus

---

## 📋 **Validation Checklist**

### **Before Deployment**
- [ ] All E2E accessibility tests pass
- [ ] No axe-core violations
- [ ] No Pa11y violations
- [ ] Keyboard navigation works for all functionality
- [ ] Screen reader testing completed
- [ ] Colour contrast ratios meet requirements
- [ ] Semantic HTML structure verified
- [ ] ARIA attributes properly implemented
- [ ] Focus management tested
- [ ] Error handling accessible

### **Component Development**
- [ ] Component has accessibility tests
- [ ] Keyboard interaction implemented
- [ ] Screen reader compatibility verified
- [ ] ARIA labels and descriptions added
- [ ] Focus indicators visible
- [ ] Colour contrast sufficient
- [ ] Semantic HTML used
- [ ] Error states accessible

---

## 🔗 **Related Documentation**

- **WCAG 2.1 Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **ARIA Authoring Practices**: https://www.w3.org/WAI/ARIA/apg/
- **Axe-Core Documentation**: https://github.com/dequelabs/axe-core
- **Pa11y Documentation**: https://pa11y.org/

---

## 📝 **Change Log**

### **23/01/2025 18:30 GMT - Initial Creation**
- Created comprehensive accessibility testing rules
- Defined WCAG 2.1 AA compliance requirements
- Established testing patterns and validation checklist
- Added component-specific accessibility requirements
- Integrated with existing testing infrastructure

---

**Status**: ✅ **ACTIVE** - All rules must be followed for web UI development 