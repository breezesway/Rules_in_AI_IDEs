import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled loading indicator with consistent theming.
///
/// This widget provides a loading spinner with GitHub-specific styling
/// and consistent sizing across the application.
class GHLoadingIndicator extends StatelessWidget {
  /// The size of the loading indicator
  final double? size;

  /// Custom color for the loading indicator
  final Color? color;

  /// Stroke width of the circular progress indicator
  final double? strokeWidth;

  /// Optional label text to display below the indicator
  final String? label;

  /// Whether to show the indicator inline or centered
  final bool centered;

  /// Custom padding around the indicator
  final EdgeInsetsGeometry? padding;

  const GHLoadingIndicator({
    super.key,
    this.size,
    this.color,
    this.strokeWidth,
    this.label,
    this.centered = false,
    this.padding,
  });

  /// Small loading indicator (16x16dp)
  const GHLoadingIndicator.small({
    super.key,
    this.color,
    this.strokeWidth,
    this.label,
    this.centered = false,
    this.padding,
  }) : size = 16.0;

  /// Medium loading indicator (24x24dp) - default
  const GHLoadingIndicator.medium({
    super.key,
    this.color,
    this.strokeWidth,
    this.label,
    this.centered = false,
    this.padding,
  }) : size = 24.0;

  /// Large loading indicator (32x32dp)
  const GHLoadingIndicator.large({
    super.key,
    this.color,
    this.strokeWidth,
    this.label,
    this.centered = false,
    this.padding,
  }) : size = 32.0;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final indicatorSize = size ?? 24.0;
    final indicatorColor = color ?? theme.colorScheme.primary;

    final indicator = Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: indicatorSize,
          height: indicatorSize,
          child: CircularProgressIndicator(
            color: indicatorColor,
            strokeWidth: strokeWidth ?? 2.0,
          ),
        ),
        if (label != null) ...[
          const SizedBox(height: GHTokens.spacing8),
          Text(
            label!,
            style: GHTokens.labelMedium.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ],
    );

    Widget content = indicator;

    if (padding != null) {
      content = Padding(padding: padding!, child: content);
    }

    if (centered) {
      return Center(child: content);
    }

    return content;
  }
}

/// A loading overlay that can be displayed over content.
///
/// This widget provides a semi-transparent overlay with a loading indicator
/// that can be shown over existing content during loading states.
class GHLoadingOverlay extends StatelessWidget {
  /// Whether to show the loading overlay
  final bool isLoading;

  /// The child widget to display behind the overlay
  final Widget child;

  /// Optional loading message
  final String? message;

  /// Custom background color for the overlay
  final Color? backgroundColor;

  /// Custom loading indicator
  final Widget? loadingIndicator;

  const GHLoadingOverlay({
    super.key,
    required this.isLoading,
    required this.child,
    this.message,
    this.backgroundColor,
    this.loadingIndicator,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        if (isLoading)
          Positioned.fill(
            child: AnimatedOpacity(
              duration: const Duration(milliseconds: 200),
              opacity: 1.0,
              child: Container(
                color:
                    backgroundColor ??
                    Theme.of(
                      context,
                    ).colorScheme.surface.withValues(alpha: 0.8),
                child: Center(
                  child:
                      loadingIndicator ??
                      GHLoadingIndicator.large(label: message, centered: true),
                ),
              ),
            ),
          ),
      ],
    );
  }
}

/// A loading button that shows a loading indicator when pressed.
///
/// This widget provides a button that automatically shows a loading state
/// when an async operation is in progress.
class GHLoadingButton extends StatefulWidget {
  /// The button text
  final String text;

  /// The async callback to execute when pressed
  final Future<void> Function()? onPressed;

  /// Optional icon to display
  final IconData? icon;

  /// Button style (elevated, outlined, text)
  final GHLoadingButtonStyle style;

  /// Whether the button is enabled
  final bool enabled;

  const GHLoadingButton({
    super.key,
    required this.text,
    this.onPressed,
    this.icon,
    this.style = GHLoadingButtonStyle.elevated,
    this.enabled = true,
  });

  @override
  State<GHLoadingButton> createState() => _GHLoadingButtonState();
}

class _GHLoadingButtonState extends State<GHLoadingButton> {
  bool _isLoading = false;

  Future<void> _handlePressed() async {
    if (_isLoading || widget.onPressed == null) return;

    setState(() {
      _isLoading = true;
    });

    try {
      await widget.onPressed!();
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  Widget _buildButtonContent() {
    if (_isLoading) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const GHLoadingIndicator.small(color: Colors.white),
          const SizedBox(width: GHTokens.spacing8),
          Text(widget.text),
        ],
      );
    }

    if (widget.icon != null) {
      return Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(widget.icon),
          const SizedBox(width: GHTokens.spacing8),
          Text(widget.text),
        ],
      );
    }

    return Text(widget.text);
  }

  @override
  Widget build(BuildContext context) {
    final isEnabled = widget.enabled && !_isLoading;

    switch (widget.style) {
      case GHLoadingButtonStyle.elevated:
        return ElevatedButton(
          onPressed: isEnabled ? _handlePressed : null,
          child: _buildButtonContent(),
        );
      case GHLoadingButtonStyle.outlined:
        return OutlinedButton(
          onPressed: isEnabled ? _handlePressed : null,
          child: _buildButtonContent(),
        );
      case GHLoadingButtonStyle.text:
        return TextButton(
          onPressed: isEnabled ? _handlePressed : null,
          child: _buildButtonContent(),
        );
    }
  }
}

/// Button styles for GHLoadingButton
enum GHLoadingButtonStyle { elevated, outlined, text }

/// A widget that provides smooth animated transitions between loading and content states.
///
/// This widget automatically handles the transition from loading indicators to
/// content with configurable fade and scale animations for improved user experience.
class GHLoadingTransition extends StatelessWidget {
  /// Whether to show the loading state
  final bool isLoading;

  /// The content to display when not loading
  final Widget child;

  /// The loading indicator to display when loading
  final Widget? loadingIndicator;

  /// Optional loading message
  final String? loadingMessage;

  /// Duration of the transition animation
  final Duration duration;

  /// Whether to use fade transition
  final bool useFadeTransition;

  /// Whether to use scale transition
  final bool useScaleTransition;

  const GHLoadingTransition({
    super.key,
    required this.isLoading,
    required this.child,
    this.loadingIndicator,
    this.loadingMessage,
    this.duration = const Duration(milliseconds: 300),
    this.useFadeTransition = true,
    this.useScaleTransition = false,
  });

  @override
  Widget build(BuildContext context) {
    Widget currentWidget = isLoading
        ? (loadingIndicator ??
              GHLoadingIndicator.large(label: loadingMessage, centered: true))
        : child;

    // Apply scale transition if enabled
    if (useScaleTransition && !isLoading) {
      currentWidget = TweenAnimationBuilder<double>(
        duration: duration,
        tween: Tween(begin: 0.8, end: 1.0),
        builder: (context, scale, child) {
          return Transform.scale(scale: scale, child: child);
        },
        child: currentWidget,
      );
    }

    // Apply fade transition if enabled
    if (useFadeTransition) {
      return AnimatedSwitcher(
        duration: duration,
        switchInCurve: Curves.easeInOut,
        switchOutCurve: Curves.easeInOut,
        child: currentWidget,
      );
    }

    return AnimatedSwitcher(duration: duration, child: currentWidget);
  }
}
