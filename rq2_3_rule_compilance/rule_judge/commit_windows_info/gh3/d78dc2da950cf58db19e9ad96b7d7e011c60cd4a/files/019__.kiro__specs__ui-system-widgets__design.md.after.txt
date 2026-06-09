# UI Widgets & Layout System Design

## Overview

The UI Widgets & Layout System builds upon the design tokens and core components from Phase 1 to deliver GitHub-specific widgets, layout templates, and content viewers. This design implements a comprehensive system of specialized widgets that provide consistent GitHub styling and behavior, along with flexible layout templates that enable rapid development of GitHub mobile screens.

The system focuses on creating reusable, composable widgets that follow the Widget-GraphQL separation pattern and provide rich interactions similar to the GitHub web experience. All components are designed with realistic fake data to enable comprehensive testing and stakeholder review.

## Architecture

### File Structure

The UI widgets system extends the existing `lib/src/ui-system/` structure:

```
lib/src/ui-system/
├── layouts/
│   ├── gh_screen_template.dart         # Standard screen structure
│   ├── gh_list_template.dart           # List layout with search/filters
│   └── gh_content_template.dart        # Content layout with sections
├── widgets/
│   ├── gh_repository_card.dart         # Repository display card
│   ├── gh_issue_card.dart              # Issue/PR display card
│   ├── gh_user_card.dart               # User profile card
│   ├── gh_file_tree_item.dart          # File/folder list item
│   ├── gh_entity_header.dart           # Entity header with stats
│   ├── gh_navigation_grid.dart         # Action grid layout
│   ├── gh_filter_bar.dart              # Horizontal filter chips
│   ├── gh_code_viewer.dart             # Code with syntax highlighting
│   └── gh_markdown_viewer.dart         # Markdown renderer
├── state_widgets/
│   ├── gh_empty_state.dart             # Empty state display
│   ├── gh_loading_indicator.dart       # Loading spinner
│   └── gh_error_state.dart             # Error state with retry
├── data/
│   ├── fake_data_service.dart          # Centralized fake data
│   ├── fake_repositories.dart          # Repository fake data
│   ├── fake_users.dart                 # User fake data
│   └── fake_issues.dart                # Issue/PR fake data
└── examples/
    ├── github_widgets_screen.dart      # GitHub widgets showcase
    ├── layout_patterns_screen.dart     # Layout templates demo
    ├── code_content_screen.dart        # Content viewers demo
    └── content_cards_screen.dart       # Interactive cards gallery
```

### Design Principles

1. **Widget-GraphQL Separation**: All widgets use explicit fields with factory constructors for GraphQL integration
2. **Composable Architecture**: Widgets can be combined to create complex layouts
3. **Consistent Information Hierarchy**: Primary, secondary, and tertiary information clearly distinguished
4. **Interactive Feedback**: All interactive elements provide immediate visual feedback
5. **Realistic Data**: Comprehensive fake data system enables proper evaluation
6. **Performance Optimized**: Efficient rendering with proper key usage and const constructors

## Components and Interfaces

### Layout Templates

#### GHScreenTemplate

The standard screen structure for all GitHub screens:

```dart
class GHScreenTemplate extends StatelessWidget {
  final String title;
  final List<Widget>? actions;
  final Widget body;
  final FloatingActionButton? floatingActionButton;
  final bool showBackButton;
  final PreferredSizeWidget? bottom;
  
  const GHScreenTemplate({
    super.key,
    required this.title,
    this.actions,
    required this.body,
    this.floatingActionButton,
    this.showBackButton = true,
    this.bottom,
  });
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          title,
          style: GHTokens.titleLarge,
        ),
        automaticallyImplyLeading: showBackButton,
        actions: actions,
        bottom: bottom,
        elevation: 0,
        surfaceTintColor: Theme.of(context).colorScheme.surface,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing16,
          ),
          child: body,
        ),
      ),
      floatingActionButton: floatingActionButton,
    );
  }
}
```

#### GHListTemplate

List layout with search, filters, and pull-to-refresh:

