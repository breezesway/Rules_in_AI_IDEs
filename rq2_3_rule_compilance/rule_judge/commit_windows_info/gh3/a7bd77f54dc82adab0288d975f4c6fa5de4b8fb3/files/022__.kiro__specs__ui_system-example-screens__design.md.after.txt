# UI System Example Screens & Navigation Design

## Overview

This design document outlines the architecture and implementation approach for Phase 3 of the UI system: Complete Example Screens & Navigation. This phase creates a comprehensive GitHub mobile app experience using the foundation and widgets built in previous phases, delivering a standalone demo application that showcases the complete design system capabilities.

## Architecture

### Application Structure

The Phase 3 implementation follows a modular architecture that builds upon the existing UI system foundation:

```
lib/src/ui-system/
├── example_screens/          # Complete GitHub app screens
│   ├── home_screen_example.dart
│   ├── user_profile_example.dart
│   ├── repository_details_example.dart
│   ├── repository_tree_example.dart
│   ├── repository_file_example.dart
│   ├── issues_list_example.dart
│   ├── issue_detail_example.dart
│   ├── pulls_list_example.dart
│   ├── pull_detail_example.dart
│   └── search_example.dart
├── navigation/               # Navigation system
│   ├── ui_system_app.dart
│   ├── example_routes.dart
│   └── navigation_service.dart
├── data/                    # Enhanced fake data system
│   ├── fake_data_service.dart (enhanced)
│   ├── fake_repositories.dart
│   ├── fake_users.dart
│   ├── fake_issues.dart
│   ├── fake_files.dart
│   └── fake_activity.dart
└── main_ui_system.dart      # Standalone demo entry point
```

### Navigation Architecture

The navigation system uses a simplified routing approach optimized for demonstration purposes:

#### Route Structure
```dart
class ExampleRoutes {
  static const String home = '/';
  static const String userProfile = '/user/:username';
  static const String repository = '/repo/:owner/:name';
  static const String repositoryTree = '/repo/:owner/:name/tree';
  static const String repositoryFile = '/repo/:owner/:name/file';
  static const String issues = '/repo/:owner/:name/issues';
  static const String issueDetail = '/repo/:owner/:name/issue/:number';
  static const String pulls = '/repo/:owner/:name/pulls';
  static const String pullDetail = '/repo/:owner/:name/pull/:number';
  static const String search = '/search';
}
```

#### Navigation Service
```dart
class NavigationService {
  static final GoRouter router = GoRouter(
    initialLocation: ExampleRoutes.home,
    routes: [
      // Route definitions with proper parameter handling
    ],
  );
  
  // Navigation helper methods
  static void navigateToUser(String username) { ... }
  static void navigateToRepository(String owner, String name) { ... }
  static void navigateToIssue(String owner, String name, int number) { ... }
}
```

## Components and Interfaces

### Example Screen Components

#### 1. Home Screen Example
**Purpose**: Authenticated GitHub dashboard with personalized content

**Key Components**:
- User profile summary card
- Quick action navigation grid (2x2 layout)
- Recent activity feed with time-based grouping
- Trending repositories section
- Global search bar

**Layout Structure**:
```dart
GHScreenTemplate(
  title: "GitHub",
  actions: [NotificationButton(), ProfileButton()],
  body: GHListTemplate(
    searchHint: "Search repositories, users, issues...",
    onRefresh: () => _refreshFeed(),
    children: [
      UserSummaryCard(),
      QuickActionsGrid(),
      ActivityFeedSection(),
      TrendingSection(),
    ],
  ),
)
```

#### 2. User Profile Example
**Purpose**: Comprehensive user profile with tabbed navigation

**Key Components**:
- Large user header with complete profile information
- Tabbed navigation (repositories, starred, organizations, etc.)
- Repository list with search and filtering
- Follow/unfollow actions with optimistic updates

**Tab Implementation**:
```dart
GHTabMenu(
  tabs: [
    TabItem(title: "Repositories", badge: "${user.publicRepos}"),
    TabItem(title: "Starred", badge: "${user.starredRepos}"),
    TabItem(title: "Organizations", badge: "${user.organizations.length}"),
    TabItem(title: "Projects"),
    TabItem(title: "Packages"),
    TabItem(title: "Gists"),
  ],
  onTabChanged: (index) => _switchTab(index),
)
```

#### 3. Repository Details Example
**Purpose**: Complete repository overview with navigation to sub-sections

