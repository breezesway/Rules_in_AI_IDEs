# Implementation Plan

- [x] 1. Set up core infrastructure and base interfaces
  - Create base route class with navigation methods (push, go, replace)
  - Create RouteProvider interface for modular route configuration
  - Create RouteCollectionService to gather routes from all providers via DI
  - _Requirements: 2.2, 2.3, 5.3, 5.4_

- [x] 2. Create typed route classes for existing screens
  - [x] 2.1 Create HomeRoute class extending AppRoute
    - Implement path property returning '/'
    - Write unit tests for HomeRoute navigation methods
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [x] 2.2 Create LoginRoute class extending AppRoute
    - Implement path property returning '/login'
    - Write unit tests for LoginRoute navigation methods
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [x] 2.3 Create LoadingRoute class extending AppRoute
    - Implement path property returning '/loading'
    - Write unit tests for LoadingRoute navigation methods
    - _Requirements: 5.1, 5.2, 5.5_
  
  - [x] 2.4 Create UserDetailsRoute class extending AppRoute with username parameter
    - Implement constructor accepting String login parameter
    - Implement path property returning '/$login'
    - Write unit tests for UserDetailsRoute with different usernames
    - _Requirements: 5.1, 5.2, 5.5_

- [x] 3. Convert ViewModels to factory pattern
  - [x] 3.1 Create HomeViewModelFactory
    - Remove @injectable annotation from HomeViewModel
    - Create injectable HomeViewModelFactory with create() method
    - Update HomeViewModel to not be registered with DI
    - Write unit tests for factory creation and dependency injection
    - _Requirements: 1.1, 1.4, 1.5, 4.1, 4.2_
  
  - [x] 3.2 Create LoginViewModelFactory
    - Create injectable LoginViewModelFactory with create() method accepting required dependencies
    - Update LoginViewModel to not be registered with DI
    - Write unit tests for factory creation with multiple dependencies
    - _Requirements: 1.1, 1.4, 1.5, 4.1, 4.2_
  
  - [x] 3.3 Create UserDetailsViewModelFactory (if needed)
    - Created placeholder UserDetailsViewModel with login parameter
    - Create injectable factory with create(String login) method
    - Updated UserDetailsScreen to use ViewModel pattern
    - Write unit tests for parameterized factory creation
    - _Requirements: 1.1, 1.4, 1.5, 4.1, 4.2_

- [ ] 4. Create route providers for each screen module
  - [ ] 4.1 Create HomeRouteProvider
    - Implement RouteProvider interface
    - Inject HomeViewModelFactory and AuthViewModel dependencies
    - Create GoRoute configuration using factory.create() for ViewModel instantiation
    - Write unit tests for route provider configuration
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [ ] 4.2 Create LoginRouteProvider
    - Implement RouteProvider interface with LoginViewModelFactory
    - Configure GoRoute with proper dependency injection
    - Write unit tests for login route configuration
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [ ] 4.3 Create LoadingRouteProvider
    - Implement RouteProvider interface for loading screen
    - Configure GoRoute with AuthViewModel dependency
    - Write unit tests for loading route configuration
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [ ] 4.4 Create UserDetailsRouteProvider
    - Implement RouteProvider interface with parameterized route
    - Configure GoRoute to extract login from path parameters
    - Use UserDetailsViewModelFactory.create(login) for ViewModel creation
    - Write unit tests for parameterized route handling
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 5. Implement ViewModel lifecycle management
  - [ ] 5.1 Add disposal pattern to ViewModels
    - Ensure all ViewModels properly implement dispose() method
    - Update screen widgets to dispose ViewModels in dispose() lifecycle
    - Write tests to verify proper cleanup of subscriptions and resources
    - _Requirements: 1.3, 4.3, 4.5_
  
  - [ ] 5.2 Update screen widgets for proper ViewModel lifecycle
    - Modify HomeScreen to dispose HomeViewModel instance
    - Modify LoginScreen to dispose LoginViewModel instance
    - Modify UserDetailsScreen to dispose ViewModel instance
    - Write widget tests to verify disposal is called
    - _Requirements: 1.3, 4.3, 4.5_

- [ ] 6. Refactor Gh3App to use dynamic route collection
  - [ ] 6.1 Update Gh3App to use RouteCollectionService
    - Remove direct screen widget imports from Gh3App
    - Inject RouteCollectionService and use collectRoutes() method
    - Remove hardcoded GoRoute configurations
    - Maintain existing redirect logic for authentication
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  
  - [ ] 6.2 Update dependency injection configuration
    - Register all route providers with @injectable annotation
    - Register all ViewModel factories with @injectable annotation
    - Remove ViewModel registrations from DI configuration
    - Run build_runner to regenerate DI configuration
    - _Requirements: 1.5, 4.1, 4.4_

- [ ] 7. Integration testing and validation
  - [ ] 7.1 Test navigation flow with new architecture
    - Write integration tests for complete navigation flows
    - Verify multiple screen instances work correctly in navigation stack
    - Test that ViewModels are properly created and disposed
    - Validate that route parameters are correctly passed
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ] 7.2 Test DI integration with factories
    - Verify all factories are properly registered and injectable
    - Test that services maintain singleton lifecycle while ViewModels are factory-created
    - Write tests for error handling in factory creation
    - _Requirements: 4.1, 4.2, 4.4_
  
  - [ ] 7.3 Validate modular architecture
    - Test that screens are self-contained modules
    - Verify that adding/removing route providers works via DI
    - Test that main app has no direct screen dependencies
    - _Requirements: 2.2, 2.3, 3.1, 3.4_