```dart
class GHListTemplate extends StatefulWidget {
  final String? searchHint;
  final List<Widget>? filters;
  final List<Widget> children;
  final Future<void> Function()? onRefresh;
  final VoidCallback? onLoadMore;
  final Function(String)? onSearch;
  final bool isLoading;
  final Widget? emptyState;
  
  const GHListTemplate({
    super.key,
    this.searchHint,
    this.filters,
    required this.children,
    this.onRefresh,
    this.onLoadMore,
    this.onSearch,
    this.isLoading = false,
    this.emptyState,
  });
  
  @override
  State<GHListTemplate> createState() => _GHListTemplateState();
}

class _GHListTemplateState extends State<GHListTemplate> {
  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }
  
  void _onScroll() {
    if (_scrollController.position.pixels >= 
        _scrollController.position.maxScrollExtent - 200) {
      widget.onLoadMore?.call();
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        if (widget.searchHint != null) ...[
          Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
            child: GHSearchBar(
              controller: _searchController,
              hintText: widget.searchHint!,
              onChanged: widget.onSearch,
            ),
          ),
        ],
        if (widget.filters != null) ...[
          SizedBox(
            height: 48,
            child: ListView(
              scrollDirection: Axis.horizontal,
              children: widget.filters!,
            ),
          ),
          const SizedBox(height: GHTokens.spacing8),
        ],
        Expanded(
          child: widget.children.isEmpty && !widget.isLoading
              ? widget.emptyState ?? const GHEmptyState(
                  icon: Icons.inbox_outlined,
                  title: 'No items found',
                  subtitle: 'Try adjusting your search or filters',
                )
              : RefreshIndicator(
                  onRefresh: widget.onRefresh ?? () async {},
                  child: ListView.separated(
                    controller: _scrollController,
                    itemCount: widget.children.length + (widget.isLoading ? 1 : 0),
                    separatorBuilder: (context, index) => 
                        const SizedBox(height: GHTokens.spacing8),
                    itemBuilder: (context, index) {
                      if (index >= widget.children.length) {
                        return const Center(
                          child: Padding(
                            padding: EdgeInsets.all(GHTokens.spacing16),
                            child: GHLoadingIndicator(),
                          ),
                        );
                      }
                      return widget.children[index];
                    },
                  ),
                ),
        ),
      ],
    );
  }
}
```

#### GHContentTemplate

Content layout with sections and metadata:

```dart
class GHContentTemplate extends StatelessWidget {
  final Widget? header;
  final List<Widget> sections;
  final List<Widget>? actions;
  final EdgeInsetsGeometry? padding;
  
  const GHContentTemplate({
    super.key,
    this.header,
    required this.sections,
    this.actions,
    this.padding,
  });
  
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: padding ?? const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (header != null) ...[
            header!,
            const SizedBox(height: GHTokens.spacing24),
          ],
          ...sections.map((section) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing24),
            child: section,
          )),
          if (actions != null) ...[
            const SizedBox(height: GHTokens.spacing16),
            Wrap(
              spacing: GHTokens.spacing8,
              runSpacing: GHTokens.spacing8,
              children: actions!,
            ),
          ],
        ],
      ),
    );
  }
}
```

### GitHub Content Widgets

#### GHRepositoryCard

Repository display card with complete metadata:

```dart
class GHRepositoryCard extends StatelessWidget {
  final String owner;
  final String name;
  final String? description;
  final String? language;
  final Color? languageColor;
  final int starCount;
  final int forkCount;
  final DateTime lastUpdated;
  final bool isPrivate;
  final VoidCallback? onTap;
  
  const GHRepositoryCard({
    super.key,
    required this.owner,
    required this.name,
    this.description,
    this.language,
    this.languageColor,
    required this.starCount,
    required this.forkCount,
    required this.lastUpdated,
    this.isPrivate = false,
    this.onTap,
  });
  
  // Factory constructor for GraphQL integration
  factory GHRepositoryCard.fromFragment(
    GRepositoryCardFragment fragment, {
    Key? key,
    VoidCallback? onTap,
  }) {
    return GHRepositoryCard(
      key: key,
      owner: fragment.owner.login,
      name: fragment.name,
      description: fragment.description,
      language: fragment.primaryLanguage?.name,
      languageColor: fragment.primaryLanguage?.color != null
          ? Color(int.parse(fragment.primaryLanguage!.color!.substring(1), radix: 16) + 0xFF000000)
          : null,
      starCount: fragment.stargazerCount,
      forkCount: fragment.forkCount,
      lastUpdated: DateTime.parse(fragment.updatedAt),
      isPrivate: fragment.isPrivate,
      onTap: onTap,
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return GHCard(
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Repository name and privacy indicator
          Row(
            children: [
              Expanded(
                child: Text(
                  '$owner/$name',
                  style: GHTokens.titleMedium.copyWith(
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              if (isPrivate)
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing4,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    border: Border.all(
                      color: Theme.of(context).colorScheme.outline,
                    ),
                    borderRadius: BorderRadius.circular(GHTokens.radius4),
                  ),
                  child: Text(
                    'Private',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ),
            ],
          ),
          
          // Description
          if (description != null) ...[
            const SizedBox(height: GHTokens.spacing4),
            Text(
              description!,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],
          
          const SizedBox(height: GHTokens.spacing12),
          
          // Metadata row
          Row(
            children: [
              // Language indicator
              if (language != null) ...[
                Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    color: languageColor ?? ColorUtils.getLanguageColor(language!),
                    shape: BoxShape.circle,
                  ),
                ),
                const SizedBox(width: GHTokens.spacing4),
                Text(
                  language!,
                  style: GHTokens.labelMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
                const SizedBox(width: GHTokens.spacing16),
              ],
              
              // Star count
              Icon(
                Icons.star_border,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              const SizedBox(width: GHTokens.spacing4),
              Text(
                NumberFormatter.formatCompact(starCount),
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              
              const SizedBox(width: GHTokens.spacing16),
              
              // Fork count
              Icon(
                Icons.fork_right,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              const SizedBox(width: GHTokens.spacing4),
              Text(
                NumberFormatter.formatCompact(forkCount),
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              
              const Spacer(),
              
              // Last updated
              Text(
                'Updated ${DateFormatter.formatRelative(lastUpdated)}',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
```

#### GHIssueCard

Issue/PR display card with status and metadata:

```dart
class GHIssueCard extends StatelessWidget {
  final int number;
  final String title;
  final GHStatus status;
  final List<String> labels;
  final String authorLogin;
  final String? authorAvatarUrl;
  final DateTime createdAt;
  final int commentCount;
  final String? assigneeLogin;
  final String? assigneeAvatarUrl;
  final VoidCallback? onTap;
  
  const GHIssueCard({
    super.key,
    required this.number,
    required this.title,
    required this.status,
    this.labels = const [],
    required this.authorLogin,
    this.authorAvatarUrl,
    required this.createdAt,
    this.commentCount = 0,
    this.assigneeLogin,
    this.assigneeAvatarUrl,
    this.onTap,
  });
  
  // Factory constructor for GraphQL integration
  factory GHIssueCard.fromFragment(
    GIssueCardFragment fragment, {
    Key? key,
    VoidCallback? onTap,
  }) {
    return GHIssueCard(
      key: key,
      number: fragment.number,
      title: fragment.title,
      status: _mapStatus(fragment.state),
      labels: fragment.labels.nodes.map((label) => label.name).toList(),
      authorLogin: fragment.author?.login ?? 'unknown',
      authorAvatarUrl: fragment.author?.avatarUrl,
      createdAt: DateTime.parse(fragment.createdAt),
      commentCount: fragment.comments.totalCount,
      assigneeLogin: fragment.assignees.nodes.isNotEmpty 
          ? fragment.assignees.nodes.first.login 
          : null,
      assigneeAvatarUrl: fragment.assignees.nodes.isNotEmpty 
          ? fragment.assignees.nodes.first.avatarUrl 
          : null,
      onTap: onTap,
    );
  }
  
  static GHStatus _mapStatus(String state) {
    switch (state.toLowerCase()) {
      case 'open':
        return GHStatus.open;
      case 'closed':
        return GHStatus.closed;
      case 'merged':
        return GHStatus.merged;
      default:
        return GHStatus.draft;
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return GHCard(
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Issue number and status
          Row(
            children: [
              GHStatusBadge(status: status),
              const SizedBox(width: GHTokens.spacing8),
              Text(
                '#$number',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const Spacer(),
              if (commentCount > 0) ...[
                Icon(
                  Icons.comment_outlined,
                  size: 16,
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                const SizedBox(width: GHTokens.spacing4),
                Text(
                  commentCount.toString(),
                  style: GHTokens.labelMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ],
          ),
          
          const SizedBox(height: GHTokens.spacing8),
          
          // Issue title
          Text(
            title,
            style: GHTokens.titleMedium,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          
          // Labels
          if (labels.isNotEmpty) ...[
            const SizedBox(height: GHTokens.spacing8),
            Wrap(
              spacing: GHTokens.spacing4,
              runSpacing: GHTokens.spacing4,
              children: labels.take(3).map((label) => GHChip(
                label: label,
                colorIndicator: ColorUtils.getLanguageColor(label),
              )).toList(),
            ),
          ],
          
          const SizedBox(height: GHTokens.spacing12),
          
          // Author and metadata
          Row(
            children: [
              // Author avatar
              if (authorAvatarUrl != null)
                CircleAvatar(
                  radius: 12,
                  backgroundImage: NetworkImage(authorAvatarUrl!),
                )
              else
                CircleAvatar(
                  radius: 12,
                  backgroundColor: Theme.of(context).colorScheme.surfaceVariant,
                  child: Icon(
                    Icons.person,
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              
              const SizedBox(width: GHTokens.spacing8),
              
              // Author and timestamp
              Expanded(
                child: Text(
                  '$authorLogin opened ${DateFormatter.formatRelative(createdAt)}',
                  style: GHTokens.labelMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              
              // Assignee avatar
              if (assigneeAvatarUrl != null) ...[
                const SizedBox(width: GHTokens.spacing8),
                CircleAvatar(
                  radius: 12,
                  backgroundImage: NetworkImage(assigneeAvatarUrl!),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}
```

