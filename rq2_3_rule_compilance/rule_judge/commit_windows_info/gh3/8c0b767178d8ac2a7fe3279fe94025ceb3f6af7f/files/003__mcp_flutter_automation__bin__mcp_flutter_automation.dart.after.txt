#!/usr/bin/env dart

import 'dart:io';
import 'package:mcp_flutter_automation/mcp_flutter_automation.dart';
import 'package:logging/logging.dart';

void main(List<String> arguments) async {
  // Setup logging
  Logger.root.level = Level.ALL;
  Logger.root.onRecord.listen((record) {
    stderr.writeln('[${record.level.name}] ${record.time}: ${record.message}');
  });

  final server = FlutterAutomationMCPServer();

  // Handle graceful shutdown
  ProcessSignal.sigint.watch().listen((_) async {
    await server.stop();
    exit(0);
  });

  ProcessSignal.sigterm.watch().listen((_) async {
    await server.stop();
    exit(0);
  });

  try {
    await server.start();
  } catch (e, stack) {
    stderr.writeln('Failed to start MCP Flutter Automation server: $e');
    stderr.writeln(stack);
    exit(1);
  }
}
