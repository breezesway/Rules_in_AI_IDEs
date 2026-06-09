# ⚡ Quick Reference Guide

## 🚨 Critical Information (Read First)

### Most Important Files (DO NOT BREAK)
1. **`src/core/types/common.ts`** - All shared types and interfaces
2. **`src/utils/services/error-handler-service.ts`** - Central error handling
3. **`src/utils/services/configuration-service.ts`** - Configuration management
4. **`src/web/server.ts`** - Main web server entry point
5. **`tests/` directory** - Unit and integration tests
6. **`jest.config.js`** - Testing framework configuration

### Singleton Services (Use `getInstance()`)
```typescript
// ✅ CORRECT
const errorHandler = ErrorHandlerService.getInstance();
const configService = ConfigurationService.getInstance();

// ❌ NEVER DO THIS
const errorHandler = new ErrorHandlerService();
```

### Import Patterns
```typescript
// ✅ Use @/ alias for src/ imports
import { ErrorHandlerService } from '@/utils/services/error-handler-service';

// ✅ Use relative paths for same directory level
import { ConfigurationService } from '../services/configuration-service';

// ✅ Use relative paths for core types
import { PageInfo, AnalysisResult } from '../../core/types/common';
```

## 🔧 Common Operations

### Adding a New Service
```typescript
// 1. Create file: src/utils/services/my-service.ts
export class MyService {
  private static instance: MyService;
  
  private constructor() {}
  
  public static getInstance(): MyService {
    if (!MyService.instance) {
      MyService.instance = new MyService();
    }
    return MyService.instance;
  }
  
  // Your service methods here
}

// 2. Add to DEPENDENCY_MAP.md
// 3. Update this QUICK_REFERENCE.md
```

### Adding a New Type
```typescript
// 1. Add to src/core/types/common.ts
export interface MyNewType {
  id: string;
  name: string;
  // ... other properties
}

// 2. Update all files that need this type
// 3. Add to DEPENDENCY_MAP.md
```

### Adding a New Test Runner
```typescript
// 1. Create file: src/utils/runners/my-test-runner.ts
export class MyTestRunner {
  constructor(private page: Page) {}
  
  async run(): Promise<ServiceResult<AnalysisResult>> {
    // Implementation
  }
}

// 2. Add to ParallelAnalyzer.registerAccessibilityTools()
// 3. Update DEPENDENCY_MAP.md
```

### Error Handling Pattern
```typescript
// ✅ CORRECT - Always use ErrorHandlerService
const errorHandler = ErrorHandlerService.getInstance();

try {
  // Your code
} catch (error) {
  return errorHandler.handleError(error, 'Context message');
}

// ✅ CORRECT - Return ServiceResult
return {
  success: true,
  data: result,
  message: 'Operation successful'
};
```

### Configuration Pattern
```typescript
// ✅ CORRECT - Always use ConfigurationService
const configService = ConfigurationService.getInstance();
const setting = configService.get('settingName', defaultValue);

// ❌ NEVER hardcode values
const setting = 'hardcoded-value';
```

### Testing Pattern
```typescript
// ✅ CORRECT - Run tests before making changes
npm test

// ✅ CORRECT - Check test coverage
npm run test:coverage

// ✅ CORRECT - Run specific test categories
npm run test:unit
npm run test:integration
npm run test:services

// ✅ CORRECT - Follow testing patterns from TESTING_ROADMAP.md
// - Use Jest for unit testing
// - Mock external dependencies with `any` types
// - Test public interfaces, not implementation details
// - Follow singleton pattern verification

// ❌ NEVER break existing tests without fixing them
// ❌ NEVER ignore TypeScript compilation errors in tests
```

