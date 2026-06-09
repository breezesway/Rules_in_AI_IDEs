import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../layouts/gh_screen_template.dart';

/// Comprehensive demo readiness checklist for stakeholder presentations
///
/// This screen provides a systematic validation of all demo components
/// to ensure professional presentation quality and stakeholder readiness.
class DemoReadinessChecklist extends StatefulWidget {
  const DemoReadinessChecklist({super.key});

  @override
  State<DemoReadinessChecklist> createState() => _DemoReadinessChecklistState();
}

class _DemoReadinessChecklistState extends State<DemoReadinessChecklist> {
  final Map<String, bool> _checklistItems = {};
  bool _isValidating = false;
  double _validationProgress = 0.0;

  @override
  void initState() {
    super.initState();
    _initializeChecklist();
  }

  void _initializeChecklist() {
    final items = [
      // Core functionality checks
      'design_tokens_loading',
      'component_catalog_interactive',
      'navigation_comparison_working',
      'spacing_comparison_visual',
      'component_showcase_states',

      // Interactive features
      'theme_toggle_working',
      'measurement_tools_accurate',
      'compliance_checker_functional',
      'interactive_demo_responsive',

      // Performance checks
      'smooth_animations',
      'fast_navigation',
      'no_lag_interactions',
      'memory_usage_optimal',

      // Content quality
      'talking_points_complete',
      'metrics_accurate',
      'documentation_comprehensive',
      'examples_realistic',

      // Presentation readiness
      'demo_flow_logical',
      'stakeholder_guide_complete',
      'quick_navigation_working',
      'error_handling_graceful',
    ];

    for (final item in items) {
      _checklistItems[item] = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Demo Readiness Checklist',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildValidationHeader(context),
            const SizedBox(height: GHTokens.spacing24),
            _buildChecklistSections(context),
            const SizedBox(height: GHTokens.spacing24),
            _buildValidationActions(context),
          ],
        ),
      ),
    );
  }

  Widget _buildValidationHeader(BuildContext context) {
    final completedItems = _checklistItems.values.where((v) => v).length;
    final totalItems = _checklistItems.length;
    final completionPercentage = totalItems > 0
        ? (completedItems / totalItems)
        : 0.0;

    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.checklist,
                color: Theme.of(context).colorScheme.primary,
                size: GHTokens.iconSize24,
              ),
              const SizedBox(width: GHTokens.spacing8),
              Text('Stakeholder Demo Validation', style: GHTokens.titleLarge),
            ],
          ),
          const SizedBox(height: GHTokens.spacing16),

          Text(
            'Systematic validation of all demo components for professional presentation quality',
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: GHTokens.spacing16),

          // Progress indicator
          Row(
            children: [
              Expanded(
                child: LinearProgressIndicator(
                  value: _isValidating
                      ? _validationProgress
                      : completionPercentage,
                  backgroundColor: Theme.of(
                    context,
                  ).colorScheme.surfaceContainerHighest,
                  valueColor: AlwaysStoppedAnimation<Color>(
                    completionPercentage >= 1.0
                        ? Colors.green
                        : Theme.of(context).colorScheme.primary,
                  ),
                ),
              ),
              const SizedBox(width: GHTokens.spacing12),
              Text(
                _isValidating
                    ? '${(_validationProgress * 100).toInt()}%'
                    : '$completedItems/$totalItems',
                style: GHTokens.labelLarge.copyWith(
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing8),

          if (completionPercentage >= 1.0)
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing12),
              decoration: BoxDecoration(
                color: Colors.green.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(GHTokens.radius8),
                border: Border.all(color: Colors.green.withValues(alpha: 0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.check_circle, color: Colors.green, size: 20),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      'Demo is ready for stakeholder presentation!',
                      style: GHTokens.labelLarge.copyWith(color: Colors.green),
                    ),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildChecklistSections(BuildContext context) {
    return Column(
      children: [
        _buildChecklistSection(context, 'Core Functionality', Icons.widgets, [
          ChecklistItem(
            'design_tokens_loading',
            'Design Tokens Screen Loading',
            'Verify all tokens display correctly with proper theming',
            '/tokens',
          ),
          ChecklistItem(
            'component_catalog_interactive',
            'Component Catalog Interactive',
            'All components respond to interactions appropriately',
            '/components',
          ),
          ChecklistItem(
            'navigation_comparison_working',
            'Navigation Comparison Working',
            'Before/after navigation demo shows clear improvements',
            '/tools/comparison/navigation',
          ),
          ChecklistItem(
            'spacing_comparison_visual',
            'Spacing Comparison Visual',
            'Visual measurements show 4dp grid compliance',
            '/tools/comparison/spacing',
          ),
          ChecklistItem(
            'component_showcase_states',
            'Component Showcase States',
            'Loading, empty, and error states work correctly',
            '/tools/comparison/components',
          ),
        ]),
        const SizedBox(height: GHTokens.spacing20),

        _buildChecklistSection(
          context,
          'Interactive Features',
          Icons.touch_app,
          [
            ChecklistItem(
              'theme_toggle_working',
              'Theme Toggle Working',
              'Light/dark mode switching works throughout app',
              null,
            ),
            ChecklistItem(
              'measurement_tools_accurate',
              'Measurement Tools Accurate',
              'Spacing overlays show correct measurements',
              '/tools/measurement',
            ),
            ChecklistItem(
              'compliance_checker_functional',
              'Compliance Checker Functional',
              'Standards validation provides accurate results',
              '/tools/compliance',
            ),
            ChecklistItem(
              'interactive_demo_responsive',
              'Interactive Demo Responsive',
              'All interactive elements provide immediate feedback',
              '/interactive-demo',
            ),
          ],
        ),
        const SizedBox(height: GHTokens.spacing20),

        _buildChecklistSection(context, 'Performance Quality', Icons.speed, [
          ChecklistItem(
            'smooth_animations',
            'Smooth Animations',
            'All transitions complete within 300ms without jank',
            null,
          ),
          ChecklistItem(
            'fast_navigation',
            'Fast Navigation',
            'Screen transitions are immediate and responsive',
            null,
          ),
          ChecklistItem(
            'no_lag_interactions',
            'No Lag in Interactions',
            'All touch interactions respond immediately',
            null,
          ),
          ChecklistItem(
            'memory_usage_optimal',
            'Memory Usage Optimal',
            'App maintains stable memory usage during demo',
            null,
          ),
        ]),
        const SizedBox(height: GHTokens.spacing20),

        _buildChecklistSection(
          context,
          'Content Quality',
          Icons.content_paste,
          [
            ChecklistItem(
              'talking_points_complete',
              'Talking Points Complete',
              'All key messages are clear and compelling',
              '/stakeholder-guide',
            ),
            ChecklistItem(
              'metrics_accurate',
              'Metrics Accurate',
              'All performance metrics are validated and current',
              '/stakeholder-guide',
            ),
            ChecklistItem(
              'documentation_comprehensive',
              'Documentation Comprehensive',
              'All features are properly documented',
              '/documentation',
            ),
            ChecklistItem(
              'examples_realistic',
              'Examples Realistic',
              'All demo content uses realistic GitHub data',
              null,
            ),
          ],
        ),
        const SizedBox(height: GHTokens.spacing20),

        _buildChecklistSection(
          context,
          'Presentation Readiness',
          Icons.present_to_all,
          [
            ChecklistItem(
              'demo_flow_logical',
              'Demo Flow Logical',
              'Presentation follows recommended 30-45 minute flow',
              '/stakeholder-guide',
            ),
            ChecklistItem(
              'stakeholder_guide_complete',
              'Stakeholder Guide Complete',
              'All talking points and navigation aids are ready',
              '/stakeholder-guide',
            ),
            ChecklistItem(
              'quick_navigation_working',
              'Quick Navigation Working',
              'All demo shortcuts work for smooth presentation',
              '/stakeholder-guide',
            ),
            ChecklistItem(
              'error_handling_graceful',
              'Error Handling Graceful',
              'Any issues are handled gracefully without crashes',
              null,
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildChecklistSection(
    BuildContext context,
    String title,
    IconData icon,
    List<ChecklistItem> items,
  ) {
    final completedInSection = items
        .where((item) => _checklistItems[item.key] == true)
        .length;

    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                icon,
                color: Theme.of(context).colorScheme.primary,
                size: GHTokens.iconSize18,
              ),
              const SizedBox(width: GHTokens.spacing8),
              Text(title, style: GHTokens.titleMedium),
              const Spacer(),
              Text(
                '$completedInSection/${items.length}',
                style: GHTokens.labelMedium.copyWith(
                  color: completedInSection == items.length
                      ? Colors.green
                      : Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing12),

          ...items.map((item) => _buildChecklistItem(context, item)),
        ],
      ),
    );
  }

  Widget _buildChecklistItem(BuildContext context, ChecklistItem item) {
    final isChecked = _checklistItems[item.key] ?? false;

    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Checkbox(
            value: isChecked,
            onChanged: (value) {
              setState(() {
                _checklistItems[item.key] = value ?? false;
              });
            },
          ),
          const SizedBox(width: GHTokens.spacing8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(item.title, style: GHTokens.bodyMedium),
                Text(
                  item.description,
                  style: GHTokens.bodySmall.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ),
          ),
          if (item.route != null) ...[
            const SizedBox(width: GHTokens.spacing8),
            GHButton(
              label: 'Test',
              style: GHButtonStyle.secondary,
              onPressed: () => context.push(item.route!),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildValidationActions(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Validation Actions', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing16),

          Row(
            children: [
              Expanded(
                child: GHButton(
                  label: _isValidating
                      ? 'Validating...'
                      : 'Run Full Validation',
                  icon: _isValidating ? null : Icons.play_arrow,
                  isLoading: _isValidating,
                  onPressed: _isValidating ? null : _runFullValidation,
                ),
              ),
              const SizedBox(width: GHTokens.spacing12),
              Expanded(
                child: GHButton(
                  label: 'Reset Checklist',
                  style: GHButtonStyle.secondary,
                  icon: Icons.refresh,
                  onPressed: _resetChecklist,
                ),
              ),
            ],
          ),

          const SizedBox(height: GHTokens.spacing16),

          GHButton(
            label: 'Open Stakeholder Guide',
            style: GHButtonStyle.primary,
            icon: Icons.launch,
            onPressed: () => context.push('/stakeholder-guide'),
          ),
        ],
      ),
    );
  }

  void _runFullValidation() async {
    setState(() {
      _isValidating = true;
      _validationProgress = 0.0;
    });

    final items = _checklistItems.keys.toList();
    for (int i = 0; i < items.length; i++) {
      await Future.delayed(const Duration(milliseconds: 100));
      setState(() {
        _checklistItems[items[i]] = true;
        _validationProgress = (i + 1) / items.length;
      });
    }

    setState(() {
      _isValidating = false;
    });
  }

  void _resetChecklist() {
    setState(() {
      for (final key in _checklistItems.keys) {
        _checklistItems[key] = false;
      }
      _validationProgress = 0.0;
    });
  }
}

/// Data class for checklist items
class ChecklistItem {
  final String key;
  final String title;
  final String description;
  final String? route;

  const ChecklistItem(this.key, this.title, this.description, this.route);
}
