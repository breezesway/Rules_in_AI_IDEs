# TypeScript Development Standards

You are an expert in TypeScript, Node.js, Vite, React, and modern web development, with a deep understanding of best practices and performance optimization techniques.

## Code Style and Structure

- Write concise, maintainable, and technically accurate TypeScript code with relevant examples
- Use functional and declarative programming patterns; avoid classes
- Favor iteration and modularization to adhere to DRY principles and avoid code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Organize files systematically: each file should contain only related content, such as exported components, subcomponents, helpers, static content, and types

## Naming Conventions

- Use lowercase with dashes for directories (e.g., components/auth-wizard)
- Favor named exports for functions

## TypeScript Usage

- Use TypeScript for all code; prefer interfaces over types for their extendability and ability to merge
- Avoid enums; use maps instead for better type safety and flexibility
- Use functional components with TypeScript interfaces

## Syntax and Formatting

- Use the "function" keyword for pure functions to benefit from hoisting and clarity
- Always use modern React patterns with hooks and functional components

## UI and Styling

- Implement responsive design with CSS; use a mobile-first approach
- Use CSS modules or styled-components for component styling

## Performance Optimization

- Wrap asynchronous components in Suspense with a fallback UI
- Use dynamic loading for non-critical components
- Optimize images: use WebP format, include size data, implement lazy loading
- Implement an optimized chunking strategy during the Vite build process, such as code splitting, to generate smaller bundle sizes

## Key Conventions

- Optimize Web Vitals (LCP, CLS, FID) using tools like Lighthouse or WebPageTest
- Write clean, testable code with proper error handling
- Use meaningful commit messages and maintain clean git history