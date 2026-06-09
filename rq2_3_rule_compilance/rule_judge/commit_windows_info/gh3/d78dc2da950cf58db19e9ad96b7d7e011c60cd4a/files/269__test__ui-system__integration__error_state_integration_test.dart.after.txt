import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/examples/repository_details_example.dart';
import 'package:gh3/src/ui-system/examples/repository_tree_example.dart';
import 'package:gh3/src/ui-system/state_widgets/gh_error_state.dart';

void main() {
  group('Error State Integration', () {
    testWidgets('repository details should show error state with retry', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: RepositoryDetailsExample(
            owner: 'test-owner',
            name: 'test-repo',
          ),
        ),
      );

      // Wait for the loading state to appear
      await tester.pump();
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // Wait for the simulated delay and error to occur
      await tester.pump(const Duration(milliseconds: 600));

      // Should show the GHErrorState with retry button
      expect(find.byType(GHErrorState), findsOneWidget);
      expect(find.text('Unable to Load Repository'), findsOneWidget);
      expect(
        find.text(
          'There was a problem loading the repository. Please try again.',
        ),
        findsOneWidget,
      );
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('repository tree should show error state with retry', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: RepositoryTreeExample(
            owner: 'test-owner',
            name: 'test-repo',
            path: '',
          ),
        ),
      );

      // Wait for the loading state to appear
      await tester.pump();
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // Wait for the simulated delay and error to occur
      await tester.pump(const Duration(milliseconds: 600));

      // Should show the GHErrorState with retry button
      expect(find.byType(GHErrorState), findsOneWidget);
      expect(find.text('Unable to Load Repository'), findsOneWidget);
      expect(
        find.text(
          'There was a problem loading the repository. Please try again.',
        ),
        findsOneWidget,
      );
      expect(find.text('Retry'), findsOneWidget);
    });

    testWidgets('error state retry button should trigger reload', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: RepositoryDetailsExample(
            owner: 'test-owner',
            name: 'test-repo',
          ),
        ),
      );

      await tester.pump();
      await tester.pump(const Duration(milliseconds: 600));

      expect(find.byType(GHErrorState), findsOneWidget);
      expect(find.text('Retry'), findsOneWidget);

      await tester.tap(find.text('Retry'));
      await tester.pump(const Duration(milliseconds: 100));

      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // Wait for all async operations to complete
      await tester.pumpAndSettle();
    });
  });
}
