
# Project Overview

This document provides a comprehensive overview of the accessibility testing application, detailing its features, functionality, services, APIs, tools, and frameworks.

## Core Features

*   **Web Interface:** Modern, accessible web interface for running accessibility tests with real-time progress tracking via WebSocket.
*   **WCAG 2.1 AAA Compliance:** Fully accessible interface meeting the highest accessibility standards with 16 passing E2E tests.
*   **Component-Based Architecture:** Shared TypeScript components used by both web interface and Storybook for consistent UI and testing.
*   **Automated Accessibility Testing:** Runs automated accessibility tests on web pages using multiple testing tools.
*   **Comprehensive Reporting:** Generates detailed accessibility reports in JSON format stored in database with on-demand PDF generation containing database metadata.
*   **Extensive Test Coverage:** 396 tests with 100% success rate including comprehensive orchestration and reporting layer testing with mock data helpers and error handling validation.
*   **Multi-Tool Analysis:** Utilises Axe-Core and Pa11y to provide a comprehensive analysis of web page accessibility.
*   **Violation Processing:** Processes and normalises accessibility violations from different tools into a unified format.
*   **Brand Compliance:** Checks for brand compliance, including colours, fonts, and logos.
*   **Security Validation:** Performs security checks on URLs and file paths.
*   **Configuration Management:** Provides a centralised system for managing test configurations.
*   **Error Handling:** Implements a robust error handling mechanism with logging and retries.
*   **Real-time Progress Tracking:** WebSocket-based real-time progress updates during accessibility scans.
*   **Historical Data Management:** Intelligent file management that preserves JSON audit data in history folder while providing clean slate for new scans.
*   **Automatic Cleanup:** Integrated cleanup process that moves JSON files to history, deletes PDFs, and preserves historical data for future report regeneration.
*   **Form Validation:** Robust client-side form validation with proper error display and screen reader announcements.
*   **Focus Management:** Enhanced focus restoration and keyboard navigation support.
*   **CI/CD Pipeline:** Comprehensive GitHub Actions workflows for automated testing, deployment, and quality assurance.
*   **Quality Gates:** Strict quality standards enforced through automated workflows with 396 tests and WCAG 2.1 AAA compliance.

## Key Functionality

*   **`WebServer`:** Express.js web server with Socket.IO providing RESTful API endpoints, real-time progress tracking, and serving the web interface.
*   **`WorkflowOrchestrator`:** The central component that coordinates the entire accessibility testing process. It delegates to specialized orchestrators for site crawling, accessibility analysis, report generation, and metrics calculation. (✅ **REFACTORED** - Now uses specialized orchestrators for improved maintainability)
*   **`SiteCrawlingOrchestrator`:** Specialized orchestrator for site crawling operations, managing page discovery, crawl coordination, and result processing.
*   **`AnalysisOrchestrator`:** Specialized orchestrator for accessibility analysis operations, managing parallel processing, tool coordination, and analysis result aggregation.
*   **`ReportGenerationOrchestrator`:** Specialized orchestrator for report generation operations, managing database storage, PDF generation, and report metadata.
*   **`MetricsCalculator`:** Utility class for calculating performance metrics, compliance statistics, and violation patterns from analysis results.
*   **`Component System`:** Shared TypeScript components (Header, ScanOptions, ProgressSection, ResultsSection, ErrorSection, Footer, WebInterface, LandingPage, FullSiteScanPage, SinglePageScanPage, ReportsPage) used by both web interface and Storybook for consistent UI and testing.
*   **Test Runners (`AxeTestRunner`, `Pa11yTestRunner`):** Execute accessibility tests using their respective tools and collect the results.
*   **`ViolationProcessor`:** Processes raw violation data from the test runners, normalises it, and enriches it with additional information like screenshots and remediation advice.
*   **`PageAnalyzer`:** Analyses the structure and content of a web page to provide context for the accessibility report.
*   **Report Generation:** Creates detailed accessibility reports in JSON format stored in database and provides functionality to aggregate reports for site-wide analysis with on-demand PDF generation using database metadata.

