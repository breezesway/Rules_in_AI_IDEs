import 'package:go_router/go_router.dart';
import 'package:injectable/injectable.dart';
import '../../routing/route_provider.dart';
import 'user_details_viewmodel_factory.dart';
import 'user_details_screen.dart';

/// Route provider for the user details screen module.
/// Implements RouteProvider interface to provide modular route configuration
/// with parameterized routes.
@Named("UserDetailsRouteProvider")
@Injectable(as: RouteProvider)
class UserDetailsRouteProvider implements RouteProvider {
  final UserDetailsViewModelFactory _userDetailsViewModelFactory;

  UserDetailsRouteProvider(this._userDetailsViewModelFactory);

  @override
  RouteBase getRoute() {
    return GoRoute(
      path: '/:login',
      builder: (context, state) {
        final login = state.pathParameters['login']!;
        return UserDetailsScreen(
          viewModel: _userDetailsViewModelFactory.create(login),
        );
      },
    );
  }
}
