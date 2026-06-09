import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'spacing_validator.dart';
import '../tokens/gh_tokens.dart';

/// Developer tools for spacing verification and debugging.
///
/// Provides a suite of tools for developers to verify spacing compliance,
/// debug spacing issues, and maintain the 4dp grid system.
class SpacingDeveloperTools {
  SpacingDeveloperTools._();

  /// Shows a debug panel with spacing validation tools
  static void showSpacingDebugPanel(BuildContext context) {
    if (!kDebugMode) return;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      builder: (context) => const _SpacingDebugPanel(),
    );
  }

  /// Analyzes all spacing constants and reports compliance
  static void analyzeSpacingCompliance() {
    if (!kDebugMode) return;

    debugPrint('🔍 Spacing Compliance Analysis');
    debugPrint('================================');

    final spacings = SpacingValidator.getStandardSpacings();
    int validCount = 0;
    int invalidCount = 0;

    for (final spacing in spacings) {
      final result = SpacingValidator.validateWithDetails(spacing);
      if (result.isValid) {
        validCount++;
        debugPrint('✅ ${result.constantName}: ${result.value}dp - VALID');
      } else {
        invalidCount++;
        debugPrint('❌ Spacing ${result.value}dp - INVALID (not 4dp aligned)');
      }
    }

    debugPrint('================================');
    debugPrint('Summary: $validCount valid, $invalidCount invalid');
    debugPrint('Grid compliance: ${invalidCount == 0 ? "PASS" : "FAIL"}');
  }

  /// Generates a spacing reference guide
  static void generateSpacingReference() {
    if (!kDebugMode) return;

    debugPrint('📐 Spacing Reference Guide');
    debugPrint('==========================');
    debugPrint('Base grid unit: 4dp');
    debugPrint('');

    final spacings = [
      ('Micro spacing', GHTokens.spacing4, 'Icon gaps, very small gaps'),
      ('Small spacing', GHTokens.spacing8, 'Chip gaps'),
      ('Medium spacing', GHTokens.spacing12, 'Section padding'),
      ('Standard spacing', GHTokens.spacing16, 'Card padding'),
      ('Large spacing', GHTokens.spacing20, 'Section margins'),
      ('XL spacing', GHTokens.spacing24, 'Screen padding'),
      ('XXL spacing', GHTokens.spacing32, 'Major sections'),
    ];

    for (final (name, value, usage) in spacings) {
      debugPrint(
        '${name.padRight(16)}: ${value.toString().padLeft(5)}dp - $usage',
      );
    }

    debugPrint('');
    debugPrint('Usage guidelines:');
    debugPrint('- Use spacing4 for micro adjustments between icons');
    debugPrint('- Use spacing8 for related items (list items)');
    debugPrint('- Use spacing12 for unrelated items');
    debugPrint('- Use spacing16 for standard card padding');
    debugPrint('- Use spacing20 for major section separation');
    debugPrint('- Use spacing24 for screen-level padding');
    debugPrint('- Use spacing32 for major content blocks');
  }

  /// Validates a custom spacing value and provides recommendations
  static void validateCustomSpacing(double spacing, {String? context}) {
    if (!kDebugMode) return;

    final result = SpacingValidator.validateWithDetails(spacing);
    final contextStr = context != null ? '[$context] ' : '';

    debugPrint('${contextStr}Custom Spacing Validation');
    debugPrint('$contextStr${"=" * 30}');
    debugPrint('${contextStr}Input value: ${result.value}dp');
    debugPrint('${contextStr}Valid: ${result.isValid ? "YES" : "NO"}');

    if (!result.isValid) {
      debugPrint('$contextStr❌ Not aligned to 4dp grid');
      debugPrint('${contextStr}Recommended: ${result.nearestValidValue}dp');
    }

    if (!result.isStandardConstant && result.isValid) {
      debugPrint('$contextStr⚠️  Valid but non-standard spacing');
      debugPrint('${contextStr}Consider using: ${result.closestStandardName}');
    }

    if (result.isStandardConstant) {
      debugPrint(
        '$contextStr✅ Using standard constant: ${result.constantName}',
      );
    }
  }

  /// Checks for common spacing antipatterns
  static void checkSpacingAntipatterns(
    List<double> spacings, {
    String? context,
  }) {
    if (!kDebugMode) return;

    final contextStr = context != null ? '[$context] ' : '';
    debugPrint('${contextStr}Checking for spacing antipatterns...');

    // Check for non-4dp aligned values
    final nonCompliant = spacings
        .where((s) => !SpacingValidator.isValidSpacing(s))
        .toList();
    if (nonCompliant.isNotEmpty) {
      debugPrint('$contextStr❌ Non-4dp aligned spacings found: $nonCompliant');
    }

    // Check for odd values that might indicate mistakes
    final oddValues = spacings.where((s) => s > 0 && s < 4).toList();
    if (oddValues.isNotEmpty) {
      debugPrint('$contextStr⚠️  Suspiciously small spacings: $oddValues');
    }

    // Check for very large spacings that might be mistakes
    final largeValues = spacings.where((s) => s > 64).toList();
    if (largeValues.isNotEmpty) {
      debugPrint('$contextStr⚠️  Unusually large spacings: $largeValues');
    }

    // Check for duplicate consecutive spacings
    for (int i = 0; i < spacings.length - 1; i++) {
      if (spacings[i] == spacings[i + 1] && spacings[i] > 0) {
        debugPrint(
          '$contextStr⚠️  Duplicate consecutive spacing: ${spacings[i]}dp at positions $i and ${i + 1}',
        );
      }
    }
  }
}

