# 🌐 Comprehensive Site-wide Accessibility Audit

<div align="center">
  <p><strong>Professional Accessibility Testing Solution</strong></p>
  <p>
    <img src="https://img.shields.io/badge/WCAG-2.1%20AA-1e214d?style=for-the-badge&logo=w3c&logoColor=white" alt="WCAG 2.1 AA" />
    <img src="https://img.shields.io/badge/Accessibility-Testing-db0064?style=for-the-badge&logo=universal-access&logoColor=white" alt="Accessibility Testing" />
    <img src="https://img.shields.io/badge/Automated-Reports-fcc700?style=for-the-badge&logo=documents&logoColor=white" alt="Automated Reports" />
  </p>
</div>

---

Automated accessibility testing system that crawls every accessible page on your
website and generates comprehensive WCAG 2.1 AA compliance reports using a
modern, modular architecture.

**Key Features:**

- 🎯 **Universal Testing**: Works with any website - no configuration needed
- 📊 **Comprehensive Reports**: Executive, research, and developer-focused
  outputs
- 🌐 **Modern Web Interface**: Interactive web-based testing with real-time progress
- 🎨 **Visual Analysis**: Screenshot capture and colour contrast validation
- 📱 **Multi-Tool Coverage**: axe-core + Pa11y combined
- 🏗️ **Modular Architecture**: Clean, maintainable service-based design

## 🚀 Getting Started

The modern web interface provides an intuitive, accessible way to run accessibility tests:

### Production Mode
```bash
# Build and start the web server
npm run build
npm start
```

### Development Mode (Recommended)
```bash
# Start development server with hot reload
npm run dev:setup
```

This will:
- Build the project if needed
- Start TypeScript compiler in watch mode
- Start the server with nodemon for automatic restarts
- Watch for changes in your source files

Then open your browser to: **http://localhost:3000**

### Alternative Development Commands
```bash
# Manual build and start
npm run dev:build

# Just start the watch mode (if already built)
npm run dev
```

**Features:**
- 🎨 Modern, responsive design with UK brand colours
- ♿ WCAG 2.1 AAA compliant interface
- 📱 Mobile-friendly design
- ⚡ Real-time progress tracking
- 📊 Interactive results display
- 🔄 Complete accessibility testing functionality

### 🎯 Simple 3-Step Process:

1. **🚀 Run Accessibility Audit**: Enter your website URL and start
   comprehensive testing (automatic cleanup included)
2. **📊 View Results**: Access detailed reports and historical data
3. **🚪 Exit**: Clean process termination

### ✨ What You Get:

- **🎯 Universal Testing**: Works with any website - no configuration needed
- **🔧 Smart Defaults**: Optimised settings for comprehensive accessibility
  analysis
- **📊 Professional Reports**: Detailed JSON data
- **🧪 Multi-Tool Analysis**: axe-core + Pa11y combined
- **🚀 Quick Results**: Comprehensive crawling (up to 50 pages, 4 levels deep)

### 🎯 Test Types Available:

The web interface offers these testing options:

1. **🧹 Full Site Audit** (recommended): Complete accessibility analysis of entire website
2. **🎯 Single Page Audit**: Focused testing of a specific page
3. **📊 Report Regeneration**: Regenerate reports from existing historical data

## 📦 Installation & Setup

### Prerequisites

Before running the accessibility testing application, ensure you have the
following installed:

- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org/)
- **npm**: Comes with Node.js (or use yarn/pnpm)
- **Git**: For cloning the repository

### Setup Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nimbleapproach/Accessability-Scanning-Tool.git
   cd Accessability-Scanning-Tool
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

   This will automatically install:
   - Playwright browsers (Chrome/Chromium)
   - TypeScript compilation tools
   - Accessibility testing libraries (axe-core, pa11y)

3. **Verify installation:**

   ```bash
   # Test web interface
   npm start
   # Then open http://localhost:3000
   ```

   The web interface should load successfully.

4. **Optional: Install Playwright browsers separately (if needed):**
   ```bash
   npx playwright install chromium
   ```

### First Run

After installation, you can immediately start testing:

```bash
npm start
# Open http://localhost:3000 in your browser
```

The web interface will guide you through:

- Entering your website URL
- Configuring test parameters (optional)
- Running comprehensive accessibility analysis
- Generating detailed reports

### Troubleshooting Setup

**Common Issues:**

