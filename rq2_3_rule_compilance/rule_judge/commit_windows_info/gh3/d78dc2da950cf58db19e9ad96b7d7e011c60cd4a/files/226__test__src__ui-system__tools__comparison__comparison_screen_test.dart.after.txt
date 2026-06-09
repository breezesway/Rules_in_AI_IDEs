import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tools/comparison/comparison_screen.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('ComparisonScreen', () {
    late List<ImprovementHighlight> testHighlights;

    setUp(() {
      testHighlights = [
        const ImprovementHighlight(description: 'Improved navigation patterns'),
        const ImprovementHighlight(description: 'Better spacing consistency'),
      ];
    });

    testWidgets('displays title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ComparisonScreen(
            title: 'Test Comparison',
            beforeWidget: const Text('Before'),
            afterWidget: const Text('After'),
            beforeDescription: 'Old implementation',
            afterDescription: 'New implementation',
            highlights: testHighlights,
          ),
        ),
      );

      expect(find.text('Test Comparison'), findsOneWidget);
    });

    testWidgets('shows improvement highlights', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ComparisonScreen(
            title: 'Test Comparison',
            beforeWidget: const Text('Before'),
            afterWidget: const Text('After'),
            beforeDescription: 'Old implementation',
            afterDescription: 'New implementation',
            highlights: testHighlights,
          ),
        ),
      );

      expect(find.text('Key Improvements'), findsOneWidget);
      expect(find.text('Improved navigation patterns'), findsOneWidget);
      expect(find.text('Better spacing consistency'), findsOneWidget);
      expect(find.byIcon(Icons.check_circle), findsNWidgets(2));
    });

    testWidgets('has Before and After tabs', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ComparisonScreen(
            title: 'Test Comparison',
            beforeWidget: const Text('Before Content'),
            afterWidget: const Text('After Content'),
            beforeDescription: 'Old implementation',
            afterDescription: 'New implementation',
            highlights: testHighlights,
          ),
        ),
      );

      expect(find.text('Before'), findsOneWidget);
      expect(find.text('After'), findsOneWidget);
    });

    testWidgets('shows before content by default', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ComparisonScreen(
            title: 'Test Comparison',
            beforeWidget: const Text('Before Content'),
            afterWidget: const Text('After Content'),
            beforeDescription: 'Old implementation',
            afterDescription: 'New implementation',
            highlights: testHighlights,
          ),
        ),
      );

      expect(find.text('Before (Old Implementation)'), findsOneWidget);
      expect(find.text('Old implementation'), findsOneWidget);
      expect(find.text('Before Content'), findsOneWidget);
    });

    testWidgets('can switch to after tab', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ComparisonScreen(
            title: 'Test Comparison',
            beforeWidget: const Text('Before Content'),
            afterWidget: const Text('After Content'),
            beforeDescription: 'Old implementation',
            afterDescription: 'New implementation',
            highlights: testHighlights,
          ),
        ),
      );

      // Tap the After tab
      await tester.tap(find.text('After'));
      await tester.pumpAndSettle();

      expect(find.text('After (New Implementation)'), findsOneWidget);
      expect(find.text('New implementation'), findsOneWidget);
      expect(find.text('After Content'), findsOneWidget);
    });
  });

  group('ImprovementHighlight', () {
    test('can be created with description only', () {
      const highlight = ImprovementHighlight(description: 'Test improvement');

      expect(highlight.description, equals('Test improvement'));
      expect(highlight.details, isNull);
    });

    test('can be created with description and details', () {
      const highlight = ImprovementHighlight(
        description: 'Test improvement',
        details: 'Additional details',
      );

      expect(highlight.description, equals('Test improvement'));
      expect(highlight.details, equals('Additional details'));
    });
  });
}
