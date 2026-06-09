import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../examples/home_screen_example.dart';
import '../examples/user_profile_example.dart';
import '../examples/repository_details_example.dart';
import '../examples/repository_tree_example.dart';
import '../examples/repository_file_example.dart';
import '../examples/issues_list_example.dart';
import '../examples/issue_detail_example.dart';
import '../examples/pulls_list_example.dart';
import '../examples/search_example.dart';
import '../examples/trending_example.dart';
import '../examples/user_repositories_screen.dart';
import '../examples/user_starred_screen.dart';
import '../examples/user_organizations_screen.dart';
import '../examples/uat_home_screen.dart';
import '../examples/design_tokens_screen.dart';
import '../examples/component_catalog_screen.dart';
import '../examples/interactive_examples_screen.dart';
import '../examples/interactive_component_demo_screen.dart';
import '../examples/documentation_screen.dart';
import '../examples/reference_patterns_guide.dart';
import '../examples/developer_guide_screen.dart';
import '../docs/stakeholder_presentation_guide.dart';
import '../docs/ui_system_impact_summary.dart';
import '../tools/comparison/navigation_comparison_screen.dart';
// import '../tools/comparison/spacing_comparison_screen.dart'; // Temporarily disabled
import '../tools/comparison/component_showcase_comparison_screen.dart';
import '../tools/measurement_validation_screen.dart';
import '../tools/standards_compliance_screen.dart';
import '../tools/demo_readiness_checklist.dart';
import 'example_routes.dart';
import 'ui_system_app.dart';