- **Node.js version**: Ensure you're using Node.js 16 or higher
- **Permission errors**: Use `sudo` on macOS/Linux if needed for global installs
- **Browser installation**: Playwright will automatically install Chromium
- **Memory issues**: Ensure at least 4GB RAM available for testing

**Getting Help:**

- Check the console output for detailed error messages
- Ensure all dependencies installed successfully with `npm list`

## 🛠️ System Requirements

- **Node.js 16+**: Required for running the application
- **Playwright**: Automatically installed with dependencies
- **Chrome/Chromium**: Automatically installed by Playwright
- **Internet connection**: Required for website crawling
- **Memory**: 4GB+ recommended for optimal performance

**Development Dependencies** (automatically installed):

- TypeScript for type checking
- Pa11y for accessibility testing
- Axe-core for accessibility analysis

## ⚠️ Known Issues

✅ **There are currently no known issues.**

All previously reported issues have been resolved:

- **Memory Constraints**: Optimised for Chrome-only testing with improved
  stability
- **Process Hanging**: Clean exit mechanism implemented with automatic cleanup

## 🔄 Smart Redirect Handling

The system intelligently handles redirects to avoid duplicate testing:

1. **🕷️ Discovers** all pages through intelligent crawling
2. **📍 Detects** when a page redirects to another URL
3. **✅ Checks** if the redirect destination has already been tested
4. **⏭️ Skips** duplicate testing while tracking both original and final URLs
5. **📊 Reports** on actual tested pages with redirect information

**Example**: If `/old-page` redirects to `/new-page`, and `/new-page` was
already tested, the system will skip `/old-page` and mark it as processed,
saving time while maintaining comprehensive coverage.

## 📊 What It Does

1. **🕷️ Smart Site Crawling**: Automatically discovers up to 50 pages across
   your website (4 levels deep)
2. **🔄 Intelligent Redirect Handling**: Tests each unique page only once, even
   when redirects occur
3. **🌐 Chrome Browser Testing**: Optimised for Chrome/Chromium browser testing:
   - **Chrome Focus**: Comprehensive testing in Chrome browser for consistent
     results
   - **Memory Optimised**: Single-browser testing reduces memory usage and
     prevents crashes
4. **🧪 Multi-Tool Testing**: Runs comprehensive accessibility analysis using
   multiple complementary tools:
   - **axe-core**: Industry-standard accessibility testing engine (violations
     with detailed remediation)
   - **Pa11y**: Command-line testing with HTML_CodeSniffer (additional coverage
     and different perspective)
   - **Combined Results**: Merges findings to eliminate gaps and provide broader WCAG 2.1 AA coverage
5. **📄 Professional Reports**: Creates detailed JSON reports with:
   - **Executive Summary** with overall compliance percentage
   - **WCAG 2.1 AA Compliance Matrix** with Pass/Fail/Not Assessed status for
     each criterion
   - **Most Common Violations** across the entire site with browser information
   - **Aggregated Site Summary** with comprehensive violation breakdowns
   - **Remediation Recommendations** with priority levels

## 📈 Reports Generated

After each audit, you'll find reports in `accessibility-reports/`:

- **📄 JSON Report**: Detailed technical data with raw violation data and
  comprehensive accessibility information
- **📄 PDF Report**: Professional, brand-compliant report with executive
  summary and detailed findings
- **📊 Site-wide Aggregate Report**: Combines results from all tested pages
  into a single comprehensive overview
- **🗂️ Page-specific Reports**: Individual JSON files for each tested page
- **📸 Screenshots**: Visual evidence of accessibility violations (optional)
- **📄 Page List Cache**: Cached list of all discovered pages for faster re-runs

### 📁 Historical Data Management

The system intelligently manages historical audit data:

- **🔄 Automatic Cleanup**: Before each new audit, JSON files are moved to history and all existing PDF reports are deleted
- **📂 History Folder**: JSON files are automatically moved to `accessibility-reports/history/` for future reference
- **🧹 Clean Slate**: All existing PDF reports are deleted to provide a clean slate for new scan
- **🔄 Report Regeneration**: Historical JSON data can be used to regenerate PDF reports without re-running accessibility scans
- **📊 Data Preservation**: All audit data is preserved for trend analysis and historical comparison
- **📄 Fresh Reports**: New PDF reports are generated after each scan completes

## ⚙️ Configuration

### Configuration

The accessibility testing system uses intelligent defaults optimised for comprehensive coverage. Configuration is handled through the web interface and internal service settings.

### Universal Timeout Strategy

