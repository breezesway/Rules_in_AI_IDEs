import 'package:flutter/material.dart';
import '../../tokens/gh_tokens.dart';
import '../../components/gh_card.dart';
import '../../components/gh_button.dart';
import '../../components/gh_chip.dart';
import '../../components/gh_text_field.dart';
import '../../state_widgets/gh_empty_state.dart';
import '../../state_widgets/gh_error_state.dart';
import '../../state_widgets/gh_loading_indicator.dart';
import 'comparison_screen.dart';
import 'mock_screen.dart';

/// A comparison screen showing component improvements.
///
/// This screen demonstrates the evolution from basic components
/// to enhanced components with proper state management.
class ComponentShowcaseComparisonScreen extends StatefulWidget {
  const ComponentShowcaseComparisonScreen({super.key});

  @override
  State<ComponentShowcaseComparisonScreen> createState() =>
      _ComponentShowcaseComparisonScreenState();
}

class _ComponentShowcaseComparisonScreenState
    extends State<ComponentShowcaseComparisonScreen> {
  bool _isLoading = false;
  bool _hasError = false;
  bool _isEmpty = false;

  @override
  Widget build(BuildContext context) {
    return ComparisonScreen(
      title: 'Component Showcase',
      beforeDescription:
          'Basic components without proper state management or consistent styling',
      afterDescription:
          'Enhanced components with state management, loading states, and GitHub-specific styling',
      highlights: const [
        ImprovementHighlight(
          description: 'Added comprehensive state management components',
        ),
        ImprovementHighlight(
          description: 'Implemented loading, empty, and error states',
        ),
        ImprovementHighlight(
          description: 'Enhanced button variants with proper feedback',
        ),
        ImprovementHighlight(
          description: 'Improved form components with validation',
        ),
        ImprovementHighlight(
          description: 'Consistent GitHub-themed styling throughout',
        ),
      ],
      beforeWidget: _buildBasicComponents(context),
      afterWidget: _buildEnhancedComponents(context),
    );
  }

  Widget _buildBasicComponents(BuildContext context) {
    return MockScreen(
      title: 'Basic Components',
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            /// Basic buttons section
            Text('Basic Buttons', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            Wrap(
              spacing: GHTokens.spacing8,
              runSpacing: GHTokens.spacing8,
              children: [
                /// Old basic button (just ElevatedButton)
                ElevatedButton(onPressed: () {}, child: const Text('Submit')),
                ElevatedButton(onPressed: null, child: const Text('Disabled')),
                OutlinedButton(onPressed: () {}, child: const Text('Cancel')),
              ],
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// Basic form components
            Text('Basic Form Components', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            /// Old basic text field
            const TextField(
              decoration: InputDecoration(
                labelText: 'Username',
                border: OutlineInputBorder(),
              ),
            ),

            const SizedBox(height: GHTokens.spacing12),

            /// Basic chips
            Wrap(
              spacing: GHTokens.spacing8,
              children: [
                Chip(label: Text('bug')),
                Chip(label: Text('enhancement')),
                Chip(label: Text('good first issue')),
              ],
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// Basic cards
            Text('Basic Cards', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Repository Card', style: GHTokens.titleMedium),
                    const SizedBox(height: GHTokens.spacing8),
                    Text(
                      'Basic card without proper GitHub styling',
                      style: GHTokens.bodyMedium,
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// No state management
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing16),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.errorContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.warning,
                        color: Theme.of(context).colorScheme.onErrorContainer,
                        size: 20,
                      ),
                      const SizedBox(width: GHTokens.spacing8),
                      Text(
                        'Issues with Basic Components',
                        style: GHTokens.titleMedium.copyWith(
                          color: Theme.of(context).colorScheme.onErrorContainer,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: GHTokens.spacing12),

                  _buildIssue(context, 'No loading states'),
                  _buildIssue(context, 'No error handling'),
                  _buildIssue(context, 'Inconsistent styling'),
                  _buildIssue(context, 'No empty states'),
                  _buildIssue(context, 'Limited interaction feedback'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEnhancedComponents(BuildContext context) {
    return MockScreen(
      title: 'Enhanced Components',
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            /// Enhanced buttons section
            Text('Enhanced GH Buttons', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            Wrap(
              spacing: GHTokens.spacing8,
              runSpacing: GHTokens.spacing8,
              children: [
                GHButton(
                  label: 'Primary Action',
                  style: GHButtonStyle.primary,
                  onPressed: () {
                    setState(() {
                      _isLoading = true;
                    });
                    Future.delayed(const Duration(seconds: 2), () {
                      if (mounted) {
                        setState(() {
                          _isLoading = false;
                        });
                      }
                    });
                  },
                ),
                GHButton(
                  label: 'Secondary Action',
                  style: GHButtonStyle.secondary,
                  onPressed: () {},
                ),
                GHButton(
                  label: 'Loading',
                  style: GHButtonStyle.primary,
                  isLoading: _isLoading,
                  onPressed: _isLoading ? null : () {},
                ),
                GHButton(
                  label: 'With Icon',
                  style: GHButtonStyle.secondary,
                  icon: Icons.star,
                  onPressed: () {},
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// Enhanced form components
            Text('Enhanced GH Form Components', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            GHTextField(
              labelText: 'Username',
              hintText: 'Enter your GitHub username',
              onChanged: (value) {},
            ),

            const SizedBox(height: GHTokens.spacing12),

            /// Enhanced chips
            Wrap(
              spacing: GHTokens.spacing8,
              children: [
                GHChip(
                  label: 'bug',
                  backgroundColor: GHTokens.error,
                  isSelected: true,
                  onTap: () {},
                ),
                GHChip(
                  label: 'enhancement',
                  backgroundColor: GHTokens.success,
                  onTap: () {},
                ),
                GHChip(
                  label: 'good first issue',
                  backgroundColor: GHTokens.primary,
                  onTap: () {},
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// Enhanced cards
            Text('Enhanced GH Cards', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            GHCard(
              onTap: () {},
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Repository Card', style: GHTokens.titleMedium),
                  const SizedBox(height: GHTokens.spacing8),
                  Text(
                    'Enhanced card with proper GitHub styling and interaction',
                    style: GHTokens.bodyMedium,
                  ),
                ],
              ),
            ),

            const SizedBox(height: GHTokens.spacing20),

            /// State management components
            Text('State Management Components', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing12),

            Row(
              children: [
                Expanded(
                  child: GHButton(
                    label: 'Show Loading',
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _isLoading = !_isLoading;
                        _hasError = false;
                        _isEmpty = false;
                      });
                    },
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: GHButton(
                    label: 'Show Error',
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _hasError = !_hasError;
                        _isLoading = false;
                        _isEmpty = false;
                      });
                    },
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: GHButton(
                    label: 'Show Empty',
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _isEmpty = !_isEmpty;
                        _isLoading = false;
                        _hasError = false;
                      });
                    },
                  ),
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing16),

            /// State demonstration
            SizedBox(height: 200, child: _buildStateDemo()),

            const SizedBox(height: GHTokens.spacing20),

            /// Benefits
            Container(
              padding: const EdgeInsets.all(GHTokens.spacing16),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        Icons.check_circle,
                        color: Theme.of(context).colorScheme.onPrimaryContainer,
                        size: 20,
                      ),
                      const SizedBox(width: GHTokens.spacing8),
                      Text(
                        'Enhanced Component Benefits',
                        style: GHTokens.titleMedium.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onPrimaryContainer,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: GHTokens.spacing12),

                  _buildBenefit(context, 'Comprehensive state management'),
                  _buildBenefit(context, 'Loading, error, and empty states'),
                  _buildBenefit(context, 'Consistent GitHub branding'),
                  _buildBenefit(context, 'Better accessibility support'),
                  _buildBenefit(context, 'Enhanced user interactions'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStateDemo() {
    if (_isLoading) {
      return const GHLoadingIndicator(label: 'Loading repositories...');
    }

    if (_hasError) {
      return GHErrorState(
        title: 'Failed to Load',
        message: 'Could not load repositories. Please try again.',
        onRetry: () {
          setState(() {
            _hasError = false;
          });
        },
      );
    }

    if (_isEmpty) {
      return GHEmptyState(
        icon: Icons.folder_open,
        title: 'No Repositories',
        subtitle: 'You haven\'t created any repositories yet.',
        action: GHButton(
          label: 'Create Repository',
          style: GHButtonStyle.primary,
          onPressed: () {
            setState(() {
              _isEmpty = false;
            });
          },
        ),
      );
    }

    return GHCard(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.folder,
              size: 48,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: GHTokens.spacing12),
            Text('Normal Content State', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              'Use the buttons above to see different states',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIssue(BuildContext context, String issue) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            Icons.close,
            size: 16,
            color: Theme.of(context).colorScheme.onErrorContainer,
          ),
          const SizedBox(width: GHTokens.spacing8),
          Expanded(
            child: Text(
              issue,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onErrorContainer,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBenefit(BuildContext context, String benefit) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            Icons.check,
            size: 16,
            color: Theme.of(context).colorScheme.onPrimaryContainer,
          ),
          const SizedBox(width: GHTokens.spacing8),
          Expanded(
            child: Text(
              benefit,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onPrimaryContainer,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