### File Operations Pattern
```typescript
// ✅ CORRECT - Always use FileOperationsService
const fileOps = FileOperationsService.getInstance();

// ✅ CORRECT - Move files safely
const moveResult = fileOps.moveFile(sourcePath, destPath);
if (moveResult.success) {
  console.log(`File moved: ${moveResult.filePath}`);
}

// ✅ CORRECT - Move files by pattern
const moveResult = fileOps.moveFilesByPattern(sourceDir, destDir, /\.json$/);
if (moveResult.success && moveResult.movedFiles) {
  console.log(`Moved ${moveResult.movedFiles.length} files`);
}

// ✅ CORRECT - Ensure directory exists
const dirResult = fileOps.ensureDirectoryExists('./accessibility-reports/history');
if (!dirResult.success) {
  console.error('Failed to create directory:', dirResult.message);
}

// ❌ NEVER use direct fs operations for critical file operations
fs.renameSync(sourcePath, destPath); // Use FileOperationsService instead
```

### Cleanup Operations Pattern
```typescript
// ✅ CORRECT - Use WorkflowOrchestrator cleanup
const orchestrator = new WorkflowOrchestrator();
await orchestrator['cleanupReportsDirectory']();

// ✅ CORRECT - Web server cleanup integration
// Cleanup is automatically called in:
// - runFullSiteScanWithProgress() (Phase 0: 0-5%)
// - runSinglePageScanWithProgress() (Phase 0: 0-5%)

// ✅ CORRECT - History preservation
// The cleanup method:
// 1. Moves JSON files to accessibility-reports/history/
// 2. Deletes all PDF files for clean slate
// 3. Preserves history folder and its contents
// 4. Removes other temporary directories

// ❌ NEVER manually delete the history folder
// The cleanup logic explicitly preserves it
```

### Browser Lifecycle Management
```typescript
// ✅ CORRECT - Use BrowserManager singleton
const browserManager = BrowserManager.getInstance();

// ✅ CORRECT - Initialize browser once
await browserManager.initialize();

// ✅ CORRECT - Get page with session management
const page = await browserManager.getPage('my-session');

// ✅ CORRECT - Close only specific pages, not entire sessions
await browserManager.closePage('my-session');

// ✅ CORRECT - Check browser health before operations
const isHealthy = await browserManager.isBrowserHealthy();
if (!isHealthy) {
  await browserManager.forceReinitialize();
}

// ✅ CORRECT - Cleanup specific sessions only
await browserManager.cleanup('my-session');

// ❌ NEVER close entire browser during workflow
await browserManager.cleanupAll(); // Only use at end of entire workflow
```

### Browser Session Patterns
```typescript
// ✅ CORRECT - Use different sessions for different phases
const crawlerPage = await browserManager.getPage('crawler-session');
const analysisPage = await browserManager.getPage('analysis-session');
const pdfPage = await browserManager.getPage('pdf-generation');

// ✅ CORRECT - Browser persists through entire workflow
// Crawling → Analysis → PDF Generation (same browser instance)

// ❌ AVOID - Don't cleanup sessions between phases
await browserManager.cleanup('crawler-session'); // This closes browser context
```

### Error Recovery Patterns
```typescript
// ✅ CORRECT - Handle browser closure gracefully
try {
  const page = await browserManager.getPage('my-session');
  // Use page
} catch (error) {
  if (error.message.includes('Target page, context or browser has been closed')) {
    // Browser was closed, reinitialize
    await browserManager.forceReinitialize();
    const page = await browserManager.getPage('my-session');
  }
}
```

## 📁 File Locations Quick Reference

### Core Files
- **Types**: `src/core/types/common.ts`
- **Browser Management**: `src/core/utils/browser-manager.ts`

### Services
- **Error Handling**: `src/utils/services/error-handler-service.ts`
- **Configuration**: `src/utils/services/configuration-service.ts`
- **File Operations**: `src/utils/services/file-operations-service.ts`
- **Security**: `src/utils/services/security-validation-service.ts`

### Test Runners
- **Axe Core**: `src/utils/runners/axe-test-runner.ts`
- **Pa11y**: `src/utils/runners/pa11y-test-runner.ts`

### Orchestration
- **Main Orchestrator**: `src/utils/orchestration/workflow-orchestrator.ts`
- **Parallel Analysis**: `src/utils/orchestration/parallel-analyzer.ts`
- **Tool Orchestrator**: `src/utils/analysis/tool-orchestrator.ts`

