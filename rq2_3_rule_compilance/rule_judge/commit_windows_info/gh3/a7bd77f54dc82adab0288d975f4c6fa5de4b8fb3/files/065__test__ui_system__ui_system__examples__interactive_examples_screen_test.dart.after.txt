import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui_system/examples/interactive_examples_screen.dart';
import 'package:gh3/src/ui_system/theme/gh_theme.dart';

void main() {
  Widget createTestWidget(Widget child) {
    return MaterialApp(
      theme: GHTheme.lightTheme(),
      darkTheme: GHTheme.darkTheme(),
      home: child,
    );
  }

  group('InteractiveExamplesScreen', () {
    testWidgets('renders correctly', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      expect(find.text('Interactive Component Examples'), findsOneWidget);
      expect(find.text('Real-World Scenarios'), findsOneWidget);
      expect(find.text('Repository Creation Flow'), findsOneWidget);
      expect(find.text('Issue Management'), findsOneWidget);
      expect(find.text('Search & Filter Experience'), findsOneWidget);
      expect(find.text('State Transitions'), findsOneWidget);
      expect(find.text('Responsive Layouts'), findsOneWidget);
    });

    testWidgets('renders section headers', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      expect(
        find.text('Interactive examples showing components in action'),
        findsOneWidget,
      );
      expect(
        find.text('Complete form interaction with validation'),
        findsOneWidget,
      );
      expect(find.text('Status transitions and filtering'), findsOneWidget);
      expect(find.text('Advanced search with live filtering'), findsOneWidget);
      expect(
        find.text('Loading, empty, and error state demonstrations'),
        findsOneWidget,
      );
      expect(
        find.text('Components adapting to different contexts'),
        findsOneWidget,
      );
    });

    testWidgets('reset button exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      expect(find.byIcon(Icons.refresh), findsOneWidget);
      expect(find.byTooltip('Reset all states'), findsOneWidget);
    });

    testWidgets('repository creation section exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      // Scroll to repository creation section
      await tester.dragUntilVisible(
        find.text('Create a new repository'),
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pumpAndSettle();

      expect(find.text('Create a new repository'), findsOneWidget);
      expect(find.text('Repository name'), findsOneWidget);
      expect(find.text('Description'), findsOneWidget);
      expect(find.text('Private repository'), findsOneWidget);
      expect(find.text('Template repository'), findsOneWidget);
      expect(find.text('Initialize with README'), findsOneWidget);
    });

    testWidgets('issue management section exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      // Scroll to issue management section
      await tester.dragUntilVisible(
        find.text('Issue Status'),
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pumpAndSettle();

      expect(find.text('Issue Status'), findsOneWidget);
      expect(find.text('Open'), findsWidgets);
      expect(find.text('Closed'), findsWidgets);
      expect(find.text('Add dark mode support #42'), findsOneWidget);
    });

    testWidgets('search section exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      // Scroll to search section
      await tester.dragUntilVisible(
        find.text('Search & Filter Experience'),
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pumpAndSettle();

      expect(find.text('Search programming languages...'), findsOneWidget);
    });

    testWidgets('state transitions section exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      // Scroll to state transitions section
      await tester.dragUntilVisible(
        find.text('State Demonstration'),
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pumpAndSettle();

      expect(find.text('State Demonstration'), findsOneWidget);
      expect(find.text('Loading'), findsWidgets);
      expect(find.text('Empty'), findsOneWidget);
      expect(find.text('Error'), findsOneWidget);
    });

    testWidgets('responsive layouts section exists', (tester) async {
      await tester.pumpWidget(
        createTestWidget(const InteractiveExamplesScreen()),
      );

      // Scroll to responsive layouts section
      await tester.dragUntilVisible(
        find.text('Card Variants in Context'),
        find.byType(SingleChildScrollView),
        const Offset(0, -200),
      );
      await tester.pumpAndSettle();

      expect(find.text('Card Variants in Context'), findsOneWidget);
      expect(find.text('Repository Details'), findsOneWidget);
      expect(find.text('Quick Actions'), findsOneWidget);
    });
  });
}
