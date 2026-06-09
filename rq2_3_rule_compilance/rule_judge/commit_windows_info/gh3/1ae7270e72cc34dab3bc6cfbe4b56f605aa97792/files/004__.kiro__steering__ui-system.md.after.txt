# UI System Architecture

## Overview

The gh3 application uses a comprehensive Material Design 3-based UI system with reusable widgets and consistent layout patterns. This document defines the high-level widget architecture, information display specifications, and design patterns for all GitHub mobile screens.

## Design Principles

### Information Hierarchy
- **Primary Information**: Most important data displayed prominently (titles, names, primary status)
- **Secondary Information**: Supporting details (descriptions, metadata, counts)
- **Tertiary Information**: Additional context (timestamps, minor details, helper text)
- **Interactive Elements**: Clear action affordances with proper touch targets (44dp minimum)
- **Status Indicators**: System state communication with color-coded badges and consistent meaning

### Material Design 3 Foundation
- Consistent spacing, typography, and colors
- Accessible contrast ratios and touch targets
- Dynamic color theming support
- Elevation and surface treatment
- Motion and interaction patterns

## Core Design Tokens

### Colors
```dart
// Primary GitHub brand colors
primary: Color(0xFF0969DA)
onPrimary: Color(0xFFFFFFFF)
primaryContainer: Color(0xFFDDE6F4)
onPrimaryContainer: Color(0xFF0A1929)

// GitHub-specific semantic colors
success: Color(0xFF1A7F37)  // Open issues, success states
warning: Color(0xFFBF8700)  // Warnings, pending states
error: Color(0xFFCF222E)    // Closed issues, error states
merged: Color(0xFF8250DF)   // Merged PRs
draft: Color(0xFF656D76)    // Draft PRs, disabled states
```

### Typography Scale
- **Headline Large**: 32sp, titles and hero text
- **Headline Medium**: 28sp, screen titles
- **Title Large**: 22sp, section headers
- **Title Medium**: 16sp, card titles
- **Body Large**: 16sp, primary content
- **Body Medium**: 14sp, secondary content
- **Label Large**: 14sp, button text
- **Label Medium**: 12sp, metadata and captions

### Spacing System
- **4dp**: Micro spacing (icon gaps)
- **8dp**: Small spacing (chip gaps)
- **12dp**: Medium spacing (section padding)
- **16dp**: Standard spacing (card padding)
- **20dp**: Large spacing (section margins)
- **24dp**: XL spacing (screen padding)
- **32dp**: XXL spacing (major sections)

## 1. Layout Widgets

### GHScreenTemplate
**Purpose**: Standard screen structure for all GitHub screens

**Information Display**:
- Screen title in app bar with consistent styling
- Optional back navigation with proper touch target
- Action buttons (star, share, etc.) in app bar
- Optional floating action button for primary actions
- Consistent padding and spacing throughout

**Usage**:
```dart
GHScreenTemplate(
  title: "Repository Name",
  actions: [StarButton(), ShareButton()],
  floatingAction: FloatingStarButton(),
  body: screenContent,
)
```

**Design Specifications**:
- App bar height: 56dp
- App bar title: Title Large typography
- Action button touch target: 48x48dp
- Screen padding: 16dp horizontal, 0dp vertical
- Floating action button: 56x56dp

### GHListTemplate  
**Purpose**: Standard list/feed layout with pull-to-refresh and search

**Information Display**:
- Optional search bar at top with clear placeholder text
- Optional filter chips below search with count indicators
- Scrollable list with pull-to-refresh capability
- Loading states with skeleton screens
- Empty states with helpful messaging
- Infinite scroll pagination with loading indicators

**Usage**:
```dart
GHListTemplate(
  searchHint: "Search issues...",
  filters: [OpenFilter(), ClosedFilter(), LabelFilters()],
  items: listOfItems,
  onRefresh: () => refresh(),
  onLoadMore: () => loadMore(),
)
```

**Design Specifications**:
- Search bar height: 48dp
- Filter chip height: 32dp
- List item minimum height: 72dp
- Pull-to-refresh trigger: 80dp
- Loading indicator size: 24x24dp

### GHContentTemplate
**Purpose**: Single content view with sections and metadata

**Information Display**:
- Main content area with vertical scrolling
- Clear section dividers and spacing
- Metadata displayed in structured format
- Action buttons contextually placed
- Responsive layout for different screen sizes

**Usage**:
```dart
GHContentTemplate(
  header: IssueHeader(),
  sections: [
    ContentSection(), 
    CommentsSection(),
    MetadataSection()
  ],
  actions: [EditButton(), CommentButton()],
)
```

**Design Specifications**:
- Section spacing: 24dp between major sections
- Content padding: 16dp horizontal
- Section divider: 1dp height with surface variant color
- Action button spacing: 8dp between buttons

## 2. Header & Summary Widgets

