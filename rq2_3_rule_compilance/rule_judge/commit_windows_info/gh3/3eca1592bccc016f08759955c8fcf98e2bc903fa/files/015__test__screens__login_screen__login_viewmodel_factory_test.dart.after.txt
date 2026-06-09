import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';

import 'package:gh3/src/screens/login_screen/login_viewmodel_factory.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';

import 'login_viewmodel_factory_test.mocks.dart';

@GenerateMocks([GithubAuthClient, AuthService, AuthViewModel])
void main() {
  group('LoginViewModelFactory', () {
    late MockGithubAuthClient mockAuthClient;
    late MockAuthService mockAuthService;
    late MockAuthViewModel mockAuthViewModel;
    late LoginViewModelFactory factory;

    setUp(() {
      mockAuthClient = MockGithubAuthClient();
      mockAuthService = MockAuthService();
      mockAuthViewModel = MockAuthViewModel();

      factory = LoginViewModelFactory(
        mockAuthClient,
        mockAuthService,
        mockAuthViewModel,
      );
    });

    test('should create LoginViewModel with correct type', () {
      // Act
      final viewModel = factory.create();

      // Assert
      expect(viewModel, isA<LoginViewModel>());
    });

    test('should create multiple independent LoginViewModel instances', () {
      // Act
      final viewModel1 = factory.create();
      final viewModel2 = factory.create();

      // Assert
      expect(viewModel1, isA<LoginViewModel>());
      expect(viewModel2, isA<LoginViewModel>());
      expect(viewModel1, isNot(same(viewModel2)));
    });
  });
}
