# GH3 UI System

A comprehensive Material Design 3 UI system for the GitHub mobile application, providing consistent, accessible, and performant components.

## Quick Start

### Running the UI System Demo

```bash
# Run on web (recommended for stakeholder review)
flutter run -d chrome --target=lib/demo/main_ui_system.dart

# Run on iOS
flutter run -d ios --target=lib/demo/main_ui_system.dart

# Run on Android
flutter run -d android --target=lib/demo/main_ui_system.dart
```

## Architecture

```
lib/src/ui-system/
├── components/          # Core UI components (buttons, cards, chips, etc.)
├── state_widgets/       # State management widgets (empty, error, loading)
├── layouts/            # Layout templates and structures
├── widgets/            # Complex GitHub-specific widgets
├── tokens/             # Design tokens (colors, typography, spacing)
├── theme/              # Material Design 3 theme configuration
├── utils/              # Utility functions (formatters, helpers)
├── examples/           # Example screens and demos
├── docs/               # Component documentation
└── navigation/         # Navigation system for examples
```

## Key Features

### 🎨 Material Design 3
- Full MD3 theming with GitHub brand colors
- Dynamic color support
- Consistent elevation and surface treatments

### 🌓 Theme Support
- Light and dark themes
- Automatic theme switching
- Consistent color semantics

### ♿ Accessibility
- 48dp minimum touch targets
- WCAG 2.1 AA color contrast compliance
- Screen reader support
- Keyboard navigation

### 📱 Responsive Design
- Mobile-first approach
- Tablet optimizations
- Adaptive layouts

### 🚀 Performance
- Const constructors throughout
- Efficient widget trees
- Lazy loading support

## Core Components

### Buttons
```dart
GHButton(
  label: 'Star',
  icon: Icons.star_border,
  onPressed: () => starRepository(),
)
```

### Cards
```dart
GHCard(          // 16dp padding - primary content
GHCard.compact(  // 12dp padding - secondary content  
GHCard.tight(    // 8dp padding - dense content
GHCard.zeroPadding( // 0dp - self-padded content
```

### Chips
```dart
GHChip(
  label: 'Open',
  count: 23,
  isSelected: true,
  onTap: () => filterByStatus('open'),
)
```

### Status Badges
```dart
GHStatusBadge(status: GHStatusType.open)    // Green
GHStatusBadge(status: GHStatusType.closed)  // Red
GHStatusBadge(status: GHStatusType.merged)  // Purple
GHStatusBadge(status: GHStatusType.draft)   // Gray
```

## State Management

### Empty States
```dart
GHEmptyStates.noRepositories(
  onCreateRepository: () => createNewRepo(),
)
```

### Error States
```dart
GHErrorStates.networkError(
  onRetry: () => retryRequest(),
)
```

### Loading States
```dart
GHLoadingIndicator.large(
  label: 'Loading repositories...',
  centered: true,
)
```

## Design Tokens

### Colors
- **Primary**: `#0969DA` (GitHub blue)
- **Success**: `#1A7F37` (Open/success states)
- **Error**: `#CF222E` (Closed/error states)
- **Merged**: `#8250DF` (Merged PRs)
- **Draft**: `#656D76` (Draft/disabled states)

### Typography
- Headlines: 32sp, 28sp
- Titles: 22sp, 16sp, 14sp
- Body: 16sp, 14sp
- Labels: 14sp, 12sp, 10sp

### Spacing
- 4dp, 8dp, 12dp, 16dp, 20dp, 24dp, 32dp

## Usage Examples

### Complete Repository Card
```dart
GHCard(
  onTap: () => navigateToRepository(repo),
  child: Column(
    children: [
      // Repository header with language indicator
      Row(
        children: [
          LanguageIndicator(language: repo.language),
          SizedBox(width: GHTokens.spacing12),
          Expanded(
            child: RepositoryTitle(repo: repo),
          ),
        ],
      ),
      // Repository stats
      RepositoryStats(
        stars: repo.starCount,
        forks: repo.forkCount,
        language: repo.language,
      ),
    ],
  ),
)
```

### Screen with States
```dart
class RepositoryListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return GHLoadingIndicator.large(
        label: 'Loading repositories...',
        centered: true,
      );
    }
    
    if (hasError) {
      return GHErrorStates.repositoryLoadError(
        onRetry: () => reloadRepositories(),
      );
    }
    
    if (repositories.isEmpty) {
      return GHEmptyStates.noRepositories(
        onCreateRepository: () => navigateToCreate(),
      );
    }
    
    return RepositoryList(repositories: repositories);
  }
}
```

## Testing

### Running Tests
```bash
# Run all UI system tests
flutter test test/ui-system/

# Run specific component tests
flutter test test/ui-system/components/
flutter test test/ui-system/state_widgets/
```

### Test Coverage
- Unit tests for all utilities
- Widget tests for all components
- Integration tests for example screens
- Golden tests for visual regression

## Development Guidelines

### 1. Always Use Design Tokens
```dart
// ✅ Good
SizedBox(height: GHTokens.spacing16)
Text('Title', style: GHTokens.titleMedium)

// ❌ Avoid
SizedBox(height: 16)
Text('Title', style: TextStyle(fontSize: 16))
```

### 2. Follow Component Patterns
- Extend StatelessWidget when possible
- Use const constructors
- Implement proper error boundaries
- Handle loading and error states

### 3. Accessibility First
- Test with screen readers
- Ensure proper contrast ratios
- Provide semantic labels
- Support keyboard navigation

### 4. Performance Optimization
- Use const widgets
- Implement proper keys
- Avoid unnecessary rebuilds
- Profile with DevTools

## Quality Standards

### Code Quality
```bash
# Must pass before commit
flutter analyze --fatal-infos --fatal-warnings
dart format .
flutter test
```

### Design Review
- All components reviewed by design team
- Accessibility audit completed
- Cross-platform testing verified
- Performance benchmarks met

## Migration Guide

### From Existing UI
1. Replace custom widgets with UI system components
2. Update color references to use design tokens
3. Replace spacing values with token values
4. Update text styles to use typography tokens

### Example Migration
```dart
// Before
Container(
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text(
    'Title',
    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
  ),
)

// After
GHCard(
  child: Text('Title', style: GHTokens.titleMedium),
)
```

## Contributing

### Adding New Components
1. Create component in `components/` directory
2. Add design tokens if needed
3. Write comprehensive tests
4. Update component catalog
5. Add usage documentation

### Component Checklist
- [ ] Follows design system patterns
- [ ] Uses design tokens consistently
- [ ] Includes all necessary states
- [ ] Has comprehensive tests
- [ ] Documented with examples
- [ ] Accessible (48dp targets, contrast, labels)
- [ ] Works in light and dark themes
- [ ] Performance optimized

## Resources

- [Component Usage Guide](docs/component_usage_guide.md)
- [Design Tokens Reference](tokens/gh_tokens.dart)
- [Material Design 3 Guidelines](https://m3.material.io)
- [Flutter Best Practices](https://docs.flutter.dev/development/ui/widgets)

## Version History

### v1.0.0 - Phase 3 Complete
- ✅ All core components implemented
- ✅ State management widgets (empty, error, loading)
- ✅ Card variants (default, compact, tight, zero padding)
- ✅ Content templates and metadata displays
- ✅ Interactive examples and documentation
- ✅ Full test coverage

## Support

For questions or issues:
- Check the [Component Usage Guide](docs/component_usage_guide.md)
- Review example implementations in `examples/`
- Run the interactive demo app
- Contact the UI team for design questions