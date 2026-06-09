import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// GitHub status types for issues and pull requests
enum GHStatusType { open, closed, merged, draft }

/// Status badge sizes
enum GHStatusBadgeSize { small, medium, large }

/// Status badge widget for GitHub issues and pull requests
class GHStatusBadge extends StatelessWidget {
  /// The status to display
  final GHStatusType status;

  /// The size of the badge
  final GHStatusBadgeSize size;

  /// Optional custom label
  final String? customLabel;

  const GHStatusBadge({
    super.key,
    required this.status,
    this.size = GHStatusBadgeSize.medium,
    this.customLabel,
  });

  @override
  Widget build(BuildContext context) {
    final config = _getStatusConfig(context);
    final sizeConfig = _getSizeConfig();

    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: sizeConfig.horizontalPadding,
        vertical: sizeConfig.verticalPadding,
      ),
      decoration: BoxDecoration(
        color: config.backgroundColor,
        borderRadius: BorderRadius.circular(sizeConfig.borderRadius),
        border: Border.all(color: config.borderColor, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(config.icon, size: sizeConfig.iconSize, color: config.iconColor),
          SizedBox(width: sizeConfig.spacing),
          Text(
            customLabel ?? _getStatusLabel(),
            style: sizeConfig.textStyle.copyWith(
              color: config.textColor,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  _StatusConfig _getStatusConfig(BuildContext context) {
    switch (status) {
      case GHStatusType.open:
        return _StatusConfig(
          backgroundColor: Theme.of(context).colorScheme.primaryContainer,
          borderColor: Theme.of(context).colorScheme.primary,
          textColor: Theme.of(context).colorScheme.onPrimaryContainer,
          iconColor: Theme.of(context).colorScheme.primary,
          icon: Icons.radio_button_unchecked,
        );
      case GHStatusType.closed:
        return _StatusConfig(
          backgroundColor: Colors.purple.shade50,
          borderColor: Colors.purple,
          textColor: Colors.purple.shade800,
          iconColor: Colors.purple,
          icon: Icons.check_circle_outline,
        );
      case GHStatusType.merged:
        return _StatusConfig(
          backgroundColor: Colors.purple.shade50,
          borderColor: Colors.purple,
          textColor: Colors.purple.shade800,
          iconColor: Colors.purple,
          icon: Icons.merge_type,
        );
      case GHStatusType.draft:
        return _StatusConfig(
          backgroundColor: Colors.grey.shade100,
          borderColor: Colors.grey,
          textColor: Colors.grey.shade800,
          iconColor: Colors.grey,
          icon: Icons.edit_outlined,
        );
    }
  }

  _SizeConfig _getSizeConfig() {
    switch (size) {
      case GHStatusBadgeSize.small:
        return _SizeConfig(
          horizontalPadding: GHTokens.spacing8,
          verticalPadding: GHTokens.spacing4,
          borderRadius: GHTokens.radius12,
          iconSize: 12,
          spacing: GHTokens.spacing4,
          textStyle: GHTokens.labelSmall,
        );
      case GHStatusBadgeSize.medium:
        return _SizeConfig(
          horizontalPadding: GHTokens.spacing8,
          verticalPadding: GHTokens.spacing4,
          borderRadius: GHTokens.radius12,
          iconSize: 14,
          spacing: GHTokens.spacing8,
          textStyle: GHTokens.labelMedium,
        );
      case GHStatusBadgeSize.large:
        return _SizeConfig(
          horizontalPadding: GHTokens.spacing12,
          verticalPadding: GHTokens.spacing8,
          borderRadius: GHTokens.radius16,
          iconSize: 16,
          spacing: GHTokens.spacing8,
          textStyle: GHTokens.labelLarge,
        );
    }
  }

  String _getStatusLabel() {
    switch (status) {
      case GHStatusType.open:
        return 'Open';
      case GHStatusType.closed:
        return 'Closed';
      case GHStatusType.merged:
        return 'Merged';
      case GHStatusType.draft:
        return 'Draft';
    }
  }
}

class _StatusConfig {
  final Color backgroundColor;
  final Color borderColor;
  final Color textColor;
  final Color iconColor;
  final IconData icon;

  const _StatusConfig({
    required this.backgroundColor,
    required this.borderColor,
    required this.textColor,
    required this.iconColor,
    required this.icon,
  });
}

class _SizeConfig {
  final double horizontalPadding;
  final double verticalPadding;
  final double borderRadius;
  final double iconSize;
  final double spacing;
  final TextStyle textStyle;

  const _SizeConfig({
    required this.horizontalPadding,
    required this.verticalPadding,
    required this.borderRadius,
    required this.iconSize,
    required this.spacing,
    required this.textStyle,
  });
}