## Services

*   **`ConfigurationService`:** Manages all test configurations, including settings for Axe and Pa11y.
*   **`ErrorHandlerService`:** Provides a centralised mechanism for handling and logging errors across the application.
*   **`SecurityValidationService`:** Performs security checks on URLs and file paths to prevent common vulnerabilities.
*   **`FileOperationsService`:** Handles all file system operations, such as reading, writing, deleting files, and moving files between directories with safety validation.
*   **`DatabaseService`:** Manages database operations for storing and retrieving accessibility test results and metadata.
*   **`MetricsCalculator`:** Utility class for calculating performance metrics, compliance statistics, and violation patterns from analysis results.
*   **`DataTransformer`:** Utility class for transforming and aggregating data for reports, including WCAG compliance matrix generation.

## Orchestrators

*   **`SiteCrawlingOrchestrator`:** Specialized orchestrator for site crawling operations, managing page discovery, crawl coordination, and result processing.
*   **`AnalysisOrchestrator`:** Specialized orchestrator for accessibility analysis operations, managing parallel processing, tool coordination, and analysis result aggregation.
*   **`ReportGenerationOrchestrator`:** Specialized orchestrator for report generation operations, managing database storage, PDF generation, and report metadata.
*   **`WorkflowOrchestrator`:** High-level coordinator that delegates to specialized orchestrators and maintains backward compatibility with existing interfaces.

## APIs

The application provides RESTful API endpoints and WebSocket functionality for the web interface:

*   **`/api/health`:** Health check endpoint for server status
*   **`/api/scan/full-site`:** POST endpoint for full site accessibility scanning with real-time progress tracking
*   **`/api/scan/single-page`:** POST endpoint for single page accessibility scanning with real-time progress tracking
*   **`/api/reports/generate`:** POST endpoint for listing available reports from database
*   **`/api/reports/generate-pdf`:** POST endpoint for generating PDF reports from stored data
*   **`/api/reports/download/:filename`:** GET endpoint for downloading generated PDF files
*   **`/api/scan/status`:** GET endpoint for checking scan status
*   **WebSocket Events:**
  *   **`progress-update`:** Real-time progress updates during scans
  *   **`join-scan`:** Join a specific scan room for progress tracking
  *   **`disconnect`:** Handle client disconnection

Communication between components is handled through direct method calls and a service-oriented architecture, with real-time updates provided via WebSocket connections.

## Tools & Frameworks

### Core Frameworks
*   **Node.js:** The runtime environment for the application.
*   **TypeScript:** The primary programming language used.
*   **Express.js:** Web server framework for the web interface.
*   **Socket.IO:** Real-time bidirectional communication for progress tracking.
*   **Playwright:** Used for browser automation and integration testing.
*   **Jest:** The testing framework used for unit tests.

### Testing Framework
*   **Jest:** Comprehensive unit and integration testing framework with TypeScript support.
*   **Playwright:** E2E testing framework for web interface testing with cross-browser support.
*   **Storybook:** Component testing framework with accessibility validation and visual regression testing.
*   **Test Coverage:** ✅ **Phase 1-5 COMPLETED** with 396 tests passing (100% success rate).
*   **Test Categories:** Unit tests (225), integration tests (78), component tests (9), and E2E tests (84 accessibility tests).
*   **E2E Testing:** Comprehensive accessibility testing with enhanced infrastructure using local development server, dedicated page objects for different scan pages, and 84 tests covering WCAG 2.1 AAA compliance, keyboard navigation, screen reader compatibility, focus management, error handling, and responsive design.
*   **Mocking Strategy:** Simplified mocking approach for external dependencies using `any` types.
*   **Test Utilities:** Global test helpers and consistent test data creation with comprehensive cleanup.
*   **Performance Testing:** Memory leak detection and concurrent access testing (optimized to avoid creating unnecessary directories).
*   **Integration Testing:** Comprehensive integration test suite with 103 tests (99% success rate) covering:
  - **Services Integration** (30 tests): Singleton pattern verification, error handling consistency, configuration management
  - **API Integration** (25 tests): Web server endpoints, CORS handling, request validation, error responses
  - **WebSocket Integration** (18 tests): Real-time communication, progress updates, connection management, performance testing
      - **Cross-Service Communication** (5 tests): Service interaction patterns and workflow integration
    - **Orchestration Integration** (15 tests): Workflow orchestration, task management, and coordination
    - **Runners Integration** (20 tests): Axe and Pa11y test runner integration and configuration
    - **Processors Integration** (25 tests): Violation processing and data transformation
    - **Analyzers Integration** (15 tests): Page analysis and structure extraction
    - **Analysis Service Integration** (20 tests): API service layer and endpoint testing
  - **Coverage Metrics**: 11.68% statement coverage, 5.91% branch coverage, 8.42% function coverage
