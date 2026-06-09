import 'package:go_router/go_router.dart';
import 'package:injectable/injectable.dart';
import '../../routing/route_provider.dart';
import '../app/auth_viewmodel.dart';
import 'loading_screen.dart';

/// Route provider for the loading screen module.
/// Implements RouteProvider interface to provide modular route configuration.
@injectable
class LoadingRouteProvider implements RouteProvider {
  final AuthViewModel _authViewModel;

  LoadingRouteProvider(this._authViewModel);

  @override
  RouteBase getRoute() {
    return GoRoute(
      path: '/loading',
      builder: (context, state) => LoadingScreen(
        authViewModel: _authViewModel,
      ),
    );
  }
}