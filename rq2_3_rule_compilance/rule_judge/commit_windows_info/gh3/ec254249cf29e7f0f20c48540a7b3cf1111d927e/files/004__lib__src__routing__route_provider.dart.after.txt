import 'package:go_router/go_router.dart';

/// Interface for providing route configurations in a modular way.
/// Each screen module should implement this interface to define its routes.
abstract class RouteProvider {
  /// Returns the route configuration for this provider
  RouteBase getRoute();
}
