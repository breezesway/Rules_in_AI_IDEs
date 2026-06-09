# Navigation Compliance Design

## Overview

This design implements user feedback to eliminate tab navigation in favor of action-based push navigation and Material Design scrolling app bars. The solution directly addresses the user's preference for push navigation patterns and eliminates duplicate title displays.

## Architecture

### User Profile Navigation Redesign

```dart
// Current: Tab-based navigation
TabBar(tabs: [
  Tab(text: 'Repositories'),
  Tab(text: 'Starred'),
  Tab(text: 'Organizations'),
])

// New: Action-based navigation
Column(
  children: [
    GHUserCard(user: user),
    SizedBox(height: GHTokens.spacing20),
    _buildActionsList(context, user),
  ],
)

Widget _buildActionsList(BuildContext context, User user) {
  return Column(
    children: [
      GHCard(
        padding: EdgeInsets.zero,
        child: ListTile(
          leading: Icon(Icons.folder_outlined),
          title: Text('Repositories'),
          subtitle: Text('${user.repositoryCount} public repositories'),
          trailing: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Chip(label: Text('${user.repositoryCount}')),
              Icon(Icons.chevron_right),
            ],
          ),
          onTap: () => NavigationService.navigateToUserRepositories(user.login),
        ),
      ),
      SizedBox(height: GHTokens.spacing8),
      // Similar cards for Starred, Organizations, etc.
    ],
  );
}
```

### Scrolling App Bar Implementation

```dart
// User Details with Material Design Scrolling App Bar
class UserDetailsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 120.0,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              title: Text(user.name),
              titlePadding: EdgeInsets.only(left: 16, bottom: 16),
              collapseMode: CollapseMode.fade,
            ),
            backgroundColor: Theme.of(context).colorScheme.surface,
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.all(GHTokens.spacing16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // User content without duplicate title
                  GHUserCard(
                    user: user,
                    showTitle: false, // Key: Don't show title in content
                  ),
                  SizedBox(height: GHTokens.spacing20),
                  _buildActionsList(context, user),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

## Component Modifications

### GHUserCard Enhancement

```dart
class GHUserCard extends StatelessWidget {
  final bool showTitle;
  final bool showLargeTitle;
  
  const GHUserCard({
    super.key,
    required this.user,
    this.showTitle = true,
    this.showLargeTitle = false,
  });

  @override
  Widget build(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              CircleAvatar(
                radius: showLargeTitle ? 32 : 24,
                backgroundImage: NetworkImage(user.avatarUrl),
              ),
              SizedBox(width: GHTokens.spacing12),
              if (showTitle) ...[
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        user.name,
                        style: showLargeTitle 
                          ? GHTokens.headlineMedium 
                          : GHTokens.titleLarge,
                      ),
                      Text(
                        '@${user.login}',
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ],
          ),
          // Rest of user card content...
        ],
      ),
    );
  }
}
```

### Navigation Service Updates

```dart
class NavigationService {
  // New dedicated navigation methods
  static void navigateToUserRepositories(String username) {
    router.push('/user/$username/repositories');
  }
  
  static void navigateToUserStarred(String username) {
    router.push('/user/$username/starred');
  }
  
  static void navigateToUserOrganizations(String username) {
    router.push('/user/$username/organizations');
  }
}
```

## Screen Implementations

### Dedicated Repository Screen

```dart
class UserRepositoriesScreen extends StatelessWidget {
  final String username;
  
  const UserRepositoriesScreen({super.key, required this.username});
  
  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Repositories',
      showBackButton: true,
      body: GHListTemplate(
        searchHint: 'Search repositories...',
        onRefresh: _handleRefresh,
        onSearch: _handleSearch,
        children: [
          // Repository list items
        ],
      ),
    );
  }
}
```

## Animation Specifications

### App Bar Transition

```dart
class ScrollingAppBarBehavior {
  static const Duration transitionDuration = Duration(milliseconds: 200);
  static const Curve transitionCurve = Curves.easeInOut;
  static const double fadeThreshold = 0.7;
  
  static Animation<double> createFadeAnimation(
    AnimationController controller,
  ) {
    return Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: controller,
      curve: Interval(fadeThreshold, 1.0, curve: transitionCurve),
    ));
  }
}
```

## Accessibility Considerations

### Touch Targets
- All action list items: minimum 48dp height
- Chevron icons: minimum 24x24dp touch area
- Count badges: proper contrast ratios

### Screen Reader Support
```dart
ListTile(
  title: Text('Repositories'),
  subtitle: Text('${user.repositoryCount} public repositories'),
  onTap: () => NavigationService.navigateToUserRepositories(user.login),
  // Accessibility
  semanticLabel: 'View ${user.repositoryCount} repositories for ${user.name}',
  excludeFromSemantics: false,
)
```

## Performance Considerations

### Lazy Loading
- Repository lists: implement pagination
- User data: cache frequently accessed profiles
- Images: use cached network images

### Memory Management
- Dispose animation controllers properly
- Clear listeners on widget disposal
- Optimize image loading and caching

This design ensures smooth navigation experiences while eliminating the tab pattern in favor of more native mobile navigation patterns.