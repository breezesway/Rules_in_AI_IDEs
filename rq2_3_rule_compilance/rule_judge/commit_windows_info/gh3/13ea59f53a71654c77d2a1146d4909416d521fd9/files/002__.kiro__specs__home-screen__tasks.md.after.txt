# Implementation Plan

- [x] 1. Create reusable UI components for home screen layout
  - [x] 1.1 Create SectionHeader widget for consistent section title styling
    - Implemented SectionHeader widget with Material 3 titleLarge styling
    - Widget accepts title parameter and applies bold font weight
    - _Requirements: 1.2, 2.2, 3.1, 3.9_
    
  - [x] 1.2 Create WorkItemListTile widget for Material 3 ListView items displaying work items
    - Implemented WorkItemListTile with icon, title, and trailing arrow
    - Uses Material 3 color scheme for consistent theming
    - Includes onTap parameter for future navigation functionality
    - _Requirements: 1.2, 2.2, 3.1, 3.9_
    
  - [x] 1.3 Create CurrentUserCard widget for current user profile display
    - Implemented Card-based user profile display with avatar, name, and login
    - Handles null avatar with fallback person icon
    - Placeholder implementation with no navigation functionality
    - _Requirements: 1.2, 2.2, 3.1, 3.9_

- [x] 2. Refactor HomeScreen to use scrollable layout with SliverAppBar
  - [x] 2.1 Replace current Scaffold with CustomScrollView and SliverAppBar implementation
    - Replaced existing ListView-based layout with CustomScrollView
    - Implemented SliverAppBar with floating, snap, and pinned properties
    - Maintained logout functionality in app bar actions
    - _Requirements: 1.4_
    
  - [x] 2.2 Implement SliverPadding with SliverList for page content structure
    - Wrapped content in SliverPadding with 16px padding
    - Used SliverChildListDelegate for static content list
    - Structured content with proper spacing between sections
    - _Requirements: 1.4_

- [x] 3. Implement "My profile" section in HomeScreen
  - [x] 3.1 Add "My profile" section header using SectionHeader widget
    - Added SectionHeader with "My profile" title
    - Positioned at top of content after app bar
    - _Requirements: 2.1, 2.2, 2.3_
    
  - [x] 3.2 Integrate CurrentUserCard widget to display current user information
    - Added CurrentUserCard with placeholder user data from HomeViewModel
    - Connected to ViewModel properties for name, login, and avatar
    - _Requirements: 2.1, 2.2, 2.3_
    
  - [x] 3.3 Remove existing "Following" section and related UI components
    - Removed entire following users list and related state management
    - Removed welcome card and following section header
    - Removed pagination and error handling UI components
    - _Requirements: 2.1, 2.2, 2.3_

- [x] 4. Implement "My work" section with static work items
  - [x] 4.1 Add "My work" section header using SectionHeader widget
    - Added SectionHeader with "My work" title below profile section
    - Proper spacing maintained between sections
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10_
    
  - [x] 4.2 Create static list of 7 work items with appropriate icons and titles
    - Issues with bug_report icon
    - Pull requests with call_merge icon
    - Discussions with forum icon
    - Projects with folder_open icon
    - Repositories with source icon
    - Organizations with business icon
    - Starred with star icon
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10_
    
  - [x] 4.3 Implement each work item using WorkItemListTile with no navigation functionality
    - All work items implemented as WorkItemListTile widgets
    - No onTap handlers specified (placeholder only)
    - Consistent Material 3 styling applied
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10_

- [x] 5. Update HomeViewModel to support new home screen requirements
  - [x] 5.1 Remove existing following users GraphQL functionality and related methods
    - Removed Ferry client dependency and GraphQL imports
    - Removed all following users related properties and methods
    - Removed pagination, loading states, and error handling
    - _Requirements: 2.2, 2.3_
    
  - [x] 5.2 Simplify ViewModel to focus on current user data access through AuthService
    - Updated constructor to accept AuthService instead of Ferry client
    - Added placeholder properties for current user data
    - Simplified ViewModel to core user data access only
    - _Requirements: 2.2, 2.3_

- [x] 6. Update HomeViewModelFactory dependencies
  - [x] 6.1 Replace Ferry client dependency with AuthService dependency
    - Updated constructor to inject AuthService instead of Ferry client
    - Updated create method to pass AuthService to HomeViewModel
    - Maintained @injectable annotation for dependency injection
    - _Requirements: 2.2_

- [x] 7. Write comprehensive tests for new home screen implementation
  - [x] 7.1 Write unit tests for HomeViewModel with AuthService integration
    - Created unit tests for HomeViewModel covering disposal and placeholder user data
    - Tests verify proper lifecycle management and data properties
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1-3.10_
    
  - [x] 7.2 Write unit tests for HomeViewModelFactory with updated dependencies
    - Updated factory tests to use AuthService instead of Ferry client
    - Tests verify proper dependency injection and factory pattern
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1-3.10_
    
  - [x] 7.3 Write widget tests for SectionHeader, WorkItemListTile, and CurrentUserCard components
    - Created comprehensive widget tests for all three components
    - Used mocktail_image_network to handle NetworkImage testing
    - Tests cover styling, theming, user interaction, and edge cases
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1-3.10_
    
  - [x] 7.4 Write integration tests for HomeScreen with SliverAppBar and CustomScrollView layout
    - Created integration tests for complete HomeScreen functionality
    - Tests verify SliverAppBar behavior, scrolling, and all content sections
    - Includes tests for user profile display and all 7 work items
    - Tests verify logout functionality and navigation structure
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 3.1-3.10_