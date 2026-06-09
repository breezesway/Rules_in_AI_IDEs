import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';

/// A GitHub-styled navigation grid for action grids and quick navigation.
///
/// This widget provides a grid layout (2x2, 2x3, etc.) with icons, titles,
/// descriptions, and count badges. It's commonly used for repository navigation,
/// user dashboard actions, and organization overviews.
class GHNavigationGrid extends StatelessWidget {
  /// List of navigation items to display
  final List<GHNavigationItem> items;

  /// Number of columns in the grid
  final int crossAxisCount;

  /// Spacing between grid items
  final double spacing;

  /// Aspect ratio of each grid item
  final double childAspectRatio;

  /// Custom padding around the grid
  final EdgeInsetsGeometry? padding;

  const GHNavigationGrid({
    super.key,
    required this.items,
    this.crossAxisCount = 2,
    this.spacing = 8.0,
    this.childAspectRatio = 1.2,
    this.padding,
  });

  /// Create a 2x2 navigation grid
  factory GHNavigationGrid.twoByTwo({
    Key? key,
    required List<GHNavigationItem> items,
    double spacing = 8.0,
    EdgeInsetsGeometry? padding,
  }) {
    return GHNavigationGrid(
      key: key,
      items: items.take(4).toList(),
      crossAxisCount: 2,
      spacing: spacing,
      childAspectRatio: 1.2,
      padding: padding,
    );
  }

  /// Create a 2x3 navigation grid
  factory GHNavigationGrid.twoByThree({
    Key? key,
    required List<GHNavigationItem> items,
    double spacing = 8.0,
    EdgeInsetsGeometry? padding,
  }) {
    return GHNavigationGrid(
      key: key,
      items: items.take(6).toList(),
      crossAxisCount: 2,
      spacing: spacing,
      childAspectRatio: 1.1,
      padding: padding,
    );
  }

  /// Create a 3x2 navigation grid
  factory GHNavigationGrid.threeByTwo({
    Key? key,
    required List<GHNavigationItem> items,
    double spacing = 8.0,
    EdgeInsetsGeometry? padding,
  }) {
    return GHNavigationGrid(
      key: key,
      items: items.take(6).toList(),
      crossAxisCount: 3,
      spacing: spacing,
      childAspectRatio: 0.9,
      padding: padding,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const SizedBox.shrink();
    }

    return Padding(
      padding: padding ?? EdgeInsets.zero,
      child: GridView.builder(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: crossAxisCount,
          crossAxisSpacing: spacing,
          mainAxisSpacing: spacing,
          childAspectRatio: childAspectRatio,
        ),
        itemCount: items.length,
        itemBuilder: (context, index) {
          return GHNavigationGridItem(item: items[index]);
        },
      ),
    );
  }
}

/// A single navigation grid item widget
class GHNavigationGridItem extends StatelessWidget {
  /// The navigation item to display
  final GHNavigationItem item;

  const GHNavigationGridItem({super.key, required this.item});

