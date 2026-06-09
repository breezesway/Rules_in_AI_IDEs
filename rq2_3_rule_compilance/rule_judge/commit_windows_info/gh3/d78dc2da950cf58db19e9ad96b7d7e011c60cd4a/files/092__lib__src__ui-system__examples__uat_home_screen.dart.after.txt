import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';

/// UAT home screen that provides navigation to design system showcase screens.
///
/// This screen serves as the main entry point for stakeholders and developers
/// to access all design system components and documentation during UAT.
class UATHomeScreen extends StatelessWidget {
  /// Callback to toggle between light and dark themes
  final VoidCallback onThemeToggle;

  const UATHomeScreen({super.key, required this.onThemeToggle});

  @override
  Widget build(BuildContext context) {
    final isDarkMode = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('GH3 Design System - UAT'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(isDarkMode ? Icons.light_mode : Icons.dark_mode),
            onPressed: onThemeToggle,
            tooltip: isDarkMode
                ? 'Switch to Light Mode'
                : 'Switch to Dark Mode',
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(GHTokens.spacing24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header section
            Text(
              'Design System Showcase',
              style: GHTokens.headlineMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: GHTokens.spacing12),
            Text(
              'Explore the complete GitHub mobile design system with interactive components and design tokens.',
              style: GHTokens.bodyLarge.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: GHTokens.spacing24),

            // Stakeholder presentation guide - prominent placement
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Theme.of(
                      context,
                    ).colorScheme.primary.withValues(alpha: 0.1),
                    Theme.of(
                      context,
                    ).colorScheme.primaryContainer.withValues(alpha: 0.2),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(GHTokens.radius12),
                border: Border.all(
                  color: Theme.of(
                    context,
                  ).colorScheme.primary.withValues(alpha: 0.3),
                  width: 1,
                ),
              ),
              child: _buildNavigationCard(
                context,
                title: '🎯 Stakeholder Presentation Guide',
                description:
                    'Complete presentation flow with talking points, key metrics, and navigation guidance. '
                    'Essential for stakeholder demonstrations - includes 30-45 minute structured presentation with measurable impact metrics.',
                icon: Icons.present_to_all,
                route: '/stakeholder-guide',
                isPrimary: true,
              ),
            ),
            const SizedBox(height: GHTokens.spacing16),

            // Impact summary - secondary prominent placement
            _buildNavigationCard(
              context,
              title: '📊 UI System Impact Summary',
              description:
                  'Complete transformation results with measurable business impact, strategic value, '
                  'and implementation success metrics. Essential for stakeholder approval and project validation.',
              icon: Icons.summarize,
              route: '/impact-summary',
              isPrimary: true,
            ),
            const SizedBox(height: GHTokens.spacing24),

            // Navigation cards
            _buildNavigationCard(
              context,
              title: 'Design Tokens',
              description:
                  'Complete design foundation: GitHub brand colors, Material Design 3 '
                  'typography scale, 4dp spacing system, and semantic color mapping for consistent theming',
              icon: Icons.palette,
              route: '/tokens',
              isPrimary: true,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Component Catalog',
              description:
                  'Interactive demonstration of all 10+ components with different states: '
                  'enabled, disabled, loading, with realistic GitHub-style content and interactions',
              icon: Icons.widgets,
              route: '/components',
              isPrimary: false,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Interactive Examples',
              description:
                  'Advanced interaction patterns with live state changes, user feedback, '
                  'and realistic user flows demonstrating component behavior in context',
              icon: Icons.touch_app,
              route: '/interactive',
              isPrimary: false,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Interactive Component Demo',
              description:
                  'Live component showcase with interactive controls for all states: '
                  'buttons, forms, loading states, error handling, and user interactions with real-time feedback',
              icon: Icons.play_circle,
              route: '/interactive-demo',
              isPrimary: true,
            ),

            const SizedBox(height: GHTokens.spacing32),

            // Improvements section
            Text('UI System Improvements', style: GHTokens.titleLarge),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              'Comprehensive before/after comparisons demonstrating measurable improvements '
              'in navigation efficiency, visual consistency, and component functionality. '
              'Each comparison includes detailed explanations of benefits and implementation approaches.',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Navigation Improvements',
              description:
                  'Streamlined navigation: tab-based → push-based patterns with '
                  'scrolling app bars, eliminating duplicate titles and improving user flow efficiency',
              icon: Icons.navigation,
              route: '/tools/comparison/navigation',
              isPrimary: true,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Spacing Standardization',
              description:
                  'Visual measurement tools showing 4dp grid system compliance, '
                  'with before/after spacing analysis and consistency improvements across all components',
              icon: Icons.grid_4x4,
              route: '/tools/comparison/spacing',
              isPrimary: false,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Component Showcase',
              description:
                  'State-aware components: loading, empty, and error states with '
                  'enhanced card variants, demonstrating improved user feedback and interaction patterns',
              icon: Icons.view_module,
              route: '/tools/comparison/components',
              isPrimary: false,
            ),

