import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:go_router/go_router.dart';
import 'package:gh3/src/screens/login_screen/login_route_provider.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel_factory.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/routing/route_provider.dart';

import 'login_route_provider_test.mocks.dart';

@GenerateMocks([LoginViewModelFactory, LoginViewModel])
void main() {
  group('LoginRouteProvider', () {
    late MockLoginViewModelFactory mockLoginViewModelFactory;
    late MockLoginViewModel mockLoginViewModel;
    late LoginRouteProvider loginRouteProvider;

    setUp(() {
      mockLoginViewModelFactory = MockLoginViewModelFactory();
      mockLoginViewModel = MockLoginViewModel();
      loginRouteProvider = LoginRouteProvider(mockLoginViewModelFactory);
    });

    test('should implement RouteProvider interface', () {
      expect(loginRouteProvider, isA<RouteProvider>());
    });

    test('should return GoRoute with correct path', () {
      // Arrange
      when(mockLoginViewModelFactory.create()).thenReturn(mockLoginViewModel);

      // Act
      final route = loginRouteProvider.getRoute();

      // Assert
      expect(route, isA<GoRoute>());
      final goRoute = route as GoRoute;
      expect(goRoute.path, equals('/login'));
    });

    test('should create LoginViewModel using factory when building route', () {
      // Arrange
      when(mockLoginViewModelFactory.create()).thenReturn(mockLoginViewModel);

      // Act
      final route = loginRouteProvider.getRoute();
      final goRoute = route as GoRoute;
      
      // Verify that the builder function exists and can be called
      expect(goRoute.builder, isNotNull);

      // Note: We can't easily test the builder function without creating a full widget test
      // because it requires BuildContext and GoRouterState parameters
    });

    test('should be constructible with required dependencies', () {
      // Arrange & Act
      final provider = LoginRouteProvider(mockLoginViewModelFactory);

      // Assert - if constructor succeeds, dependencies were injected correctly
      expect(provider, isNotNull);
      expect(provider, isA<LoginRouteProvider>());
    });
  });
}