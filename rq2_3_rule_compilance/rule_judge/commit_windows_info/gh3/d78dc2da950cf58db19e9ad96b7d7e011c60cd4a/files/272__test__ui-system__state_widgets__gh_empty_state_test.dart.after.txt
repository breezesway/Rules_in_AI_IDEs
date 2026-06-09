import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/state_widgets/gh_empty_state.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHEmptyState', () {
    testWidgets('should display icon, title, and subtitle', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              subtitle: 'Test Subtitle',
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.folder_outlined), findsOneWidget);
      expect(find.text('Test Title'), findsOneWidget);
      expect(find.text('Test Subtitle'), findsOneWidget);
    });

    testWidgets('should display without subtitle when not provided', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.folder_outlined), findsOneWidget);
      expect(find.text('Test Title'), findsOneWidget);
    });

    testWidgets('should display action button when provided', (tester) async {
      bool actionPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              action: ElevatedButton(
                onPressed: () => actionPressed = true,
                child: const Text('Test Action'),
              ),
            ),
          ),
        ),
      );

      expect(find.text('Test Action'), findsOneWidget);

      await tester.tap(find.text('Test Action'));
      expect(actionPressed, isTrue);
    });

    testWidgets('should use custom icon size and color', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              iconSize: 100.0,
              iconColor: Colors.red,
            ),
          ),
        ),
      );

      final iconWidget = tester.widget<Icon>(
        find.byIcon(Icons.folder_outlined),
      );
      expect(iconWidget.size, equals(100.0));
      expect(iconWidget.color, equals(Colors.red));
    });

    testWidgets('should use custom text styles', (tester) async {
      const customTitleStyle = TextStyle(fontSize: 30, color: Colors.blue);
      const customSubtitleStyle = TextStyle(fontSize: 18, color: Colors.green);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              subtitle: 'Test Subtitle',
              titleStyle: customTitleStyle,
              subtitleStyle: customSubtitleStyle,
            ),
          ),
        ),
      );

      final titleText = tester.widget<Text>(find.text('Test Title'));
      final subtitleText = tester.widget<Text>(find.text('Test Subtitle'));

      expect(titleText.style?.fontSize, equals(30));
      expect(titleText.style?.color, equals(Colors.blue));
      expect(subtitleText.style?.fontSize, equals(18));
      expect(subtitleText.style?.color, equals(Colors.green));
    });

    testWidgets('should not center content when centered is false', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              centered: false,
            ),
          ),
        ),
      );

      // When not centered, there should be no Center widget wrapping the content
      final paddingWidget = find.byType(Padding);
      expect(paddingWidget, findsOneWidget);

      final padding = tester.widget<Padding>(paddingWidget);
      expect(padding.child, isA<Column>());
    });

    testWidgets('should use custom padding', (tester) async {
      const customPadding = EdgeInsets.all(50.0);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              padding: customPadding,
            ),
          ),
        ),
      );

      final paddingWidget = tester.widget<Padding>(find.byType(Padding));
      expect(paddingWidget.padding, equals(customPadding));
    });
  });

  group('GHEmptyStates factory methods', () {
    testWidgets('noRepositories should create appropriate empty state', (
      tester,
    ) async {
      bool createPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noRepositories(
              onCreateRepository: () => createPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.folder_outlined), findsOneWidget);
      expect(find.text('No repositories'), findsOneWidget);
      expect(
        find.text('Create your first repository to get started'),
        findsOneWidget,
      );
      expect(find.text('Create repository'), findsOneWidget);

      await tester.tap(find.text('Create repository'));
      expect(createPressed, isTrue);
    });

    testWidgets('noIssues should create appropriate empty state', (
      tester,
    ) async {
      bool createPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noIssues(
              onCreateIssue: () => createPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.bug_report_outlined), findsOneWidget);
      expect(find.text('No issues'), findsOneWidget);
      expect(
        find.text('Issues help you track bugs and feature requests'),
        findsOneWidget,
      );
      expect(find.text('Create issue'), findsOneWidget);

      await tester.tap(find.text('Create issue'));
      expect(createPressed, isTrue);
    });

    testWidgets('noPullRequests should create appropriate empty state', (
      tester,
    ) async {
      bool createPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noPullRequests(
              onCreatePR: () => createPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.merge_type_outlined), findsOneWidget);
      expect(find.text('No pull requests'), findsOneWidget);
      expect(
        find.text('Pull requests help you collaborate on code changes'),
        findsOneWidget,
      );
      expect(find.text('Create pull request'), findsOneWidget);

      await tester.tap(find.text('Create pull request'));
      expect(createPressed, isTrue);
    });

    testWidgets('noSearchResults should create appropriate empty state', (
      tester,
    ) async {
      bool clearPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noSearchResults(
              query: 'test query',
              onClearSearch: () => clearPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.search_off_outlined), findsOneWidget);
      expect(find.text('No results found'), findsOneWidget);
      expect(find.text('No results found for "test query"'), findsOneWidget);
      expect(find.text('Clear search'), findsOneWidget);

      await tester.tap(find.text('Clear search'));
      expect(clearPressed, isTrue);
    });

    testWidgets('noStarredRepos should create appropriate empty state', (
      tester,
    ) async {
      bool explorePressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noStarredRepos(
              onExplore: () => explorePressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.star_border_outlined), findsOneWidget);
      expect(find.text('No starred repositories'), findsOneWidget);
      expect(
        find.text(
          'Star repositories to keep track of projects you find interesting',
        ),
        findsOneWidget,
      );
      expect(find.text('Explore repositories'), findsOneWidget);

      await tester.tap(find.text('Explore repositories'));
      expect(explorePressed, isTrue);
    });

    testWidgets('noFollowers should create appropriate empty state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHEmptyStates.noFollowers())),
      );

      expect(find.byIcon(Icons.people_outline), findsOneWidget);
      expect(find.text('No followers yet'), findsOneWidget);
      expect(
        find.text('When people follow you, they\'ll appear here'),
        findsOneWidget,
      );
    });

    testWidgets('noFollowing should create appropriate empty state', (
      tester,
    ) async {
      bool explorePressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noFollowing(
              onExplore: () => explorePressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.person_add_outlined), findsOneWidget);
      expect(find.text('Not following anyone'), findsOneWidget);
      expect(
        find.text('Follow people to see their activity in your dashboard'),
        findsOneWidget,
      );
      expect(find.text('Explore people'), findsOneWidget);

      await tester.tap(find.text('Explore people'));
      expect(explorePressed, isTrue);
    });

    testWidgets('noActivity should create appropriate empty state', (
      tester,
    ) async {
      bool explorePressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noActivity(
              onExplore: () => explorePressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.timeline_outlined), findsOneWidget);
      expect(find.text('Your activity will appear here'), findsOneWidget);
      expect(
        find.text(
          'When you star repositories, follow people, or contribute to projects, your activity will show up here',
        ),
        findsOneWidget,
      );
      expect(find.text('Explore GitHub'), findsOneWidget);

      await tester.tap(find.text('Explore GitHub'));
      expect(explorePressed, isTrue);
    });

    testWidgets('emptyList should create generic empty state', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.emptyList(
              title: 'Custom Title',
              subtitle: 'Custom Subtitle',
              icon: Icons.list_outlined,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.list_outlined), findsOneWidget);
      expect(find.text('Custom Title'), findsOneWidget);
      expect(find.text('Custom Subtitle'), findsOneWidget);
    });
  });

  group('GHEmptyState design token compliance', () {
    testWidgets('should use correct spacing between elements', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHEmptyState(
              icon: Icons.folder_outlined,
              title: 'Test Title',
              subtitle: 'Test Subtitle',
              action: ElevatedButton(onPressed: null, child: Text('Action')),
            ),
          ),
        ),
      );

      final sizedBoxes = find.byType(SizedBox);
      expect(sizedBoxes, findsNWidgets(4));

      // Check spacing between icon and title (16dp)
      final sizedBoxList = tester.widgetList<SizedBox>(sizedBoxes).toList();
      // Skip the first SizedBox which is the icon's intrinsic size
      expect(sizedBoxList[1].height, equals(GHTokens.spacing16));

      // Check spacing between title and subtitle (8dp)
      expect(sizedBoxList[2].height, equals(GHTokens.spacing8));

      // Check spacing between subtitle and action (24dp)
      expect(sizedBoxList[3].height, equals(GHTokens.spacing24));
    });

    testWidgets('should use default padding from design tokens', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: GHEmptyState(icon: Icons.folder_outlined, title: 'Test Title'),
        ),
      );

      final paddingWidget = tester.widget<Padding>(find.byType(Padding));
      expect(
        paddingWidget.padding,
        equals(const EdgeInsets.all(GHTokens.spacing24)),
      );
    });
  });
}
