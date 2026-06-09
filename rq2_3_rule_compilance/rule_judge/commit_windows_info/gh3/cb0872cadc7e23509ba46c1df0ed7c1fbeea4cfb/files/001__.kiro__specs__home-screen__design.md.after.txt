# Home Screen Technical Design

## 1. Architecture Overview

The home screen follows the modular screen architecture pattern with complete separation of concerns:
- **HomeScreen** - UI layer with Scaffold and layout
- **HomeViewModel** - Business logic and state management  
- **HomeViewModelFactory** - Dependency injection for ViewModel creation
- **HomeRouteProvider** - Route creation and navigation integration
- **HomeRoute** - Typed route class extending AppRoute

## 2. Component Structure

### 2.1 Screen Module Organization
```
lib/src/screens/home_screen/
├── home_screen.dart           # Main screen widget
├── home_viewmodel.dart        # State management and business logic
├── home_viewmodel_factory.dart # ViewModel factory for DI
├── home_route_provider.dart   # Route provider service
├── home_route.dart           # Typed route class
├── home_screen.graphql       # GraphQL queries (if needed)
└── __generated__/            # Generated GraphQL code
```

### 2.2 URL Routing Integration
- **Route Pattern**: `/` (root path)
- **Parameter Handling**: No URL parameters needed
- **Navigation**: Integrate with existing modular navigation architecture
- **Route Registration**: Register with RouteCollectionService

## 3. UI Component Design

### 3.1 Screen Layout Structure
```dart
Scaffold(
  body: CustomScrollView(
    slivers: [
      // App Bar
      SliverAppBar(
        title: Text('Home'),
        floating: true,
        snap: true,
        pinned: false,
      ),
      
      // Page Content
      SliverPadding(
        padding: EdgeInsets.all(16.0),
        sliver: SliverList(
          delegate: SliverChildListDelegate([
            // My Profile Section
            SectionHeader(title: 'My profile'),
            SizedBox(height: 8),
            CurrentUserCard(), // Placeholder user card
            SizedBox(height: 24),
            
            // My Work Section  
            SectionHeader(title: 'My work'),
            SizedBox(height: 8),
            
            // Work Items List (static UI definition)
            WorkItemListTile(title: 'Issues', icon: Icons.bug_report),
            WorkItemListTile(title: 'Pull requests', icon: Icons.call_merge),
            WorkItemListTile(title: 'Discussions', icon: Icons.forum),
            WorkItemListTile(title: 'Projects', icon: Icons.folder_open),
            WorkItemListTile(title: 'Repositories', icon: Icons.source),
            WorkItemListTile(title: 'Organizations', icon: Icons.business),
            WorkItemListTile(title: 'Starred', icon: Icons.star),
            
            // Bottom padding for scrolling comfort
            SizedBox(height: 16),
          ]),
        ),
      ),
    ],
  ),
)
```

### 3.2 Scrollable Layout Benefits

The CustomScrollView with SliverAppBar approach provides several advantages:
- **Responsive Design**: Content automatically scrolls when it exceeds screen height
- **App Bar Behavior**: SliverAppBar can float, snap, and hide/show during scroll
- **Performance**: Slivers provide efficient scrolling for large content lists
- **Material Design**: Follows Material 3 scrolling patterns and behaviors
- **Future Extensibility**: Easy to add pull-to-refresh, nested scrolling, or expandable app bar

### 3.3 Reusable Components

#### SectionHeader Widget
```dart
class SectionHeader extends StatelessWidget {
  final String title;
  
  const SectionHeader({required this.title});
  
  @override
  Widget build(BuildContext context) {
    return Text(
      title,
      style: Theme.of(context).textTheme.titleLarge?.copyWith(
        fontWeight: FontWeight.bold,
      ),
    );
  }
}
```

#### WorkItemListTile Widget
```dart
class WorkItemListTile extends StatelessWidget {
  final String title;
  final IconData icon;
  final VoidCallback? onTap;
  
  const WorkItemListTile({
    required this.title,
    required this.icon,
    this.onTap,
  });
  
  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: Theme.of(context).colorScheme.onSurfaceVariant),
      title: Text(
        title,
        style: Theme.of(context).textTheme.bodyLarge,
      ),
      trailing: Icon(
        Icons.arrow_forward_ios, 
        size: 16,
        color: Theme.of(context).colorScheme.onSurfaceVariant,
      ),
      onTap: onTap, // Placeholder - no functionality initially
      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    );
  }
}
```

#### CurrentUserCard Widget
```dart
class CurrentUserCard extends StatelessWidget {
  final String? name;
  final String? login;
  final String? avatarUrl;
  
  const CurrentUserCard({
    this.name,
    this.login,
    this.avatarUrl,
  });
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: avatarUrl != null ? NetworkImage(avatarUrl!) : null,
          child: avatarUrl == null ? Icon(Icons.person) : null,
        ),
        title: Text(name ?? 'User'),
        subtitle: Text('@${login ?? 'username'}'),
        trailing: Icon(Icons.arrow_forward_ios, size: 16),
        onTap: null, // Placeholder - no navigation initially
      ),
    );
  }
}
```

