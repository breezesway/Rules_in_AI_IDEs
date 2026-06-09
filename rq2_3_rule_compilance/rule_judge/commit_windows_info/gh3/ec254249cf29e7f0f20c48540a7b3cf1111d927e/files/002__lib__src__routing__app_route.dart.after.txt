import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

/// Base class for all typed routes in the application.
/// Provides common navigation methods for type-safe routing.
abstract class AppRoute {
  /// The path for this route
  String get path;

  /// Navigate to this route by pushing it onto the navigation stack
  void push(BuildContext context) {
    context.push(path);
  }

  /// Navigate to this route by replacing the current location
  void go(BuildContext context) {
    context.go(path);
  }

  /// Replace the current route with this route
  void replace(BuildContext context) {
    context.replace(path);
  }
}
