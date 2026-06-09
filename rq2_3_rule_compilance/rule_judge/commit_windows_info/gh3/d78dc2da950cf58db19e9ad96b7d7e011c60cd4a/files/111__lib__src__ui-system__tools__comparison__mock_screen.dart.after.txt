import 'package:flutter/material.dart';
import '../../tokens/gh_tokens.dart';

/// A mock screen widget used to demonstrate UI patterns in comparisons.
///
/// This widget simulates a basic app screen structure for showing
/// before/after states in the comparison framework.
class MockScreen extends StatelessWidget {
  /// Title displayed in the mock app bar
  final String title;

  /// Body content of the mock screen
  final Widget body;

  /// Optional actions for the mock app bar
  final List<Widget>? actions;

  /// Whether to show the back button
  final bool showBackButton;

  /// Background color of the mock screen
  final Color? backgroundColor;

  const MockScreen({
    super.key,
    required this.title,
    required this.body,
    this.actions,
    this.showBackButton = true,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: backgroundColor ?? Theme.of(context).colorScheme.surface,
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
        ),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          /// Mock app bar
          Container(
            height: 56,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              border: Border(
                bottom: BorderSide(
                  color: Theme.of(
                    context,
                  ).colorScheme.outline.withValues(alpha: 0.2),
                ),
              ),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(8),
                topRight: Radius.circular(8),
              ),
            ),
            child: Row(
              children: [
                if (showBackButton) ...[
                  const SizedBox(width: GHTokens.spacing4),
                  IconButton(
                    icon: const Icon(Icons.arrow_back),
                    onPressed: null,

                    /// Disabled for demo
                  ),
                ] else
                  const SizedBox(width: GHTokens.spacing16),

                Expanded(
                  child: title.isNotEmpty
                      ? Text(title, style: GHTokens.titleLarge)
                      : const SizedBox.shrink(),
                ),

                if (actions != null) ...actions!,
                const SizedBox(width: GHTokens.spacing16),
              ],
            ),
          ),

          /// Mock body
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(GHTokens.spacing16),
              child: body,
            ),
          ),
        ],
      ),
    );
  }
}

/// A mock tab widget for demonstrating old tab-based navigation.
class MockTab extends StatelessWidget {
  /// Label text for the tab
  final String label;

  /// Whether this tab is active/selected
  final bool isActive;

  /// Optional badge count to display
  final String? badge;

  const MockTab({
    super.key,
    required this.label,
    this.isActive = false,
    this.badge,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 48,
      decoration: BoxDecoration(
        color: isActive
            ? Theme.of(context).colorScheme.primaryContainer
            : Colors.transparent,
        border: Border(
          bottom: BorderSide(
            color: isActive
                ? Theme.of(context).colorScheme.primary
                : Colors.transparent,
            width: 2,
          ),
        ),
      ),
      child: Center(
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              label,
              style: GHTokens.labelLarge.copyWith(
                color: isActive
                    ? Theme.of(context).colorScheme.primary
                    : Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            if (badge != null) ...[
              const SizedBox(width: GHTokens.spacing4),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: GHTokens.spacing8,
                  vertical: GHTokens.spacing4,
                ),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  badge!,
                  style: GHTokens.labelSmall.copyWith(
                    color: Theme.of(context).colorScheme.onPrimary,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

/// A mock user card widget for demonstrations.
class MockUserCard extends StatelessWidget {
  /// Whether to show the title in the card (old way)
  final bool showTitle;

  /// The user's display name
  final String displayName;

  /// The user's username
  final String username;

  /// The user's bio/description
  final String bio;

  const MockUserCard({
    super.key,
    this.showTitle = false,
    this.displayName = 'The Octocat',
    this.username = '@octocat',
    this.bio = 'GitHub mascot and friendly neighborhood cat.',
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
        ),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (showTitle) ...[
            Text(displayName, style: GHTokens.headlineMedium),
            const SizedBox(height: GHTokens.spacing16),
          ],

          Row(
            children: [
              CircleAvatar(
                radius: 24,
                backgroundColor: Theme.of(context).colorScheme.primary,
                child: Text(
                  displayName[0],
                  style: GHTokens.titleMedium.copyWith(
                    color: Theme.of(context).colorScheme.onPrimary,
                  ),
                ),
              ),
              const SizedBox(width: GHTokens.spacing12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (!showTitle)
                      Text(displayName, style: GHTokens.titleLarge),
                    Text(
                      username,
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),

          const SizedBox(height: GHTokens.spacing12),

          Text(bio, style: GHTokens.bodyMedium),

          const SizedBox(height: GHTokens.spacing16),

          Row(
            children: [
              _buildStat(context, '1.2k', 'followers'),
              const SizedBox(width: GHTokens.spacing20),
              _buildStat(context, '234', 'following'),
              const SizedBox(width: GHTokens.spacing20),
              _buildStat(context, '45', 'repositories'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStat(BuildContext context, String count, String label) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(count, style: GHTokens.titleMedium),
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