## 4. State Management

### 4.1 Architecture Principle
The ViewModel follows clean architecture principles by managing only business logic and data, not UI structure. Work item definitions (titles, icons, order) are considered UI presentation logic and are defined in the UI layer, not the ViewModel. This separation ensures the ViewModel remains focused on data and business concerns.

### 4.2 ViewModel Responsibilities
```dart
class HomeViewModel extends DisposableViewModel {
  final AuthService _authService;
  
  HomeViewModel(this._authService);
  
  // Current user data (from AuthService or placeholder)
  String? get currentUserName => _authService.currentUser?.name;
  String? get currentUserLogin => _authService.currentUser?.login;
  String? get currentUserAvatar => _authService.currentUser?.avatarUrl;
  
  @override
  void onDispose() {
    // Clean up resources if needed
  }
}
```

### 4.3 Dependency Injection
- **HomeViewModelFactory**: Registered with `@injectable`
- **HomeRouteProvider**: Registered with `@injectable` 
- **Dependencies**: AuthService (for current user context)

## 5. Navigation Integration

### 5.1 Route Definition
```dart
class HomeRoute extends AppRoute {
  const HomeRoute();
  
  @override
  String get path => '/';
}
```

### 5.2 Route Provider Integration
```dart
@injectable
class HomeRouteProvider {
  final HomeViewModelFactory _viewModelFactory;
  
  HomeRouteProvider(this._viewModelFactory);
  
  HomeRoute createRoute() => const HomeRoute();
  
  Widget buildScreen(HomeRoute route) {
    final viewModel = _viewModelFactory.create();
    return HomeScreen(viewModel: viewModel);
  }
}
```

### 5.3 Factory Pattern
```dart
@injectable
class HomeViewModelFactory {
  final AuthService _authService;
  
  HomeViewModelFactory(this._authService);
  
  HomeViewModel create() {
    return HomeViewModel(_authService);
  }
}
```

## 6. Implementation Strategy

### 6.1 Phase 1: Basic Structure (Current Implementation)
- Implement scrollable UI with SliverAppBar and CustomScrollView
- Use Material 3 ListView items for work items within SliverList
- No navigation functionality in list items (placeholder only)
- Work items are statically defined in UI layer (not data-driven)
- Root path routing ("/") for home screen access

### 6.2 Phase 2: Enhanced Integration (Future)
- Add GraphQL queries for real user data
- Implement navigation to different work item screens
- Add pull-to-refresh functionality using SliverAppBar refresh indicator
- Implement user profile navigation
- Add dynamic counts/badges to work item list tiles
- Consider SliverAppBar expansion/collapse animations

### 6.3 Current vs Requirements Alignment
The current home screen implementation shows a "Following" users feed, but the requirements specify:
- **My profile** section with current user card
- **My work** section with 7 static work items as Material 3 ListView items
- URL pattern `/` for home screen access (root path)
- **Scrollable content** to handle content longer than phone screen size

This design document aligns with the requirements rather than the current implementation, using a scrollable layout with SliverAppBar and Material 3 design patterns.

## 7. Testing Strategy

### 7.1 Unit Tests
- **HomeViewModel**: Test current user data access
- **HomeViewModelFactory**: Test ViewModel creation with dependencies
- **HomeRouteProvider**: Test route creation and screen building

### 7.2 Widget Tests
- **HomeScreen**: Test scrollable UI layout with SliverAppBar and CustomScrollView
- **SectionHeader**: Test title display and styling
- **WorkItemListTile**: Test Material 3 ListTile layout and styling
- **CurrentUserCard**: Test user information display
- **Scrolling Behavior**: Test that content scrolls properly on small screens

### 7.3 Integration Tests
- **Navigation**: Test URL routing to root path ("/")
- **Route Registration**: Test route collection integration
- **ViewModel Integration**: Test screen-ViewModel communication

## 8. Implementation Dependencies

### 8.1 Required Services
- **AuthService**: For current user context and data
- **RouteCollectionService**: For route registration

### 8.2 Required Widgets (New)
- **SectionHeader**: For consistent section title styling
- **WorkItemListTile**: For Material 3 ListView items displaying work items
- **CurrentUserCard**: For current user profile display

### 8.3 Existing Widget Reuse
- May reuse **UserCard** patterns for CurrentUserCard implementation
- Follow existing card styling patterns from the app

## 9. Performance Considerations

### 9.1 Lazy Loading
- ViewModel creation only when route is accessed
- Lightweight placeholder cards with minimal data

### 9.2 Memory Management
- Proper ViewModel disposal through DisposableViewModel
- Efficient SliverList with SliverChildListDelegate for scrollable content
- CustomScrollView provides better scroll performance for long content

### 9.3 Future Optimization
- GraphQL query optimization when real data is integrated
- Implement caching for user profile data
- Add pagination for work items when real data is available