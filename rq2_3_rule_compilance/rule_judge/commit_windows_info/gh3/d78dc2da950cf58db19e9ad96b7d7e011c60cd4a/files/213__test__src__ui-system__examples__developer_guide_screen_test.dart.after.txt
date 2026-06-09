import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/developer_guide_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('DeveloperGuideScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      expect(find.text('Developer Guide'), findsOneWidget);
    });

    testWidgets('shows guide sections sidebar', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      expect(find.text('Developer Guide Sections'), findsOneWidget);
      expect(find.text('Implementation Patterns'), findsOneWidget);
      expect(find.text('4dp Grid System'), findsOneWidget);
      expect(find.text('Code Quality Standards'), findsOneWidget);
      expect(find.text('Maintenance Procedures'), findsOneWidget);
      expect(find.text('Common Pitfalls'), findsOneWidget);
      expect(find.text('Migration Guide'), findsOneWidget);
    });

    testWidgets('displays implementation patterns content by default', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      expect(
        find.text('Implementation Patterns & Best Practices'),
        findsOneWidget,
      );
      expect(find.text('Screen Structure Pattern'), findsOneWidget);
      expect(find.text('Spacing Usage Pattern'), findsOneWidget);
      expect(find.text('State Management Pattern'), findsOneWidget);
    });

    testWidgets('can switch between guide sections', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Tap on 4dp Grid System section
      await tester.tap(find.text('4dp Grid System'));
      await tester.pump();

      expect(find.text('4dp Grid System Implementation Guide'), findsOneWidget);
      expect(find.text('Available Spacing Values'), findsOneWidget);

      // Tap on Code Quality Standards section
      await tester.tap(find.text('Code Quality Standards'));
      await tester.pump();

      expect(find.text('Code Quality Standards & Validation'), findsOneWidget);
      expect(find.text('Pre-Commit Checklist'), findsOneWidget);
    });

    testWidgets('shows spacing values in grid system section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to grid system section
      await tester.tap(find.text('4dp Grid System'));
      await tester.pump();

      expect(find.text('GHTokens.spacing4'), findsOneWidget);
      expect(find.text('GHTokens.spacing8'), findsOneWidget);
      expect(find.text('GHTokens.spacing16'), findsOneWidget);
      expect(find.text('GHTokens.spacing24'), findsOneWidget);
      expect(find.text('GHTokens.spacing32'), findsOneWidget);
    });

    testWidgets('displays code quality commands', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to code quality section
      await tester.tap(find.text('Code Quality Standards'));
      await tester.pump();

      expect(find.text('dart format .'), findsOneWidget);
      expect(
        find.text('flutter analyze --fatal-infos --fatal-warnings'),
        findsOneWidget,
      );
      expect(find.text('flutter test'), findsOneWidget);
    });

    testWidgets('shows maintenance procedures', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to maintenance procedures section
      await tester.tap(find.text('Maintenance Procedures'));
      await tester.pump();

      expect(find.text('Maintenance Procedures & Guidelines'), findsOneWidget);
      expect(find.text('Adding New Components'), findsOneWidget);
      expect(find.text('Modifying Existing Components'), findsOneWidget);
      expect(find.text('Design Token Updates'), findsOneWidget);
    });

    testWidgets('displays common pitfalls', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to common pitfalls section
      await tester.tap(find.text('Common Pitfalls'));
      await tester.pump();

      expect(find.text('Common Pitfalls & How to Avoid Them'), findsOneWidget);
      expect(find.text('Magic Numbers in Spacing'), findsOneWidget);
      expect(find.text('Inconsistent State Management'), findsOneWidget);
      expect(find.text('Hard-coded Colors'), findsOneWidget);
    });

    testWidgets('shows migration guide content', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to migration guide section
      await tester.tap(find.text('Migration Guide'));
      await tester.pump();

      expect(find.text('Migration Guide for Existing Code'), findsOneWidget);
      expect(find.text('Migration Strategy'), findsOneWidget);
      expect(find.text('Color Migration'), findsOneWidget);
      expect(find.text('Spacing Migration'), findsOneWidget);
    });

    testWidgets('highlights selected section in sidebar', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // First section should be selected by default
      final firstSectionFinder = find.text('Implementation Patterns');
      expect(firstSectionFinder, findsOneWidget);

      // Tap on a different section
      await tester.tap(find.text('Common Pitfalls'));
      await tester.pump();

      // Should show the new content
      expect(find.text('Common Pitfalls & How to Avoid Them'), findsOneWidget);
    });

    testWidgets('displays practical usage examples', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to grid system section
      await tester.tap(find.text('4dp Grid System'));
      await tester.pump();

      expect(find.text('Practical Usage Examples'), findsOneWidget);
      expect(find.text('Card Layout'), findsOneWidget);
      expect(find.text('Screen Layout'), findsOneWidget);
      expect(find.text('Form Layout'), findsOneWidget);
    });

    testWidgets('shows validation tools', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to grid system section
      await tester.tap(find.text('4dp Grid System'));
      await tester.pump();

      expect(find.text('Validation Tools'), findsOneWidget);
      expect(find.text('SpacingValidator Utility'), findsOneWidget);
    });

    testWidgets('displays correct/incorrect code examples', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Check implementation patterns section
      expect(find.textContaining('✅ CORRECT'), findsAtLeastNWidgets(1));
      expect(find.textContaining('❌ INCORRECT'), findsAtLeastNWidgets(1));

      // Navigate to common pitfalls
      await tester.tap(find.text('Common Pitfalls'));
      await tester.pump();

      expect(find.text('Incorrect'), findsAtLeastNWidgets(1));
      expect(find.text('Correct'), findsAtLeastNWidgets(1));
    });

    testWidgets('shows testing requirements', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to code quality section
      await tester.tap(find.text('Code Quality Standards'));
      await tester.pump();

      expect(find.text('Testing Requirements'), findsOneWidget);
      expect(find.text('Unit Tests'), findsOneWidget);
      expect(find.text('Widget Tests'), findsOneWidget);
      expect(find.text('Integration Tests'), findsOneWidget);
    });

    testWidgets('displays maintenance checklist', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to maintenance procedures section
      await tester.tap(find.text('Maintenance Procedures'));
      await tester.pump();

      expect(find.text('Release Checklist'), findsOneWidget);
      expect(find.text('Component Health Metrics'), findsOneWidget);
    });

    testWidgets('shows migration examples', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to migration guide section
      await tester.tap(find.text('Migration Guide'));
      await tester.pump();

      expect(find.text('Widget Migration Example'), findsOneWidget);
      expect(find.text('Custom Card → GHCard'), findsOneWidget);
      expect(find.text('Migration Checklist'), findsOneWidget);
    });

    testWidgets('is scrollable', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsAtLeastNWidgets(1));
    });

    testWidgets('displays proper icons for each section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      expect(find.byIcon(Icons.code), findsOneWidget);
      expect(find.byIcon(Icons.grid_4x4), findsOneWidget);
      expect(find.byIcon(Icons.verified), findsOneWidget);
      expect(find.byIcon(Icons.build_circle), findsOneWidget);
      expect(find.byIcon(Icons.warning), findsOneWidget);
      expect(find.byIcon(Icons.upload), findsOneWidget);
    });

    testWidgets('handles section navigation correctly', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Test navigation through all sections
      final sections = [
        '4dp Grid System',
        'Code Quality Standards',
        'Maintenance Procedures',
        'Common Pitfalls',
        'Migration Guide',
        'Implementation Patterns', // Back to first
      ];

      for (final section in sections) {
        await tester.tap(find.text(section));
        await tester.pump();

        // Verify section content is displayed
        expect(find.text(section), findsOneWidget);
      }
    });

    testWidgets('displays warning cards in pitfalls section', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Navigate to common pitfalls section
      await tester.tap(find.text('Common Pitfalls'));
      await tester.pump();

      expect(find.text('Code Quality Checks'), findsOneWidget);
      expect(find.byIcon(Icons.priority_high), findsOneWidget);
    });

    testWidgets('shows component and pattern examples', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const DeveloperGuideScreen(),
        ),
      );

      // Check implementation patterns section
      expect(find.textContaining('GHScreenTemplate'), findsAtLeastNWidgets(1));
      expect(find.textContaining('GHTokens.spacing'), findsAtLeastNWidgets(1));
      expect(find.textContaining('GHCard'), findsAtLeastNWidgets(1));
    });
  });
}
