# 🌐 Comprehensive Site-wide Accessibility Audit

<div align="center">
  <p><strong>Professional Accessibility Testing Solution</strong></p>
  <p>
    <img src="https://img.shields.io/badge/WCAG-2.1%20AAA-1e214d?style=for-the-badge&logo=w3c&logoColor=white" alt="WCAG 2.1 AAA" />
    <img src="https://img.shields.io/badge/Accessibility-Testing-db0064?style=for-the-badge&logo=universal-access&logoColor=white" alt="Accessibility Testing" />
    <img src="https://img.shields.io/badge/Automated-Reports-fcc700?style=for-the-badge&logo=documents&logoColor=white" alt="Automated Reports" />
    <img src="https://img.shields.io/badge/E2E%20Tests-40%2B%20Tests-28a745?style=for-the-badge&logo=test&logoColor=white" alt="40+ Tests" />
  </p>
</div>

---

Automated accessibility testing system that crawls every accessible page on your
website and generates comprehensive WCAG 2.1 AAA compliance reports using a
modern, modular architecture.

**Key Features:**

- 🎯 **Universal Testing**: Works with any website - no configuration needed
- 📊 **Comprehensive Reports**: Executive, research, and developer-focused
  outputs
- 🌐 **Modern Web Interface**: Interactive web-based testing with real-time progress
- 🎨 **Visual Analysis**: Screenshot capture and colour contrast validation
- 📱 **Multi-Tool Coverage**: axe-core + Pa11y combined
- 🏗️ **Modular Architecture**: Clean, maintainable service-based design
- ♿ **WCAG 2.1 AAA Compliant**: Interface meets highest accessibility standards

## 🚀 Getting Started

### Prerequisites

- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 8.0.0 or higher
- **Git**: For version control
- **Docker and Docker Compose** (for local MongoDB development)

### Installation & Setup

#### Quick Start with Local MongoDB

```bash
# Clone the repository
git clone https://github.com/nimbleapproach/Accessability-Scanning-Tool.git
cd Accessability-Scanning-Tool

# Install dependencies
npm install

# Generate secure secrets for local development
npm run secrets:generate

# Validate environment configuration (optional but recommended)
npm run validate:env

# Start everything together (recommended)
npm run dev:full
```

