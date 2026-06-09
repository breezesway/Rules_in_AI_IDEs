# Linting and Formatting Setup

This project uses ESLint and Prettier to maintain code quality and consistent
formatting.

## Tools Used

- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **TypeScript ESLint**: TypeScript-specific linting rules
- **Playwright ESLint Plugin**: Playwright-specific linting rules

## Configuration Files

- `eslint.config.js` - ESLint configuration (v9 format)
- `.prettierrc.js` - Prettier configuration
- `.prettierignore` - Files to exclude from formatting
- `tsconfig.json` - TypeScript configuration

## Available Scripts

```bash
# Type checking
npm run typecheck

# Linting
npm run lint          # Check for linting issues
npm run lint:fix      # Fix auto-fixable linting issues

# Formatting
npm run format        # Format all files
npm run format:check  # Check if files are formatted correctly

# Combined checks
npm run code:check    # Run all checks (typecheck + lint + format:check)
npm run code:fix      # Fix all auto-fixable issues (typecheck + lint:fix + format)
npm run pre-commit    # Run all checks before committing
```

## Linting Rules

### TypeScript Rules

- No unused variables (except those prefixed with `_`)
- Explicit `any` types are warnings (not errors)
- No var-requires allowed for dynamic imports
- Function return types are optional

### General Code Quality

- Console logs allowed (for test reporting)
- No debugger statements
- Prefer template literals over string concatenation
- Prefer const over let/var
- No duplicate imports

### Playwright-Specific Rules

- Expect assertions required in tests
- No page.pause() in production code
- Prefer element handles over eval
- No eval() usage
- No focused or skipped tests (warnings)

### Accessibility Testing Specific

- Empty functions allowed (for test stubs)
- Magic numbers allowed (for test configurations)
- More lenient rules in test files

## Code Style (Prettier)

- **Print Width**: 100 characters
- **Indentation**: 2 spaces
- **Quotes**: Single quotes
- **Semicolons**: Required
- **Trailing Commas**: ES5 style
- **Bracket Spacing**: Enabled
- **Arrow Function Parens**: Avoid when possible

## File Overrides

### Test Files (`*.spec.ts`, `*.test.ts`)

- More lenient `any` type usage
- Non-null assertions allowed
- Empty blocks allowed

### Config Files

- `require()` statements allowed
- More flexible formatting rules

## Ignored Files

The following files/directories are ignored by both ESLint and Prettier:

- `node_modules/`
- `dist/`, `build/`
- Test results and reports
- Generated/minified files
- Lock files
- Environment files
- IDE and OS files

## Usage Tips

1. **Before committing**: Run `npm run code:check` to ensure all code meets
   standards
2. **Auto-fix issues**: Use `npm run code:fix` to automatically resolve fixable
   problems
3. **IDE Integration**: Configure your IDE to run ESLint and Prettier on save
4. **CI/CD**: Add `npm run code:check` to your CI pipeline

## Common Issues and Solutions

### TypeScript Configuration Errors

If you see "file not found in project" errors:

1. Check that the file is included in `tsconfig.json`
2. Verify the file extension matches the ESLint configuration

### Formatting Conflicts

If ESLint and Prettier conflict:

1. Prettier rules take precedence
2. Use `npm run format` to apply Prettier formatting
3. Then run `npm run lint:fix` to fix remaining ESLint issues

### Test-Specific Issues

For accessibility testing code:

- `any` types are warnings, not errors
- Use `_` prefix for intentionally unused parameters
- Playwright `$$eval()` warnings can be ignored if necessary for accessibility
  testing

## Contributing

When adding new linting rules:

1. Update `eslint.config.js`
2. Test with `npm run lint`
3. Update this documentation
4. Ensure all existing code passes the new rules
