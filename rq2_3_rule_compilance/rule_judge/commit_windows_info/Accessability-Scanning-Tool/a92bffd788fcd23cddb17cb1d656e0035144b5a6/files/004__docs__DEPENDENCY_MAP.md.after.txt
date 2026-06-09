# Dependency Map

## 📋 **Overview**

This document provides a comprehensive mapping of all dependencies, imports, and relationships within the accessibility testing application. It serves as a reference for understanding the codebase structure and maintaining consistency.

**Last Updated**: 24/01/2025 10:45 GMT  
**Status**: ✅ **CURRENT** - All issues resolved, 100% test success rate achieved, complete component coverage implemented, progress section fixes completed

---

## 🔗 **Import Patterns**

### **✅ Standardized Import Patterns** (Phase 1.1 Completed)

All imports now use the `@/` alias pattern as defined in `tsconfig.json`:

```typescript
// ✅ CORRECT - Use @/ alias
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { ServiceResult } from '@/core/types/common';

// ❌ INCORRECT - Relative imports (FIXED)
import { ErrorHandlerService } from '../services/error-handler-service';
import { ConfigurationService } from '../../utils/services/configuration-service';
```

### **Files Updated** (Phase 1.1 - ✅ **COMPLETED**)

**Core Files**:
- `src/core/utils/browser-manager.ts` - ✅ Updated to `@/` alias
- `src/web/server.ts` - ✅ Updated to `@/` alias

**Service Files**:
- `src/utils/services/error-handler-service.ts` - ✅ Already using correct pattern
- `src/utils/services/configuration-service.ts` - ✅ Already using correct pattern
- `src/utils/services/database-service.ts` - ✅ Already using correct pattern
- `src/utils/services/file-operations-service.ts` - ✅ Already using correct pattern
- `src/utils/services/security-validation-service.ts` - ✅ Already using correct pattern

**Utility Files**:
- `src/utils/crawler/site-crawler.ts` - ✅ Updated to `@/` alias
- `src/utils/runners/axe-test-runner.ts` - ✅ Updated to `@/` alias
- `src/utils/runners/pa11y-test-runner.ts` - ✅ Updated to `@/` alias
- `src/utils/api/analysis-service.ts` - ✅ Updated to `@/` alias
- `src/utils/analyzers/page-analyzer.ts` - ✅ Updated to `@/` alias

**Orchestration Files**:
- `src/utils/orchestration/accessibility-test-orchestrator.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/analysis-cache.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/task-queue.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/smart-batcher.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/workflow-orchestrator.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/parallel-analyzer.ts` - ✅ Updated to `@/` alias
- `src/utils/orchestration/metrics-calculator.ts` - ✅ **NEW** - Utility class for metrics calculation
- `src/utils/orchestration/site-crawling-orchestrator.ts` - ✅ **NEW** - Site crawling coordination class
- `src/utils/orchestration/analysis-orchestrator.ts` - ✅ **NEW** - Accessibility analysis coordination class
- `src/utils/orchestration/report-generation-orchestrator.ts` - ✅ **NEW** - Report generation coordination class

**Processing Files**:
- `src/utils/processors/violation-processor.ts` - ✅ Updated to `@/` alias

**Analysis Files**:
- `src/utils/analysis/accessibility-tool.ts` - ✅ Updated to `@/` alias

### **✅ Issues Resolved** (Phase 1.2 - **COMPLETED**)

**TypeScript Compilation Errors**: All 169 errors resolved
- ✅ **Missing Type Definitions**: `@types/node`, `@types/events` installed
- ✅ **Incorrect Playwright Imports**: Updated to use `@playwright/test`
- ✅ **Missing Package Type Declarations**: All type definitions added

**Files with Import Issues**:
- ✅ All files using correct Playwright import paths
- ✅ All files have Node.js type definitions
- ✅ All files have event emitter type definitions

### **✅ Recent Error Handling Improvements** (Latest Updates)

**Critical Runtime Issues Fixed**:

**PDF Generation Safety**:
- ✅ `src/utils/reporting/pdf-generators/pdf-template-generator.ts` - Added null checks for all summary properties
- ✅ `generateStakeholderContent()` - Safe handling of `mostCommonViolations`
- ✅ `generateResearcherContent()` - Safe handling of undefined violation arrays
- ✅ `generateDeveloperContent()` - Added null checks for all summary properties
- ✅ `generatePriorityMatrix()` - Safe handling of undefined violations
- ✅ `getViolationsByImpact()` - Added null check for mostCommonViolations

