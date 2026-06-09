import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/comparison/component_showcase_comparison_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('ComponentShowcaseComparisonScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      expect(find.text('Component Showcase'), findsOneWidget);
    });

    testWidgets('shows improvement highlights', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      expect(find.text('Key Improvements'), findsOneWidget);
      expect(
        find.text('Added comprehensive state management components'),
        findsOneWidget,
      );
      expect(
        find.text('Implemented loading, empty, and error states'),
        findsOneWidget,
      );
      expect(
        find.text('Enhanced button variants with proper feedback'),
        findsOneWidget,
      );
      expect(
        find.text('Improved form components with validation'),
        findsOneWidget,
      );
      expect(
        find.text('Consistent GitHub-themed styling throughout'),
        findsOneWidget,
      );
    });

    testWidgets('has Before and After tabs', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      expect(find.text('Before'), findsOneWidget);
      expect(find.text('After'), findsOneWidget);
    });

    testWidgets('shows before description correctly', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      expect(
        find.text(
          'Basic components without proper state management or consistent styling',
        ),
        findsOneWidget,
      );
    });

    testWidgets('can switch to after tab and shows after description', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Tap the After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      expect(
        find.text(
          'Enhanced components with state management, loading states, and GitHub-specific styling',
        ),
        findsOneWidget,
      );
    });

    testWidgets('before tab shows basic components and issues', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Should show basic component sections
      expect(find.text('Basic Buttons'), findsOneWidget);
      expect(find.text('Basic Form Components'), findsOneWidget);
      expect(find.text('Basic Cards'), findsOneWidget);

      // Should show issues with basic components
      expect(find.text('Issues with Basic Components'), findsOneWidget);
      expect(find.text('No loading states'), findsOneWidget);
      expect(find.text('No error handling'), findsOneWidget);
      expect(find.text('Inconsistent styling'), findsOneWidget);
    });

    testWidgets('after tab shows enhanced components and benefits', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show enhanced component sections
      expect(find.text('Enhanced GH Buttons'), findsOneWidget);
      expect(find.text('Enhanced GH Form Components'), findsOneWidget);
      expect(find.text('Enhanced GH Cards'), findsOneWidget);
      expect(find.text('State Management Components'), findsOneWidget);

      // Should show benefits
      expect(find.text('Enhanced Component Benefits'), findsOneWidget);
      expect(find.text('Comprehensive state management'), findsOneWidget);
      expect(find.text('Loading, error, and empty states'), findsOneWidget);
    });

    testWidgets('shows interactive state controls in after tab', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show state control buttons
      expect(find.text('Show Loading'), findsOneWidget);
      expect(find.text('Show Error'), findsOneWidget);
      expect(find.text('Show Empty'), findsOneWidget);

      // Should show normal content state initially
      expect(find.text('Normal Content State'), findsOneWidget);
    });

    testWidgets('shows state management components in after tab', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show state management section
      expect(find.text('State Management Components'), findsOneWidget);
      expect(find.text('Normal Content State'), findsOneWidget);
    });

    testWidgets('shows component examples in both views', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Should show components in before view
      expect(find.text('Submit'), findsOneWidget);
      expect(find.text('Cancel'), findsOneWidget);
      expect(find.text('Repository Card'), findsOneWidget);

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show enhanced components in after view
      expect(find.text('Primary Action'), findsOneWidget);
      expect(find.text('Secondary Action'), findsOneWidget);
      expect(find.text('Repository Card'), findsOneWidget);
    });

    testWidgets('shows enhanced components in after view', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ComponentShowcaseComparisonScreen(),
        ),
      );

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show enhanced component types
      expect(find.text('Primary Action'), findsOneWidget);
      expect(find.text('Secondary Action'), findsOneWidget);
      expect(find.text('Loading'), findsOneWidget);
      expect(find.text('With Icon'), findsOneWidget);
    });
  });
}
