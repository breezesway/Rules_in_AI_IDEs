import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel_factory.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:mockito/annotations.dart';

@GenerateNiceMocks([MockSpec<AuthService>()])
import 'home_viewmodel_factory_test.mocks.dart';

void main() {
  group('HomeViewModelFactory', () {
    late MockAuthService mockAuthService;
    late HomeViewModelFactory factory;

    setUp(() {
      mockAuthService = MockAuthService();
      factory = HomeViewModelFactory(mockAuthService);
    });

    group('Factory Creation', () {
      test('should create factory with AuthService dependency', () {
        expect(factory, isNotNull);
        expect(factory, isA<HomeViewModelFactory>());
      });

      test('should create HomeViewModel instance with injected dependencies', () {
        // Act
        final viewModel = factory.create();

        // Assert
        expect(viewModel, isNotNull);
        expect(viewModel, isA<HomeViewModel>());
        
        // Clean up
        viewModel.dispose();
      });

      test('should create multiple independent HomeViewModel instances', () {
        // Act
        final viewModel1 = factory.create();
        final viewModel2 = factory.create();

        // Assert
        expect(viewModel1, isNotNull);
        expect(viewModel2, isNotNull);
        expect(viewModel1, isNot(same(viewModel2)));
        expect(viewModel1, isA<HomeViewModel>());
        expect(viewModel2, isA<HomeViewModel>());
        
        // Clean up
        viewModel1.dispose();
        viewModel2.dispose();
      });
    });

    group('Dependency Injection', () {
      test('should inject AuthService correctly', () {
        // Act
        final viewModel = factory.create();

        // Assert - Verify the ViewModel provides expected placeholder data
        expect(viewModel.currentUserName, equals('GitHub User'));
        expect(viewModel.currentUserLogin, equals('githubuser'));
        expect(viewModel.currentUserAvatar, isNull);

        // Clean up
        viewModel.dispose();
      });
    });

    group('ViewModel Lifecycle', () {
      test('should create ViewModels that can be disposed independently', () {
        // Act
        final viewModel1 = factory.create();
        final viewModel2 = factory.create();

        // Assert - Should be able to dispose one without affecting the other
        expect(() => viewModel1.dispose(), returnsNormally);
        expect(() => viewModel2.dispose(), returnsNormally);
      });

      test('should create ViewModels with proper initial state', () {
        // Act
        final viewModel = factory.create();

        // Assert - Check all initial state properties
        expect(viewModel.currentUserName, equals('GitHub User'));
        expect(viewModel.currentUserLogin, equals('githubuser'));
        expect(viewModel.currentUserAvatar, isNull);

        // Clean up
        viewModel.dispose();
      });
    });

    group('Factory Pattern Validation', () {
      test('should maintain factory pattern principles', () {
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
    });
  });
}