The system uses an **adaptive timeout strategy** that works for any website:

1. **First attempt**: Fast loading (`domcontentloaded`) with base timeout
2. **Second attempt**: Full resource loading (`load`) with 1.3x timeout
3. **Third attempt**: Network idle (`networkidle`) with 1.6x timeout

This approach handles:

- **Fast static sites**: Quick first-attempt success
- **Complex web apps**: Progressive fallback to more patient loading
- **Single Page Apps**: Final networkidle attempt for dynamic content



### Customise Target Website

The target website can be configured through the web interface. The system automatically adapts to any website without code changes required.

### ⏱️ Comprehensive Coverage Settings

The system prioritises **comprehensive coverage over speed** with these
settings:

- **Intelligent Crawling**: Site crawled with intelligent redirect handling
- **Multi-Tool Analysis**: Axe-core and Pa11y for comprehensive coverage
- **Screenshot Capture**: Visual documentation of accessibility violations
- **Comprehensive Analysis**: All issue types (errors, warnings, notices) included
- **Extended Crawling**: Up to 50 pages at depth 4 for thorough site discovery
- **Multi-Tool Coverage**: axe-core + Pa11y with all ruleset categories enabled

**Performance Optimisations**:

- **Parallel Processing**: Concurrent page analysis for efficiency
- **Smart Caching**: Page lists cached for improved performance
- **Modular Architecture**: Efficient service-based design reduces overhead
- **Real-time Updates**: WebSocket-based progress tracking

**Performance Trade-offs**: The audit provides maximum accessibility coverage with comprehensive multi-tool analysis.

## 🏗️ Architecture

### 🚀 Modular Service-Based Architecture

The system follows **SOLID principles** with a clean, maintainable architecture:

**🔧 Core Services**:

- **`ConfigurationService`**: Centralised configuration management
- **`ErrorHandlerService`**: Consistent error handling and logging
- **`FileOperationsService`**: File system operations and cleanup

**🧪 Test Runners**:

- **`AxeTestRunner`**: Focused axe-core accessibility testing
- **`Pa11yTestRunner`**: Dedicated Pa11y analysis execution

**⚙️ Processing Layer**:

- **`ViolationProcessor`**: Violation processing and merging from multiple tools
- **`PageAnalyzer`**: Page structure and accessibility feature analysis

**📄 PDF Generation**:

- **`PdfTemplateGenerator`**: HTML template generation for reports
- **`PdfOrchestrator`**: PDF creation and file management

**🎯 Orchestration**:

- **`AccessibilityTestOrchestrator`**: Main coordinator for all testing
  activities
- **`TestSetupUtil`**: Shared test utilities and setup

### 🚀 Web Interface Architecture

The system provides a modern web interface with real-time progress tracking and comprehensive accessibility testing:

**🌐 Web Server Features**:

- **Express.js Server**: RESTful API endpoints for accessibility testing
- **Socket.IO Integration**: Real-time progress updates during scans
- **Static File Serving**: Modern web interface with responsive design
- **Error Handling**: Comprehensive error handling and user feedback

**🔧 Analysis Components**:

- **Site Crawling**: Intelligent page discovery and caching
- **Multi-Tool Analysis**: Axe-core and Pa11y integration
- **Parallel Processing**: Concurrent page analysis for efficiency
- **Report Generation**: PDF and JSON report creation

**📊 Benefits**:

- **⚡ Real-time Updates**: Live progress tracking via WebSocket
- **🎯 Comprehensive Coverage**: Multi-tool accessibility analysis
- **🔧 Modern Interface**: Responsive web design with UK brand compliance
- **📄 Professional Reports**: Audience-specific PDF and JSON outputs
- **💾 Historical Data**: Intelligent file management with data preservation
- **🏗️ Maintainable Code**: Clean service-based architecture

**🏃‍♂️ Workflow**:

1. **Clean Start**: Automatic cleanup of previous reports (JSON moved to history, PDFs deleted)
2. **Site Crawling**: Discovers pages with intelligent redirect handling
3. **Accessibility Analysis**: Multi-tool testing with axe-core and Pa11y
4. **Report Generation**: Creates audience-specific PDF reports and detailed JSON data
5. **Historical Preservation**: JSON data preserved for future report regeneration
6. **Clean Exit**: Automatic process cleanup and termination

## 🛠️ Code Quality & Development Tools

The project includes comprehensive code quality tools and documentation
standards:

### 📝 Documentation Standards

