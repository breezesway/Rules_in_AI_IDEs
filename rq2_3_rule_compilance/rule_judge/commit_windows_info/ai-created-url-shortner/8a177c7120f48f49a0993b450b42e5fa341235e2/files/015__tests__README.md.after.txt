# Testing Setup

This project is configured with comprehensive testing using `@nuxt/test-utils` for unit tests, component tests, and end-to-end tests.

## 🧪 Test Types

### Unit Tests

Test individual functions, utilities, and composables in isolation.
**Co-located tests are preferred** - place test files next to the code they test.

**Example:**

```bash
npm run test:unit
```

### Component Tests

Test Vue components with Nuxt context and auto-imports.
**Co-located tests are preferred** - place test files next to your component files.

**Example:**

```bash
npm run test -- app/components
```

### End-to-End Tests (`tests/e2e/`)

Test complete user workflows using Playwright.

**Example:**

```bash
npm run test:e2e
```

## 🚀 Quick Start

### Run all tests

```bash
npm run test
```

### Run tests in watch mode

```bash
npm run test:watch
```

### Run specific test files

```bash
# All unit tests (includes co-located)
npm run test:unit

# Tests in specific directory
npm run test -- tests/unit

# Co-located component test
npm run test -- app/components/ui/button/Button.nuxt.test.ts

# Co-located utility test
npm run test -- app/lib/utils.test.ts

# Single test file by pattern
npm run test -- --run "**/Button*.test.ts"
```

### Run E2E tests

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run specific browser
npx playwright test --project=chromium
```

## 📁 Test File Conventions

### Unit/Component Tests (Vitest)

**Co-located Tests:**

- Place test files next to the code they test
- `ComponentName.test.ts` or `ComponentName.nuxt.test.ts` next to `ComponentName.vue`
- `utils.test.ts` next to `utils.ts`
- `composable.nuxt.test.ts` next to `composable.ts`

### E2E Tests (Playwright)

- Files ending with `.spec.ts` in `tests/e2e/` directory
- Use Playwright's test runner

### File Naming Patterns

- `*.test.ts` - Unit tests (Node environment)
- `*.nuxt.test.ts` - Unit tests (Nuxt environment)
- `*.spec.ts` - Any test type
- `*.nuxt.spec.ts` - Nuxt environment tests

## 🔧 Writing Tests

### Co-located Unit Tests

```typescript
// app/lib/utils.test.ts
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";
import { myUtilFunction } from "./utils"; // relative import

describe("utils", () => {
  it("should work correctly", () => {
    expect(myUtilFunction("input")).toBe("expected");
  });
});
```

### Co-located Component Tests

```typescript
// app/components/ui/button/Button.nuxt.test.ts
// @vitest-environment nuxt
import { mountSuspended } from "@nuxt/test-utils/runtime";
import Button from "./Button.vue"; // relative import

it("renders correctly", async () => {
  const component = await mountSuspended(Button, {
    props: { title: "Test" },
  });

  expect(component.text()).toContain("Test");
});
```

### Co-located Composable Tests

```typescript
// app/composables/useExample.nuxt.test.ts
// @vitest-environment nuxt
import { describe, it, expect } from "vitest";
import { useExample } from "./useExample";

describe("useExample", () => {
  it("works correctly", () => {
    const { count, increment } = useExample();
    expect(count.value).toBe(0);
    increment();
    expect(count.value).toBe(1);
  });
});
```

### E2E Tests

```typescript
import { test, expect } from "@nuxt/test-utils/playwright";

test("homepage works", async ({ page, goto }) => {
  await goto("/");
  await expect(page.getByText("Hello World")).toBeVisible();
});
```

## 🛠️ Available Test Utilities

### Unit/Component Tests

- `mountSuspended()` - Mount components with Nuxt context
- `renderSuspended()` - Render with Testing Library
- All Nuxt composables (`useRoute`, `useRouter`, etc.)
- Auto-imports work as expected

### E2E Tests

- `goto(path)` - Navigate to pages
- `$fetch(url)` - Fetch server responses
- `createPage(url)` - Create browser pages
- Full Playwright API available

## 📊 Coverage

Run tests with coverage:

```bash
npm run test:coverage
```

## 🐛 Debugging

### Debug Unit/Component Tests

```bash
# Run single test file with verbose output
npm run test -- --reporter=verbose app/components/ui/button/Button.nuxt.test.ts

# Run tests in UI mode (if configured)
npm run test -- --ui
```

### Debug E2E Tests

```bash
# Run with browser visible
npx playwright test --headed

# Run with debug mode
npx playwright test --debug

# Run with UI
npm run test:e2e:ui
```

## 🎯 Best Practices

### Test Organization

- **Co-locate tests with source code** for better maintainability
- Use descriptive test file names that match source files
- Group related tests in describe blocks
- Use relative imports in co-located tests

### Unit Tests

- Test one thing at a time
- Use descriptive test names
- Mock external dependencies
- Test edge cases and error conditions

### Component Tests

- Test component behavior, not implementation
- Use realistic props and slots
- Test user interactions
- Verify rendered output

### E2E Tests

- Test critical user journeys
- Use data-testid attributes for reliable selectors
- Test responsive behavior
- Include accessibility checks

## 🔧 Configuration

### Vitest Config (`vitest.config.ts`)

- Configured for Nuxt environment
- HappyDOM for fast DOM simulation
- Built-in mocks enabled
- **Supports co-located tests** with include patterns

### Playwright Config (`playwright.config.ts`)

- Tests run against development server
- Multiple browsers supported (Chromium enabled by default)
- Screenshots and traces on failure

## 📚 Resources

- [Nuxt Test Utils Documentation](https://nuxt.com/docs/getting-started/testing)
- [Vitest Documentation](https://vitest.dev/)
- [Playwright Documentation](https://playwright.dev/)
- [Vue Test Utils](https://vue-test-utils.vuejs.org/)
