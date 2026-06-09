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
  /// Routes are sorted by specificity to ensure specific routes like '/:login'
  /// have higher priority than general routes like '/loading'
  List<RouteBase> collectRoutes() {
    try {
      final routeProviders = GetIt.instance.getAll<RouteProvider>();
      final routes = routeProviders.map((provider) => provider.getRoute()).toList();
      return _sortRoutesBySpecificity(routes);
    } catch (e) {
      // If no route providers are registered yet, return empty list
      // This allows the app to start even if route providers aren't ready
      return <RouteBase>[];
    }
  }

  /// Sorts routes by specificity to ensure correct matching priority.
  /// More specific routes (fewer path parameters, more literal segments) come first.
  List<RouteBase> _sortRoutesBySpecificity(List<RouteBase> routes) {
    final List<RouteBase> sortedRoutes = List.from(routes);
    
    sortedRoutes.sort((a, b) {
      final pathA = _extractPath(a);
      final pathB = _extractPath(b);
      
      if (pathA == null || pathB == null) return 0;
      
      final specificityA = _calculateSpecificity(pathA);
      final specificityB = _calculateSpecificity(pathB);
      
      // Higher specificity comes first (descending order)
      return specificityB.compareTo(specificityA);
    });
    
    return sortedRoutes;
  }

  /// Extracts the path from a RouteBase (only supports GoRoute currently)
  String? _extractPath(RouteBase route) {
    if (route is GoRoute) {
      return route.path;
    }
    return null;
  }

  /// Calculates route specificity score.
  /// Higher score = more specific route
  int _calculateSpecificity(String path) {
    int score = 0;
    final segments = path.split('/').where((s) => s.isNotEmpty);
    
    for (final segment in segments) {
      if (segment.startsWith(':')) {
        // Parameter segment: lower specificity
        score += 1;
      } else {
        // Literal segment: higher specificity
        score += 10;
      }
    }
    
    // Longer paths with same segment types are more specific
    score += segments.length;
    
    return score;
  }
}
