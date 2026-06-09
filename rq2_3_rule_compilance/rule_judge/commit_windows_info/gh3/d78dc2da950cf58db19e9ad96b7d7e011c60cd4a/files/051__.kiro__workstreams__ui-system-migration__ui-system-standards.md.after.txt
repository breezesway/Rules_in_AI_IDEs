# GH3 UI System Standards

## Overview

This document defines the comprehensive standards for the GH3 UI system based on user feedback and Material Design principles. All screens and components must adhere to these standards to ensure consistency and quality.

## Navigation Standards

### 1. Push Navigation Pattern
- **Principle**: All navigation uses push navigation (`router.push()`)
- **Implementation**:
  - Never use `router.go()` except for deep linking
  - Each screen pushes onto the navigation stack
  - Users can always navigate back through their history
  - Example flow: Home → User Profile → Repository → Issues → Issue Detail

### 2. Home Screen as Root
- **Principle**: Home screen is the root with no back navigation
- **Implementation**:
  - Home screen sets `showBackButton: false`
  - All other screens show back button by default
  - No way to navigate "before" home screen

### 3. No Tab Navigation
- **Principle**: Avoid tab navigation in favor of action lists
- **Implementation**:
  - User details page: Replace tabs with action list items
  - Each action (Repositories, Starred, Organizations) pushes new screen
  - Maintains clear navigation hierarchy
  - Better for mobile navigation patterns

## Layout Standards

### 1. Page Structure
```dart
GHScreenTemplate(
  title: "Screen Title",
  showBackButton: true,  // false only for root screens
  body: GHListTemplate(  // or direct content
    children: [...],
  ),
)
```

### 2. Scrolling App Bar Pattern
- **Principle**: Avoid duplicate titles between app bar and content
- **Implementation**:
  - Use `SliverAppBar` with collapsing title
  - Title starts in content area (large)
  - Transitions to app bar on scroll
  - Smooth fade animation
  - Example: User details screen

## Spacing Standards

### 1. Base Grid System
All spacing must use the 4dp grid system from design tokens:

| Token | Value | Usage |
|-------|-------|-------|
| `spacing4` | 4dp | Tight spacing (rare) |
| `spacing8` | 8dp | Between related items |
| `spacing12` | 12dp | Default card spacing |
| `spacing16` | 16dp | Page margins |
| `spacing20` | 20dp | Section breaks |
| `spacing24` | 24dp | Large sections |
| `spacing32` | 32dp | Major breaks |

### 2. Page Padding
- **Horizontal**: Always 16dp (`GHTokens.spacing16`)
- **Vertical**: 16dp top and bottom
- **Applied via**: `GHScreenTemplate` automatically

### 3. Card Spacing Rules
- **Between cards (same type)**: 12dp
- **Between related items**: 8dp (e.g., activity items)
- **Between sections**: 20dp
- **After headers**: 12dp

### 4. Card Padding Variants

#### Standard Card
```dart
GHCard(
  padding: EdgeInsets.all(GHTokens.spacing16), // Default
  child: content,
)
```
- Use for: Primary content, detailed information

#### Compact Card
```dart
GHCard(
  padding: EdgeInsets.all(GHTokens.spacing12),
  child: content,
)
```
- Use for: Lists, secondary content

#### Tight Card
```dart
GHCard(
  padding: EdgeInsets.all(GHTokens.spacing8),
  child: content,
)
```
- Use for: Dense lists, minimal content

#### No Padding Card
```dart
GHCard(
  padding: EdgeInsets.zero,
  child: ListTile(...), // Content with own padding
)
```
- Use for: ListTiles, custom padded content

## Supported Components Guide

### Component Quick Reference

