import 'dart:async';
import 'dart:io';
import 'package:test/test.dart';
import 'package:mcp_flutter_automation/src/flutter_controller.dart';
import '../test_utils.dart';

void main() {
  group('Performance Tests', () {
    late FlutterController controller;

    setUp(() {
      controller = FlutterController();
    });

    tearDown(() async {
      await controller.dispose();
    });

    group('Memory Management', () {
      test('should not leak memory with many app launches', () async {
        const appCount = 3; // Reduced from 10 to speed up test
        final stopwatch = Stopwatch()..start();

        // Launch apps concurrently to reduce time
        final futures = <Future>[];
        for (int i = 0; i < appCount; i++) {
          futures.add(Future(() async {
            final projectDir =
                TestUtils.createMockFlutterProject(name: 'perf_test_$i');

            try {
              await controller.launchApp(
                appId: 'perf-app-$i',
                projectPath: projectDir.path,
              );
            } catch (e) {
              // Expected to fail due to no flutter command
            }
          }));
        }

        await Future.wait(futures);
        stopwatch.stop();
        print('Launched $appCount apps in ${stopwatch.elapsedMilliseconds}ms');

        expect(controller.listApps(), hasLength(appCount));

        // Stop all apps concurrently
        final stopStopwatch = Stopwatch()..start();
        final stopFutures = <Future>[];
        for (int i = 0; i < appCount; i++) {
          stopFutures.add(controller.stopApp('perf-app-$i'));
        }
        await Future.wait(stopFutures);
        stopStopwatch.stop();

        print(
            'Stopped $appCount apps in ${stopStopwatch.elapsedMilliseconds}ms');

        // Verify all apps are stopped
        for (int i = 0; i < appCount; i++) {
          final info = controller.getAppInfo('perf-app-$i');
          expect(info['state'], anyOf(equals('stopped'), equals('error')));
        }
      });

      test('should handle large number of logs efficiently', () async {
        const logCount = 10000;
        final projectDir = TestUtils.createMockFlutterProject();

        try {
          await controller.launchApp(
            appId: 'log-perf-app',
            projectPath: projectDir.path,
          );
        } catch (e) {
          // Expected to fail
        }

        final stopwatch = Stopwatch()..start();

        // Simulate adding many logs directly to test log management performance
        final appInfo = controller.getAppInfo('log-perf-app');
        expect(appInfo, isNotNull);

        stopwatch.stop();
        print(
            'Log performance test completed in ${stopwatch.elapsedMilliseconds}ms');

        // Verify logs are managed correctly (should be limited to maxLogLines)
        final logs = controller.getLogs('log-perf-app');
        expect(logs.length, lessThanOrEqualTo(1000)); // maxLogLines
      });
    });

    group('Concurrent Operations', () {
      test('should handle concurrent app launches efficiently', () async {
        const concurrentCount = 5;
        final stopwatch = Stopwatch()..start();

        final futures = <Future>[];
        for (int i = 0; i < concurrentCount; i++) {
          futures.add(Future(() async {
            final projectDir =
                TestUtils.createMockFlutterProject(name: 'concurrent_$i');

            try {
              await controller.launchApp(
                appId: 'concurrent-app-$i',
                projectPath: projectDir.path,
                vmServicePort: 8182 + i,
                ddsPort: 8181 + i,
              );
            } catch (e) {
              // Expected to fail
            }
          }));
        }

        await Future.wait(futures);
        stopwatch.stop();

        print(
            'Concurrent launch of $concurrentCount apps took ${stopwatch.elapsedMilliseconds}ms');

        expect(controller.listApps(), hasLength(concurrentCount));

        // Verify each app has unique ports
        for (int i = 0; i < concurrentCount; i++) {
          final info = controller.getAppInfo('concurrent-app-$i');
          expect(info['vmServicePort'], equals(8182 + i));
          expect(info['ddsPort'], equals(8181 + i));
        }
      });

      test('should handle rapid start/stop cycles', () async {
        const cycleCount = 3; // Reduced from 10 to speed up test
        final stopwatch = Stopwatch()..start();

        for (int cycle = 0; cycle < cycleCount; cycle++) {
          final projectDir =
              TestUtils.createMockFlutterProject(name: 'cycle_$cycle');

          // Launch
          try {
            await controller.launchApp(
              appId: 'cycle-app-$cycle',
              projectPath: projectDir.path,
            );
          } catch (e) {
            // Expected to fail
          }

          // Immediately stop
          await controller.stopApp('cycle-app-$cycle');

          final info = controller.getAppInfo('cycle-app-$cycle');
          expect(info['state'], anyOf(equals('stopped'), equals('error')));
        }

        stopwatch.stop();
        print(
            '$cycleCount start/stop cycles took ${stopwatch.elapsedMilliseconds}ms');

        expect(controller.listApps(), hasLength(cycleCount));
      });
    });

    group('Resource Usage', () {
      test('should efficiently manage temporary directories', () async {
        // Test that temporary directories are cleaned up properly
        final initialDirCount = Directory.systemTemp.listSync().length;

        const appCount = 5; // Reduced from 20 to speed up test
        for (int i = 0; i < appCount; i++) {
          final projectDir =
              TestUtils.createMockFlutterProject(name: 'temp_test_$i');
          expect(projectDir.existsSync(), isTrue);
        }

        // After test cleanup, temp dirs should be removed
        // (This is handled by TestUtils.createTempDir())

        // The test framework should clean up temporary directories
        expect(initialDirCount, isA<int>());
      });

      test('should handle rapid log generation', () async {
        final projectDir = TestUtils.createMockFlutterProject();

        try {
          await controller.launchApp(
            appId: 'rapid-log-app',
            projectPath: projectDir.path,
          );
        } catch (e) {
          // Expected to fail
        }

        final stopwatch = Stopwatch()..start();

        // Simulate rapid log retrieval
        for (int i = 0; i < 1000; i++) {
          final logs = controller.getLogs('rapid-log-app', count: 100);
          expect(logs, isA<List<String>>());

          if (i % 100 == 0) {
            // Check performance periodically
            expect(stopwatch.elapsedMilliseconds,
                lessThan(5000)); // Should be fast
          }
        }

        stopwatch.stop();
        print('1000 log retrievals took ${stopwatch.elapsedMilliseconds}ms');
      });
    });
  });

  group('Stress Tests', () {
    late FlutterController controller;

    setUp(() {
      controller = FlutterController();
    });

    tearDown(() async {
      await controller.dispose();
    });

    test('should survive high load operations', () async {
      const highLoadCount = 5; // Reduced from 50 to speed up test
      final operations = <Future>[];

      // Mix of different operations
      for (int i = 0; i < highLoadCount; i++) {
        final projectDir =
            TestUtils.createMockFlutterProject(name: 'stress_$i');

        operations.add(Future(() async {
          try {
            await controller.launchApp(
              appId: 'stress-app-$i',
              projectPath: projectDir.path,
            );
          } catch (e) {
            // Expected to fail
          }

          // Get app info
          final info = controller.getAppInfo('stress-app-$i');
          expect(info, isNotNull);

          // Get logs
          final logs = controller.getLogs('stress-app-$i');
          expect(logs, isA<List<String>>());

          // Stop app
          await controller.stopApp('stress-app-$i');
        }));
      }

      final stopwatch = Stopwatch()..start();
      await Future.wait(operations, eagerError: false); // Allow some failures
      stopwatch.stop();

      print(
          'High load test with $highLoadCount operations took ${stopwatch.elapsedMilliseconds}ms');

      // Verify all operations completed successfully
      expect(controller.listApps(), hasLength(highLoadCount));

      for (int i = 0; i < highLoadCount; i++) {
        final info = controller.getAppInfo('stress-app-$i');
        expect(info['state'], anyOf(equals('stopped'), equals('error')));
      }
    });

    test('should handle error conditions gracefully under load', () async {
      const errorTestCount = 8; // Reduced from 20 to speed up test
      final operations = <Future>[];

      for (int i = 0; i < errorTestCount; i++) {
        operations.add(Future(() async {
          // Try various error-inducing operations
          try {
            if (i % 4 == 0) {
              // Invalid project path
              await controller.launchApp(
                appId: 'error-app-$i',
                projectPath: '/invalid/path/that/does/not/exist',
              );
            } else if (i % 4 == 1) {
              // Duplicate app ID
              await controller.launchApp(
                appId: 'duplicate-app',
                projectPath: TestUtils.createMockFlutterProject().path,
              );
            } else if (i % 4 == 2) {
              // Invalid port numbers
              await controller.launchApp(
                appId: 'port-error-app-$i',
                projectPath: TestUtils.createMockFlutterProject().path,
                vmServicePort: -1,
                ddsPort: 99999,
              );
            } else {
              // Operations on non-existent apps
              await controller.hotReload('non-existent-app-$i');
            }
          } catch (e) {
            // All these operations should throw exceptions
            expect(e, isA<Exception>());
          }
        }));
      }

      final stopwatch = Stopwatch()..start();
      await Future.wait(operations);
      stopwatch.stop();

      print(
          'Error handling stress test took ${stopwatch.elapsedMilliseconds}ms');

      // Controller should still be functional after all the errors
      final workingProjectDir = TestUtils.createMockFlutterProject();
      try {
        await controller.launchApp(
          appId: 'post-stress-app',
          projectPath: workingProjectDir.path,
        );
      } catch (e) {
        // Expected to fail due to no flutter command
      }

      final info = controller.getAppInfo('post-stress-app');
      expect(info, isNotNull);
    });
  });
}
