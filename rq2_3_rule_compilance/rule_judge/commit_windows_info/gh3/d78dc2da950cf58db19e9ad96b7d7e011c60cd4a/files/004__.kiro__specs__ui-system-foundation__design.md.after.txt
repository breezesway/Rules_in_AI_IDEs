# Design System Foundation Design

## Overview

The Design System Foundation provides the core building blocks for the gh3 GitHub mobile application UI system. This design implements a comprehensive design tokens system, Material Design 3 theme configuration, core UI components library, utility functions, and showcase screens that demonstrate the complete system with realistic fake data.

**User Acceptance Testing Strategy**: To enable effective UAT for the design system, this implementation will include a dedicated UAT entry point that allows stakeholders to easily access and evaluate the design system. The UI system is designed to work seamlessly across both web and mobile platforms, providing flexibility for demonstration and testing.

## Architecture

### File Structure

The UI system follows a modular architecture organized in `lib/src/ui-system/`:

```
lib/src/ui-system/
├── tokens/
│   └── gh_tokens.dart              # Centralized design tokens
├── theme/
│   └── gh_theme.dart               # Material Design 3 theme configuration
├── components/
│   ├── gh_card.dart                # Elevated card component
│   ├── gh_button.dart              # Primary/secondary buttons
│   ├── gh_chip.dart                # Filter chips with badges
│   ├── gh_list_tile.dart           # Enhanced list items
│   ├── gh_search_bar.dart          # Search input component
│   ├── gh_status_badge.dart        # Status indicators
│   └── gh_text_field.dart          # Form input component
├── utils/
│   ├── date_formatter.dart         # Relative date formatting
│   ├── number_formatter.dart       # Compact number formatting
│   └── color_utils.dart            # Programming language colors
└── examples/
    ├── design_tokens_screen.dart   # Design tokens showcase
    └── component_catalog_screen.dart # Component library showcase
```

### Design Principles

1. **Token-Based Design**: All visual properties derive from centralized design tokens
2. **Material Design 3 Compliance**: Full integration with Material Design 3 theming system
3. **GitHub Brand Alignment**: Colors and styling match GitHub's visual identity
4. **Accessibility First**: All components meet WCAG 2.1 AA standards
5. **Performance Optimized**: Compile-time constants and efficient widget composition
6. **Cross-Platform UAT**: Design system works seamlessly on both web and mobile platforms to enable flexible stakeholder review and user acceptance testing

## Components and Interfaces

### Design Tokens System (GHTokens)

The `GHTokens` class provides centralized access to all design tokens:

```dart
class GHTokens {
  // Colors - GitHub Brand
  static const Color primary = Color(0xFF0969DA);
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color primaryContainer = Color(0xFFDDE6F4);
  static const Color onPrimaryContainer = Color(0xFF0A1929);
  
  // GitHub Semantic Colors
  static const Color success = Color(0xFF1A7F37);
  static const Color warning = Color(0xFFBF8700);
  static const Color error = Color(0xFFCF222E);
  static const Color merged = Color(0xFF8250DF);
  static const Color draft = Color(0xFF656D76);
  
  // Typography Scale
  static const TextStyle headlineLarge = TextStyle(fontSize: 32, fontWeight: FontWeight.w400);
  static const TextStyle headlineMedium = TextStyle(fontSize: 28, fontWeight: FontWeight.w400);
  static const TextStyle titleLarge = TextStyle(fontSize: 22, fontWeight: FontWeight.w500);
  static const TextStyle titleMedium = TextStyle(fontSize: 16, fontWeight: FontWeight.w500);
  static const TextStyle bodyLarge = TextStyle(fontSize: 16, fontWeight: FontWeight.w400);
  static const TextStyle bodyMedium = TextStyle(fontSize: 14, fontWeight: FontWeight.w400);
  static const TextStyle labelLarge = TextStyle(fontSize: 14, fontWeight: FontWeight.w500);
  static const TextStyle labelMedium = TextStyle(fontSize: 12, fontWeight: FontWeight.w500);
  
  // Spacing System
  static const double spacing4 = 4.0;
  static const double spacing8 = 8.0;
  static const double spacing12 = 12.0;
  static const double spacing16 = 16.0;
  static const double spacing20 = 20.0;
  static const double spacing24 = 24.0;
  static const double spacing32 = 32.0;
  
  // Border Radius
  static const double radius4 = 4.0;
  static const double radius8 = 8.0;
  static const double radius12 = 12.0;
  static const double radius16 = 16.0;
}
```

