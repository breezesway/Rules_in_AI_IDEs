import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/user_details/user_details_route.dart';

void main() {
  group('UserDetailsRoute', () {
    test('should return correct path for different usernames', () {
      final route1 = UserDetailsRoute('testuser');
      expect(route1.path, equals('/testuser'));

      final route2 = UserDetailsRoute('anotheruser');
      expect(route2.path, equals('/anotheruser'));

      final route3 = UserDetailsRoute('user-with-dash');
      expect(route3.path, equals('/user-with-dash'));

      final route4 = UserDetailsRoute('user123');
      expect(route4.path, equals('/user123'));
    });

    test('should handle special characters in username', () {
      final routeWithDash = UserDetailsRoute('user-name');
      expect(routeWithDash.path, equals('/user-name'));

      final routeWithNumbers = UserDetailsRoute('user123');
      expect(routeWithNumbers.path, equals('/user123'));

      final routeWithUnderscore = UserDetailsRoute('user_name');
      expect(routeWithUnderscore.path, equals('/user_name'));
    });
  });
}