/// Navigation service for the UI system example screens
class NavigationService {
  static final GoRouter router = GoRouter(
    initialLocation: '/',
    routes: [
      // UAT Home Screen (main entry point)
      GoRoute(path: '/', builder: (context, state) => _UATHomeWrapper()),

      // Design System Showcase Routes
      GoRoute(
        path: '/tokens',
        builder: (context, state) => const DesignTokensScreen(),
      ),
      GoRoute(
        path: '/components',
        builder: (context, state) => const ComponentCatalogScreen(),
      ),
      GoRoute(
        path: '/interactive',
        builder: (context, state) => const InteractiveExamplesScreen(),
      ),
      GoRoute(
        path: '/interactive-demo',
        builder: (context, state) => const InteractiveComponentDemoScreen(),
      ),

      // Comparison Routes (updated paths to match UATHomeScreen)
      GoRoute(
        path: '/tools/comparison/navigation',
        builder: (context, state) => const NavigationComparisonScreen(),
      ),
      // GoRoute(
      //   path: '/tools/comparison/spacing',
      //   builder: (context, state) => const SpacingComparisonScreen(),
      // ), // Temporarily disabled
      GoRoute(
        path: '/tools/comparison/components',
        builder: (context, state) => const ComponentShowcaseComparisonScreen(),
      ),

      // Developer Tools Routes
      GoRoute(
        path: '/tools/measurement',
        builder: (context, state) => const MeasurementValidationScreen(),
      ),
      GoRoute(
        path: '/tools/compliance',
        builder: (context, state) => const StandardsComplianceScreen(),
      ),
      GoRoute(
        path: '/tools/demo-checklist',
        builder: (context, state) => const DemoReadinessChecklist(),
      ),

      // Documentation Routes
      GoRoute(
        path: '/documentation',
        builder: (context, state) => const DocumentationScreen(),
      ),
      GoRoute(
        path: '/reference',
        builder: (context, state) => const ReferencePatternsGuide(),
      ),
      GoRoute(
        path: '/developer-guide',
        builder: (context, state) => const DeveloperGuideScreen(),
      ),
      GoRoute(
        path: '/stakeholder-guide',
        builder: (context, state) => const StakeholderPresentationGuide(),
      ),
      GoRoute(
        path: '/impact-summary',
        builder: (context, state) => const UISystemImpactSummary(),
      ),

      // Example Screens Routes
      GoRoute(
        path: ExampleRoutes.home,
        builder: (context, state) => const HomeScreenExample(),
      ),
      GoRoute(
        path: ExampleRoutes.userProfile,
        builder: (context, state) {
          final username = state.pathParameters['username']!;
          return UserProfileExample(username: username);
        },
      ),
      GoRoute(
        path: ExampleRoutes.repository,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          return RepositoryDetailsExample(owner: owner, name: name);
        },
      ),
      GoRoute(
        path: ExampleRoutes.repositoryTree,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          final path = state.uri.queryParameters['path'];
          return RepositoryTreeExample(owner: owner, name: name, path: path);
        },
      ),
      GoRoute(
        path: ExampleRoutes.repositoryFile,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          final filePath = state.uri.queryParameters['path'] ?? 'README.md';
          return RepositoryFileExample(
            owner: owner,
            name: name,
            filePath: filePath,
          );
        },
      ),
      GoRoute(
        path: ExampleRoutes.issues,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          return IssuesListExample(owner: owner, name: name);
        },
      ),
      GoRoute(
        path: ExampleRoutes.issueDetail,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          final number = int.parse(state.pathParameters['number']!);
          return IssueDetailExample(owner: owner, name: name, number: number);
        },
      ),
      GoRoute(
        path: ExampleRoutes.pulls,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          return PullsListExample(owner: owner, name: name);
        },
      ),
      GoRoute(
        path: ExampleRoutes.pullDetail,
        builder: (context, state) {
          final owner = state.pathParameters['owner']!;
          final name = state.pathParameters['name']!;
          final number = state.pathParameters['number']!;
          return _buildPlaceholderScreen('Pull Request #$number: $owner/$name');
        },
      ),
      GoRoute(
        path: ExampleRoutes.search,
        builder: (context, state) {
          final query = state.uri.queryParameters['q'];
          return SearchExample(initialQuery: query);
        },
      ),
      GoRoute(
        path: ExampleRoutes.trending,
        builder: (context, state) => const TrendingExample(),
      ),
      GoRoute(
        path: ExampleRoutes.starred,
        builder: (context, state) => _buildPlaceholderScreen('Starred'),
      ),
      GoRoute(
        path: ExampleRoutes.userRepositories,
        builder: (context, state) {
          final username = state.pathParameters['username']!;
          return UserRepositoriesScreen(username: username);
        },
      ),
      GoRoute(
        path: ExampleRoutes.userStarred,
        builder: (context, state) {
          final username = state.pathParameters['username']!;
          return UserStarredScreen(username: username);
        },
      ),
      GoRoute(
        path: ExampleRoutes.userOrganizations,
        builder: (context, state) {
          final username = state.pathParameters['username']!;
          return UserOrganizationsScreen(username: username);
        },
      ),
    ],
  );

  /// Navigation helper methods - Using push navigation
  static void navigateToUser(String username) {
    router.push(ExampleRoutes.userProfilePath(username));
  }

  static void navigateToRepository(String owner, String name) {
    router.push(ExampleRoutes.repositoryPath(owner, name));
  }

  static void navigateToRepositoryTree(
    String owner,
    String name, {
    String? path,
  }) {
    router.push(ExampleRoutes.repositoryTreePath(owner, name, path: path));
  }

  static void navigateToRepositoryFile(
    String owner,
    String name, {
    String? filePath,
  }) {
    router.push(
      ExampleRoutes.repositoryFilePath(owner, name, filePath: filePath),
    );
  }

  static void navigateToIssues(String owner, String name) {
    router.push(ExampleRoutes.issuesPath(owner, name));
  }

  static void navigateToIssue(String owner, String name, int number) {
    router.push(ExampleRoutes.issueDetailPath(owner, name, number));
  }

  static void navigateToPulls(String owner, String name) {
    router.push(ExampleRoutes.pullsPath(owner, name));
  }

  static void navigateToPull(String owner, String name, int number) {
    router.push(ExampleRoutes.pullDetailPath(owner, name, number));
  }

  static void navigateToSearch({String? query}) {
    if (query != null && query.isNotEmpty) {
      router.push(
        '${ExampleRoutes.search}?q=${Uri.encodeQueryComponent(query)}',
      );
    } else {
      router.push(ExampleRoutes.search);
    }
  }

  static void navigateToTrending() {
    router.push(ExampleRoutes.trending);
  }

  static void navigateToStarred() {
    router.push(ExampleRoutes.starred);
  }

  static void navigateToUserRepositories(String username) {
    router.push(ExampleRoutes.userRepositoriesPath(username));
  }

  static void navigateToUserStarred(String username) {
    router.push(ExampleRoutes.userStarredPath(username));
  }

  static void navigateToUserOrganizations(String username) {
    router.push(ExampleRoutes.userOrganizationsPath(username));
  }

  /// Navigate back
  static void navigateBack() {
    if (router.canPop()) {
      router.pop();
    }
  }

  /// Check if can navigate back
  static bool canNavigateBack() {
    return router.canPop();
  }

  /// Build placeholder screen for routes not yet implemented
  static Widget _buildPlaceholderScreen(String title) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.construction, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text(
              title,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              'This screen is under construction',
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}

/// Theme-aware wrapper for UAT Home Screen
class _UATHomeWrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeProvider = ThemeProvider.of(context);
    return UATHomeScreen(onThemeToggle: themeProvider.onThemeToggle);
  }
}
