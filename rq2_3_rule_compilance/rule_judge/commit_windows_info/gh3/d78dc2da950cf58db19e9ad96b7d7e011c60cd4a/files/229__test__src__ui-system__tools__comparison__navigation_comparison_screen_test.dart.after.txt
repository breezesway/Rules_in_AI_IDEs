import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/comparison/navigation_comparison_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('NavigationComparisonScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      expect(find.text('Navigation Improvements'), findsOneWidget);
    });

    testWidgets('shows improvement highlights', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      expect(find.text('Key Improvements'), findsOneWidget);
      expect(
        find.text('Eliminated tab navigation in favor of action lists'),
        findsOneWidget,
      );
      expect(
        find.text('Implemented Material Design scrolling app bar'),
        findsOneWidget,
      );
      expect(find.text('Removed duplicate title display'), findsOneWidget);
      expect(
        find.text('Consistent push navigation throughout app'),
        findsOneWidget,
      );
      expect(
        find.text('Better scalability for adding new sections'),
        findsOneWidget,
      );
    });

    testWidgets('has Before and After tabs', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
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
          home: const NavigationComparisonScreen(),
        ),
      );

      expect(
        find.text(
          'Tab-based navigation with duplicate titles and limited scalability',
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
          home: const NavigationComparisonScreen(),
        ),
      );

      // Tap the After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      expect(
        find.text(
          'Action-based push navigation with scrolling app bar and improved user experience',
        ),
        findsOneWidget,
      );
    });

    testWidgets('before tab shows tab-based navigation elements', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      // Should show tabs in before view
      expect(find.text('Repositories'), findsOneWidget);
      expect(find.text('Starred'), findsOneWidget);
      expect(find.text('Organizations'), findsOneWidget);
      expect(find.text('Repository content would appear here'), findsOneWidget);
    });

    testWidgets('after tab shows navigation grid and benefits', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should show navigation benefits
      expect(find.text('Navigation Benefits'), findsOneWidget);
      expect(find.text('Push Navigation'), findsOneWidget);
      expect(find.text('Scrolling App Bar'), findsOneWidget);
      expect(find.text('Scalable Grid'), findsOneWidget);
      expect(find.text('Mobile Optimized'), findsOneWidget);
    });

    testWidgets('shows user card in both views', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      // Should show user info in before view
      expect(find.text('The Octocat'), findsWidgets);
      expect(find.text('@octocat'), findsWidgets);

      // Switch to After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      // Should still show user info in after view
      expect(find.text('The Octocat'), findsWidgets);
      expect(find.text('@octocat'), findsWidgets);
    });

    testWidgets('shows badges on tabs in before view', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const NavigationComparisonScreen(),
        ),
      );

      // Should show count badges on tabs - note that numbers appear in multiple places
      expect(find.text('45'), findsWidgets);
      expect(find.text('234'), findsWidgets);
      expect(find.text('3'), findsWidgets);

      // More specific: check that we have the tab labels
      expect(find.text('Repositories'), findsOneWidget);
      expect(find.text('Starred'), findsOneWidget);
      expect(find.text('Organizations'), findsOneWidget);
    });
  });
}
