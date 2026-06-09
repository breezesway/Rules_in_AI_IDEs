
# Project Overview

This document provides a comprehensive overview of the accessibility testing application, detailing its features, functionality, services, APIs, tools, and frameworks.

## Core Features

*   **Web Interface:** Modern, accessible web interface for running accessibility tests with real-time progress tracking via WebSocket.
*   **Automated Accessibility Testing:** Runs automated accessibility tests on web pages using multiple testing tools.
*   **Comprehensive Reporting:** Generates detailed accessibility reports in JSON format.
*   **Multi-Tool Analysis:** Utilises Axe-Core and Pa11y to provide a comprehensive analysis of web page accessibility.
*   **Violation Processing:** Processes and normalises accessibility violations from different tools into a unified format.
*   **Brand Compliance:** Checks for brand compliance, including colours, fonts, and logos.
*   **Security Validation:** Performs security checks on URLs and file paths.
*   **Configuration Management:** Provides a centralised system for managing test configurations.
*   **Error Handling:** Implements a robust error handling mechanism with logging and retries.
*   **Real-time Progress Tracking:** WebSocket-based real-time progress updates during accessibility scans.
*   **Historical Data Management:** Intelligent file management that preserves JSON audit data in history folder while providing clean slate for new scans.
*   **Automatic Cleanup:** Integrated cleanup process that moves JSON files to history, deletes PDFs, and preserves historical data for future report regeneration.

## Key Functionality

*   **`WebServer`:** Express.js web server with Socket.IO providing RESTful API endpoints, real-time progress tracking, and serving the web interface.
*   **`WorkflowOrchestrator`:** The central component that coordinates the entire accessibility testing process. It manages test runners, violation processors, report generators, and cleanup operations.
*   **Test Runners (`AxeTestRunner`, `Pa11yTestRunner`):** Execute accessibility tests using their respective tools and collect the results.
*   **`ViolationProcessor`:** Processes raw violation data from the test runners, normalises it, and enriches it with additional information like screenshots and remediation advice.
*   **`PageAnalyzer`:** Analyses the structure and content of a web page to provide context for the accessibility report.
*   **Report Generation:** Creates detailed accessibility reports in JSON format and provides functionality to aggregate reports for site-wide analysis.

## Services

*   **`ConfigurationService`:** Manages all test configurations, including settings for Axe and Pa11y.
*   **`ErrorHandlerService`:** Provides a centralised mechanism for handling and logging errors across the application.
*   **`SecurityValidationService`:** Performs security checks on URLs and file paths to prevent common vulnerabilities.
*   **`FileOperationsService`:** Handles all file system operations, such as reading, writing, deleting files, and moving files between directories with safety validation.

## APIs

The application provides RESTful API endpoints and WebSocket functionality for the web interface:

*   **`/api/health`:** Health check endpoint for server status
*   **`/api/scan/full-site`:** POST endpoint for full site accessibility scanning with real-time progress tracking
*   **`/api/scan/single-page`:** POST endpoint for single page accessibility scanning with real-time progress tracking
*   **`/api/reports/regenerate`:** POST endpoint for regenerating reports from existing data
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

### Accessibility Tools
*   **Axe-Core:** A leading accessibility testing engine.
*   **Pa11y:** An automated accessibility testing tool. 