### GHEntityHeader
**Purpose**: Display primary information about any GitHub entity (repository, user, issue)

**Information Display**:
- Entity name/title with primary typography
- Description/subtitle with secondary typography
- Key statistics (stars, forks, followers) with icons
- Status indicators (open/closed, public/private) with color coding
- Language indicators with color dots
- Action buttons (star, follow, watch) with proper spacing

**Usage**:
```dart
GHEntityHeader(
  title: "facebook/react",
  description: "A declarative library for building UIs",
  avatar: RepositoryIcon(),
  stats: [
    StatItem(icon: Icons.star, count: 45200, label: "stars"),
    StatItem(icon: Icons.fork, count: 8900, label: "forks"),
    StatItem(colorDot: Colors.blue, label: "JavaScript"),
  ],
  status: PublicBadge(),
  actions: [StarButton(), WatchButton()],
)
```

**Design Specifications**:
- Header padding: 16dp all sides
- Title typography: Headline Medium
- Description typography: Body Large
- Stat icon size: 16x16dp
- Language color dot: 12x12dp circle
- Action button minimum size: 48x48dp

### GHUserHeader
**Purpose**: Display user/organization profile information

**Information Display**:
- Profile avatar (48x48dp) with rounded corners
- Display name with primary typography
- Username with secondary typography and @ prefix
- Bio/description with proper line height
- Location and company with icons
- Follower/following counts with clear labels
- Join date information

**Usage**:
```dart
GHUserHeader(
  avatar: CircleAvatar(url: user.avatarUrl),
  displayName: "John Doe",
  username: "@johndoe",
  bio: "Software developer passionate about open source",
  location: "San Francisco, CA",
  company: "GitHub",
  stats: [
    StatItem(count: 1200, label: "followers"),
    StatItem(count: 345, label: "following"),
  ],
)
```

**Design Specifications**:
- Avatar size: 48x48dp with 8dp radius
- Display name typography: Title Large
- Username typography: Body Medium with onSurfaceVariant color
- Bio typography: Body Medium with 1.5 line height
- Metadata icon size: 16x16dp
- Stat spacing: 16dp between items

## 3. Navigation & Menu Widgets

### GHNavigationGrid
**Purpose**: Grid of navigation cards for main actions

**Information Display**:
- Action title with clear hierarchy
- Brief description for context
- Icon representation for quick recognition
- Count badges when applicable
- Visual hierarchy with consistent spacing

**Usage**:
```dart
GHNavigationGrid(
  items: [
    NavItem(
      icon: Icons.code,
      title: "Code",
      description: "Browse repository files",
      onTap: () => navigateToCode(),
    ),
    NavItem(
      icon: Icons.bug_report,
      title: "Issues",
      badge: "23 open",
      onTap: () => navigateToIssues(),
    ),
    NavItem(
      icon: Icons.merge_type,
      title: "Pull Requests", 
      badge: "5 open",
      onTap: () => navigateToPRs(),
    ),
  ],
)
```

**Design Specifications**:
- Grid item height: 88dp minimum
- Grid spacing: 8dp between items
- Icon size: 24x24dp
- Title typography: Title Medium
- Description typography: Body Medium
- Badge typography: Label Medium

### GHTabMenu
**Purpose**: Horizontal scrollable tab navigation

**Information Display**:
- Tab titles with clear active/inactive states
- Count badges for relevant tabs
- Scroll indicators when content overflows
- Smooth transition animations

**Usage**:
```dart
GHTabMenu(
  tabs: [
    TabItem(title: "Code", isActive: true),
    TabItem(title: "Issues", badge: "23"),
    TabItem(title: "Pull Requests", badge: "5"),
    TabItem(title: "Actions"),
  ],
  onTabChanged: (index) => switchTab(index),
)
```

**Design Specifications**:
- Tab height: 48dp
- Tab padding: 16dp horizontal, 12dp vertical
- Active indicator height: 2dp
- Badge size: minimum 16x16dp
- Typography: Label Large

## 4. Content Display Widgets

### GHIssueCard
**Purpose**: Display issue/PR summary in lists

**Information Display**:
- Issue number with # prefix for identification
- Issue title with proper truncation
- Status icon and badge (open/closed/merged) with semantic colors
- Labels as colored chips with consistent styling
- Author avatar (24x24dp) and name
- Creation/update timestamp in relative format
- Assignee information when present
- Comment count indicator with icon

**Usage**:
```dart
GHIssueCard(
  number: 1234,
  title: "Add dark mode support",
  status: IssueStatus.open,
  author: UserMini(avatar: avatar, name: "johndoe"),
  timestamp: "2 hours ago",
  labels: ["enhancement", "ui"],
  commentCount: 5,
  assignee: UserMini(avatar: avatar, name: "janedoe"),
  onTap: () => openIssue(1234),
)
```