**Browser Navigation Resilience**:
- ✅ `src/core/utils/browser-manager.ts` - Enhanced `navigateToUrl()` with retry logic
- ✅ Added specific handling for `net::ERR_ABORTED` errors
- ✅ Implemented retry logic with more lenient settings
- ✅ Added proper TypeScript error typing for all error handlers
- ✅ Improved logging and error context for debugging

**Directory Creation Safety**:
- ✅ `src/utils/orchestration/workflow-orchestrator.ts` - Added automatic directory creation
- ✅ Ensures `accessibility-reports` directory exists before writing files

### **✅ E2E Testing Infrastructure** (Latest Enhancement)

**New Test Infrastructure**:
- ✅ `scripts/check-dev-server.js` - **NEW** - Server check and startup script
- ✅ `tests/e2e/pages/FullSiteScanPage.ts` - **NEW** - Page object for full site scan
- ✅ `tests/e2e/pages/SinglePageScanPage.ts` - **NEW** - Page object for single page scan
- ✅ `tests/e2e/full-site-scan.test.ts` - **NEW** - E2E tests for full site scan (7 tests)
- ✅ `tests/e2e/single-page-scan.test.ts` - **NEW** - E2E tests for single page scan (7 tests)

**Updated Test Infrastructure**:
- ✅ `playwright.config.ts` - Updated to use local development server
- ✅ `tests/e2e/setup/test-setup.ts` - Added page-specific setup functions
- ✅ `tests/e2e/pages/HomePage.ts` - Updated for landing page structure
- ✅ `tests/e2e/pages/index.ts` - Added new page object exports

**Test Dependencies**:
- ✅ E2E tests now use full development server (including MongoDB)
- ✅ Automatic server startup and health checking
- ✅ Page object model for different scan pages
- ✅ Proper navigation to `/full-site` and `/single-page` routes

**TypeScript Error Handling**:
- ✅ Fixed all TypeScript errors related to unknown error types
- ✅ Proper error typing throughout the codebase
- ✅ Enhanced error context and logging

---

## 🏗️ **Service Dependencies**

### **Core Services** (Singleton Pattern)

```typescript
// ✅ CORRECT - Use getInstance()
const errorHandler = ErrorHandlerService.getInstance();
const configService = ConfigurationService.getInstance();
const databaseService = DatabaseService.getInstance();
const fileOps = FileOperationsService.getInstance();
const securityService = SecurityValidationService.getInstance();

// ❌ INCORRECT - Direct instantiation (PREVENTED)
const errorHandler = new ErrorHandlerService(); // Throws error
```

### **Service Relationships**

```
ErrorHandlerService
├── Used by: ALL services and utilities
├── Dependencies: None (base service)
└── Pattern: Singleton

ConfigurationService
├── Used by: ALL services and utilities
├── Dependencies: ErrorHandlerService
└── Pattern: Singleton

DatabaseService
├── Used by: WorkflowOrchestrator, WebServer
├── Dependencies: ErrorHandlerService, ConfigurationService
└── Pattern: Singleton

FileOperationsService
├── Used by: WorkflowOrchestrator, AnalysisCache
├── Dependencies: ErrorHandlerService, ConfigurationService
└── Pattern: Singleton

SecurityValidationService
├── Used by: SiteCrawler, WebServer
├── Dependencies: ErrorHandlerService, ConfigurationService
└── Pattern: Singleton

MetricsCalculator
├── Used by: WorkflowOrchestrator, DataTransformer
├── Dependencies: None (pure utility class)
└── Pattern: Utility Class

DataTransformer
├── Used by: WorkflowOrchestrator, ReportGenerationOrchestrator
├── Dependencies: MetricsCalculator
└── Pattern: Utility Class

SiteCrawlingOrchestrator
├── Used by: WorkflowOrchestrator
├── Dependencies: BrowserManager, ErrorHandlerService, MetricsCalculator
└── Pattern: Orchestrator Class

AnalysisOrchestrator
├── Used by: WorkflowOrchestrator
├── Dependencies: ParallelAnalyzer, ErrorHandlerService, MetricsCalculator
└── Pattern: Orchestrator Class

ReportGenerationOrchestrator
├── Used by: WorkflowOrchestrator
├── Dependencies: DatabaseService, ErrorHandlerService, MetricsCalculator
└── Pattern: Orchestrator Class

---

## 🔧 **Core Dependencies**

### **Type Definitions** (Phase 1.2 - **NEEDS FIXING**)

```typescript
// ✅ CORRECT - Core types
import { ServiceResult, AnalysisResult, PageInfo } from '@/core/types/common';

