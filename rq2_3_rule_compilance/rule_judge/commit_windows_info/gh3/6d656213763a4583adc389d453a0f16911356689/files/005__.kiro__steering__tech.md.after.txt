# Technology Stack

## Framework & Language
- **Flutter** (Dart SDK ^3.8.1) - iOS-first development (future: Android, macOS, Windows, Web)
- **Dart** - Primary programming language

## Architecture & Patterns
- **Hybrid Dependency Injection** - Services use Injectable + GetIt, ViewModels manually instantiated
- **Screen-based modular architecture** - each screen is a self-contained module
- **ViewModel Factory pattern** - Factories registered with DI create ViewModels with explicit dependencies
- **RouteProvider pattern** - Each screen module provides its own route configuration
- **GoRouter** for declarative routing with ViewModel factory integration
- **Explicit dependency management** - All dependencies injected through constructors, no hidden GetIt calls
- **Avoid strict layer separation** - focus on modularity and testability

## Key Dependencies

### Core Flutter
- `flutter` - Flutter SDK
- `go_router: ^16.0.0` - Declarative routing

### State Management & DI
- `injectable: ^2.5.0` - Code generation for dependency injection
- `get_it: ^8.0.3` - Service locator for dependency injection

### GraphQL & API
- `ferry: ^0.16.2-dev.4` - GraphQL client for Flutter
- `gql_http_link: ^1.1.0` - HTTP transport for GraphQL
- `http: ^1.4.0` - HTTP client

### Authentication & Storage
- `shared_preferences: ^2.0.0` - Local data persistence
- `flutter_custom_tabs: ^2.4.0` - OAuth authentication with custom tabs

### UI & Utilities
- `flutter_octicons: ^1.52.0` - GitHub-style icons
- `flutter_markdown: ^0.7.4+1` - Markdown rendering
- `envied: ^1.1.1` - Environment variable management

### Development & Testing
- `build_runner: ^2.5.4` - Code generation
- `ferry_generator: ^0.14.0-dev.0` - GraphQL code generation
- `mockito: ^5.4.4` - Mocking for tests
- `flutter_test` - Testing framework

## Build System & Code Generation

### GraphQL Code Generation
```bash
# Generate GraphQL types and queries
flutter packages pub run build_runner build

# Watch for changes and regenerate
flutter packages pub run build_runner watch
```

### Dependency Injection Generation
```bash
# Generate DI configuration
flutter packages pub run build_runner build --delete-conflicting-outputs
```

## Common Commands

### Development
```bash
# Run the app
flutter run

# Hot reload during development
# Press 'r' in terminal or use IDE hot reload

# Clean build
flutter clean && flutter pub get
```

### Testing
```bash
# Run all tests
flutter test

# Run tests with coverage
flutter test --coverage

# Run specific test file
flutter test test/path/to/test_file.dart
```

### Code Quality
```bash
# Analyze code
flutter analyze

# Format code
dart format .

# Check for linting issues
flutter analyze --fatal-infos
```

### Build & Release
```bash
# Build iOS (primary platform)
flutter build ios

# Build iOS for release
flutter build ios --release

# Future platform builds:
# flutter build apk (Android)
# flutter build macos (macOS)
# flutter build windows (Windows)
# flutter build web (Web)
```

## GraphQL Schema
- Uses GitHub's GraphQL API v4
- Schema file: `lib/github_schema.graphql`
- Generated code in `lib/__generated__/` and component-specific `__generated__/` folders