| Component | Use Case | Key Features |
|-----------|----------|--------------|
| **Layout** | | |
| `GHScreenTemplate` | All screens | App bar, padding, theme |
| `GHListTemplate` | List screens | Search, refresh, scroll |
| `GHContentTemplate` | Content screens | Sections, metadata |
| **Core** | | |
| `GHButton` | All buttons | Primary/secondary, loading |
| `GHCard` | All cards | Standard/compact/zero padding |
| `GHChip` | Tags, filters | Selection, counts, colors |
| `GHTextField` | Text input | Consistent styling |
| `GHSearchBar` | Search functionality | Debouncing, clear button |
| **GitHub Widgets** | | |
| `GHUserCard` | User profiles | Avatar, stats, follow |
| `GHRepositoryCard` | Repository lists | Language, stats, star |
| `GHIssueCard` | Issue/PR lists | Status, labels, author |
| `GHEntityHeader` | Detail headers | Stats, actions, privacy |
| `GHNavigationGrid` | Quick actions | Icons, badges, 2x2 grid |
| `GHFilterBar` | Filter interfaces | Scrolling, counts |
| `GHStatusBadge` | Status indicators | Semantic colors |
| **State** | | |
| `GHLoadingIndicator` | Loading states | Spinner, message |
| `GHEmptyState` | Empty states | Icon, title, action |
| **List** | | |
| `GHListTile` | Simple lists | Consistent styling |
| `GHFileTreeItem` | File listings | Icons, commit info |

### 1. Layout Components

#### GHScreenTemplate
```dart
GHScreenTemplate(
  title: "Screen Title",
  showBackButton: true,
  actions: [...],
  body: content,
)
```
- **Use for**: All main screen structures
- **Features**: Consistent app bar, automatic padding, theme integration
- **Required**: Every screen must use this

#### GHListTemplate
```dart
GHListTemplate(
  searchHint: "Search...",
  onRefresh: _handleRefresh,
  onSearch: _handleSearch,
  children: [...],
)
```
- **Use for**: List-based screens with search/refresh
- **Features**: Pull-to-refresh, search bar, consistent list styling
- **Examples**: Home screen, repository lists, issue lists

#### GHContentTemplate
```dart
GHContentTemplate(
  sections: [...],
  metadata: {...},
)
```
- **Use for**: Content-heavy screens with sections
- **Features**: Section dividers, metadata display, proper spacing
- **Examples**: Article pages, documentation views

### 2. Core Components

#### GHButton
```dart
GHButton(
  label: "Star",
  style: GHButtonStyle.primary, // or .secondary
  isLoading: false,
  icon: Icons.star,
  onPressed: () {},
)
```
- **Use for**: All buttons in the app
- **Primary**: Main actions (Star, Follow, Create)
- **Secondary**: Secondary actions (Cancel, Settings)
- **Features**: Loading states, consistent sizing, proper touch targets

#### GHCard
```dart
// Standard card
GHCard(child: content)

// Compact card
GHCard(
  padding: EdgeInsets.all(GHTokens.spacing12),
  child: content,
)

// Zero padding (for ListTile)
GHCard(
  padding: EdgeInsets.zero,
  child: ListTile(...),
)
```
- **Use for**: All card-based content
- **Standard**: Rich content, forms, detailed info
- **Compact**: Lists, secondary content
- **Zero padding**: Content with own padding (ListTile, custom layouts)

#### GHChip
```dart
GHChip(
  label: "bug",
  isSelected: true,
  count: 12,
  colorIndicator: Colors.red,
  onTap: () {},
)
```
- **Use for**: Tags, filters, labels
- **Features**: Selection states, count badges, color indicators
- **Examples**: Issue labels, language tags, filter chips

#### GHTextField
```dart
GHTextField(
  label: "Search repositories",
  hint: "Enter repository name...",
  onChanged: (value) {},
)
```
- **Use for**: All text input fields
- **Features**: Consistent styling, error states, validation

#### GHSearchBar
```dart
GHSearchBar(
  hint: "Search repositories, users, issues...",
  onChanged: (query) {},
  onSubmitted: (query) {},
)
```
- **Use for**: Search functionality
- **Features**: GitHub-style search, debouncing, clear button

### 3. GitHub-Specific Widgets

