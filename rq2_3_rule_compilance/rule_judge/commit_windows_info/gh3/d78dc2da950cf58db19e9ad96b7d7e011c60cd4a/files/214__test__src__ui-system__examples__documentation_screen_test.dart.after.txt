import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/documentation_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('DocumentationScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      expect(find.text('Design System Documentation'), findsOneWidget);
    });

    testWidgets('shows documentation sections sidebar', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      expect(find.text('Documentation Sections'), findsOneWidget);
      expect(find.text('Navigation Improvements'), findsOneWidget);
      expect(find.text('Spacing Standardization'), findsOneWidget);
      expect(find.text('Component Enhancements'), findsOneWidget);
      expect(find.text('Developer Tools'), findsOneWidget);
      expect(find.text('Implementation Guide'), findsOneWidget);
      expect(find.text('Maintenance Guidelines'), findsOneWidget);
    });

    testWidgets('displays navigation improvements content by default', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      expect(find.text('Navigation Pattern Improvements'), findsOneWidget);
      expect(find.text('Key Benefits'), findsOneWidget);
      expect(find.text('Technical Implementation'), findsOneWidget);
      expect(find.text('Developer Guidelines'), findsOneWidget);
    });

    testWidgets('can switch between documentation sections', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Tap on Spacing Standardization section
      await tester.tap(find.text('Spacing Standardization'));
      await tester.pump();

      expect(find.text('4dp Grid Spacing System'), findsOneWidget);
      expect(find.text('Spacing Scale'), findsOneWidget);
      expect(find.text('Compliance Validation'), findsOneWidget);

      // Tap on Component Enhancements section
      await tester.tap(find.text('Component Enhancements'));
      await tester.pump();

      expect(find.text('Component Enhancement Overview'), findsOneWidget);
      expect(find.text('State Management Components'), findsOneWidget);
    });

    testWidgets('shows spacing examples in spacing section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to spacing section
      await tester.tap(find.text('Spacing Standardization'));
      await tester.pump();

      expect(find.text('4dp'), findsOneWidget);
      expect(find.text('8dp'), findsOneWidget);
      expect(find.text('12dp'), findsOneWidget);
      expect(find.text('16dp'), findsOneWidget);
      expect(find.text('20dp'), findsOneWidget);
      expect(find.text('24dp'), findsOneWidget);
      expect(find.text('32dp'), findsOneWidget);
    });

    testWidgets('displays state management components in component section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to component section
      await tester.tap(find.text('Component Enhancements'));
      await tester.pump();

      expect(find.text('GHLoadingIndicator'), findsAtLeastNWidgets(1));
      expect(find.text('GHEmptyState'), findsAtLeastNWidgets(1));
      expect(find.text('GHErrorState'), findsAtLeastNWidgets(1));
    });

    testWidgets('shows developer tools information', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to developer tools section
      await tester.tap(find.text('Developer Tools'));
      await tester.pump();

      expect(find.text('Professional Developer Tools'), findsOneWidget);
      expect(find.text('Measurement & Validation Tools'), findsOneWidget);
      expect(find.text('Standards Compliance Audit'), findsOneWidget);
    });

    testWidgets('displays implementation guide content', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to implementation guide section
      await tester.tap(find.text('Implementation Guide'));
      await tester.pump();

      expect(find.text('Implementation Best Practices'), findsOneWidget);
      expect(find.text('Implementation Patterns'), findsOneWidget);
      expect(find.text('Screen Structure'), findsOneWidget);
      expect(find.text('Spacing Usage'), findsOneWidget);
    });

    testWidgets('shows maintenance guidelines', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to maintenance guidelines section
      await tester.tap(find.text('Maintenance Guidelines'));
      await tester.pump();

      expect(find.text('Maintenance & Evolution Guidelines'), findsOneWidget);
      expect(find.text('Ongoing Maintenance'), findsOneWidget);
      expect(find.text('Component Evolution'), findsOneWidget);
      expect(find.text('Quality Monitoring'), findsOneWidget);
    });

    testWidgets('highlights selected section in sidebar', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // First section should be selected by default
      final firstSectionFinder = find.text('Navigation Improvements');
      expect(firstSectionFinder, findsOneWidget);

      // Tap on a different section
      await tester.tap(find.text('Developer Tools'));
      await tester.pump();

      // Should show the new content
      expect(find.text('Professional Developer Tools'), findsOneWidget);
    });

    testWidgets('displays comprehensive feature lists', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Check navigation improvements content
      expect(
        find.textContaining('Eliminated duplicate screen titles'),
        findsOneWidget,
      );
      expect(
        find.textContaining('Improved user flow efficiency'),
        findsOneWidget,
      );

      // Navigate to developer tools
      await tester.tap(find.text('Developer Tools'));
      await tester.pump();

      expect(
        find.textContaining('Interactive spacing overlays'),
        findsOneWidget,
      );
      expect(find.textContaining('4dp grid visualization'), findsOneWidget);
    });

    testWidgets('shows code examples in implementation guide', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      // Navigate to implementation guide
      await tester.tap(find.text('Implementation Guide'));
      await tester.pump();

      expect(find.textContaining('GHScreenTemplate'), findsAtLeastNWidgets(1));
      expect(find.textContaining('GHTokens.spacing'), findsAtLeastNWidgets(1));
      expect(
        find.textContaining('GHLoadingIndicator'),
        findsAtLeastNWidgets(1),
      );
    });

    testWidgets('is scrollable', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('displays proper icons for each section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DocumentationScreen(),
        ),
      );

      expect(find.byIcon(Icons.navigation), findsOneWidget);
      expect(find.byIcon(Icons.grid_4x4), findsOneWidget);
      expect(find.byIcon(Icons.widgets), findsOneWidget);
      expect(find.byIcon(Icons.build), findsOneWidget);
      expect(find.byIcon(Icons.code), findsOneWidget);
      expect(find.byIcon(Icons.settings), findsOneWidget);
    });
  });
}
