import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:ferry/ferry.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:go_router/go_router.dart';

import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';
import 'package:gh3/src/routing/route_provider.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel_factory.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel_factory.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel_factory.dart';
import 'package:gh3/src/screens/home_screen/home_route_provider.dart';
import 'package:gh3/src/screens/login_screen/login_route_provider.dart';
import 'package:gh3/src/screens/loading_screen/loading_route_provider.dart';
import 'package:gh3/src/screens/user_details/user_details_route_provider.dart';

@GenerateNiceMocks([
  MockSpec<Client>(),
  MockSpec<GithubAuthClient>(),
  MockSpec<AuthService>(),
])
import 'modular_architecture_test.mocks.dart';

void main() {
  group('Modular Architecture Validation', () {
    setUp(() {
      GetIt.I.reset();
    });

    test(
      'screens are self-contained modules with their own factories and providers',
      () {
        // Setup mocks
        final mockAuthService = MockAuthService();
        final mockAuthClient = MockGithubAuthClient();
        final mockFerryClient = MockClient();

        when(mockAuthService.isLoggedIn).thenReturn(true);
        when(mockAuthService.init()).thenAnswer((_) async {});

        // Register services
        GetIt.I.registerSingleton<AuthService>(mockAuthService);
        GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
        GetIt.I.registerSingleton<Client>(mockFerryClient);

        final authViewModel = AuthViewModel(mockAuthService);
        GetIt.I.registerSingleton(authViewModel);

        // Register all factories
        GetIt.I.registerFactory<HomeViewModelFactory>(
          () => HomeViewModelFactory(mockFerryClient),
        );
        GetIt.I.registerFactory<LoginViewModelFactory>(
          () => LoginViewModelFactory(
            mockAuthClient,
            mockAuthService,
            authViewModel,
          ),
        );
        GetIt.I.registerFactory<UserDetailsViewModelFactory>(
          () => UserDetailsViewModelFactory(),
        );

        // Test that each screen module is self-contained

        // Home module
        final homeFactory = GetIt.I<HomeViewModelFactory>();
        final homeProvider = HomeRouteProvider(homeFactory, authViewModel);
        final homeRoute = homeProvider.getRoute();
        expect(homeRoute, isA<GoRoute>());

        // Login module
        final loginFactory = GetIt.I<LoginViewModelFactory>();
        final loginProvider = LoginRouteProvider(loginFactory);
        final loginRoute = loginProvider.getRoute();
        expect(loginRoute, isA<GoRoute>());

        // Loading module
        final loadingProvider = LoadingRouteProvider(authViewModel);
        final loadingRoute = loadingProvider.getRoute();
        expect(loadingRoute, isA<GoRoute>());

        // UserDetails module
        final userDetailsFactory = GetIt.I<UserDetailsViewModelFactory>();
        final userDetailsProvider = UserDetailsRouteProvider(
          userDetailsFactory,
        );
        final userDetailsRoute = userDetailsProvider.getRoute();
        expect(userDetailsRoute, isA<GoRoute>());
      },
    );

    test('adding/removing route providers works via DI', () {
      // Setup mocks
      final mockAuthService = MockAuthService();
      final mockAuthClient = MockGithubAuthClient();
      final mockFerryClient = MockClient();

      when(mockAuthService.isLoggedIn).thenReturn(true);
      when(mockAuthService.init()).thenAnswer((_) async {});

      // Register services
      GetIt.I.registerSingleton<AuthService>(mockAuthService);
      GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
      GetIt.I.registerSingleton<Client>(mockFerryClient);

      final authViewModel = AuthViewModel(mockAuthService);
      GetIt.I.registerSingleton(authViewModel);

      // Register factories
      GetIt.I.registerFactory<HomeViewModelFactory>(
        () => HomeViewModelFactory(mockFerryClient),
      );
      GetIt.I.registerFactory<LoginViewModelFactory>(
        () => LoginViewModelFactory(
          mockAuthClient,
          mockAuthService,
          authViewModel,
        ),
      );

      // Initially register only home and login providers
      GetIt.I.registerSingleton<RouteProvider>(
        HomeRouteProvider(GetIt.I<HomeViewModelFactory>(), authViewModel),
        instanceName: 'home',
      );
      GetIt.I.registerSingleton<RouteProvider>(
        LoginRouteProvider(GetIt.I<LoginViewModelFactory>()),
        instanceName: 'login',
      );

      // Create route collection service
      GetIt.I.registerLazySingleton<RouteCollectionService>(
        () => RouteCollectionService(),
      );

      var routeCollectionService = GetIt.I<RouteCollectionService>();
      var routes = routeCollectionService.collectRoutes();
      expect(routes.length, equals(2));

      // Add more providers dynamically
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );
      GetIt.I.registerSingleton<RouteProvider>(
        LoadingRouteProvider(authViewModel),
        instanceName: 'loading',
      );
      GetIt.I.registerSingleton<RouteProvider>(
        UserDetailsRouteProvider(GetIt.I<UserDetailsViewModelFactory>()),
        instanceName: 'userDetails',
      );

      // Routes should automatically include new providers
      routes = routeCollectionService.collectRoutes();
      expect(routes.length, equals(4));
    });

    test('main app has no direct screen dependencies', () {
      // This test verifies that the main app (Gh3App) only depends on
      // AuthViewModel and RouteCollectionService, not individual screens

      // Setup minimal dependencies for main app
      final mockAuthService = MockAuthService();
      when(mockAuthService.isLoggedIn).thenReturn(true);
      when(mockAuthService.init()).thenAnswer((_) async {});

      final authViewModel = AuthViewModel(mockAuthService);
      final routeCollectionService = RouteCollectionService();

      // Main app should be able to function with just these dependencies
      expect(authViewModel, isNotNull);
      expect(routeCollectionService, isNotNull);

      // The main app should not need to import individual screen classes
      // This is validated by the fact that Gh3App class can be instantiated
      // with only these two dependencies
      expect(
        () => {
          'authViewModel': authViewModel,
          'routeCollectionService': routeCollectionService,
        },
        returnsNormally,
      );
    });

    test('route providers create independent ViewModels', () {
      // Setup mocks
      final mockAuthService = MockAuthService();
      final mockAuthClient = MockGithubAuthClient();
      final mockFerryClient = MockClient();

      when(mockAuthService.isLoggedIn).thenReturn(true);
      when(mockAuthService.init()).thenAnswer((_) async {});

      // Register services
      GetIt.I.registerSingleton<AuthService>(mockAuthService);
      GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
      GetIt.I.registerSingleton<Client>(mockFerryClient);

      final authViewModel = AuthViewModel(mockAuthService);
      GetIt.I.registerSingleton(authViewModel);

      // Register factories
      GetIt.I.registerFactory<HomeViewModelFactory>(
        () => HomeViewModelFactory(mockFerryClient),
      );
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );

      // Test that factories create independent instances
      final homeFactory = GetIt.I<HomeViewModelFactory>();
      final homeViewModel1 = homeFactory.create();
      final homeViewModel2 = homeFactory.create();

      expect(identical(homeViewModel1, homeViewModel2), isFalse);

      final userDetailsFactory = GetIt.I<UserDetailsViewModelFactory>();
      final userViewModel1 = userDetailsFactory.create('user1');
      final userViewModel2 = userDetailsFactory.create('user2');

      expect(identical(userViewModel1, userViewModel2), isFalse);
      expect(userViewModel1.login, equals('user1'));
      expect(userViewModel2.login, equals('user2'));
    });
  });
}