### Web Interface
- **Server**: `src/web/server.ts`
- **HTML**: `src/public/index.html`
- **CSS**: `src/public/styles.css`
- **JavaScript**: `src/public/app.js`

## 🔍 Common Issues & Solutions

### Import Resolution Errors
```bash
# Problem: Module not found
Error: Cannot find module '@/utils/services/error-handler-service'

# Solution: Check tsconfig.json paths
{
  "paths": {
    "@/*": ["*"]
  }
}

# Also ensure tsc-alias is installed and used in build
npm install tsc-alias
```

### Singleton Pattern Violations
```typescript
// Problem: Multiple instances created
const service1 = new ErrorHandlerService();
const service2 = new ErrorHandlerService();

// Solution: Use getInstance()
const service1 = ErrorHandlerService.getInstance();
const service2 = ErrorHandlerService.getInstance();
// service1 === service2 (same instance)
```

### Type Errors
```typescript
// Problem: Missing type definitions
Property 'newProperty' does not exist on type 'PageInfo'

// Solution: Add to common.ts
export interface PageInfo {
  url: string;
  title: string;
  depth: number;
  foundOn: string;
  status: number;
  loadTime?: number;
  newProperty?: string; // Add here
}
```

### Service Method Missing
```typescript
// Problem: Method not found
errorHandler.newMethod is not a function

// Solution: Add method to service class
export class ErrorHandlerService {
  // ... existing methods
  
  public newMethod(): void {
    // Implementation
  }
}
```

## 🚀 Development Workflow

### Before Making Changes
1. ✅ Read `DEPENDENCY_MAP.md` for affected files
2. ✅ Check `ARCHITECTURE_DIAGRAM.md` for data flow
3. ✅ Review this `QUICK_REFERENCE.md`
4. ✅ Understand the change impact

### During Development
1. ✅ Use correct import patterns (`@/` vs `../`)
2. ✅ Use Singleton services with `getInstance()`
3. ✅ Handle errors with `ErrorHandlerService`
4. ✅ Use `ConfigurationService` for settings
5. ✅ Return `ServiceResult<T>` from services

### After Making Changes
1. ✅ Run TypeScript compilation: `npm run typecheck`
2. ✅ Test CLI functionality: `npm run cli`
3. ✅ Update documentation if needed
4. ✅ Add to CHANGELOG.md
5. ✅ Update this reference if adding new patterns

## 📋 Validation Checklist

### Before Committing
- [ ] TypeScript compilation passes (`npm run typecheck`)
- [ ] Web interface runs without errors (`npm start`)
- [ ] All imports use correct patterns
- [ ] Singleton services use `getInstance()`
- [ ] Error handling uses `ErrorHandlerService`
- [ ] Configuration uses `ConfigurationService`
- [ ] No hardcoded values
- [ ] Documentation updated if needed

### For New Features
- [ ] Added to `DEPENDENCY_MAP.md`
- [ ] Added to `ARCHITECTURE_DIAGRAM.md`
- [ ] Added to this `QUICK_REFERENCE.md`
- [ ] Added to `CHANGELOG.md`
- [ ] Follows existing patterns

## 🎯 Common Patterns

### Service Method Pattern
```typescript
public async myMethod(param: string): Promise<ServiceResult<MyType>> {
  const errorHandler = ErrorHandlerService.getInstance();
  
  try {
    // Implementation
    const result = await this.doSomething(param);
    
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

### Configuration Access Pattern
```typescript
const configService = ConfigurationService.getInstance();
const setting = configService.get('settingName', 'defaultValue');
```

### Error Handling Pattern
```typescript
const errorHandler = ErrorHandlerService.getInstance();

try {
  // Risky operation
} catch (error) {
  return errorHandler.handleError(error, 'Operation context');
}
```

### Type Definition Pattern
```typescript
// In src/core/types/common.ts
export interface MyNewInterface {
  id: string;
  name: string;
  optionalField?: string;
  readonly immutableField: string;
}
```

---

**Last Updated**: 18/12/2024 14:30 GMT
**Purpose**: Quick reference for common operations and troubleshooting