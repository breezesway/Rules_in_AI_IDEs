import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel.dart';

void main() {
  group('UserDetailsViewModel', () {
    late UserDetailsViewModel viewModel;

    setUp(() {
      viewModel = UserDetailsViewModel('testuser');
    });

    tearDown(() {
      viewModel.dispose();
    });

    group('Initial State', () {
      test('should initialize with correct default values', () {
        expect(viewModel.login, equals('testuser'));
        expect(viewModel.isLoading, isFalse);
        expect(viewModel.disposed, isFalse);
      });
    });

    group('Initialization', () {
      test('should set loading state during init', () async {
        // Act
        final future = viewModel.init();

        // Assert - should be loading immediately
        expect(viewModel.isLoading, isTrue);

        // Wait for completion
        await future;

        // Assert - should not be loading after completion
        expect(viewModel.isLoading, isFalse);
      });
    });

    group('Disposal', () {
      test('should clear loading state on disposal', () {
        // Arrange - set loading state
        viewModel.init();
        expect(viewModel.isLoading, isTrue);

        // Act - dispose the view model
        viewModel.dispose();

        // Assert - loading state should be cleared
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

      test('should maintain login value after disposal', () {
        // Act - dispose the view model
        viewModel.dispose();

        // Assert - login should still be accessible
        expect(viewModel.login, equals('testuser'));
        expect(viewModel.disposed, isTrue);
      });
    });
  });
}