**Key Components**:
- Repository entity header with stats and actions
- Navigation menu for different repository sections
- README markdown viewer
- Recent releases and contributors sections
- Star/watch/fork actions

#### 4. Repository File Browser Example
**Purpose**: File tree navigation and code viewing

**Key Components**:
- Breadcrumb navigation
- File tree with proper icons and metadata
- Code viewer with syntax highlighting
- Copy-to-clipboard functionality

#### 5. Issues and Pull Requests Examples
**Purpose**: Issue/PR management and viewing

**Key Components**:
- Filterable lists with status indicators
- Advanced search and filtering
- Detail views with comments and reactions
- Status badges and label chips

### Enhanced Fake Data System

#### Data Models
```dart
class FakeUser {
  final String login;
  final String? name;
  final String? bio;
  final String avatarUrl;
  final String? location;
  final String? company;
  final String? website;
  final int publicRepos;
  final int followers;
  final int following;
  final DateTime createdAt;
  final List<String> organizations;
}

class FakeRepository {
  final String owner;
  final String name;
  final String? description;
  final String? language;
  final Color? languageColor;
  final int starCount;
  final int forkCount;
  final int watcherCount;
  final bool isPrivate;
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<String> topics;
  final String? license;
  final String? homepage;
  final List<FakeFile> files;
  final List<FakeIssue> issues;
  final List<FakeRelease> releases;
}

class FakeIssue {
  final int number;
  final String title;
  final String? body;
  final IssueStatus status;
  final FakeUser author;
  final DateTime createdAt;
  final DateTime? closedAt;
  final List<String> labels;
  final FakeUser? assignee;
  final int commentCount;
  final List<FakeComment> comments;
}
```

#### Data Generation Strategy
```dart
class FakeDataService {
  // Generate realistic data sets
  static List<FakeUser> generateUsers(int count) { ... }
  static List<FakeRepository> generateRepositories(int count) { ... }
  static List<FakeIssue> generateIssues(int count) { ... }
  
  // Search and filtering
  List<FakeRepository> searchRepositories(String query) { ... }
  List<FakeUser> searchUsers(String query) { ... }
  List<FakeIssue> filterIssues(IssueFilter filter) { ... }
  
  // Realistic data relationships
  List<FakeRepository> getUserRepositories(String username) { ... }
  List<FakeRepository> getUserStarredRepos(String username) { ... }
  List<FakeIssue> getRepositoryIssues(String owner, String name) { ... }
}
```

## Data Models

### Screen State Management

Each example screen follows a consistent state management pattern:

```dart
class ExampleScreenState {
  final bool isLoading;
  final String? error;
  final dynamic data;
  final Map<String, dynamic> filters;
  final String searchQuery;
  
  ExampleScreenState({
    this.isLoading = false,
    this.error,
    this.data,
    this.filters = const {},
    this.searchQuery = '',
  });
}
```

### Navigation State

```dart
class NavigationState {
  final String currentRoute;
  final Map<String, String> parameters;
  final Map<String, String> queryParameters;
  final List<String> history;
  
  NavigationState({
    required this.currentRoute,
    this.parameters = const {},
    this.queryParameters = const {},
    this.history = const [],
  });
}
```

## Error Handling

### Error Types and Recovery

```dart
enum ExampleError {
  networkError,
  dataNotFound,
  invalidParameters,
  searchTimeout,
  navigationError,
}

class ErrorHandler {
  static Widget buildErrorState(ExampleError error, VoidCallback onRetry) {
    return GHErrorState(
      title: _getErrorTitle(error),
      message: _getErrorMessage(error),
      onRetry: onRetry,
    );
  }
}
```

### Loading States

```dart
class LoadingStateManager {
  static Widget buildLoadingState(String context) {
    return GHLoadingIndicator(
      message: _getLoadingMessage(context),
    );
  }
  
  static Widget buildSkeletonLoader(SkeletonType type) {
    switch (type) {
      case SkeletonType.repositoryCard:
        return RepositoryCardSkeleton();
      case SkeletonType.userProfile:
        return UserProfileSkeleton();
      // ... other skeleton types
    }
  }
}
```

## Testing Strategy

### Test Structure

```
test/src/ui-system/
├── example_screens/
│   ├── home_screen_example_test.dart
│   ├── user_profile_example_test.dart
│   ├── repository_details_example_test.dart
│   └── ...
├── navigation/
│   ├── navigation_service_test.dart
│   └── example_routes_test.dart
├── data/
│   ├── fake_data_service_test.dart
│   └── data_generation_test.dart
└── integration/
    ├── full_navigation_test.dart
    ├── search_functionality_test.dart
    └── user_flows_test.dart
```

