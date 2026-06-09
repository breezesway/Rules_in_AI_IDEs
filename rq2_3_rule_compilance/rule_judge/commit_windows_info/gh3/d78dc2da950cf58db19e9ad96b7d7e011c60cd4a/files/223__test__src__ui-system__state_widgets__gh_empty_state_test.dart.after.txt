import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../../../../lib/src/ui-system/state_widgets/gh_empty_state.dart';

void main() {
  group('GHEmptyStates Additional Methods', () {
    testWidgets('noNotifications should display correct content', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHEmptyStates.noNotifications())),
      );

      expect(find.text('No notifications'), findsOneWidget);
      expect(
        find.text('When you have notifications, they\'ll appear here'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.notifications_none_outlined), findsOneWidget);
    });

    testWidgets('noNotifications should not have action button', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHEmptyStates.noNotifications())),
      );

      expect(find.byType(ElevatedButton), findsNothing);
      expect(find.byType(TextButton), findsNothing);
    });

    testWidgets('noIssues should display create issue action', (tester) async {
      bool actionCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noIssues(
              onCreateIssue: () => actionCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('No issues'), findsOneWidget);
      expect(
        find.text('Issues help you track bugs and feature requests'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.bug_report_outlined), findsOneWidget);

      // Test action button
      expect(find.text('Create issue'), findsOneWidget);
      await tester.tap(find.text('Create issue'));
      await tester.pump();

      expect(actionCalled, isTrue);
    });

    testWidgets('noStarredRepos should display explore action', (tester) async {
      bool actionCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noStarredRepos(
              onExplore: () => actionCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('No starred repositories'), findsOneWidget);
      expect(
        find.text(
          'Star repositories to keep track of projects you find interesting',
        ),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.star_border_outlined), findsOneWidget);

      // Test action button
      expect(find.text('Explore repositories'), findsOneWidget);
      await tester.tap(find.text('Explore repositories'));
      await tester.pump();

      expect(actionCalled, isTrue);
    });

    testWidgets('noActivity should display correct content and action', (
      tester,
    ) async {
      bool actionCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHEmptyStates.noActivity(
              onExplore: () => actionCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('Your activity will appear here'), findsOneWidget);
      expect(
        find.text(
          'When you star repositories, follow people, or contribute to projects, your activity will show up here',
        ),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.timeline_outlined), findsOneWidget);

      // Test action button
      expect(find.text('Explore GitHub'), findsOneWidget);
      await tester.tap(find.text('Explore GitHub'));
      await tester.pump();

      expect(actionCalled, isTrue);
    });
  });
}
