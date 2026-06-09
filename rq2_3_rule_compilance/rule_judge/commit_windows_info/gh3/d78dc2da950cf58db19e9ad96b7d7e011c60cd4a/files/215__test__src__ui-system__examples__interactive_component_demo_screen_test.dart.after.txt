import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/interactive_component_demo_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('InteractiveComponentDemoScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      expect(find.text('Interactive Demo Controls'), findsOneWidget);
    });

    testWidgets('shows demo category selector', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      expect(find.text('Demo Categories'), findsOneWidget);
      expect(find.text('Button States'), findsOneWidget);
      expect(find.text('Form Components'), findsOneWidget);
      expect(find.text('App States'), findsOneWidget);
      expect(find.text('User Interactions'), findsOneWidget);
    });

    testWidgets('defaults to button demo', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Should show button demo by default
      expect(find.text('Button State Controls'), findsOneWidget);
      expect(find.text('Button Variants'), findsOneWidget);
    });

    testWidgets('can switch demo categories', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Switch to form demo
      await tester.tap(find.text('Form Components'));
      await tester.pumpAndSettle();

      expect(find.text('Form Component Controls'), findsOneWidget);
      expect(find.text('Username'), findsOneWidget);
    });

    testWidgets('button demo shows interactive controls', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Should show button controls and examples
      expect(find.text('Start Loading'), findsOneWidget);
      expect(find.text('Primary Buttons'), findsOneWidget);
      expect(find.text('Secondary Buttons'), findsOneWidget);
      expect(
        find.text('Normal'),
        findsNWidgets(2),
      ); // One for primary, one for secondary
    });

    testWidgets('can toggle loading state in button demo', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Tap start loading
      await tester.tap(find.text('Start Loading'));
      await tester.pump();

      // Should change to stop loading
      expect(find.text('Stop Loading'), findsOneWidget);
    });

    testWidgets('form demo shows interactive form elements', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Switch to form demo
      await tester.tap(find.text('Form Components'));
      await tester.pump();

      // Should show form elements
      expect(find.text('Username'), findsOneWidget);
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
    });

    testWidgets('state demo shows controls and normal state', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Switch to state demo
      await tester.tap(find.text('App States'));
      await tester.pump();

      // Should show state controls
      expect(find.text('App State Controls'), findsOneWidget);
      expect(find.text('Normal'), findsOneWidget);
      expect(find.text('Loading'), findsOneWidget);
      expect(find.text('Error'), findsOneWidget);
      expect(find.text('Empty'), findsOneWidget);
    });

    testWidgets('interaction demo shows interactive elements', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // Switch to interaction demo
      await tester.tap(find.text('User Interactions'));
      await tester.pumpAndSettle();

      // Should show interactive elements
      expect(find.text('Interactive Elements'), findsOneWidget);
      expect(find.text('Tappable Cards'), findsOneWidget);
      expect(find.text('Interaction Feedback'), findsOneWidget);
      expect(find.text('Interactive Card 1'), findsOneWidget);
      expect(find.text('Show Success'), findsOneWidget);
    });

    testWidgets('displays component categories correctly', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const InteractiveComponentDemoScreen(),
        ),
      );

      // All demo categories should be visible
      expect(find.text('Button States'), findsOneWidget);
      expect(find.text('Form Components'), findsOneWidget);
      expect(find.text('App States'), findsOneWidget);
      expect(find.text('User Interactions'), findsOneWidget);
    });
  });
}