### Theme Configuration (GHTheme)

The `GHTheme` class provides Material Design 3 theme configuration:

```dart
class GHTheme {
  static ThemeData lightTheme() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: GHTokens.primary,
      brightness: Brightness.light,
    ).copyWith(
      primary: GHTokens.primary,
      onPrimary: GHTokens.onPrimary,
      primaryContainer: GHTokens.primaryContainer,
      onPrimaryContainer: GHTokens.onPrimaryContainer,
      error: GHTokens.error,
    );
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _buildTextTheme(),
      cardTheme: _buildCardTheme(),
      elevatedButtonTheme: _buildElevatedButtonTheme(),
      chipTheme: _buildChipTheme(),
    );
  }
  
  static ThemeData darkTheme() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: GHTokens.primary,
      brightness: Brightness.dark,
    ).copyWith(
      primary: GHTokens.primary,
      error: GHTokens.error,
    );
    
    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _buildTextTheme(),
      cardTheme: _buildCardTheme(),
      elevatedButtonTheme: _buildElevatedButtonTheme(),
      chipTheme: _buildChipTheme(),
    );
  }
}
```

### Core UI Components

#### GHCard Component

```dart
class GHCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final VoidCallback? onTap;
  final double? elevation;
  
  const GHCard({
    super.key,
    required this.child,
    this.padding,
    this.onTap,
    this.elevation,
  });
  
  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: elevation ?? 1.0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: padding ?? const EdgeInsets.all(GHTokens.spacing16),
          child: child,
        ),
      ),
    );
  }
}
```

#### GHButton Component

```dart
enum GHButtonStyle { primary, secondary }

class GHButton extends StatelessWidget {
  final String label;
  final VoidCallback? onPressed;
  final GHButtonStyle style;
  final bool isLoading;
  final IconData? icon;
  
  const GHButton({
    super.key,
    required this.label,
    this.onPressed,
    this.style = GHButtonStyle.primary,
    this.isLoading = false,
    this.icon,
  });
  
  @override
  Widget build(BuildContext context) {
    if (style == GHButtonStyle.primary) {
      return ElevatedButton.icon(
        onPressed: isLoading ? null : onPressed,
        icon: isLoading 
          ? const SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : (icon != null ? Icon(icon, size: 18) : const SizedBox.shrink()),
        label: Text(label, style: GHTokens.labelLarge),
        style: ElevatedButton.styleFrom(
          minimumSize: const Size(88, 48),
          padding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing16,
            vertical: GHTokens.spacing12,
          ),
        ),
      );
    } else {
      return OutlinedButton.icon(
        onPressed: isLoading ? null : onPressed,
        icon: isLoading 
          ? const SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : (icon != null ? Icon(icon, size: 18) : const SizedBox.shrink()),
        label: Text(label, style: GHTokens.labelLarge),
        style: OutlinedButton.styleFrom(
          minimumSize: const Size(88, 48),
          padding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing16,
            vertical: GHTokens.spacing12,
          ),
        ),
      );
    }
  }
}
```

#### GHChip Component

```dart
class GHChip extends StatelessWidget {
  final String label;
  final bool isSelected;
  final VoidCallback? onTap;
  final int? count;
  final Color? colorIndicator;
  
  const GHChip({
    super.key,
    required this.label,
    this.isSelected = false,
    this.onTap,
    this.count,
    this.colorIndicator,
  });
  
  @override
  Widget build(BuildContext context) {
    return FilterChip(
      label: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (colorIndicator != null) ...[
            Container(
              width: 12,
              height: 12,
              decoration: BoxDecoration(
                color: colorIndicator,
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: GHTokens.spacing4),
          ],
          Text(label, style: GHTokens.labelMedium),
          if (count != null) ...[
            const SizedBox(width: GHTokens.spacing4),
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: GHTokens.spacing4,
                vertical: 2,
              ),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceVariant,
                borderRadius: BorderRadius.circular(GHTokens.radius8),
              ),
              child: Text(
                count.toString(),
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ),
          ],
        ],
      ),
      selected: isSelected,
      onSelected: onTap != null ? (_) => onTap!() : null,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius16),
      ),
    );
  }
}
```

