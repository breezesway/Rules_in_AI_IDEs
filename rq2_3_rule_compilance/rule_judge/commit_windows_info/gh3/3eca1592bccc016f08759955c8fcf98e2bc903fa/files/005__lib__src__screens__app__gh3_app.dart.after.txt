import 'package:flutter/material.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/screens/home_screen/home_screen.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/screens/home_screen/home_route.dart';
import 'package:gh3/src/screens/loading_screen/loading_screen.dart';
import 'package:gh3/src/screens/loading_screen/loading_route.dart';
import 'package:gh3/src/screens/login_screen/login_screen.dart';
import 'package:gh3/src/screens/login_screen/login_viewmodel.dart';
import 'package:gh3/src/screens/login_screen/login_route.dart';
import 'package:gh3/src/screens/user_details/user_details_screen.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel_factory.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:go_router/go_router.dart';

class Gh3App extends StatelessWidget {
  final AuthViewModel authViewModel;
  final AuthService authService;
  final GithubAuthClient githubAuthClient;
  final HomeViewModel homeViewModel;
  final UserDetailsViewModelFactory userDetailsViewModelFactory;

  const Gh3App({
    super.key,
    required this.authViewModel,
    required this.authService,
    required this.githubAuthClient,
    required this.homeViewModel,
    required this.userDetailsViewModelFactory,
  });

  @override
  Widget build(BuildContext context) {
    // Create route instances for type-safe navigation
    final homeRoute = HomeRoute();
    final loginRoute = LoginRoute();
    final loadingRoute = LoadingRoute();

    // Configure GoRouter
    final router = GoRouter(
      refreshListenable: authViewModel,
      initialLocation: loadingRoute.path,
      routes: [
        GoRoute(
          path: '/loading',
          builder: (context, state) =>
              LoadingScreen(authViewModel: authViewModel),
        ),
        GoRoute(
          path: '/login',
          builder: (context, state) => LoginScreen(
            viewModel: LoginViewModel(
              githubAuthClient,
              authService,
              authViewModel,
            ),
          ),
        ),
        GoRoute(
          path: '/',
          builder: (context, state) => HomeScreen(
            authViewModel: authViewModel,
            homeViewModel: homeViewModel,
          ),
        ),
        GoRoute(
          path: '/:login',
          builder: (context, state) => UserDetailsScreen(
            viewModel: userDetailsViewModelFactory.create(
              state.pathParameters['login']!,
            ),
          ),
        ),
      ],
      redirect: (context, state) {
        if (authViewModel.loading) {
          return loadingRoute.path;
        }
        final loc = state.uri.path;
        if (!authViewModel.loggedIn && loc != loginRoute.path) {
          return loginRoute.path;
        }
        if (authViewModel.loggedIn &&
            (loc == loginRoute.path || loc == loadingRoute.path)) {
          return homeRoute.path;
        }
        return null;
      },
    );
    return MaterialApp.router(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.black),
      ),
      routerConfig: router,
    );
  }
}