// ❌ INCORRECT - Missing type definitions (NEEDS FIXING)
import { EventEmitter } from 'events'; // Missing @types/events
import * as fs from 'fs'; // Missing @types/node
```

### **External Libraries**

```typescript
// ✅ CORRECT - External libraries
import express from 'express';
import { Server as SocketIOServer } from 'socket.io';
import { chromium, Page } from '@playwright/test'; // ✅ Correct Playwright import

// ❌ INCORRECT - Wrong Playwright import (NEEDS FIXING)
import { Page } from 'playwright'; // Should be @playwright/test
```

---

## 📦 **Package Dependencies**

### **Production Dependencies**

```json
{
  "@axe-core/playwright": "^4.9.1",
  "@playwright/test": "^1.46.1",
  "axe-core": "^4.9.1",
  "body-parser": "^1.20.2",
  "cors": "^2.8.5",
  "dotenv": "^17.2.0",
  "express": "^4.18.2",
  "mongodb": "^6.17.0",
  "mongoose": "^8.16.4", // ⚠️ UNUSED - Remove in Phase 1.3
  "pa11y": "^9.0.0",
  "puppeteer": "^24.14.0", // ⚠️ UNUSED - Remove in Phase 1.3
  "socket.io": "^4.7.2"
}
```

### **Development Dependencies**

```json
{
  "@types/body-parser": "^1.19.5",
  "@types/cors": "^2.8.17",
  "@types/express": "^4.17.21",
  "@types/jest": "^29.5.12",
  "@types/pa11y": "^5.3.7",
  "@types/supertest": "^6.0.3",
  // ⚠️ MISSING - Add in Phase 1.2
  // "@types/node": "^20.0.0",
  // "@types/events": "^3.0.0",
  "concurrently": "^9.2.0",
  "jest": "^29.7.0",
  "nodemon": "^3.1.10",
  "rimraf": "^6.0.1",
  "socket.io-client": "^4.8.1",
  "supertest": "^7.1.3",
  "ts-jest": "^29.1.2",
  "ts-loader": "^9.5.2",
  "tsc-alias": "^1.8.16",
  "typescript": "^5.5.4"
}
```

---

## 🧪 **Test Dependencies**

### **Test File Structure**

```
tests/
├── unit/ (210 tests)
│   ├── services/ - Service unit tests
│   ├── runners/ - Test runner unit tests
│   ├── processors/ - Violation processor tests
│   └── core/ - Core type tests
├── integration/ (70 tests)
│   ├── api/ - API endpoint tests
│   ├── services/ - Service integration tests
│   └── websocket/ - WebSocket tests
├── e2e/ (26 tests)
│   ├── accessibility-scanning.test.ts
│   ├── interface-accessibility.test.ts
│   └── performance.test.ts
└── storybook/ (9 tests)
    └── storybook-validation.test.ts
```

### **Test Import Patterns**

```typescript
// ✅ CORRECT - Test imports
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

// ✅ CORRECT - Test utilities
import { TestUtils } from '@/tests/e2e/utils/TestUtils';
```

---

## 🔄 **Breaking Change Prevention**

### **Import Pattern Rules**

1. **ALWAYS use `@/` alias** for imports from `src/`
2. **NEVER use relative imports** (`../`, `../../`)
3. **ALWAYS use `getInstance()`** for services
4. **NEVER use `new Service()`** for singleton services

### **TypeScript Configuration**

```json
{
  "compilerOptions": {
    "baseUrl": "./src",
    "paths": {
      "@/*": ["./*"],
      "@/utils/*": ["utils/*"],
      "@/core/*": ["core/*"]
    }
  }
}
```

### **Validation Scripts**

```bash
# Check import patterns
npm run typecheck

# Check for relative imports
grep -r "import.*\.\./" src/