  Widget _buildBadge(BuildContext context) {
    if (item.badge == null) return const SizedBox.shrink();

    return Positioned(
      top: GHTokens.spacing8,
      right: GHTokens.spacing8,
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing4,
          vertical: 2,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.error,
          borderRadius: BorderRadius.circular(GHTokens.radius8),
        ),
        constraints: const BoxConstraints(minWidth: 16, minHeight: 16),
        child: Text(
          item.badge!,
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onError,
            fontSize: 10,
          ),
          textAlign: TextAlign.center,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return GHCard(
      onTap: item.onTap,
      padding: const EdgeInsets.all(GHTokens.spacing12),
      child: Stack(
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Icon
              Icon(
                item.icon,
                size: GHTokens.iconSize24,
                color: item.iconColor ?? theme.colorScheme.primary,
              ),

              const SizedBox(height: GHTokens.spacing8),

              // Title
              Text(
                item.title,
                style: GHTokens.titleMedium.copyWith(
                  color: theme.colorScheme.onSurface,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),

              // Description
              if (item.description != null) ...[
                const SizedBox(height: GHTokens.spacing4),
                Expanded(
                  child: Text(
                    item.description!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: theme.colorScheme.onSurfaceVariant,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],

              // Count
              if (item.count != null) ...[
                const SizedBox(height: GHTokens.spacing4),
                Text(
                  item.count!,
                  style: GHTokens.labelLarge.copyWith(
                    color: theme.colorScheme.primary,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ],
          ),

          // Badge
          _buildBadge(context),
        ],
      ),
    );
  }
}

/// A navigation item for the grid
class GHNavigationItem {
  /// The icon to display
  final IconData icon;

  /// The title text
  final String title;

  /// Optional description text
  final String? description;

  /// Optional count text
  final String? count;

  /// Optional badge text (for notifications, etc.)
  final String? badge;

  /// Custom icon color
  final Color? iconColor;

  /// Callback when the item is tapped
  final VoidCallback? onTap;

  const GHNavigationItem({
    required this.icon,
    required this.title,
    this.description,
    this.count,
    this.badge,
    this.iconColor,
    this.onTap,
  });

  /// Create a navigation item with a count
  factory GHNavigationItem.withCount({
    required IconData icon,
    required String title,
    String? description,
    required int count,
    String? badge,
    Color? iconColor,
    VoidCallback? onTap,
  }) {
    return GHNavigationItem(
      icon: icon,
      title: title,
      description: description,
      count: count.toString(),
      badge: badge,
      iconColor: iconColor,
      onTap: onTap,
    );
  }

  /// Create a navigation item with a formatted count
  factory GHNavigationItem.withFormattedCount({
    required IconData icon,
    required String title,
    String? description,
    required String formattedCount,
    String? badge,
    Color? iconColor,
    VoidCallback? onTap,
  }) {
    return GHNavigationItem(
      icon: icon,
      title: title,
      description: description,
      count: formattedCount,
      badge: badge,
      iconColor: iconColor,
      onTap: onTap,
    );
  }

  /// Create a simple navigation item without count
  factory GHNavigationItem.simple({
    required IconData icon,
    required String title,
    String? description,
    String? badge,
    Color? iconColor,
    VoidCallback? onTap,
  }) {
    return GHNavigationItem(
      icon: icon,
      title: title,
      description: description,
      badge: badge,
      iconColor: iconColor,
      onTap: onTap,
    );
  }
}

/// Predefined navigation items for common GitHub actions
class GHNavigationItems {
  const GHNavigationItems._();

  /// Repository navigation items
  static List<GHNavigationItem> repository({
    required int issues,
    required int pullRequests,
    required int actions,
    VoidCallback? onCodeTap,
    VoidCallback? onIssuesTap,
    VoidCallback? onPullRequestsTap,
    VoidCallback? onActionsTap,
  }) {
    return [
      GHNavigationItem.simple(
        icon: Icons.code,
        title: 'Code',
        description: 'Browse source files',
        onTap: onCodeTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.bug_report,
        title: 'Issues',
        description: 'Track bugs and features',
        count: issues,
        onTap: onIssuesTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.merge_type,
        title: 'Pull Requests',
        description: 'Review code changes',
        count: pullRequests,
        onTap: onPullRequestsTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.play_circle,
        title: 'Actions',
        description: 'CI/CD workflows',
        count: actions,
        onTap: onActionsTap,
      ),
    ];
  }

  /// User dashboard navigation items
  static List<GHNavigationItem> userDashboard({
    required int repositories,
    required int starred,
    required int organizations,
    VoidCallback? onRepositoriesTap,
    VoidCallback? onStarredTap,
    VoidCallback? onOrganizationsTap,
    VoidCallback? onSettingsTap,
  }) {
    return [
      GHNavigationItem.withCount(
        icon: Icons.folder,
        title: 'Repositories',
        description: 'Your repositories',
        count: repositories,
        onTap: onRepositoriesTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.star,
        title: 'Starred',
        description: 'Starred repositories',
        count: starred,
        onTap: onStarredTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.business,
        title: 'Organizations',
        description: 'Your organizations',
        count: organizations,
        onTap: onOrganizationsTap,
      ),
      GHNavigationItem.simple(
        icon: Icons.settings,
        title: 'Settings',
        description: 'Account settings',
        onTap: onSettingsTap,
      ),
    ];
  }

  /// Organization navigation items
  static List<GHNavigationItem> organization({
    required int repositories,
    required int members,
    required int teams,
    VoidCallback? onRepositoriesTap,
    VoidCallback? onMembersTap,
    VoidCallback? onTeamsTap,
    VoidCallback? onProjectsTap,
  }) {
    return [
      GHNavigationItem.withCount(
        icon: Icons.folder,
        title: 'Repositories',
        description: 'Organization repos',
        count: repositories,
        onTap: onRepositoriesTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.people,
        title: 'Members',
        description: 'Organization members',
        count: members,
        onTap: onMembersTap,
      ),
      GHNavigationItem.withCount(
        icon: Icons.group,
        title: 'Teams',
        description: 'Organization teams',
        count: teams,
        onTap: onTeamsTap,
      ),
      GHNavigationItem.simple(
        icon: Icons.dashboard,
        title: 'Projects',
        description: 'Organization projects',
        onTap: onProjectsTap,
      ),
    ];
  }
}
