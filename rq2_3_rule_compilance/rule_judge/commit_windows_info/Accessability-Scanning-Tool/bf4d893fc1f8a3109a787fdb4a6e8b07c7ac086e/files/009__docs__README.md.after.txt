# 📚 Documentation Directory

This directory contains comprehensive documentation for the accessibility testing application, designed to help both human developers and AI tools understand and work with the codebase safely.

## 📋 Documentation Files

### 🤖 AI Development Support

- **[`AI_DEVELOPMENT_GUIDE.md`](AI_DEVELOPMENT_GUIDE.md)** - AI-specific development guidelines and critical rules
  - **Purpose**: Guide AI tools (Cursor, Copilot, etc.) to work safely with the codebase
  - **Contains**: Critical rules, common mistakes to avoid, development workflow
  - **When to use**: Before making any changes to the codebase

- **[`DEPENDENCY_MAP.md`](DEPENDENCY_MAP.md)** - Complete dependency relationships and import patterns
  - **Purpose**: Show all import relationships and dependencies between modules
  - **Contains**: Directory structure, critical files, import patterns, breaking change prevention
  - **When to use**: Understanding how modules interact, planning changes

- **[`ARCHITECTURE_DIAGRAM.md`](ARCHITECTURE_DIAGRAM.md)** - Visual system architecture and data flow
  - **Purpose**: Visual representation of system architecture and component relationships
  - **Contains**: ASCII diagrams, data flow patterns, service layer architecture
  - **When to use**: Understanding system design and data flow

- **[`QUICK_REFERENCE.md`](QUICK_REFERENCE.md)** - Fast reference for common operations and troubleshooting
  - **Purpose**: Quick answers to common questions and operations
  - **Contains**: Critical information, common operations, file locations, troubleshooting
  - **When to use**: Daily reference, quick lookups, troubleshooting issues

- **[`TESTING_ROADMAP.md`](TESTING_ROADMAP.md)** - Testing strategy and coverage plan
  - **Purpose**: Comprehensive testing roadmap and coverage targets
  - **Contains**: Current state assessment, 4-phase implementation plan, testing best practices
  - **When to use**: Understanding testing strategy, fixing tests, achieving coverage targets

### 📖 Project Documentation

- **[`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md)** - High-level project understanding
  - **Purpose**: Comprehensive overview of the accessibility testing application
  - **Contains**: Core features, key functionality, services, APIs, tools & frameworks
  - **When to use**: Understanding what the project does and how it works

- **[`DOCUMENTATION_SYSTEM.md`](DOCUMENTATION_SYSTEM.md)** - Complete documentation system overview
  - **Purpose**: Explain how the documentation system works and how AI tools use it
  - **Contains**: Problem solution, workflow, benefits, system components
  - **When to use**: Understanding how the documentation system prevents breaking changes

## 🎯 How to Use This Documentation

### For AI Tools (Cursor, Copilot, etc.)

1. **Start with** `AI_DEVELOPMENT_GUIDE.md` - Read this first before making any changes
2. **Check** `DEPENDENCY_MAP.md` - Understand dependencies and affected files
3. **Review** `ARCHITECTURE_DIAGRAM.md` - Understand data flow and system design
4. **Consult** `QUICK_REFERENCE.md` - For specific patterns and operations
5. **Update** relevant files after making changes (as specified in `.cursorrules`)

### For Human Developers

1. **New to the project**: Start with `PROJECT_OVERVIEW.md`
2. **Understanding structure**: Use `DEPENDENCY_MAP.md`
3. **System design**: Review `ARCHITECTURE_DIAGRAM.md`
4. **Daily reference**: Keep `QUICK_REFERENCE.md` handy
5. **Documentation maintenance**: Use `DOCUMENTATION_SYSTEM.md`

## 🔧 Documentation Maintenance

The documentation is automatically maintained through:

- **Pre-commit hooks** - Validate documentation consistency
- **NPM scripts** - Easy commands for documentation maintenance
- **Automated analysis** - Suggest updates based on code changes

### Available Commands

```bash
# Check if all reference files exist
npm run docs:check

# Analyze changes and suggest documentation updates
npm run docs:analyze

# Validate critical files exist
npm run docs:validate

# Run all documentation checks
npm run docs:all
```

## 🚨 Critical Information

### Most Important Files (DO NOT BREAK)
1. `src/core/types/common.ts` - All shared types and interfaces
2. `src/utils/services/error-handler-service.ts` - Central error handling
3. `src/utils/services/configuration-service.ts` - Configuration management
4. `src/cli/accessibility-test-cli.ts` - Main CLI entry point
5. `tests/` directory - Unit and integration tests
6. `jest.config.js` - Testing framework configuration

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
```

## 📊 Documentation Structure

```
docs/
├── README.md                    # This file - documentation overview
├── AI_DEVELOPMENT_GUIDE.md      # AI-specific guidelines
├── DEPENDENCY_MAP.md            # Dependency relationships
├── ARCHITECTURE_DIAGRAM.md      # Visual architecture
├── QUICK_REFERENCE.md           # Fast reference guide
├── PROJECT_OVERVIEW.md          # High-level understanding
├── TESTING_ROADMAP.md           # Testing strategy and coverage plan
└── DOCUMENTATION_SYSTEM.md      # System overview
```

## 🔄 Keeping Documentation Updated

### For New Services
- Add to `DEPENDENCY_MAP.md` service dependencies section
- Update `ARCHITECTURE_DIAGRAM.md` service layer diagram
- Add pattern to `QUICK_REFERENCE.md` common patterns section

### For New Types
- Add to `DEPENDENCY_MAP.md` core dependencies section
- Update `QUICK_REFERENCE.md` type definition patterns

### For New Imports
- Update `DEPENDENCY_MAP.md` import patterns section
- Verify consistency in `QUICK_REFERENCE.md`

### For Architecture Changes
- Update `ARCHITECTURE_DIAGRAM.md` relevant sections
- Update `DEPENDENCY_MAP.md` dependency relationships
- Update `AI_DEVELOPMENT_GUIDE.md` if patterns change

### For Testing Changes
- Update `TESTING_ROADMAP.md` with new test coverage information
- Update `DEPENDENCY_MAP.md` with test file dependencies
- Update `QUICK_REFERENCE.md` with testing patterns
- Update `AI_DEVELOPMENT_GUIDE.md` with testing rules

## 🎉 Benefits

This documentation system provides:

1. **Reduced Breaking Changes** - AI tools understand dependencies before making changes
2. **Consistent Documentation** - Automated maintenance ensures documentation stays updated
3. **Better AI Performance** - Comprehensive context and clear rules
4. **Easier Maintenance** - Automated tools reduce manual documentation work
5. **Protected Critical Files** - Validation ensures important files aren't broken

---

**Last Updated**: 18/12/2024 14:30 GMT
**Purpose**: Overview of documentation structure and usage 