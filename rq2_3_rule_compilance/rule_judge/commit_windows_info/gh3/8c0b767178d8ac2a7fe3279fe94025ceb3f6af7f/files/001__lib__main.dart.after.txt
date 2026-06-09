import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:gh3/src/init.dart';
import 'package:gh3/src/screens/app/gh3_app.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/routing/route_collection_service.dart';
import 'package:gh3/src/widgets/screenshot_wrapper.dart';
import 'dart:async';
import 'package:flutter_driver/driver_extension.dart';

Future<void> main() async {
  runZonedGuarded(
    () async {
      // Enable flutter driver extension for screenshots
      if (kDebugMode) {
        enableFlutterDriverExtension();
      }

      WidgetsFlutterBinding.ensureInitialized();

      configureDependencies();

      // Get services from dependency injection
      final authVM = getIt<AuthViewModel>();
      final routeCollectionService = getIt<RouteCollectionService>();
      authVM.init();

      runApp(
        ScreenshotWrapper(
          child: Gh3App(
            authViewModel: authVM,
            routeCollectionService: routeCollectionService,
          ),
        ),
      );
    },
    (error, stack) {
      print('Error: $error');
      print('Stack: $stack');
    },
  );
}
