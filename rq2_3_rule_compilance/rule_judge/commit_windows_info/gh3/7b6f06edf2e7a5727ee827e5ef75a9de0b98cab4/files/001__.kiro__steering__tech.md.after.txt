# Technology Stack

## Framework & Language
- **Flutter** (Dart SDK ^3.8.1) - iOS-first development (future: Android, macOS, Windows, Web)
- **Dart** - Primary programming language

## Architecture & Patterns
- **Hybrid Dependency Injection** - Services use Injectable + GetIt, ViewModels manually instantiated
- **Injectable-first approach** - Prefer `@injectable` annotations over direct `getIt` calls
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
- `injectable: ^2.5.0` - Code generation for dependency injection (preferred approach)
- `get_it: ^8.0.3` - Service locator for dependency injection (underlying container)

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

## Dependency Injection Guidelines

### Injectable-First Approach
**Prefer `@injectable` annotations over direct `getIt` calls** for better maintainability and testability.

#### ✅ Preferred Pattern
```dart
@injectable
class MyService {
  final ApiClient _apiClient;
  MyService(this._apiClient);
}

@injectable 
class MyViewModel {
  final MyService _service;
  MyViewModel(this._service);
}
```

#### ❌ Avoid Direct getIt
```dart
class MyService {
  late final ApiClient _apiClient;
  
  MyService() {
    _apiClient = getIt<ApiClient>(); // Avoid this
  }
}
```

#### Direct getIt Usage Exceptions
Direct `getIt` calls are **only** acceptable in these specific locations:

**Application Bootstrapping:**
- `lib/main.dart` - Root application setup and initial dependency resolution

**Integration Test Setup:**
- `test/integration/*` - Test harness configuration and mock dependency setup

**Generated Code:**
- `*.g.dart` files - Code generation outputs (exempt from this rule)
- `*.config.dart` files - Generated DI configuration files

**Current Exception Locations in Codebase:**
- `lib/main.dart:13-14` - `AuthService` and `RouteCollectionService` resolution for app bootstrap

All other code locations should use `@injectable`, `@lazySingleton`, or `@singleton` annotations for dependency management.

### RouteProvider Dependency Injection Pattern

RouteProviders follow a specific registration pattern to enable modular route collection:

#### ✅ Correct Pattern
```dart
@Named("HomeRouteProvider")
@Injectable(as: RouteProvider)
class HomeRouteProvider implements RouteProvider {
  final HomeViewModelFactory _factory;
  HomeRouteProvider(this._factory);
  
  @override
  RouteBase getRoute() => GoRoute(/* route config */);
}
```

#### ❌ Incorrect Pattern
```dart
// Don't register concrete types
@injectable
class HomeRouteProvider implements RouteProvider { /* ... */ }
```

**Key Requirements:**
- Use `@Named("ClassName")` for unique identification
- Use `@Injectable(as: RouteProvider)` to register as interface type
- **Do NOT** register concrete RouteProvider types with `@injectable`
- Only register as the `RouteProvider` interface to enable `getAll<RouteProvider>()` collection

This pattern enables `RouteCollectionService` to collect all routes via `GetIt.instance.getAll<RouteProvider>()` while maintaining modular architecture.

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