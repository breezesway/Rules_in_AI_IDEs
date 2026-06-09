# MCP Flutter Automation Server - Test Suite

This directory contains comprehensive tests for the MCP Flutter Automation Server, covering unit tests, integration tests, and performance tests.

## Test Structure

```
test/
├── README.md                    # This file
├── all_tests.dart               # Combined test runner
├── dart_test.yaml               # Test configuration
├── test_utils.dart              # Shared utilities and helpers
├── unit/                        # Unit tests
│   ├── flutter_app_test.dart    # FlutterApp model tests
│   └── flutter_controller_test.dart # FlutterController tests
├── integration/                 # Integration tests
│   └── mcp_server_test.dart     # MCP server integration tests
├── performance/                 # Performance tests
│   └── performance_test.dart    # Load and stress tests
├── mocks/                       # Mock objects (generated)
└── fixtures/                    # Test data and fixtures
```

## Test Categories

### Unit Tests (`test/unit/`)

**FlutterApp Model Tests** (`flutter_app_test.dart`)
- ✅ Initialization with various configurations
- ✅ Log management (add, clear, retrieve recent logs)
- ✅ Log size limiting (max 1000 lines)
- ✅ State management transitions
- ✅ VM service URI and isolate ID management
- ✅ Immutable logs getter functionality
- ✅ AppState enum validation

**FlutterController Tests** (`flutter_controller_test.dart`)
- ✅ App launch with various parameters
- ✅ Duplicate app ID prevention
- ✅ Default and custom port handling
- ✅ App lifecycle management
- ✅ Log retrieval and management
- ✅ Hot reload/restart error handling
- ✅ VM service operation error handling
- ✅ App stopping and cleanup
- ✅ Multiple concurrent app management
- ✅ Resource disposal

### Integration Tests (`test/integration/`)

**MCP Server Tests** (`mcp_server_test.dart`)
- ✅ Tool registration verification
- ✅ Tool execution with valid parameters
- ✅ Error handling for invalid parameters
- ✅ Resource access (devices, flutter doctor)
- ✅ Concurrent tool execution
- ✅ Resource cleanup on server stop
- ✅ Real Flutter command integration (when available)

### Performance Tests (`test/performance/`)

**Performance and Stress Tests** (`performance_test.dart`)
- ✅ Memory management with many app launches
- ✅ Large log volume handling
- ✅ Concurrent app launches
- ✅ Rapid start/stop cycles
- ✅ Resource usage optimization
- ✅ High load operations (50+ concurrent)
- ✅ Error handling under stress

## Test Utilities (`test_utils.dart`)

### TestUtils Class
- `createTempDir()`: Creates auto-cleanup temporary directories
- `createMockFlutterProject()`: Creates realistic Flutter project structure
- `createMockVmResponse()`: Generates VM service response data
- `createMockScreenshotResponse()`: Creates base64 PNG screenshot data
- `createMockWidgetTreeResponse()`: Generates widget tree data
- `waitForCondition()`: Async condition waiting with timeout
- `createMockProcess()`: Creates mock Process objects

### Custom Matchers
- `containsVmServiceUrl()`: Matches VM service URL patterns
- `isBase64Image()`: Validates base64 encoded PNG images

### Test Data
- Sample VM service output
- Sample error messages
- Flutter devices JSON response
- Various test constants

## Running Tests

### Using the Test Runner Script

```bash
# Make script executable (first time only)
chmod +x scripts/run_tests.sh

# Setup (install dependencies, generate mocks)
./scripts/run_tests.sh setup

# Quick development checks
./scripts/run_tests.sh quick

# Run specific test suites
./scripts/run_tests.sh unit
./scripts/run_tests.sh integration
./scripts/run_tests.sh performance

# Run all tests
./scripts/run_tests.sh all

# CI/CD pipeline
./scripts/run_tests.sh ci

# Generate coverage report
./scripts/run_tests.sh coverage
```

### Using Dart Test Directly

