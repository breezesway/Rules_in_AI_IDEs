import 'package:flutter/material.dart';
import '../../tokens/gh_tokens.dart';
import '../../components/gh_card.dart';
import '../../layouts/gh_screen_template.dart';

/// A reusable screen widget for displaying before/after comparisons.
///
/// This widget provides a tabbed interface to showcase improvements
/// made to the UI system by comparing the old implementation with
/// the new one.
class ComparisonScreen extends StatefulWidget {
  /// The title displayed in the app bar
  final String title;

  /// Widget showing the "before" state
  final Widget beforeWidget;

  /// Widget showing the "after" state
  final Widget afterWidget;

  /// Description text for the before state
  final String beforeDescription;

  /// Description text for the after state
  final String afterDescription;

  /// List of improvement highlights to display
  final List<ImprovementHighlight> highlights;

  const ComparisonScreen({
    super.key,
    required this.title,
    required this.beforeWidget,
    required this.afterWidget,
    required this.beforeDescription,
    required this.afterDescription,
    required this.highlights,
  });

  @override
  State<ComparisonScreen> createState() => _ComparisonScreenState();
}

class _ComparisonScreenState extends State<ComparisonScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: widget.title,
      body: Column(
        children: [
          /// Improvement highlights section
          _buildHighlightsSection(),
          const SizedBox(height: GHTokens.spacing20),

          /// Before/After tabs
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              borderRadius: BorderRadius.circular(8),
            ),
            child: TabBar(
              controller: _tabController,
              labelColor: Theme.of(context).colorScheme.primary,
              unselectedLabelColor: Theme.of(
                context,
              ).colorScheme.onSurfaceVariant,
              indicator: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              tabs: const [
                Tab(text: 'Before'),
                Tab(text: 'After'),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing16),

          /// Tab content
          Expanded(
            child: TabBarView(
              controller: _tabController,
              children: [_buildBeforeView(), _buildAfterView()],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHighlightsSection() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Key Improvements', style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing12),

          ...widget.highlights.map(
            (highlight) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.check_circle, size: 20, color: GHTokens.success),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      highlight.description,
                      style: GHTokens.bodyMedium,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBeforeView() {
    return Column(
      children: [
        /// Description card
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(Icons.warning, color: GHTokens.warning, size: 20),
                  const SizedBox(width: GHTokens.spacing8),
                  Text(
                    'Before (Old Implementation)',
                    style: GHTokens.titleMedium.copyWith(
                      color: GHTokens.warning,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing8),
              Text(widget.beforeDescription, style: GHTokens.bodyMedium),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        /// Before widget
        Expanded(child: widget.beforeWidget),
      ],
    );
  }

  Widget _buildAfterView() {
    return Column(
      children: [
        /// Description card
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(Icons.check_circle, color: GHTokens.success, size: 20),
                  const SizedBox(width: GHTokens.spacing8),
                  Text(
                    'After (New Implementation)',
                    style: GHTokens.titleMedium.copyWith(
                      color: GHTokens.success,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing8),
              Text(widget.afterDescription, style: GHTokens.bodyMedium),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        /// After widget
        Expanded(child: widget.afterWidget),
      ],
    );
  }
}

/// Represents a single improvement highlight.
class ImprovementHighlight {
  /// Description of the improvement
  final String description;

  /// Optional additional details about the improvement
  final String? details;

  const ImprovementHighlight({required this.description, this.details});
}
