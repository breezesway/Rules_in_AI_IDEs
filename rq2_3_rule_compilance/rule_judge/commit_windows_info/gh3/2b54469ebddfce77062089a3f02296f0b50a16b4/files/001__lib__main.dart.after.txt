import 'package:flutter/material.dart';
import 'package:gh3/src/init.dart';
import 'package:gh3/src/screens/app/gh3_app.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  configureDependencies();

  // Get services from dependency injection
  final authVM = getIt<AuthViewModel>();
  final routeCollectionService = getIt<RouteCollectionService>();
  authVM.init();

  runApp(
    Gh3App(
      authViewModel: authVM,
      routeCollectionService: routeCollectionService,
    ),
  );
}
