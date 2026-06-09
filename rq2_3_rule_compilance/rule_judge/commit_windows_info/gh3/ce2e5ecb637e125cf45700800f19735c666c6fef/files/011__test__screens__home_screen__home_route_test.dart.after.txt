import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/home_screen/home_route.dart';

void main() {
  group('HomeRoute', () {
    test('should return correct path', () {
      final homeRoute = HomeRoute();
      expect(homeRoute.path, equals('/'));
    });
  });
}
