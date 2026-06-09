import 'package:gh3/src/routing/app_route.dart';

/// Typed route for the user details screen with username parameter
class UserDetailsRoute extends AppRoute {
  final String login;

  UserDetailsRoute(this.login);

  @override
  String get path => '/$login';
}