### Testing Approaches

#### Unit Tests
- Individual screen widget testing
- Fake data service functionality
- Navigation helper methods
- Search and filtering logic

#### Widget Tests
- Complete screen rendering
- User interaction simulation
- State management verification
- Error and loading state handling

#### Integration Tests
- End-to-end navigation flows
- Cross-screen data consistency
- Search and filtering across screens
- Performance with large data sets

### Test Data Management

```dart
class TestDataFactory {
  static FakeUser createTestUser({String? login}) { ... }
  static FakeRepository createTestRepository({String? name}) { ... }
  static List<FakeIssue> createTestIssues(int count) { ... }
  
  // Realistic test scenarios
  static TestScenario createUserWithManyRepos() { ... }
  static TestScenario createRepositoryWithIssues() { ... }
  static TestScenario createEmptyUserProfile() { ... }
}
```

## Performance Considerations

### Rendering Optimization

```dart
class PerformanceOptimizations {
  // Efficient list rendering
  static Widget buildOptimizedList<T>(
    List<T> items,
    Widget Function(T item) itemBuilder,
  ) {
    return ListView.builder(
      itemCount: items.length,
      itemBuilder: (context, index) => itemBuilder(items[index]),
      // Add performance optimizations
    );
  }
  
  // Image caching for avatars
  static Widget buildCachedAvatar(String url) {
    return CachedNetworkImage(
      imageUrl: url,
      placeholder: (context, url) => CircularProgressIndicator(),
      errorWidget: (context, url, error) => Icon(Icons.error),
    );
  }
}
```

### Memory Management

```dart
class MemoryManager {
  // Dispose resources properly
  static void disposeScreen(StatefulWidget screen) { ... }
  
  // Limit data retention
  static void limitDataCache(int maxItems) { ... }
  
  // Efficient search indexing
  static SearchIndex buildSearchIndex(List<dynamic> data) { ... }
}
```

## Accessibility Implementation

### Screen Reader Support

```dart
class AccessibilityHelper {
  static Widget makeAccessible(Widget child, String semanticLabel) {
    return Semantics(
      label: semanticLabel,
      child: child,
    );
  }
  
  static String generateScreenReaderText(dynamic data) { ... }
}
```

### Touch Target Compliance

```dart
class TouchTargetHelper {
  static const double minTouchTarget = 48.0;
  
  static Widget ensureTouchTarget(Widget child) {
    return Container(
      constraints: BoxConstraints(
        minWidth: minTouchTarget,
        minHeight: minTouchTarget,
      ),
      child: child,
    );
  }
}
```

## Platform Considerations

### Cross-Platform Compatibility

The example screens are designed to work seamlessly across all Flutter platforms:

- **Web**: Optimized for browser navigation and URL handling
- **iOS**: Native iOS navigation patterns and gestures
- **Android**: Material Design 3 compliance and Android-specific behaviors
- **Desktop**: Keyboard navigation and window management

### Responsive Design

```dart
class ResponsiveHelper {
  static bool isTablet(BuildContext context) {
    return MediaQuery.of(context).size.width > 600;
  }
  
  static Widget buildResponsiveLayout(
    BuildContext context,
    Widget mobile,
    Widget tablet,
  ) {
    return isTablet(context) ? tablet : mobile;
  }
}
```

## Integration Guidelines

### Using Example Screens as Templates

The example screens serve as reference implementations for production code:

1. **Component Usage**: Demonstrates proper use of UI system components
2. **State Management**: Shows effective state management patterns
3. **Navigation Integration**: Provides navigation implementation examples
4. **Data Handling**: Illustrates data loading and error handling patterns
5. **Testing Approaches**: Offers comprehensive testing examples

### Customization Points

```dart
class CustomizationOptions {
  // Theme customization
  static ThemeData customizeTheme(ThemeData base) { ... }
  
  // Component customization
  static Widget customizeComponent(Widget base, CustomizationConfig config) { ... }
  
  // Navigation customization
  static GoRouter customizeNavigation(List<RouteBase> additionalRoutes) { ... }
}
```

This design provides a comprehensive foundation for implementing complete GitHub mobile app screens that showcase the full capabilities of the UI system while maintaining high performance, accessibility, and code quality standards.