- **CHANGELOG Tracking**: Every chat prompt automatically logged with timestamp
  and description
- **README Maintenance**: Systematic updates based on change type:
  - New features → Getting Started, What It Does, Reports Generated sections
  - CLI changes → Getting Started section updates
  - Configuration changes → Configuration section updates
  - Architecture changes → Architecture and System Requirements sections
  - Setup changes → Installation & Setup section updates
- **UK Standards**: British spelling, date formats (DD/MM/YYYY), and GMT/BST
  timezone usage
- **Accessibility Compliance**: All documentation meets WCAG 2.1 AA standards

### 🤖 AI Development Support

The project includes comprehensive reference documentation to help AI tools
(Cursor, GitHub Copilot, etc.) understand the codebase and prevent breaking
changes:

#### 📚 Reference Documentation Files

- **`docs/AI_DEVELOPMENT_GUIDE.md`** - AI-specific development guidelines and critical rules
- **`docs/DEPENDENCY_MAP.md`** - Complete dependency relationships and import patterns
- **`docs/ARCHITECTURE_DIAGRAM.md`** - Visual system architecture and data flow
- **`docs/QUICK_REFERENCE.md`** - Fast reference for common operations and troubleshooting
- **`docs/PROJECT_OVERVIEW.md`** - High-level project understanding

#### 🔧 Documentation Maintenance

The project includes automated tools to maintain documentation consistency:

```bash
# Check if all reference files exist
npm run docs:check

# Analyze changes and suggest documentation updates
npm run docs:analyze

# Validate critical files exist
npm run docs:validate

# Run all documentation checks
npm run docs:all

# Show documentation script help
npm run docs:help
```

#### 🚨 Critical Development Rules

AI tools must follow these rules to prevent breaking changes:

1. **Singleton Services**: Always use `getInstance()` pattern
2. **Import Patterns**: Use `@/` alias for `src/` imports
3. **Error Handling**: Always use `ErrorHandlerService`
4. **Configuration**: Always use `ConfigurationService`
5. **Documentation Updates**: Update reference files after changes

#### 🔄 Development Workflow

The development workflow includes:
- Documentation consistency checks
- TypeScript compilation validation
- Automated testing with Playwright
- Comprehensive error handling

### 📖 Documentation

See `LINTING.md` for detailed configuration and troubleshooting information.

## 📋 What Gets Tested

### 🔧 Multi-Tool Coverage

Each page is analysed by **four complementary tools** to ensure comprehensive
coverage:

**axe-core Detection (Primary Engine):**

- ✅ **Colour Contrast**: WCAG AA compliance ratios
- ✅ **ARIA Implementation**: Labels, roles, and properties
- ✅ **Keyboard Navigation**: Focus management and tab order
- ✅ **Form Accessibility**: Labels and validation
- ✅ **Image Alt Text**: Alternative text for images
- ✅ **Heading Structure**: Logical heading hierarchy
- ✅ **Focus Management**: Visible focus indicators
- ✅ **Interactive Elements**: Button and link accessibility
- ✅ **WCAG 2.1 AA**: Current accessibility standards compliance
- ✅ **EN 301 549**: European accessibility requirements
- ✅ **Best Practices**: Industry-standard recommendations
- ✅ **Experimental Rules**: Cutting-edge accessibility tests

**Pa11y Additional Coverage (HTML_CodeSniffer):**

- ✅ **HTML Structure**: Semantic markup validation
- ✅ **Content Organisation**: Document structure and landmarks
- ✅ **Text Alternatives**: Comprehensive alt text analysis
- ✅ **Language Attributes**: Proper language declarations
- ✅ **Document Outline**: Heading hierarchy validation
- ✅ **Table Structure**: Data table accessibility
- ✅ **Link Context**: Link purpose and context
- ✅ **Best Practice Notices**: Additional improvement recommendations
- ✅ **Extended Analysis**: 2-minute per-page analysis with content loading
  waits

**Visual Analysis**:

- ✅ **Screenshot Capture**: Comprehensive screenshot capture of all
  accessibility violations
- ✅ **Colour Contrast**: Advanced colour contrast validation using
  Playwright's built-in colour contrast checker

### 🎯 Combined Benefits

- **Maximum Coverage**: Comprehensive analysis prioritises thoroughness over
  speed with 4-tool validation
- **Broader Detection**: Four different engines catch different violation types
  and edge cases
- **Reduced False Negatives**: Issues missed by one tool are caught by others
  - **Multiple Testing Approaches**: DOM-based (axe), HTML parsing (Pa11y)
