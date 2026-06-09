import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled list tile component with enhanced styling.
///
/// This component provides a Material Design list tile with GitHub-specific
/// styling, proper spacing, and consistent visual hierarchy.
class GHListTile extends StatelessWidget {
  /// The primary content of the list item
  final Widget? title;

  /// Optional secondary content displayed below the title
  final Widget? subtitle;

  /// A widget to display before the title
  final Widget? leading;

  /// A widget to display after the title
  final Widget? trailing;

  /// Callback when the list tile is tapped
  final VoidCallback? onTap;

  /// Whether this list tile is intended to display three lines of text
  final bool isThreeLine;

  /// Whether this list tile is part of a vertically dense list
  final bool dense;

  /// Custom content padding
  final EdgeInsetsGeometry? contentPadding;

  const GHListTile({
    super.key,
    this.title,
    this.subtitle,
    this.leading,
    this.trailing,
    this.onTap,
    this.isThreeLine = false,
    this.dense = false,
    this.contentPadding,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ListTile(
      title: title,
      subtitle: subtitle,
      leading: leading,
      trailing: trailing,
      onTap: onTap,
      isThreeLine: isThreeLine,
      dense: dense,
      contentPadding:
          contentPadding ??
          const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing16,
            vertical: GHTokens.spacing8,
          ),
      titleTextStyle: GHTokens.bodyLarge.copyWith(
        color: theme.colorScheme.onSurface,
      ),
      subtitleTextStyle: GHTokens.bodyMedium.copyWith(
        color: theme.colorScheme.onSurfaceVariant,
      ),
      iconColor: theme.colorScheme.onSurfaceVariant,
      minVerticalPadding: GHTokens.spacing8,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
    );
  }
}