#### GHStatusBadge Component

```dart
enum GHStatus { open, closed, merged, draft }

class GHStatusBadge extends StatelessWidget {
  final GHStatus status;
  final String? customLabel;
  
  const GHStatusBadge({
    super.key,
    required this.status,
    this.customLabel,
  });
  
  @override
  Widget build(BuildContext context) {
    final config = _getStatusConfig(status);
    
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing8,
        vertical: GHTokens.spacing4,
      ),
      decoration: BoxDecoration(
        color: config.color,
        borderRadius: BorderRadius.circular(GHTokens.radius12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            config.icon,
            size: 16,
            color: config.textColor,
          ),
          const SizedBox(width: GHTokens.spacing4),
          Text(
            customLabel ?? config.label,
            style: GHTokens.labelMedium.copyWith(
              color: config.textColor,
            ),
          ),
        ],
      ),
    );
  }
  
  _StatusConfig _getStatusConfig(GHStatus status) {
    switch (status) {
      case GHStatus.open:
        return _StatusConfig(
          color: GHTokens.success,
          textColor: Colors.white,
          icon: Icons.error_outline,
          label: 'Open',
        );
      case GHStatus.closed:
        return _StatusConfig(
          color: GHTokens.error,
          textColor: Colors.white,
          icon: Icons.check_circle_outline,
          label: 'Closed',
        );
      case GHStatus.merged:
        return _StatusConfig(
          color: GHTokens.merged,
          textColor: Colors.white,
          icon: Icons.merge_type,
          label: 'Merged',
        );
      case GHStatus.draft:
        return _StatusConfig(
          color: GHTokens.draft,
          textColor: Colors.white,
          icon: Icons.edit_outlined,
          label: 'Draft',
        );
    }
  }
}

class _StatusConfig {
  final Color color;
  final Color textColor;
  final IconData icon;
  final String label;
  
  const _StatusConfig({
    required this.color,
    required this.textColor,
    required this.icon,
    required this.label,
  });
}
```

### Utility Functions

#### Date Formatter

```dart
class DateFormatter {
  static String formatRelative(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);
    
    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes} minutes ago';
    } else if (difference.inHours < 24) {
      return '${difference.inHours} hours ago';
    } else if (difference.inDays < 7) {
      return '${difference.inDays} days ago';
    } else if (difference.inDays < 30) {
      final weeks = (difference.inDays / 7).floor();
      return weeks == 1 ? 'Last week' : '$weeks weeks ago';
    } else if (difference.inDays < 365) {
      final months = (difference.inDays / 30).floor();
      return months == 1 ? 'Last month' : '$months months ago';
    } else {
      final years = (difference.inDays / 365).floor();
      return years == 1 ? 'Last year' : '$years years ago';
    }
  }
}
```

#### Number Formatter

```dart
class NumberFormatter {
  static String formatCompact(int number) {
    if (number < 1000) {
      return number.toString();
    } else if (number < 1000000) {
      final k = number / 1000;
      return k % 1 == 0 ? '${k.toInt()}k' : '${k.toStringAsFixed(1)}k';
    } else if (number < 1000000000) {
      final m = number / 1000000;
      return m % 1 == 0 ? '${m.toInt()}M' : '${m.toStringAsFixed(1)}M';
    } else {
      final b = number / 1000000000;
      return b % 1 == 0 ? '${b.toInt()}B' : '${b.toStringAsFixed(1)}B';
    }
  }
}
```

#### Color Utils