This will:
- Generate secure secrets for MongoDB
- Create a `.env.local` file with all necessary environment variables
- Validate environment configuration for correctness
- Start the complete MongoDB stack (MongoDB, Mongo Express)
- Wait for all services to be ready
- Auto-populate environment configuration
- Build the application
- Start the development server
- Open the web interface at [http://localhost:3000](http://localhost:3000)

#### Manual Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/nimbleapproach/Accessability-Scanning-Tool.git
   cd Accessability-Scanning-Tool
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the application**:
   ```bash
   npm run build
   ```

4. **Start the web interface**:
   ```bash
   npm start
   ```

5. **Access the interface**: Open [http://localhost:3000](http://localhost:3000) in your browser

### Development Mode

For development with hot reloading:

```bash
# Start everything together (recommended)
npm run dev:full

# Alternative commands:
npm run dev:start     # Same as dev:full
npm run dev:mongodb-only  # Start database only
npm run dev:app-only       # Start app only (requires DB to be running)

# Legacy commands (still work):
npm run dev:setup:mongodb  # Old setup command
npm run dev:setup:no-mongodb  # Without MongoDB
npm run dev                 # Standard development mode
```

This starts both TypeScript compilation in watch mode and the web server with nodemon.

### Local MongoDB Development

For local development with a full MongoDB instance:

```bash
# Start local MongoDB instance
npm run mongodb:start

# Check MongoDB status
npm run mongodb:status

# View MongoDB logs
npm run mongodb:logs

# Stop MongoDB
npm run mongodb:stop

# Reset MongoDB (delete all data)
npm run mongodb:reset
```

**Local MongoDB Services:**
- **MongoDB Database**: `localhost:27017` (admin/password123)
- **Mongo Express (Web UI)**: `http://localhost:8081` (admin/password123)

### Environment Validation

The project includes automatic environment file validation to ensure your local development setup is correct:

```bash
# Validate environment configuration
npm run validate:env

# Show validation help
npm run validate:env:help
```

**What the validation checks:**
- ✅ Required environment variables are present
- ✅ No placeholder values (e.g., `your_mongodb_url_here`)
- ✅ Proper variable formatting and syntax
- ✅ Consistency between related variables (e.g., database URLs)
- ✅ Valid port configurations
- ✅ No duplicate variables

**Automatic validation:**
- Environment validation runs automatically before starting MongoDB or the development server
- If validation fails, the startup process will stop and show detailed error messages
- The validation provides specific suggestions for fixing any issues found

**Example validation output:**
```bash
✅ Environment file validation passed!
ℹ️ Found 18 variables
✅ No fixes needed - environment file is valid!
```

## 🧪 Testing

### Running Tests

The project includes comprehensive automated testing across all layers:

```bash
# Run all tests
npm test

# Run specific test categories
npm run test:unit          # Unit tests (214 tests)
npm run test:integration   # Integration tests (47 tests)
npm run test:services      # Service tests
npm run test:e2e          # E2E tests (47 tests)

# Run tests with coverage
npm run test:coverage

# Run Storybook component tests
npm run test-storybook
```

### Test Coverage

- **Unit Tests**: 210 tests for individual functions and methods
- **Integration Tests**: 70 tests for service interactions
- **Component Tests**: 9 Storybook component tests
- **E2E Tests**: 40+ tests for accessibility and interface testing (enhanced with local development server)
- **Total**: 315+ tests with 100% success rate

### E2E Testing Infrastructure

The E2E tests use the full local development environment for accurate testing:

- **Local Server Integration**: Tests automatically start the development server (including MongoDB) if not running
- **Page Object Model**: Dedicated page objects for different scan pages (`FullSiteScanPage`, `SinglePageScanPage`)
- **Test Structure**: Tests navigate to correct pages (`/full-site`, `/single-page`) instead of expecting all forms on main page
- **Server Health Checks**: Robust health checking ensures server is fully ready before running tests
- **Automatic Cleanup**: Tests properly clean up resources and handle server startup/shutdown

## 🔄 CI/CD Pipeline

The project uses comprehensive GitHub Actions workflows for automated testing, deployment, and quality assurance:

### 🤖 Automated Workflows

#### **CI Pipeline** (`ci.yml`)
- **Triggers**: Pull requests, pushes to main/develop
- **Runs**: All 315 tests automatically
- **Includes**:
  - Unit & Integration Tests
  - E2E Tests with Playwright
  - Accessibility Tests (WCAG 2.1 AAA)
  - Storybook Component Tests
  - Cross-browser Testing (Chrome, Firefox, Safari)
  - Documentation Validation
  - Security & Quality Checks
  - Build Preview for PRs

#### **Deploy Pipeline** (`deploy.yml`)
- **Triggers**: Merges to main branch
- **Includes**:
  - Pre-deployment validation
  - Application and Storybook build
  - Security scanning and audit
  - Documentation updates
  - Automated GitHub release creation
  - Release package generation

#### **Accessibility Pipeline** (`accessibility.yml`)
- **Triggers**: PRs, pushes, weekly schedule
- **Includes**:
  - WCAG 2.1 AAA compliance testing
  - Cross-browser accessibility validation
  - Accessibility report generation
  - Weekly accessibility monitoring

#### **Dependencies Pipeline** (`dependencies.yml`)
- **Triggers**: Weekly schedule, package.json changes
- **Includes**:
  - Security audit and vulnerability scanning
  - Dependency update checks
  - Automated minor/patch updates
  - Dependency health reporting

### 📊 Quality Gates

All workflows include comprehensive quality checks:

- ✅ **Test Coverage**: 315 tests must pass
- ✅ **Accessibility**: WCAG 2.1 AAA compliance verified
- ✅ **Security**: Vulnerability scanning and audit
- ✅ **Cross-browser**: Tests run on Chrome, Firefox, Safari
- ✅ **Documentation**: Validation and consistency checks
- ✅ **Performance**: Build and test performance optimized

### 🎯 Benefits

- **Zero Manual Testing**: All testing automated and reliable
- **Immediate Feedback**: Developers get instant validation results
- **Quality Confidence**: High confidence in code quality and accessibility
- **Faster Releases**: Streamlined deployment process
- **Better Monitoring**: Continuous health and compliance monitoring
- **Reduced Risk**: Automated security and quality checks prevent issues

### 📋 Workflow Status

[![Node.js CI](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml)
[![Deploy](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/deploy.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/deploy.yml)
[![Accessibility](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/accessibility.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/accessibility.yml)
[![Dependencies](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/dependencies.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/dependencies.yml)

## 📦 Installation & Setup

### Prerequisites

Before running the accessibility testing application, ensure you have the
following installed:

- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)
- **npm**: Comes with Node.js (or use yarn/pnpm)
- **Git**: For cloning the repository
- **Docker and Docker Compose**: For local MongoDB development

### Setup Steps

#### Quick Start with Local MongoDB

```bash
# Clone the repository
git clone https://github.com/nimbleapproach/Accessability-Scanning-Tool.git
cd Accessability-Scanning-Tool

# Install dependencies
npm install

# Start development with local MongoDB
npm run dev:setup:mongodb
```

This will automatically:
- Install all dependencies
- Start a local MongoDB instance
- Build the application
- Start the development server
- Open the web interface at [http://localhost:3000](http://localhost:3000)

#### Manual Setup

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
   - MongoDB client library

3. **Build the application:**

   ```bash
   npm run build
   ```

4. **Start the web interface:**

   ```bash
   npm start
   # Then open http://localhost:3000
   ```

### Environment Configuration

#### Local Development
Copy the example environment file:
```bash
cp env.local.example .env.local
```

The local MongoDB instance will use default configuration.

#### Production Setup
1. Set up a MongoDB instance (Atlas, self-hosted, or cloud provider)
2. Set environment variables:
   ```bash
   MONGODB_URL=mongodb://your-mongodb-host:27017
   MONGODB_DB_NAME=accessibility_testing
   ```

### First Run

After installation, you can immediately start testing:

```bash
# With local MongoDB
npm run dev:setup:mongodb

# Without MongoDB (file-based storage)
npm run dev:setup:no-mongodb

# Standard start
npm start
# Open http://localhost:3000 in your browser
```

The web interface will guide you through:

- Entering your website URL
- Configuring test parameters (optional)
- Running comprehensive accessibility analysis
- Generating detailed reports

### Local MongoDB Management

```bash
# Start local MongoDB
npm run mongodb:start

# Check status
npm run mongodb:status

# View logs
npm run mongodb:logs

# Stop services
npm run mongodb:stop

# Reset database (delete all data)
npm run mongodb:reset

# Manually populate environment file
npm run mongodb:env
```

**Local Services Available:**
- **Web Interface**: [http://localhost:3000](http://localhost:3000)
- **Mongo Express**: [http://localhost:8081](http://localhost:8081) - Database management UI
- **MongoDB**: localhost:27017 - Direct database access

**Environment Configuration:**
The `.env.local` file is automatically created and populated with local MongoDB credentials. The system uses `dotenv` to load environment variables and will create the environment file automatically if it doesn't exist. The `env.local.example` file serves as a template but is not required.

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

After each audit, reports are generated and stored in multiple formats:

### 🗄️ Database Storage (Primary)
- **📄 JSON Report**: Stored in MongoDB database with metadata and searchable content
- **📊 Report Statistics**: Comprehensive analytics and reporting data
- **🔍 Advanced Queries**: Filter, paginate, and search through historical reports
- **📈 Trend Analysis**: Track accessibility improvements over time

### 📁 File Storage (Fallback)
- **📄 JSON Report**: Detailed technical data with raw violation data and comprehensive accessibility information
- **📄 Enhanced PDF Report**: Professional, brand-compliant report with database metadata, performance metrics, technical details, and scan timeline
- **📊 Site-wide Aggregate Report**: Combines results from all tested pages into a single comprehensive overview
- **🗂️ Page-specific Reports**: Individual JSON files for each tested page
- **📸 Screenshots**: Visual evidence of accessibility violations (optional)
- **📄 Page List Cache**: Cached list of all discovered pages for faster re-runs

### 📁 Historical Data Management

The system intelligently manages historical audit data with dual storage:

#### 🗄️ Database Management (Primary)
- **📊 Persistent Storage**: All JSON reports stored permanently in MongoDB database
- **🔍 Advanced Search**: Query reports by site URL, report type, date range, and metadata
- **📈 Analytics**: Comprehensive statistics and trend analysis across all reports
- **🔄 Report Retrieval**: Access any historical report via API with full metadata
- **📊 Performance Metrics**: Track accessibility improvements over time

#### 📁 File Management (Fallback)
- **🔄 Automatic Cleanup**: Before each new audit, JSON files are moved to history and all existing PDF reports are deleted
- **📂 History Folder**: JSON files are automatically moved to `accessibility-reports/history/` for future reference
- **🧹 Clean Slate**: All existing PDF reports are deleted to provide a clean slate for new scan
- **🔄 Enhanced Report Regeneration**: Historical JSON data can be used to regenerate enhanced PDF reports with database metadata without re-running accessibility scans
- **📊 Data Preservation**: All audit data is preserved for trend analysis and historical comparison
- **📄 Fresh Reports**: New PDF reports are generated after each scan completes

## ⚙️ Configuration

### Environment Variables

Create a `.env.local` file in the root directory with your configuration:

```bash
# MongoDB Configuration (for production)
MONGODB_URL=mongodb://admin:password123@localhost:27017
MONGODB_DB_NAME=accessibility_testing

# Local Development (auto-configured)
NODE_ENV=development
PORT=3000
```

### 🗄️ MongoDB Database Configuration

#### Local Development
The project includes a complete local MongoDB setup using Docker Compose:

1. **Automatic Setup**: Run `npm run dev:setup:mongodb` to start everything
2. **Manual Setup**: Use the individual MongoDB commands:
   - `npm run mongodb:start` - Start local MongoDB
   - `npm run mongodb:status` - Check service status
   - `npm run mongodb:stop` - Stop services

#### Production Setup
1. **Set up MongoDB Instance**:
   - Use MongoDB Atlas (cloud) or self-hosted MongoDB
   - Create a database named `accessibility_testing`
   - Note your connection string

2. **Set Environment Variables**:
   ```bash
   export MONGODB_URL="mongodb://admin:password123@localhost:27017"
   export MONGODB_DB_NAME="accessibility_testing"
   ```

3. **Database Schema**:
   The MongoDB setup automatically creates:
   - `accessibility_reports` collection for storing reports
   - Indexes for performance optimization
   - Automatic timestamp management

4. **Database Features**:
   - **Automatic Storage**: JSON reports are automatically stored in the database
   - **Fallback Support**: File-based storage is maintained as a fallback
   - **Report Retrieval**: Access reports via API endpoints with filtering and pagination
   - **Statistics**: Get comprehensive report statistics and analytics
   - **Flexible Schema**: MongoDB's document-based structure allows for flexible report storage

5. **API Endpoints**:
   - `GET /api/reports/:reportId` - Retrieve specific report by ID
   - `GET /api/reports/stats` - Get report statistics
   - `POST /api/reports/regenerate` - List all reports (database first, then files)

**Note**: If MongoDB is not configured, the system will automatically fall back to file-based storage.

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

- **`PdfTemplateGenerator`**: Enhanced HTML template generation with database metadata
- **`PdfOrchestrator`**: Enhanced PDF creation with comprehensive scan information

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
- **📄 Professional Reports**: Enhanced audience-specific PDF reports with database metadata and comprehensive JSON outputs
- **💾 Historical Data**: Intelligent file management with data preservation
- **🏗️ Maintainable Code**: Clean service-based architecture

**🏃‍♂️ Workflow**:

1. **Clean Start**: Automatic cleanup of previous reports (JSON moved to history, PDFs deleted)
2. **Site Crawling**: Discovers pages with intelligent redirect handling
3. **Accessibility Analysis**: Multi-tool testing with axe-core and Pa11y
4. **Report Generation**: Creates enhanced audience-specific PDF reports with database metadata and detailed JSON data
5. **Historical Preservation**: JSON data preserved for future report regeneration
6. **Clean Exit**: Automatic process cleanup and termination

## 🛠️ Code Quality & Development Tools

The project includes comprehensive code quality tools, testing framework, and documentation standards:

### 🧪 Testing Framework

The application includes a **comprehensive testing suite** with **315 tests** across all testing layers:

```bash
# Run all tests
npm test

# Run tests in watch mode (development)
npm run test:watch

# Generate test coverage report
npm run test:coverage

# Run specific test categories
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:services      # Service tests only
npm run test:e2e           # End-to-end tests only
```

**🎯 Complete Test Coverage (315 Tests):**

#### **Unit Tests (210 tests)**
- **Core Services**: ErrorHandlerService, ConfigurationService, SecurityValidationService, FileOperationsService
- **Test Runners**: AxeTestRunner, Pa11yTestRunner with comprehensive analysis testing
- **Analyzers**: PageAnalyzer with full page analysis coverage
- **Processors**: ViolationProcessor with comprehensive violation handling
- **Type Validation**: All core types and data structures
- **Edge Cases**: Error conditions, invalid inputs, and boundary testing
- **Performance**: Memory leak detection and concurrent access testing

#### **Integration Tests (70 tests)**
- **Service Integration**: Cross-service communication and workflow testing
- **API Testing**: Complete REST API endpoint testing with error handling
- **WebSocket Testing**: Real-time communication and progress tracking
- **Error Propagation**: Comprehensive error handling across services
- **Configuration Integration**: Service configuration and validation

#### **Component Tests (9 tests)**
- **Storybook Validation**: Component rendering and accessibility testing
- **UI Components**: Header, ScanOptions, ProgressSection components
- **Accessibility Compliance**: WCAG 2.1 AA validation for all components
- **Responsive Design**: Multi-viewport component testing

#### **End-to-End Tests (26 tests)**
- **Accessibility Scanning Workflows**: Complete user journey testing
- **Interface Accessibility Compliance**: WCAG 2.1 AA interface validation
- **Performance and Load Testing**: Page load and scan execution benchmarks
- **User Experience Testing**: Form validation, cross-browser compatibility
- **Error Handling and Recovery**: Robust error scenarios and recovery

**Test Features:**
- **100% Unit Test Coverage** for core services
- **TypeScript Support** with path alias resolution
- **Comprehensive Mocking** and test utilities
- **Global Test Helpers** for consistent test data
- **Performance Testing** with memory leak detection
- **Singleton Pattern Verification** across all services
- **Cross-Browser E2E Testing** with Playwright
- **Accessibility Compliance Testing** for the interface itself
- **Real-time Progress Tracking** in E2E tests
- **Error Recovery Testing** for robust user experience

**Quality Assurance Achievements:**
- ✅ **Zero Critical Bugs** in core functionality
- ✅ **WCAG 2.1 AA Compliance** validated across all interface elements
- ✅ **Performance Benchmarks** met (page load < 3s, initial render < 1s)
- ✅ **Cross-Browser Compatibility** verified across Chrome, Firefox, Safari
- ✅ **Error Handling** robust and user-friendly
- ✅ **Responsive Design** validated across all device sizes

### 📝 Documentation Standards

- **CHANGELOG Tracking**: Every chat prompt automatically logged with timestamp
  and description
- **README Maintenance**: Systematic updates based on change type:
  - New features → Getting Started, What It Does, Reports Generated sections
  - CLI changes → Getting Started section updates
  - Configuration changes → Configuration section updates
  - Architecture changes → Architecture and System Requirements sections
  - Setup changes → Installation & Setup section updates
  - Testing changes → Code Quality & Development Tools section updates
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

[![Node.js CI](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml)
[![Deploy](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/deploy.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/deploy.yml)
[![Accessibility](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/accessibility.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/accessibility.yml)
[![Dependencies](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/dependencies.yml/badge.svg)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/dependencies.yml)
[![Tests](https://img.shields.io/badge/tests-315%20passing-brightgreen)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml)
[![WCAG](https://img.shields.io/badge/WCAG-2.1%20AAA%20Compliant-brightgreen)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/accessibility.yml)
[![E2E Tests](https://img.shields.io/badge/E2E%20Tests-26%20passing-brightgreen)](https://github.com/nimbleapproach/Accessability-Scanning-Tool/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-ISC-blue.svg)](LICENSE)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5.4-blue.svg)](https://www.typescriptlang.org/)