#### GHUserCard
```dart
GHUserCard.fromFakeUser(
  user,
  showFollowButton: true,
  onTap: () {},
  onFollowTap: () {},
)
```
- **Use for**: User profile displays
- **Features**: Avatar, name, bio, stats, follow button
- **Contains**: Built-in card styling (don't wrap in GHCard)

#### GHRepositoryCard
```dart
GHRepositoryCard.fromFakeRepository(
  repository,
  showStarButton: true,
  onTap: () {},
  onStarTap: () {},
)
```
- **Use for**: Repository listings
- **Features**: Language color, stats, star button, last updated
- **Contains**: Built-in card styling

#### GHIssueCard
```dart
GHIssueCard.fromFakeIssue(
  issue,
  onTap: () {},
  onLabelTap: (label) {},
)
```
- **Use for**: Issue and PR listings
- **Features**: Status badge, labels, author, comment count
- **Contains**: Built-in card styling

#### GHEntityHeader
```dart
GHEntityHeader(
  title: "Repository Name",
  subtitle: "Repository description",
  avatar: CircleAvatar(...),
  stats: [
    GHEntityStat(icon: Icons.star, label: "Stars", value: "1.2k"),
    GHEntityStat(icon: Icons.fork_right, label: "Forks", value: "234"),
  ],
  actions: [
    GHButton(label: "Star", onPressed: () {}),
  ],
)
```
- **Use for**: Entity detail headers (repository, user, organization)
- **Features**: Statistics, action buttons, privacy indicators

#### GHNavigationGrid
```dart
GHNavigationGrid.twoByTwo(
  items: [
    GHNavigationItem(
      icon: Icons.star,
      title: "Starred",
      description: "Your starred repositories",
      badge: "45",
      onTap: () {},
    ),
  ],
)
```
- **Use for**: Dashboard quick actions, navigation grids
- **Features**: Icons, titles, descriptions, count badges
- **Variants**: 2x2, 2x3, custom grid

#### GHFilterBar
```dart
GHFilterBar(
  filters: [
    GHFilter(label: "Open", count: 12, isSelected: true),
    GHFilter(label: "Closed", count: 8, isSelected: false),
  ],
  onFilterTap: (filter) {},
)
```
- **Use for**: Filter interfaces (issues, repositories)
- **Features**: Horizontal scrolling, count indicators, selection states

#### GHStatusBadge
```dart
GHStatusBadge(
  status: GHStatusType.open,
  customLabel: "In Progress",
)
```
- **Use for**: Status indicators
- **Types**: Open, closed, merged, draft
- **Features**: Semantic colors, consistent styling

### 4. State Components

#### GHLoadingIndicator
```dart
GHLoadingIndicator(
  message: "Loading repositories...",
)
```
- **Use for**: Loading states
- **Features**: Consistent spinner, optional message

#### GHEmptyState
```dart
GHEmptyState(
  icon: Icons.inbox,
  title: "No issues found",
  subtitle: "Try adjusting your search criteria",
  action: GHButton(
    label: "Clear filters",
    onPressed: () {},
  ),
)
```
- **Use for**: Empty states
- **Features**: Icon, title, subtitle, optional action

### 5. List Components

#### GHListTile
```dart
GHListTile(
  leading: CircleAvatar(...),
  title: "Issue title",
  subtitle: "Issue description",
  trailing: GHStatusBadge(...),
  onTap: () {},
)
```
- **Use for**: Simple list items
- **Features**: Consistent styling, proper touch targets

#### GHFileTreeItem
```dart
GHFileTreeItem(
  name: "src/main.dart",
  isDirectory: false,
  lastCommitMessage: "Add new feature",
  fileSize: "2.1 KB",
  onTap: () {},
)
```
- **Use for**: File/directory listings
- **Features**: File type icons, commit info, size display

## Component Usage Rules

### 1. Never Nest Cards
- **Wrong**: `GHCard(child: GHUserCard(...))`
- **Right**: `GHUserCard(...)`
- **Reason**: GitHub widgets already include card styling

### 2. Activity Lists
- **Pattern**: `GHCard(padding: EdgeInsets.zero, child: ListTile(...))`
- **Reason**: ListTile has its own padding, prevents double padding

### 3. Touch Targets
- **Minimum**: 48x48dp for all interactive elements
- **Built-in**: All GH components meet this requirement

### 4. Loading States
- **Pattern**: Show `GHLoadingIndicator` while loading
- **Buttons**: Use `isLoading: true` on buttons during actions

### 5. Empty States
- **Pattern**: Use `GHEmptyState` when no content
- **Message**: Be helpful and actionable
- **Actions**: Provide way to resolve empty state

## Content Organization

### 1. Screen Sections
```dart
Column(
  children: [
    // Section 1
    _buildUserSection(),
    SizedBox(height: GHTokens.spacing20), // Section break
    
    // Section 2
    _buildQuickActions(),
    SizedBox(height: GHTokens.spacing20), // Section break
    
    // Section 3
    _buildActivityFeed(),
  ],
)
```

### 2. Section Headers
```dart
Padding(
  padding: EdgeInsets.symmetric(horizontal: GHTokens.spacing12),
  child: Row(
    mainAxisAlignment: MainAxisAlignment.spaceBetween,
    children: [
      Text('Section Title', style: GHTokens.titleLarge),
      TextButton(onPressed: ..., child: Text('See all')),
    ],
  ),
),
SizedBox(height: GHTokens.spacing12), // After header
```

## Accessibility Standards

### 1. Touch Targets
- **Minimum**: 48x48dp for all interactive elements
- **Buttons**: Use standard `GHButton` components
- **List items**: Ensure proper height

### 2. Text Contrast
- **Follow**: Material Design contrast ratios
- **Test**: Both light and dark themes
- **Use**: Theme colors from `GHTokens`

## Implementation Checklist

For every screen implementation:

### Layout Requirements
- [ ] Uses `GHScreenTemplate` with correct `showBackButton`
- [ ] Uses `GHListTemplate` for list-based screens
- [ ] Uses `GHContentTemplate` for content-heavy screens
- [ ] Follows push navigation pattern
- [ ] Uses consistent page padding (16dp horizontal)

### Component Usage
- [ ] Uses appropriate GH components for functionality
- [ ] No nested cards (check GitHub widgets)
- [ ] Proper card padding variants (standard/compact/zero)
- [ ] Uses `GHButton` for all buttons
- [ ] Uses `GHLoadingIndicator` for loading states
- [ ] Uses `GHEmptyState` for empty states
- [ ] Uses GitHub widgets for content (GHUserCard, GHRepositoryCard, etc.)

### Spacing Standards
- [ ] Sections separated by 20dp
- [ ] Related items separated by 8dp
- [ ] Unrelated items separated by 12dp
- [ ] Follows spacing standards between elements

### Accessibility & UX
- [ ] Touch targets meet 48dp minimum
- [ ] No duplicate information (app bar vs content)
- [ ] Proper loading and error states
- [ ] Consistent interaction patterns

### Technical Standards
- [ ] Follows Material Design principles
- [ ] Uses design tokens consistently
- [ ] Implements proper state management

## Examples

### Good: Home Screen Structure
```dart
GHScreenTemplate(
  title: "GitHub",
  showBackButton: false,  // Root screen
  body: GHListTemplate(
    children: [
      // User card (no extra wrapper)
      GHUserCard.fromFakeUser(user),
      
      SizedBox(height: GHTokens.spacing20), // Section break
      
      // Quick actions section
      _buildQuickActions(),
      
      SizedBox(height: GHTokens.spacing20), // Section break
      
      // Activity section with compact cards
      ...activities.map((activity) => Padding(
        padding: EdgeInsets.only(bottom: GHTokens.spacing8), // Related items
        child: GHCard(
          padding: EdgeInsets.zero,  // ListTile has own padding
          child: ListTile(...),
        ),
      )),
    ],
  ),
)
```

### Good: User Details Navigation
```dart
// Instead of tabs, use action list
Column(
  children: [
    GHCard(
      onTap: () => NavigationService.push('/user/repos'),
      child: ListTile(
        leading: Icon(Icons.folder),
        title: Text('Repositories'),
        subtitle: Text('128 public repositories'),
        trailing: Icon(Icons.chevron_right),
      ),
    ),
    SizedBox(height: GHTokens.spacing12),
    
    GHCard(
      onTap: () => NavigationService.push('/user/starred'),
      child: ListTile(
        leading: Icon(Icons.star),
        title: Text('Starred'),
        subtitle: Text('1,234 starred repositories'),
        trailing: Icon(Icons.chevron_right),
      ),
    ),
    // ... more actions
  ],
)
```

## Version History

- **v1.1** (2025-01-28): Comprehensive component guide
  - Added complete component catalog with use cases
  - Component quick reference table
  - Detailed usage examples and code snippets
  - Component usage rules and patterns
  - Updated implementation checklist

- **v1.0** (2025-01-28): Initial standards based on user feedback
  - Push navigation pattern
  - Spacing consistency rules
  - Component usage guidelines
  - Material Design alignment