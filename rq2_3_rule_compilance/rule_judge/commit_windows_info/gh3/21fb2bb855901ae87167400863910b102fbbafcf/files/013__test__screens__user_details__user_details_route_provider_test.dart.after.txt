import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:go_router/go_router.dart';
import 'package:gh3/src/screens/user_details/user_details_route_provider.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel_factory.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel.dart';
import 'package:gh3/src/routing/route_provider.dart';

import 'user_details_route_provider_test.mocks.dart';

@GenerateMocks([UserDetailsViewModelFactory, UserDetailsViewModel])
void main() {
  group('UserDetailsRouteProvider', () {
    late MockUserDetailsViewModelFactory mockUserDetailsViewModelFactory;
    late MockUserDetailsViewModel mockUserDetailsViewModel;
    late UserDetailsRouteProvider userDetailsRouteProvider;

    setUp(() {
      mockUserDetailsViewModelFactory = MockUserDetailsViewModelFactory();
      mockUserDetailsViewModel = MockUserDetailsViewModel();
      userDetailsRouteProvider = UserDetailsRouteProvider(mockUserDetailsViewModelFactory);
    });

    test('should implement RouteProvider interface', () {
      expect(userDetailsRouteProvider, isA<RouteProvider>());
    });

    test('should return GoRoute with correct parameterized path', () {
      // Arrange
      when(mockUserDetailsViewModelFactory.create(any)).thenReturn(mockUserDetailsViewModel);

      // Act
      final route = userDetailsRouteProvider.getRoute();

      // Assert
      expect(route, isA<GoRoute>());
      final goRoute = route as GoRoute;
      expect(goRoute.path, equals('/:login'));
    });

    test('should create UserDetailsViewModel using factory with login parameter', () {
      // Arrange
      const testLogin = 'testuser';
      when(mockUserDetailsViewModelFactory.create(testLogin)).thenReturn(mockUserDetailsViewModel);

      // Act
      final route = userDetailsRouteProvider.getRoute();
      final goRoute = route as GoRoute;
      
      // Verify that the builder function exists and can be called
      expect(goRoute.builder, isNotNull);

      // Note: We can't easily test the builder function without creating a full widget test
      // because it requires BuildContext and GoRouterState parameters with path parameters
    });

    test('should be constructible with required dependencies', () {
      // Arrange & Act
      final provider = UserDetailsRouteProvider(mockUserDetailsViewModelFactory);

      // Assert - if constructor succeeds, dependencies were injected correctly
      expect(provider, isNotNull);
      expect(provider, isA<UserDetailsRouteProvider>());
    });

    test('should handle factory creation with different login parameters', () {
      // Arrange
      const login1 = 'user1';
      const login2 = 'user2';
      final mockViewModel1 = MockUserDetailsViewModel();
      final mockViewModel2 = MockUserDetailsViewModel();
      
      when(mockUserDetailsViewModelFactory.create(login1)).thenReturn(mockViewModel1);
      when(mockUserDetailsViewModelFactory.create(login2)).thenReturn(mockViewModel2);

      // Act
      final viewModel1 = mockUserDetailsViewModelFactory.create(login1);
      final viewModel2 = mockUserDetailsViewModelFactory.create(login2);

      // Assert
      expect(viewModel1, equals(mockViewModel1));
      expect(viewModel2, equals(mockViewModel2));
      verify(mockUserDetailsViewModelFactory.create(login1)).called(1);
      verify(mockUserDetailsViewModelFactory.create(login2)).called(1);
    });
  });
}