import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// Button style variants for GitHub components
enum GHButtonStyle {
  /// Primary button with filled background
  primary,

  /// Secondary button with outlined style
  secondary,
}

/// A GitHub-styled button component with loading states and consistent styling.
///
/// This component provides primary and secondary button variants with
/// loading states, proper touch targets, and GitHub-specific styling.
class GHButton extends StatelessWidget {
  /// The text label to display on the button
  final String label;

  /// Callback when the button is pressed
  final VoidCallback? onPressed;

  /// The visual style of the button
  final GHButtonStyle style;

  /// Whether the button is in a loading state
  final bool isLoading;

  /// Optional icon to display alongside the label
  final IconData? icon;

  /// Custom width for the button
  final double? width;

  const GHButton({
    super.key,
    required this.label,
    this.onPressed,
    this.style = GHButtonStyle.primary,
    this.isLoading = false,
    this.icon,
    this.width,
  });

  @override
  Widget build(BuildContext context) {
    final buttonChild = _buildButtonContent();

    if (style == GHButtonStyle.primary) {
      return SizedBox(
        width: width,
        child: ElevatedButton(
          onPressed: isLoading ? null : onPressed,
          style: ElevatedButton.styleFrom(
            minimumSize: const Size(88, GHTokens.minTouchTarget),
            padding: const EdgeInsets.symmetric(
              horizontal: GHTokens.spacing16,
              vertical: GHTokens.spacing12,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            textStyle: GHTokens.labelLarge,
          ),
          child: buttonChild,
        ),
      );
    } else {
      return SizedBox(
        width: width,
        child: OutlinedButton(
          onPressed: isLoading ? null : onPressed,
          style: OutlinedButton.styleFrom(
            minimumSize: const Size(88, GHTokens.minTouchTarget),
            padding: const EdgeInsets.symmetric(
              horizontal: GHTokens.spacing16,
              vertical: GHTokens.spacing12,
            ),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            textStyle: GHTokens.labelLarge,
          ),
          child: buttonChild,
        ),
      );
    }
  }

  Widget _buildButtonContent() {
    if (isLoading) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(
            width: GHTokens.iconSize16,
            height: GHTokens.iconSize16,
            child: CircularProgressIndicator(strokeWidth: 2),
          ),
          const SizedBox(width: GHTokens.spacing8),
          Text(label, style: GHTokens.labelLarge),
        ],
      );
    }

    if (icon != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: GHTokens.iconSize18),
          const SizedBox(width: GHTokens.spacing8),
          Text(label, style: GHTokens.labelLarge),
        ],
      );
    }

    return Text(label, style: GHTokens.labelLarge);
  }
}
