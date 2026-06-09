import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/reference_patterns_guide.dart';
import 'package:gh3/src/ui-system/theme/gh_theme.dart';

void main() {
  group('ReferencePatternGuide', () {
    testWidgets('buildScreenPattern creates proper structure', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: ReferencePatternGuide.buildScreenPattern(
            'Test Screen',
            const Text('Content'),
          ),
        ),
      );

      expect(find.text('Test Screen'), findsOneWidget);
      expect(find.text('Content'), findsOneWidget);
      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });

    testWidgets('buildSectionHeader displays title with proper styling', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildSectionHeader('Test Section'),
          ),
        ),
      );

      expect(find.text('Test Section'), findsOneWidget);
    });

    testWidgets('buildContentCard creates tappable card', (
      WidgetTester tester,
    ) async {
      bool tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildContentCard(
              onTap: () => tapped = true,
              child: const Text('Card Content'),
            ),
          ),
        ),
      );

      expect(find.text('Card Content'), findsOneWidget);

      await tester.tap(find.text('Card Content'));
      await tester.pump();

      expect(tapped, true);
    });

    testWidgets('buildButtonRow creates proper button layout', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildButtonRow([
              ElevatedButton(onPressed: () {}, child: const Text('Button 1')),
              ElevatedButton(onPressed: () {}, child: const Text('Button 2')),
              ElevatedButton(onPressed: () {}, child: const Text('Button 3')),
            ]),
          ),
        ),
      );

      expect(find.text('Button 1'), findsOneWidget);
      expect(find.text('Button 2'), findsOneWidget);
      expect(find.text('Button 3'), findsOneWidget);
      expect(find.byType(Expanded), findsNWidgets(3));
    });

    testWidgets('buildLoadingWrapper shows loading indicator when loading', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildLoadingWrapper(
              isLoading: true,
              loadingMessage: 'Loading...',
              child: const Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Loading...'), findsOneWidget);
      expect(find.text('Content'), findsNothing);
    });

    testWidgets('buildLoadingWrapper shows content when not loading', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildLoadingWrapper(
              isLoading: false,
              child: const Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('buildEmptyStateWrapper shows empty state when empty', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildEmptyStateWrapper(
              isEmpty: true,
              emptyTitle: 'No Items',
              emptyMessage: 'Add some items',
              child: const Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('No Items'), findsOneWidget);
      expect(find.text('Add some items'), findsOneWidget);
      expect(find.text('Content'), findsNothing);
    });

    testWidgets('buildErrorStateWrapper shows error state when has error', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildErrorStateWrapper(
              hasError: true,
              errorTitle: 'Error Title',
              errorMessage: 'Error Message',
              onRetry: () {},
              child: const Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Error Title'), findsOneWidget);
      expect(find.text('Error Message'), findsOneWidget);
      expect(find.text('Content'), findsNothing);
    });

    testWidgets('buildInteractiveListItem creates tappable list item', (
      WidgetTester tester,
    ) async {
      bool tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Scaffold(
            body: ReferencePatternGuide.buildInteractiveListItem(
              title: 'Item Title',
              subtitle: 'Item Subtitle',
              leadingIcon: Icons.star,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      expect(find.text('Item Title'), findsOneWidget);
      expect(find.text('Item Subtitle'), findsOneWidget);
      expect(find.byIcon(Icons.star), findsOneWidget);

      await tester.tap(find.text('Item Title'));
      await tester.pump();

      expect(tapped, true);
    });

    testWidgets('buildFormField creates proper form layout', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: Builder(
            builder: (context) => Scaffold(
              body: ReferencePatternGuide.buildFormField(
                context,
                label: 'Field Label',
                field: const TextField(),
                helpText: 'Help text',
              ),
            ),
          ),
        ),
      );

      expect(find.text('Field Label'), findsOneWidget);
      expect(find.text('Help text'), findsOneWidget);
      expect(find.byType(TextField), findsOneWidget);
    });
  });

  group('ReferenceExampleScreen', () {
    testWidgets('displays screen title correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      expect(find.text('Reference Implementation Example'), findsOneWidget);
    });

    testWidgets('shows state control buttons', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      expect(find.text('Loading'), findsOneWidget);
      expect(find.text('Error'), findsOneWidget);
      expect(find.text('Empty'), findsOneWidget);
      expect(find.text('Reset'), findsOneWidget);
    });

    testWidgets('displays content items by default', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 2'), findsOneWidget);
      expect(find.text('Item 3'), findsOneWidget);
    });

    testWidgets('shows loading state when loading button pressed', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      await tester.tap(find.text('Loading'));
      await tester.pump();

      expect(find.text('Loading data...'), findsOneWidget);

      // Wait for the async operation to complete
      await tester.pump(const Duration(seconds: 3));
    });

    testWidgets('shows error state when error button pressed', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      await tester.tap(find.text('Error'));
      await tester.pump();

      expect(find.text('Something Went Wrong'), findsOneWidget);
      expect(
        find.text('Unable to load data. Please try again.'),
        findsOneWidget,
      );
    });

    testWidgets('shows empty state when empty button pressed', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      await tester.tap(find.text('Empty'));
      await tester.pump();

      expect(find.text('No Items Found'), findsOneWidget);
      expect(
        find.text('Try adding some items to see them here.'),
        findsOneWidget,
      );
    });

    testWidgets('shows normal content by default', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      // Check that items are shown by default
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 2'), findsOneWidget);
      expect(find.text('Item 3'), findsOneWidget);

      // Check that control buttons exist
      expect(find.text('Reset'), findsOneWidget);
    });

    testWidgets('handles item tap interactions', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      await tester.tap(find.text('Item 1'));
      await tester.pump();

      expect(find.text('Tapped Item 1'), findsOneWidget);
    });

    testWidgets('shows proper section headers', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      expect(find.text('State Controls'), findsOneWidget);
      expect(find.text('Content Items'), findsOneWidget);
    });

    testWidgets('is scrollable', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          theme: GHTheme.lightTheme(),
          home: const ReferenceExampleScreen(),
        ),
      );

      expect(find.byType(SingleChildScrollView), findsOneWidget);
    });
  });
}
