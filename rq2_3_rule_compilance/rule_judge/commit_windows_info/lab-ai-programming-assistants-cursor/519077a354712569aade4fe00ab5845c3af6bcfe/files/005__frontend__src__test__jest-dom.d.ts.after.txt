import '@testing-library/jest-dom';

declare global {
  namespace Vi {
    interface Assertion {
      toBeInTheDocument(): void;
      toBeDisabled(): void;
      toBeEnabled(): void;
      toBeVisible(): void;
      toBeInTheDOM(): void;
      toHaveAttribute(attr: string, value?: string): void;
      toHaveClass(className: string): void;
      toHaveTextContent(text: string | RegExp): void;
      toHaveValue(value: string | string[] | number): void;
      toBeChecked(): void;
      toBeEmpty(): void;
      toBeEmptyDOMElement(): void;
      toBeRequired(): void;
      toHaveFocus(): void;
      toHaveStyle(css: string | object): void;
    }
  }
} 