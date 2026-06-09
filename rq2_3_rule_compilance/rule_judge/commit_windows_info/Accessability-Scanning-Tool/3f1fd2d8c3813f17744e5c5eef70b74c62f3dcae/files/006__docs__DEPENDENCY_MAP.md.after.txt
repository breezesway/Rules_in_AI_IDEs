# 🔗 Dependency Map & Architecture Reference

This document provides a comprehensive map of all dependencies, import relationships, and architectural patterns in the accessibility testing application. Use this as a reference when making changes to prevent breaking existing functionality.

## 📁 Directory Structure & Module Relationships

```
src/
├── components/                            # Shared UI Components (NEW)
│   ├── Header.ts                          # Header component
│   ├── ScanOptions.ts                     # Scan options component
│   ├── ProgressSection.ts                 # Progress tracking component
│   ├── ResultsSection.ts                  # Results display component
│   ├── ErrorSection.ts                    # Error handling component
│   ├── Footer.ts                          # Footer component
│   ├── WebInterface.ts                    # Main web interface component
│   └── index.ts                           # Component exports
├── web/
│   └── server.ts                          # Express web server with WebSocket support
├── public/
│   ├── index.html                         # Web interface HTML
│   ├── styles.css                         # Web interface CSS (shared with Storybook)
│   └── app.js                             # Web interface JavaScript
├── core/
│   ├── types/
│   │   └── common.ts                      # Shared type definitions
│   └── utils/
│       └── browser-manager.ts             # Browser lifecycle management
tests/
├── e2e/                                   # Playwright E2E tests for web interface
│   ├── README.md                          # E2E testing documentation
│   └── web-interface.test.ts              # Web interface E2E tests
├── unit/                                  # Jest unit tests
├── integration/                           # Jest integration tests
├── storybook/                             # Storybook validation tests
│   └── storybook-validation.test.ts       # Component architecture validation
└── setup.ts                               # Global test setup
```
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
│   │       └── common.test.ts             # Core types validation tests (26 tests passing)
│   ├── services/
│   │   ├── error-handler-service.test.ts  # ErrorHandlerService tests (25 tests passing)
│   │   ├── configuration-service.test.ts  # ConfigurationService tests (22 tests passing)
│   │   ├── security-validation-service.test.ts # SecurityValidationService tests (26 tests passing)
│   │   └── file-operations-service.test.ts # FileOperationsService tests (pending)
│   └── processors/
│       └── violation-processor.test.ts    # ViolationProcessor tests (9 tests passing)
├── e2e/
│   ├── README.md                          # E2E testing documentation
│   └── web-interface.test.ts              # Web interface E2E tests (24 tests across 3 browsers)
└── integration/
    └── services-integration.test.ts       # Cross-service integration tests (21 tests passing)
```

## 🔄 Import Dependency Graph

### Core Dependencies (Most Critical)

**`src/core/types/common.ts`** - **CRITICAL: DO NOT MODIFY WITHOUT UPDATING ALL IMPORTERS**
- **Used by**: 15+ files across the entire codebase
- **Contains**: All shared interfaces, types, and data structures
- **Key Types**: `PageInfo`, `ProcessedViolation`, `ServiceResult`, `AnalysisResult`, `SiteWideAccessibilityReport`

### Component Dependencies (NEW - Component-Based Architecture)

**`src/components/`** - **Shared UI Components**
- **Used by**: Web interface (`src/public/index.html`) and Storybook (`stories/`)
- **Pattern**: TypeScript components with render functions returning HTML strings
- **Purpose**: Single source of truth for UI components between web interface and Storybook

**Component Hierarchy**:
```
WebInterface.ts (Main Component)
├── Header.ts
├── ScanOptions.ts
├── ProgressSection.ts
├── ResultsSection.ts
├── ErrorSection.ts
└── Footer.ts
```

**Key Components**:
- **`Header.ts`**: Renders application header with title, subtitle, and version
- **`ScanOptions.ts`**: Renders scan configuration forms (full site, single page, regenerate)
- **`ProgressSection.ts`**: Renders real-time progress tracking with stages
- **`ResultsSection.ts`**: Renders scan results with statistics and actions
- **`ErrorSection.ts`**: Renders error states with retry options
- **`Footer.ts`**: Renders application footer with copyright and compliance info
- **`WebInterface.ts`**: Main component that combines all other components
- **`index.ts`**: Exports all components for easy importing

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

## 🧪 Testing Framework & Coverage

### Current Test Status (Phase 1-5 Complete)
- **Total Tests**: 301 tests passing, 0 failing
- **Coverage**: 100% success rate (Phase 1-5 target achieved)
- **Test Categories**: Unit tests (214), integration tests (47), component tests (9), E2E tests (ready for implementation)
- **Framework**: Jest with TypeScript support, Storybook for component testing, Playwright for E2E testing
- **Test Cleanup**: Comprehensive cleanup system for temporary files including HTML files from PDF generation
- **Component Testing**: Storybook with accessibility validation (4 components, WCAG 2.1 AA compliance)

### Test Dependencies & Patterns
```typescript
// ✅ CORRECT - Singleton pattern testing
const service1 = ErrorHandlerService.getInstance();
const service2 = ErrorHandlerService.getInstance();
expect(service1).toBe(service2); // Same instance

// ✅ CORRECT - Mocking external dependencies
const mockAxeResult: any = { violations: [] };
const mockPa11yResult: any = { issues: [] };

// ✅ CORRECT - Memory testing (avoid creating directories)
// Test memory usage without creating actual files
for (let i = 0; i < 1000; i++) {
  service.operation(); // Test operations, not file creation
}

// ❌ INCORRECT - Creating unnecessary test directories
for (let i = 0; i < 1000; i++) {
  fs.mkdirSync(`test-dir-${i}`); // Don't do this
}
```

### Test File Dependencies
- **`tests/setup.ts`**: Global test utilities and cleanup helpers
- **Unit Tests**: Test individual services and components in isolation
- **Integration Tests**: Test cross-service communication and workflows
- **E2E Tests**: Test complete user workflows and web interface functionality
- **Mocking Strategy**: Use `any` types for complex external dependencies

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