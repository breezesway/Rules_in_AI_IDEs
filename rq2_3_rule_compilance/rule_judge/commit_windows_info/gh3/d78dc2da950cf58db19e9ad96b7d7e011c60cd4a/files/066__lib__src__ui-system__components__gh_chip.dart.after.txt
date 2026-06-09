import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// Chip size options
enum GHChipSize { small, medium, large }

/// A GitHub-styled chip component with selection states and count badges.
///
/// This component provides filter chips with GitHub-specific styling,
/// selection states, count badges, and color indicators.
class GHChip extends StatelessWidget {
  /// The text label to display on the chip
  final String label;

  /// Whether the chip is currently selected
  final bool isSelected;

  /// Callback when the chip is tapped
  final VoidCallback? onTap;

  /// Optional count to display as a badge
  final int? count;

  /// Optional color indicator dot
  final Color? colorIndicator;

  /// Whether the chip can be selected/deselected
  final bool isSelectable;

  /// Size of the chip
  final GHChipSize size;

  /// Custom background color
  final Color? backgroundColor;

  /// Custom text color
  final Color? textColor;

  const GHChip({
    super.key,
    required this.label,
    this.isSelected = false,
    this.onTap,
    this.count,
    this.colorIndicator,
    this.isSelectable = true,
    this.size = GHChipSize.medium,
    this.backgroundColor,
    this.textColor,
  });

  EdgeInsetsGeometry _getPadding() {
    switch (size) {
      case GHChipSize.small:
        return const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing4,
          vertical: 2,
        );
      case GHChipSize.medium:
        return const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing8,
          vertical: GHTokens.spacing4,
        );
      case GHChipSize.large:
        return const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing12,
          vertical: GHTokens.spacing8,
        );
    }
  }

  TextStyle _getTextStyle() {
    switch (size) {
      case GHChipSize.small:
        return GHTokens.labelMedium.copyWith(fontSize: 10);
      case GHChipSize.medium:
        return GHTokens.labelMedium;
      case GHChipSize.large:
        return GHTokens.labelLarge;
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final chipTextStyle = _getTextStyle().copyWith(
      color:
          textColor ??
          (isSelected
              ? theme.colorScheme.onPrimary
              : theme.colorScheme.onSurface),
    );

    if (isSelectable) {
      return FilterChip(
        label: _buildChipContent(theme, chipTextStyle),
        selected: isSelected,
        onSelected: onTap != null ? (_) => onTap!() : null,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(GHTokens.radius16),
        ),
        labelStyle: chipTextStyle,
        padding: _getPadding(),
        materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
        backgroundColor: backgroundColor,
        selectedColor: backgroundColor ?? theme.colorScheme.primary,
      );
    } else {
      return Container(
        padding: _getPadding(),
        decoration: BoxDecoration(
          color: backgroundColor ?? theme.colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(GHTokens.radius16),
        ),
        child: _buildChipContent(theme, chipTextStyle),
      );
    }
  }

  Widget _buildChipContent(ThemeData theme, TextStyle textStyle) {
    final indicatorSize = size == GHChipSize.small ? 8.0 : 12.0;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (colorIndicator != null) ...[
          Container(
            width: indicatorSize,
            height: indicatorSize,
            decoration: BoxDecoration(
              color: colorIndicator,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: GHTokens.spacing4),
        ],
        Text(label, style: textStyle),
        if (count != null) ...[
          const SizedBox(width: GHTokens.spacing4),
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: GHTokens.spacing4,
              vertical: 2,
            ),
            decoration: BoxDecoration(
              color: theme.colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Text(
              count.toString(),
              style: GHTokens.labelMedium.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ),
          ),
        ],
      ],
    );
  }
}
