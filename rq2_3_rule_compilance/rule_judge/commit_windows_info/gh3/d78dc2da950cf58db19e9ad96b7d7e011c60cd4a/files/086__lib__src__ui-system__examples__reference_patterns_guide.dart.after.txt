import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../state_widgets/gh_loading_indicator.dart';
import '../state_widgets/gh_empty_state.dart';
import '../state_widgets/gh_error_state.dart';
import '../layouts/gh_screen_template.dart';

/// **REFERENCE PATTERNS GUIDE** - Implementation Best Practices
///
/// This file serves as a comprehensive guide for implementing GH3 design system
/// components with correct patterns, spacing, and state management.
///
/// **CRITICAL IMPLEMENTATION PATTERNS:**
///
/// 1. **Screen Structure Pattern:**
///    - Always use GHScreenTemplate for screen consistency
///    - Use GHTokens.spacing16 for standard screen padding
///    - Implement proper scroll behavior with SingleChildScrollView
///
/// 2. **Spacing Pattern:**
///    - Use GHTokens spacing constants exclusively (no magic numbers)
///    - Follow 4dp grid system: spacing4, spacing8, spacing12, spacing16, etc.
///    - Use spacing32 for major section separations
///    - Use spacing16 for standard component spacing
///    - Use spacing8 for compact layouts
///
/// 3. **Component Pattern:**
///    - Wrap related components in GHCard for content grouping
///    - Use consistent padding inside cards
///    - Implement proper onTap handlers for interactive elements
///
/// 4. **Typography Pattern:**
///    - Use GHTokens typography constants exclusively
///    - headlineMedium for page titles
///    - titleLarge for major sections
///    - titleMedium for component titles
///    - bodyMedium for standard content
///    - labelLarge for captions and metadata
///
/// 5. **State Management Pattern:**
///    - Use GHLoadingIndicator for async operations
///    - Use GHEmptyState when content is unavailable
///    - Use GHErrorState with retry functionality for errors
///    - Implement proper loading states for all async operations
///
/// 6. **Color Pattern:**
///    - Use Theme.of(context).colorScheme for colors
///    - Use semantic colors: primary, secondary, error, surface
///    - Implement proper contrast with onPrimary, onSurface variants
///
/// 7. **Navigation Pattern:**
///    - Use push navigation instead of tab navigation
///    - Implement proper back button handling
///    - Use context.push for route navigation
///
/// **COPY-PASTE READY PATTERNS:**
class ReferencePatternGuide {
  // PATTERN 1: Standard screen structure
  static Widget buildScreenPattern(String title, Widget content) {
    return GHScreenTemplate(
      title: title,
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [content],
        ),
      ),
    );
  }

  // PATTERN 2: Section header with proper spacing
  static Widget buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(
        bottom: GHTokens.spacing16,
        top: GHTokens.spacing24,
      ),
      child: Text(title, style: GHTokens.titleLarge),
    );
  }

  // PATTERN 3: Content card with standard padding
  static Widget buildContentCard({
    required Widget child,
    VoidCallback? onTap,
    double? elevation,
  }) {
    return GHCard(
      onTap: onTap,
      elevation: elevation ?? GHTokens.elevation1,
      child: child,
    );
  }

  // PATTERN 4: Button row with proper spacing
  static Widget buildButtonRow(List<Widget> buttons) {
    return Row(
      children: buttons
          .expand(
            (button) => [
              Expanded(child: button),
              if (button != buttons.last)
                const SizedBox(width: GHTokens.spacing12),
            ],
          )
          .toList(),
    );
  }

  // PATTERN 5: Loading state wrapper
  static Widget buildLoadingWrapper({
    required bool isLoading,
    required Widget child,
    String? loadingMessage,
  }) {
    if (isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const GHLoadingIndicator(),
            if (loadingMessage != null) ...[
              const SizedBox(height: GHTokens.spacing16),
              Text(
                loadingMessage,
                style: GHTokens.bodyMedium,
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
      );
    }
    return child;
  }

  // PATTERN 6: Empty state wrapper
  static Widget buildEmptyStateWrapper({
    required bool isEmpty,
    required Widget child,
    required String emptyTitle,
    required String emptyMessage,
    String? emptyActionLabel,
    VoidCallback? emptyActionCallback,
  }) {
    if (isEmpty) {
      return Center(
        child: GHEmptyState(
          icon: Icons.inbox_outlined,
          title: emptyTitle,
          subtitle: emptyMessage,
        ),
      );
    }
    return child;
  }

  // PATTERN 7: Error state wrapper
  static Widget buildErrorStateWrapper({
    required bool hasError,
    required Widget child,
    required String errorTitle,
    required String errorMessage,
    required VoidCallback onRetry,
  }) {
    if (hasError) {
      return Center(
        child: GHErrorState(
          title: errorTitle,
          message: errorMessage,
          onRetry: onRetry,
        ),
      );
    }
    return child;
  }

  // PATTERN 8: Complete state management wrapper
  static Widget buildStateWrapper({
    required bool isLoading,
    required bool isEmpty,
    required bool hasError,
    required Widget child,
    String? loadingMessage,
    required String emptyTitle,
    required String emptyMessage,
    String? emptyActionLabel,
    VoidCallback? emptyActionCallback,
    required String errorTitle,
    required String errorMessage,
    required VoidCallback onRetry,
  }) {
    return buildLoadingWrapper(
      isLoading: isLoading,
      loadingMessage: loadingMessage,
      child: buildErrorStateWrapper(
        hasError: hasError,
        errorTitle: errorTitle,
        errorMessage: errorMessage,
        onRetry: onRetry,
        child: buildEmptyStateWrapper(
          isEmpty: isEmpty,
          emptyTitle: emptyTitle,
          emptyMessage: emptyMessage,
          emptyActionLabel: emptyActionLabel,
          emptyActionCallback: emptyActionCallback,
          child: child,
        ),
      ),
    );
  }

  // PATTERN 9: Interactive list item
  static Widget buildInteractiveListItem({
    required String title,
    String? subtitle,
    IconData? leadingIcon,
    Widget? trailing,
    required VoidCallback onTap,
  }) {
    return GHCard(
      onTap: onTap,
      child: Row(
        children: [
          if (leadingIcon != null) ...[
            Icon(
              leadingIcon,
              size: GHTokens.iconSize24,
              color: GHTokens.primary,
            ),
            const SizedBox(width: GHTokens.spacing12),
          ],
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: GHTokens.titleMedium),
                if (subtitle != null) ...[
                  const SizedBox(height: GHTokens.spacing4),
                  Text(subtitle, style: GHTokens.bodyMedium),
                ],
              ],
            ),
          ),
          if (trailing != null) ...[
            const SizedBox(width: GHTokens.spacing12),
            trailing,
          ],
        ],
      ),
    );
  }

  // PATTERN 10: Form field with proper spacing
  static Widget buildFormField(
    BuildContext context, {
    required String label,
    required Widget field,
    String? helpText,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: GHTokens.labelLarge),
        const SizedBox(height: GHTokens.spacing8),
        field,
        if (helpText != null) ...[
          const SizedBox(height: GHTokens.spacing4),
          Text(
            helpText,
            style: GHTokens.bodySmall.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
        const SizedBox(height: GHTokens.spacing16),
      ],
    );
  }
}