- **All Issue Types**: Includes errors, warnings, notices, and enterprise-level
  insights
- **Enhanced Confidence**: Quadruple tool validation maximizes reliability
- **Professional Standards**: Industry-leading tools for comprehensive
  compliance
- **Deep Analysis**: Extended timeouts and comprehensive rulesets ensure
  thorough testing

## 🎯 Results Interpretation

- **🏆 100% Compliance**: Fully accessible website
- **👍 80%+ Compliance**: Good accessibility with minor issues
- **🔧 <80% Compliance**: Significant improvements needed

## 🛠️ Developer Fix Guide

The system generates **three audience-specific PDF reports** tailored to
different roles:

### 📊 Product Owners & Stakeholders

- **Focus**: Business impact, risk assessment, and ROI
- **Size**: ~300KB - Executive summary optimised for decision makers
- **Content**: Compliance overview, implementation timeline, cost estimates

### 🔬 User Researchers & UCD

- **Focus**: User impact analysis and testing methodology
- **Size**: ~400KB - Research-focused insights and testing guidance
- **Content**: User journey analysis, testing scenarios, research
  recommendations

### 💻 Developers & Testers

- **Focus**: Technical implementation and code fixes
- **Size**: ~2MB - Comprehensive technical guide with visual elements
- **Content**: Complete Developer Fix Guide with condensed affected locations
  table

The comprehensive **Developer Fix Guide** (in the Developers & Testers report)
makes fixing accessibility violations straightforward:

### 📸 Visual Context

- **Element Screenshots**: See exactly what element is failing
- **Precise Location**: CSS selectors and coordinates for easy targeting

### 💻 Code Solutions

- **Current Code**: The problematic HTML causing the violation
- **Suggested Fix**: Specific code changes to resolve the issue
- **Smart Suggestions**: Violation-specific fixes for common issues like:
  - Missing alt text for images
  - Insufficient colour contrast
  - Missing form labels
  - Incorrect heading hierarchy
  - Missing viewport meta tags

### 📍 Context & Prioritisation

- **Page Information**: Exact URL and page title
- **Impact Level**: Critical, Serious, Moderate, or Minor
- **Priority & Effort**: Development team planning information
- **WCAG References**: Relevant guidelines and conformance levels

### 🎯 Example Fix Suggestions

**Missing Alt Text**:

```html
<!-- Before -->
<img src="logo.png" />

<!-- After -->
<img src="logo.png" alt="Company Logo" />
```

**Colour Contrast Issues**:

```css
/* Fix: Use colors with proper WCAG AA contrast ratios */
.button {
  color: #212529; /* Dark gray - 4.5:1 contrast ratio */
  background: #fff;
  border: 2px solid #212529;
}

.button:hover {
  color: #fff;
  background: #212529;
}

.button.primary {
  color: #fff;
  background: #0d6efd; /* Blue - meets WCAG AA standards */
}

.button.success {
  color: #fff;
  background: #198754; /* Green - meets WCAG AA standards */
}

.button.warning {
  color: #000;
  background: #ffc107; /* Yellow - meets WCAG AA standards */
}

.button.danger {
  color: #fff;
  background: #dc3545; /* Red - meets WCAG AA standards */
}
```

**Missing Form Labels**:

```html
<!-- Before -->
<input type="email" />

<!-- After -->
<label for="email">Email Address</label>
<input type="email" id="email" />
```

---

<div align="center">
  <h3>🎯 Ready to Test Your Website?</h3>
  <p>Get started with our modern web interface in under 2 minutes:</p>
  
  ```bash
  npm start
  # Then open http://localhost:3000
  ```
  
  <p>
    <img src="https://img.shields.io/badge/Node.js-16%2B-1e214d?style=flat-square&logo=node.js&logoColor=white" alt="Node.js 16+" />
    <img src="https://img.shields.io/badge/TypeScript-Ready-db0064?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript Ready" />
    <img src="https://img.shields.io/badge/Playwright-Powered-fcc700?style=flat-square&logo=playwright&logoColor=1e214d" alt="Playwright Powered" />
  </p>
  
  <p><em>Professional accessibility testing made simple</em></p>
</div>

---

## 🚀 Implementation Roadmap & Action Plan

1. **Enhanced Testing Coverage**
   - Expand Playwright test suite for comprehensive validation
   - **Priority**: MEDIUM - Important for maintaining code quality standards