#### GHUserCard

User profile card with statistics:

```dart
class GHUserCard extends StatelessWidget {
  final String login;
  final String? name;
  final String? bio;
  final String avatarUrl;
  final int repositoryCount;
  final int followerCount;
  final int followingCount;
  final VoidCallback? onTap;
  
  const GHUserCard({
    super.key,
    required this.login,
    this.name,
    this.bio,
    required this.avatarUrl,
    required this.repositoryCount,
    required this.followerCount,
    required this.followingCount,
    this.onTap,
  });
  
  // Factory constructor for GraphQL integration
  factory GHUserCard.fromFragment(
    GUserCardFragment fragment, {
    Key? key,
    VoidCallback? onTap,
  }) {
    return GHUserCard(
      key: key,
      login: fragment.login,
      name: fragment.name,
      bio: fragment.bio,
      avatarUrl: fragment.avatarUrl,
      repositoryCount: fragment.repositories.totalCount,
      followerCount: fragment.followers.totalCount,
      followingCount: fragment.following.totalCount,
      onTap: onTap,
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return GHCard(
      onTap: onTap,
      child: Row(
        children: [
          // Avatar
          CircleAvatar(
            radius: 24,
            backgroundImage: NetworkImage(avatarUrl),
          ),
          
          const SizedBox(width: GHTokens.spacing12),
          
          // User info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Name and username
                Text(
                  name ?? login,
                  style: GHTokens.titleMedium,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                if (name != null) ...[
                  const SizedBox(height: 2),
                  Text(
                    '@$login',
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
                
                // Bio
                if (bio != null) ...[
                  const SizedBox(height: GHTokens.spacing4),
                  Text(
                    bio!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
                
                const SizedBox(height: GHTokens.spacing8),
                
                // Statistics
                Row(
                  children: [
                    _buildStat(context, 'Repos', repositoryCount),
                    const SizedBox(width: GHTokens.spacing16),
                    _buildStat(context, 'Followers', followerCount),
                    const SizedBox(width: GHTokens.spacing16),
                    _buildStat(context, 'Following', followingCount),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
  
  Widget _buildStat(BuildContext context, String label, int count) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          NumberFormatter.formatCompact(count),
          style: GHTokens.labelLarge.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        Text(
          label,
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }
}
```

### Content Viewers

#### GHCodeViewer

Code viewer with syntax highlighting:

