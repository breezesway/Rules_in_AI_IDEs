import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateNiceMocks([MockSpec<AuthService>()])
import 'auth_viewmodel_test.mocks.dart';

void main() {
  group('AuthViewModel', () {
    late MockAuthService mockAuthService;
    late AuthViewModel viewModel;

    setUp(() {
      mockAuthService = MockAuthService();
      viewModel = AuthViewModel(mockAuthService);
    });

    tearDown(() {
      viewModel.dispose();
    });

    group('Initial State', () {
      test('should initialize with correct default values', () {
        expect(viewModel.loading, isTrue);
        expect(viewModel.loggedIn, isFalse);
        expect(viewModel.disposed, isFalse);
      });
    });

    group('Initialization', () {
      test('should update state after init', () async {
        // Arrange
        when(mockAuthService.init()).thenAnswer((_) async {});
        when(mockAuthService.isLoggedIn).thenReturn(true);

        // Act
        await viewModel.init();

        // Assert
        expect(viewModel.loading, isFalse);
        expect(viewModel.loggedIn, isTrue);
        verify(mockAuthService.init()).called(1);
      });
    });

    group('Logout', () {
      test('should update state after logout', () async {
        // Arrange
        when(mockAuthService.logout()).thenAnswer((_) async {});
        viewModel.loggedIn = true; // Set initial state

        // Act
        await viewModel.logout();

        // Assert
        expect(viewModel.loggedIn, isFalse);
        verify(mockAuthService.logout()).called(1);
      });
    });

    group('Auth State Update', () {
      test('should update logged in state', () {
        // Arrange
        when(mockAuthService.isLoggedIn).thenReturn(true);

        // Act
        viewModel.updateAuthState();

        // Assert
        expect(viewModel.loggedIn, isTrue);
      });
    });

    group('Disposal', () {
      test('should reset state on disposal', () {
        // Arrange - set some state
        viewModel.loading = false;
        viewModel.loggedIn = true;

        // Act - dispose the view model
        viewModel.dispose();

        // Assert - state should be reset
        expect(viewModel.disposed, isTrue);
      });

      test('should not notify listeners after disposal', () {
        // Arrange
        bool listenerCalled = false;
        viewModel.addListener(() {
          listenerCalled = true;
        });

        // Act - dispose the view model
        viewModel.dispose();

        // Try to notify listeners (this should not call the listener)
        viewModel.notifyListeners();

        // Assert
        expect(listenerCalled, isFalse);
        expect(viewModel.disposed, isTrue);
      });

      test('should handle multiple dispose calls gracefully', () {
        // Act - dispose multiple times
        viewModel.dispose();
        viewModel.dispose();
        viewModel.dispose();

        // Assert - should not throw and should remain disposed
        expect(viewModel.disposed, isTrue);
      });
    });
  });
}
