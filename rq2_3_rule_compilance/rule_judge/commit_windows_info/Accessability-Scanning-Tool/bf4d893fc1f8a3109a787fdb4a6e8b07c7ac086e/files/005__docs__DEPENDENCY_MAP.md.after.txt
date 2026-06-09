# 🔗 Dependency Map & Architecture Reference

This document provides a comprehensive map of all dependencies, import relationships, and architectural patterns in the accessibility testing application. Use this as a reference when making changes to prevent breaking existing functionality.

## 📁 Directory Structure & Module Relationships

```
src/
├── web/
│   └── server.ts                          # Express web server with WebSocket support
├── public/
│   ├── index.html                         # Web interface HTML
│   ├── styles.css                         # Web interface CSS
│   └── app.js                             # Web interface JavaScript
├── core/
│   ├── types/
│   │   └── common.ts                      # Shared type definitions
│   └── utils/
│       └── browser-manager.ts             # Browser lifecycle management
└── utils/
    ├── analysis/
    │   ├── accessibility-tool.ts          # Base accessibility tool interface
    │   └── tool-orchestrator.ts           # Multi-tool coordination
    ├── analyzers/
    │   └── page-analyzer.ts               # Page structure analysis
    ├── api/
    │   └── analysis-service.ts            # API service layer
    ├── crawler/
    │   └── site-crawler.ts                # Website crawling logic
    ├── orchestration/
    │   ├── accessibility-test-orchestrator.ts  # Main orchestrator
    │   ├── analysis-cache.ts              # Caching layer
    │   ├── analysis-worker.ts             # Worker pool management
    │   ├── parallel-analyzer.ts           # Parallel execution
    │   ├── smart-batcher.ts               # Batch processing
    │   ├── task-queue.ts                  # Task queue management
    │   └── workflow-orchestrator.ts       # Workflow coordination
    ├── processors/
    │   └── violation-processor.ts         # Violation processing
    ├── reporting/
    │   └── pdf-generators/
    │       ├── pdf-orchestrator.ts        # PDF generation orchestration
    │       └── pdf-template-generator.ts  # PDF template creation
    ├── runners/
    │   ├── axe-test-runner.ts             # axe-core integration
    │   └── pa11y-test-runner.ts           # Pa11y integration
    └── services/
        ├── configuration-service.ts       # Configuration management
        ├── error-handler-service.ts       # Error handling & logging
        ├── file-operations-service.ts     # File system operations
        └── security-validation-service.ts # Security validation

tests/
├── setup.ts                               # Global test setup and utilities
├── unit/
│   ├── core/
│   │   └── types/
│   │       └── common.test.ts             # Core types validation tests
│   ├── services/
│   │   ├── error-handler-service.test.ts  # ErrorHandlerService tests
│   │   ├── configuration-service.test.ts  # ConfigurationService tests
│   │   ├── security-validation-service.test.ts # SecurityValidationService tests
│   │   └── file-operations-service.test.ts # FileOperationsService tests
│   └── processors/
│       └── violation-processor.test.ts    # ViolationProcessor tests
└── integration/
    └── services-integration.test.ts       # Cross-service integration tests
```

## 🔄 Import Dependency Graph

### Core Dependencies (Most Critical)

**`src/core/types/common.ts`** - **CRITICAL: DO NOT MODIFY WITHOUT UPDATING ALL IMPORTERS**
- **Used by**: 15+ files across the entire codebase
- **Contains**: All shared interfaces, types, and data structures
- **Key Types**: `PageInfo`, `ProcessedViolation`, `ServiceResult`, `AnalysisResult`, `SiteWideAccessibilityReport`

**`src/utils/services/error-handler-service.ts`** - **CRITICAL: Singleton Service**
- **Used by**: 12+ files
- **Pattern**: Singleton with `getInstance()` method
- **Purpose**: Centralised error handling and logging

**`src/utils/services/configuration-service.ts`** - **CRITICAL: Singleton Service**
- **Used by**: 8+ files
- **Pattern**: Singleton with `getInstance()` method
- **Purpose**: Centralised configuration management

**`src/web/server.ts`** - **Web Server**
- **Dependencies**: `WorkflowOrchestrator`, `ErrorHandlerService`, `ConfigurationService`
- **Purpose**: Express.js web server providing RESTful API endpoints
- **Pattern**: Uses existing services for business logic
- **Key Methods**:
  - `runFullSiteScanWithProgress()` - Includes cleanup phase (0-5%)
  - `runSinglePageScanWithProgress()` - Includes cleanup phase (0-5%)
  - `/api/reports/regenerate` - Searches both main and history directories

