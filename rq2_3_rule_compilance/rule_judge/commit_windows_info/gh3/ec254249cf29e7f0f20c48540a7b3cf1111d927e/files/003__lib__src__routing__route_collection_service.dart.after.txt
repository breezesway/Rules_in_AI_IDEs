import 'package:go_router/go_router.dart';
import 'package:injectable/injectable.dart';
import 'package:get_it/get_it.dart';
import 'route_provider.dart';

/// Service that collects routes from all registered RouteProvider instances
/// via dependency injection. This enables modular route configuration.
@injectable
class RouteCollectionService {
  RouteCollectionService();

  /// Collects all routes from registered RouteProvider instances
  List<RouteBase> collectRoutes() {
    try {
      final routeProviders = GetIt.instance.getAll<RouteProvider>();
      return routeProviders.map((provider) => provider.getRoute()).toList();
    } catch (e) {
      // If no route providers are registered yet, return empty list
      // This allows the app to start even if route providers aren't ready
      return <RouteBase>[];
    }
  }
}
