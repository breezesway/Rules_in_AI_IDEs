import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/login_screen/login_route.dart';

void main() {
  group('LoginRoute', () {
    test('should return correct path', () {
      final loginRoute = LoginRoute();
      expect(loginRoute.path, equals('/login'));
    });
  });
}
