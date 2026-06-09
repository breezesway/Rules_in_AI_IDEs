import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled screen template with consistent app bar and body structure.
///
/// This template provides a standard screen layout with app bar, body content,
/// and optional floating action button. It ensures consistent spacing, padding,
/// and styling across all GitHub screens.
class GHScreenTemplate extends StatelessWidget {
  /// The title to display in the app bar
  final String title;

  /// Optional action buttons to display in the app bar
  final List<Widget>? actions;

  /// The main body content of the screen
  final Widget body;

  /// Optional floating action button
  final FloatingActionButton? floatingActionButton;

  /// Whether to show the back button in the app bar
  final bool showBackButton;

  /// Optional bottom widget for the app bar (like TabBar)
  final PreferredSizeWidget? bottom;

  /// Custom app bar elevation
  final double? elevation;

  /// Whether to apply safe area padding to the body
  final bool applySafeArea;

  const GHScreenTemplate({
    super.key,
    required this.title,
    this.actions,
    required this.body,
    this.floatingActionButton,
    this.showBackButton = true,
    this.bottom,
    this.elevation,
    this.applySafeArea = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(
          title,
          style: GHTokens.titleLarge.copyWith(
            color: theme.colorScheme.onSurface,
          ),
        ),
        automaticallyImplyLeading: showBackButton,
        actions: actions,
        bottom: bottom,
        elevation: elevation ?? GHTokens.elevation0,
        surfaceTintColor: theme.colorScheme.surface,
        backgroundColor: theme.colorScheme.surface,
        foregroundColor: theme.colorScheme.onSurface,
        iconTheme: IconThemeData(
          color: theme.colorScheme.onSurface,
          size: GHTokens.iconSize24,
        ),
        actionsIconTheme: IconThemeData(
          color: theme.colorScheme.onSurface,
          size: GHTokens.iconSize24,
        ),
      ),
      body: applySafeArea
          ? SafeArea(
              child: Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: GHTokens.spacing16,
                ),
                child: body,
              ),
            )
          : Padding(
              padding: const EdgeInsets.symmetric(
                horizontal: GHTokens.spacing16,
              ),
              child: body,
            ),
      floatingActionButton: floatingActionButton,
      backgroundColor: theme.colorScheme.surface,
    );
  }
}
