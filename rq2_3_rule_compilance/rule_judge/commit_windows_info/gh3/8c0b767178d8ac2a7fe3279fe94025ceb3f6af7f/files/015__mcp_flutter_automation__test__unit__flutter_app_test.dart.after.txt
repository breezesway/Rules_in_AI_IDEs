import 'package:test/test.dart';
import 'package:mcp_flutter_automation/src/models/flutter_app.dart';

void main() {
  group('FlutterApp', () {
    late FlutterApp app;

    setUp(() {
      app = FlutterApp(
        projectPath: '/test/project',
        targetFile: 'lib/main.dart',
        deviceId: 'test-device',
        vmServicePort: 8182,
        ddsPort: 8181,
      );
    });

    group('initialization', () {
      test('should initialize with correct values', () {
        expect(app.projectPath, equals('/test/project'));
        expect(app.targetFile, equals('lib/main.dart'));
        expect(app.deviceId, equals('test-device'));
        expect(app.vmServicePort, equals(8182));
        expect(app.ddsPort, equals(8181));
        expect(app.state, equals(AppState.notStarted));
        expect(app.logs, isEmpty);
        expect(app.process, isNull);
        expect(app.vmService, isNull);
        expect(app.vmServiceUri, isNull);
        expect(app.isolateId, isNull);
      });

      test('should use default ports when not specified', () {
        final defaultApp = FlutterApp(projectPath: '/test');
        expect(defaultApp.vmServicePort, equals(8182));
        expect(defaultApp.ddsPort, equals(8181));
      });

      test('should allow null optional parameters', () {
        final minimalApp = FlutterApp(projectPath: '/test');
        expect(minimalApp.targetFile, isNull);
        expect(minimalApp.deviceId, isNull);
      });
    });

    group('log management', () {
      test('should add logs correctly', () {
        app.addLog('First log');
        app.addLog('Second log');

        expect(app.logs, hasLength(2));
        expect(app.logs[0], equals('First log'));
        expect(app.logs[1], equals('Second log'));
      });

      test('should maintain log order', () {
        for (int i = 0; i < 10; i++) {
          app.addLog('Log $i');
        }

        expect(app.logs, hasLength(10));
        for (int i = 0; i < 10; i++) {
          expect(app.logs[i], equals('Log $i'));
        }
      });

      test('should limit logs to maxLogLines', () {
        // Add more logs than the maximum
        for (int i = 0; i < 1500; i++) {
          app.addLog('Log $i');
        }

        expect(app.logs, hasLength(1000)); // maxLogLines = 1000
        expect(
            app.logs.first, equals('Log 500')); // First 500 should be removed
        expect(app.logs.last, equals('Log 1499'));
      });

      test('should clear logs', () {
        app.addLog('Test log 1');
        app.addLog('Test log 2');
        expect(app.logs, hasLength(2));

        app.clearLogs();
        expect(app.logs, isEmpty);
      });

      test('should get recent logs correctly', () {
        for (int i = 0; i < 10; i++) {
          app.addLog('Log $i');
        }

        final recentLogs = app.getRecentLogs(3);
        expect(recentLogs, hasLength(3));
        expect(recentLogs[0], equals('Log 7'));
        expect(recentLogs[1], equals('Log 8'));
        expect(recentLogs[2], equals('Log 9'));
      });

      test('should return all logs when requesting more than available', () {
        app.addLog('Log 1');
        app.addLog('Log 2');

        final recentLogs = app.getRecentLogs(10);
        expect(recentLogs, hasLength(2));
        expect(recentLogs[0], equals('Log 1'));
        expect(recentLogs[1], equals('Log 2'));
      });

      test('should return empty list when no logs', () {
        final recentLogs = app.getRecentLogs(5);
        expect(recentLogs, isEmpty);
      });
    });

    group('state management', () {
      test('should update state correctly', () {
        expect(app.state, equals(AppState.notStarted));

        app.state = AppState.starting;
        expect(app.state, equals(AppState.starting));

        app.state = AppState.running;
        expect(app.state, equals(AppState.running));

        app.state = AppState.stopped;
        expect(app.state, equals(AppState.stopped));

        app.state = AppState.error;
        expect(app.state, equals(AppState.error));
      });
    });

    group('VM service management', () {
      test('should update VM service URI', () {
        expect(app.vmServiceUri, isNull);

        app.vmServiceUri = 'http://127.0.0.1:8181/abc123/';
        expect(app.vmServiceUri, equals('http://127.0.0.1:8181/abc123/'));
      });

      test('should update isolate ID', () {
        expect(app.isolateId, isNull);

        app.isolateId = 'isolates/123456789';
        expect(app.isolateId, equals('isolates/123456789'));
      });
    });

    group('AppState enum', () {
      test('should have all expected states', () {
        expect(AppState.values, hasLength(5));
        expect(AppState.values, contains(AppState.notStarted));
        expect(AppState.values, contains(AppState.starting));
        expect(AppState.values, contains(AppState.running));
        expect(AppState.values, contains(AppState.stopped));
        expect(AppState.values, contains(AppState.error));
      });

      test('should have correct string representation', () {
        expect(AppState.notStarted.name, equals('notStarted'));
        expect(AppState.starting.name, equals('starting'));
        expect(AppState.running.name, equals('running'));
        expect(AppState.stopped.name, equals('stopped'));
        expect(AppState.error.name, equals('error'));
      });
    });

    group('immutable logs getter', () {
      test('should return unmodifiable list', () {
        app.addLog('Test log');
        final logs = app.logs;

        expect(() => logs.add('Should fail'), throwsUnsupportedError);
        expect(() => logs.clear(), throwsUnsupportedError);
        expect(() => logs[0] = 'Should fail', throwsUnsupportedError);
      });

      test('should reflect changes when accessed again', () {
        app.addLog('First log');
        expect(app.logs, hasLength(1));

        app.addLog('Second log');
        expect(app.logs, hasLength(2));
      });
    });
  });
}
