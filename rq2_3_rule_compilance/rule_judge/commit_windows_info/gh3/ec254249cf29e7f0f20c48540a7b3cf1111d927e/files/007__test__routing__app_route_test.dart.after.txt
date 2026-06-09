import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';

import 'package:gh3/src/routing/routing.dart';

// Test implementation of AppRoute
class TestRoute extends AppRoute {
  final String _path;

  TestRoute(this._path);

  @override
  String get path => _path;
}

void main() {
  group('AppRoute', () {
    late TestRoute route;
    late GoRouter router;
    late Widget testApp;

    setUp(() {
      route = TestRoute('/test');
      router = GoRouter(
        routes: [
          GoRoute(
            path: '/',
            builder: (context, state) => const Scaffold(body: Text('Home')),
          ),
          GoRoute(
            path: '/test',
            builder: (context, state) => const Scaffold(body: Text('Test')),
          ),
        ],
      );
      testApp = MaterialApp.router(routerConfig: router);
    });

    testWidgets('should have correct path', (tester) async {
      expect(route.path, equals('/test'));
    });

    testWidgets('push should navigate to route', (tester) async {
      await tester.pumpWidget(testApp);

      final context = tester.element(find.byType(Scaffold));
      route.push(context);

      await tester.pumpAndSettle();
      expect(find.text('Test'), findsOneWidget);
    });

    testWidgets('go should navigate to route', (tester) async {
      await tester.pumpWidget(testApp);

      final context = tester.element(find.byType(Scaffold));
      route.go(context);

      await tester.pumpAndSettle();
      expect(find.text('Test'), findsOneWidget);
    });

    testWidgets('replace should navigate to route', (tester) async {
      await tester.pumpWidget(testApp);

      final context = tester.element(find.byType(Scaffold));
      route.replace(context);

      await tester.pumpAndSettle();
      expect(find.text('Test'), findsOneWidget);
    });
  });
}