### Service Layer Dependencies

**Core Services** (Singleton Pattern):
```
ErrorHandlerService (Singleton)
├── Used by: All other services and utilities
└── Dependencies: None (base service)

ConfigurationService (Singleton)
├── Used by: BrowserManager, SiteCrawler, TestRunners
└── Dependencies: None (base service)

FileOperationsService (Singleton)
├── Used by: PDF generators, report creation, WorkflowOrchestrator (cleanup)
├── Dependencies: ConfigurationService, SecurityValidationService
└── New Methods: moveFile(), moveFilesByPattern() for historical data preservation

SecurityValidationService (Singleton)
├── Used by: FileOperationsService
└── Dependencies: None (base service)
```

### Test Runner Dependencies

**`src/utils/runners/axe-test-runner.ts`**:
- **Dependencies**: `ConfigurationService`, `ErrorHandlerService`
- **External**: `@axe-core/playwright`, `axe-core`
- **Used by**: `ParallelAnalyzer`, `ToolOrchestrator`

**`src/utils/runners/pa11y-test-runner.ts`**:
- **Dependencies**: `ConfigurationService`, `ErrorHandlerService`
- **External**: `pa11y` (default import)
- **Used by**: `ParallelAnalyzer`, `ToolOrchestrator`

### Orchestration Layer Dependencies

**`src/utils/orchestration/parallel-analyzer.ts`**:
- **Dependencies**: `BrowserManager`, `ErrorHandlerService`, `ConfigurationService`
- **Imports**: `AxeTestRunner`, `Pa11yTestRunner` (dynamic imports)
- **Used by**: `AnalysisService`, `WorkflowOrchestrator`

**`src/utils/orchestration/workflow-orchestrator.ts`**:
- **Dependencies**: `BrowserManager`, `ParallelAnalyzer`, `FileOperationsService`
- **Used by**: CLI entry point, WebServer
- **Key Methods**: 
  - `cleanupReportsDirectory()` - Moves JSON files to history, deletes PDFs, preserves history folder
  - `runAccessibilityAudit()` - Main workflow with cleanup integration
  - `regenerateReportsFromExistingData()` - Searches both main and history directories

### Analysis Layer Dependencies

**`src/utils/analysis/tool-orchestrator.ts`**:
- **Dependencies**: `ErrorHandlerService`, `ViolationProcessor`
- **Used by**: `AnalysisService`, `AnalysisWorker`

**`src/utils/processors/violation-processor.ts`**:
- **Dependencies**: `ConfigurationService`, `ErrorHandlerService`
- **Used by**: `ToolOrchestrator`, `AccessibilityTestOrchestrator`

## 🚨 Critical Import Patterns

### Path Alias Usage (`@/`)

**ALWAYS USE** `@/` path alias for imports from `src/`:
```typescript
// ✅ CORRECT
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

// ❌ INCORRECT - Use relative paths
import { ErrorHandlerService } from '../services/error-handler-service';
```

**Files using `@/` alias**:
- `src/utils/orchestration/workflow-orchestrator.ts`
- `src/utils/orchestration/accessibility-test-orchestrator.ts`
- `src/utils/orchestration/parallel-analyzer.ts`
- `src/utils/api/analysis-service.ts`
- `src/utils/crawler/site-crawler.ts`
- `src/utils/analysis/accessibility-tool.ts`
- `src/utils/processors/violation-processor.ts`
- `src/utils/analysis/tool-orchestrator.ts`
- `src/core/utils/browser-manager.ts`

### Relative Path Usage (`../`)

**Use relative paths** for imports within the same directory level:
```typescript
// ✅ CORRECT - Same directory level
import { ConfigurationService } from '../services/configuration-service';
import { ErrorHandlerService } from '../services/error-handler-service';

// ✅ CORRECT - Core types
import { PageInfo, AnalysisResult } from '../../core/types/common';
```

## 🔧 Singleton Service Pattern

**CRITICAL**: All services use the Singleton pattern. Never create new instances:

```typescript
// ✅ CORRECT
const errorHandler = ErrorHandlerService.getInstance();
const configService = ConfigurationService.getInstance();

// ❌ INCORRECT
const errorHandler = new ErrorHandlerService();
```

**Singleton Services**:
- `ErrorHandlerService`
- `ConfigurationService`
- `FileOperationsService`
- `SecurityValidationService`
- `BrowserManager`
- `AnalysisCache`

## 📊 Data Flow Architecture

