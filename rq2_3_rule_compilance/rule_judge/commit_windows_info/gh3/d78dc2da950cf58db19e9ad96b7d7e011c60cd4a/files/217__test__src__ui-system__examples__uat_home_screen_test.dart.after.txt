import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/uat_home_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('UATHomeScreen', () {
    testWidgets('displays app title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      expect(find.text('GH3 Design System - UAT'), findsOneWidget);
    });

    testWidgets('shows main navigation sections', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      // Design system sections
      expect(find.text('Design Tokens'), findsOneWidget);
      expect(find.text('Component Catalog'), findsOneWidget);
      expect(find.text('Interactive Examples'), findsOneWidget);
    });

    testWidgets('shows UI improvements section', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      // Improvements section
      expect(find.text('UI System Improvements'), findsOneWidget);
      expect(find.text('Navigation Improvements'), findsOneWidget);
      expect(find.text('Spacing Standardization'), findsOneWidget);
      expect(find.text('Component Showcase'), findsOneWidget);
    });

    testWidgets('shows developer tools section', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      // Developer tools section
      expect(find.text('Developer Tools'), findsOneWidget);
      expect(find.text('Measurement & Validation Tools'), findsOneWidget);
    });

    testWidgets('shows description and info sections', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      expect(find.text('Design System Showcase'), findsOneWidget);
      expect(find.text('About This UAT Build'), findsOneWidget);
      expect(find.text('Quick Actions'), findsOneWidget);
    });

    testWidgets('has theme toggle button', (WidgetTester tester) async {
      bool themeToggled = false;

      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () => themeToggled = true),
        ),
      );

      // Should have theme toggle button
      expect(find.byIcon(Icons.dark_mode), findsOneWidget);

      // Tap theme toggle
      await tester.tap(find.byIcon(Icons.dark_mode));
      await tester.pump();

      expect(themeToggled, isTrue);
    });

    testWidgets('shows quick action buttons', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      expect(find.text('View Tokens'), findsOneWidget);
      expect(find.text('View Components'), findsOneWidget);
    });

    testWidgets('shows feature highlights', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      expect(find.text('Material Design 3 Foundation'), findsOneWidget);
      expect(find.text('Navigation Efficiency Improvements'), findsOneWidget);
      expect(find.text('Visual Consistency Through 4dp Grid'), findsOneWidget);
      expect(find.text('Enhanced State Management'), findsOneWidget);
    });

    testWidgets('shows build information', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      expect(find.text('Build Information'), findsOneWidget);
      expect(
        find.text('GitHub Mobile Design System v1.0.0 - Phase 4 Demo'),
        findsOneWidget,
      );
    });

    testWidgets('can navigate through scroll content', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: UATHomeScreen(onThemeToggle: () {}),
        ),
      );

      // Should be scrollable
      expect(find.byType(SingleChildScrollView), findsOneWidget);

      // Scroll down and verify content is still accessible
      await tester.drag(
        find.byType(SingleChildScrollView),
        const Offset(0, -300),
      );
      await tester.pump();

      // Should still find content after scrolling
      expect(find.text('GH3 Design System - UAT'), findsOneWidget);
    });
  });
}
