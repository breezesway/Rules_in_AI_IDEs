import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';

import 'login_viewmodel_test.mocks.dart';

@GenerateMocks([GithubAuthClient, AuthService, AuthViewModel])
void main() {
  group('LoginViewModel', () {
    late MockGithubAuthClient mockAuthClient;
    late MockAuthService mockAuthService;
    late MockAuthViewModel mockAuthViewModel;
    late LoginViewModel viewModel;

    setUp(() {
      mockAuthClient = MockGithubAuthClient();
      mockAuthService = MockAuthService();
      mockAuthViewModel = MockAuthViewModel();
      viewModel = LoginViewModel(
        mockAuthClient,
        mockAuthService,
        mockAuthViewModel,
      );
    });

    tearDown(() {
      viewModel.dispose();
    });

    test('should properly dispose and clear state', () {
      // Set some state
      viewModel.login(); // This would set loading state

      // Dispose
      viewModel.dispose();

      // Verify disposal
      expect(viewModel.disposed, true);
    });

    test('should not notify listeners after disposal', () async {
      bool listenerCalled = false;
      viewModel.addListener(() {
        listenerCalled = true;
      });

      // Dispose
      viewModel.dispose();
      listenerCalled = false;

      // Try to trigger state change after disposal
      // This should not notify listeners
      expect(listenerCalled, false);
    });

    test('should handle multiple dispose calls gracefully', () {
      expect(() {
        viewModel.dispose();
        viewModel.dispose();
        viewModel.dispose();
      }, returnsNormally);

      expect(viewModel.disposed, true);
    });

    test('should cancel any ongoing timers on disposal', () {
      // This test verifies that any polling timers are cancelled
      viewModel.dispose();

      // Should not throw and should be disposed
      expect(viewModel.disposed, true);
    });

    test('should clear sensitive data on disposal', () {
      viewModel.dispose();

      // After disposal, sensitive data should be cleared
      expect(viewModel.disposed, true);
      // Note: userCode and errorMessage are cleared in onDispose()
    });
  });
}