### 1. Entry Point
```
Web Interface: index.html → app.js → /api/* → WebServer → WorkflowOrchestrator
```

### 2. Workflow Orchestration
```
WorkflowOrchestrator → SiteCrawler → ParallelAnalyzer
```

### 3. Analysis Pipeline
```
ParallelAnalyzer → ToolOrchestrator → [AxeTestRunner, Pa11yTestRunner]
```

### 4. Processing Pipeline
```
ToolOrchestrator → ViolationProcessor → PageAnalyzer
```

### 5. Reporting Pipeline
```
ViolationProcessor → PDF Generators → FileOperationsService
```

### 6. Web Response Pipeline
```
FileOperationsService → WebServer → JSON Response → app.js → UI Update
```

## 🚨 Breaking Change Prevention Rules

### 1. Type Safety
- **NEVER** modify interfaces in `common.ts` without updating all implementers
- **ALWAYS** use TypeScript strict mode for new code
- **NEVER** use `any` type - use proper interfaces

### 2. Service Dependencies
- **NEVER** create new service instances - use `getInstance()`
- **ALWAYS** check existing service usage before modifying
- **NEVER** remove service methods without updating all callers

### 3. Import Patterns
- **ALWAYS** use `@/` alias for imports from `src/`
- **NEVER** mix relative and absolute imports inconsistently
- **ALWAYS** check import paths when moving files

### 4. Error Handling
- **ALWAYS** use `ErrorHandlerService` for error handling
- **NEVER** throw raw errors without proper logging
- **ALWAYS** return `ServiceResult<T>` from service methods

### 5. Configuration
- **ALWAYS** use `ConfigurationService` for configuration
- **NEVER** hardcode configuration values
- **ALWAYS** validate configuration before use

## 🔍 Quick Reference for Common Changes

### Adding a New Service
1. Create service file in `src/utils/services/`
2. Implement Singleton pattern with `getInstance()`
3. Add to dependency map above
4. Update this document

### Adding a New Type
1. Add to `src/core/types/common.ts`
2. Update all files that need the type
3. Add to dependency map above

### Moving a File
1. Update all import statements (check both `@/` and `../` patterns)
2. Update `tsconfig.json` paths if needed
3. Update this dependency map

### Adding a New Test Runner
1. Create runner in `src/utils/runners/`
2. Implement required interfaces
3. Add to `ParallelAnalyzer.registerAccessibilityTools()`
4. Update dependency map

## 📋 Validation Checklist

Before making any changes, verify:

- [ ] All imports use correct patterns (`@/` vs `../`)
- [ ] Singleton services use `getInstance()` pattern
- [ ] New types are added to `common.ts`
- [ ] Error handling uses `ErrorHandlerService`
- [ ] Configuration uses `ConfigurationService`
- [ ] All dependencies are documented above
- [ ] TypeScript compilation passes
- [ ] No circular dependencies created

---

**Last Updated**: 18/12/2024 14:30 GMT
**Maintained by**: AI Assistant
**Purpose**: Prevent breaking changes during AI-assisted development 

## 🔄 Browser Lifecycle Management Dependencies

### BrowserManager Dependencies
- **Singleton Pattern**: `BrowserManager.getInstance()` - Single browser instance across entire application
- **Health Management**: `isBrowserHealthy()` → `forceReinitialize()` - Automatic browser recovery
- **Session Management**: `getContext()` → `getPage()` → `closePage()` - Granular resource management
- **Error Recovery**: Automatic reinitialization when browser is closed unexpectedly

### Workflow Browser Usage
```
WorkflowOrchestrator
├── performSiteCrawling() → BrowserManager.getPage('crawler-session')
├── performAccessibilityAnalysis() → ParallelAnalyzer → BrowserManager.getPage('analysis-*')
└── generateReports() → BrowserManager.getPage('pdf-generation')
```

### Critical Browser Rules
- **NEVER** call `cleanupAll()` during workflow execution
- **ALWAYS** use `closePage()` instead of `cleanup(sessionId)` for individual pages
- **CHECK** browser health before PDF generation: `isBrowserHealthy()`
- **RECOVER** from browser closure: `forceReinitialize()`

### Browser Session Lifecycle
1. **Initialization**: `BrowserManager.initialize()` (once per application)
2. **Crawling**: `getPage('crawler-session')` → `closePage('crawler-session')`
3. **Analysis**: `getPage('analysis-*')` → `closePage('analysis-*')`
4. **PDF Generation**: `getPage('pdf-generation')` → `cleanup('pdf-generation')`
5. **Final Cleanup**: `cleanupAll()` (only at end of entire workflow) 