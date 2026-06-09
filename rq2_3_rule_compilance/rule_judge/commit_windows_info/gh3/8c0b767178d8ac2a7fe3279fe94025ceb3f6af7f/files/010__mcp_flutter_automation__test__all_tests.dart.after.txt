import 'package:test/test.dart';

// Import all test files
import 'unit/flutter_app_test.dart' as flutter_app_tests;
import 'unit/flutter_controller_test.dart' as flutter_controller_tests;
import 'integration/mcp_server_test.dart' as mcp_server_tests;

void main() {
  group('MCP Flutter Automation - All Tests', () {
    group('Unit Tests', () {
      group('FlutterApp Model Tests', flutter_app_tests.main);
      group('FlutterController Tests', flutter_controller_tests.main);
    });

    group('Integration Tests', () {
      group('MCP Server Tests', mcp_server_tests.main);
    });
  });
}
