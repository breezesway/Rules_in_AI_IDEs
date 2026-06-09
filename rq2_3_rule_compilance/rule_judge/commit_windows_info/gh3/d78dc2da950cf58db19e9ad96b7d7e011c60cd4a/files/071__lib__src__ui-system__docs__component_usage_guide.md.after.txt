# GH3 UI System Component Usage Guide

This guide provides comprehensive usage examples and best practices for all components in the GH3 UI system.

## Table of Contents

1. [Core Components](#core-components)
2. [State Management Components](#state-management-components)
3. [Layout Components](#layout-components)
4. [Content Display Components](#content-display-components)
5. [Best Practices](#best-practices)

## Core Components

### GHCard

The `GHCard` component provides consistent card styling with multiple padding variants.

#### Basic Usage
```dart
GHCard(
  child: Text('Card content'),
  onTap: () => print('Card tapped'),
)
```

#### Card Variants

**Compact Card (12dp padding)**
```dart
GHCard.compact(
  child: Column(
    children: [
      Text('Secondary content'),
      Text('Perfect for lists'),
    ],
  ),
)
```

**Tight Card (8dp padding)**
```dart
GHCard.tight(
  child: Column(
    children: [
      Text('123', style: GHTokens.titleLarge),
      Text('Count', style: GHTokens.labelMedium),
    ],
  ),
)
```

**Zero Padding Card**
```dart
GHCard.zeroPadding(
  child: ListTile(
    leading: Icon(Icons.person),
    title: Text('User name'),
    subtitle: Text('User details'),
  ),
)
```

#### When to Use Each Variant
- **Default (16dp)**: General content, primary information
- **Compact (12dp)**: Secondary content, list items
- **Tight (8dp)**: Metrics, counts, dense information
- **Zero padding**: Content with built-in padding (ListTile, etc.)

### GHButton

GitHub-styled buttons with primary and secondary variants.

#### Primary Button
```dart
GHButton(
  label: 'Star',
  icon: Icons.star_border,
  onPressed: () => starRepository(),
)
```

#### Secondary Button
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
GHButton(
  label: 'Loading',
  isLoading: true,
  onPressed: null, // Disabled during loading
)
```

### GHChip

Filter chips with optional count badges and color indicators.

#### Basic Chip
```dart
GHChip(
  label: 'Open',
  count: 23,
  isSelected: true,
  onTap: () => filterByStatus('open'),
)
```

#### With Color Indicator
```dart
GHChip(
  label: 'JavaScript',
  colorIndicator: ColorUtils.getLanguageColor('JavaScript'),
  isSelectable: false,
)
```

### GHListTile

Enhanced list tile with GitHub styling.

```dart
GHListTile(
  leading: CircleAvatar(
    backgroundImage: NetworkImage(user.avatarUrl),
  ),
  title: Text(user.name),
  subtitle: Text('@${user.username}'),
  trailing: Icon(Icons.chevron_right),
  onTap: () => navigateToUser(user),
)
```

### GHSearchBar

Search input with customizable icons and actions.

```dart
GHSearchBar(
  hintText: 'Search repositories...',
  onChanged: (query) => searchRepositories(query),
  onSubmitted: (query) => executeSearch(query),
  suffixIcon: Icons.filter_list,
  onSuffixIconTap: () => showFilterOptions(),
)
```

### GHStatusBadge

Status indicators with GitHub semantic colors.

```dart
// Predefined statuses
GHStatusBadge(status: GHStatusType.open)
GHStatusBadge(status: GHStatusType.closed)
GHStatusBadge(status: GHStatusType.merged)
GHStatusBadge(status: GHStatusType.draft)

// Custom label
GHStatusBadge(
  status: GHStatusType.open,
  customLabel: 'In Progress',
)
```

### GHTextField

Form input fields with GitHub styling.

```dart
GHTextField(
  labelText: 'Repository Name',
  hintText: 'my-awesome-project',
  helperText: 'Choose a unique name',
  required: true,
  errorText: errors['name'],
  onChanged: (value) => validateName(value),
)
```

## State Management Components

### GHEmptyState

Display helpful empty states with actions.

#### Pre-built Empty States
```dart
// No repositories
GHEmptyStates.noRepositories(
  onCreateRepository: () => navigateToCreateRepo(),
)

// No search results
GHEmptyStates.noSearchResults(
  query: 'flutter-ui',
  onClearSearch: () => clearSearch(),
)

// No activity
GHEmptyStates.noActivity(
  onExplore: () => navigateToExplore(),
)
```

#### Custom Empty State
```dart
GHEmptyState(
  icon: Icons.folder_open,
  title: 'No files found',
  subtitle: 'This directory is empty',
  action: GHButton(
    label: 'Create file',
    onPressed: () => createNewFile(),
  ),
)
```

### GHErrorState

Display error states with retry functionality.

#### Pre-built Error States
```dart
// Network error
GHErrorStates.networkError(
  onRetry: () => retryNetworkRequest(),
)

// Repository load error
GHErrorStates.repositoryLoadError(
  onRetry: () => reloadRepository(),
)

// Rate limit error
GHErrorStates.rateLimitError(
  onRetry: () => scheduleRetry(),
)
```

#### Custom Error State
```dart
GHErrorState(
  title: 'Build Failed',
  message: 'The workflow run failed with errors',
  actionLabel: 'View logs',
  onRetry: () => navigateToLogs(),
  isLoading: isRetrying,
)
```

### GHLoadingIndicator

Consistent loading indicators with optional messages.

```dart
// Basic loading
GHLoadingIndicator()

// With message
GHLoadingIndicator.large(
  label: 'Loading repositories...',
  centered: true,
)

// Different sizes
GHLoadingIndicator.small() // 16x16
GHLoadingIndicator()       // 24x24 (default)
GHLoadingIndicator.large() // 32x32
```

## Layout Components

### GHContentTemplate

Organize content into sections with consistent spacing.

```dart
GHContentTemplate(
  sections: [
    GHContentSection(
      title: 'Repository Details',
      content: RepositoryHeader(),
    ),
    GHContentSection(
      title: 'README',
      content: MarkdownViewer(content: readme),
    ),
    GHContentSection(
      title: 'Recent Activity',
      content: ActivityList(items: activities),
    ),
  ],
)
```

### GHContentMetadata

Display metadata in a structured format.

```dart
GHContentMetadata(
  title: 'Repository Info',
  showDividers: true,
  items: [
    GHMetadataItem(
      icon: Icons.code,
      label: 'Language',
      value: 'Dart',
    ),
    GHMetadataItem(
      icon: Icons.balance,
      label: 'License',
      value: 'MIT',
      isLink: true,
      onTap: () => showLicenseDetails(),
    ),
  ],
)
```

#### Metadata as Chips
```dart
GHMetadataChips(
  title: 'Topics',
  items: [
    GHMetadataItem(label: 'flutter', value: 'flutter'),
    GHMetadataItem(label: 'dart', value: 'dart'),
    GHMetadataItem(label: 'mobile', value: 'mobile'),
  ],
)
```

## Content Display Components

### Complete Repository Card Example
```dart
GHCard(
  onTap: () => navigateToRepository(repo),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: ColorUtils.getLanguageColor(repo.language),
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Icon(Icons.code, color: Colors.white),
          ),
          SizedBox(width: GHTokens.spacing12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(repo.owner, style: GHTokens.bodyMedium),
                    Text('/', style: GHTokens.bodyMedium),
                    Text(repo.name, style: GHTokens.titleMedium),
                    if (repo.isPrivate)
                      Padding(
                        padding: EdgeInsets.only(left: GHTokens.spacing8),
                        child: GHStatusBadge(
                          status: GHStatusType.draft,
                          customLabel: 'Private',
                        ),
                      ),
                  ],
                ),
                if (repo.description != null)
                  Padding(
                    padding: EdgeInsets.only(top: GHTokens.spacing4),
                    child: Text(
                      repo.description!,
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
      SizedBox(height: GHTokens.spacing12),
      Row(
        children: [
          if (repo.language != null) ...[
            GHChip(
              label: repo.language!,
              colorIndicator: ColorUtils.getLanguageColor(repo.language!),
              isSelectable: false,
            ),
            SizedBox(width: GHTokens.spacing8),
          ],
          Icon(Icons.star, size: GHTokens.iconSize16),
          SizedBox(width: GHTokens.spacing4),
          Text(
            NumberFormatter.format(repo.starCount),
            style: GHTokens.labelMedium,
          ),
          SizedBox(width: GHTokens.spacing16),
          Icon(Icons.fork_right, size: GHTokens.iconSize16),
          SizedBox(width: GHTokens.spacing4),
          Text(
            NumberFormatter.format(repo.forkCount),
            style: GHTokens.labelMedium,
          ),
          Spacer(),
          Text(
            DateFormatter.relative(repo.updatedAt),
            style: GHTokens.labelMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    ],
  ),
)
```

### Complete Issue Card Example
```dart
GHCard(
  onTap: () => navigateToIssue(issue),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Row(
        children: [
          Icon(
            issue.status == GHStatusType.open
                ? Icons.error_outline
                : Icons.check_circle_outline,
            color: issue.status == GHStatusType.open
                ? GHTokens.success
                : GHTokens.error,
            size: GHTokens.iconSize24,
          ),
          SizedBox(width: GHTokens.spacing12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${issue.title} #${issue.number}',
                  style: GHTokens.titleMedium,
                ),
                SizedBox(height: GHTokens.spacing4),
                Text(
                  issue.status == GHStatusType.open
                      ? 'opened ${DateFormatter.relative(issue.createdAt)} by @${issue.author}'
                      : 'closed ${DateFormatter.relative(issue.closedAt)} by @${issue.closedBy}',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ),
          ),
          GHStatusBadge(status: issue.status),
        ],
      ),
      if (issue.labels.isNotEmpty) ...[
        SizedBox(height: GHTokens.spacing12),
        Wrap(
          spacing: GHTokens.spacing8,
          children: issue.labels.map((label) =>
            GHChip(
              label: label.name,
              colorIndicator: label.color,
              isSelectable: false,
            ),
          ).toList(),
        ),
      ],
      if (issue.commentCount > 0) ...[
        SizedBox(height: GHTokens.spacing12),
        Row(
          children: [
            Icon(
              Icons.comment,
              size: GHTokens.iconSize16,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            SizedBox(width: GHTokens.spacing4),
            Text(
              '${issue.commentCount} comments',
              style: GHTokens.labelMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ],
    ],
  ),
)
```

## Best Practices

### 1. Consistent Token Usage
Always use design tokens for spacing, typography, and colors:
```dart
// Good
SizedBox(height: GHTokens.spacing16)
Text('Title', style: GHTokens.titleMedium)

// Avoid
SizedBox(height: 16)
Text('Title', style: TextStyle(fontSize: 16))
```

### 2. Proper Card Variant Selection
- Use default padding for primary content
- Use compact for secondary content and lists
- Use tight for metrics and counts
- Use zero padding for self-padded content

### 3. Loading States
Always show loading indicators for async operations:
```dart
if (isLoading) {
  return GHLoadingIndicator.large(
    label: 'Loading data...',
    centered: true,
  );
}
```

### 4. Error Handling
Provide meaningful error messages with retry options:
```dart
if (hasError) {
  return GHErrorStates.networkError(
    onRetry: () => reloadData(),
  );
}
```

### 5. Empty States
Guide users when content is missing:
```dart
if (items.isEmpty) {
  return GHEmptyStates.noSearchResults(
    query: searchQuery,
    onClearSearch: () => clearSearch(),
  );
}
```

### 6. Accessibility
- Ensure all interactive elements have proper touch targets (48dp minimum)
- Provide semantic labels for screen readers
- Use sufficient color contrast ratios

### 7. Theme Support
Always test components in both light and dark themes:
```dart
Theme.of(context).colorScheme.onSurfaceVariant // Adapts to theme
```

### 8. Performance
- Use const constructors where possible
- Implement proper keys for list items
- Avoid rebuilding unchanged widgets

## Component Composition Example

Here's a complete example showing how to compose multiple components:

```dart
class RepositoryListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: EdgeInsets.all(GHTokens.spacing16),
            child: GHSearchBar(
              hintText: 'Search repositories...',
              onChanged: (query) => searchRepositories(query),
            ),
          ),
          
          // Filter chips
          Container(
            height: 48,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: EdgeInsets.symmetric(horizontal: GHTokens.spacing16),
              children: [
                GHChip(
                  label: 'All',
                  count: totalCount,
                  isSelected: filter == 'all',
                  onTap: () => setFilter('all'),
                ),
                SizedBox(width: GHTokens.spacing8),
                GHChip(
                  label: 'Public',
                  count: publicCount,
                  isSelected: filter == 'public',
                  onTap: () => setFilter('public'),
                ),
                // More filters...
              ],
            ),
          ),
          
          // Content area
          Expanded(
            child: Builder(
              builder: (context) {
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
                
                return ListView.separated(
                  padding: EdgeInsets.all(GHTokens.spacing16),
                  itemCount: repositories.length,
                  separatorBuilder: (context, index) => 
                    SizedBox(height: GHTokens.spacing8),
                  itemBuilder: (context, index) {
                    final repo = repositories[index];
                    return RepositoryCard(repository: repo);
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

This guide covers all components in the GH3 UI system with practical examples and best practices for implementation.