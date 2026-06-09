# 🤖 AI Development Guide

## 🎯 Purpose

This guide is specifically designed to help AI tools (like Cursor, GitHub Copilot, etc.) understand the accessibility testing codebase and prevent breaking changes during development. Use this guide before making any modifications to the codebase.

## 📚 Reference Documents

Before making any changes, **ALWAYS** consult these documents:

1. **`DEPENDENCY_MAP.md`** - Complete dependency relationships and import patterns
2. **`ARCHITECTURE_DIAGRAM.md`** - Visual system architecture and data flow
3. **`QUICK_REFERENCE.md`** - Fast answers to common questions and operations
4. **`PROJECT_OVERVIEW.md`** - High-level project understanding
5. **`TESTING_ROADMAP.md`** - Testing strategy and coverage plan
6. **`README.md`** - User-facing documentation and features

## 🚨 Critical Rules (NEVER BREAK)

### 1. Singleton Services
```typescript
// ✅ ALWAYS use getInstance()
const errorHandler = ErrorHandlerService.getInstance();
const configService = ConfigurationService.getInstance();

// ❌ NEVER create new instances
const errorHandler = new ErrorHandlerService(); // BREAKS EVERYTHING
```

### 2. Web Interface Architecture
```typescript
// ✅ Web server uses existing services
const orchestrator = new WorkflowOrchestrator();
const result = await orchestrator.runAccessibilityAudit(url, options);

// ✅ API endpoints return consistent JSON responses
res.json({
  success: true,
  data: result
});

// ❌ DON'T create new business logic in web server
// Use existing services and orchestrators
```

### 3. Import Patterns
```typescript
// ✅ Use @/ alias for src/ imports
import { ErrorHandlerService } from '@/utils/services/error-handler-service';

// ✅ Use relative paths for same directory level
import { ConfigurationService } from '../services/configuration-service';

// ✅ Use relative paths for core types
import { PageInfo, AnalysisResult } from '../../core/types/common';
```

### 4. Cleanup Operations
```typescript
// ✅ CORRECT - Use WorkflowOrchestrator cleanup
const orchestrator = new WorkflowOrchestrator();
await orchestrator['cleanupReportsDirectory']();

// ✅ CORRECT - Web server automatically includes cleanup
// runFullSiteScanWithProgress() and runSinglePageScanWithProgress()
// both include cleanup phase (0-5%)

// ✅ CORRECT - History preservation is automatic
// JSON files moved to accessibility-reports/history/
// History folder and contents are preserved
// All PDF files deleted for clean slate

// ❌ NEVER manually delete history folder
// The cleanup logic explicitly preserves it with: if (file !== 'history')
```

### 5. Error Handling
```typescript
// ✅ ALWAYS use ErrorHandlerService
const errorHandler = ErrorHandlerService.getInstance();

try {
  // Your code
} catch (error) {
  return errorHandler.handleError(error, 'Context message');
}

// ✅ ALWAYS return ServiceResult<T>
return {
  success: true,
  data: result,
  message: 'Operation successful'
};
```

### 6. Configuration
```typescript
// ✅ ALWAYS use ConfigurationService
const configService = ConfigurationService.getInstance();
const setting = configService.get('settingName', defaultValue);

// ❌ NEVER hardcode values
const setting = 'hardcoded-value'; // BREAKS CONFIGURATION
```

### 7. Testing Framework
```typescript
// ✅ ALWAYS run tests before making changes
npm test

// ✅ ALWAYS check test coverage
npm run test:coverage

// ✅ ALWAYS follow testing patterns from TESTING_ROADMAP.md
// - Use Jest for unit testing
// - Mock external dependencies with `any` types
// - Test public interfaces, not implementation details
// - Follow singleton pattern verification

// ❌ NEVER break existing tests without fixing them
// ❌ NEVER ignore TypeScript compilation errors in tests
```

## 🔍 Pre-Change Checklist

Before making ANY changes, verify:

### 1. Understand the Change Impact
- [ ] Which files will be affected?
- [ ] Are there any dependencies that will break?
- [ ] Does this change existing functionality?
- [ ] Will this affect the CLI entry point?

### 2. Check Critical Files
- [ ] `src/core/types/common.ts` - Are types being modified?
- [ ] `src/utils/services/error-handler-service.ts` - Is error handling affected?
- [ ] `src/utils/services/configuration-service.ts` - Is configuration involved?
- [ ] `src/cli/accessibility-test-cli.ts` - Is CLI functionality affected?
- [ ] `tests/` directory - Are tests being modified or added?
- [ ] `jest.config.js` - Is testing configuration affected?

### 3. Verify Import Patterns
- [ ] Are imports using correct patterns (`@/` vs `../`)?
- [ ] Are all imports resolving correctly?
- [ ] Are there any circular dependencies?

### 4. Check Service Usage
- [ ] Are Singleton services using `getInstance()`?
- [ ] Are all service methods being called correctly?
- [ ] Are return types consistent with `ServiceResult<T>`?

## 🛠️ Common AI Development Scenarios

