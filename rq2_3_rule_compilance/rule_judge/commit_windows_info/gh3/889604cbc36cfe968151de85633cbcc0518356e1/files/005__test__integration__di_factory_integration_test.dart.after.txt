import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:ferry/ferry.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

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
import 'di_factory_integration_test.mocks.dart';

void main() {
  group('DI Integration Tests', () {
    setUp(() {
      GetIt.I.reset();
    });

    test('all factories are properly registered and injectable', () {
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

      // Register AuthViewModel
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
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );

      // Test route providers can be created from factories
      final homeProvider = HomeRouteProvider(GetIt.I<HomeViewModelFactory>(), authViewModel);
      final loginProvider = LoginRouteProvider(GetIt.I<LoginViewModelFactory>());
      final loadingProvider = LoadingRouteProvider(authViewModel);
      final userDetailsProvider = UserDetailsRouteProvider(GetIt.I<UserDetailsViewModelFactory>());

      // Verify all providers can be created
      expect(homeProvider, isNotNull);
      expect(loginProvider, isNotNull);
      expect(loadingProvider, isNotNull);
      expect(userDetailsProvider, isNotNull);

      // Register route collection service
      GetIt.I.registerLazySingleton<RouteCollectionService>(
        () => RouteCollectionService(),
      );

      // Verify all factories can be retrieved
      expect(() => GetIt.I<HomeViewModelFactory>(), returnsNormally);
      expect(() => GetIt.I<LoginViewModelFactory>(), returnsNormally);
      expect(() => GetIt.I<UserDetailsViewModelFactory>(), returnsNormally);

      // Verify all route providers implement RouteProvider interface
      expect(homeProvider, isA<RouteProvider>());
      expect(loginProvider, isA<RouteProvider>());
      expect(loadingProvider, isA<RouteProvider>());
      expect(userDetailsProvider, isA<RouteProvider>());

      // Verify route collection service can be retrieved
      expect(() => GetIt.I<RouteCollectionService>(), returnsNormally);
    });

    test('factories create ViewModels with proper dependencies', () {
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
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );

      // Test factory creation
      final homeFactory = GetIt.I<HomeViewModelFactory>();
      final homeViewModel = homeFactory.create();
      expect(homeViewModel, isNotNull);

      final loginFactory = GetIt.I<LoginViewModelFactory>();
      final loginViewModel = loginFactory.create();
      expect(loginViewModel, isNotNull);

      final userDetailsFactory = GetIt.I<UserDetailsViewModelFactory>();
      final userDetailsViewModel = userDetailsFactory.create('testuser');
      expect(userDetailsViewModel, isNotNull);
      expect(userDetailsViewModel.login, equals('testuser'));
    });

    test('route providers work with manual route collection', () {
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
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );

      // Create route providers manually (not registered with GetIt)
      final homeProvider = HomeRouteProvider(GetIt.I<HomeViewModelFactory>(), authViewModel);
      final loginProvider = LoginRouteProvider(GetIt.I<LoginViewModelFactory>());
      final loadingProvider = LoadingRouteProvider(authViewModel);
      final userDetailsProvider = UserDetailsRouteProvider(GetIt.I<UserDetailsViewModelFactory>());

      // Test that each provider can create routes
      final homeRoute = homeProvider.getRoute();
      final loginRoute = loginProvider.getRoute();
      final loadingRoute = loadingProvider.getRoute();
      final userDetailsRoute = userDetailsProvider.getRoute();

      // Verify routes are created correctly
      expect(homeRoute, isNotNull);
      expect(loginRoute, isNotNull);
      expect(loadingRoute, isNotNull);
      expect(userDetailsRoute, isNotNull);

      // Test manual route collection (simulating what RouteCollectionService does)
      final routes = [homeRoute, loginRoute, loadingRoute, userDetailsRoute];
      expect(routes, hasLength(4));
    });

    test('error handling in factory creation', () {
      // Test factory creation without proper DI setup
      GetIt.I.registerFactory<UserDetailsViewModelFactory>(
        () => UserDetailsViewModelFactory(),
      );

      final factory = GetIt.I<UserDetailsViewModelFactory>();

      // Factory creation should not throw
      expect(() => factory.create('testuser'), returnsNormally);
    });

    test(
      'services maintain singleton lifecycle while ViewModels are factory-created',
      () {
        // Setup mocks
        final mockAuthService = MockAuthService();
        final mockAuthClient = MockGithubAuthClient();
        final mockFerryClient = MockClient();

        when(mockAuthService.isLoggedIn).thenReturn(true);
        when(mockAuthService.init()).thenAnswer((_) async {});

        // Register services as singletons
        GetIt.I.registerSingleton<AuthService>(mockAuthService);
        GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
        GetIt.I.registerSingleton<Client>(mockFerryClient);

        final authViewModel = AuthViewModel(mockAuthService);
        GetIt.I.registerSingleton(authViewModel);

        // Register factories
        GetIt.I.registerFactory<HomeViewModelFactory>(
          () => HomeViewModelFactory(mockFerryClient),
        );

        // Verify singletons return same instance
        final authService1 = GetIt.I<AuthService>();
        final authService2 = GetIt.I<AuthService>();
        expect(identical(authService1, authService2), isTrue);

        final ferryClient1 = GetIt.I<Client>();
        final ferryClient2 = GetIt.I<Client>();
        expect(identical(ferryClient1, ferryClient2), isTrue);

        // Verify factories return new instances
        final factory1 = GetIt.I<HomeViewModelFactory>();
        final factory2 = GetIt.I<HomeViewModelFactory>();
        expect(identical(factory1, factory2), isFalse);

        // But ViewModels created by factories should be different instances
        final viewModel1 = factory1.create();
        final viewModel2 = factory1.create();
        expect(identical(viewModel1, viewModel2), isFalse);
      },
    );
  });
}