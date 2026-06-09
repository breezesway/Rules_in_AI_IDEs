import 'package:flutter_test/flutter_test.dart';
import 'package:ferry/ferry.dart';
import 'package:mockito/mockito.dart';

import 'package:gh3/src/screens/user_details/user_details_viewmodel_factory.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel.dart';

class MockFerryClient extends Mock implements Client {}

void main() {
  group('UserDetailsViewModelFactory', () {
    late UserDetailsViewModelFactory factory;
    late MockFerryClient mockFerryClient;

    setUp(() {
      mockFerryClient = MockFerryClient();
      factory = UserDetailsViewModelFactory(mockFerryClient);
    });

    test('should create UserDetailsViewModel with correct type', () {
      // Act
      final viewModel = factory.create('testuser');

      // Assert
      expect(viewModel, isA<UserDetailsViewModel>());
    });

    test('should create UserDetailsViewModel with correct login', () {
      // Arrange
      const login = 'testuser';

      // Act
      final viewModel = factory.create(login);

      // Assert
      expect(viewModel.login, login);
    });

    test(
      'should create multiple independent UserDetailsViewModel instances',
      () {
        // Act
        final viewModel1 = factory.create('user1');
        final viewModel2 = factory.create('user2');

        // Assert
        expect(viewModel1, isA<UserDetailsViewModel>());
        expect(viewModel2, isA<UserDetailsViewModel>());
        expect(viewModel1, isNot(same(viewModel2)));
        expect(viewModel1.login, 'user1');
        expect(viewModel2.login, 'user2');
      },
    );
  });
}
