# Requirements Document

## Introduction

This feature focuses on refactoring the current navigation and dependency injection architecture to support a more modular, scalable approach. The current implementation has architectural limitations where the main app holds references to all screens and viewmodels, and viewmodels are registered as singletons rather than factories, which doesn't work well with stack navigation where multiple instances of screens can exist simultaneously.

## Requirements

### Requirement 1

**User Story:** As a developer, I want ViewModels to be created as factories rather than singletons, so that multiple instances of the same screen can exist independently in the navigation stack.

#### Acceptance Criteria

1. WHEN a screen is pushed onto the navigation stack THEN a new ViewModel instance SHALL be created for that screen
2. WHEN multiple instances of the same screen exist in the stack THEN each SHALL have its own independent ViewModel instance
3. WHEN a screen is popped from the stack THEN its ViewModel instance SHALL be properly disposed
4. IF a ViewModel has dependencies THEN the factory SHALL inject those dependencies into each new instance
5. WHEN registering with dependency injection THEN only ViewModel factory classes SHALL be registered, not the ViewModels themselves

### Requirement 2

**User Story:** As a developer, I want routing configuration to be distributed to individual screen modules, so that each screen becomes self-contained and the architecture scales better.

#### Acceptance Criteria

1. WHEN defining routes THEN each screen module SHALL contain its own route configuration
2. WHEN the app initializes THEN route configurations SHALL be collected from all screen modules automatically via DI
3. WHEN the app builds routes THEN it SHALL discover screen modules automatically through dependency injection

### Requirement 3

**User Story:** As a developer, I want the main app (gh3_app) to not hold direct references to all screens and viewmodels, so that the architecture is more loosely coupled and maintainable.

#### Acceptance Criteria

1. WHEN the main app is initialized THEN it SHALL not import individual screen widgets directly
2. WHEN routing occurs THEN screen widgets SHALL be resolved dynamically through the routing system
3. WHEN the app builds routes THEN it SHALL discover screen modules automatically
4. IF a screen module is removed THEN the main app SHALL continue to function without modification

### Requirement 4

**User Story:** As a developer, I want the dependency injection system to support factory pattern for ViewModel creation while maintaining proper lifecycle management, so that resources are used efficiently.

#### Acceptance Criteria

1. WHEN a ViewModel factory class is registered with DI THEN it SHALL be injectable (e.g., HomeViewModelFactory)
2. WHEN a ViewModel factory's create method is called THEN it SHALL return a new ViewModel instance with injected dependencies
3. WHEN a ViewModel is no longer needed THEN it SHALL be properly disposed to prevent memory leaks
4. WHEN services are injected into ViewModels THEN they SHALL maintain their appropriate lifecycle (singleton for services, factory for ViewModels)
5. IF a ViewModel implements Disposable THEN it SHALL be automatically disposed when the screen is removed

### Requirement 5

**User Story:** As a developer, I want typed route classes for type-safe navigation, so that navigation is more reliable and easier to maintain.

#### Acceptance Criteria

1. WHEN defining a screen THEN it SHALL have a corresponding typed route class (e.g., HomeRoute(), UserDetailsRoute(String login))
2. WHEN a route class is created THEN it SHALL have a method to generate the URI path
3. WHEN navigating THEN route classes SHALL provide methods like push(context), go(context), replace(context)
4. WHEN route classes are defined THEN they SHALL extend a base route class that provides common navigation methods
5. IF a route requires parameters THEN those SHALL be type-safe constructor parameters
