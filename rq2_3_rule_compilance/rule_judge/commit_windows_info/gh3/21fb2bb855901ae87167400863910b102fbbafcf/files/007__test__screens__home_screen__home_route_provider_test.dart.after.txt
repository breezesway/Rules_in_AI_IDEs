import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'package:gh3/src/routing/route_provider.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/screens/home_screen/home_route_provider.dart';
import 'package:gh3/src/screens/home_screen/home_screen.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel_factory.dart';

import 'home_route_provider_test.mocks.dart';

@GenerateMocks([HomeViewModelFactory, AuthViewModel, HomeViewModel, BuildContext, GoRouterState])
void main() {
  group('HomeRouteProvider', () {
    late MockHomeViewModelFactory mockHomeViewModelFactory;
    late MockAuthViewModel mockAuthViewModel;
    late MockHomeViewModel mockHomeViewModel;
    late MockBuildContext mockBuildContext;
    late MockGoRouterState mockGoRouterState;
    late HomeRouteProvider homeRouteProvider;

    setUp(() {
      mockHomeViewModelFactory = MockHomeViewModelFactory();
      mockAuthViewModel = MockAuthViewModel();
      mockHomeViewModel = MockHomeViewModel();
      mockBuildContext = MockBuildContext();
      mockGoRouterState = MockGoRouterState();
      homeRouteProvider = HomeRouteProvider(mockHomeViewModelFactory, mockAuthViewModel);
    });

    test('should implement RouteProvider interface', () {
      expect(homeRouteProvider, isA<RouteProvider>());
    });

    test('should return GoRoute with correct path', () {
      // Act
      final route = homeRouteProvider.getRoute();

      // Assert
      expect(route, isA<GoRoute>());
      final goRoute = route as GoRoute;
      expect(goRoute.path, equals('/'));
    });

    test('should create HomeViewModel using factory when building route', () {
      // Arrange
      when(mockHomeViewModelFactory.create()).thenReturn(mockHomeViewModel);

      // Act
      final route = homeRouteProvider.getRoute();
      final goRoute = route as GoRoute;
      
      // Build the widget to trigger factory call
      final widget = goRoute.builder!(mockBuildContext, mockGoRouterState);

      // Assert
      verify(mockHomeViewModelFactory.create()).called(1);
      expect(widget, isA<HomeScreen>());
    });

    test('should inject dependencies correctly into HomeScreen', () {
      // Arrange
      when(mockHomeViewModelFactory.create()).thenReturn(mockHomeViewModel);

      // Act
      final route = homeRouteProvider.getRoute();
      final goRoute = route as GoRoute;
      final widget = goRoute.builder!(mockBuildContext, mockGoRouterState) as HomeScreen;

      // Assert
      expect(widget.authViewModel, equals(mockAuthViewModel));
      expect(widget.homeViewModel, equals(mockHomeViewModel));
    });
  });
}