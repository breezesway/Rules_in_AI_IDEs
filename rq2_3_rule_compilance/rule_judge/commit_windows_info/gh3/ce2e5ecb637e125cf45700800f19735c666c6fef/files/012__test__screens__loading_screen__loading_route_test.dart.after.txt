import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/loading_screen/loading_route.dart';

void main() {
  group('LoadingRoute', () {
    test('should return correct path', () {
      final loadingRoute = LoadingRoute();
      expect(loadingRoute.path, equals('/loading'));
    });
  });
}
