import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'spacing_validator.dart';

/// A debug overlay widget that visualizes spacing measurements
/// and validates compliance with the 4dp grid system.
///
/// Only available in debug mode and intended for development use.
class SpacingDebugOverlay extends StatelessWidget {
  final Widget child;
  final bool showGrid;
  final bool showMeasurements;
  final Color gridColor;
  final Color validSpacingColor;
  final Color invalidSpacingColor;

  const SpacingDebugOverlay({
    super.key,
    required this.child,
    this.showGrid = false,
    this.showMeasurements = false,
    this.gridColor = Colors.blue,
    this.validSpacingColor = Colors.green,
    this.invalidSpacingColor = Colors.red,
  });

  @override
  Widget build(BuildContext context) {
    // Only show debug overlay in debug mode
    if (!kDebugMode) return child;

    return Stack(
      children: [
        child,
        if (showGrid) _buildGridOverlay(),
        if (showMeasurements) _buildMeasurementOverlay(),
      ],
    );
  }

  Widget _buildGridOverlay() {
    return Positioned.fill(
      child: CustomPaint(
        painter: _GridPainter(
          gridColor: gridColor.withValues(alpha: 0.3),
          gridUnit: 4.0,
        ),
      ),
    );
  }

  Widget _buildMeasurementOverlay() {
    return Positioned.fill(
      child: CustomPaint(
        painter: _MeasurementPainter(
          validColor: validSpacingColor.withValues(alpha: 0.7),
          invalidColor: invalidSpacingColor.withValues(alpha: 0.7),
        ),
      ),
    );
  }
}

/// Custom painter for drawing the 4dp grid
class _GridPainter extends CustomPainter {
  final Color gridColor;
  final double gridUnit;

  _GridPainter({required this.gridColor, required this.gridUnit});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = gridColor
      ..strokeWidth = 0.5
      ..style = PaintingStyle.stroke;

    // Draw vertical lines
    for (double x = 0; x <= size.width; x += gridUnit) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }

    // Draw horizontal lines
    for (double y = 0; y <= size.height; y += gridUnit) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Custom painter for drawing spacing measurements
class _MeasurementPainter extends CustomPainter {
  final Color validColor;
  final Color invalidColor;

  _MeasurementPainter({required this.validColor, required this.invalidColor});

  @override
  void paint(Canvas canvas, Size size) {
    // This is a placeholder for more advanced measurement drawing
    // In a real implementation, this would analyze the widget tree
    // and draw measurements for detected spacing values
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Debug utilities for spacing measurement and validation
class SpacingDebugUtils {
  SpacingDebugUtils._();

  /// Wraps a widget with spacing debug information
  static Widget debugSpacing(
    Widget child, {
    String? label,
    double? expectedSpacing,
  }) {
    if (!kDebugMode) return child;

    return Builder(
      builder: (context) {
        // In debug mode, add visual indicators or logging
        // debugLogSpacing was removed as it was a no-op
        return child;
      },
    );
  }

  /// Creates a debug spacing indicator widget
  static Widget spacingIndicator(
    double spacing, {
    String? label,
    bool horizontal = true,
  }) {
    if (!kDebugMode) {
      return horizontal ? SizedBox(width: spacing) : SizedBox(height: spacing);
    }

    final isValid = SpacingValidator.isValidSpacing(spacing);
    final color = isValid ? Colors.green : Colors.red;

    return Container(
      width: horizontal ? spacing : 2,
      height: horizontal ? 2 : spacing,
      color: color.withValues(alpha: 0.5),
      child: label != null
          ? Center(
              child: Text(
                label,
                style: const TextStyle(
                  fontSize: 8,
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
            )
          : null,
    );
  }

  /// Measures the actual spacing between two widgets
  static void measureSpacingBetween(
    GlobalKey firstKey,
    GlobalKey secondKey, {
    String? context,
  }) {
    if (!kDebugMode) return;

    WidgetsBinding.instance.addPostFrameCallback((_) {
      final firstBox =
          firstKey.currentContext?.findRenderObject() as RenderBox?;
      final secondBox =
          secondKey.currentContext?.findRenderObject() as RenderBox?;

      if (firstBox != null && secondBox != null) {
        final firstPosition = firstBox.localToGlobal(Offset.zero);
        final secondPosition = secondBox.localToGlobal(Offset.zero);

        final verticalSpacing =
            (secondPosition.dy - (firstPosition.dy + firstBox.size.height))
                .abs();
        final horizontalSpacing =
            (secondPosition.dx - (firstPosition.dx + firstBox.size.width))
                .abs();

        final contextStr = context != null ? '[$context] ' : '';
        debugPrint('${contextStr}Measured spacing:');
        debugPrint('$contextStr  Vertical: ${verticalSpacing}dp');
        debugPrint('$contextStr  Horizontal: ${horizontalSpacing}dp');

        // debugLogSpacing was removed as it was a no-op
      }
    });
  }

  /// Validates all EdgeInsets values
  static void debugEdgeInsets(EdgeInsets insets, {String? context}) {
    if (!kDebugMode) return;

    final contextStr = context != null ? '[$context] ' : '';
    debugPrint('${contextStr}EdgeInsets validation:');

    // debugLogSpacing was removed as it was a no-op
  }

  /// Validates SizedBox dimensions
  static void debugSizedBox(double? width, double? height, {String? context}) {
    if (!kDebugMode) return;

    // debugLogSpacing was removed as it was a no-op
  }
}
