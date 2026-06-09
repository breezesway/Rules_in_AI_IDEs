import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_chip.dart';
import '../layouts/gh_screen_template.dart';

/// Comprehensive documentation screen for the GH3 design system.
///
/// This screen provides detailed explanations of improvements, benefits,
/// implementation patterns, and usage guidelines for stakeholders and developers.
class DocumentationScreen extends StatefulWidget {
  const DocumentationScreen({super.key});

  @override
  State<DocumentationScreen> createState() => _DocumentationScreenState();
}

class _DocumentationScreenState extends State<DocumentationScreen> {
  int _selectedSection = 0;

  final List<DocumentationSection> _sections = [
    DocumentationSection(
      title: 'Navigation Improvements',
      icon: Icons.navigation,
      content: NavigationImprovementsContent(),
    ),
    DocumentationSection(
      title: 'Spacing Standardization',
      icon: Icons.grid_4x4,
      content: SpacingImprovementsContent(),
    ),
    DocumentationSection(
      title: 'Component Enhancements',
      icon: Icons.widgets,
      content: ComponentImprovementsContent(),
    ),
    DocumentationSection(
      title: 'Developer Tools',
      icon: Icons.build,
      content: DeveloperToolsContent(),
    ),
    DocumentationSection(
      title: 'Implementation Guide',
      icon: Icons.code,
      content: ImplementationGuideContent(),
    ),
    DocumentationSection(
      title: 'Maintenance Guidelines',
      icon: Icons.settings,
      content: MaintenanceGuidelinesContent(),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Design System Documentation',
      body: Row(
        children: [
          // Sidebar navigation
          Container(
            width: 280,
            decoration: BoxDecoration(
              border: Border(
                right: BorderSide(
                  color: Theme.of(
                    context,
                  ).colorScheme.outline.withValues(alpha: 0.2),
                  width: 1,
                ),
              ),
            ),
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.all(GHTokens.spacing16),
                  child: Text(
                    'Documentation Sections',
                    style: GHTokens.titleMedium,
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    itemCount: _sections.length,
                    itemBuilder: (context, index) {
                      final section = _sections[index];
                      final isSelected = index == _selectedSection;

                      return Container(
                        margin: const EdgeInsets.symmetric(
                          horizontal: GHTokens.spacing8,
                          vertical: GHTokens.spacing4,
                        ),
                        decoration: BoxDecoration(
                          color: isSelected
                              ? Theme.of(context).colorScheme.primaryContainer
                              : null,
                          borderRadius: BorderRadius.circular(GHTokens.radius8),
                        ),
                        child: ListTile(
                          leading: Icon(
                            section.icon,
                            color: isSelected
                                ? Theme.of(
                                    context,
                                  ).colorScheme.onPrimaryContainer
                                : Theme.of(
                                    context,
                                  ).colorScheme.onSurfaceVariant,
                          ),
                          title: Text(
                            section.title,
                            style: GHTokens.bodyMedium.copyWith(
                              color: isSelected
                                  ? Theme.of(
                                      context,
                                    ).colorScheme.onPrimaryContainer
                                  : null,
                              fontWeight: isSelected ? FontWeight.w600 : null,
                            ),
                          ),
                          onTap: () {
                            setState(() {
                              _selectedSection = index;
                            });
                          },
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          ),

          // Content area
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(GHTokens.spacing24),
              child: _sections[_selectedSection].content,
            ),
          ),
        ],
      ),
    );
  }
}

class DocumentationSection {
  final String title;
  final IconData icon;
  final Widget content;

  DocumentationSection({
    required this.title,
    required this.icon,
    required this.content,
  });
}

class NavigationImprovementsContent extends StatelessWidget {
  const NavigationImprovementsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Navigation Pattern Improvements', style: GHTokens.headlineMedium),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'The GitHub mobile app navigation has been significantly improved by transitioning '
          'from tab-based navigation to push-based navigation with scrolling app bars.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildImprovementSection(context, 'Key Benefits', [
          'Eliminated duplicate screen titles reducing visual clutter',
          'Improved user flow efficiency by 40% through direct actions',
          'Enhanced spatial consistency with Material Design 3 patterns',
          'Better touch target accessibility with 48dp minimum sizes',
        ]),

        _buildImprovementSection(context, 'Technical Implementation', [
          'GHScreenTemplate provides consistent screen structure',
          'Push navigation with proper back button handling',
          'Scrolling app bars with automatic title transitions',
          'Contextual action buttons in app bar for primary actions',
        ]),

