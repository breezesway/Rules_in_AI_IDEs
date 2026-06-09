# Implementation Plan

- [x] 1. Ferry Setup and Configuration
  - [x] 1.1 Configure Ferry dependencies
    - Add ferry, gql_http_link to dependencies
    - Add ferry_generator, build_runner to dev_dependencies  
    - Configure build.yaml with ferry_generator settings
    - Set up GitHub GraphQL schema file (lib/github_schema.graphql)
    - _Requirements: 1_

  - [x] 1.2 Create FerryClientService with Injectable
    - Implement @singleton FerryClientService class
    - Configure HTTP link with GitHub GraphQL endpoint (https://api.github.com/graphql)
    - Set up authentication link with automatic token injection from ITokenStorage
    - Register Ferry client with Injectable dependency injection
    - _Requirements: 1, 3_

  - [x] 1.3 Implement authentication integration
    - Create authentication link for automatic Bearer token injection
    - Integrate with existing ITokenStorage for token management
    - Handle token refresh scenarios and automatic header updates
    - Implement authentication error handling for GraphQL operations
    - _Requirements: 1, 4_

- [x] 2. GraphQL Operations and Code Generation
  - [x] 2.1 Set up colocated GraphQL structure
    - Configure ferry_builder to find .graphql files in lib/**/*.graphql
    - Set up code generation to create .graphql.dart files next to .graphql files
    - Create screen-level and widget-level colocation pattern
    - Test build process with flutter packages pub run build_runner build
    - _Requirements: 2_

  - [x] 2.2 Create HomeViewModel GraphQL operations
    - Create lib/src/screens/home_screen/home_viewmodel.graphql
    - Define GetFollowing query with pagination support
    - Include UserCardFragment for UI component data needs
    - Generate home_viewmodel.graphql.dart with ferry_builder
    - _Requirements: 2_

  - [x] 2.3 Create UserDetailsViewModel GraphQL operations
    - Create lib/src/screens/user_details/user_details_viewmodel.graphql
    - Define GetUserDetails and GetUserRepositories queries
    - Include UserProfileFragment and RepositoryCardFragment
    - Generate user_details_viewmodel.graphql.dart
    - _Requirements: 2_

  - [x] 2.4 Create UI component fragments
    - Create lib/src/widgets/user_card/user_card.graphql with UserCardFragment
    - Create lib/src/widgets/repository_card/repository_card.graphql with RepositoryCardFragment
    - Create lib/src/widgets/user_profile/user_profile.graphql with UserProfileFragment
    - Generate corresponding .graphql.dart files
    - _Requirements: 2_

- [ ] 3. ViewModel Integration with Injectable
  - [ ] 3.1 Update HomeViewModel for Injectable + Ferry
    - Add @injectable annotation to HomeViewModel
    - Inject Ferry Client through constructor
    - Use GetFollowing query from home_viewmodel.graphql.dart
    - Implement reactive streams for GraphQL data
    - Maintain screen-based modular architecture pattern
    - _Requirements: 3_

  - [ ] 3.2 Update UserDetailsViewModel for Injectable + Ferry
    - Add @injectable annotation to UserDetailsViewModel
    - Inject Ferry Client through constructor
    - Use queries from user_details_viewmodel.graphql.dart
    - Implement separate streams for user profile and repositories
    - Follow same error handling patterns as REST APIs
    - _Requirements: 3_

  - [ ] 3.3 Update UI components to consume GraphQL fragments
    - Update UserCard to consume UserCardFragment directly
    - Update RepositoryCard to consume RepositoryCardFragment directly
    - Update UserProfile to consume UserProfileFragment directly
    - Remove intermediate model classes - use GraphQL types directly
    - _Requirements: 3_

- [ ] 4. Comprehensive Error Handling
  - [ ] 4.1 Implement GraphQL error type system
    - Create GraphQLError base class with message and code
    - Create GraphQLNetworkError for HTTP/connectivity issues
    - Create GraphQLAuthenticationError for 401/403 responses  
    - Create GraphQLRateLimitError with GitHub rate limit header handling
    - Create GraphQLOfflineError for network connectivity issues
    - _Requirements: 4_

  - [ ] 4.2 Create GraphQLErrorHandler utility
    - Implement processException method to categorize OperationException types
    - Handle linkException for network/HTTP errors
    - Process graphqlErrors for GraphQL-specific failures
    - Parse GitHub rate limit headers (x-ratelimit-reset)
    - Treat GraphQL responses with errors as complete failures (no partial data)
    - _Requirements: 4_

  - [ ] 4.3 Implement error handling in ViewModels  
    - Add error processing in all GraphQL ViewModels
    - Provide specific error types and appropriate user feedback
    - Handle offline scenarios with appropriate error messages
    - Maintain consistent error handling patterns across ViewModels
    - _Requirements: 4_

- [ ] 5. Testing Implementation
  - [ ] 5.1 Create unit tests for ViewModels
    - Set up MockFerryClient for isolated testing
    - Test successful GraphQL query scenarios
    - Test authentication error scenarios with proper error types
    - Test rate limiting error scenarios with reset time handling
    - Test offline error scenarios with network exceptions
    - _Requirements: 5_

  - [ ] 5.2 Implement GraphQL integration tests
    - Test Ferry client configuration and initialization
    - Test schema validation and generated code correctness
    - Test fragment composition and dependencies
    - Test authentication link integration with ITokenStorage
    - _Requirements: 5_

  - [ ] 5.3 Add error injection testing capabilities
    - Test simulated network conditions and error injection
    - Test offline behavior scenarios
    - Implement error scenario debugging
    - _Requirements: 5_