### Scenario 1: Adding a New Feature
```
1. Read DEPENDENCY_MAP.md to understand affected components
2. Check ARCHITECTURE_DIAGRAM.md for data flow
3. Follow patterns in QUICK_REFERENCE.md
4. Add types to common.ts if needed
5. Implement feature following existing patterns
6. Update documentation
7. Add to CHANGELOG.md
```

### Scenario 2: Fixing a Bug
```
1. Identify the root cause using dependency map
2. Check if it's a service, type, or import issue
3. Follow existing error handling patterns
4. Test the fix thoroughly
5. Update documentation if needed
6. Add to CHANGELOG.md
```

### Scenario 3: Refactoring Code
```
1. Map all dependencies before starting
2. Check for Singleton service violations
3. Verify import patterns are maintained
4. Ensure error handling is preserved
5. Test thoroughly after refactoring
6. Update all reference documents
```

## 🚫 Common AI Mistakes to Avoid

### 1. Breaking Singleton Pattern
```typescript
// ❌ WRONG - This breaks the entire system
export class MyService {
  constructor() {} // Should be private
}

// ✅ CORRECT
export class MyService {
  private static instance: MyService;
  private constructor() {}
  
  public static getInstance(): MyService {
    if (!MyService.instance) {
      MyService.instance = new MyService();
    }
    return MyService.instance;
  }
}
```

### 2. Incorrect Import Patterns
```typescript
// ❌ WRONG - Mixed import patterns
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '../services/configuration-service';

// ✅ CORRECT - Consistent patterns
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
```

### 3. Missing Error Handling
```typescript
// ❌ WRONG - No error handling
public async myMethod(): Promise<MyType> {
  return await this.doSomething();
}

// ✅ CORRECT - Proper error handling
public async myMethod(): Promise<ServiceResult<MyType>> {
  const errorHandler = ErrorHandlerService.getInstance();
  
  try {
    const result = await this.doSomething();
    return {
      success: true,
      data: result,
      message: 'Operation successful'
    };
  } catch (error) {
    return errorHandler.handleError(error, 'Context for myMethod');
  }
}
```

### 4. Hardcoding Values
```typescript
// ❌ WRONG - Hardcoded configuration
const timeout = 30000;
const maxRetries = 3;

// ✅ CORRECT - Configuration service
const configService = ConfigurationService.getInstance();
const timeout = configService.get('timeout', 30000);
const maxRetries = configService.get('maxRetries', 3);
```

## 🔧 Development Workflow for AI Tools

### Step 1: Analysis
1. Read the user's request carefully
2. Identify which components are involved
3. Check `DEPENDENCY_MAP.md` for dependencies
4. Review `ARCHITECTURE_DIAGRAM.md` for data flow
5. Consult `QUICK_REFERENCE.md` for patterns

### Step 2: Planning
1. Map out the changes needed
2. Identify potential breaking points
3. Plan the implementation approach
4. Consider error handling requirements
5. Plan documentation updates

### Step 3: Implementation
1. Follow existing patterns strictly
2. Use correct import patterns
3. Implement proper error handling
4. Use Singleton services correctly
5. Return appropriate types

### Step 4: Validation
1. Check TypeScript compilation
2. Verify CLI functionality
3. Test error scenarios
4. Update documentation
5. Add to CHANGELOG.md

## 📋 Validation Commands

After making changes, always run:

```bash
# TypeScript compilation check
npm run typecheck

# Run all tests
npm test

# Check test coverage
npm run test:coverage

# CLI functionality test
npm run cli

# Build verification
npm run build
```

## 🎯 Key Principles for AI Development

### 1. Conservative Approach
- When in doubt, don't change it
- Preserve existing functionality
- Follow established patterns exactly

### 2. Documentation First
- Always check reference documents
- Update documentation when making changes
- Maintain consistency across all docs

### 3. Error Handling
- Always handle errors properly
- Use ErrorHandlerService for all errors
- Return ServiceResult<T> from services

### 4. Configuration
- Never hardcode values
- Use ConfigurationService for all settings
- Provide sensible defaults

### 5. Testing
- Test changes thoroughly
- Verify CLI functionality
- Check for regressions

## 🚨 Emergency Stop

If you encounter any of these issues, STOP and ask for help:

1. **TypeScript compilation errors** - Don't proceed until resolved
2. **Import resolution failures** - Check path aliases and dependencies
3. **Singleton pattern violations** - This breaks the entire system
4. **Missing error handling** - Can cause silent failures
5. **Hardcoded configuration** - Breaks flexibility

## 📞 Getting Help

If you're unsure about any aspect:

1. **Check the reference documents first**
2. **Look for similar patterns in existing code**
3. **Ask for clarification before proceeding**
4. **Start with a small, safe change**
5. **Test thoroughly before making larger changes**

---

**Remember**: This codebase is complex with many interdependencies. When in doubt, be conservative and follow existing patterns exactly. It's better to ask for clarification than to break the system.

**Last Updated**: 18/12/2024 14:30 GMT
**Purpose**: Guide AI tools to work safely with the accessibility testing codebase 