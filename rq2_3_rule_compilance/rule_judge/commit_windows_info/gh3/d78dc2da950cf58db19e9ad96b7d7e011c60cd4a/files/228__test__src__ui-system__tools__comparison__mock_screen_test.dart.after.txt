import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/comparison/mock_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('MockScreen', () {
    testWidgets('displays title and body', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MockScreen(title: 'Test Screen', body: Text('Test Body')),
        ),
      );

      expect(find.text('Test Screen'), findsOneWidget);
      expect(find.text('Test Body'), findsOneWidget);
    });

    testWidgets('shows back button by default', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MockScreen(title: 'Test Screen', body: Text('Test Body')),
        ),
      );

      expect(find.byIcon(Icons.arrow_back), findsOneWidget);
    });

    testWidgets('can hide back button', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MockScreen(
            title: 'Test Screen',
            body: Text('Test Body'),
            showBackButton: false,
          ),
        ),
      );

      expect(find.byIcon(Icons.arrow_back), findsNothing);
    });

    testWidgets('can display actions', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MockScreen(
            title: 'Test Screen',
            body: Text('Test Body'),
            actions: [Icon(Icons.star), Icon(Icons.share)],
          ),
        ),
      );

      expect(find.byIcon(Icons.star), findsOneWidget);
      expect(find.byIcon(Icons.share), findsOneWidget);
    });

    testWidgets('handles empty title', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const MockScreen(title: '', body: Text('Test Body')),
        ),
      );

      expect(find.text('Test Body'), findsOneWidget);
      // Should not crash with empty title
    });
  });

  group('MockTab', () {
    testWidgets('displays label', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(
            body: Row(
              children: [Expanded(child: MockTab(label: 'Test Tab'))],
            ),
          ),
        ),
      );

      expect(find.text('Test Tab'), findsOneWidget);
    });

    testWidgets('shows different styling when active', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(
            body: Row(
              children: [
                Expanded(child: MockTab(label: 'Active Tab', isActive: true)),
                Expanded(
                  child: MockTab(label: 'Inactive Tab', isActive: false),
                ),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Active Tab'), findsOneWidget);
      expect(find.text('Inactive Tab'), findsOneWidget);
    });

    testWidgets('can display badge', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(
            body: Row(
              children: [
                Expanded(
                  child: MockTab(label: 'Tab with Badge', badge: '42'),
                ),
              ],
            ),
          ),
        ),
      );

      expect(find.text('Tab with Badge'), findsOneWidget);
      expect(find.text('42'), findsOneWidget);
    });
  });

  group('MockUserCard', () {
    testWidgets('displays user information', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(body: MockUserCard()),
        ),
      );

      expect(find.text('The Octocat'), findsOneWidget);
      expect(find.text('@octocat'), findsOneWidget);
      expect(
        find.text('GitHub mascot and friendly neighborhood cat.'),
        findsOneWidget,
      );
    });

    testWidgets('can show title when requested', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(body: MockUserCard(showTitle: true)),
        ),
      );

      // When showTitle is true, the name appears in the title at the top
      expect(find.text('The Octocat'), findsOneWidget);
    });

    testWidgets('displays stats', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(body: MockUserCard()),
        ),
      );

      expect(find.text('1.2k'), findsOneWidget);
      expect(find.text('followers'), findsOneWidget);
      expect(find.text('234'), findsOneWidget);
      expect(find.text('following'), findsOneWidget);
      expect(find.text('45'), findsOneWidget);
      expect(find.text('repositories'), findsOneWidget);
    });

    testWidgets('can use custom user data', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const Scaffold(
            body: MockUserCard(
              displayName: 'John Doe',
              username: '@johndoe',
              bio: 'Software developer',
            ),
          ),
        ),
      );

      expect(find.text('John Doe'), findsOneWidget);
      expect(find.text('@johndoe'), findsOneWidget);
      expect(find.text('Software developer'), findsOneWidget);
    });
  });
}
