import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled empty state widget with icon, title, and optional action.
///
/// This widget provides a consistent way to display empty states across
/// the application with proper spacing, typography, and optional action buttons.
class GHEmptyState extends StatelessWidget {
  /// The icon to display at the top of the empty state
  final IconData icon;

  /// The main title text
  final String title;

  /// Optional subtitle or description text
  final String? subtitle;

  /// Optional action button
  final Widget? action;

  /// Custom icon size (defaults to 64x64dp)
  final double? iconSize;

  /// Custom icon color
  final Color? iconColor;

  /// Custom title style
  final TextStyle? titleStyle;

  /// Custom subtitle style
  final TextStyle? subtitleStyle;

  /// Whether to center the content
  final bool centered;

  /// Custom padding around the content
  final EdgeInsetsGeometry? padding;

  const GHEmptyState({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    this.action,
    this.iconSize,
    this.iconColor,
    this.titleStyle,
    this.subtitleStyle,
    this.centered = true,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final content = Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Icon
        Icon(
          icon,
          size: iconSize ?? 64.0,
          color:
              iconColor ??
              theme.colorScheme.onSurfaceVariant.withValues(alpha: 0.6),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Title
        Text(
          title,
          style:
              titleStyle ??
              GHTokens.headlineMedium.copyWith(
                color: theme.colorScheme.onSurface,
              ),
          textAlign: TextAlign.center,
        ),

        // Subtitle
        if (subtitle != null) ...[
          const SizedBox(height: GHTokens.spacing8),
          Text(
            subtitle!,
            style:
                subtitleStyle ??
                GHTokens.bodyMedium.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
            textAlign: TextAlign.center,
          ),
        ],

        // Action button
        if (action != null) ...[
          const SizedBox(height: GHTokens.spacing24),
          action!,
        ],
      ],
    );

    if (centered) {
      return Padding(
        padding: padding ?? const EdgeInsets.all(GHTokens.spacing24),
        child: Center(child: content),
      );
    }

    return Padding(
      padding: padding ?? const EdgeInsets.all(GHTokens.spacing24),
      child: content,
    );
  }
}

/// Predefined empty state configurations for common scenarios.
class GHEmptyStates {
  const GHEmptyStates._();

  /// Empty state for no repositories
  static GHEmptyState noRepositories({VoidCallback? onCreateRepository}) {
    return GHEmptyState(
      icon: Icons.folder_outlined,
      title: 'No repositories',
      subtitle: 'Create your first repository to get started',
      action: onCreateRepository != null
          ? ElevatedButton.icon(
              onPressed: onCreateRepository,
              icon: const Icon(Icons.add),
              label: const Text('Create repository'),
            )
          : null,
    );
  }

  /// Empty state for no issues
  static GHEmptyState noIssues({VoidCallback? onCreateIssue}) {
    return GHEmptyState(
      icon: Icons.bug_report_outlined,
      title: 'No issues',
      subtitle: 'Issues help you track bugs and feature requests',
      action: onCreateIssue != null
          ? ElevatedButton.icon(
              onPressed: onCreateIssue,
              icon: const Icon(Icons.add),
              label: const Text('Create issue'),
            )
          : null,
    );
  }

  /// Empty state for no pull requests
  static GHEmptyState noPullRequests({VoidCallback? onCreatePR}) {
    return GHEmptyState(
      icon: Icons.merge_type_outlined,
      title: 'No pull requests',
      subtitle: 'Pull requests help you collaborate on code changes',
      action: onCreatePR != null
          ? ElevatedButton.icon(
              onPressed: onCreatePR,
              icon: const Icon(Icons.add),
              label: const Text('Create pull request'),
            )
          : null,
    );
  }

  /// Empty state for no search results
  static GHEmptyState noSearchResults({
    String? query,
    VoidCallback? onClearSearch,
  }) {
    return GHEmptyState(
      icon: Icons.search_off_outlined,
      title: 'No results found',
      subtitle: query != null
          ? 'No results found for "$query"'
          : 'Try adjusting your search terms',
      action: onClearSearch != null
          ? TextButton(
              onPressed: onClearSearch,
              child: const Text('Clear search'),
            )
          : null,
    );
  }

  /// Empty state for no starred repositories
  static GHEmptyState noStarredRepos({VoidCallback? onExplore}) {
    return GHEmptyState(
      icon: Icons.star_border_outlined,
      title: 'No starred repositories',
      subtitle:
          'Star repositories to keep track of projects you find interesting',
      action: onExplore != null
          ? ElevatedButton(
              onPressed: onExplore,
              child: const Text('Explore repositories'),
            )
          : null,
    );
  }

  /// Empty state for no followers
  static GHEmptyState noFollowers() {
    return const GHEmptyState(
      icon: Icons.people_outline,
      title: 'No followers yet',
      subtitle: 'When people follow you, they\'ll appear here',
    );
  }

  /// Empty state for no following
  static GHEmptyState noFollowing({VoidCallback? onExplore}) {
    return GHEmptyState(
      icon: Icons.person_add_outlined,
      title: 'Not following anyone',
      subtitle: 'Follow people to see their activity in your dashboard',
      action: onExplore != null
          ? ElevatedButton(
              onPressed: onExplore,
              child: const Text('Explore people'),
            )
          : null,
    );
  }

  /// Empty state for no activity feed
  static GHEmptyState noActivity({VoidCallback? onExplore}) {
    return GHEmptyState(
      icon: Icons.timeline_outlined,
      title: 'Your activity will appear here',
      subtitle:
          'When you star repositories, follow people, or contribute to projects, your activity will show up here',
      action: onExplore != null
          ? ElevatedButton(
              onPressed: onExplore,
              child: const Text('Explore GitHub'),
            )
          : null,
    );
  }

  /// Empty state for no notifications
  static GHEmptyState noNotifications() {
    return const GHEmptyState(
      icon: Icons.notifications_none_outlined,
      title: 'No notifications',
      subtitle: 'When you have notifications, they\'ll appear here',
    );
  }

  /// Generic empty state for lists
  static GHEmptyState emptyList({
    required String title,
    String? subtitle,
    IconData icon = Icons.inbox_outlined,
    Widget? action,
  }) {
    return GHEmptyState(
      icon: icon,
      title: title,
      subtitle: subtitle,
      action: action,
    );
  }
}
