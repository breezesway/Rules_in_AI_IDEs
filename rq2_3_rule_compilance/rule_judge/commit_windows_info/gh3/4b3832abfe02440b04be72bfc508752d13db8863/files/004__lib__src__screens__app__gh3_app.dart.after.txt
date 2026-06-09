import 'package:flutter/material.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';
import 'package:go_router/go_router.dart';

class Gh3App extends StatelessWidget {
  final AuthViewModel authViewModel;
  final RouteCollectionService routeCollectionService;

  const Gh3App({
    super.key,
    required this.authViewModel,
    required this.routeCollectionService,
  });

  @override
  Widget build(BuildContext context) {
    // Define route paths as constants to avoid direct route class dependencies
    const homePath = '/';
    const loginPath = '/login';
    const loadingPath = '/loading';

    // Configure GoRouter with dynamically collected routes
    final router = GoRouter(
      refreshListenable: authViewModel,
      initialLocation: loadingPath,
      routes: routeCollectionService.collectRoutes(),
      redirect: (context, state) {
        if (authViewModel.loading) {
          return loadingPath;
        }
        final loc = state.uri.path;
        if (!authViewModel.loggedIn && loc != loginPath) {
          return loginPath;
        }
        if (authViewModel.loggedIn &&
            (loc == loginPath || loc == loadingPath)) {
          return homePath;
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