**Design Specifications**:
- Card padding: 16dp all sides
- Card elevation: 1dp
- Status icon size: 16x16dp
- Author avatar size: 24x24dp
- Label chip height: 24dp
- Comment icon size: 16x16dp
- Minimum touch target: 48dp height

### GHFileCard
**Purpose**: Display file/folder information in directory listings

**Information Display**:
- File/folder icon based on type and extension
- File name with proper truncation
- Last commit message with ellipsis
- Last modified timestamp in relative format
- File size for files (formatted appropriately)
- Directory indicator for folders
- Author information for last modification

**Usage**:
```dart
GHFileCard(
  name: "README.md",
  type: FileType.markdown,
  lastCommit: "Update installation instructions",
  lastModified: "3 days ago",
  author: "johndoe",
  size: "2.4 KB",
  onTap: () => openFile("README.md"),
)
```

**Design Specifications**:
- List item height: 72dp
- Icon size: 24x24dp
- File name typography: Body Large
- Commit message typography: Body Medium
- Metadata typography: Label Medium
- Chevron icon: 16x16dp

### GHRepositoryCard
**Purpose**: Display repository summary in lists

**Information Display**:
- Repository name and owner with clear hierarchy
- Description text with proper line limits
- Primary language with color indicator dot
- Star and fork counts with icons
- Last updated timestamp
- Visibility indicator (public/private badge)

**Usage**:
```dart
GHRepositoryCard(
  owner: "facebook",
  name: "react",
  description: "A declarative library for building UIs",
  language: Language(name: "JavaScript", color: Colors.yellow),
  starCount: 45200,
  forkCount: 8900,
  lastUpdated: "2 hours ago",
  visibility: Visibility.public,
  onTap: () => openRepository("facebook/react"),
)
```

**Design Specifications**:
- Card padding: 16dp
- Card spacing: 8dp between cards
- Owner/name typography: Title Medium
- Description typography: Body Medium
- Language dot size: 12x12dp
- Stat icon size: 16x16dp

## 5. Filter & Search Widgets

### GHFilterBar
**Purpose**: Horizontal scrollable filter options

**Information Display**:
- Filter categories as chips with clear labels
- Active/inactive states with color differentiation
- Count indicators for each filter category
- Clear all filters option when filters are active
- Smooth horizontal scrolling

**Usage**:
```dart
GHFilterBar(
  filters: [
    FilterChip(label: "Open", count: 23, isActive: true),
    FilterChip(label: "Closed", count: 145, isActive: false),
    FilterChip(label: "bug", color: Colors.red, isActive: false),
    FilterChip(label: "enhancement", color: Colors.blue, isActive: false),
  ],
  onFilterChanged: (filter) => applyFilter(filter),
  onClearAll: () => clearFilters(),
)
```

**Design Specifications**:
- Filter chip height: 32dp
- Chip spacing: 8dp horizontal
- Active chip background: primaryContainer
- Inactive chip background: surfaceVariant
- Count badge: minimum 16x16dp

### GHSearchHeader
**Purpose**: Search input with suggestions and filters

**Information Display**:
- Search input field with descriptive placeholder
- Search suggestions dropdown with recent/popular queries
- Quick filter buttons below input
- Results count indicator
- Clear search functionality

**Usage**:
```dart
GHSearchHeader(
  placeholder: "Search issues and pull requests",
  suggestions: ["is:open", "is:closed", "label:bug"],
  quickFilters: ["Open issues", "My issues", "Assigned to me"],
  resultCount: "142 results",
  onSearch: (query) => performSearch(query),
)
```

**Design Specifications**:
- Search field height: 48dp
- Search field radius: 8dp
- Suggestion item height: 40dp
- Quick filter chip height: 32dp
- Results text typography: Label Medium

## 6. Status & Metadata Widgets

### GHStatusIndicator
**Purpose**: Display status information with appropriate semantic colors

**Information Display**:
- Status text with clear labeling
- Color-coded background following GitHub conventions
- Status icon when applicable for better recognition
- Timestamp of status change for context

**Usage**:
```dart
GHStatusIndicator(
  status: Status.open,
  text: "Open",
  timestamp: "opened 2 days ago",
  icon: Icons.error_outline,
  color: Colors.green,
)
```

