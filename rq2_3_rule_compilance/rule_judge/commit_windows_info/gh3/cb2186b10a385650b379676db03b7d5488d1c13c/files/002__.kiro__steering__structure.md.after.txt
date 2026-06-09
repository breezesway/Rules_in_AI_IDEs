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

#### Screens (`lib/src/screens/`)
Self-contained screen modules - each folder contains everything for that screen:
- `app/` - Main app and auth view models
  - `gh3_app.dart` - Root app widget with routing
  - `auth_viewmodel.dart` - Authentication state management
- `loading_screen/` - Loading/splash screen module
- `login_screen/` - OAuth login flow module
- `home_screen/` - Main dashboard module
- `user_details/` - User profile details module

Each screen folder contains:
- `*_screen.dart` - Screen widget with Scaffold
- `*_viewmodel.dart` - Business logic and state management
- `*.graphql` - GraphQL queries (if needed)
- `__generated__/` - Generated GraphQL code
- Routing configuration integrated in main app

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
- `test/screens/` - Screen widget tests
- `test/services/` - Service unit tests
- `test/widgets/` - Widget component tests
- `*.mocks.dart` - Generated mock classes for testing

## Architecture Patterns

### Modular Screen Architecture
- **Screen Modules**: Each screen is a self-contained module that can be easily added/removed
- **Complete Screen Components**: Each screen folder contains screen widget, viewmodel, routing, and related components
- **Business Logic Separation**: Complex logic moved from screen widgets into ViewModels
- **Dependency Injection**: Use `@injectable` annotations, avoid direct `getIt` calls

### Dependency Flow
1. **Services** - Registered with `@injectable` in DI container
2. **ViewModels** - Injected with service dependencies, contain business logic
3. **Screens** - Focus on UI, delegate complex logic to ViewModels
4. **Widgets** - Receive data through parameters, minimal business logic

### File Naming Conventions
- `*_service.dart` - Business logic services
- `*_viewmodel.dart` - UI state management
- `*_screen.dart` - Full screen widgets
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