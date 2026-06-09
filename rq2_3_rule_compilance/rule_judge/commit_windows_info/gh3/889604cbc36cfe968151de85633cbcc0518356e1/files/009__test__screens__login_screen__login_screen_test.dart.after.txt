import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:gh3/src/screens/login_screen/login_screen.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'login_screen_test.mocks.dart';

@GenerateMocks([GithubAuthClient, AuthService, AuthViewModel, LoginViewModel])
void main() {
  group('LoginScreen', () {
    late MockLoginViewModel mockLoginViewModel;

    setUp(() {
      mockLoginViewModel = MockLoginViewModel();
      when(mockLoginViewModel.userCode).thenReturn(null);
      when(mockLoginViewModel.isLoading).thenReturn(false);
      when(mockLoginViewModel.errorMessage).thenReturn(null);
      when(mockLoginViewModel.isAuthorized).thenReturn(false);
    });

    testWidgets('renders sign in button', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
      );
      expect(find.text('Sign in with GitHub'), findsOneWidget);
    });

    testWidgets('shows user code when available', (WidgetTester tester) async {
      when(mockLoginViewModel.userCode).thenReturn('ABC123');

      await tester.pumpWidget(
        MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
      );

      expect(find.text('Your user code is: ABC123'), findsOneWidget);
      expect(find.text('Copy and Open browser'), findsOneWidget);
    });

    testWidgets('shows loading state', (WidgetTester tester) async {
      when(mockLoginViewModel.isLoading).thenReturn(true);

      await tester.pumpWidget(
        MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows error message when present', (
      WidgetTester tester,
    ) async {
      when(mockLoginViewModel.errorMessage).thenReturn('Login failed');

      await tester.pumpWidget(
        MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
      );

      expect(find.text('Login failed'), findsOneWidget);
    });

    group('Lifecycle Management', () {
      testWidgets('should add listeners properly', (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
        );

        // Verify that the viewModel was set up with listeners
        verify(mockLoginViewModel.addListener(any)).called(1);
      });

      testWidgets('should remove listeners when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
        );
        await tester.pumpWidget(Container()); // Replace with empty widget

        verify(mockLoginViewModel.removeListener(any)).called(1);
      });

      testWidgets('should dispose ViewModel when widget is disposed', (
        WidgetTester tester,
      ) async {
        await tester.pumpWidget(
          MaterialApp(home: LoginScreen(viewModel: mockLoginViewModel)),
        );
        await tester.pumpWidget(Container()); // Replace with empty widget

        // Verify that the ViewModel's dispose method was called
        verify(mockLoginViewModel.dispose()).called(1);
      });
    });
  });
}