```dart
class GHCodeViewer extends StatelessWidget {
  final String content;
  final String? language;
  final bool showLineNumbers;
  final String? fileName;
  final String? fileSize;
  final VoidCallback? onCopy;
  
  const GHCodeViewer({
    super.key,
    required this.content,
    this.language,
    this.showLineNumbers = true,
    this.fileName,
    this.fileSize,
    this.onCopy,
  });
  
  @override
  Widget build(BuildContext context) {
    final lines = content.split('\n');
    
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // File header
        if (fileName != null || language != null || onCopy != null)
          Container(
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceVariant,
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(GHTokens.radius8),
                topRight: Radius.circular(GHTokens.radius8),
              ),
            ),
            child: Row(
              children: [
                if (fileName != null) ...[
                  Icon(
                    _getFileIcon(fileName!),
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                  Text(
                    fileName!,
                    style: GHTokens.labelMedium.copyWith(
                      fontFamily: 'monospace',
                    ),
                  ),
                ],
                
                if (language != null) ...[
                  if (fileName != null) const SizedBox(width: GHTokens.spacing8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: GHTokens.spacing4,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: ColorUtils.getLanguageColor(language!),
                      borderRadius: BorderRadius.circular(GHTokens.radius4),
                    ),
                    child: Text(
                      language!,
                      style: GHTokens.labelMedium.copyWith(
                        color: Colors.white,
                        fontSize: 10,
                      ),
                    ),
                  ),
                ],
                
                if (fileSize != null) ...[
                  const SizedBox(width: GHTokens.spacing8),
                  Text(
                    fileSize!,
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
                
                const Spacer(),
                
                if (onCopy != null)
                  IconButton(
                    onPressed: onCopy,
                    icon: const Icon(Icons.copy, size: 16),
                    iconSize: 16,
                    constraints: const BoxConstraints(
                      minWidth: 32,
                      minHeight: 32,
                    ),
                    padding: const EdgeInsets.all(GHTokens.spacing4),
                  ),
              ],
            ),
          ),
        
        // Code content
        Container(
          width: double.infinity,
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            border: Border.all(
              color: Theme.of(context).colorScheme.outline,
            ),
            borderRadius: fileName != null || language != null || onCopy != null
                ? const BorderRadius.only(
                    bottomLeft: Radius.circular(GHTokens.radius8),
                    bottomRight: Radius.circular(GHTokens.radius8),
                  )
                : BorderRadius.circular(GHTokens.radius8),
          ),
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: IntrinsicWidth(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: lines.asMap().entries.map((entry) {
                  final lineNumber = entry.key + 1;
                  final line = entry.value;
                  
                  return Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (showLineNumbers) ...[
                        Container(
                          width: 48,
                          padding: const EdgeInsets.symmetric(
                            horizontal: GHTokens.spacing8,
                            vertical: 2,
                          ),
                          color: Theme.of(context).colorScheme.surfaceVariant,
                          child: Text(
                            lineNumber.toString(),
                            style: GHTokens.labelMedium.copyWith(
                              fontFamily: 'monospace',
                              color: Theme.of(context).colorScheme.onSurfaceVariant,
                            ),
                            textAlign: TextAlign.right,
                          ),
                        ),
                      ],
                      Expanded(
                        child: Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: GHTokens.spacing12,
                            vertical: 2,
                          ),
                          child: Text(
                            line.isEmpty ? ' ' : line,
                            style: GHTokens.bodyMedium.copyWith(
                              fontFamily: 'monospace',
                              height: 1.4,
                            ),
                          ),
                        ),
                      ),
                    ],
                  );
                }).toList(),
              ),
            ),
          ),
        ),
      ],
    );
  }
  
  IconData _getFileIcon(String fileName) {
    final extension = fileName.split('.').last.toLowerCase();
    switch (extension) {
      case 'dart':
        return Icons.code;
      case 'js':
      case 'ts':
        return Icons.javascript;
      case 'py':
        return Icons.code;
      case 'md':
        return Icons.description;
      case 'json':
        return Icons.data_object;
      case 'yaml':
      case 'yml':
        return Icons.settings;
      default:
        return Icons.insert_drive_file;
    }
  }
}
```

#### GHMarkdownViewer

Markdown renderer with GitHub styling:

