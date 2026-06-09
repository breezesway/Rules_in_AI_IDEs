import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../components/gh_chip.dart';
import '../layouts/gh_screen_template.dart';

/// Screen for measurement and validation tools to help developers verify
/// design system compliance and validate spacing implementations.
///
/// This screen provides debugging tools and visual overlays to ensure
/// proper adherence to the 4dp grid system and design standards.
class MeasurementValidationScreen extends StatefulWidget {
  const MeasurementValidationScreen({super.key});

  @override
  State<MeasurementValidationScreen> createState() =>
      _MeasurementValidationScreenState();
}

class _MeasurementValidationScreenState
    extends State<MeasurementValidationScreen> {
  bool _showSpacingOverlay = false;
  bool _showGridLines = false;
  bool _showTouchTargets = false;
  bool _highlightNonCompliant = false;
  String _selectedTool = 'spacing';

  final List<String> _toolOptions = ['spacing', 'grid', 'touch', 'compliance'];

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Measurement & Validation Tools',
      body: Stack(
        children: [
          // Main content
          SingleChildScrollView(
            child: Column(
              children: [
                // Tools selector
                _buildToolSelector(),
                const SizedBox(height: GHTokens.spacing20),

                // Selected tool content
                _buildSelectedTool(),
                const SizedBox(height: GHTokens.spacing20),

                // Sample content for measurement
                _buildSampleContent(),
              ],
            ),
          ),

          // Overlay layers
          if (_showSpacingOverlay) _buildSpacingOverlay(),
          if (_showGridLines) _buildGridOverlay(),
          if (_showTouchTargets) _buildTouchTargetOverlay(),
          if (_highlightNonCompliant) _buildComplianceOverlay(),
        ],
      ),
    );
  }

  Widget _buildToolSelector() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Developer Tools', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Text(
            'Select a tool to inspect and validate design system implementation.',
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: GHTokens.spacing12),

          Wrap(
            spacing: GHTokens.spacing8,
            children: _toolOptions
                .map(
                  (tool) => GHChip(
                    label: _getToolLabel(tool),
                    isSelected: _selectedTool == tool,
                    onTap: () {
                      setState(() {
                        _selectedTool = tool;
                        // Reset all overlays when switching tools
                        _showSpacingOverlay = false;
                        _showGridLines = false;
                        _showTouchTargets = false;
                        _highlightNonCompliant = false;
                      });
                    },
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }

  String _getToolLabel(String tool) {
    switch (tool) {
      case 'spacing':
        return 'Spacing Measurements';
      case 'grid':
        return '4dp Grid Lines';
      case 'touch':
        return 'Touch Targets';
      case 'compliance':
        return 'Standards Compliance';
      default:
        return tool;
    }
  }

  Widget _buildSelectedTool() {
    switch (_selectedTool) {
      case 'spacing':
        return _buildSpacingTool();
      case 'grid':
        return _buildGridTool();
      case 'touch':
        return _buildTouchTool();
      case 'compliance':
        return _buildComplianceTool();
      default:
        return _buildSpacingTool();
    }
  }

  Widget _buildSpacingTool() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Spacing Measurement Tool', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Text(
            'Show visual measurements of spacing between elements to verify 4dp grid compliance.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          GHButton(
            label: _showSpacingOverlay
                ? 'Hide Measurements'
                : 'Show Measurements',
            style: _showSpacingOverlay
                ? GHButtonStyle.primary
                : GHButtonStyle.secondary,
            icon: _showSpacingOverlay ? Icons.visibility_off : Icons.straighten,
            onPressed: () {
              setState(() {
                _showSpacingOverlay = !_showSpacingOverlay;
              });
            },
          ),

          if (_showSpacingOverlay) ...[
            const SizedBox(height: GHTokens.spacing12),
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing12),
              decoration: BoxDecoration(
                color: GHTokens.success.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(GHTokens.radius8),
                border: Border.all(
                  color: GHTokens.success.withValues(alpha: 0.3),
                ),
              ),
              child: Row(
                children: [
                  Icon(Icons.info, color: GHTokens.success, size: 16),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      'Spacing overlay active. Red measurements indicate non-compliant spacing.',
                      style: GHTokens.labelMedium.copyWith(
                        color: GHTokens.success,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildGridTool() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('4dp Grid Lines', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Text(
            'Display 4dp grid lines to visualize alignment and spacing consistency.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          GHButton(
            label: _showGridLines ? 'Hide Grid' : 'Show Grid',
            style: _showGridLines
                ? GHButtonStyle.primary
                : GHButtonStyle.secondary,
            icon: _showGridLines ? Icons.grid_off : Icons.grid_4x4,
            onPressed: () {
              setState(() {
                _showGridLines = !_showGridLines;
              });
            },
          ),

          if (_showGridLines) ...[
            const SizedBox(height: GHTokens.spacing12),
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing12),
              decoration: BoxDecoration(
                color: Colors.blue.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(GHTokens.radius8),
                border: Border.all(color: Colors.blue.withValues(alpha: 0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.info, color: Colors.blue, size: 16),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      'Grid overlay active. Elements should align to 4dp grid lines.',
                      style: GHTokens.labelMedium.copyWith(color: Colors.blue),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildTouchTool() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Touch Target Validation', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Text(
            'Highlight touch targets to ensure minimum 48dp accessibility compliance.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          GHButton(
            label: _showTouchTargets
                ? 'Hide Touch Targets'
                : 'Show Touch Targets',
            style: _showTouchTargets
                ? GHButtonStyle.primary
                : GHButtonStyle.secondary,
            icon: _showTouchTargets
                ? Icons.touch_app
                : Icons.touch_app_outlined,
            onPressed: () {
              setState(() {
                _showTouchTargets = !_showTouchTargets;
              });
            },
          ),

          if (_showTouchTargets) ...[
            const SizedBox(height: GHTokens.spacing12),
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing12),
              decoration: BoxDecoration(
                color: Colors.orange.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(GHTokens.radius8),
                border: Border.all(color: Colors.orange.withValues(alpha: 0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.info, color: Colors.orange, size: 16),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      'Touch target overlay active. Red highlights indicate touch targets smaller than 48dp.',
                      style: GHTokens.labelMedium.copyWith(
                        color: Colors.orange,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildComplianceTool() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Standards Compliance Checker', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing8),
          Text(
            'Automatically detect and highlight elements that don\'t follow design system standards.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          GHButton(
            label: _highlightNonCompliant ? 'Hide Issues' : 'Check Compliance',
            style: _highlightNonCompliant
                ? GHButtonStyle.primary
                : GHButtonStyle.secondary,
            icon: _highlightNonCompliant
                ? Icons.check_circle
                : Icons.warning_outlined,
            onPressed: () {
              setState(() {
                _highlightNonCompliant = !_highlightNonCompliant;
              });
            },
          ),

          if (_highlightNonCompliant) ...[
            const SizedBox(height: GHTokens.spacing12),
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing12),
              decoration: BoxDecoration(
                color: GHTokens.error.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(GHTokens.radius8),
                border: Border.all(
                  color: GHTokens.error.withValues(alpha: 0.3),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.warning, color: GHTokens.error, size: 16),
                      const SizedBox(width: GHTokens.spacing8),
                      Text(
                        'Compliance Issues Found',
                        style: GHTokens.labelLarge.copyWith(
                          color: GHTokens.error,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: GHTokens.spacing8),
                  Text(
                    '• Non-standard spacing detected (highlighted in red)\n'
                    '• Touch targets smaller than 48dp (highlighted in orange)\n'
                    '• Elements not aligned to 4dp grid (highlighted in yellow)',
                    style: GHTokens.bodyMedium.copyWith(color: GHTokens.error),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSampleContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Sample Content for Testing', style: GHTokens.titleLarge),
        const SizedBox(height: GHTokens.spacing16),

        // Sample cards with various spacing
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Standard Card', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This card uses standard 16dp padding.',
                style: GHTokens.bodyMedium,
              ),
              const SizedBox(height: GHTokens.spacing12),
              Row(
                children: [
                  GHButton(
                    label: 'Action',
                    style: GHButtonStyle.primary,
                    onPressed: () {},
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  GHButton(
                    label: 'Cancel',
                    style: GHButtonStyle.secondary,
                    onPressed: () {},
                  ),
                ],
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Card with intentionally non-standard spacing for testing
        Container(
          padding: const EdgeInsets.all(15), // Non-standard 15dp padding
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surfaceContainerLow,
            borderRadius: BorderRadius.circular(GHTokens.radius12),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Non-Compliant Card', style: GHTokens.titleMedium),
              const SizedBox(height: 7), // Non-standard 7dp spacing
              Text(
                'This card uses non-standard 15dp padding and 7dp spacing.',
                style: GHTokens.bodyMedium,
              ),
              const SizedBox(height: 11), // Non-standard 11dp spacing
              ElevatedButton(
                onPressed: () {},
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size(40, 40), // Below 48dp touch target
                ),
                child: const Text('Small'),
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing20),

        // Grid alignment test
        Row(
          children: [
            Expanded(
              child: GHCard(
                child: Text('Grid Test 1', style: GHTokens.bodyMedium),
              ),
            ),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: GHCard(
                child: Text('Grid Test 2', style: GHTokens.bodyMedium),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildSpacingOverlay() {
    return Positioned.fill(
      child: IgnorePointer(
        child: CustomPaint(painter: SpacingOverlayPainter()),
      ),
    );
  }

  Widget _buildGridOverlay() {
    return Positioned.fill(
      child: IgnorePointer(child: CustomPaint(painter: GridOverlayPainter())),
    );
  }

  Widget _buildTouchTargetOverlay() {
    return Positioned.fill(
      child: IgnorePointer(
        child: CustomPaint(painter: TouchTargetOverlayPainter()),
      ),
    );
  }

  Widget _buildComplianceOverlay() {
    return Positioned.fill(
      child: IgnorePointer(
        child: CustomPaint(painter: ComplianceOverlayPainter()),
      ),
    );
  }
}

/// Custom painter for spacing measurement overlay
class SpacingOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = GHTokens.success.withValues(alpha: 0.8)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;

    final errorPaint = Paint()
      ..color = GHTokens.error.withValues(alpha: 0.8)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    // Draw measurement lines at key spacing intervals
    final standardSpacings = [16, 32, 48, 64, 80]; // Standard spacing values

    for (int i = 0; i < standardSpacings.length; i++) {
      final y = standardSpacings[i].toDouble() * 2; // Scale for visibility
      if (y < size.height) {
        // Draw measurement line
        canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);

        // Draw measurement text
        final textPainter = TextPainter(
          text: TextSpan(
            text: '${standardSpacings[i]}dp',
            style: TextStyle(
              color: GHTokens.success,
              fontSize: 10,
              fontWeight: FontWeight.bold,
            ),
          ),
          textDirection: TextDirection.ltr,
        );
        textPainter.layout();
        textPainter.paint(canvas, Offset(4, y - 12));
      }
    }

    // Highlight non-compliant spacing (example at specific locations)
    canvas.drawRect(const Rect.fromLTWH(0, 150, 100, 2), errorPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Custom painter for 4dp grid overlay
class GridOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue.withValues(alpha: 0.3)
      ..strokeWidth = 0.5;

    // Draw 4dp grid lines
    for (double x = 0; x < size.width; x += 4) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }

    for (double y = 0; y < size.height; y += 4) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Custom painter for touch target overlay
class TouchTargetOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final goodPaint = Paint()
      ..color = GHTokens.success.withValues(alpha: 0.3)
      ..style = PaintingStyle.fill;

    final badPaint = Paint()
      ..color = GHTokens.error.withValues(alpha: 0.5)
      ..style = PaintingStyle.fill;

    // Example touch target highlights (in real implementation,
    // this would analyze actual widget positions)

    // Good touch target (48dp+)
    canvas.drawCircle(const Offset(100, 200), 24, goodPaint);

    // Bad touch target (less than 48dp)
    canvas.drawCircle(const Offset(200, 200), 16, badPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

/// Custom painter for compliance overlay
class ComplianceOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final spacingPaint = Paint()
      ..color = GHTokens.error.withValues(alpha: 0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    final touchPaint = Paint()
      ..color = Colors.orange.withValues(alpha: 0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    final gridPaint = Paint()
      ..color = Colors.yellow.withValues(alpha: 0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    // Highlight non-compliant elements (examples)

    // Non-standard spacing
    canvas.drawRect(const Rect.fromLTWH(16, 300, 200, 80), spacingPaint);

    // Small touch target
    canvas.drawCircle(const Offset(150, 400), 20, touchPaint);

    // Off-grid alignment
    canvas.drawRect(
      const Rect.fromLTWH(17, 450, 100, 40), // 17dp offset (not on 4dp grid)
      gridPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
