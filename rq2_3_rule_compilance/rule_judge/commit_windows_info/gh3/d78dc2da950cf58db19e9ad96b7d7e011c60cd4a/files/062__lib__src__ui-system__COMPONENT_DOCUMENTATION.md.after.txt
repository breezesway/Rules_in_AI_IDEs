# UI System Component Documentation

This document provides detailed usage examples and best practices for all components in the GH3 UI System.

## Table of Contents

1. [Design Tokens](#design-tokens)
2. [Core Components](#core-components)
3. [State Components](#state-components)
4. [Layout Components](#layout-components)
5. [GitHub-Specific Widgets](#github-specific-widgets)
6. [Usage Guidelines](#usage-guidelines)

## Design Tokens

### GHTokens

The `GHTokens` class provides all design tokens for consistent styling across the application.

```dart
import '../tokens/gh_tokens.dart';

// Colors
Container(
  color: GHTokens.primary,
  child: Text(
    'Primary color background',
    style: TextStyle(color: GHTokens.onPrimary),
  ),
)

// Typography
Text('Title', style: GHTokens.titleLarge),
Text('Body text', style: GHTokens.bodyMedium),
Text('Caption', style: GHTokens.labelMedium),

// Spacing
Padding(
  padding: const EdgeInsets.all(GHTokens.spacing16),
  child: Container(
    margin: const EdgeInsets.only(bottom: GHTokens.spacing8),
    // content
  ),
)

// Border radius
Container(
  decoration: BoxDecoration(
    borderRadius: BorderRadius.circular(GHTokens.radius8),
  ),
)
```

## Core Components

### GHCard

A Material Design 3 card with consistent styling and GitHub theming.

#### Basic Usage

```dart
import '../components/gh_card.dart';

GHCard(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Card Title', style: GHTokens.titleMedium),
      const SizedBox(height: GHTokens.spacing8),
      Text('Card content goes here', style: GHTokens.bodyMedium),
    ],
  ),
)
```

#### Interactive Cards

```dart
GHCard(
  onTap: () => print('Card tapped'),
  child: ListTile(
    leading: Icon(Icons.star),
    title: Text('Tappable Card'),
    trailing: Icon(Icons.chevron_right),
  ),
)
```

#### Card Variants

```dart
// Compact card (12dp padding) - for secondary content
GHCard.compact(
  child: Text('Compact content'),
)

// Tight card (8dp padding) - for dense layouts like metrics
GHCard.tight(
  child: Column(
    children: [
      Text('1.2k', style: GHTokens.titleLarge),
      Text('Stars', style: GHTokens.labelMedium),
    ],
  ),
)

// Zero padding card - for content that manages its own spacing
GHCard.zeroPadding(
  child: ListTile(
    title: Text('Self-padded content'),
    subtitle: Text('Perfect for ListTile'),
  ),
)
```

#### Custom Elevation

```dart
GHCard(
  elevation: GHTokens.elevation3,
  child: Text('Elevated card'),
)
```

### GHButton

GitHub-styled buttons with consistent theming and loading states.

#### Primary Buttons

```dart
import '../components/gh_button.dart';

GHButton(
  label: 'Star Repository',
  icon: Icons.star_border,
  onPressed: () => starRepository(),
)

GHButton(
  label: 'Watch',
  icon: Icons.visibility,
  count: 142, // Show count badge
  onPressed: () => watchRepository(),
)
```

#### Secondary Buttons

```dart
GHButton(
  label: 'Follow',
  style: GHButtonStyle.secondary,
  icon: Icons.person_add,
  onPressed: () => followUser(),
)
```

#### Loading State

```dart
class _MyWidgetState extends State<MyWidget> {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return GHButton(
      label: 'Submit',
      isLoading: _isLoading,
      onPressed: () async {
        setState(() => _isLoading = true);
        await performAction();
        setState(() => _isLoading = false);
      },
    );
  }
}
```

#### Disabled Button

```dart
GHButton(
  label: 'Disabled',
  onPressed: null, // null onPressed disables the button
)
```

### GHChip

Filter chips with GitHub styling and optional count indicators.

#### Basic Chips

```dart
import '../components/gh_chip.dart';

GHChip(
  label: 'Open',
  count: 23,
  isSelected: true,
  onTap: () => filterByOpen(),
)

GHChip(
  label: 'bug',
  colorIndicator: Colors.red,
  count: 12,
  onTap: () => filterByLabel('bug'),
)
```

#### Language Chips

```dart
import '../utils/color_utils.dart';

GHChip(
  label: 'JavaScript',
  colorIndicator: ColorUtils.getLanguageColor('JavaScript'),
  isSelectable: false, // Display only, not interactive
)
```

#### Non-interactive Chips

```dart
GHChip(
  label: 'Status: Merged',
  colorIndicator: GHTokens.merged,
  isSelectable: false,
)
```

### GHTextField

Form input fields with GitHub styling and validation support.

#### Basic Text Field

```dart
import '../components/gh_text_field.dart';

GHTextField(
  labelText: 'Repository Name',
  hintText: 'Enter repository name',
  onChanged: (value) => setState(() => _repoName = value),
)
```

#### With Validation

```dart
GHTextField(
  labelText: 'Email',
  hintText: 'Enter your email',
  keyboardType: TextInputType.emailAddress,
  prefixIcon: Icons.email,
  errorText: _emailError,
  required: true,
  onChanged: (value) => _validateEmail(value),
)
```

#### Multi-line Text Field

```dart
GHTextField(
  labelText: 'Description',
  hintText: 'Describe your repository',
  maxLines: 4,
  minLines: 3,
)
```

#### Password Field

```dart
GHTextField(
  labelText: 'Password',
  hintText: 'Enter password',
  obscureText: true,
  prefixIcon: Icons.lock,
)
```

### GHSearchBar

Search input with GitHub styling and custom icons.

#### Basic Search Bar

```dart
import '../components/gh_search_bar.dart';

GHSearchBar(
  hintText: 'Search repositories...',
  onChanged: (query) => performSearch(query),
  onSubmitted: (query) => submitSearch(query),
)
```

#### With Custom Icons

```dart
GHSearchBar(
  hintText: 'Filter issues',
  prefixIcon: Icons.filter_list,
  suffixIcon: Icons.tune,
  onSuffixIconTap: () => showFilterDialog(),
  onChanged: (query) => filterIssues(query),
)
```

### GHListTile

Enhanced list tile with GitHub styling.

#### Basic Usage

```dart
import '../components/gh_list_tile.dart';

GHListTile(
  leading: CircleAvatar(child: Icon(Icons.person)),
  title: Text('John Doe'),
  subtitle: Text('@johndoe • 2 years ago'),
  trailing: Icon(Icons.chevron_right),
  onTap: () => openUserProfile(),
)
```

#### Repository List Item

```dart
GHListTile(
  leading: Container(
    width: 40,
    height: 40,
    decoration: BoxDecoration(
      color: ColorUtils.getLanguageColor('Dart'),
      borderRadius: BorderRadius.circular(8),
    ),
    child: Icon(Icons.code, color: Colors.white),
  ),
  title: Text('flutter/flutter'),
  subtitle: Text('UI toolkit for building natively compiled applications'),
  trailing: Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Icon(Icons.star, size: 16),
      Text('155k'),
    ],
  ),
  onTap: () => openRepository(),
)
```

## State Components

### GHEmptyState

Display empty states with helpful messaging and actions.

#### Basic Empty State

```dart
import '../state_widgets/gh_empty_state.dart';

GHEmptyState(
  icon: Icons.inbox_outlined,
  title: 'No items found',
  subtitle: 'Items you add will appear here',
  action: ElevatedButton(
    onPressed: () => addItem(),
    child: Text('Add Item'),
  ),
)
```

#### Predefined Empty States

```dart
// No repositories
GHEmptyStates.noRepositories(
  onCreateRepository: () => showCreateRepositoryDialog(),
)

// No search results
GHEmptyStates.noSearchResults(
  query: 'flutter ui toolkit',
  onClearSearch: () => clearSearch(),
)

// No activity
GHEmptyStates.noActivity(
  onExplore: () => navigateToExplore(),
)

// No issues
GHEmptyStates.noIssues(
  onCreateIssue: () => createNewIssue(),
)

// No starred repositories
GHEmptyStates.noStarredRepos(
  onExplore: () => exploreRepositories(),
)
```

### GHErrorState

Display error states with retry functionality.

#### Basic Error State

```dart
import '../state_widgets/gh_error_state.dart';

GHErrorState(
  icon: Icons.error_outline,
  title: 'Something went wrong',
  message: 'An unexpected error occurred. Please try again.',
  onRetry: () => retryOperation(),
)
```

#### Predefined Error States

```dart
// Network error
GHErrorStates.networkError(
  onRetry: () => retryNetworkRequest(),
)

// Authentication error
GHErrorStates.authenticationError(
  onRetry: () => signInAgain(),
)

// Rate limit error
GHErrorStates.rateLimitError(
  resetTime: DateTime.now().add(Duration(minutes: 5)),
  onRetry: () => retryAfterLimit(),
)

// Repository load error
GHErrorStates.repositoryLoadError(
  onRetry: () => reloadRepository(),
)

// Search error
GHErrorStates.searchError(
  query: 'flutter ui',
  onRetry: () => retrySearch(),
)
```

#### With Loading State During Retry

```dart
class _MyWidgetState extends State<MyWidget> {
  bool _isRetrying = false;

  @override
  Widget build(BuildContext context) {
    return GHErrorState(
      icon: Icons.cloud_off,
      title: 'Connection Error',
      message: 'Unable to connect to server',
      isRetrying: _isRetrying,
      onRetry: () async {
        setState(() => _isRetrying = true);
        try {
          await retryOperation();
        } finally {
          setState(() => _isRetrying = false);
        }
      },
    );
  }
}
```

### GHLoadingIndicator

Consistent loading indicators across the application.

#### Basic Loading Indicator

```dart
import '../state_widgets/gh_loading_indicator.dart';

// Default size
GHLoadingIndicator()

// Large size
GHLoadingIndicator.large()

// Small size
GHLoadingIndicator.small()
```

#### With Label

```dart
GHLoadingIndicator.large(
  label: 'Loading repositories...',
  centered: true,
)
```

#### In Context

```dart
class _RepositoryListState extends State<RepositoryList> {
  bool _isLoading = true;
  List<Repository> _repositories = [];

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return GHLoadingIndicator.large(
        label: 'Loading repositories...',
        centered: true,
      );
    }

    return ListView.builder(
      itemCount: _repositories.length,
      itemBuilder: (context, index) => RepositoryTile(_repositories[index]),
    );
  }
}
```

### GHStatusBadge

Display status indicators with semantic colors.

#### Basic Status Badges

```dart
import '../widgets/gh_status_badge.dart';

GHStatusBadge(status: GHStatusType.open)
GHStatusBadge(status: GHStatusType.closed)
GHStatusBadge(status: GHStatusType.merged)
GHStatusBadge(status: GHStatusType.draft)
```

#### Custom Labels

```dart
GHStatusBadge(
  status: GHStatusType.open,
  customLabel: 'In Progress',
)

GHStatusBadge(
  status: GHStatusType.merged,
  customLabel: 'Approved',
)
```

## Layout Components

### GHContentTemplate

Organize content into clearly defined sections.

#### Basic Usage

```dart
import '../layouts/gh_content_template.dart';

GHContentTemplate(
  sections: [
    GHContentSection(
      title: 'Repository Info',
      content: RepositoryHeader(),
    ),
    GHContentSection(
      title: 'Statistics',
      content: RepositoryStats(),
    ),
    GHContentSection(
      title: 'README',
      content: MarkdownViewer(content: readme),
    ),
  ],
)
```

#### Scrollable Content Template

```dart
GHContentTemplate(
  isScrollable: true,
  sections: [
    GHContentSection(
      title: 'Overview',
      content: ProjectOverview(),
    ),
    GHContentSection(
      title: 'Recent Activity',
      content: ActivityFeed(),
    ),
  ],
)
```

### GHContentMetadata

Display structured metadata information.

#### Basic Metadata

```dart
import '../widgets/gh_content_metadata.dart';

GHContentMetadata(
  title: 'Project Details',
  items: [
    GHMetadataItem(
      icon: Icons.person,
      label: 'Owner',
      value: 'flutter',
    ),
    GHMetadataItem(
      icon: Icons.schedule,
      label: 'Updated',
      value: '2 hours ago',
    ),
    GHMetadataItem(
      icon: Icons.link,
      label: 'Website',
      value: 'flutter.dev',
      isLink: true,
      onTap: () => launchUrl('https://flutter.dev'),
    ),
  ],
)
```

#### With Dividers

```dart
GHContentMetadata(
  showDividers: true,
  items: [
    GHMetadataItem(
      icon: Icons.folder,
      label: 'Size',
      value: '124.5 MB',
    ),
    GHMetadataItem(
      icon: Icons.code,
      label: 'Language',
      value: 'Dart',
    ),
  ],
)
```

#### Metadata Chips

```dart
GHMetadataChips(
  title: 'Topics',
  items: [
    GHMetadataItem(
      icon: Icons.mobile_friendly,
      label: 'mobile',
      value: 'mobile',
    ),
    GHMetadataItem(
      icon: Icons.web,
      label: 'web',
      value: 'web',
    ),
    GHMetadataItem(
      icon: Icons.desktop_mac,
      label: 'desktop',
      value: 'desktop',
    ),
  ],
)
```

## GitHub-Specific Widgets

### Color Utilities

Get language-specific colors for repositories.

```dart
import '../utils/color_utils.dart';

// Get color for a specific language
Color jsColor = ColorUtils.getLanguageColor('JavaScript');
Color dartColor = ColorUtils.getLanguageColor('Dart');

// Get popular languages with colors
List<Map<String, dynamic>> languages = ColorUtils.getPopularLanguages();
for (var lang in languages) {
  String name = lang['language'];
  Color color = lang['color'];
  // Use in UI
}
```

### Date Formatting

Format dates in GitHub style.

```dart
import '../utils/date_formatter.dart';

// Relative formatting
String relative = DateFormatter.formatRelative(DateTime.now().subtract(Duration(hours: 2)));
// Output: "2 hours ago"

// Absolute formatting
String absolute = DateFormatter.formatAbsolute(DateTime(2024, 1, 15));
// Output: "Jan 15, 2024"
```

### Number Formatting

Format numbers in compact notation.

```dart
import '../utils/number_formatter.dart';

String compact = NumberFormatter.formatCompact(1250);
// Output: "1.3k"

String compactLarge = NumberFormatter.formatCompact(1500000);
// Output: "1.5M"
```

## Usage Guidelines

### Design Token Compliance

Always use design tokens for consistent styling:

```dart
// ✅ Good - Uses design tokens
Container(
  padding: const EdgeInsets.all(GHTokens.spacing16),
  decoration: BoxDecoration(
    color: GHTokens.surface,
    borderRadius: BorderRadius.circular(GHTokens.radius8),
  ),
  child: Text(
    'Content',
    style: GHTokens.bodyMedium,
  ),
)

// ❌ Bad - Hardcoded values
Container(
  padding: const EdgeInsets.all(20),
  decoration: BoxDecoration(
    color: Color(0xFFFFFFFF),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text(
    'Content',
    style: TextStyle(fontSize: 16),
  ),
)
```

### Accessibility Requirements

Ensure all components meet accessibility standards:

```dart
// Minimum touch target size (48x48dp)
GestureDetector(
  onTap: () => handleTap(),
  child: Container(
    width: 48,
    height: 48,
    alignment: Alignment.center,
    child: Icon(Icons.favorite),
  ),
)

// Semantic labels for screen readers
Semantics(
  label: 'Star this repository',
  child: GHButton(
    icon: Icons.star,
    onPressed: () => starRepository(),
  ),
)
```

### Component Selection Guide

Choose the right component for your use case:

- **GHCard**: Use for grouping related content
  - Default: General content (16dp padding)
  - Compact: Secondary content, lists (12dp padding)
  - Tight: Dense content, metrics (8dp padding)
  - ZeroPadding: Content with built-in padding (ListTile, etc.)

- **GHButton**: Use for actions
  - Primary: Main actions (star, fork, create)
  - Secondary: Supporting actions (follow, watch)

- **GHChip**: Use for filters and tags
  - With count: Filter chips showing item counts
  - With color: Language indicators, status labels
  - Non-interactive: Display-only tags

- **Empty States**: Use when content is missing
  - Provide helpful messaging
  - Include actionable next steps when possible
  - Use appropriate icons for context

- **Error States**: Use when operations fail
  - Provide clear error messages
  - Always include retry functionality when applicable
  - Show loading state during retry

- **Loading Indicators**: Use during async operations
  - Include descriptive messages for longer operations
  - Use appropriate size for context
  - Center in available space

### Performance Best Practices

Optimize component usage for better performance:

```dart
// Use const constructors when possible
const GHEmptyState(
  icon: Icons.inbox,
  title: 'No items',
  subtitle: 'Items will appear here',
)

// Use keys for list items
ListView.builder(
  itemBuilder: (context, index) => GHCard(
    key: ValueKey(_items[index].id),
    child: ItemContent(_items[index]),
  ),
)

// Avoid rebuilding heavy widgets
class ExpensiveWidget extends StatelessWidget {
  const ExpensiveWidget({super.key});
  
  @override
  Widget build(BuildContext context) {
    // Heavy widget content
  }
}
```

### Testing Components

Test components properly:

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('GHButton should handle tap', (tester) async {
    bool tapped = false;
    
    await tester.pumpWidget(
      MaterialApp(
        home: GHButton(
          label: 'Test',
          onPressed: () => tapped = true,
        ),
      ),
    );
    
    await tester.tap(find.text('Test'));
    await tester.pump();
    
    expect(tapped, isTrue);
  });
}
```

## Conclusion

This UI system provides a comprehensive set of components for building consistent GitHub-style interfaces. Always use design tokens, follow accessibility guidelines, and choose the appropriate component variant for your specific use case.

For more examples, see the Component Catalog screen in the example screens directory.