```dart
class GHMarkdownViewer extends StatelessWidget {
  final String content;
  final String? baseUrl;
  final Function(String)? onLinkTap;
  
  const GHMarkdownViewer({
    super.key,
    required this.content,
    this.baseUrl,
    this.onLinkTap,
  });
  
  @override
  Widget build(BuildContext context) {
    return MarkdownBody(
      data: content,
      styleSheet: MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
        h1: GHTokens.headlineLarge,
        h2: GHTokens.headlineMedium,
        h3: GHTokens.titleLarge,
        h4: GHTokens.titleMedium,
        h5: GHTokens.bodyLarge.copyWith(fontWeight: FontWeight.w600),
        h6: GHTokens.bodyMedium.copyWith(fontWeight: FontWeight.w600),
        p: GHTokens.bodyLarge,
        code: GHTokens.bodyMedium.copyWith(
          fontFamily: 'monospace',
          backgroundColor: Theme.of(context).colorScheme.surfaceVariant,
        ),
        codeblockDecoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(GHTokens.radius8),
        ),
        blockquote: GHTokens.bodyLarge.copyWith(
          color: Theme.of(context).colorScheme.onSurfaceVariant,
          fontStyle: FontStyle.italic,
        ),
        blockquoteDecoration: BoxDecoration(
          border: Border(
            left: BorderSide(
              color: Theme.of(context).colorScheme.primary,
              width: 4,
            ),
          ),
        ),
        listBullet: GHTokens.bodyLarge,
        tableHead: GHTokens.bodyLarge.copyWith(fontWeight: FontWeight.w600),
        tableBody: GHTokens.bodyLarge,
        tableBorder: TableBorder.all(
          color: Theme.of(context).colorScheme.outline,
        ),
        a: GHTokens.bodyLarge.copyWith(
          color: Theme.of(context).colorScheme.primary,
          decoration: TextDecoration.underline,
        ),
      ),
      onTapLink: (text, href, title) {
        if (href != null) {
          onLinkTap?.call(href);
        }
      },
      imageBuilder: (uri, title, alt) {
        return ClipRRect(
          borderRadius: BorderRadius.circular(GHTokens.radius8),
          child: Image.network(
            uri.toString(),
            errorBuilder: (context, error, stackTrace) {
              return Container(
                padding: const EdgeInsets.all(GHTokens.spacing16),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceVariant,
                  borderRadius: BorderRadius.circular(GHTokens.radius8),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.broken_image,
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: GHTokens.spacing8),
                    Text(
                      alt ?? 'Failed to load image',
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        );
      },
    );
  }
}
```

### State Widgets

#### GHEmptyState

Empty state display with action:

```dart
class GHEmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final String? actionLabel;
  final VoidCallback? onAction;
  
  const GHEmptyState({
    super.key,
    required this.icon,
    required this.title,
    required this.subtitle,
    this.actionLabel,
    this.onAction,
  });
  
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 64,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              title,
              style: GHTokens.headlineMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              subtitle,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            if (actionLabel != null && onAction != null) ...[
              const SizedBox(height: GHTokens.spacing24),
              GHButton(
                label: actionLabel!,
                onPressed: onAction,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## Data Models

### Comprehensive Fake Data System

The fake data system provides realistic GitHub data for all widgets:

```dart
// lib/src/ui-system/data/fake_data_service.dart
class FakeDataService {
  static final FakeDataService _instance = FakeDataService._internal();
  factory FakeDataService() => _instance;
  FakeDataService._internal();
  
  // Repository data
  List<FakeRepository> get repositories => FakeRepositories.all;
  List<FakeRepository> get trendingRepositories => FakeRepositories.trending;
  
  // User data
  List<FakeUser> get users => FakeUsers.all;
  List<FakeUser> get popularUsers => FakeUsers.popular;
  
  // Issue data
  List<FakeIssue> get issues => FakeIssues.all;
  List<FakeIssue> get openIssues => FakeIssues.open;
  List<FakeIssue> get closedIssues => FakeIssues.closed;
  
  // Code samples
  Map<String, String> get codeSamples => FakeCodeSamples.all;
  
  // Markdown content
  List<String> get markdownSamples => FakeMarkdownContent.all;
  
  // Search functionality
  List<FakeRepository> searchRepositories(String query) {
    if (query.isEmpty) return repositories;
    return repositories.where((repo) =>
      repo.name.toLowerCase().contains(query.toLowerCase()) ||
      repo.owner.toLowerCase().contains(query.toLowerCase()) ||
      (repo.description?.toLowerCase().contains(query.toLowerCase()) ?? false)
    ).toList();
  }
  
  List<FakeUser> searchUsers(String query) {
    if (query.isEmpty) return users;
    return users.where((user) =>
      user.login.toLowerCase().contains(query.toLowerCase()) ||
      (user.name?.toLowerCase().contains(query.toLowerCase()) ?? false) ||
      (user.bio?.toLowerCase().contains(query.toLowerCase()) ?? false)
    ).toList();
  }
  
