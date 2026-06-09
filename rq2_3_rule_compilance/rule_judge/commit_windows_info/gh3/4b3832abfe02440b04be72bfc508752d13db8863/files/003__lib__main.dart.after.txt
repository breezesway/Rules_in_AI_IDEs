import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:gh3/src/init.dart';
import 'package:gh3/src/screens/app/gh3_app.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';
import 'package:gh3/src/services/auth_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  configureDependencies();

  // Get services from dependency injection
  final authService = getIt<AuthService>();
  final routeCollectionService = getIt<RouteCollectionService>();

  // Create ViewModels manually with their dependencies
  final authVM = AuthViewModel(authService);
  await authVM.init();

  runApp(
    Gh3App(
      authViewModel: authVM,
      routeCollectionService: routeCollectionService,
    ),
  );
}