/// Reference Patterns Guide Screen - Shows implementation patterns and examples
class ReferencePatternsGuide extends StatelessWidget {
  const ReferencePatternsGuide({super.key});

  @override
  Widget build(BuildContext context) {
    return const ReferenceExampleScreen();
  }
}

/// **EXAMPLE USAGE SCREEN** - How to implement patterns in practice
class ReferenceExampleScreen extends StatefulWidget {
  const ReferenceExampleScreen({super.key});

  @override
  State<ReferenceExampleScreen> createState() => _ReferenceExampleScreenState();
}

class _ReferenceExampleScreenState extends State<ReferenceExampleScreen> {
  bool _isLoading = false;
  bool _hasError = false;
  bool _isEmpty = false;
  List<String> _items = ['Item 1', 'Item 2', 'Item 3'];

  void _simulateLoading() async {
    setState(() {
      _isLoading = true;
      _hasError = false;
    });

    await Future.delayed(const Duration(seconds: 2));

    setState(() {
      _isLoading = false;
    });
  }

  void _simulateError() {
    setState(() {
      _hasError = true;
      _isLoading = false;
    });
  }

  void _simulateEmpty() {
    setState(() {
      _isEmpty = true;
      _hasError = false;
      _isLoading = false;
      _items.clear();
    });
  }

  void _resetState() {
    setState(() {
      _isLoading = false;
      _hasError = false;
      _isEmpty = false;
      _items = ['Item 1', 'Item 2', 'Item 3'];
    });
  }

  @override
  Widget build(BuildContext context) {
    // REFERENCE PATTERN: Complete screen with state management
    return ReferencePatternGuide.buildScreenPattern(
      'Reference Implementation Example',
      ReferencePatternGuide.buildStateWrapper(
        isLoading: _isLoading,
        isEmpty: _isEmpty,
        hasError: _hasError,
        loadingMessage: 'Loading data...',
        emptyTitle: 'No Items Found',
        emptyMessage: 'Try adding some items to see them here.',
        emptyActionLabel: null,
        emptyActionCallback: null,
        errorTitle: 'Something Went Wrong',
        errorMessage: 'Unable to load data. Please try again.',
        onRetry: _simulateLoading,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // REFERENCE PATTERN: Action buttons section
            ReferencePatternGuide.buildSectionHeader('State Controls'),
            ReferencePatternGuide.buildButtonRow([
              GHButton(
                label: 'Loading',
                onPressed: _simulateLoading,
                style: GHButtonStyle.primary,
              ),
              GHButton(
                label: 'Error',
                onPressed: _simulateError,
                style: GHButtonStyle.secondary,
              ),
              GHButton(
                label: 'Empty',
                onPressed: _simulateEmpty,
                style: GHButtonStyle.secondary,
              ),
              GHButton(
                label: 'Reset',
                onPressed: _resetState,
                style: GHButtonStyle.secondary,
              ),
            ]),

            // REFERENCE PATTERN: Content section
            ReferencePatternGuide.buildSectionHeader('Content Items'),
            ...(_items.map(
              (item) => Padding(
                padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
                child: ReferencePatternGuide.buildInteractiveListItem(
                  title: item,
                  subtitle: 'This is a sample item description',
                  leadingIcon: Icons.star,
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    ScaffoldMessenger.of(
                      context,
                    ).showSnackBar(SnackBar(content: Text('Tapped $item')));
                  },
                ),
              ),
            )),

            const SizedBox(height: GHTokens.spacing32),
          ],
        ),
      ),
    );
  }
}
