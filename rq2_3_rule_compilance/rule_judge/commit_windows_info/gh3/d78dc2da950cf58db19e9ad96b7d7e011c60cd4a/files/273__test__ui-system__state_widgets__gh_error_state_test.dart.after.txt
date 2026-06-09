import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/state_widgets/gh_error_state.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHErrorState', () {
    testWidgets('should display title and message', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
            ),
          ),
        ),
      );

      expect(find.text('Test Error'), findsOneWidget);
      expect(find.text('Test error message'), findsOneWidget);
      expect(find.byIcon(Icons.error_outline), findsOneWidget);
    });

    testWidgets('should display retry button when onRetry is provided', (
      tester,
    ) async {
      bool retryPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              onRetry: () => retryPressed = true,
            ),
          ),
        ),
      );

      expect(find.text('Retry'), findsOneWidget);

      await tester.tap(find.text('Retry'));
      expect(retryPressed, isTrue);
    });

    testWidgets('should show loading state when isRetrying is true', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              onRetry: () {},
              isRetrying: true,
            ),
          ),
        ),
      );

      expect(find.text('Retrying...'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);

      // The button should still exist - check that it contains the correct text and loading indicator
      expect(find.text('Retrying...'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should not show retry button when onRetry is null', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
            ),
          ),
        ),
      );

      expect(find.byType(ElevatedButton), findsNothing);
    });

    testWidgets('should use custom icon, size, and color', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              icon: Icons.wifi_off,
              iconSize: 100.0,
              iconColor: Colors.red,
            ),
          ),
        ),
      );

      final iconWidget = tester.widget<Icon>(find.byIcon(Icons.wifi_off));
      expect(iconWidget.size, equals(100.0));
      expect(iconWidget.color, equals(Colors.red));
    });

    testWidgets('should use custom text styles', (tester) async {
      const customTitleStyle = TextStyle(fontSize: 30, color: Colors.blue);
      const customMessageStyle = TextStyle(fontSize: 18, color: Colors.green);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              titleStyle: customTitleStyle,
              messageStyle: customMessageStyle,
            ),
          ),
        ),
      );

      final titleText = tester.widget<Text>(find.text('Test Error'));
      final messageText = tester.widget<Text>(find.text('Test error message'));

      expect(titleText.style?.fontSize, equals(30));
      expect(titleText.style?.color, equals(Colors.blue));
      expect(messageText.style?.fontSize, equals(18));
      expect(messageText.style?.color, equals(Colors.green));
    });

    testWidgets('should use custom retry button text', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              onRetry: () {},
              retryButtonText: 'Try Again',
            ),
          ),
        ),
      );

      expect(find.text('Try Again'), findsOneWidget);
    });

    testWidgets('should not center content when centered is false', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              centered: false,
            ),
          ),
        ),
      );

      // When not centered, there should be no Center widget wrapping the content
      final paddingWidget = find.byType(Padding);
      expect(paddingWidget, findsOneWidget);

      final padding = tester.widget<Padding>(paddingWidget);
      expect(padding.child, isA<Column>());
    });

    testWidgets('should use custom padding', (tester) async {
      const customPadding = EdgeInsets.all(50.0);

      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              padding: customPadding,
            ),
          ),
        ),
      );

      final paddingWidget = tester.widget<Padding>(find.byType(Padding));
      expect(paddingWidget.padding, equals(customPadding));
    });
  });

  group('GHErrorStates factory methods', () {
    testWidgets('networkError should create appropriate error state', (
      tester,
    ) async {
      bool retryPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.networkError(
              onRetry: () => retryPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.wifi_off_outlined), findsOneWidget);
      expect(find.text('Connection Error'), findsOneWidget);
      expect(
        find.text(
          'Unable to connect to GitHub. Please check your internet connection and try again.',
        ),
        findsOneWidget,
      );
      expect(find.text('Retry'), findsOneWidget);

      await tester.tap(find.text('Retry'));
      expect(retryPressed, isTrue);
    });

    testWidgets('serverError should create appropriate error state', (
      tester,
    ) async {
      bool retryPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.serverError(onRetry: () => retryPressed = true),
          ),
        ),
      );

      expect(find.byIcon(Icons.cloud_off_outlined), findsOneWidget);
      expect(find.text('Server Error'), findsOneWidget);
      expect(
        find.text(
          'GitHub servers are currently experiencing issues. Please try again in a few moments.',
        ),
        findsOneWidget,
      );

      await tester.tap(find.text('Retry'));
      expect(retryPressed, isTrue);
    });

    testWidgets('notFoundError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.notFoundError(resourceType: 'repository'),
          ),
        ),
      );

      expect(find.byIcon(Icons.search_off_outlined), findsOneWidget);
      expect(find.text('Repository Not Found'), findsOneWidget);
      expect(
        find.text(
          'The repository you\'re looking for doesn\'t exist or has been moved.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('forbiddenError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHErrorStates.forbiddenError())),
      );

      expect(find.byIcon(Icons.lock_outlined), findsOneWidget);
      expect(find.text('Access Denied'), findsOneWidget);
      expect(
        find.text(
          'You don\'t have permission to access this resource. Please check your access rights.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('rateLimitError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHErrorStates.rateLimitError())),
      );

      expect(find.byIcon(Icons.hourglass_empty_outlined), findsOneWidget);
      expect(find.text('Rate Limit Exceeded'), findsOneWidget);
      expect(
        find.text(
          'You\'ve exceeded the API rate limit. Please wait before making more requests.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('rateLimitError with reset time should show countdown', (
      tester,
    ) async {
      final resetTime = DateTime.now().add(
        const Duration(minutes: 5, seconds: 30),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.rateLimitError(resetTime: resetTime),
          ),
        ),
      );

      expect(find.text('Rate Limit Exceeded'), findsOneWidget);
      expect(
        find.textContaining('Rate limit will reset in 5m'),
        findsOneWidget,
      );
    });

    testWidgets('authenticationError should create appropriate error state', (
      tester,
    ) async {
      bool signInPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.authenticationError(
              onRetry: () => signInPressed = true,
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.person_off_outlined), findsOneWidget);
      expect(find.text('Authentication Required'), findsOneWidget);
      expect(
        find.text('Please sign in to access this content.'),
        findsOneWidget,
      );
      expect(find.text('Sign In'), findsOneWidget);

      await tester.tap(find.text('Sign In'));
      expect(signInPressed, isTrue);
    });

    testWidgets('repositoryLoadError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHErrorStates.repositoryLoadError())),
      );

      expect(find.byIcon(Icons.folder_off_outlined), findsOneWidget);
      expect(find.text('Unable to Load Repository'), findsOneWidget);
      expect(
        find.text(
          'There was a problem loading the repository. Please try again.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('issuesLoadError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: GHErrorStates.issuesLoadError())),
      );

      expect(find.byIcon(Icons.bug_report_outlined), findsOneWidget);
      expect(find.text('Unable to Load Issues'), findsOneWidget);
      expect(
        find.text('There was a problem loading the issues. Please try again.'),
        findsOneWidget,
      );
    });

    testWidgets('pullRequestsLoadError should create appropriate error state', (
      tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(body: GHErrorStates.pullRequestsLoadError()),
        ),
      );

      expect(find.byIcon(Icons.merge_type_outlined), findsOneWidget);
      expect(find.text('Unable to Load Pull Requests'), findsOneWidget);
      expect(
        find.text(
          'There was a problem loading the pull requests. Please try again.',
        ),
        findsOneWidget,
      );
    });

    testWidgets('genericError should create custom error state', (
      tester,
    ) async {
      bool retryPressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorStates.genericError(
              title: 'Custom Error',
              message: 'Custom error message',
              icon: Icons.warning_outlined,
              onRetry: () => retryPressed = true,
              retryButtonText: 'Try Again',
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.warning_outlined), findsOneWidget);
      expect(find.text('Custom Error'), findsOneWidget);
      expect(find.text('Custom error message'), findsOneWidget);
      expect(find.text('Try Again'), findsOneWidget);

      await tester.tap(find.text('Try Again'));
      expect(retryPressed, isTrue);
    });
  });

  group('GHErrorState design token compliance', () {
    testWidgets('should use correct spacing between elements', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
              onRetry: () {},
            ),
          ),
        ),
      );

      final sizedBoxes = find.byType(SizedBox);
      expect(sizedBoxes, findsNWidgets(6));

      final sizedBoxList = tester.widgetList<SizedBox>(sizedBoxes).toList();
      // Skip the first SizedBox which is the icon's intrinsic size
      expect(sizedBoxList[1].height, equals(GHTokens.spacing16));

      // Check spacing between title and message (8dp)
      expect(sizedBoxList[2].height, equals(GHTokens.spacing8));

      // Check spacing between message and retry button (24dp)
      expect(sizedBoxList[3].height, equals(GHTokens.spacing24));
    });

    testWidgets('should use default padding from design tokens', (
      tester,
    ) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: GHErrorState(
              title: 'Test Error',
              message: 'Test error message',
            ),
          ),
        ),
      );

      final paddingWidget = tester.widget<Padding>(find.byType(Padding));
      expect(
        paddingWidget.padding,
        equals(const EdgeInsets.all(GHTokens.spacing24)),
      );
    });
  });
}
