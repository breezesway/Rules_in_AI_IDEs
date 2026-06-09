import 'package:go_router/go_router.dart';
import 'package:injectable/injectable.dart';
import '../../routing/route_provider.dart';
import 'home_viewmodel_factory.dart';
import '../app/auth_viewmodel.dart';
import 'home_screen.dart';

/// Route provider for the home screen module.
/// Implements RouteProvider interface to provide modular route configuration.
@Named("HomeRouteProvider")
@Singleton(as: RouteProvider)
class HomeRouteProvider implements RouteProvider {
  final HomeViewModelFactory _homeViewModelFactory;
  final AuthViewModel _authViewModel;

  HomeRouteProvider(this._homeViewModelFactory, this._authViewModel);

  @override
  RouteBase getRoute() {
    return GoRoute(
      path: '/',
      builder: (context, state) => HomeScreen(
        authViewModel: _authViewModel,
        homeViewModel: _homeViewModelFactory.create(),
      ),
    );
  }
}
