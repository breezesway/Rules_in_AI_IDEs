import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:ferry/ferry.dart';
import 'package:gh3/src/screens/app/gh3_app.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:gh3/src/screens/home_screen/__generated__/home_viewmodel.data.gql.dart';
import 'package:gh3/src/screens/home_screen/__generated__/home_viewmodel.var.gql.dart';
import 'package:go_router/go_router.dart';

import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/screens/home_screen/home_screen.dart';
import 'package:gh3/src/screens/login_screen/login_screen.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/token_storage.dart';
import 'package:gh3/src/services/scope_service.dart';
import 'package:gh3/src/services/timer_service.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';

@GenerateNiceMocks([
  MockSpec<Client>(),
  MockSpec<GithubAuthClient>(),
  MockSpec<ITokenStorage>(),
  MockSpec<IScopeService>(),
  MockSpec<TimerService>(),
  MockSpec<AuthService>(),
  MockSpec<RouteCollectionService>(),
])
import 'app_start_test.mocks.dart';

T anyRequest<T>() => any as T;

void main() {
  setUp(() {
    // Reset DI before each test
    GetIt.I.reset();
  });

  testWidgets('eventually shows HomeScreen when already logged in', (
    WidgetTester tester,
  ) async {
    // Register required dependencies
    final mockAuthService = MockAuthService();
    final mockAuthClient = MockGithubAuthClient();
    final mockFerryClient = MockClient();
    final mockRouteCollectionService = MockRouteCollectionService();

    when(mockAuthService.isLoggedIn).thenReturn(true);
    when(mockAuthService.init()).thenAnswer((_) async {});
    when(
      mockFerryClient.request<GGetFollowingData, GGetFollowingVars>(any),
    ).thenAnswer((_) => const Stream.empty());

    // Mock route collection service to return test routes
    when(mockRouteCollectionService.collectRoutes()).thenReturn([
      GoRoute(
        path: '/',
        builder: (context, state) => HomeScreen(
          authViewModel: AuthViewModel(mockAuthService),
          homeViewModel: HomeViewModel(mockFerryClient),
        ),
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => LoginScreen(
          viewModel: LoginViewModel(
            mockAuthClient,
            mockAuthService,
            AuthViewModel(mockAuthService),
          ),
        ),
      ),
      GoRoute(
        path: '/loading',
        builder: (context, state) => const Scaffold(body: Text('Loading')),
      ),
    ]);

    GetIt.I.registerSingleton<AuthService>(mockAuthService);
    GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
    GetIt.I.registerSingleton<Client>(mockFerryClient);

    // Create and initialize AuthViewModel
    final authViewModel = AuthViewModel(mockAuthService);
    await authViewModel.init();
    GetIt.I.registerSingleton(authViewModel);

    GetIt.I.registerLazySingleton<LoginViewModel>(
      () => LoginViewModel(mockAuthClient, mockAuthService, authViewModel),
    );

    await tester.pumpWidget(
      Gh3App(
        authViewModel: authViewModel,
        routeCollectionService: mockRouteCollectionService,
      ),
    );

    // Wait for router redirects to complete
    await tester.pump();
    await tester.pump();

    // Should show home screen
    expect(find.byType(HomeScreen), findsOneWidget);
  });

  testWidgets('eventually shows LoginScreen when not logged in', (
    WidgetTester tester,
  ) async {
    // Register required dependencies
    final mockAuthService = MockAuthService();
    final mockAuthClient = MockGithubAuthClient();
    final mockFerryClient = MockClient();
    final mockRouteCollectionService = MockRouteCollectionService();

    when(mockAuthService.isLoggedIn).thenReturn(false);
    when(mockAuthService.init()).thenAnswer((_) async {});
    // ignore: argument_type_not_assignable, avoid_redundant_argument_values
    when(
      mockFerryClient.request<GGetFollowingData, GGetFollowingVars>(captureAny),
    ).thenAnswer((_) => const Stream.empty());

    // Mock route collection service to return test routes
    when(mockRouteCollectionService.collectRoutes()).thenReturn([
      GoRoute(
        path: '/',
        builder: (context, state) => HomeScreen(
          authViewModel: AuthViewModel(mockAuthService),
          homeViewModel: HomeViewModel(mockFerryClient),
        ),
      ),
      GoRoute(
        path: '/login',
        builder: (context, state) => LoginScreen(
          viewModel: LoginViewModel(
            mockAuthClient,
            mockAuthService,
            AuthViewModel(mockAuthService),
          ),
        ),
      ),
      GoRoute(
        path: '/loading',
        builder: (context, state) => const Scaffold(body: Text('Loading')),
      ),
    ]);

    GetIt.I.registerSingleton<AuthService>(mockAuthService);
    GetIt.I.registerSingleton<GithubAuthClient>(mockAuthClient);
    GetIt.I.registerSingleton<Client>(mockFerryClient);

    // Create and initialize AuthViewModel
    final authViewModel = AuthViewModel(mockAuthService);
    await authViewModel.init();
    GetIt.I.registerSingleton(authViewModel);

    GetIt.I.registerLazySingleton<LoginViewModel>(
      () => LoginViewModel(mockAuthClient, mockAuthService, authViewModel),
    );

    await tester.pumpWidget(
      Gh3App(
        authViewModel: authViewModel,
        routeCollectionService: mockRouteCollectionService,
      ),
    );

    // Wait for router redirects to complete
    await tester.pump();
    await tester.pump();

    // Should show login screen
    expect(find.byType(LoginScreen), findsOneWidget);
  });
}
