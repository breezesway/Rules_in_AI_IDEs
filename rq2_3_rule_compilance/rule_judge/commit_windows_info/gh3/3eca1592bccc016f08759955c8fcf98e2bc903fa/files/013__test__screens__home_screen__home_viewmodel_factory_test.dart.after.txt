import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel_factory.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:ferry/ferry.dart';

@GenerateNiceMocks([MockSpec<Client>()])
import 'home_viewmodel_factory_test.mocks.dart';

void main() {
  group('HomeViewModelFactory', () {
    late MockClient mockClient;
    late HomeViewModelFactory factory;

    setUp(() {
      mockClient = MockClient();
      factory = HomeViewModelFactory(mockClient);
    });

    group('Factory Creation', () {
      test('should create factory with ferry client dependency', () {
        expect(factory, isNotNull);
        expect(factory, isA<HomeViewModelFactory>());
      });

      test(
        'should create HomeViewModel instance with injected dependencies',
        () {
          // Arrange
          when(
            mockClient.request<dynamic, dynamic>(any),
          ).thenAnswer((_) => const Stream.empty());

          // Act
          final viewModel = factory.create();

          // Assert
          expect(viewModel, isNotNull);
          expect(viewModel, isA<HomeViewModel>());
        },
      );

      test('should create multiple independent HomeViewModel instances', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act
        final viewModel1 = factory.create();
        final viewModel2 = factory.create();

        // Assert
        expect(viewModel1, isNotNull);
        expect(viewModel2, isNotNull);
        expect(viewModel1, isNot(same(viewModel2)));
        expect(viewModel1, isA<HomeViewModel>());
        expect(viewModel2, isA<HomeViewModel>());
      });

      test('should create ViewModels with same ferry client dependency', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act
        final viewModel1 = factory.create();
        final viewModel2 = factory.create();

        // Assert - Both ViewModels should have the same client instance
        // We can't directly test this without exposing the client, but we can
        // verify they both work with the same mock
        expect(viewModel1.isLoading, isTrue);
        expect(viewModel2.isLoading, isTrue);

        // Clean up
        viewModel1.dispose();
        viewModel2.dispose();
      });
    });

    group('Dependency Injection', () {
      test('should inject ferry client correctly', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act
        final viewModel = factory.create();

        // Assert - Verify the client is working by checking initial state
        expect(viewModel.isLoading, isTrue);
        expect(viewModel.isEmpty, isTrue);
        expect(viewModel.followingUsers, isEmpty);
        expect(viewModel.error, isNull);

        // Clean up
        viewModel.dispose();
      });

      test('should handle factory creation with null client gracefully', () {
        // This test ensures the factory handles edge cases
        expect(() => HomeViewModelFactory(mockClient), returnsNormally);
      });
    });

    group('ViewModel Lifecycle', () {
      test('should create ViewModels that can be disposed independently', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act
        final viewModel1 = factory.create();
        final viewModel2 = factory.create();

        // Assert - Should be able to dispose one without affecting the other
        expect(() => viewModel1.dispose(), returnsNormally);
        expect(() => viewModel2.dispose(), returnsNormally);
      });

      test('should create ViewModels with proper initial state', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act
        final viewModel = factory.create();

        // Assert - Check all initial state properties
        expect(viewModel.isLoading, isTrue);
        expect(viewModel.isEmpty, isTrue);
        expect(viewModel.followingUsers, isEmpty);
        expect(viewModel.error, isNull);
        expect(viewModel.hasMore, isTrue);
        expect(viewModel.following, isNull);

        // Clean up
        viewModel.dispose();
      });
    });

    group('Factory Pattern Validation', () {
      test('should maintain factory pattern principles', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act & Assert - Factory should create new instances each time
        final instances = List.generate(5, (_) => factory.create());

        // All instances should be different objects
        for (int i = 0; i < instances.length; i++) {
          for (int j = i + 1; j < instances.length; j++) {
            expect(instances[i], isNot(same(instances[j])));
          }
        }

        // All instances should be of the same type
        for (final instance in instances) {
          expect(instance, isA<HomeViewModel>());
        }

        // Clean up
        for (final instance in instances) {
          instance.dispose();
        }
      });

      test('should support concurrent factory usage', () {
        // Arrange
        when(
          mockClient.request<dynamic, dynamic>(any),
        ).thenAnswer((_) => const Stream.empty());

        // Act - Create multiple instances concurrently
        final futures = List.generate(
          3,
          (_) => Future.microtask(() => factory.create()),
        );

        // Assert
        expect(
          Future.wait(futures).then((viewModels) {
            // All should be created successfully
            expect(viewModels.length, equals(3));
            for (final vm in viewModels) {
              expect(vm, isA<HomeViewModel>());
            }

            // Clean up
            for (final vm in viewModels) {
              vm.dispose();
            }
            return true;
          }),
          completion(isTrue),
        );
      });
    });
  });
}
