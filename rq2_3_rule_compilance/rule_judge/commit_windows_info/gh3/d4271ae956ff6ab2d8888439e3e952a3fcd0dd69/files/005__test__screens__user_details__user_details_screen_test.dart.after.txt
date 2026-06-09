import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:gh3/src/screens/user_details/user_details_screen.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel.dart';

import 'user_details_screen_test.mocks.dart';

@GenerateMocks([UserDetailsViewModel])
void main() {
  group('UserDetailsScreen', () {
    late MockUserDetailsViewModel mockUserDetailsViewModel;

    setUp(() {
      mockUserDetailsViewModel = MockUserDetailsViewModel();
      when(mockUserDetailsViewModel.login).thenReturn('testuser');
      when(mockUserDetailsViewModel.isLoading).thenReturn(false);
    });

    testWidgets('renders user details screen with app bar', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
        ),
      );

      expect(find.text('User Details'), findsOneWidget);
      expect(find.byType(AppBar), findsOneWidget);
      expect(find.byType(BackButton), findsOneWidget);
    });

    testWidgets('shows loading indicator when loading', (
      WidgetTester tester,
    ) async {
      when(mockUserDetailsViewModel.isLoading).thenReturn(true);

      await tester.pumpWidget(
        MaterialApp(
          home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows user login when not loading', (
      WidgetTester tester,
    ) async {
      when(mockUserDetailsViewModel.isLoading).thenReturn(false);
      when(mockUserDetailsViewModel.login).thenReturn('testuser');

      await tester.pumpWidget(
        MaterialApp(
          home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
        ),
      );

      expect(find.text('User: testuser'), findsOneWidget);
    });

    testWidgets('calls init on ViewModel during initState', (
      WidgetTester tester,
    ) async {
      await tester.pumpWidget(
        MaterialApp(
          home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
        ),
      );

      verify(mockUserDetailsViewModel.init()).called(1);
    });

    group('Lifecycle Management', () {
      testWidgets('should add listeners properly', (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
          ),
        );

        // Verify that the viewModel was set up with listeners
        verify(mockUserDetailsViewModel.addListener(any)).called(1);
      });

      testWidgets('should remove listeners when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
          ),
        );
        await tester.pumpWidget(Container()); // Replace with empty widget

        verify(mockUserDetailsViewModel.removeListener(any)).called(1);
      });

      testWidgets('should dispose ViewModel when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(
            home: UserDetailsScreen(viewModel: mockUserDetailsViewModel),
          ),
        );
        await tester.pumpWidget(Container()); // Replace with empty widget

        // Verify that the ViewModel's dispose method was called
        verify(mockUserDetailsViewModel.dispose()).called(1);
      });
    });
  });
}