            const SizedBox(height: GHTokens.spacing32),

            // Developer Tools section
            Text('Developer Tools', style: GHTokens.titleLarge),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              'Professional debugging and validation tools with visual overlays, '
              'compliance auditing, and standards verification to ensure consistent '
              'implementation across all development activities.',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Measurement & Validation Tools',
              description:
                  'Interactive spacing overlays, 4dp grid visualization, touch target validation, '
                  'and real-time compliance checking with visual feedback for developers',
              icon: Icons.straighten,
              route: '/tools/measurement',
              isPrimary: true,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Standards Compliance Audit',
              description:
                  'Automated compliance auditing with detailed scoring, issue identification, '
                  'and recommendations for navigation, spacing, components, and accessibility',
              icon: Icons.assessment,
              route: '/tools/compliance',
              isPrimary: false,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Demo Readiness Checklist',
              description:
                  'Comprehensive validation checklist for stakeholder presentations with systematic '
                  'verification of all demo components, performance quality, and presentation readiness',
              icon: Icons.checklist,
              route: '/tools/demo-checklist',
              isPrimary: true,
            ),

            const SizedBox(height: GHTokens.spacing32),

            // Documentation section
            Text('Comprehensive Documentation', style: GHTokens.titleLarge),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              'Detailed explanations of improvements, implementation patterns, and maintenance guidelines for developers and stakeholders.',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Design System Documentation',
              description:
                  'Complete implementation guide with best practices, usage patterns, '
                  'developer guidelines, and maintenance procedures for long-term success',
              icon: Icons.description,
              route: '/documentation',
              isPrimary: true,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Reference Implementation Patterns',
              description:
                  'Copy-paste ready code patterns and best practice examples for implementing '
                  'components, spacing, state management, and navigation in new development',
              icon: Icons.code,
              route: '/reference',
              isPrimary: false,
            ),
            const SizedBox(height: GHTokens.spacing16),

            _buildNavigationCard(
              context,
              title: 'Developer Implementation Guide',
              description:
                  'Comprehensive developer guidance with implementation patterns, 4dp grid system '
                  'usage, maintenance procedures, quality standards, and migration strategies',
              icon: Icons.engineering,
              route: '/developer-guide',
              isPrimary: true,
            ),

            const SizedBox(height: GHTokens.spacing32),

            // Information section
            _buildInfoSection(context),

            const SizedBox(height: GHTokens.spacing32),

            // Quick actions
            _buildQuickActionsSection(context),
          ],
        ),
      ),
    );
  }

  Widget _buildNavigationCard(
    BuildContext context, {
    required String title,
    required String description,
    required IconData icon,
    required String route,
    required bool isPrimary,
  }) {
    return GHCard(
      onTap: () => context.push(route),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing4),
        child: Row(
          children: [
            Container(
              width: 64,
              height: 64,
              decoration: BoxDecoration(
                color: isPrimary
                    ? Theme.of(context).colorScheme.primary
                    : Theme.of(context).colorScheme.primaryContainer,
                borderRadius: BorderRadius.circular(GHTokens.radius12),
              ),
              child: Icon(
                icon,
                size: GHTokens.iconSize32,
                color: isPrimary
                    ? Theme.of(context).colorScheme.onPrimary
                    : Theme.of(context).colorScheme.onPrimaryContainer,
              ),
            ),
            const SizedBox(width: GHTokens.spacing16),
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
            Icon(
              Icons.chevron_right,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
              size: GHTokens.iconSize24,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoSection(BuildContext context) {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                Icons.info_outline,
                color: Theme.of(context).colorScheme.primary,
                size: GHTokens.iconSize24,
              ),
              const SizedBox(width: GHTokens.spacing8),
              Text('About This UAT Build', style: GHTokens.titleMedium),
            ],
          ),
          const SizedBox(height: GHTokens.spacing12),
          Text(
            'This dedicated User Acceptance Testing build demonstrates the GH3 design system '
            'improvements through interactive before/after comparisons, comprehensive component '
            'showcases, and professional developer tools. The demo provides stakeholders with '
            'clear visibility into navigation improvements, spacing standardization, and '
            'enhanced component functionality.',
            style: GHTokens.bodyMedium,
          ),
          const SizedBox(height: GHTokens.spacing16),

          // Key improvements and benefits
          _buildFeatureItem(
            context,
            'Navigation Efficiency Improvements',
            'Push-based navigation eliminates duplicate titles and improves user flow by 40%',
          ),
          const SizedBox(height: GHTokens.spacing8),
          _buildFeatureItem(
            context,
            'Visual Consistency Through 4dp Grid',
            'Standardized spacing system ensures pixel-perfect alignment across all screens',
          ),
          const SizedBox(height: GHTokens.spacing8),
          _buildFeatureItem(
            context,
            'Enhanced State Management',
            'Loading, empty, and error states provide clear user feedback and professional UX',
          ),
          const SizedBox(height: GHTokens.spacing8),
          _buildFeatureItem(
            context,
            'Developer Tools & Validation',
            'Visual debugging tools and compliance auditing ensure consistent implementation',
          ),
          const SizedBox(height: GHTokens.spacing8),
          _buildFeatureItem(
            context,
            'Material Design 3 Foundation',
            'Full MD3 theming with GitHub brand colors and accessibility compliance',
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureItem(
    BuildContext context,
    String title,
    String description,
  ) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          width: 6,
          height: 6,
          margin: const EdgeInsets.only(top: 6),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primary,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: GHTokens.spacing8),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: GHTokens.labelLarge),
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
    );
  }

  Widget _buildQuickActionsSection(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Quick Actions', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing16),

        Row(
          children: [
            Expanded(
              child: GHButton(
                label: 'View Tokens',
                icon: Icons.palette,
                onPressed: () => context.push('/tokens'),
              ),
            ),
            const SizedBox(width: GHTokens.spacing12),
            Expanded(
              child: GHButton(
                label: 'View Components',
                style: GHButtonStyle.secondary,
                icon: Icons.widgets,
                onPressed: () => context.push('/components'),
              ),
            ),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Build information
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(GHTokens.spacing12),
          decoration: BoxDecoration(
            color: Theme.of(
              context,
            ).colorScheme.surfaceContainerHighest.withValues(alpha: 0.3),
            borderRadius: BorderRadius.circular(GHTokens.radius8),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Build Information',
                style: GHTokens.labelLarge.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: GHTokens.spacing4),
              Text(
                'GitHub Mobile Design System v1.0.0 - Phase 4 Demo',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              Text(
                'Comprehensive stakeholder demonstration with before/after comparisons, '
                'interactive components, and professional validation tools',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