```dart
class ColorUtils {
  static const Map<String, Color> languageColors = {
    'JavaScript': Color(0xFFF1E05A),
    'Dart': Color(0xFF00B4AB),
    'Python': Color(0xFF3572A5),
    'Swift': Color(0xFFFA7343),
    'TypeScript': Color(0xFF2B7489),
    'Java': Color(0xFFB07219),
    'C++': Color(0xFFF34B7D),
    'Go': Color(0xFF00ADD8),
    'Rust': Color(0xFFDEA584),
    'Kotlin': Color(0xFFA97BFF),
    'C#': Color(0xFF239120),
    'Ruby': Color(0xFF701516),
    'PHP': Color(0xFF4F5D95),
    'Shell': Color(0xFF89E051),
    'HTML': Color(0xFFE34C26),
  };
  
  static const Color defaultLanguageColor = Color(0xFF858585);
  
  static Color getLanguageColor(String language) {
    return languageColors[language] ?? defaultLanguageColor;
  }
  
  static List<String> getSupportedLanguages() {
    return languageColors.keys.toList()..sort();
  }
}
```

## Data Models

### Fake Data Models

The showcase screens use structured fake data models to demonstrate realistic usage:

```dart
class FakeRepository {
  final String name;
  final String owner;
  final String description;
  final String language;
  final int starCount;
  final int forkCount;
  final DateTime lastUpdated;
  
  const FakeRepository({
    required this.name,
    required this.owner,
    required this.description,
    required this.language,
    required this.starCount,
    required this.forkCount,
    required this.lastUpdated,
  });
}

class FakeUser {
  final String login;
  final String name;
  final String bio;
  final String avatarUrl;
  final int followers;
  final int following;
  final int repositories;
  
  const FakeUser({
    required this.login,
    required this.name,
    required this.bio,
    required this.avatarUrl,
    required this.followers,
    required this.following,
    required this.repositories,
  });
}
```

### Fake Data Providers

```dart
class FakeDataProvider {
  static final List<FakeRepository> repositories = [
    FakeRepository(
      name: 'react',
      owner: 'facebook',
      description: 'A declarative, efficient, and flexible JavaScript library for building user interfaces.',
      language: 'JavaScript',
      starCount: 218000,
      forkCount: 45200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 2)),
    ),
    FakeRepository(
      name: 'flutter',
      owner: 'flutter',
      description: 'Flutter makes it easy and fast to build beautiful apps for mobile and beyond.',
      language: 'Dart',
      starCount: 162000,
      forkCount: 26700,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 5)),
    ),
    // ... more repositories
  ];
  
  static final List<String> buttonLabels = [
    'Star', 'Watch', 'Fork', 'Follow', 'Clone', 'Download', 'Subscribe', 'Unwatch'
  ];
  
  static final List<String> statusLabels = [
    'Open', 'Closed', 'Merged', 'Draft', 'In Progress', 'Approved', 'Pending', 'Rejected'
  ];
}
```

## Error Handling

### Component Error States

All components include proper error handling and fallback states:

```dart
class GHButton extends StatelessWidget {
  // ... existing code
  
  @override
  Widget build(BuildContext context) {
    try {
      // Component implementation
    } catch (e) {
      // Fallback to basic button if component fails
      return TextButton(
        onPressed: onPressed,
        child: Text(label),
      );
    }
  }
}
```

### Theme Fallbacks

The theme system includes fallbacks for missing or invalid configurations:

```dart
class GHTheme {
  static ThemeData lightTheme() {
    try {
      return _buildLightTheme();
    } catch (e) {
      // Fallback to Material Design default
      return ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      );
    }
  }
}
```

## Testing Strategy

### Unit Testing

Each component and utility function includes comprehensive unit tests:

```dart
// test/src/ui-system/components/gh_button_test.dart
void main() {
  group('GHButton', () {
    testWidgets('displays label correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHButton(
              label: 'Test Button',
              onPressed: () {},
            ),
          ),
        ),
      );
      
      expect(find.text('Test Button'), findsOneWidget);
    });
    
    testWidgets('shows loading state', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHButton(
              label: 'Loading',
              isLoading: true,
              onPressed: () {},
            ),
          ),
        ),
      );
      
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });
}
```

### Widget Testing

Showcase screens include widget tests to verify proper rendering:

```dart
// test/src/ui-system/examples/design_tokens_screen_test.dart
void main() {
  group('DesignTokensScreen', () {
    testWidgets('displays all typography styles', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: DesignTokensScreen(),
        ),
      );
      
      expect(find.text('Headline Large'), findsOneWidget);
      expect(find.text('Headline Medium'), findsOneWidget);
      expect(find.text('Title Large'), findsOneWidget);
      // ... test all typography styles
    });
  });
}
```

### Integration Testing

Integration tests verify theme switching and component interactions:

```dart
// test/integration/design_system_integration_test.dart
void main() {
  group('Design System Integration', () {
    testWidgets('theme switching works correctly', (tester) async {
      await tester.pumpWidget(MyApp());
      
      // Test light theme
      expect(Theme.of(tester.element(find.byType(Scaffold))).brightness, 
             equals(Brightness.light));
      
      // Switch to dark theme
      await tester.tap(find.byIcon(Icons.dark_mode));
      await tester.pumpAndSettle();
      
      // Verify dark theme
      expect(Theme.of(tester.element(find.byType(Scaffold))).brightness, 
             equals(Brightness.dark));
    });
  });
}
```

## Cross-Platform UAT Support

### Platform Compatibility

The design system implementation supports both web and mobile platforms with consistent behavior:

1. **Responsive Layout**: Showcase screens adapt to different screen sizes and orientations
2. **Input Methods**: Components support both touch and mouse/keyboard interactions
3. **Accessibility**: Full accessibility support across platforms
4. **Performance**: Optimized rendering for both web and mobile platforms
5. **Consistent Behavior**: Identical functionality and appearance across platforms

### UAT Deployment Strategy

To facilitate user acceptance testing, we'll create a dedicated UAT entry point:

**File Structure for UAT:**
```
lib/
├── main.dart                      # Default main (production app)
├── main_ui_system_uat.dart       # UAT-specific main for design system
└── src/ui-system/
    └── examples/
        ├── design_tokens_screen.dart
        ├── component_catalog_screen.dart
        └── uat_home_screen.dart      # UAT navigation screen
```

**UAT-Specific Main Entry Point (`lib/main_ui_system_uat.dart`):**
```dart
// UAT-specific main entry point for design system demonstration
void main() {
  runApp(DesignSystemUATApp());
}

class DesignSystemUATApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GH3 Design System - UAT',
      theme: GHTheme.lightTheme(),
      darkTheme: GHTheme.darkTheme(),
      home: UATHomeScreen(),
      routes: {
        '/tokens': (context) => DesignTokensScreen(),
        '/components': (context) => ComponentCatalogScreen(),
      },
    );
  }
}
```

**Build Commands for UAT:**
```bash
# Run on web for stakeholder review
flutter run -d chrome --target=lib/main_ui_system_uat.dart

# Run on mobile for testing
flutter run -d ios --target=lib/main_ui_system_uat.dart
flutter run -d android --target=lib/main_ui_system_uat.dart

# Build for deployment
flutter build web --target=lib/main_ui_system_uat.dart
```

**UAT Home Screen:**
```dart
class UATHomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('GH3 Design System - UAT'),
        actions: [
          IconButton(
            icon: Icon(Icons.brightness_6),
            onPressed: () => _toggleTheme(context),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Design System Showcase',
              style: GHTokens.headlineMedium,
              textAlign: TextAlign.center,
            ),
            SizedBox(height: GHTokens.spacing32),
            GHButton(
              label: 'Design Tokens Showcase',
              onPressed: () => Navigator.pushNamed(context, '/tokens'),
            ),
            SizedBox(height: GHTokens.spacing16),
            GHButton(
              label: 'Component Catalog',
              style: GHButtonStyle.secondary,
              onPressed: () => Navigator.pushNamed(context, '/components'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Steering Documentation Update Requirement

As part of this implementation, the project steering documentation must be updated to reflect the temporary decision to use web platform for design system UAT. This ensures all stakeholders understand the rationale and approach for design system validation.

This comprehensive design provides a solid foundation for the gh3 application's UI system, ensuring consistency, accessibility, and maintainability across all components and screens, with web platform optimization for effective user acceptance testing.