# Project Structure

## Root Directory
```
gh3/
├── lib/                    # Main application code
├── test/                   # Test files (mirrors lib/ structure)
├── ios/                    # iOS-specific configuration
├── build/                  # Build artifacts (generated)
├── coverage/               # Test coverage reports
├── pubspec.yaml           # Dependencies and project configuration
├── build.yaml             # Build configuration for code generation
└── analysis_options.yaml  # Dart analyzer configuration
```

## Library Structure (`lib/`)

### Main Entry Point
- `lib/main.dart` - Application entry point with DI setup and app initialization
- `lib/github_schema.graphql` - GitHub GraphQL schema definition

### Generated Code
- `lib/__generated__/` - Global GraphQL generated files
  - `github_schema.*.dart` - Schema types and serializers
  - `serializers.gql.dart` - GraphQL serialization

### Source Code (`lib/src/`)

#### Core Setup
- `lib/src/init.dart` - Dependency injection configuration
- `lib/src/init.config.dart` - Generated DI configuration

#### Services (`lib/src/services/`)
Business logic layer - registered with dependency injection:
- `auth_service.dart` - Authentication state management
- `github_auth_client.dart` - GitHub OAuth client
- `token_storage.dart` - Secure token persistence
- `ferry_client_service.dart` - GraphQL client configuration
- `ferry_module.dart` - Ferry GraphQL module setup
- `scope_service.dart` - Application scope management
- `timer_service.dart` - Timer utilities

#### Routing (`lib/src/routing/`)
Centralized routing infrastructure:
- `app_route.dart` - Base class for all typed routes
- `route_provider.dart` - Route provider service
- `route_collection_service.dart` - Route collection management
- `routes.dart` - Convenience export file for all routes

#### Screens (`lib/src/screens/`)
Self-contained screen modules - each folder contains everything for that screen:
- `app/` - Main app and auth view models
  - `gh3_app.dart` - Root app widget with routing
  - `auth_viewmodel.dart` - Authentication state management
- `loading_screen/` - Loading/splash screen module
  - `loading_route.dart` - Typed route class for navigation
- `login_screen/` - OAuth login flow module
  - `login_route.dart` - Typed route class for navigation
- `home_screen/` - Main dashboard module
  - `home_route.dart` - Typed route class for navigation
- `user_details/` - User profile details module
  - `user_details_route.dart` - Typed route class for navigation

Each screen folder contains:
- `*_screen.dart` - Screen widget with Scaffold
- `*_viewmodel.dart` - Business logic and state management
- `*_route.dart` - Typed route class extending AppRoute for type-safe navigation
- `*.graphql` - GraphQL queries (if needed)
- `__generated__/` - Generated GraphQL code

#### Widgets (`lib/src/widgets/`)
Reusable UI components with their own GraphQL queries:
- `user_card/` - User profile card component
- `user_profile/` - Detailed user profile widget
- `repository_card/` - Repository display component

Each widget folder contains:
- `*.dart` - Widget implementation
- `*.graphql` - GraphQL query definitions
- `__generated__/` - Generated GraphQL code

## Test Structure (`test/`)
Mirrors the `lib/` structure:
- `test/screens/` - Screen widget tests and route tests (co-located with screen modules)
- `test/services/` - Service unit tests
- `test/widgets/` - Widget component tests
- `test/routing/` - Core routing infrastructure tests
- `*.mocks.dart` - Generated mock classes for testing

## Architecture Patterns

### Modular Screen Architecture
- **Screen Modules**: Each screen is a self-contained module that can be easily added/removed
- **Complete Screen Components**: Each screen folder contains screen widget, viewmodel, routing, and related components
- **Business Logic Separation**: Complex logic moved from screen widgets into ViewModels
- **Dependency Injection**: Use `@injectable` annotations, avoid direct `getIt` calls

### Hybrid Dependency Injection Pattern
1. **Services** - Registered with `@injectable`/`@lazySingleton` in DI container
2. **ViewModel Factories** - Registered with `@injectable`, create ViewModels with explicit dependencies
3. **ViewModels** - Manually instantiated by factories, extend `DisposableViewModel` for lifecycle management
4. **RouteProviders** - Registered with `@injectable`, create routes with ViewModel factory integration
5. **Screens** - Receive ViewModels through constructor parameters, focus on UI
6. **Widgets** - Receive data through parameters, minimal business logic


### ViewModel Lifecycle Management
- **Manual Creation**: ViewModels created by factories, not DI container
- **Explicit Dependencies**: All dependencies injected through constructors
- **Resource Disposal**: ViewModels extend `DisposableViewModel` with `onDispose()` hook
- **State Management**: ViewModels extend `ChangeNotifier` for UI reactivity

### File Naming Conventions
- `*_service.dart` - Business logic services (registered with DI)
- `*_viewmodel.dart` - UI state management (manually instantiated)
- `*_viewmodel_factory.dart` - ViewModel factory classes (registered with DI)
- `*_route_provider.dart` - Route provider classes (registered with DI)
- `*_screen.dart` - Full screen widgets
- `*_route.dart` - Typed route classes for navigation
- `*_test.dart` - Test files
- `*.mocks.dart` - Generated mock files
- `*.graphql` - GraphQL query definitions

### GraphQL Code Generation
Each component with GraphQL queries has:
- `component_name.graphql` - Query definitions
- `__generated__/component_name.*.dart` - Generated types, requests, and data classes

### Environment Configuration
- `.env` - Environment variables (not committed)
- `lib/src/env/` - Environment configuration classes