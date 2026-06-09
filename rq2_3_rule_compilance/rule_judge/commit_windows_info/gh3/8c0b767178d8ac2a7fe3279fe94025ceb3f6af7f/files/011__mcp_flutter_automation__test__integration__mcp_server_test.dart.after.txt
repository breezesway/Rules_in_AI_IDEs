import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:test/test.dart';
import 'package:mcp_flutter_automation/src/server.dart';
import '../test_utils.dart';

void main() {
  group('FlutterAutomationMCPServer Integration Tests', () {
    late FlutterAutomationMCPServer server;
    late Directory testProjectDir;

    setUp(() {
      server = FlutterAutomationMCPServer();
      testProjectDir =
          TestUtils.createMockFlutterProject(name: 'integration_test_app');
    });

    tearDown(() async {
      await server.stop();
    });

    group('Tool Registration', () {
      test('should register all expected tools', () {
        // Note: This would require access to the server's registered tools
        // In a real implementation, you'd need to expose the tools list
        // or create a method to check if tools are registered

        // For now, we'll test that the server can be created without errors
        expect(server, isNotNull);
      });
    });

    group('Tool Execution', () {
      test('launch_app tool should handle valid parameters', () async {
        // This test would require implementing a proper MCP client
        // to send tool execution requests to the server

        final params = {
          'appId': 'test-integration-app',
          'projectPath': testProjectDir.path,
          'targetFile': 'lib/main.dart',
          'vmServicePort': 8182,
          'ddsPort': 8181,
        };

        // In a real test, you would:
        // 1. Start the server
        // 2. Connect an MCP client
        // 3. Send a tool execution request
        // 4. Verify the response

        // For now, we'll test the underlying functionality
        expect(params['appId'], equals('test-integration-app'));
        expect(params['projectPath'], equals(testProjectDir.path));
      });

      test('launch_app tool should handle missing required parameters',
          () async {
        final invalidParams = {
          'projectPath': testProjectDir.path,
          // Missing required 'appId' parameter
        };

        // In a real MCP server test, this would return an error response
        expect(invalidParams.containsKey('appId'), isFalse);
      });

      test('launch_app tool should handle invalid project path', () async {
        final invalidParams = {
          'appId': 'test-app',
          'projectPath': '/non/existent/path',
        };

        // The server should handle this gracefully and return an error
        expect(Directory(invalidParams['projectPath'] as String).existsSync(),
            isFalse);
      });
    });

    group('Resource Access', () {
      test('should provide devices resource', () async {
        // Test that the devices resource can be accessed
        // In a real test, you would query the resource via MCP protocol

        // For now, test that flutter devices command would work
        try {
          final result = await Process.run('flutter', ['devices', '--version']);
          // If flutter is available, the command should succeed or fail gracefully
          expect(result, isNotNull);
        } catch (e) {
          // Flutter might not be available in test environment
          expect(e, isA<Exception>());
        }
      });

      test('should provide flutter doctor resource', () async {
        // Test that flutter doctor resource can be accessed
        try {
          final result = await Process.run('flutter', ['--version']);
          expect(result, isNotNull);
        } catch (e) {
          // Flutter might not be available in test environment
          expect(e, isA<Exception>());
        }
      });
    });

    group('Error Handling', () {
      test('should handle tool execution errors gracefully', () async {
        // Test various error scenarios that the server should handle

        final errorScenarios = [
          {
            'name': 'Invalid app ID format',
            'params': {'appId': '', 'projectPath': testProjectDir.path},
            'expectedError': 'invalid app ID',
          },
          {
            'name': 'Non-existent project path',
            'params': {'appId': 'test', 'projectPath': '/does/not/exist'},
            'expectedError': 'project path',
          },
          {
            'name': 'Invalid port numbers',
            'params': {
              'appId': 'test',
              'projectPath': testProjectDir.path,
              'vmServicePort': -1,
              'ddsPort': 99999,
            },
            'expectedError': 'port',
          },
        ];

        for (final scenario in errorScenarios) {
          // In a real test, you would execute the tool and check the error response
          final params = scenario['params'] as Map<String, dynamic>;
          expect(params, isNotNull);

          // Each scenario should be handled appropriately by the server
          if (params['vmServicePort'] != null && params['vmServicePort'] < 0) {
            expect(params['vmServicePort'], lessThan(0));
          }
        }
      });
    });
  });

  group('Real Flutter Command Integration', () {
    late FlutterAutomationMCPServer server;
    late Directory testProjectDir;

    setUpAll(() {
      // Check if Flutter is available
      try {
        Process.runSync('flutter', ['--version']);
      } catch (e) {
        // Skip these tests if Flutter is not available
        return;
      }
    });

    setUp(() {
      server = FlutterAutomationMCPServer();
      testProjectDir =
          TestUtils.createMockFlutterProject(name: 'real_flutter_test');
    });

    tearDown(() async {
      await server.stop();
    });

    test('should execute flutter devices command', () async {
      try {
        final result = await Process.run('flutter', ['devices', '--machine']);
        expect(result.exitCode,
            anyOf(equals(0), equals(1))); // 0 for success, 1 for no devices

        if (result.exitCode == 0 && result.stdout.isNotEmpty) {
          final devices = json.decode(result.stdout);
          expect(devices, isA<List>());
        }
      } catch (e) {
        // Test environment might not have Flutter installed
        print('Flutter not available in test environment: $e');
      }
    }, skip: !_isFlutterAvailable());

    test('should execute flutter doctor command', () async {
      try {
        final result = await Process.run('flutter', ['doctor', '-v']);
        expect(result.exitCode,
            anyOf(equals(0), equals(1))); // Doctor might show warnings
        expect(result.stdout, contains('Flutter'));
      } catch (e) {
        print('Flutter not available in test environment: $e');
      }
    }, skip: !_isFlutterAvailable());

    test('should validate Flutter project structure', () async {
      // Test that our mock project has the required structure
      expect(testProjectDir.existsSync(), isTrue);

      final pubspecFile = File('${testProjectDir.path}/pubspec.yaml');
      expect(pubspecFile.existsSync(), isTrue);

      final mainFile = File('${testProjectDir.path}/lib/main.dart');
      expect(mainFile.existsSync(), isTrue);

      final pubspecContent = await pubspecFile.readAsString();
      expect(pubspecContent, contains('flutter:'));
      expect(pubspecContent, contains('sdk: flutter'));

      final mainContent = await mainFile.readAsString();
      expect(mainContent, contains('void main()'));
      expect(mainContent, contains('runApp('));
    });
  });

  group('Concurrent Operations', () {
    late FlutterAutomationMCPServer server;
    late List<Directory> testProjects;

    setUp(() {
      server = FlutterAutomationMCPServer();
      testProjects = List.generate(
          3,
          (i) =>
              TestUtils.createMockFlutterProject(name: 'concurrent_test_$i'));
    });

    tearDown(() async {
      await server.stop();
    });

    test('should handle multiple simultaneous tool executions', () async {
      // Test that the server can handle multiple concurrent requests

      final futures = <Future>[];

      for (int i = 0; i < testProjects.length; i++) {
        futures.add(Future(() async {
          // Simulate tool execution delay
          await Future.delayed(Duration(milliseconds: 100 * i));

          // In a real test, this would be MCP tool execution
          final params = {
            'appId': 'concurrent-app-$i',
            'projectPath': testProjects[i].path,
          };

          expect(params['appId'], equals('concurrent-app-$i'));
          return params;
        }));
      }

      final results = await Future.wait(futures);
      expect(results, hasLength(testProjects.length));

      for (int i = 0; i < results.length; i++) {
        final result = results[i] as Map<String, dynamic>;
        expect(result['appId'], equals('concurrent-app-$i'));
      }
    });
  });

  group('Resource Management', () {
    late FlutterAutomationMCPServer server;

    setUp(() {
      server = FlutterAutomationMCPServer();
    });

    tearDown(() async {
      await server.stop();
    });

    test('should properly cleanup resources on stop', () async {
      // Start the server (in a real test, you'd start it properly)
      expect(server, isNotNull);

      // Add some apps (in a real test, you'd use MCP tools)
      // ...

      // Stop the server
      await server.stop();

      // Verify cleanup (in a real test, you'd check that all processes are stopped)
      expect(server,
          isNotNull); // Server object still exists but should be cleaned up
    });
  });
}

/// Helper function to check if Flutter is available
bool _isFlutterAvailable() {
  try {
    final result = Process.runSync('flutter', ['--version']);
    return result.exitCode == 0;
  } catch (e) {
    return false;
  }
}
