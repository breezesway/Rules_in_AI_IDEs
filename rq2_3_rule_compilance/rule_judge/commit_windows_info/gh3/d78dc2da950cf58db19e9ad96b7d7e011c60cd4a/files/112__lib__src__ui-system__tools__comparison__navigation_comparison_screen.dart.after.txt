import 'package:flutter/material.dart';
import '../../tokens/gh_tokens.dart';
import '../../components/gh_card.dart';
import '../../widgets/gh_navigation_grid.dart';
import 'comparison_screen.dart';
import 'mock_screen.dart';

/// A comparison screen showing navigation improvements.
///
/// This screen demonstrates the transition from tab-based navigation
/// to action-based push navigation with scrolling app bars.
class NavigationComparisonScreen extends StatelessWidget {
  const NavigationComparisonScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ComparisonScreen(
      title: 'Navigation Improvements',
      beforeDescription:
          'Tab-based navigation with duplicate titles and limited scalability',
      afterDescription:
          'Action-based push navigation with scrolling app bar and improved user experience',
      highlights: const [
        ImprovementHighlight(
          description: 'Eliminated tab navigation in favor of action lists',
        ),
        ImprovementHighlight(
          description: 'Implemented Material Design scrolling app bar',
        ),
        ImprovementHighlight(description: 'Removed duplicate title display'),
        ImprovementHighlight(
          description: 'Consistent push navigation throughout app',
        ),
        ImprovementHighlight(
          description: 'Better scalability for adding new sections',
        ),
      ],
      beforeWidget: _buildTabBasedProfile(context),
      afterWidget: _buildActionBasedProfile(context),
    );
  }

  Widget _buildTabBasedProfile(BuildContext context) {
    return MockScreen(
      title: 'The Octocat',
      showBackButton: false,
      body: SingleChildScrollView(
        child: Column(
          children: [
            /// User card with title (old way - title appears twice)
            const MockUserCard(showTitle: true),

            const SizedBox(height: GHTokens.spacing16),

            /// Tab bar (the old way)
            Container(
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainer,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: MockTab(
                      label: 'Repositories',
                      isActive: true,
                      badge: '45',
                    ),
                  ),
                  Expanded(
                    child: MockTab(label: 'Starred', badge: '234'),
                  ),
                  Expanded(
                    child: MockTab(label: 'Organizations', badge: '3'),
                  ),
                ],
              ),
            ),

            const SizedBox(height: GHTokens.spacing16),

            /// Mock content area
            SizedBox(
              height: 200,
              child: GHCard(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.folder,
                        size: 48,
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                      const SizedBox(height: GHTokens.spacing12),
                      Text(
                        'Repository content would appear here',
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(height: GHTokens.spacing8),
                      Text(
                        'Tab content is limited to this area',
                        style: GHTokens.labelMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionBasedProfile(BuildContext context) {
    return MockScreen(
      title: 'The Octocat',
      backgroundColor: Theme.of(context).colorScheme.surface,
      body: CustomScrollView(
        slivers: [
          /// User card without title (new way - no duplicate)
          SliverToBoxAdapter(
            child: Column(
              children: [
                const MockUserCard(showTitle: false),
                const SizedBox(height: GHTokens.spacing20),

                /// Action grid (new way)
                GHNavigationGrid.twoByThree(
                  items: [
                    GHNavigationItem(
                      icon: Icons.folder,
                      title: 'Repositories',
                      description: 'Browse code',
                      count: '45',
                      onTap: () {},
                    ),
                    GHNavigationItem(
                      icon: Icons.star,
                      title: 'Starred',
                      description: 'Starred repos',
                      count: '234',
                      onTap: () {},
                    ),
                    GHNavigationItem(
                      icon: Icons.people,
                      title: 'Organizations',
                      description: 'Member of',
                      count: '3',
                      onTap: () {},
                    ),
                    GHNavigationItem(
                      icon: Icons.work,
                      title: 'Projects',
                      description: 'View projects',
                      onTap: () {},
                    ),
                    GHNavigationItem(
                      icon: Icons.article,
                      title: 'Gists',
                      description: 'Code snippets',
                      onTap: () {},
                    ),
                    GHNavigationItem(
                      icon: Icons.settings,
                      title: 'Settings',
                      description: 'Account settings',
                      onTap: () {},
                    ),
                  ],
                ),

                const SizedBox(height: GHTokens.spacing20),

                /// Benefits explanation
                GHCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.lightbulb,
                            color: GHTokens.success,
                            size: 20,
                          ),
                          const SizedBox(width: GHTokens.spacing8),
                          Text(
                            'Navigation Benefits',
                            style: GHTokens.titleMedium.copyWith(
                              color: GHTokens.success,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: GHTokens.spacing12),

                      _buildBenefit(
                        context,
                        Icons.touch_app,
                        'Push Navigation',
                        'Each action opens a dedicated screen with full-screen content',
                      ),

                      _buildBenefit(
                        context,
                        Icons.expand_more,
                        'Scrolling App Bar',
                        'App bar title appears/disappears based on scroll position',
                      ),

                      _buildBenefit(
                        context,
                        Icons.grid_view,
                        'Scalable Grid',
                        'Easy to add new navigation options without redesigning',
                      ),

                      _buildBenefit(
                        context,
                        Icons.mobile_friendly,
                        'Mobile Optimized',
                        'Better use of screen real estate on mobile devices',
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBenefit(
    BuildContext context,
    IconData icon,
    String title,
    String description,
  ) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 16, color: Theme.of(context).colorScheme.primary),
          const SizedBox(width: GHTokens.spacing8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: GHTokens.labelLarge.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: GHTokens.spacing4),
                Text(
                  description,
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
}
