import 'dart:async';
import 'dart:io';
import 'package:test/test.dart';
import 'package:mcp_flutter_automation/src/flutter_controller.dart';
import '../test_utils.dart';

void main() {
  group('FlutterController', () {
    late FlutterController controller;
    late Directory testProjectDir;

    setUp(() {
      controller = FlutterController();
      testProjectDir = TestUtils.createMockFlutterProject(name: 'test_app');
    });

    tearDown(() async {
      await controller.dispose();
    });

    group('launchApp', () {
      test('should create and register new app', () async {
        const appId = 'test-app-1';

        // Launch app - will succeed and be registered even if Flutter process fails
        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
            targetFile: 'lib/main.dart',
            deviceId: 'test-device',
          );
        } catch (e) {
          // Process may fail but app should still be registered
        }

        // Check that app was created and registered
        final apps = controller.listApps();
        expect(apps, hasLength(1));
        expect(apps.first['id'], equals(appId));
        expect(apps.first['projectPath'], equals(testProjectDir.path));
      });

      test('should throw exception if app ID already exists', () async {
        const appId = 'duplicate-app';

        // First launch
        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        // Second launch with same ID should throw
        expect(
          () async => await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          ),
          throwsA(predicate((e) =>
              e is Exception && e.toString().contains('already running'))),
        );
      });

      test('should use default ports when not specified', () async {
        const appId = 'default-ports-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        final appInfo = controller.getAppInfo(appId);
        expect(appInfo['vmServicePort'], equals(8182));
        expect(appInfo['ddsPort'], equals(8181));
      });

      test('should use custom ports when specified', () async {
        const appId = 'custom-ports-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
            vmServicePort: 9182,
            ddsPort: 9181,
          );
        } catch (e) {
          // Expected - process may fail
        }

        final appInfo = controller.getAppInfo(appId);
        expect(appInfo['vmServicePort'], equals(9182));
        expect(appInfo['ddsPort'], equals(9181));
      });
    });

    group('app management', () {
      test('should list apps correctly', () async {
        // Create multiple apps
        for (int i = 1; i <= 3; i++) {
          try {
            await controller.launchApp(
              appId: 'app-$i',
              projectPath: testProjectDir.path,
            );
          } catch (e) {
            // Expected - process may fail
          }
        }

        final apps = controller.listApps();
        expect(apps, hasLength(3));
        expect(apps.map((app) => app['id']),
            containsAll(['app-1', 'app-2', 'app-3']));
      });

      test('should get app info correctly', () async {
        const appId = 'info-test-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
            targetFile: 'lib/main.dart',
            deviceId: 'test-device',
          );
        } catch (e) {
          // Expected - process may fail
        }

        final info = controller.getAppInfo(appId);
        expect(info['id'], equals(appId));
        expect(info['projectPath'], equals(testProjectDir.path));
        expect(info['targetFile'], equals('lib/main.dart'));
        expect(info['deviceId'], equals('test-device'));
        expect(info['state'], isA<String>());
        expect(info['hasVmService'], isA<bool>());
        expect(info['logCount'], isA<int>());
        expect(info['logCount'], greaterThanOrEqualTo(0));
      });

      test('should throw exception for non-existent app info', () {
        expect(
          () => controller.getAppInfo('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });
    });

    group('log management', () {
      test('should get logs for existing app', () async {
        const appId = 'log-test-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        final logs = controller.getLogs(appId);
        expect(logs, isA<List<String>>());
        // Logs may contain Flutter output, so don't expect empty
      });

      test('should get recent logs with count limit', () async {
        const appId = 'recent-logs-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        final logs = controller.getLogs(appId, count: 5);
        expect(logs, isA<List<String>>());
        expect(logs.length, lessThanOrEqualTo(5));
      });

      test('should throw exception for non-existent app logs', () {
        expect(
          () => controller.getLogs('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });
    });

    group('hot reload/restart', () {
      test('should throw exception for non-existent app hot reload', () {
        expect(
          () async => await controller.hotReload('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });

      test('should throw exception for non-existent app hot restart', () {
        expect(
          () async => await controller.hotRestart('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });

      test('should handle hot reload for stopped app', () async {
        const appId = 'stopped-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        // Hot reload should either work or throw appropriate exception
        try {
          await controller.hotReload(appId);
          // If it succeeds, that's fine
        } catch (e) {
          // If it fails, should contain appropriate message
          expect(
              e.toString(),
              anyOf(
                contains('not running'),
                contains('not found'),
                contains('process'),
              ));
        }
      });

      test('should handle hot restart for stopped app', () async {
        const appId = 'stopped-app-2';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        // Hot restart should either work or throw appropriate exception
        try {
          await controller.hotRestart(appId);
          // If it succeeds, that's fine
        } catch (e) {
          // If it fails, should contain appropriate message
          expect(
              e.toString(),
              anyOf(
                contains('not running'),
                contains('not found'),
                contains('process'),
              ));
        }
      });
    });

    group('VM service operations', () {
      test('should throw exception for screenshot without VM service',
          () async {
        const appId = 'no-vm-app';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        expect(
          () async => await controller.captureScreenshot(appId),
          throwsA(predicate((e) =>
              e is Exception &&
              e.toString().contains('VM Service not connected'))),
        );
      });

      test('should throw exception for widget tree without VM service',
          () async {
        const appId = 'no-vm-app-2';

        try {
          await controller.launchApp(
            appId: appId,
            projectPath: testProjectDir.path,
          );
        } catch (e) {
          // Expected - process may fail
        }

        expect(
          () async => await controller.getWidgetTree(appId),
          throwsA(predicate((e) =>
              e is Exception &&
              e.toString().contains('VM Service not connected'))),
        );
      });

      test('should throw exception for non-existent app screenshot', () {
        expect(
          () async => await controller.captureScreenshot('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });

      test('should throw exception for non-existent app widget tree', () {
        expect(
          () async => await controller.getWidgetTree('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });
    });

    group('app stopping', () {
      test('should throw exception for non-existent app stop', () {
        expect(
          () async => await controller.stopApp('non-existent-app'),
          throwsA(predicate(
              (e) => e is Exception && e.toString().contains('not found'))),
        );
      });
    });

    group('dispose', () {
      test('should stop all apps on dispose', () async {
        // Create multiple apps
        for (int i = 1; i <= 3; i++) {
          try {
            await controller.launchApp(
              appId: 'dispose-app-$i',
              projectPath: testProjectDir.path,
            );
          } catch (e) {
            // Expected - process may fail
          }
        }

        expect(controller.listApps(), hasLength(3));

        // Dispose should not throw
        await controller.dispose();

        // After dispose, controller should be clean
        expect(controller.listApps(), isEmpty);
      });
    });
  });

  group('FlutterController - Integration scenarios', () {
    late FlutterController controller;
    late Directory testProjectDir;

    setUp(() {
      controller = FlutterController();
      testProjectDir = TestUtils.createMockFlutterProject();
    });

    tearDown(() async {
      await controller.dispose();
    });

    test('should handle complete app lifecycle', () async {
      const appId = 'lifecycle-app';

      // Initially no apps
      expect(controller.listApps(), isEmpty);

      // Launch app
      try {
        await controller.launchApp(
          appId: appId,
          projectPath: testProjectDir.path,
        );
      } catch (e) {
        // Expected - process may fail
      }

      // App should be registered
      expect(controller.listApps(), hasLength(1));
      final appInfo = controller.getAppInfo(appId);
      expect(appInfo['id'], equals(appId));

      // Get logs
      final logs = controller.getLogs(appId);
      expect(logs, isA<List<String>>());

      // Stop app
      await controller.stopApp(appId);

      // App should still be registered but stopped
      final stoppedAppInfo = controller.getAppInfo(appId);
      expect(
          stoppedAppInfo['state'], anyOf(equals('stopped'), equals('error')));
    });

    test('should handle multiple concurrent apps', () async {
      final appIds = ['concurrent-1', 'concurrent-2', 'concurrent-3'];

      // Launch multiple apps concurrently
      final futures = appIds.map((id) async {
        try {
          await controller.launchApp(
            appId: id,
            projectPath: testProjectDir.path,
            vmServicePort: 8182 + appIds.indexOf(id),
            ddsPort: 8181 + appIds.indexOf(id),
          );
        } catch (e) {
          // Expected - process may fail
        }
      });

      await Future.wait(futures);

      // All apps should be registered
      expect(controller.listApps(), hasLength(3));

      // Each app should have unique ports
      for (int i = 0; i < appIds.length; i++) {
        final info = controller.getAppInfo(appIds[i]);
        expect(info['vmServicePort'], equals(8182 + i));
        expect(info['ddsPort'], equals(8181 + i));
      }
    });
  });
}