**Design Specifications**:
- Badge height: 24dp minimum
- Badge radius: 12dp (pill shape)
- Icon size: 16x16dp
- Typography: Label Medium
- Color mapping:
  - Open: success color (#1A7F37)
  - Closed: error color (#CF222E)
  - Merged: merged color (#8250DF)
  - Draft: draft color (#656D76)

### GHMetadataSection
**Purpose**: Display metadata information in structured format

**Information Display**:
- Key-value pairs with clear visual hierarchy
- Links to related entities with proper styling
- Expandable/collapsible sections for space efficiency
- Copy-to-clipboard functionality for relevant data

**Usage**:
```dart
GHMetadataSection(
  title: "Details",
  items: [
    MetadataItem(label: "Assignees", value: "johndoe, janedoe"),
    MetadataItem(label: "Labels", value: LabelChips()),
    MetadataItem(label: "Milestone", value: "v2.0", isLink: true),
    MetadataItem(label: "Projects", value: "Mobile App Redesign"),
  ],
  isCollapsible: true,
)
```

**Design Specifications**:
- Section padding: 16dp
- Item spacing: 8dp vertical
- Label typography: Label Medium
- Value typography: Body Medium
- Link color: primary color
- Collapse icon size: 16x16dp

## 7. Action Widgets

### GHActionButton
**Purpose**: Primary and secondary action buttons

**Information Display**:
- Action text/label with clear hierarchy
- Optional icon for better recognition
- Loading states with spinner animation
- Disabled states with reduced opacity
- Count indicators (for star, watch, etc.)

**Usage**:
```dart
GHActionButton(
  label: "Star",
  icon: Icons.star_border,
  count: 1200,
  style: ActionStyle.primary,
  isLoading: false,
  onPressed: () => toggleStar(),
)
```

**Design Specifications**:
- Button height: 40dp (medium), 48dp (large)
- Button radius: 8dp
- Icon size: 18x18dp
- Typography: Label Large
- Minimum touch target: 48x48dp
- Loading spinner: 16x16dp

### GHActionSheet
**Purpose**: Bottom sheet with multiple action options

**Information Display**:
- Sheet title with clear context
- List of available actions with descriptions
- Destructive action indicators with warning colors
- Icons for each action for quick recognition
- Proper spacing and touch targets

**Usage**:
```dart
GHActionSheet(
  title: "Repository Actions",
  actions: [
    ActionItem(
      title: "Star repository", 
      icon: Icons.star,
      onTap: () => star(),
    ),
    ActionItem(
      title: "Watch repository",
      icon: Icons.visibility,
      onTap: () => watch(),
    ),
    ActionItem(
      title: "Report issue",
      icon: Icons.flag,
      isDestructive: true,
      onTap: () => report(),
    ),
  ],
)
```

**Design Specifications**:
- Sheet max height: 60% of screen
- Sheet radius: 16dp top corners
- Action item height: 56dp
- Action icon size: 24x24dp
- Title typography: Title Medium
- Action typography: Body Large

## 8. Common Layout Patterns

### GHFeedLayout
**Purpose**: Standard feed/timeline layout pattern

**Information Display**:
- Chronological list of items with clear time grouping
- Time-based grouping headers (Today, Yesterday, etc.)
- Infinite scroll with smooth loading indicators
- Pull-to-refresh capability with visual feedback
- Empty state messaging with helpful guidance

**Usage**:
```dart
GHFeedLayout(
  groupBy: GroupBy.date,
  items: [
    FeedGroup(
      header: "Today",
      items: [item1, item2, item3],
    ),
    FeedGroup(
      header: "Yesterday", 
      items: [item4, item5],
    ),
  ],
  emptyState: EmptyFeedMessage(
    icon: Icons.inbox,
    title: "No recent activity",
    subtitle: "Activity will appear here as it happens",
  ),
)
```

**Design Specifications**:
- Group header height: 40dp
- Group header typography: Title Medium
- Item spacing: 8dp between items
- Section spacing: 24dp between groups
- Empty state icon size: 48x48dp

### GHMasterDetailLayout
**Purpose**: Two-pane layout for tablets/wide screens

**Information Display**:
- Master list on left (30-40% width) with clear selection
- Detail view on right (60-70% width) with full content
- Selected item highlighting in master list
- Responsive behavior for mobile (stack vertically)

**Usage**:
```dart
GHMasterDetailLayout(
  masterPane: IssueList(
    items: issues,
    selectedId: currentIssueId,
    onSelectionChanged: (id) => selectIssue(id),
  ),
  detailPane: IssueDetail(
    issue: selectedIssue,
  ),
  breakpoint: 600, // Switch to stacked on mobile
)
```

**Design Specifications**:
- Breakpoint: 600dp width
- Master pane width: 40% on tablet
- Detail pane width: 60% on tablet
- Divider width: 1dp
- Selected item background: primaryContainer

### GHModalLayout
**Purpose**: Full-screen modal presentation

**Information Display**:
- Modal header with clear title and close button
- Scrollable content area with proper padding
- Optional bottom action bar with primary/secondary actions
- Backdrop dimming for focus

**Usage**:
```dart
GHModalLayout(
  title: "Create New Issue",
  content: IssueForm(),
  actions: [
    SecondaryButton(text: "Cancel"),
    PrimaryButton(text: "Create Issue"),
  ],
  onClose: () => closeModal(),
)
```

**Design Specifications**:
- Modal radius: 16dp top corners
- Header height: 56dp
- Close button size: 48x48dp
- Content padding: 16dp horizontal
- Action bar height: 72dp

## 9. Specialized Content Widgets

### GHCodeViewer
**Purpose**: Display code content with syntax highlighting

**Information Display**:
- Syntax-highlighted code with language-appropriate colors
- Optional line numbers with proper alignment
- Copy to clipboard functionality with user feedback
- Language indicator badge
- File size and encoding information
- Horizontal scroll for long lines

**Usage**:
```dart
GHCodeViewer(
  content: codeString,
  language: "dart",
  showLineNumbers: true,
  fileName: "main.dart",
  fileSize: "2.4 KB",
  encoding: "UTF-8",
  onCopy: () => copyCode(),
)
```

**Design Specifications**:
- Font family: monospace
- Font size: 14sp
- Line height: 1.4
- Line number width: 48dp
- Code padding: 16dp
- Copy button size: 32x32dp

### GHMarkdownViewer
**Purpose**: Display markdown content (README, comments, etc.)

**Information Display**:
- Rendered markdown with GitHub-style formatting
- Code syntax highlighting in code blocks
- Link handling for GitHub references (@mentions, #issues)
- Image display with responsive sizing
- Table formatting with proper alignment

**Usage**:
```dart
GHMarkdownViewer(
  content: markdownString,
  baseUrl: "https://github.com/owner/repo",
  onLinkTap: (url) => handleLink(url),
  theme: MarkdownTheme.github,
)
```

**Design Specifications**:
- Base font size: 16sp (Body Large)
- Heading scale: 1.25 ratio
- Code font: monospace, 14sp
- Link color: primary color
- Block quote border: 4dp left, primaryContainer color

### GHCommentThread
**Purpose**: Display threaded comments/discussions

**Information Display**:
- User avatars (32x32dp) with proper spacing
- User names with timestamp information
- Nested reply structure with indentation
- Reaction indicators with counts
- Edit/delete actions when applicable
- Threading lines for visual hierarchy

**Usage**:
```dart
GHCommentThread(
  comments: [
    Comment(
      author: User(name: "johndoe", avatar: avatar),
      content: "This looks good to me!",
      timestamp: "2 hours ago",
      reactions: [Reaction.thumbsUp(3), Reaction.heart(1)],
      replies: [nestedComment],
    ),
  ],
  onReply: (commentId) => replyToComment(commentId),
  onReact: (commentId, reaction) => addReaction(commentId, reaction),
)
```

**Design Specifications**:
- Avatar size: 32x32dp
- Reply indentation: 48dp
- Comment padding: 16dp
- Reaction button size: 32x24dp
- Threading line width: 2dp
- Threading line color: surfaceVariant

## Implementation Guidelines

### Widget Architecture
- All widgets extend StatelessWidget when possible
- Use composition over inheritance
- Implement proper const constructors
- Follow single responsibility principle

### Accessibility
- Minimum touch target size: 48x48dp
- Color contrast ratio: 4.5:1 for normal text, 3:1 for large text
- Screen reader support with semantic labels
- Keyboard navigation support

### Performance
- Use const constructors for static widgets
- Implement proper key usage for list items
- Lazy loading for large lists
- Image caching and optimization

### Testing
- Unit tests for all business logic
- Widget tests for UI components
- Integration tests for user flows
- Accessibility testing with screen readers

## Migration Strategy

### Phase 1: Core Components
1. Implement design tokens and theme
2. Create base layout widgets
3. Build core navigation components

### Phase 2: Content Widgets
1. Implement specialized GitHub widgets
2. Create filter and search components
3. Build action and status widgets

### Phase 3: Screen Implementation
1. Migrate existing screens to new system
2. Implement P1 screens using widget system
3. Create comprehensive widget documentation

### Phase 4: Enhancement
1. Add advanced interaction patterns
2. Implement micro-interactions and animations
3. Optimize performance and accessibility

This UI system provides a comprehensive foundation for building consistent, accessible, and maintainable GitHub mobile interfaces while following Material Design 3 principles and GitHub-specific design patterns.

## Screen Layout Specifications

### Home Screen Layout
**Purpose**: Authenticated user dashboard showing personalized GitHub activity

**Layout Structure**:
```dart
GHScreenTemplate(
  title: "GitHub",
  showBackButton: false,
  actions: [NotificationButton(), ProfileButton()],
  body: GHListTemplate(
    searchHint: "Search repositories, users, issues...",
    onRefresh: () => refreshFeed(),
    children: [
      // User profile summary
      GHUserSummaryCard(
        user: currentUser,
        onTap: () => navigateToProfile(),
      ),
      
      // Quick actions grid
      GHNavigationGrid(
        title: "Quick Actions",
        items: [
          NavItem(icon: Icons.star, title: "Starred", count: "45"),
          NavItem(icon: Icons.folder, title: "Repositories", count: "12"),
          NavItem(icon: Icons.people, title: "Organizations", count: "3"),
          NavItem(icon: Icons.notifications, title: "Notifications"),
        ],
      ),
      
      // Recent activity feed
      GHFeedLayout(
        title: "Recent Activity",
        groupBy: GroupBy.date,
        items: activityItems,
        emptyState: EmptyFeedMessage(
          icon: Icons.timeline,
          title: "No recent activity",
          subtitle: "Your GitHub activity will appear here",
        ),
      ),
      
      // Trending repositories
      GHContentSection(
        title: "Trending Today",
        actions: [TextButton(text: "See all")],
        content: Column(
          children: trendingRepos.map((repo) => 
            GHRepositoryCard.fromRepo(repo)
          ).toList(),
        ),
      ),
    ],
  ),
)
```

**Information Display**:
- User avatar and basic profile info at top
- Quick access to starred repos, personal repos, organizations
- Chronological activity feed with time grouping
- Trending repositories discovery section
- Search bar for global GitHub search
- Notification indicator in app bar

**Design Specifications**:
- User summary card height: 88dp
- Quick action grid: 2x2 layout on mobile
- Activity item height: 72dp minimum
- Trending repo card: 120dp height
- Pull-to-refresh threshold: 80dp

### User Details Screen Layout
**Purpose**: Display comprehensive user profile information and repositories

**Layout Structure**:
```dart
GHScreenTemplate(
  title: user.displayName ?? user.username,
  actions: [ShareButton(), MoreActionsButton()],
  body: GHListTemplate(
    onRefresh: () => refreshUserData(),
    children: [
      // User profile header
      GHUserHeader(
        avatar: CircleAvatar(radius: 40, url: user.avatarUrl),
        displayName: user.displayName,
        username: user.username,
        bio: user.bio,
        location: user.location,
        company: user.company,
        website: user.website,
        stats: [
          StatItem(count: user.followers, label: "followers"),
          StatItem(count: user.following, label: "following"),
          StatItem(count: user.publicRepos, label: "repositories"),
        ],
        joinDate: user.createdAt,
      ),
      
      // Action buttons
      Row(
        children: [
          Expanded(child: GHActionButton(
            label: isFollowing ? "Unfollow" : "Follow",
            style: ActionStyle.primary,
            onPressed: () => toggleFollow(),
          )),
          SizedBox(width: 8),
          GHActionButton(
            icon: Icons.message,
            style: ActionStyle.secondary,
            onPressed: () => openChat(),
          ),
        ],
      ),
      
      // Navigation tabs
      GHTabMenu(
        tabs: [
          TabItem(title: "Repositories", badge: "${user.publicRepos}"),
          TabItem(title: "Starred", badge: "${user.starredRepos}"),
          TabItem(title: "Organizations", badge: "${user.organizations.length}"),
          TabItem(title: "Projects"),
        ],
        selectedIndex: currentTab,
        onTabChanged: (index) => switchTab(index),
      ),
      
      // Tab content
      if (currentTab == 0) ...[
        // Repositories tab
        GHFilterBar(
          filters: [
            FilterChip(label: "All", isActive: true),
            FilterChip(label: "Sources"),
            FilterChip(label: "Forks"),
            FilterChip(label: "Archived"),
          ],
        ),
        SearchBar(hintText: "Find a repository..."),
        ...repositories.map((repo) => GHRepositoryCard.fromRepo(repo)),
      ],
      
      if (currentTab == 1) ...[
        // Starred repositories
        SearchBar(hintText: "Search starred repositories..."),
        ...starredRepos.map((repo) => GHRepositoryCard.fromRepo(repo)),
      ],
      
      // Additional tabs content...
    ],
  ),
)
```

**Information Display**:
- Large profile avatar (80x80dp) with full user metadata
- Follow/unfollow action with current relationship status
- Tabbed navigation for different content types
- Repository listings with search and filter capabilities
- Organization memberships and projects
- Social proof through follower/following counts

**Design Specifications**:
- Profile avatar: 80x80dp with 16dp radius
- Header section height: 280dp minimum
- Tab bar height: 48dp
- Repository card spacing: 8dp vertical
- Action button height: 48dp

### Repository Details Screen Layout
**Purpose**: Display comprehensive repository information and navigation

**Layout Structure**:
```dart
GHScreenTemplate(
  title: "${repo.owner}/${repo.name}",
  actions: [StarButton(), ShareButton(), MoreActionsButton()],
  floatingAction: FloatingActionButton(
    child: Icon(repo.isStarred ? Icons.star : Icons.star_border),
    onPressed: () => toggleStar(),
  ),
  body: GHContentTemplate(
    sections: [
      // Repository header
      GHEntityHeader(
        title: repo.name,
        subtitle: repo.description,
        avatar: repo.owner.avatarUrl != null 
          ? CircleAvatar(url: repo.owner.avatarUrl) 
          : null,
        stats: [
          StatItem(icon: Icons.star, count: repo.starCount, label: "stars"),
          StatItem(icon: Icons.fork_right, count: repo.forkCount, label: "forks"),
          StatItem(icon: Icons.visibility, count: repo.watcherCount, label: "watching"),
          if (repo.language != null)
            StatItem(
              colorIndicator: repo.languageColor,
              label: repo.language!,
            ),
        ],
        status: repo.isPrivate ? PrivateBadge() : PublicBadge(),
        actions: [
          GHActionButton(
            label: "Watch",
            icon: Icons.visibility,
            style: ActionStyle.secondary,
            onPressed: () => toggleWatch(),
          ),
          GHActionButton(
            label: "Fork",
            icon: Icons.fork_right,
            style: ActionStyle.secondary,
            onPressed: () => forkRepository(),
          ),
        ],
      ),
      
      // Repository navigation
      GHNavigationMenu(
        items: [
          GHNavigationItem(
            icon: Icons.code,
            title: "Code",
            subtitle: "Browse source files",
            onTap: () => navigateToCode(),
          ),
          GHNavigationItem(
            icon: Icons.bug_report,
            title: "Issues",
            badge: "${repo.openIssues}",
            subtitle: "${repo.openIssues} open, ${repo.closedIssues} closed",
            onTap: () => navigateToIssues(),
          ),
          GHNavigationItem(
            icon: Icons.merge_type,
            title: "Pull Requests",
            badge: "${repo.openPRs}",
            subtitle: "${repo.openPRs} open, ${repo.mergedPRs} merged",
            onTap: () => navigateToPRs(),
          ),
          GHNavigationItem(
            icon: Icons.play_circle,
            title: "Actions",
            trailing: repo.lastWorkflowStatus != null 
              ? GHStatusIndicator(status: repo.lastWorkflowStatus!) 
              : null,
            onTap: () => navigateToActions(),
          ),
          GHNavigationItem(
            icon: Icons.security,
            title: "Security",
            onTap: () => navigateToSecurity(),
          ),
          GHNavigationItem(
            icon: Icons.insights,
            title: "Insights",
            onTap: () => navigateToInsights(),
          ),
        ],
      ),
      
      // Repository metadata
      GHMetadataSection(
        title: "About",
        items: [
          if (repo.topics.isNotEmpty)
            MetadataItem(
              label: "Topics",
              value: Wrap(
                children: repo.topics.map((topic) => 
                  GHChip(label: topic)
                ).toList(),
              ),
            ),
          if (repo.license != null)
            MetadataItem(label: "License", value: repo.license!),
          if (repo.homepage != null)
            MetadataItem(
              label: "Website", 
              value: repo.homepage!, 
              isLink: true,
            ),
          MetadataItem(
            label: "Last updated", 
            value: formatDate(repo.updatedAt),
          ),
        ],
      ),
      
      // README section
      if (repo.readme != null)
        GHContentSection(
          title: "README",
          content: GHMarkdownViewer(
            content: repo.readme!,
            baseUrl: repo.url,
          ),
        ),
      
      // Recent releases
      if (repo.releases.isNotEmpty)
        GHContentSection(
          title: "Releases",
          actions: [TextButton(text: "View all")],
          content: Column(
            children: repo.releases.take(3).map((release) =>
              GHReleaseCard(release: release)
            ).toList(),
          ),
        ),
      
      // Contributors
      GHContentSection(
        title: "Contributors",
        actions: [TextButton(text: "View all ${repo.contributorCount}")],
        content: Row(
          children: repo.topContributors.map((contributor) =>
            Padding(
              padding: EdgeInsets.only(right: 8),
              child: CircleAvatar(
                radius: 20,
                backgroundImage: NetworkImage(contributor.avatarUrl),
              ),
            )
          ).toList(),
        ),
      ),
    ],
  ),
)
```

**Information Display**:
- Repository name, description, and key statistics
- Owner information with avatar
- Star/watch/fork actions prominently displayed
- Clear navigation to different repository sections
- README content with proper markdown rendering
- Recent releases and contributor information
- Repository metadata (license, topics, links)

**Design Specifications**:
- Header section height: 200dp minimum
- Navigation menu item height: 64dp
- README section collapsible after 300dp
- Contributor avatar size: 40x40dp
- Floating action button: 56x56dp

### Starred Repositories Screen Layout
**Purpose**: Display user's starred repositories with search and filtering

**Layout Structure**:
```dart
GHScreenTemplate(
  title: "Starred Repositories",
  body: GHListTemplate(
    searchHint: "Search starred repositories...",
    filters: [
      FilterChip(label: "All", count: starredRepos.length, isActive: true),
      FilterChip(label: "Recently starred", isActive: false),
      FilterChip(label: "Recently active", isActive: false),
      ...languageFilters.map((lang) => FilterChip(
        label: lang.name,
        count: lang.count,
        colorIndicator: lang.color,
      )),
    ],
    onRefresh: () => refreshStarredRepos(),
    children: [
      // Filter summary
      if (hasActiveFilters)
        GHCard(
          child: Row(
            children: [
              Text(
                "${filteredRepos.length} of ${starredRepos.length} repositories",
                style: GHTokens.bodyMedium,
              ),
              Spacer(),
              TextButton(
                onPressed: () => clearFilters(),
                child: Text("Clear filters"),
              ),
            ],
          ),
        ),
      
      // Sort options
      GHCard(
        child: Row(
          children: [
            Icon(Icons.sort, size: 16),
            SizedBox(width: 8),
            Text("Sort by:", style: GHTokens.labelMedium),
            SizedBox(width: 8),
            DropdownButton<SortOption>(
              value: currentSort,
              items: [
                DropdownMenuItem(
                  value: SortOption.recentlyStarred,
                  child: Text("Recently starred"),
                ),
                DropdownMenuItem(
                  value: SortOption.recentlyUpdated,
                  child: Text("Recently updated"),
                ),
                DropdownMenuItem(
                  value: SortOption.name,
                  child: Text("Name"),
                ),
                DropdownMenuItem(
                  value: SortOption.stars,
                  child: Text("Stars"),
                ),
              ],
              onChanged: (sort) => changeSortOrder(sort),
            ),
          ],
        ),
      ),
      
      // Repository list
      ...filteredRepos.map((repo) => GHRepositoryCard(
        owner: repo.owner,
        name: repo.name,
        description: repo.description,
        language: repo.language,
        starCount: repo.starCount,
        forkCount: repo.forkCount,
        lastUpdated: repo.updatedAt,
        starredAt: repo.starredAt, // Show when user starred
        onTap: () => openRepository(repo),
        onUnstar: () => unstarRepository(repo),
      )),
      
      // Empty state
      if (filteredRepos.isEmpty && !isLoading)
        EmptyState(
          icon: Icons.star_border,
          title: hasActiveFilters 
            ? "No repositories match your filters"
            : "No starred repositories",
          subtitle: hasActiveFilters
            ? "Try adjusting your search or filters"
            : "Star repositories to see them here",
          action: hasActiveFilters 
            ? ActionButton(text: "Clear filters", onPressed: clearFilters)
            : ActionButton(text: "Explore repositories", onPressed: explore),
        ),
    ],
  ),
)
```

**Information Display**:
- Total count of starred repositories
- Advanced filtering by language, activity, date starred
- Sort options (recently starred, updated, name, stars)
- Repository cards with starring timestamp
- Quick unstar action on each card
- Empty states for no results or no starred repos
- Search functionality across starred repos

**Design Specifications**:
- Filter chip bar height: 48dp
- Sort dropdown height: 40dp
- Repository card height: 120dp with starred date
- Empty state icon size: 64x64dp
- Unstar button size: 32x32dp
- Search results update: 300ms debounce

**Common Design Patterns Across Screens**:
- Consistent header treatment with actions
- Pull-to-refresh on all list screens
- Search integration where appropriate
- Empty states with helpful messaging
- Loading states with skeleton screens
- Error states with retry options
- Accessibility support throughout
- Responsive layout for different screen sizes

## Implementation Status

The UI system has been implemented across 4 phases with comprehensive components, examples, and testing:

- ✅ **Phase 1**: Foundation & core components (design tokens, theme, basic components)
- ✅ **Phase 2**: GitHub content widgets & layout system  
- ✅ **Phase 3**: Complete example screens & navigation
- ✅ **Phase 4**: Demo-ready application with stakeholder review capabilities

For detailed implementation tracking, see:
- [Implementation Specs](.kiro/specs/) - Requirements, design, and task tracking for each phase
- [Migration Workstream](.kiro/workstreams/ui-system-migration/) - Progress tracking and feedback
- [Developer Documentation](../../lib/src/ui-system/README.md) - Technical implementation guide

## UAT Demo Application

### Quick Start
```bash
# Run UAT app on web (recommended for stakeholder review)
flutter run -d chrome --target=lib/main_ui_system_uat.dart

# Run on mobile platforms  
flutter run -d ios --target=lib/main_ui_system_uat.dart
flutter run -d android --target=lib/main_ui_system_uat.dart
```

### UAT Features
- **Cross-Platform Compatibility**: Works on web, iOS, and Android
- **Interactive Theme Switching**: Live light/dark mode toggle
- **Complete Component Showcase**: All design system components with realistic data
- **Navigation System**: Easy access to design tokens, component catalog, and example screens

The UAT application provides stakeholders with a professional demonstration of the complete UI system while enabling developers to validate implementation quality and gather feedback for continuous improvement.