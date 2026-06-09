#!/bin/bash

# MCP Flutter Automation Server - Test Runner Script
# This script provides various ways to run the test suite

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Flutter is available
check_flutter() {
    if command -v flutter &> /dev/null; then
        flutter --version | head -1
        return 0
    else
        print_warning "Flutter not found. Some tests may be skipped."
        return 1
    fi
}

# Function to run dart pub get
setup_dependencies() {
    print_status "Installing dependencies..."
    dart pub get
    print_success "Dependencies installed"
}

# Function to generate mocks
generate_mocks() {
    print_status "Generating mocks..."
    if dart run build_runner build --delete-conflicting-outputs; then
        print_success "Mocks generated successfully"
    else
        print_warning "Mock generation failed, but continuing..."
    fi
}

# Function to run unit tests
run_unit_tests() {
    print_status "Running unit tests..."
    dart test test/unit/ --reporter=expanded --coverage=coverage/unit
    print_success "Unit tests completed"
}

# Function to run integration tests
run_integration_tests() {
    print_status "Running integration tests..."
    dart test test/integration/ --reporter=expanded --coverage=coverage/integration
    print_success "Integration tests completed"
}

# Function to run performance tests
run_performance_tests() {
    print_status "Running performance tests..."
    dart test test/performance/ --reporter=expanded --timeout=120s
    print_success "Performance tests completed"
}

# Function to run all tests
run_all_tests() {
    print_status "Running all tests..."
    dart test --reporter=expanded --coverage=coverage/all
    print_success "All tests completed"
}

# Function to generate coverage report
generate_coverage() {
    print_status "Generating coverage report..."
    
    if command -v genhtml &> /dev/null; then
        # Convert to LCOV format and generate HTML report
        dart pub global activate coverage
        dart pub global run coverage:format_coverage \
            --lcov \
            --in=coverage \
            --out=coverage/lcov.info \
            --packages=.dart_tool/package_config.json \
            --report-on=lib
            
        genhtml coverage/lcov.info -o coverage/html/
        print_success "Coverage report generated in coverage/html/"
    else
        print_warning "genhtml not found. Install lcov for HTML coverage reports."
        print_status "Raw coverage data available in coverage/ directory"
    fi
}

# Function to lint code
run_lint() {
    print_status "Running dart analyze..."
    dart analyze --fatal-infos --fatal-warnings
    print_success "Code analysis passed"
}

# Function to format code
format_code() {
    print_status "Formatting code..."
    dart format --set-exit-if-changed .
    print_success "Code formatting checked"
}

# Function to run quick checks (lint + format + unit tests)
run_quick_checks() {
    print_status "Running quick checks..."
    run_lint
    format_code
    run_unit_tests
    print_success "Quick checks completed"
}

# Function to run CI checks (everything except performance tests)
run_ci_checks() {
    print_status "Running CI checks..."
    setup_dependencies
    run_lint
    format_code
    run_unit_tests
    run_integration_tests
    generate_coverage
    print_success "CI checks completed"
}

# Function to clean coverage data
clean_coverage() {
    print_status "Cleaning coverage data..."
    rm -rf coverage/
    mkdir -p coverage
    print_success "Coverage data cleaned"
}

# Function to show help
show_help() {
    echo "MCP Flutter Automation Server - Test Runner"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup          Install dependencies and generate mocks"
    echo "  unit           Run unit tests only"
    echo "  integration    Run integration tests only"
    echo "  performance    Run performance tests only"
    echo "  all            Run all tests"
    echo "  coverage       Generate coverage report"
    echo "  lint           Run dart analyze"
    echo "  format         Check code formatting"
    echo "  quick          Run quick checks (lint + format + unit tests)"
    echo "  ci             Run CI checks (everything except performance)"
    echo "  clean          Clean coverage data"
    echo "  help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup       # First time setup"
    echo "  $0 quick       # Quick development checks"
    echo "  $0 all         # Full test suite"
    echo "  $0 ci          # CI/CD pipeline"
}

# Main script logic
main() {
    # Check if we're in the right directory
    if [[ ! -f "pubspec.yaml" ]]; then
        print_error "Must be run from the project root directory"
        exit 1
    fi
    
    # Check Flutter availability
    if check_flutter; then
        print_success "Flutter is available"
    fi
    
    # Parse command line arguments
    case "${1:-help}" in
        "setup")
            setup_dependencies
            generate_mocks
            ;;
        "unit")
            run_unit_tests
            ;;
        "integration")
            run_integration_tests
            ;;
        "performance")
            run_performance_tests
            ;;
        "all")
            setup_dependencies
            generate_mocks
            run_all_tests
            generate_coverage
            ;;
        "coverage")
            generate_coverage
            ;;
        "lint")
            run_lint
            ;;
        "format")
            format_code
            ;;
        "quick")
            run_quick_checks
            ;;
        "ci")
            run_ci_checks
            ;;
        "clean")
            clean_coverage
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"