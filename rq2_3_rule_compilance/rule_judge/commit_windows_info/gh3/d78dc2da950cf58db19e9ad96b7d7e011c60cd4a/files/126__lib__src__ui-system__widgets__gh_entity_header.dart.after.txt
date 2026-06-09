import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import 'gh_status_badge.dart';
import '../utils/number_formatter.dart';
import '../utils/color_utils.dart';

/// A GitHub-styled entity header for repositories, users, and organizations.
///
/// This widget displays entity information including title, description,
/// statistics with icons, status indicators, and action buttons. It provides
/// a consistent header layout for different GitHub entity types.
class GHEntityHeader extends StatelessWidget {
  /// Entity title (repository name, user name, etc.)
  final String title;

  /// Entity subtitle or description
  final String? subtitle;

  /// Optional avatar or icon
  final Widget? avatar;

  /// List of statistics to display
  final List<GHEntityStat> stats;

  /// Optional status badge
  final GHStatusType? status;

  /// List of action buttons
  final List<Widget> actions;

  /// Whether to show the entity as private
  final bool isPrivate;

  /// Custom background color
  final Color? backgroundColor;

  /// Whether to show a divider at the bottom
  final bool showDivider;

  const GHEntityHeader({
    super.key,
    required this.title,
    this.subtitle,
    this.avatar,
    this.stats = const [],
    this.status,
    this.actions = const [],
    this.isPrivate = false,
    this.backgroundColor,
    this.showDivider = true,
  });

  Widget _buildPrivacyIndicator(BuildContext context) {
    if (!isPrivate) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing4,
        vertical: 2,
      ),
      decoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).colorScheme.outline),
        borderRadius: BorderRadius.circular(GHTokens.radius4),
      ),
      child: Text(
        'Private',
        style: GHTokens.labelMedium.copyWith(
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }

  Widget _buildStats(BuildContext context) {
    if (stats.isEmpty) return const SizedBox.shrink();

    return Wrap(
      spacing: GHTokens.spacing16,
      runSpacing: GHTokens.spacing8,
      children: stats.map((stat) => _buildStat(context, stat)).toList(),
    );
  }

  Widget _buildStat(BuildContext context, GHEntityStat stat) {
    final theme = Theme.of(context);

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (stat.icon != null) ...[
          Icon(
            stat.icon,
            size: GHTokens.iconSize16,
            color: theme.colorScheme.onSurfaceVariant,
          ),
          const SizedBox(width: GHTokens.spacing4),
        ],
        if (stat.colorIndicator != null) ...[
          Container(
            width: 12,
            height: 12,
            decoration: BoxDecoration(
              color: stat.colorIndicator,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: GHTokens.spacing4),
        ],
        if (stat.count != null) ...[
          Text(
            NumberFormatter.formatCompact(stat.count!),
            style: GHTokens.labelLarge.copyWith(
              fontWeight: FontWeight.w600,
              color: theme.colorScheme.onSurface,
            ),
          ),
          const SizedBox(width: GHTokens.spacing4),
        ],
        Text(
          stat.label,
          style: GHTokens.labelMedium.copyWith(
            color: theme.colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildActions() {
    if (actions.isEmpty) return const SizedBox.shrink();

    return Wrap(
      spacing: GHTokens.spacing8,
      runSpacing: GHTokens.spacing8,
      children: actions,
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: backgroundColor ?? theme.colorScheme.surface,
        border: showDivider
            ? Border(
                bottom: BorderSide(
                  color: theme.colorScheme.outline.withValues(alpha: 0.2),
                  width: 1,
                ),
              )
            : null,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Title row with avatar, title, status, and privacy
          Row(
            children: [
              if (avatar != null) ...[
                avatar!,
                const SizedBox(width: GHTokens.spacing12),
              ],
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            title,
                            style: GHTokens.headlineMedium.copyWith(
                              color: theme.colorScheme.onSurface,
                            ),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(width: GHTokens.spacing8),
                        if (status != null) ...[
                          GHStatusBadge(status: status!),
                          const SizedBox(width: GHTokens.spacing8),
                        ],
                        _buildPrivacyIndicator(context),
                      ],
                    ),
                    if (subtitle != null && subtitle!.isNotEmpty) ...[
                      const SizedBox(height: GHTokens.spacing4),
                      Text(
                        subtitle!,
                        style: GHTokens.bodyLarge.copyWith(
                          color: theme.colorScheme.onSurfaceVariant,
                        ),
                        maxLines: 3,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ],
                ),
              ),
            ],
          ),

          // Statistics
          if (stats.isNotEmpty) ...[
            const SizedBox(height: GHTokens.spacing16),
            _buildStats(context),
          ],

          // Actions
          if (actions.isNotEmpty) ...[
            const SizedBox(height: GHTokens.spacing16),
            _buildActions(),
          ],
        ],
      ),
    );
  }
}

/// A statistic item for the entity header
class GHEntityStat {
  /// The label for the statistic
  final String label;

  /// Optional count value
  final int? count;

  /// Optional icon
  final IconData? icon;

  /// Optional color indicator
  final Color? colorIndicator;

  const GHEntityStat({
    required this.label,
    this.count,
    this.icon,
    this.colorIndicator,
  });

  /// Create a stat with an icon and count
  factory GHEntityStat.withIcon({
    required String label,
    required IconData icon,
    int? count,
  }) {
    return GHEntityStat(label: label, icon: icon, count: count);
  }

  /// Create a stat with a color indicator (for languages)
  factory GHEntityStat.withColor({
    required String label,
    required Color color,
    int? count,
  }) {
    return GHEntityStat(label: label, colorIndicator: color, count: count);
  }

  /// Create a simple text stat
  factory GHEntityStat.text({required String label}) {
    return GHEntityStat(label: label);
  }
}

/// Predefined entity stats for common GitHub entities
class GHEntityStats {
  const GHEntityStats._();

  /// Repository statistics
  static List<GHEntityStat> repository({
    required int stars,
    required int forks,
    required int watchers,
    String? language,
    Color? languageColor,
  }) {
    return [
      GHEntityStat.withIcon(
        label: 'stars',
        icon: Icons.star_border,
        count: stars,
      ),
      GHEntityStat.withIcon(
        label: 'forks',
        icon: Icons.fork_right,
        count: forks,
      ),
      GHEntityStat.withIcon(
        label: 'watching',
        icon: Icons.visibility,
        count: watchers,
      ),
      if (language != null)
        GHEntityStat.withColor(
          label: language,
          color: languageColor ?? ColorUtils.getLanguageColor(language),
        ),
    ];
  }

  /// User statistics
  static List<GHEntityStat> user({
    required int repositories,
    required int followers,
    required int following,
  }) {
    return [
      GHEntityStat.withIcon(
        label: 'repositories',
        icon: Icons.folder,
        count: repositories,
      ),
      GHEntityStat.withIcon(
        label: 'followers',
        icon: Icons.people,
        count: followers,
      ),
      GHEntityStat.withIcon(
        label: 'following',
        icon: Icons.person_add,
        count: following,
      ),
    ];
  }

  /// Organization statistics
  static List<GHEntityStat> organization({
    required int repositories,
    required int members,
    required int teams,
  }) {
    return [
      GHEntityStat.withIcon(
        label: 'repositories',
        icon: Icons.folder,
        count: repositories,
      ),
      GHEntityStat.withIcon(
        label: 'members',
        icon: Icons.people,
        count: members,
      ),
      GHEntityStat.withIcon(label: 'teams', icon: Icons.group, count: teams),
    ];
  }
}