```bash
# Run all tests
dart test

# Run with coverage
dart test --coverage=coverage

# Run specific test files
dart test test/unit/flutter_app_test.dart
dart test test/integration/

# Run with specific tags
dart test --tags unit
dart test --tags integration

# Run with custom timeout
dart test --timeout=60s
```

### Test Configuration

Tests are configured via `dart_test.yaml`:
- **Unit tests**: 10s timeout, 4 concurrent
- **Integration tests**: 60s timeout, 2 concurrent  
- **Performance tests**: 120s timeout, 1 concurrent

## Test Environment Requirements

### Required
- Dart SDK 3.0+
- Dependencies from `pubspec.yaml`

### Optional (for full test coverage)
- Flutter SDK (for Flutter command integration tests)
- `lcov` package (for HTML coverage reports)
- Sufficient system resources for performance tests

### Environment Setup

```bash
# Install dependencies
dart pub get

# Generate mocks (if using mockito)
dart run build_runner build

# Install coverage tools (optional)
dart pub global activate coverage

# Install lcov for HTML reports (optional)
# macOS: brew install lcov
# Ubuntu: sudo apt-get install lcov
```

## Test Coverage

The test suite aims for high coverage across:

- **Model Classes**: 100% line coverage
- **Controller Logic**: 95%+ line coverage  
- **MCP Server**: 90%+ functional coverage
- **Error Handling**: Comprehensive error scenarios
- **Performance**: Memory, concurrency, and load testing

### Coverage Reports

Coverage reports are generated in multiple formats:
- **Raw**: `coverage/` directory
- **LCOV**: `coverage/lcov.info`
- **HTML**: `coverage/html/index.html` (if lcov installed)

## Mock Strategy

The test suite uses a hybrid approach:
- **Real objects** for pure Dart classes (FlutterApp, etc.)
- **Mocks** for external dependencies (Process, VmService, etc.)
- **Test doubles** for Flutter-specific components
- **Fake implementations** for complex integrations

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: dart-lang/setup-dart@v1
      - run: ./scripts/run_tests.sh ci
```

### Test Optimization for CI

- Parallel test execution where safe
- Mocked external dependencies
- Skipped tests requiring Flutter when not available
- Optimized timeouts for CI environments

## Debugging Tests

### Common Issues

1. **Flutter Not Available**: Tests requiring Flutter are automatically skipped
2. **Port Conflicts**: Tests use incremental ports to avoid conflicts
3. **Timeout Issues**: Increase timeout for slow environments
4. **Mock Generation**: Run `dart run build_runner build` if mocks fail

### Debug Mode

```bash
# Run with verbose output
dart test --reporter=expanded

# Run single test with debug
dart test test/unit/flutter_app_test.dart --reporter=expanded

# Run with Observatory (for debugging)
dart --observe test/unit/flutter_app_test.dart
```

## Contributing to Tests

### Adding New Tests

1. **Unit Tests**: Add to appropriate file in `test/unit/`
2. **Integration Tests**: Add to `test/integration/`
3. **Performance Tests**: Add to `test/performance/`
4. **Utilities**: Extend `test_utils.dart`

### Test Naming Conventions

- Test files: `*_test.dart`
- Test groups: Descriptive names matching functionality
- Test cases: "should [expected behavior] when [condition]"
- Mock files: `*.mocks.dart` (generated)

### Best Practices

1. **Isolation**: Each test should be independent
2. **Setup/Teardown**: Use `setUp()` and `tearDown()` appropriately
3. **Assertions**: Use descriptive matchers
4. **Mocking**: Mock external dependencies, not internal logic
5. **Performance**: Keep unit tests fast (<1s each)
6. **Documentation**: Comment complex test scenarios

## Test Metrics

Target metrics for the test suite:
- **Execution Time**: Unit tests <10s total, Integration <60s, Performance <120s
- **Coverage**: >90% line coverage, >95% branch coverage
- **Reliability**: <1% flaky test rate
- **Maintainability**: Tests should be easy to read and modify