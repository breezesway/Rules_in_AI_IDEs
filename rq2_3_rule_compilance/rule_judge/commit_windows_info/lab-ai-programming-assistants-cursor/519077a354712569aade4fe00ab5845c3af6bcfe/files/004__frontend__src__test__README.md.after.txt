# Frontend Testing Guide

This project uses Vitest and React Testing Library for unit testing. This document provides guidelines for writing and running tests.

## Test Stack

- **Vitest**: Test runner and framework
- **React Testing Library**: DOM testing utilities for React
- **jest-dom**: Custom DOM element matchers
- **User Event**: Simulate user interactions

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode (development)
npm run test:watch

# Run tests with UI
npm run test:ui

# Run tests with coverage report
npm run test:coverage
```

## Writing Tests

### Component Testing

Basic component test structure:

```tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import YourComponent from './YourComponent';

describe('YourComponent', () => {
  it('renders correctly', () => {
    render(<YourComponent />);
    
    // Assert element exists
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

### Testing with Router or other Providers

Use the `renderWithProviders` utility:

```tsx
import { describe, it, expect } from 'vitest';
import { renderWithProviders, screen } from '../test/utils';
import YourComponent from './YourComponent';

describe('YourComponent', () => {
  it('renders correctly with router context', () => {
    renderWithProviders(<YourComponent />, { route: '/some-route' });
    
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

### Testing User Interactions

```tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import YourComponent from './YourComponent';

describe('YourComponent', () => {
  it('handles button click', async () => {
    const handleClick = vi.fn();
    render(<YourComponent onClick={handleClick} />);
    
    const button = screen.getByRole('button', { name: 'Click Me' });
    await userEvent.click(button);
    
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Best Practices

1. Test component behavior, not implementation details
2. Prefer user-centric queries (getByRole, getByText) over test IDs
3. Write tests that resemble how users interact with your app
4. Keep tests focused and small
5. Test edge cases and error states
6. Use mocks judiciously for external dependencies

## Folder Structure

Tests should be located next to the component they test with a `.test.tsx` or `.spec.tsx` extension.

```
src/
├── components/
│   ├── Button.tsx
│   ├── Button.test.tsx  # Test file for Button component
│   └── ...
├── test/
│   ├── setup.ts         # Global test setup
│   └── utils.tsx        # Test utilities
└── ...
``` 