/// Debug panel widget for spacing tools
class _SpacingDebugPanel extends StatefulWidget {
  const _SpacingDebugPanel();

  @override
  State<_SpacingDebugPanel> createState() => _SpacingDebugPanelState();
}

class _SpacingDebugPanelState extends State<_SpacingDebugPanel> {
  double _customSpacing = 16.0;
  final _customSpacingController = TextEditingController(text: '16.0');

  @override
  void dispose() {
    _customSpacingController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.7,
      padding: const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Row(
            children: [
              const Icon(Icons.space_bar, size: 24),
              const SizedBox(width: GHTokens.spacing8),
              Text(
                'Spacing Developer Tools',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const Spacer(),
              IconButton(
                onPressed: () => Navigator.of(context).pop(),
                icon: const Icon(Icons.close),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing16),

          // Quick actions
          Wrap(
            spacing: GHTokens.spacing8,
            runSpacing: GHTokens.spacing8,
            children: [
              ElevatedButton.icon(
                onPressed: () =>
                    SpacingDeveloperTools.analyzeSpacingCompliance(),
                icon: const Icon(Icons.analytics, size: 16),
                label: const Text('Analyze Compliance'),
              ),
              ElevatedButton.icon(
                onPressed: () =>
                    SpacingDeveloperTools.generateSpacingReference(),
                icon: const Icon(Icons.library_books, size: 16),
                label: const Text('Show Reference'),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing20),

          // Custom spacing validator
          Text(
            'Custom Spacing Validator',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: GHTokens.spacing8),
          Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _customSpacingController,
                  keyboardType: TextInputType.number,
                  decoration: const InputDecoration(
                    labelText: 'Spacing value (dp)',
                    border: OutlineInputBorder(),
                  ),
                  onChanged: (value) {
                    final spacing = double.tryParse(value);
                    if (spacing != null) {
                      setState(() {
                        _customSpacing = spacing;
                      });
                    }
                  },
                ),
              ),
              const SizedBox(width: GHTokens.spacing8),
              ElevatedButton(
                onPressed: () => SpacingDeveloperTools.validateCustomSpacing(
                  _customSpacing,
                  context: 'Debug Panel',
                ),
                child: const Text('Validate'),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing12),

          // Validation result
          _buildValidationResult(),

          const SizedBox(height: GHTokens.spacing20),

          // Standard spacings reference
          Text(
            'Standard Spacing Constants',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: GHTokens.spacing8),
          Expanded(child: _buildSpacingReference()),
        ],
      ),
    );
  }

  Widget _buildValidationResult() {
    final result = SpacingValidator.validateWithDetails(_customSpacing);

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  result.isValid ? Icons.check_circle : Icons.error,
                  color: result.isValid ? Colors.green : Colors.red,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Text(
                  result.isValid ? 'Valid spacing' : 'Invalid spacing',
                  style: Theme.of(context).textTheme.titleSmall,
                ),
              ],
            ),
            const SizedBox(height: GHTokens.spacing4),
            if (!result.isValid) ...[
              Text('Nearest valid: ${result.nearestValidValue}dp'),
            ],
            if (result.isStandardConstant) ...[
              Text('Standard constant: ${result.constantName}'),
            ] else ...[
              Text(
                'Closest standard: ${result.closestStandardName} (${result.closestStandardValue}dp)',
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildSpacingReference() {
    final spacings = [
      ('spacing4', GHTokens.spacing4, 'Micro spacing'),
      ('spacing8', GHTokens.spacing8, 'Small spacing'),
      ('spacing12', GHTokens.spacing12, 'Medium spacing'),
      ('spacing16', GHTokens.spacing16, 'Standard spacing'),
      ('spacing20', GHTokens.spacing20, 'Large spacing'),
      ('spacing24', GHTokens.spacing24, 'XL spacing'),
      ('spacing32', GHTokens.spacing32, 'XXL spacing'),
    ];

    return ListView.builder(
      itemCount: spacings.length,
      itemBuilder: (context, index) {
        final (name, value, description) = spacings[index];
        return ListTile(
          leading: Container(
            width: 40,
            height: 20,
            decoration: BoxDecoration(
              color: Colors.blue.withValues(alpha: 0.3),
              border: Border.all(color: Colors.blue),
            ),
            child: Center(
              child: Text(
                '${value.toInt()}',
                style: const TextStyle(
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          title: Text('GHTokens.$name'),
          subtitle: Text('$description (${value}dp)'),
          dense: true,
        );
      },
    );
  }
}
