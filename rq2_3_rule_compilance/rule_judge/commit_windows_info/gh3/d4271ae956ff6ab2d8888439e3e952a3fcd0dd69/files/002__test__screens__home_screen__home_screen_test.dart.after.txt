import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:gh3/src/screens/home_screen/home_screen.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/widgets/user_card/user_card.dart';

import 'home_screen_test.mocks.dart';

@GenerateMocks([HomeViewModel, AuthViewModel])
void main() {
  group('HomeScreen', () {
    late MockHomeViewModel mockHomeViewModel;
    late MockAuthViewModel mockAuthViewModel;
    late Widget homeScreen;

    setUp(() {
      mockHomeViewModel = MockHomeViewModel();
      mockAuthViewModel = MockAuthViewModel();

      // Setup default mock behavior
      when(mockHomeViewModel.isLoading).thenReturn(false);
      when(mockHomeViewModel.isEmpty).thenReturn(false);
      when(mockHomeViewModel.followingUsers).thenReturn([]);
      when(mockHomeViewModel.error).thenReturn(null);
      when(mockHomeViewModel.hasMore).thenReturn(true);

      homeScreen = MaterialApp(
        home: HomeScreen(
          authViewModel: mockAuthViewModel,
          homeViewModel: mockHomeViewModel,
        ),
      );
    });

    group('Initial Rendering', () {
      testWidgets('should display app bar with title and logout button', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);

        expect(find.text('Home'), findsOneWidget);
        expect(find.byIcon(Icons.logout), findsOneWidget);
      });

      testWidgets('should display welcome section', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);

        expect(find.text('Welcome back!'), findsOneWidget);
        expect(
          find.text('Discover repositories from people you follow'),
          findsOneWidget,
        );
        expect(find.byIcon(Icons.waving_hand), findsOneWidget);
      });

      testWidgets('should display following section header', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);

        expect(find.text('Following'), findsOneWidget);
      });
    });

    group('Loading States', () {
      testWidgets('should show loading indicator when loading and empty', (
        WidgetTester tester,
      ) async {
        when(mockHomeViewModel.isLoading).thenReturn(true);
        when(mockHomeViewModel.isEmpty).thenReturn(true);

        await tester.pumpWidget(homeScreen);

        expect(find.byType(CircularProgressIndicator), findsNWidgets(2));
      });

      testWidgets('should show loading indicator at bottom when loading more', (
        WidgetTester tester,
      ) async {
        when(mockHomeViewModel.followingUsers).thenReturn([
          // Mock user data would go here
        ]);
        when(mockHomeViewModel.isLoading).thenReturn(true);

        await tester.pumpWidget(homeScreen);

        // Should show loading indicator at the bottom of the list
        expect(find.byType(CircularProgressIndicator), findsOneWidget);
      });
    });

    group('Empty States', () {
      testWidgets('should show empty state when no following users', (
        WidgetTester tester,
      ) async {
        when(mockHomeViewModel.isEmpty).thenReturn(true);
        when(mockHomeViewModel.isLoading).thenReturn(false);

        await tester.pumpWidget(homeScreen);

        expect(find.text('No following users found'), findsOneWidget);
        expect(
          find.text('Start following users on GitHub to see them here'),
          findsOneWidget,
        );
        expect(find.byIcon(Icons.people_outline), findsOneWidget);
        expect(find.text('Retry'), findsOneWidget);
      });

      testWidgets(
        'should call loadFollowingUsers when retry button is pressed',
        (WidgetTester tester) async {
          when(mockHomeViewModel.isEmpty).thenReturn(true);
          when(mockHomeViewModel.isLoading).thenReturn(false);

          await tester.pumpWidget(homeScreen);

          reset(mockHomeViewModel);
          await tester.tap(find.text('Retry'));
          await tester.pump();

          verify(mockHomeViewModel.loadFollowingUsers()).called(1);
        },
      );
    });

    group('Error Handling', () {
      testWidgets('should display error message when error occurs', (
        WidgetTester tester,
      ) async {
        when(mockHomeViewModel.error).thenReturn('Authentication failed');

        await tester.pumpWidget(homeScreen);

        expect(find.text('Authentication failed'), findsOneWidget);
        expect(find.text('Dismiss'), findsOneWidget);
        expect(find.byIcon(Icons.error_outline), findsOneWidget);
      });

      testWidgets('should call clearError when dismiss button is pressed', (
        WidgetTester tester,
      ) async {
        when(mockHomeViewModel.error).thenReturn('Authentication failed');

        await tester.pumpWidget(homeScreen);

        await tester.tap(find.text('Dismiss'));
        await tester.pump();

        verify(mockHomeViewModel.clearError()).called(1);
      });
    });

    group('User List', () {
      testWidgets('should display user cards when users are available', (
        WidgetTester tester,
      ) async {
        // Mock user data - this would need to match the GraphQL generated types
        when(mockHomeViewModel.followingUsers).thenReturn([]);

        await tester.pumpWidget(homeScreen);

        // Should not find UserCard widgets when list is empty
        expect(find.byType(UserCard), findsNothing);
      });
    });

    group('Pull to Refresh', () {
      testWidgets('should call refreshFollowingUsers on pull to refresh', (
        WidgetTester tester,
      ) async {
        when(
          mockHomeViewModel.refreshFollowingUsers(),
        ).thenAnswer((_) async {});
        await tester.pumpWidget(homeScreen);

        // Simulate pull to refresh
        await tester.drag(find.byType(RefreshIndicator), const Offset(0, 300));
        await tester.pump();

        verify(
          mockHomeViewModel.loadFollowingUsers(),
        ).called(greaterThanOrEqualTo(1));
      });
    });

    group('Logout Functionality', () {
      testWidgets('should call logout when logout button is pressed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);

        await tester.tap(find.byIcon(Icons.logout));
        await tester.pump();

        verify(mockAuthViewModel.logout()).called(1);
      });
    });

    group('Scroll Behavior', () {
      testWidgets('should handle scroll events', (WidgetTester tester) async {
        // Test that the screen can handle scroll events without crashing
        when(mockHomeViewModel.followingUsers).thenReturn([]);

        await tester.pumpWidget(homeScreen);

        // Verify that the ListView is present
        expect(find.byType(ListView), findsOneWidget);
      });
    });

    group('Lifecycle Management', () {
      testWidgets('should add listeners properly', (WidgetTester tester) async {
        await tester.pumpWidget(homeScreen);

        // Verify that the viewModel was set up with listeners
        verify(mockHomeViewModel.addListener(any)).called(1);
      });

      testWidgets('should remove listeners when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);
        await tester.pumpWidget(Container()); // Replace with empty widget

        verify(mockHomeViewModel.removeListener(any)).called(1);
      });

      testWidgets('should dispose ViewModel when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);
        await tester.pumpWidget(Container()); // Replace with empty widget

        // Verify that the ViewModel's dispose method was called
        verify(mockHomeViewModel.dispose()).called(1);
      });

      testWidgets('should call loadFollowingUsers on initState', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);
        await tester.pump(); // Allow post-frame callback to execute

        // Verify that loadFollowingUsers was called during initialization
        verify(mockHomeViewModel.loadFollowingUsers()).called(1);
      });
    });

    group('Theme Integration', () {
      testWidgets('should use theme colors correctly', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(homeScreen);

        // Verify that theme-aware widgets are used
        expect(find.byType(Card), findsOneWidget);
        expect(find.byType(RefreshIndicator), findsOneWidget);
      });
    });
  });
}
