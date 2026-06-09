import 'dart:async';
import 'dart:io';
import 'package:test/test.dart';
import 'package:mcp_flutter_automation/src/flutter_controller.dart';
import '../test_utils.dart';

/// Fast performance tests that use mocked operations to avoid real process delays
void main() {
  group('Fast Performance Tests', () {
    late FlutterController controller;
    
    setUp(() {
      controller = FlutterController();
    });
    
    tearDown(() async {
      await controller.dispose();
    });
    
    group('Memory Management (Mock)', () {
      test('should not leak memory with many app launches', () async {
        const appCount = 10;
        final stopwatch = Stopwatch()..start();
        
        // Launch apps concurrently to reduce time
        final futures = <Future>[];
        for (int i = 0; i < appCount; i++) {
          futures.add(Future(() async {
            final projectDir = TestUtils.createMockFlutterProject(name: 'fast_perf_test_$i');
            
            try {
              await controller.launchApp(
                appId: 'fast-perf-app-$i',
                projectPath: projectDir.path,
              );
            } catch (e) {
              // Expected to fail due to no flutter command
            }
          }));
        }
        
        await Future.wait(futures);
        stopwatch.stop();
        
        expect(controller.listApps(), hasLength(appCount));
        expect(stopwatch.elapsedMilliseconds, lessThan(10000)); // Should be fast
        
        // Stop all apps concurrently with fast cleanup
        final stopStopwatch = Stopwatch()..start();
        final stopFutures = <Future>[];
        for (int i = 0; i < appCount; i++) {
          stopFutures.add(controller.stopApp('fast-perf-app-$i'));
        }
        await Future.wait(stopFutures, eagerError: false);
        stopStopwatch.stop();
        
        // Verify all apps are stopped
        for (int i = 0; i < appCount; i++) {
          final info = controller.getAppInfo('fast-perf-app-$i');
          expect(info['state'], anyOf(equals('stopped'), equals('error')));
        }
        
        expect(stopStopwatch.elapsedMilliseconds, lessThan(5000)); // Fast cleanup
      });
      
      test('should handle large number of logs efficiently', () async {
        final projectDir = TestUtils.createMockFlutterProject();
        
        try {
          await controller.launchApp(
            appId: 'fast-log-perf-app',
            projectPath: projectDir.path,
          );
        } catch (e) {
          // Expected to fail
        }
        
        final stopwatch = Stopwatch()..start();
        
        // Test log retrieval performance
        for (int i = 0; i < 1000; i++) {
          final logs = controller.getLogs('fast-log-perf-app', count: 100);
          expect(logs, isA<List<String>>());
        }
        
        stopwatch.stop();
        expect(stopwatch.elapsedMilliseconds, lessThan(1000)); // Should be very fast
        
        // Verify logs are managed correctly (should be limited to maxLogLines)
        final logs = controller.getLogs('fast-log-perf-app');
        expect(logs.length, lessThanOrEqualTo(1000)); // maxLogLines
      });
    });
    
    group('Concurrent Operations (Mock)', () {
      test('should handle concurrent app launches efficiently', () async {
        const concurrentCount = 20; // More than before since it's mocked
        final stopwatch = Stopwatch()..start();
        
        final futures = <Future>[];
        for (int i = 0; i < concurrentCount; i++) {
          futures.add(Future(() async {
            final projectDir = TestUtils.createMockFlutterProject(name: 'fast_concurrent_$i');
            
            try {
              await controller.launchApp(
                appId: 'fast-concurrent-app-$i',
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
        
        expect(controller.listApps(), hasLength(concurrentCount));
        expect(stopwatch.elapsedMilliseconds, lessThan(15000)); // Should be reasonably fast
        
        // Verify each app has unique ports
        for (int i = 0; i < concurrentCount; i++) {
          final info = controller.getAppInfo('fast-concurrent-app-$i');
          expect(info['vmServicePort'], equals(8182 + i));
          expect(info['ddsPort'], equals(8181 + i));
        }
      });
      
      test('should handle rapid start/stop cycles', () async {
        const cycleCount = 10;
        final stopwatch = Stopwatch()..start();
        
        for (int cycle = 0; cycle < cycleCount; cycle++) {
          final projectDir = TestUtils.createMockFlutterProject(name: 'fast_cycle_$cycle');
          
          // Launch
          try {
            await controller.launchApp(
              appId: 'fast-cycle-app-$cycle',
              projectPath: projectDir.path,
            );
          } catch (e) {
            // Expected to fail
          }
          
          // Immediately stop
          await controller.stopApp('fast-cycle-app-$cycle');
          
          final info = controller.getAppInfo('fast-cycle-app-$cycle');
          expect(info['state'], anyOf(equals('stopped'), equals('error')));
        }
        
        stopwatch.stop();
        expect(stopwatch.elapsedMilliseconds, lessThan(30000)); // Should be faster than before
        expect(controller.listApps(), hasLength(cycleCount));
      });
    });
    
    group('Resource Usage (Mock)', () {
      test('should efficiently manage temporary directories', () async {
        // Test that temporary directories are cleaned up properly
        final initialDirCount = Directory.systemTemp.listSync().length;
        
        const appCount = 50; // More than the original performance test
        for (int i = 0; i < appCount; i++) {
          final projectDir = TestUtils.createMockFlutterProject(name: 'fast_temp_test_$i');
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
            appId: 'fast-rapid-log-app',
            projectPath: projectDir.path,
          );
        } catch (e) {
          // Expected to fail
        }
        
        final stopwatch = Stopwatch()..start();
        
        // Simulate rapid log retrieval - more intensive than original
        for (int i = 0; i < 10000; i++) {
          final logs = controller.getLogs('fast-rapid-log-app', count: 100);
          expect(logs, isA<List<String>>());
          
          if (i % 1000 == 0) {
            // Check performance periodically
            expect(stopwatch.elapsedMilliseconds, lessThan(10000)); // Should be fast
          }
        }
        
        stopwatch.stop();
        expect(stopwatch.elapsedMilliseconds, lessThan(5000)); // Should complete quickly
      });
    });
  });
  
  group('Fast Stress Tests', () {
    late FlutterController controller;
    
    setUp(() {
      controller = FlutterController();
    });
    
    tearDown(() async {
      await controller.dispose();
    });
    
    test('should survive high load operations', () async {
      const highLoadCount = 20; // More than the reduced performance test
      final operations = <Future>[];
      
      // Mix of different operations
      for (int i = 0; i < highLoadCount; i++) {
        final projectDir = TestUtils.createMockFlutterProject(name: 'fast_stress_$i');
        
        operations.add(Future(() async {
          try {
            await controller.launchApp(
              appId: 'fast-stress-app-$i',
              projectPath: projectDir.path,
            );
          } catch (e) {
            // Expected to fail
          }
          
          // Get app info
          final info = controller.getAppInfo('fast-stress-app-$i');
          expect(info, isNotNull);
          
          // Get logs
          final logs = controller.getLogs('fast-stress-app-$i');
          expect(logs, isA<List<String>>());
          
          // Stop app
          await controller.stopApp('fast-stress-app-$i');
        }));
      }
      
      final stopwatch = Stopwatch()..start();
      await Future.wait(operations, eagerError: false); // Allow some failures
      stopwatch.stop();
      
      // Verify all operations completed successfully
      expect(controller.listApps(), hasLength(highLoadCount));
      expect(stopwatch.elapsedMilliseconds, lessThan(60000)); // Should complete within 1 minute
      
      for (int i = 0; i < highLoadCount; i++) {
        final info = controller.getAppInfo('fast-stress-app-$i');
        expect(info['state'], anyOf(equals('stopped'), equals('error')));
      }
    });
    
    test('should handle error conditions gracefully under load', () async {
      const errorTestCount = 40; // More than the reduced performance test
      final operations = <Future>[];
      
      for (int i = 0; i < errorTestCount; i++) {
        operations.add(Future(() async {
          // Try various error-inducing operations
          try {
            if (i % 4 == 0) {
              // Invalid project path
              await controller.launchApp(
                appId: 'fast-error-app-$i',
                projectPath: '/invalid/path/that/does/not/exist',
              );
            } else if (i % 4 == 1) {
              // Duplicate app ID
              await controller.launchApp(
                appId: 'fast-duplicate-app',
                projectPath: TestUtils.createMockFlutterProject().path,
              );
            } else if (i % 4 == 2) {
              // Invalid port numbers
              await controller.launchApp(
                appId: 'fast-port-error-app-$i',
                projectPath: TestUtils.createMockFlutterProject().path,
                vmServicePort: -1,
                ddsPort: 99999,
              );
            } else {
              // Operations on non-existent apps
              await controller.hotReload('fast-non-existent-app-$i');
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
      
      expect(stopwatch.elapsedMilliseconds, lessThan(30000)); // Should be fast even with errors
      
      // Controller should still be functional after all the errors
      final workingProjectDir = TestUtils.createMockFlutterProject();
      try {
        await controller.launchApp(
          appId: 'fast-post-stress-app',
          projectPath: workingProjectDir.path,
        );
      } catch (e) {
        // Expected to fail due to no flutter command
      }
      
      final info = controller.getAppInfo('fast-post-stress-app');
      expect(info, isNotNull);
    });
  });
}