# Check for direct service instantiation
grep -r "new.*Service" src/
```

---

## ✅ **Issues Resolved** (Phase 1.2 & 1.3 - **COMPLETED**)

### **TypeScript Compilation Errors** ✅ **RESOLVED**

**Missing Type Definitions**:
- ✅ `@types/node` - Required for Node.js built-in modules
- ✅ `@types/events` - Required for EventEmitter

**Incorrect Playwright Imports**:
- ✅ All files using `import { Page } from '@playwright/test'`
- ✅ All Playwright imports updated to use correct package

**Missing Package Type Declarations**:
- ✅ All packages have proper type definitions
- ✅ No packages have implicit `any` types

### **Unused Dependencies** ✅ **RESOLVED**

**Dependencies Removed**:
- ✅ `mongoose` - No imports found in codebase
- ✅ `puppeteer` - No imports found in codebase

**Impact**: Reduced package bloat and potential security risks

---

## 📊 **Dependency Metrics**

### **Current Status**
- **Total Files**: 84 active code files
- **Import Patterns**: ✅ All standardized to `@/` alias
- **Service Pattern**: ✅ All services use singleton pattern
- **TypeScript Errors**: ✅ 0 compilation errors (all resolved)
- **Unused Dependencies**: ✅ 0 unused packages (all removed)

### **Quality Metrics**
- **Import Consistency**: 100% (all files use `@/` alias)
- **Service Pattern Compliance**: 100% (all services use singleton)
- **Type Safety**: ✅ Excellent (all type definitions present)
- **Dependency Efficiency**: ✅ Excellent (no unused packages)

---

## 🎯 **Next Steps**

### **Phase 1.2: TypeScript Compilation Fixes** ✅ **COMPLETED**
1. ✅ Installed missing type definitions (`@types/node`, `@types/events`)
2. ✅ Fixed Playwright import paths (use `@playwright/test`)
3. ✅ Added missing type declarations for various packages
4. ✅ Verified TypeScript compilation passes (0 errors)

### **Phase 1.3: Dependency Cleanup** ✅ **COMPLETED**
1. ✅ Removed `mongoose` from `package.json`
2. ✅ Removed `puppeteer` from `package.json`
3. ✅ Ran `npm install` to update lock file
4. ✅ Verified no functionality is broken

### **Phase 1.4: Code Quality Verification** ✅ **COMPLETED**
1. ✅ Verified singleton pattern compliance
2. ✅ Checked error handling patterns
3. ✅ Validated configuration service usage
4. ✅ Reviewed TypeScript type safety

---

**Last Updated**: 23/01/2025 18:00 GMT  
**Status**: ✅ **CURRENT** - All issues resolved, documentation updated  
**Next Review**: After next major feature addition 

## Orchestration Layer Dependencies

### Core Orchestrators
- **WorkflowOrchestrator** (`src/utils/orchestration/workflow-orchestrator.ts`)
  - **Dependencies:**
    - `SiteCrawlingOrchestrator` - Site crawling operations
    - `AnalysisOrchestrator` - Accessibility analysis operations
    - `ReportGenerationOrchestrator` - Report generation operations
    - `MetricsCalculator` - Workflow metrics calculation
    - `BrowserManager` - Browser management
    - `ErrorHandlerService` - Error handling
    - `ConfigurationService` - Configuration management
    - `DatabaseService` - Database operations
    - `ParallelAnalyzer` - Parallel analysis coordination
  - **Responsibilities:**
    - High-level workflow coordination
    - Delegation to specialized orchestrators
    - Backward compatibility maintenance
    - Overall audit lifecycle management

- **SiteCrawlingOrchestrator** (`src/utils/orchestration/site-crawling-orchestrator.ts`)
  - **Dependencies:**
    - `BrowserManager` - Browser management
    - `ErrorHandlerService` - Error handling
    - `SiteCrawler` - Site crawling logic
  - **Responsibilities:**
    - Site crawling coordination
    - Page discovery and validation
    - Crawl result processing

- **AnalysisOrchestrator** (`src/utils/orchestration/analysis-orchestrator.ts`)
  - **Dependencies:**
    - `ParallelAnalyzer` - Parallel analysis coordination
    - `ErrorHandlerService` - Error handling
    - `AccessibilityTool` - Accessibility testing tools
    - `ToolOrchestrator` - Tool coordination
  - **Responsibilities:**
    - Accessibility analysis coordination
    - Parallel processing management
    - Analysis result aggregation

- **ReportGenerationOrchestrator** (`src/utils/orchestration/report-generation-orchestrator.ts`)
  - **Dependencies:**
    - `DatabaseService` - Database operations
    - `ErrorHandlerService` - Error handling
    - `PdfOrchestrator` - PDF generation
    - `FileOperationsService` - File operations
  - **Responsibilities:**
    - Report generation coordination
    - Database and PDF report creation
    - Report validation and quality checks

- **MetricsCalculator** (`src/utils/orchestration/metrics-calculator.ts`)
  - **Dependencies:**
    - `PageInfo` - Page information types
    - `AnalysisResult` - Analysis result types
  - **Responsibilities:**
    - Workflow metrics calculation
    - Performance analysis
    - Success rate calculations

## Test Coverage Dependencies

### New Test Files Added
- **MetricsCalculator Tests** (`tests/unit/orchestration/metrics-calculator.test.ts`)
  - **Dependencies:**
    - `MetricsCalculator` - Main class under test
    - `ProcessedViolation` - Mock violation data
    - `AnalysisResult` - Mock analysis results
    - `PageInfo` - Mock page information
  - **Coverage:**
    - Workflow metrics calculation
    - Compliance metrics calculation
    - Violation pattern analysis
    - Performance reporting

- **DataTransformer Tests** (`tests/unit/orchestration/data-transformer.test.ts`)
  - **Dependencies:**
    - `DataTransformer` - Main class under test
    - `SiteWideAccessibilityReport` - Mock report data
    - `ProcessedViolation` - Mock violation data
    - `AnalysisResult` - Mock analysis results
  - **Coverage:**
    - Data transformation methods
    - WCAG compliance matrix generation
    - Violation aggregation
    - PDF data preparation

- **PDF Orchestrator Tests** (`tests/unit/reporting/pdf-orchestrator.test.ts`)
  - **Dependencies:**
    - `PdfOrchestrator` - Main class under test
    - `@playwright/test` - Mocked Playwright components
    - `SiteWideAccessibilityReport` - Mock report data
  - **Coverage:**
    - PDF generation functionality
    - Audience targeting
    - Error handling
    - Custom configuration options

## Integration Test Dependencies

### Integration Test Suite Overview
- **Total Tests**: 103 integration tests (99% success rate)
- **Test Suites**: 9 integration test suites
- **Coverage**: 11.68% statement coverage, 5.91% branch coverage

### Integration Test Files
- **Services Integration** (`tests/integration/services-integration.test.ts`)
  - **Dependencies:**
    - `ErrorHandlerService` - Error handling service
    - `ConfigurationService` - Configuration service
    - `SecurityValidationService` - Security validation service
    - `FileOperationsService` - File operations service
  - **Coverage:**
    - Singleton pattern verification
    - Error handling integration
    - Configuration management
    - Security validation
    - File operations
    - Cross-service communication

- **API Integration** (`tests/integration/api/web-server-api.test.ts`)
  - **Dependencies:**
    - `WebServer` - Main web server class
    - `supertest` - HTTP testing library
    - `ErrorHandlerService` - Error handling
    - `ConfigurationService` - Configuration management
  - **Coverage:**
    - Health check endpoints
    - Full site scan endpoints
    - Single page scan endpoints
    - Report generation endpoints
    - CORS and headers
    - Request validation

- **WebSocket Integration** (`tests/integration/websocket/websocket-integration.test.ts`)
  - **Dependencies:**
    - `WebServer` - WebSocket server
    - `socket.io-client` - WebSocket client
    - `ErrorHandlerService` - Error handling
  - **Coverage:**
    - WebSocket connection management
    - Scan room management
    - Progress update communication
    - Real-time scan workflow
    - Error handling and edge cases
    - Performance and scalability

- **Service Integration** (`tests/integration/services/service-integration.test.ts`)
  - **Dependencies:**
    - All service classes - Service integration testing
    - `ErrorHandlerService` - Error handling
    - `ConfigurationService` - Configuration management
  - **Coverage:**
    - Multi-service workflow integration
    - Error recovery and resilience
    - Performance and resource management
    - Configuration persistence and recovery 