import 'package:go_router/go_router.dart';
import 'package:injectable/injectable.dart';
import '../../routing/route_provider.dart';
import 'login_viewmodel_factory.dart';
import 'login_screen.dart';

/// Route provider for the login screen module.
/// Implements RouteProvider interface to provide modular route configuration.
@injectable
class LoginRouteProvider implements RouteProvider {
  final LoginViewModelFactory _loginViewModelFactory;

  LoginRouteProvider(this._loginViewModelFactory);

  @override
  RouteBase getRoute() {
    return GoRoute(
      path: '/login',
      builder: (context, state) => LoginScreen(
        viewModel: _loginViewModelFactory.create(),
      ),
    );
  }
}