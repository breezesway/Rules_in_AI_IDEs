import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled content template with organized sections and metadata.
///
/// This template provides a scrollable content layout with optional header,
/// multiple sections with proper spacing, and action buttons. It's ideal
/// for displaying detailed content like repository details, user profiles,
/// or issue descriptions.
class GHContentTemplate extends StatelessWidget {
  /// Optional header widget displayed at the top
  final Widget? header;

  /// List of section widgets with automatic spacing
  final List<Widget> sections;

  /// Optional action buttons displayed at the bottom
  final List<Widget>? actions;

  /// Custom padding around the content
  final EdgeInsetsGeometry? padding;

  /// Custom scroll controller
  final ScrollController? scrollController;

  /// Whether to show dividers between sections
  final bool showDividers;

  /// Custom divider widget
  final Widget? divider;

  /// Cross axis alignment for sections
  final CrossAxisAlignment crossAxisAlignment;

  /// Whether to apply physics to the scroll view
  final ScrollPhysics? physics;

  const GHContentTemplate({
    super.key,
    this.header,
    required this.sections,
    this.actions,
    this.padding,
    this.scrollController,
    this.showDividers = false,
    this.divider,
    this.crossAxisAlignment = CrossAxisAlignment.start,
    this.physics,
  });

  Widget _buildDivider(BuildContext context) {
    if (divider != null) {
      return divider!;
    }

    return Container(
      height: 1,
      margin: const EdgeInsets.symmetric(vertical: GHTokens.spacing12),
      color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
    );
  }

  List<Widget> _buildSectionsWithSpacing(BuildContext context) {
    if (sections.isEmpty) {
      return [];
    }

    final List<Widget> spacedSections = [];

    for (int i = 0; i < sections.length; i++) {
      spacedSections.add(sections[i]);

      // Add spacing or divider between sections (but not after the last one)
      if (i < sections.length - 1) {
        if (showDividers) {
          spacedSections.add(_buildDivider(context));
        } else {
          spacedSections.add(const SizedBox(height: GHTokens.spacing24));
        }
      }
    }

    return spacedSections;
  }

  Widget _buildActions() {
    if (actions == null || actions!.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      children: [
        const SizedBox(height: GHTokens.spacing16),
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          children: actions!,
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      controller: scrollController,
      physics: physics,
      padding: padding ?? const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: crossAxisAlignment,
        children: [
          // Header section
          if (header != null) ...[
            header!,
            const SizedBox(height: GHTokens.spacing24),
          ],

          // Main sections with spacing
          ..._buildSectionsWithSpacing(context),

          // Action buttons
          _buildActions(),
        ],
      ),
    );
  }
}

/// A helper widget for creating content sections with consistent styling.
///
/// This widget provides a standard way to create sections within the
/// GHContentTemplate with optional titles and consistent spacing.
class GHContentSection extends StatelessWidget {
  /// Optional section title
  final String? title;

  /// The main content of the section
  final Widget content;

  /// Optional subtitle or description
  final String? subtitle;

  /// Optional action widgets for the section header
  final List<Widget>? actions;

  /// Whether to show the section title
  final bool showTitle;

  const GHContentSection({
    super.key,
    this.title,
    required this.content,
    this.subtitle,
    this.actions,
    this.showTitle = true,
  });

  Widget _buildHeader(BuildContext context) {
    if (!showTitle ||
        (title == null &&
            subtitle == null &&
            (actions == null || actions!.isEmpty))) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (title != null || (actions != null && actions!.isNotEmpty))
          Row(
            children: [
              if (title != null)
                Expanded(
                  child: Text(
                    title!,
                    style: GHTokens.titleMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                  ),
                ),
              if (actions != null && actions!.isNotEmpty) ...[
                const SizedBox(width: GHTokens.spacing8),
                ...actions!,
              ],
            ],
          ),
        if (subtitle != null) ...[
          const SizedBox(height: GHTokens.spacing4),
          Text(
            subtitle!,
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
        const SizedBox(height: GHTokens.spacing12),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [_buildHeader(context), content],
    );
  }
}