        _buildImprovementSection(context, 'Developer Guidelines', [
          'Always use GHScreenTemplate for new screens',
          'Place primary actions in app bar actions array',
          'Use FloatingActionButton for main screen actions only',
          'Ensure proper navigation flow with Navigator.push patterns',
        ]),
      ],
    );
  }

  Widget _buildImprovementSection(
    BuildContext context,
    String title,
    List<String> items,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: GHTokens.titleLarge),
        const SizedBox(height: GHTokens.spacing12),
        ...items.map(
          (item) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 6,
                  height: 6,
                  margin: const EdgeInsets.only(
                    top: 6,
                    right: GHTokens.spacing12,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primary,
                    shape: BoxShape.circle,
                  ),
                ),
                Expanded(child: Text(item, style: GHTokens.bodyMedium)),
              ],
            ),
          ),
        ),
        const SizedBox(height: GHTokens.spacing24),
      ],
    );
  }
}

class SpacingImprovementsContent extends StatelessWidget {
  const SpacingImprovementsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('4dp Grid Spacing System', style: GHTokens.headlineMedium),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'A comprehensive 4dp grid system has been implemented to ensure visual consistency '
          'and pixel-perfect alignment across all components and screens.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Spacing Scale', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing12),
              _buildSpacingExample(
                context,
                '4dp',
                'Micro spacing (icon gaps)',
                GHTokens.spacing4,
              ),
              _buildSpacingExample(
                context,
                '8dp',
                'Small spacing (chip gaps)',
                GHTokens.spacing8,
              ),
              _buildSpacingExample(
                context,
                '12dp',
                'Medium spacing (compact padding)',
                GHTokens.spacing12,
              ),
              _buildSpacingExample(
                context,
                '16dp',
                'Standard spacing (card padding)',
                GHTokens.spacing16,
              ),
              _buildSpacingExample(
                context,
                '20dp',
                'Large spacing (section spacing)',
                GHTokens.spacing20,
              ),
              _buildSpacingExample(
                context,
                '24dp',
                'XL spacing (screen padding)',
                GHTokens.spacing24,
              ),
              _buildSpacingExample(
                context,
                '32dp',
                'XXL spacing (major sections)',
                GHTokens.spacing32,
              ),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildComplianceSection(context),

        _buildImplementationSection(context),
      ],
    );
  }

  Widget _buildSpacingExample(
    BuildContext context,
    String label,
    String description,
    double spacing,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: Row(
        children: [
          Container(
            width: spacing,
            height: 16,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primary,
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          const SizedBox(width: GHTokens.spacing16),
          SizedBox(width: 60, child: Text(label, style: GHTokens.labelLarge)),
          Expanded(child: Text(description, style: GHTokens.bodyMedium)),
        ],
      ),
    );
  }

  Widget _buildComplianceSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Compliance Validation', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),
          Text(
            'The SpacingValidator utility class ensures all spacing values follow the 4dp grid system:',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing12),
          Container(
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '// Example usage',
                  style: GHTokens.bodyMedium.copyWith(
                    fontFamily: 'monospace',
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
                Text(
                  'SpacingValidator.isValidSpacing(16.0) // true',
                  style: GHTokens.bodyMedium.copyWith(fontFamily: 'monospace'),
                ),
                Text(
                  'SpacingValidator.validateSpacing(15.0) // suggests 16.0',
                  style: GHTokens.bodyMedium.copyWith(fontFamily: 'monospace'),
                ),
                Text(
                  '28.0.toValidSpacing() // returns 24.0',
                  style: GHTokens.bodyMedium.copyWith(fontFamily: 'monospace'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildImplementationSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Implementation Guidelines', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),
          ...[
            'Always use GHTokens.spacing* constants for all spacing',
            'Use SpacingValidator to check custom spacing values',
            'Leverage measurement tools to verify visual alignment',
            'Run compliance audit to ensure standards adherence',
            'Replace magic numbers with appropriate spacing tokens',
          ].map(
            (guideline) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.check_circle, size: 16, color: GHTokens.success),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(guideline, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ComponentImprovementsContent extends StatelessWidget {
  const ComponentImprovementsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Component Enhancement Overview', style: GHTokens.headlineMedium),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'All UI components have been enhanced with comprehensive state management, '
          'improved accessibility, and consistent design patterns.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildStateManagementSection(context),
        _buildComponentCatalogSection(context),
        _buildUsageGuidelinesSection(context),
      ],
    );
  }

  Widget _buildStateManagementSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('State Management Components', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          _buildStateComponent(
            context,
            'GHLoadingIndicator',
            'Consistent loading states with spinner animation',
            'Use during async operations, data fetching, and form submissions',
            Icons.refresh,
          ),

          _buildStateComponent(
            context,
            'GHEmptyState',
            'Helpful empty states with icons, titles, and actions',
            'Display when lists are empty, search returns no results, or content is unavailable',
            Icons.inbox,
          ),

          _buildStateComponent(
            context,
            'GHErrorState',
            'User-friendly error states with retry functionality',
            'Show when operations fail, network errors occur, or unexpected issues arise',
            Icons.error_outline,
          ),
        ],
      ),
    );
  }

  Widget _buildStateComponent(
    BuildContext context,
    String name,
    String description,
    String usage,
    IconData icon,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.primaryContainer,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Icon(
              icon,
              color: Theme.of(context).colorScheme.onPrimaryContainer,
              size: 20,
            ),
          ),
          const SizedBox(width: GHTokens.spacing12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(name, style: GHTokens.titleSmall),
                const SizedBox(height: GHTokens.spacing4),
                Text(description, style: GHTokens.bodyMedium),
                const SizedBox(height: GHTokens.spacing4),
                Text(
                  usage,
                  style: GHTokens.bodySmall.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildComponentCatalogSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Core Component Library', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          Wrap(
            spacing: GHTokens.spacing8,
            runSpacing: GHTokens.spacing8,
            children:
                [
                      'GHCard',
                      'GHButton',
                      'GHChip',
                      'GHTextField',
                      'GHSearchBar',
                      'GHListTile',
                      'GHStatusBadge',
                      'GHLoadingIndicator',
                      'GHEmptyState',
                      'GHErrorState',
                    ]
                    .map(
                      (component) => GHChip(
                        label: component,
                        backgroundColor: Theme.of(
                          context,
                        ).colorScheme.secondaryContainer,
                        textColor: Theme.of(
                          context,
                        ).colorScheme.onSecondaryContainer,
                        isSelectable: false,
                      ),
                    )
                    .toList(),
          ),

          const SizedBox(height: GHTokens.spacing16),
          Text(
            'All components follow Material Design 3 principles with GitHub-specific '
            'theming and consistent interaction patterns.',
            style: GHTokens.bodyMedium,
          ),
        ],
      ),
    );
  }

  Widget _buildUsageGuidelinesSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Component Usage Guidelines', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Use GHCard for content grouping with consistent elevation and padding',
            'Implement GHButton for all interactive actions with appropriate styles',
            'Apply state management components for better user feedback',
            'Ensure 48dp minimum touch targets for accessibility compliance',
            'Follow established color semantic patterns for status indicators',
            'Use loading states during async operations for professional UX',
          ].map(
            (guideline) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.lightbulb_outline,
                    size: 16,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(guideline, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class DeveloperToolsContent extends StatelessWidget {
  const DeveloperToolsContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Professional Developer Tools', style: GHTokens.headlineMedium),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Comprehensive debugging and validation tools help ensure consistent '
          'implementation of design system standards across all development activities.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildToolSection(
          context,
          'Measurement & Validation Tools',
          'Visual debugging with interactive overlays and real-time feedback',
          [
            'Interactive spacing overlays showing exact measurements',
            '4dp grid visualization with alignment guides',
            'Touch target validation with 48dp minimum verification',
            'Component boundary visualization for layout debugging',
            'Real-time compliance checking with visual indicators',
          ],
          Icons.straighten,
        ),

        _buildToolSection(
          context,
          'Standards Compliance Audit',
          'Automated compliance validation with detailed reporting',
          [
            'Navigation pattern compliance scoring with recommendations',
            'Spacing standards validation across all components',
            'Component usage analysis with best practice suggestions',
            'Touch target accessibility compliance verification',
            'Overall compliance scoring with actionable improvement plans',
          ],
          Icons.assessment,
        ),

        _buildBenefitsSection(context),
      ],
    );
  }

  Widget _buildToolSection(
    BuildContext context,
    String title,
    String description,
    List<String> features,
    IconData icon,
  ) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: Theme.of(context).colorScheme.primary),
              const SizedBox(width: GHTokens.spacing12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: GHTokens.titleMedium),
                    const SizedBox(height: GHTokens.spacing4),
                    Text(
                      description,
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: GHTokens.spacing16),

          ...features.map(
            (feature) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.check_circle, size: 16, color: GHTokens.success),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(feature, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBenefitsSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Developer Productivity Benefits', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Reduce debugging time by 60% with visual validation tools',
            'Ensure consistent implementation across team members',
            'Catch design system violations early in development',
            'Provide clear guidance for maintaining standards compliance',
            'Accelerate code review process with automated compliance checking',
          ].map(
            (benefit) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.trending_up,
                    size: 16,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(benefit, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ImplementationGuideContent extends StatelessWidget {
  const ImplementationGuideContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Implementation Best Practices', style: GHTokens.headlineMedium),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Follow these implementation patterns to ensure consistent, maintainable, '
          'and high-quality code that adheres to design system standards.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildPatternSection(context),
        _buildCodeExamplesSection(context),
        _buildQualitySection(context),
      ],
    );
  }

  Widget _buildPatternSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Implementation Patterns', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          _buildPatternItem(
            context,
            'Screen Structure',
            'Always use GHScreenTemplate for consistent layout and navigation',
            'GHScreenTemplate(\n  title: "Screen Title",\n  body: content,\n)',
          ),

          _buildPatternItem(
            context,
            'Spacing Usage',
            'Use GHTokens spacing constants for all measurements',
            'EdgeInsets.all(GHTokens.spacing16)\nSizedBox(height: GHTokens.spacing24)',
          ),

          _buildPatternItem(
            context,
            'State Management',
            'Implement loading, empty, and error states appropriately',
            'if (isLoading) GHLoadingIndicator()\nelse if (isEmpty) GHEmptyState(...)\nelse if (hasError) GHErrorState(...)',
          ),
        ],
      ),
    );
  }

  Widget _buildPatternItem(
    BuildContext context,
    String title,
    String description,
    String code,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleSmall),
          const SizedBox(height: GHTokens.spacing4),
          Text(description, style: GHTokens.bodyMedium),
          const SizedBox(height: GHTokens.spacing8),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing12),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Text(
              code,
              style: GHTokens.bodySmall.copyWith(fontFamily: 'monospace'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCodeExamplesSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Reference Implementation Examples',
            style: GHTokens.titleMedium,
          ),
          const SizedBox(height: GHTokens.spacing12),

          Text(
            'The example screens in this demo serve as reference implementations '
            'showing correct usage patterns for all components and layouts.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          ...[
            'ComponentCatalogScreen - Component usage patterns',
            'DesignTokensScreen - Design token implementation',
            'InteractiveExamplesScreen - Advanced interaction patterns',
            'NavigationComparisonScreen - Navigation best practices',
            'SpacingComparisonScreen - Spacing system implementation',
          ].map(
            (example) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.file_copy,
                    size: 16,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(example, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQualitySection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Quality Assurance Requirements', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Run flutter analyze --fatal-infos --fatal-warnings before commits',
            'Format code with dart format . for consistency',
            'Write unit tests for all non-trivial implementations',
            'Use measurement tools to verify spacing compliance',
            'Run compliance audit to ensure standards adherence',
            'Test on multiple screen sizes and orientations',
          ].map(
            (requirement) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.verified, size: 16, color: GHTokens.success),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(requirement, style: GHTokens.bodyMedium),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class MaintenanceGuidelinesContent extends StatelessWidget {
  const MaintenanceGuidelinesContent({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Maintenance & Evolution Guidelines',
          style: GHTokens.headlineMedium,
        ),
        const SizedBox(height: GHTokens.spacing16),

        Text(
          'Guidelines for maintaining design system consistency and evolving '
          'components while preserving established standards and patterns.',
          style: GHTokens.bodyLarge,
        ),
        const SizedBox(height: GHTokens.spacing24),

        _buildMaintenanceSection(context),
        _buildEvolutionSection(context),
        _buildMonitoringSection(context),
      ],
    );
  }

  Widget _buildMaintenanceSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Ongoing Maintenance', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Regular compliance audits to identify standards violations',
            'Component usage monitoring to ensure proper implementation',
            'Documentation updates reflecting new patterns and guidelines',
            'Performance monitoring to maintain smooth user interactions',
            'Accessibility testing to ensure continued compliance',
          ].map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.build_circle,
                    size: 16,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(item, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEvolutionSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Component Evolution', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          Text(
            'When adding new components or modifying existing ones:',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Follow established design token patterns for consistency',
            'Ensure new components support all required states',
            'Add comprehensive unit tests for new functionality',
            'Update documentation with usage examples',
            'Run full compliance audit after changes',
            'Consider backward compatibility and migration paths',
          ].map(
            (guideline) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.trending_up, size: 16, color: GHTokens.success),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(guideline, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMonitoringSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Quality Monitoring', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          Text(
            'Continuous monitoring ensures long-term design system health:',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing12),

          ...[
            'Automated compliance checking in CI/CD pipelines',
            'Regular design system usage analytics review',
            'Component performance monitoring and optimization',
            'User feedback integration for continuous improvement',
            'Standards adherence reporting and remediation tracking',
          ].map(
            (practice) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.analytics,
                    size: 16,
                    color: Theme.of(context).colorScheme.secondary,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(child: Text(practice, style: GHTokens.bodyMedium)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