  List<FakeIssue> searchIssues(String query) {
    if (query.isEmpty) return issues;
    return issues.where((issue) =>
      issue.title.toLowerCase().contains(query.toLowerCase()) ||
      issue.labels.any((label) => label.toLowerCase().contains(query.toLowerCase()))
    ).toList();
  }
}
```

### Fake Repository Data

```dart
// lib/src/ui-system/data/fake_repositories.dart
class FakeRepositories {
  static final List<FakeRepository> all = [
    FakeRepository(
      owner: 'facebook',
      name: 'react',
      description: 'A declarative, efficient, and flexible JavaScript library for building user interfaces.',
      language: 'JavaScript',
      starCount: 218000,
      forkCount: 45200,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 2)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'flutter',
      name: 'flutter',
      description: 'Flutter makes it easy and fast to build beautiful apps for mobile and beyond.',
      language: 'Dart',
      starCount: 162000,
      forkCount: 26700,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 5)),
      isPrivate: false,
    ),
    FakeRepository(
      owner: 'microsoft',
      name: 'vscode',
      description: 'Visual Studio Code',
      language: 'TypeScript',
      starCount: 158000,
      forkCount: 28100,
      lastUpdated: DateTime.now().subtract(const Duration(hours: 1)),
      isPrivate: false,
    ),
    // ... 47 more repositories with realistic data
  ];
  
  static List<FakeRepository> get trending => all.take(10).toList();
  
  static List<FakeRepository> filterByLanguage(String language) {
    return all.where((repo) => repo.language == language).toList();
  }
}
```

## Error Handling

### Widget Error Boundaries

All widgets include proper error handling:

```dart
class GHRepositoryCard extends StatelessWidget {
  // ... existing code
  
  @override
  Widget build(BuildContext context) {
    try {
      return _buildCard(context);
    } catch (e) {
      return GHCard(
        child: Column(
          children: [
            Icon(
              Icons.error_outline,
              color: Theme.of(context).colorScheme.error,
            ),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              'Error loading repository',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.error,
              ),
            ),
          ],
        ),
      );
    }
  }
}
```

### Data Loading Error States

The fake data service includes error simulation:

```dart
class FakeDataService {
  // ... existing code
  
  Future<List<FakeRepository>> loadRepositories({
    bool simulateError = false,
    Duration delay = const Duration(milliseconds: 500),
  }) async {
    await Future.delayed(delay);
    
    if (simulateError) {
      throw Exception('Failed to load repositories');
    }
    
    return repositories;
  }
}
```

## Testing Strategy

### Widget Testing

Each widget includes comprehensive tests:

```dart
// test/src/ui-system/widgets/gh_repository_card_test.dart
void main() {
  group('GHRepositoryCard', () {
    testWidgets('displays repository information correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: GHRepositoryCard(
              owner: 'facebook',
              name: 'react',
              description: 'A declarative library',
              language: 'JavaScript',
              starCount: 218000,
              forkCount: 45200,
              lastUpdated: DateTime.now(),
            ),
          ),
        ),
      );
      
      expect(find.text('facebook/react'), findsOneWidget);
      expect(find.text('A declarative library'), findsOneWidget);
      expect(find.text('JavaScript'), findsOneWidget);
      expect(find.text('218k'), findsOneWidget);
      expect(find.text('45.2k'), findsOneWidget);
    });
    
    testWidgets('handles tap events', (tester) async {
      bool tapped = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHRepositoryCard(
              owner: 'test',
              name: 'repo',
              starCount: 0,
              forkCount: 0,
              lastUpdated: DateTime.now(),
              onTap: () => tapped = true,
            ),
          ),
        ),
      );
      
      await tester.tap(find.byType(GHRepositoryCard));
      expect(tapped, isTrue);
    });
  });
}
```

### Integration Testing

Integration tests verify component interactions:

```dart
// test/integration/ui_widgets_integration_test.dart
void main() {
  group('UI Widgets Integration', () {
    testWidgets('search functionality works correctly', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHListTemplate(
              searchHint: 'Search repositories',
              children: FakeDataService().repositories
                  .map((repo) => GHRepositoryCard.fromFakeData(repo))
                  .toList(),
              onSearch: (query) {
                // Search implementation
              },
            ),
          ),
        ),
      );
      
      // Test search input
      await tester.enterText(find.byType(TextField), 'react');
      await tester.pump(const Duration(milliseconds: 300));
      
      // Verify search results
      expect(find.text('facebook/react'), findsOneWidget);
    });
  });
}
```

This comprehensive design provides a complete GitHub-specific widget system that enables rapid development of GitHub mobile screens with consistent styling, realistic data, and rich interactions. The system builds upon the foundation from Phase 1 and provides all the components needed for a complete GitHub mobile experience.