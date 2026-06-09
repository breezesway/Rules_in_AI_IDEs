import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import '../../../../lib/src/ui-system/state_widgets/gh_error_state.dart';

void main() {
  group('GHErrorStates Additional Methods', () {
    testWidgets('searchError should display correct content with query', (
      tester,
    ) async {
      const query = 'flutter ui toolkit';
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.searchError(
              query: query,
              onRetry: () => retryCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('Search Failed'), findsOneWidget);
      expect(
        find.text('Unable to search for "$query". Please try again.'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.search_off_outlined), findsOneWidget);

      // Test retry button
      expect(find.text('Retry'), findsOneWidget);
      await tester.tap(find.text('Retry'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });

    testWidgets('searchError should display correct content without query', (
      tester,
    ) async {
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.searchError(onRetry: () => retryCalled = true),
          ),
        ),
      );

      expect(find.text('Search Failed'), findsOneWidget);
      expect(
        find.text('Search request failed. Please try again.'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.search_off_outlined), findsOneWidget);

      // Test retry button
      expect(find.text('Retry'), findsOneWidget);
      await tester.tap(find.text('Retry'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });

    testWidgets('authenticationError should display correct content', (
      tester,
    ) async {
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.authenticationError(
              onRetry: () => retryCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('Authentication Required'), findsOneWidget);
      expect(
        find.text('Please sign in to access this content.'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.person_off_outlined), findsOneWidget);

      // Test custom retry button text
      expect(find.text('Sign In'), findsOneWidget);
      await tester.tap(find.text('Sign In'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });

    testWidgets('rateLimitError should display correct content', (
      tester,
    ) async {
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.rateLimitError(
              onRetry: () => retryCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('Rate Limit Exceeded'), findsOneWidget);
      expect(
        find.textContaining('You\'ve exceeded the API rate limit'),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.hourglass_empty_outlined), findsOneWidget);

      // Test retry button
      expect(find.text('Retry'), findsOneWidget);
      await tester.tap(find.text('Retry'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });

    testWidgets('rateLimitError with resetTime should display countdown', (
      tester,
    ) async {
      final resetTime = DateTime.now().add(Duration(minutes: 5, seconds: 30));

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.rateLimitError(
              resetTime: resetTime,
              onRetry: () {},
            ),
          ),
        ),
      );

      expect(find.text('Rate Limit Exceeded'), findsOneWidget);
      expect(find.textContaining('Rate limit will reset in'), findsOneWidget);
      expect(find.textContaining('5m'), findsOneWidget);
      expect(find.byIcon(Icons.hourglass_empty_outlined), findsOneWidget);
    });

    testWidgets('networkError should display correct content', (tester) async {
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.networkError(onRetry: () => retryCalled = true),
          ),
        ),
      );

      expect(find.text('Connection Error'), findsOneWidget);
      expect(
        find.text(
          'Unable to connect to GitHub. Please check your internet connection and try again.',
        ),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.wifi_off_outlined), findsOneWidget);

      // Test retry button
      expect(find.text('Retry'), findsOneWidget);
      await tester.tap(find.text('Retry'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });

    testWidgets('repositoryLoadError should display correct content', (
      tester,
    ) async {
      bool retryCalled = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.repositoryLoadError(
              onRetry: () => retryCalled = true,
            ),
          ),
        ),
      );

      expect(find.text('Unable to Load Repository'), findsOneWidget);
      expect(
        find.text(
          'There was a problem loading the repository. Please try again.',
        ),
        findsOneWidget,
      );
      expect(find.byIcon(Icons.folder_off_outlined), findsOneWidget);

      // Test retry button
      expect(find.text('Retry'), findsOneWidget);
      await tester.tap(find.text('Retry'));
      await tester.pump();

      expect(retryCalled, isTrue);
    });
  });
}
