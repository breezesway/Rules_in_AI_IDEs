# Navigation Pattern Documentation

## Overview

The gh3 application uses a **push navigation pattern** for all screen transitions.

## Key Principles

1. **Push Navigation Only**: All navigation uses `router.push()` instead of `router.go()`
2. **Home Screen as Root**: The home screen is the root of the navigation stack with no back button
3. **Stack-Based Navigation**: Each new screen is pushed onto the navigation stack, allowing users to navigate back through their history

## Implementation Details

### Navigation Service

The `NavigationService` class in `lib/src/ui-system/navigation/navigation_service.dart` provides centralized navigation methods:

```dart
// All navigation methods use push
static void navigateToUser(String username) {
  router.push(ExampleRoutes.userProfilePath(username));
}

static void navigateToRepository(String owner, String name) {
  router.push(ExampleRoutes.repositoryPath(owner, name));
}
```

### Home Screen Configuration

The home screen (`HomeScreenExample`) is configured as the root screen:
- Sets `showBackButton: false` in `GHScreenTemplate`
- Serves as the starting point for all navigation flows
- No way to navigate "back" from the home screen

### Navigation Flow Example

```
Home Screen (no back button)
  └─> User Profile (back to Home)
       └─> Repository Details (back to User Profile)
            └─> Issues List (back to Repository Details)
                 └─> Issue Detail (back to Issues List)
```

## Benefits

1. **Predictable Navigation**: Users always know where the back button will take them
2. **Deep Navigation Support**: Users can navigate deep into the app hierarchy
3. **History Preservation**: Full navigation history is maintained
4. **Consistent UX**: Matches native mobile app navigation patterns

## Usage Guidelines

### For Developers

1. Always use `NavigationService` methods for navigation
2. Never use `router.go()` except for special cases (like deep linking)
3. Configure root screens with `showBackButton: false`
4. Use `NavigationService.canNavigateBack()` to check if back navigation is available

### Screen Configuration

```dart
// Root screen (like Home)
GHScreenTemplate(
  title: "GitHub",
  showBackButton: false,  // No back button
  body: ...,
)

// Sub-screens
GHScreenTemplate(
  title: "User Profile",
  showBackButton: true,   // Shows back button (default)
  body: ...,
)
```

## Migration Notes

- Updated from `router.go()` to `router.push()` in all navigation methods
- Home screen configured with `showBackButton: false`
- All example screens follow push navigation pattern
- No changes needed to screen implementations (only navigation service)