# Implementation Plan

- [ ] 1. Create reusable UI components for home screen layout
  - Create SectionHeader widget for consistent section title styling
  - Create WorkItemListTile widget for Material 3 ListView items displaying work items
  - Create CurrentUserCard widget for current user profile display
  - _Requirements: 1.2, 2.2, 3.1, 3.9_

- [ ] 2. Refactor HomeScreen to use scrollable layout with SliverAppBar
  - Replace current Scaffold with CustomScrollView and SliverAppBar implementation
  - Implement SliverPadding with SliverList for page content structure
  - Configure SliverAppBar with floating, snap, and pinned properties as specified in design
  - _Requirements: 1.4_

- [ ] 3. Implement "My profile" section in HomeScreen
  - Add "My profile" section header using SectionHeader widget
  - Integrate CurrentUserCard widget to display current user information
  - Remove existing "Following" section and related UI components
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 4. Implement "My work" section with static work items
  - Add "My work" section header using SectionHeader widget
  - Create static list of 7 work items (Issues, Pull requests, Discussions, Projects, Repositories, Organizations, Starred)
  - Implement each work item using WorkItemListTile with appropriate icons and titles
  - Ensure work items have no navigation functionality (placeholder only)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10_

- [ ] 5. Update HomeViewModel to support new home screen requirements
  - Remove existing following users GraphQL functionality and related methods
  - Simplify ViewModel to focus on current user data access through AuthService
  - Add properties for current user name, login, and avatar URL
  - Remove pagination, loading states, and error handling related to following users
  - _Requirements: 2.2, 2.3_

- [ ] 6. Update HomeViewModelFactory dependencies
  - Replace Ferry client dependency with AuthService dependency
  - Update factory create method to pass AuthService to HomeViewModel constructor
  - Ensure proper dependency injection registration
  - _Requirements: 2.2_

- [ ] 7. Write comprehensive tests for new home screen implementation
  - Write unit tests for HomeViewModel with AuthService integration
  - Write unit tests for HomeViewModelFactory with updated dependencies
  - Write widget tests for HomeScreen with SliverAppBar and CustomScrollView layout
  - Write widget tests for SectionHeader, WorkItemListTile, and CurrentUserCard components
  - Write integration tests for home screen navigation and route handling
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1-3.10_