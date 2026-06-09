import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:go_router/go_router.dart';
import 'package:gh3/src/screens/loading_screen/loading_route_provider.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_provider.dart';

import 'loading_route_provider_test.mocks.dart';

@GenerateMocks([AuthViewModel])
void main() {
  group('LoadingRouteProvider', () {
    late MockAuthViewModel mockAuthViewModel;
    late LoadingRouteProvider loadingRouteProvider;

    setUp(() {
      mockAuthViewModel = MockAuthViewModel();
      loadingRouteProvider = LoadingRouteProvider(mockAuthViewModel);
    });

    test('should implement RouteProvider interface', () {
      expect(loadingRouteProvider, isA<RouteProvider>());
    });

    test('should return GoRoute with correct path', () {
      // Act
      final route = loadingRouteProvider.getRoute();

      // Assert
      expect(route, isA<GoRoute>());
      final goRoute = route as GoRoute;
      expect(goRoute.path, equals('/loading'));
    });

    test('should create route with builder function', () {
      // Act
      final route = loadingRouteProvider.getRoute();
      final goRoute = route as GoRoute;

      // Verify that the builder function exists and can be called
      expect(goRoute.builder, isNotNull);

      // Note: We can't easily test the builder function without creating a full widget test
      // because it requires BuildContext and GoRouterState parameters
    });

    test('should be constructible with required dependencies', () {
      // Arrange & Act
      final provider = LoadingRouteProvider(mockAuthViewModel);

      // Assert - if constructor succeeds, dependencies were injected correctly
      expect(provider, isNotNull);
      expect(provider, isA<LoadingRouteProvider>());
    });
  });
}