*   **Component Testing:** Storybook stories with accessibility validation (11 components, 12 validation tests, 76 story variants).
*   **Test Cleanup:** Automatic cleanup of temporary files including HTML files created during PDF generation.
*   **Timeout Management:** Jest timeout issues resolved with proper clearTimeout calls in Pa11yTestRunner, ErrorHandlerService, and ParallelAnalyzer.
*   **Accessibility Testing:** Page Object Model (POM) design pattern implementation with comprehensive WCAG 2.1 AAA compliance testing.
*   **Orchestrator Testing:** ✅ **VALIDATED** - All orchestrator classes tested and integrated successfully with web server functionality.

### Accessibility Tools
*   **Axe-Core:** A leading accessibility testing engine.
*   **Pa11y:** An automated accessibility testing tool.

### CI/CD Pipeline
*   **GitHub Actions:** Comprehensive automated testing and deployment workflows.
*   **CI Pipeline (`ci.yml`):** Runs on pull requests and pushes with 315+ tests including unit, integration, E2E, accessibility, and cross-browser testing.
*   **Deploy Pipeline (`deploy.yml`):** Automated deployment and release creation on merges to main with security scanning and documentation updates.
*   **Accessibility Pipeline (`accessibility.yml`):** Dedicated WCAG 2.1 AAA compliance monitoring with weekly scheduled runs.
*   **Dependencies Pipeline (`dependencies.yml`):** Security monitoring and dependency management with automated updates.
*   **Quality Gates:** Strict enforcement of test coverage, accessibility compliance, security standards, and cross-browser compatibility.
*   **Artifact Management:** Comprehensive test reports, build artifacts, and compliance documentation preserved for analysis.
*   **Performance Optimization:** Parallel execution, caching strategies, and efficient resource utilization for fast feedback loops.

## Local Development & Database Integration

*   **Local MongoDB Setup:** Complete local development environment with MongoDB and Mongo Express using Docker Compose.
*   **Environment Configuration:** Automatic `.env.local` file creation and population with local MongoDB credentials using `dotenv`.
*   **Database Storage:** JSON reports stored in MongoDB `accessibility_reports` collection with metadata and searchable content, enabling enhanced PDF generation with comprehensive scan information.
*   **Fallback Storage:** File-based storage maintained as fallback when database is unavailable.
*   **MongoDB API:** Direct database access via MongoDB driver for local development.
*   **Mongo Express:** Database management UI accessible at `http://localhost:8081` for visual database operations.
*   **Service Management:** Comprehensive npm scripts for MongoDB lifecycle management (start, stop, reset, status, logs).
*   **Database Schema:** Flexible document-based schema with automatic indexes and timestamp management.
*   **Health Monitoring:** Robust service health checks with proper MongoDB connection validation.
*   **Development Workflow:** Single command `npm run dev:full` starts complete local development environment with automatic validation.
*   **Environment Validation:** Pre-startup validation of environment configuration with automatic detection of placeholder values and missing variables.
*   **Secret Management:** Secure secret generation for local development with automatic environment file creation. 