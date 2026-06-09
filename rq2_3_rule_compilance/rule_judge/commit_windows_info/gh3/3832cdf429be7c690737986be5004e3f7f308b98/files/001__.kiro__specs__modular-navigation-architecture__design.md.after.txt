# Design Document

## Overview

This design refactors the current navigation and dependency injection architecture to support a modular, factory-based approach. The solution introduces ViewModel factories, distributed routing configuration, and self-contained screen modules that work seamlessly with Flutter's GoRouter and the existing Injectable/GetIt dependency injection system.

## Architecture

### Current Architecture Issues

The current implementation has several architectural limitations:
- ViewModels are registered as singletons with `@injectable`, causing issues with stack navigation
- The main `Gh3App` class holds direct references to all screens and ViewModels
- Route configuration is centralized in `gh3_app.dart`, making it hard to scale
- Screen modules are not self-contained, requiring modifications to multiple files when adding screens

### New Modular Architecture

The new architecture introduces:
1. **ViewModel Factory Pattern**: Injectable factory classes that create ViewModel instances
2. **Distributed Routing**: Each screen module defines its own routes via a route provider
3. **Self-Contained Modules**: Each screen contains all its components (widget, factory, routes)
4. **Dynamic Route Discovery**: Routes are collected automatically via dependency injection

## Components and Interfaces

### 1. ViewModel Factory Pattern

Each ViewModel will have its own factory class without a common interface, allowing for different parameters:

```dart
@injectable
class HomeViewModelFactory {
  final Client _ferryClient;
  
  HomeViewModelFactory(this._ferryClient);
  
  HomeViewModel create() {
    return HomeViewModel(_ferryClient);
  }
}

@injectable
class UserDetailsViewModelFactory {
  final Client _ferryClient;
  
  UserDetailsViewModelFactory(this._ferryClient);
  
  UserDetailsViewModel create(String username) {
    return UserDetailsViewModel(_ferryClient, username);
  }
}
```

### 2. Route Provider Interface

```dart
abstract class RouteProvider {
  RouteBase getRoute();
}
```

### 3. Typed Route Classes

Base route class providing common navigation methods:

```dart
abstract class AppRoute {
  String get path;
  
  void push(BuildContext context) {
    context.push(path);
  }
  
  void go(BuildContext context) {
    context.go(path);
  }
  
  void replace(BuildContext context) {
    context.replace(path);
  }
}
```

Example typed route implementations:

```dart
class HomeRoute extends AppRoute {
  @override
  String get path => '/';
}

class UserDetailsRoute extends AppRoute {
  final String login;
  
  UserDetailsRoute(this.login);
  
  @override
  String get path => '/$login';
}
```

### 4. Screen Module Structure

Each screen module will contain:
- `*_screen.dart` - The screen widget
- `*_viewmodel.dart` - The ViewModel class (not injectable)
- `*_viewmodel_factory.dart` - Injectable factory for creating ViewModels
- `*_route_provider.dart` - Injectable route configuration provider

### 5. Example Factory Implementation

```dart
@injectable()
class HomeViewModelFactory {
  final Client _ferryClient;
  
  HomeViewModelFactory(this._ferryClient);
  
  HomeViewModel create() {
    return HomeViewModel(_ferryClient);
  }
}
```

### 6. Example Route Provider Implementation

```dart
@injectable(as: RouteProvider)
class HomeRouteProvider implements RouteProvider {
  final HomeViewModelFactory _homeViewModelFactory;
  final AuthViewModel _authViewModel;
  
  HomeRouteProvider(this._homeViewModelFactory, this._authViewModel);
  
  @override
  RouteBase getRoute() {
    return GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(
        authViewModel: _authViewModel,
        homeViewModel: _homeViewModelFactory.create(),
      ),
    );
  }
}
```

## Data Models

### ViewModel Lifecycle Management

ViewModels will implement a disposal pattern:

```dart
abstract class DisposableViewModel {
  void dispose();
}
```

Screen widgets will be responsible for disposing ViewModels when they're removed from the widget tree:

```dart
class HomeScreen extends StatefulWidget {
  final HomeViewModel homeViewModel;
  
  @override
  void dispose() {
    homeViewModel.dispose();
    super.dispose();
  }
}
```

### Route Configuration Model

```dart
class RouteConfiguration {
  final List<RouteBase> routes;
  final String? initialLocation;
  final GoRouterRedirect? redirect;
  
  RouteConfiguration({
    required this.routes,
    this.initialLocation,
    this.redirect,
  });
}
```

## Error Handling

### Factory Creation Errors

- Factory classes will handle dependency injection errors gracefully
- Missing dependencies will be caught at DI configuration time
- Runtime factory errors will be logged and fallback to error screens

### Route Resolution Errors

- Invalid routes will be caught during route collection
- Duplicate route paths will be detected and reported
- Missing route providers will not break the app initialization

### ViewModel Disposal Errors

- Disposal errors will be logged but not crash the app
- Memory leaks will be monitored through proper disposal patterns
- Subscription cleanup will be enforced in ViewModel base classes

## Testing Strategy

### Unit Testing

1. **Factory Testing**: Test that factories create ViewModels with correct dependencies
2. **Route Provider Testing**: Test that route providers return valid route configurations
3. **ViewModel Testing**: Test ViewModels in isolation using mocked dependencies

### Integration Testing

1. **Navigation Testing**: Test that navigation works correctly with the new architecture
2. **Lifecycle Testing**: Test that ViewModels are created and disposed properly
3. **DI Integration Testing**: Test that the dependency injection system works with factories

### Widget Testing

1. **Screen Testing**: Test screens with mocked ViewModels
2. **Factory Integration**: Test that screens work with real factories
3. **Route Testing**: Test that routes resolve to correct screens

## Implementation Details

### Phase 1: Core Infrastructure

1. Create base interfaces (`ViewModelFactory`, `RouteProvider`)
2. Create route collection service that gathers routes from all providers
3. Update `Gh3App` to use dynamic route collection

### Phase 2: Screen Module Refactoring

1. Convert existing ViewModels to use factory pattern
2. Create route providers for each screen
3. Remove direct screen imports from `Gh3App`

### Phase 3: Lifecycle Management

1. Implement proper ViewModel disposal
2. Add memory leak detection
3. Optimize factory performance

### Dependency Injection Changes

The DI configuration will change from:
```dart
// Current - ViewModel registered directly
@injectable
class HomeViewModel extends ChangeNotifier { ... }
```

To:
```dart
// New - Only factory registered
@injectable
class HomeViewModelFactory { ... }

// ViewModel not registered with DI
class HomeViewModel extends ChangeNotifier { ... }
```

### Route Collection Service

```dart
@injectable
class RouteCollectionService {
  RouteCollectionService();
  
  List<RouteBase> collectRoutes() {
    final routeProviders = getIt.getAll<RouteProvider>();
    return routeProviders
        .map((provider) => provider.getRoute())
        .toList();
  }
}
```

This design ensures that the architecture is modular, scalable, and maintains proper separation of concerns while working seamlessly with Flutter's navigation system and the existing dependency injection setup.