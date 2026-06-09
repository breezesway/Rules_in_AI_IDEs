import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A metadata item representing a key-value pair with optional icon and action.
class GHMetadataItem {
  /// Optional icon for the metadata item
  final IconData? icon;

  /// The label/key for the metadata
  final String label;

  /// The value of the metadata
  final String value;

  /// Optional callback when the item is tapped
  final VoidCallback? onTap;

  /// Whether the value should be styled as a link
  final bool isLink;

  const GHMetadataItem({
    this.icon,
    required this.label,
    required this.value,
    this.onTap,
    this.isLink = false,
  });
}

/// A widget for displaying metadata as a formatted list of key-value pairs.
///
/// This widget provides consistent styling for metadata display across the
/// application, including proper spacing, typography, and interaction handling.
class GHContentMetadata extends StatelessWidget {
  /// List of metadata items to display
  final List<GHMetadataItem> items;

  /// Title for the metadata section
  final String? title;

  /// Whether to show dividers between items
  final bool showDividers;

  /// Custom spacing between items
  final double? itemSpacing;

  /// Cross axis alignment for items
  final CrossAxisAlignment crossAxisAlignment;

  /// Custom padding around the metadata container
  final EdgeInsetsGeometry? padding;

  const GHContentMetadata({
    super.key,
    required this.items,
    this.title,
    this.showDividers = false,
    this.itemSpacing,
    this.crossAxisAlignment = CrossAxisAlignment.start,
    this.padding,
  });

  Widget _buildTitle(BuildContext context) {
    if (title == null) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: crossAxisAlignment,
      children: [
        Text(
          title!,
          style: GHTokens.titleMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurface,
          ),
        ),
        const SizedBox(height: GHTokens.spacing12),
      ],
    );
  }

  Widget _buildDivider(BuildContext context) {
    return Container(
      height: 1,
      color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.1),
    );
  }

  Widget _buildMetadataItem(BuildContext context, GHMetadataItem item) {
    final hasAction = item.onTap != null;
    final valueColor = hasAction || item.isLink
        ? Theme.of(context).colorScheme.primary
        : Theme.of(context).colorScheme.onSurface;

    return InkWell(
      onTap: item.onTap,
      borderRadius: BorderRadius.circular(GHTokens.radius4),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 2),
        child: Row(
          children: [
            if (item.icon != null) ...[
              Icon(
                item.icon!,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              const SizedBox(width: GHTokens.spacing8),
            ],
            Text(
              item.label,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: Text(
                item.value,
                style: GHTokens.bodyMedium.copyWith(
                  color: valueColor,
                  decoration: item.isLink ? TextDecoration.underline : null,
                ),
              ),
            ),
            if (hasAction)
              Icon(
                Icons.open_in_new,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildItems(BuildContext context) {
    if (items.isEmpty) {
      return [];
    }

    final List<Widget> widgets = [];
    final spacing = itemSpacing ?? GHTokens.spacing8;

    for (int i = 0; i < items.length; i++) {
      widgets.add(_buildMetadataItem(context, items[i]));

      // Add spacing or divider between items (but not after the last one)
      if (i < items.length - 1) {
        if (showDividers) {
          widgets.add(SizedBox(height: spacing));
          widgets.add(_buildDivider(context));
          widgets.add(SizedBox(height: spacing));
        } else {
          widgets.add(SizedBox(height: spacing));
        }
      }
    }

    return widgets;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: padding ?? EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: crossAxisAlignment,
        children: [_buildTitle(context), ..._buildItems(context)],
      ),
    );
  }
}

/// A simplified metadata widget for displaying metadata as chips.
///
/// This widget displays metadata items as compact chips with icons and text,
/// useful for showing tags, categories, or other categorical metadata.
class GHMetadataChips extends StatelessWidget {
  /// List of metadata items to display as chips
  final List<GHMetadataItem> items;

  /// Title for the metadata section
  final String? title;

  /// Spacing between chips
  final double spacing;

  /// Run spacing for wrapped chips
  final double runSpacing;

  /// Cross axis alignment for the container
  final CrossAxisAlignment crossAxisAlignment;

  /// Custom padding around the chips container
  final EdgeInsetsGeometry? padding;

  const GHMetadataChips({
    super.key,
    required this.items,
    this.title,
    this.spacing = GHTokens.spacing8,
    this.runSpacing = GHTokens.spacing4,
    this.crossAxisAlignment = CrossAxisAlignment.start,
    this.padding,
  });

  Widget _buildTitle(BuildContext context) {
    if (title == null) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: crossAxisAlignment,
      children: [
        Text(
          title!,
          style: GHTokens.labelLarge.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
      ],
    );
  }

  Widget _buildChip(BuildContext context, GHMetadataItem item) {
    return InkWell(
      onTap: item.onTap,
      borderRadius: BorderRadius.circular(GHTokens.radius16),
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing8,
          vertical: GHTokens.spacing4,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(GHTokens.radius16),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (item.icon != null) ...[
              Icon(
                item.icon!,
                size: 14,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              const SizedBox(width: GHTokens.spacing4),
            ],
            Text(
              item.value,
              style: GHTokens.labelSmall.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (items.isEmpty) {
      return const SizedBox.shrink();
    }

    return Padding(
      padding: padding ?? EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: crossAxisAlignment,
        children: [
          _buildTitle(context),
          Wrap(
            spacing: spacing,
            runSpacing: runSpacing,
            children: items.map((item) => _buildChip(context, item)).toList(),
          ),
        ],
      ),
    );
  }
}
