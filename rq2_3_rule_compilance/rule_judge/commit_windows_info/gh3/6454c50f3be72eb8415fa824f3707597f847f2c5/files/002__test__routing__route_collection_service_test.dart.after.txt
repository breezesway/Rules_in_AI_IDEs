import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:go_router/go_router.dart';
import 'package:get_it/get_it.dart';

import 'package:gh3/src/routing/routing.dart';

import 'route_collection_service_test.mocks.dart';

@GenerateMocks([RouteProvider])
void main() {
  group('RouteCollectionService', () {
    late RouteCollectionService service;
    late GetIt getIt;

    setUp(() {
      getIt = GetIt.instance;
      getIt.reset();
      service = RouteCollectionService();
    });

    tearDown(() {
      getIt.reset();
    });

    test('should return empty list when no route providers are registered', () {
      final routes = service.collectRoutes();
      expect(routes, isEmpty);
    });

    test('should collect routes from registered providers', () {
      // Arrange
      final mockProvider1 = MockRouteProvider();
      final mockProvider2 = MockRouteProvider();

      final route1 = GoRoute(
        path: '/test1',
        builder: (context, state) => const SizedBox(),
      );
      final route2 = GoRoute(
        path: '/test2',
        builder: (context, state) => const SizedBox(),
      );

      when(mockProvider1.getRoute()).thenReturn(route1);
      when(mockProvider2.getRoute()).thenReturn(route2);

      getIt.registerSingleton<RouteProvider>(
        mockProvider1,
        instanceName: 'provider1',
      );
      getIt.registerSingleton<RouteProvider>(
        mockProvider2,
        instanceName: 'provider2',
      );

      // Act
      final routes = service.collectRoutes();

      // Assert
      expect(routes, hasLength(2));
      expect(routes, contains(route1));
      expect(routes, contains(route2));
    });

    test('should sort routes by specificity with literal segments having higher priority', () {
      // Arrange
      final mockProvider1 = MockRouteProvider();
      final mockProvider2 = MockRouteProvider();
      final mockProvider3 = MockRouteProvider();

      final parameterizedRoute = GoRoute(
        path: '/:login',
        builder: (context, state) => const SizedBox(),
      );
      final literalRoute = GoRoute(
        path: '/loading',
        builder: (context, state) => const SizedBox(),
      );
      final complexRoute = GoRoute(
        path: '/users/:id/profile',
        builder: (context, state) => const SizedBox(),
      );

      when(mockProvider1.getRoute()).thenReturn(parameterizedRoute);
      when(mockProvider2.getRoute()).thenReturn(literalRoute);
      when(mockProvider3.getRoute()).thenReturn(complexRoute);

      getIt.registerSingleton<RouteProvider>(
        mockProvider1,
        instanceName: 'provider1',
      );
      getIt.registerSingleton<RouteProvider>(
        mockProvider2,
        instanceName: 'provider2',
      );
      getIt.registerSingleton<RouteProvider>(
        mockProvider3,
        instanceName: 'provider3',
      );

      // Act
      final routes = service.collectRoutes();

      // Assert
      expect(routes, hasLength(3));
      
      // Extract paths for easier testing
      final paths = routes.map((r) => (r as GoRoute).path).toList();
      
      // Most specific should come first: /users/:id/profile (2 literal + 1 param + length)
      // Then: /loading (1 literal)
      // Then: /:login (1 param)
      expect(paths[0], equals('/users/:id/profile'));
      expect(paths[1], equals('/loading'));
      expect(paths[2], equals('/:login'));
    });
  });
}
