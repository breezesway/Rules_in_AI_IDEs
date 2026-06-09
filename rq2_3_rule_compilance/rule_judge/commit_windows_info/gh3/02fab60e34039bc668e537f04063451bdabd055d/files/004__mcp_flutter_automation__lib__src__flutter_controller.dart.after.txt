import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'package:vm_service/vm_service.dart';
import 'package:web_socket_channel/io.dart';
import 'models/flutter_app.dart';

class FlutterController {
  final _logger = Logger('FlutterController');

  // Instance-based registry for child processes
  final Map<String, FlutterApp> _apps = {};
  static bool _exitHandlerRegistered = false;
  static final List<FlutterController> _allControllers = [];

  FlutterController() {
    // Minimal logging for MCP compatibility
    if (Logger.root.level == Level.ALL) {
      Logger.root.level = Level.WARNING;
    }

    // Register this controller for cleanup
    _allControllers.add(this);

    // Register exit handler once to cleanup all Flutter processes
    if (!_exitHandlerRegistered) {
      _registerExitHandler();
      _exitHandlerRegistered = true;
    }
  }

  void _registerExitHandler() {
    // Handle SIGTERM (normal termination)
    ProcessSignal.sigterm.watch().listen((_) {
      _logger.info('SIGTERM received - cleaning up Flutter processes');
      _cleanupAllProcesses();
      exit(0);
    });

    // Handle SIGINT (Ctrl+C)
    ProcessSignal.sigint.watch().listen((_) {
      _logger.info('SIGINT received - cleaning up Flutter processes');
      _cleanupAllProcesses();
      exit(0);
    });

    _logger.info('Exit handlers registered for process cleanup');
  }

  static void _cleanupAllProcesses() {
    final logger = Logger('FlutterController.cleanup');
    int totalApps = 0;

    for (final controller in _allControllers) {
      totalApps += controller._apps.length;
    }

    logger.info(
        'Cleaning up $totalApps Flutter processes across ${_allControllers.length} controllers');

    for (final controller in _allControllers) {
      for (final entry in controller._apps.entries) {
        final appId = entry.key;
        final app = entry.value;

        try {
          logger.info('Stopping Flutter app: $appId');

          if (app.process != null) {
            // Kill the process group to ensure all child processes are terminated
            Process.killPid(app.process!.pid, ProcessSignal.sigterm);

            // Brief delay for graceful termination (synchronous)
            sleep(Duration(milliseconds: 500));

            // Force kill if still running
            if (!app.process!.kill(ProcessSignal.sigkill)) {
              Process.killPid(app.process!.pid, ProcessSignal.sigkill);
            }
          }

          app.vmService?.dispose();
          logger.info('Successfully stopped app: $appId');
        } catch (e) {
          logger.warning('Failed to stop app $appId: $e');
        }
      }

      controller._apps.clear();
    }

    _allControllers.clear();
    logger.info('All Flutter processes cleaned up');
  }

  Future<FlutterApp> launchApp({
    required String appId,
    required String projectPath,
    String? targetFile,
    String? deviceId,
    int vmServicePort = 8182,
    int ddsPort = 8181,
  }) async {
    // Check if app is already running
    if (_apps.containsKey(appId)) {
      final existingApp = _apps[appId]!;
      if (existingApp.state == AppState.running ||
          existingApp.state == AppState.starting) {
        throw Exception('App $appId is already running');
      }
    }

    final app = FlutterApp(
      projectPath: projectPath,
      targetFile: targetFile,
      deviceId: deviceId,
      vmServicePort: vmServicePort,
      ddsPort: ddsPort,
    );

    _apps[appId] = app;
    app.state = AppState.starting;

    try {
      // Build flutter run command
      final command = [
        'flutter',
        'run',
        '--debug',
        '--host-vmservice-port=$vmServicePort',
        '--dds-port=$ddsPort',
        '--enable-vm-service',
        '--disable-service-auth-codes',
      ];

      if (targetFile != null) {
        command.addAll(['-t', targetFile]);
      }

      if (deviceId != null) {
        command.addAll(['-d', deviceId]);
      }

      _logger.info('Launching Flutter app: ${command.join(' ')}');

      // Start the process as a child process that will be killed when parent exits
      final process = await Process.start(
        command.first,
        command.skip(1).toList(),
        workingDirectory: projectPath,
        mode: ProcessStartMode.normal,
        runInShell: false, // Ensure direct process control
      );

      _logger.info('Flutter process started with PID: ${process.pid}');

      app.process = process;

      // Listen to stdout
      process.stdout.transform(utf8.decoder).listen((data) {
        app.addLog(data);
        _logger.fine('Flutter stdout: $data');

        // Look for VM service URL
        final vmServiceMatch =
            RegExp(r'VM Service[^\n]*at[:\s]+(http[^\s]+)').firstMatch(data);
        if (vmServiceMatch != null) {
          app.vmServiceUri = vmServiceMatch.group(1);
          _logger.info('Found VM Service URI: ${app.vmServiceUri}');
          _connectToVmService(app);
        }
      });

      // Listen to stderr
      process.stderr.transform(utf8.decoder).listen((data) {
        app.addLog('[ERROR] $data');
        _logger.warning('Flutter stderr: $data');
      });

      // Monitor process exit
      process.exitCode.then((code) {
        _logger.info('Flutter process exited with code: $code');
        app.state = code == 0 ? AppState.stopped : AppState.error;
        app.vmService?.dispose();
        app.vmService = null;
      });

      // Wait a shorter time for the app to start (reduced for faster testing)
      await Future.delayed(Duration(milliseconds: 500));

      if (app.process != null) {
        app.state = AppState.running;
      }

      return app;
    } catch (e) {
      app.state = AppState.error;
      _logger.severe('Failed to launch app: $e');
      rethrow;
    }
  }

  Future<void> _connectToVmService(FlutterApp app) async {
    if (app.vmServiceUri == null) return;

    try {
      // Use DDS port for connection with retry logic
      final ddsUri = 'ws://127.0.0.1:${app.ddsPort}/ws';
      _logger.info('=== VM SERVICE CONNECTION DEBUG ===');
      _logger.info('Connecting to VM Service via DDS at: $ddsUri');
      _logger.info('Original VM Service URI: ${app.vmServiceUri}');
      _logger.info('DDS Port: ${app.ddsPort}');
      _logger.info('VM Service Port: ${app.vmServicePort}');

      // Try both DDS and direct VM service connection methods
      final connectionUris = [
        ddsUri, // DDS connection (preferred)
        'ws://127.0.0.1:${app.vmServicePort}/ws', // Direct VM service (backup script method)
      ];

      VmService? vmService;
      for (String uri in connectionUris) {
        _logger.info('Trying connection method: $uri');

        for (int attempt = 1; attempt <= 3; attempt++) {
          try {
            _logger.info('Connection attempt $attempt to $uri');
            final channel = IOWebSocketChannel.connect(uri);
            vmService = VmService(
              channel.stream,
              (message) => channel.sink.add(message),
            );

            // Test the connection by getting VM info
            final vm = await vmService.getVM().timeout(Duration(seconds: 5));
            _logger.info(
                '✅ Connected to VM: ${vm.name} via $uri (attempt $attempt)');
            _logger.info('VM isolates: ${vm.isolates?.length ?? 0}');

            // Get main isolate
            if (vm.isolates?.isNotEmpty ?? false) {
              for (int i = 0; i < vm.isolates!.length; i++) {
                final isolateRef = vm.isolates![i];
                _logger.info(
                    'Isolate $i: id=${isolateRef.id}, name=${isolateRef.name}');
              }

              app.isolateId = vm.isolates!.first.id;
              _logger.info('Selected isolate: ${app.isolateId}');

              // Test if screenshot extension is available
              try {
                final isolate = await vmService.getIsolate(app.isolateId!);
                _logger.info('Isolate extensions: ${isolate.extensionRPCs}');
                if (isolate.extensionRPCs?.contains('ext.gh3.screenshot') ==
                    true) {
                  _logger.info('✅ ext.gh3.screenshot extension is available!');
                } else {
                  _logger.warning('❌ ext.gh3.screenshot extension not found');
                }
              } catch (e) {
                _logger.warning('Failed to check extensions: $e');
              }
            }

            app.vmService = vmService;
            _logger.info('=== VM SERVICE CONNECTION SUCCESS ===');
            return; // Success!
          } catch (e) {
            _logger.warning('Connection attempt $attempt to $uri failed: $e');
            vmService?.dispose();

            if (attempt < 3) {
              await Future.delayed(Duration(milliseconds: 1000 * attempt));
            }
          }
        }
        _logger.warning('All attempts failed for $uri');
      }

      _logger.warning('All VM Service connection attempts failed');
    } catch (e) {
      _logger.warning('Failed to connect to VM Service: $e');
      // Don't throw - app can still run without VM service
    }
  }

  Future<void> hotReload(String appId) async {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    if (app.state != AppState.running) {
      throw Exception('App $appId is not running');
    }

    // Send 'r' to the process stdin for hot reload
    app.process?.stdin.writeln('r');
    await Future.delayed(Duration(milliseconds: 500));
  }

  Future<void> hotRestart(String appId) async {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    if (app.state != AppState.running) {
      throw Exception('App $appId is not running');
    }

    // Send 'R' to the process stdin for hot restart
    app.process?.stdin.writeln('R');
    await Future.delayed(Duration(seconds: 2));
  }

  Future<void> stopApp(String appId) async {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    if (app.process != null) {
      // First, just try to kill the process directly for faster cleanup
      // In tests, this is preferred since we're not running real Flutter apps
      try {
        app.process!.kill(ProcessSignal.sigterm);

        // Wait a short time for graceful termination
        await app.process!.exitCode.timeout(
          Duration(milliseconds: 500),
          onTimeout: () {
            // Force kill if SIGTERM didn't work
            try {
              app.process!.kill(ProcessSignal.sigkill);
            } catch (e) {
              // Process might already be dead
            }
            return -1;
          },
        );
      } catch (e) {
        // Process might already be dead or kill failed, that's fine
      }
    }

    app.state = AppState.stopped;
    app.vmService?.dispose();
    app.vmService = null;
  }

  Future<String?> captureScreenshot(String appId) async {
    final app = _apps[appId];
    if (app == null) {
      throw Exception(
          'App $appId not found. Use launch_app first to start the Flutter app.');
    }

    _logger.info('=== SCREENSHOT DEBUG START ===');
    _logger.info('Screenshot request for app $appId');
    _logger.info('VM Service connected: ${app.vmService != null}');
    _logger.info('Current isolate ID: ${app.isolateId}');
    _logger.info('VM Service URI: ${app.vmServiceUri}');

    if (app.vmService == null) {
      throw Exception('VM Service not connected for app $appId');
    }

    try {
      // Get VM info and log details
      _logger.info('Getting VM info...');
      final vm = await app.vmService!.getVM();
      _logger.info('VM name: ${vm.name}, version: ${vm.version}');
      _logger.info('VM isolates count: ${vm.isolates?.length ?? 0}');

      if (vm.isolates?.isNotEmpty ?? false) {
        for (int i = 0; i < vm.isolates!.length; i++) {
          final isolateRef = vm.isolates![i];
          _logger
              .info('Isolate $i: id=${isolateRef.id}, name=${isolateRef.name}');
        }

        final oldIsolateId = app.isolateId;
        app.isolateId = vm.isolates!.first.id;
        _logger.info('Isolate ID updated: $oldIsolateId -> ${app.isolateId}');

        // Get detailed isolate info
        final isolate = await app.vmService!.getIsolate(app.isolateId!);
        _logger.info(
            'Isolate details: runnable=${isolate.runnable}, pauseOnExit=${isolate.pauseOnExit}');
        _logger.info('Available extensions: ${isolate.extensionRPCs}');
      } else {
        throw Exception('No isolates found in VM');
      }

      // Try our custom gh3 screenshot extension first (RenderRepaintBoundary approach)
      try {
        _logger.info(
            'Attempting to call ext.gh3.screenshot with isolate ${app.isolateId}...');
        final response = await app.vmService!
            .callServiceExtension(
              'ext.gh3.screenshot',
              isolateId: app.isolateId,
            )
            .timeout(Duration(seconds: 10));
        _logger.info('ext.gh3.screenshot call completed successfully');

        _logger.info('ext.gh3.screenshot response: ${response.json}');
        _logger.info('Response type: ${response.json.runtimeType}');
        _logger.info('Response keys: ${response.json?.keys.toList()}');

        // Handle both response formats: wrapped in 'result' or direct
        Map<String, dynamic>? responseData;

        if (response.json != null) {
          if (response.json!.containsKey('result')) {
            // Format 1: {"result": "{\"success\":true,...}"}
            final result = response.json!['result'];
            if (result is String) {
              try {
                responseData = json.decode(result) as Map<String, dynamic>;
                _logger.info('Parsed wrapped result format');
              } catch (e) {
                _logger.warning('Failed to decode wrapped result: $e');
              }
            } else if (result is Map<String, dynamic>) {
              responseData = result;
              _logger.info('Got direct result format');
            }
          } else if (response.json!.containsKey('success')) {
            // Format 2: {"success": true, "screenshot": "...", ...}
            responseData = response.json!;
            _logger.info('Got direct response format');
          }
        }

        if (responseData != null &&
            responseData['success'] == true &&
            responseData['screenshot'] != null) {
          final base64Data = responseData['screenshot'] as String;
          _logger.info(
              'Screenshot captured via custom gh3 extension, size: ${base64Data.length}');
          _logger.info('Format: ${responseData['format']}');
          _logger.info('Method: ${responseData['method']}');

          // Save screenshot to file
          try {
            final bytes = base64Decode(base64Data);
            final timestamp = DateTime.now().millisecondsSinceEpoch;
            final fileName = 'screenshot_${timestamp}.png';
            final filePath = '${app.projectPath}/$fileName';
            final file = File(filePath);
            await file.writeAsBytes(bytes);
            _logger
                .info('Screenshot saved to: $filePath (${bytes.length} bytes)');

            // Also save as latest screenshot
            final latestPath = '${app.projectPath}/latest_screenshot.png';
            final latestFile = File(latestPath);
            await latestFile.writeAsBytes(bytes);
            _logger.info('Latest screenshot saved to: $latestPath');
          } catch (e) {
            _logger.warning('Failed to save screenshot to file: $e');
          }

          return base64Data;
        } else {
          _logger.warning(
              'Response missing success or screenshot field: ${response.json}');
        }
      } catch (e) {
        _logger.severe('=== ext.gh3.screenshot FAILED ===');
        _logger.severe('Error: $e');
        _logger.severe('Error type: ${e.runtimeType}');
        _logger.severe('Stack trace: ${StackTrace.current}');
      }

      // Try the test extension
      try {
        _logger.info('Testing ext.gh3.test extension...');
        final response = await app.vmService!.callServiceExtension(
          'ext.gh3.test',
          isolateId: app.isolateId,
        );
        _logger.info('ext.gh3.test response: ${response.json}');
      } catch (e) {
        _logger.warning('Test extension failed: $e');
      }

      // Fallback to flutter driver screenshot
      try {
        final response = await app.vmService!.callServiceExtension(
          'ext.flutter.driver.screenshot',
          isolateId: app.isolateId,
        );

        if (response.json != null && response.json!.containsKey('screenshot')) {
          _logger.info('Screenshot captured via flutter driver extension');
          return response.json!['screenshot'] as String?;
        }
      } catch (e) {
        _logger.fine('Driver screenshot extension not available: $e');
      }

      // List available extensions for debugging
      try {
        final vm = await app.vmService!.getVM();
        if (vm.isolates?.isNotEmpty ?? false) {
          final isolate =
              await app.vmService!.getIsolate(vm.isolates!.first.id!);
          _logger.info('Available extensions: ${isolate.extensionRPCs}');
        }
      } catch (e) {
        _logger.fine('Could not list extensions: $e');
      }

      // Final fallback: Direct VM service connection like backup script
      _logger.info('=== ATTEMPTING DIRECT VM SERVICE CONNECTION ===');
      try {
        // Connect directly to VM service like the backup script does
        final vmServiceUri = 'ws://127.0.0.1:${app.vmServicePort}/ws';
        _logger.info('Connecting directly to VM service at: $vmServiceUri');

        final channel = IOWebSocketChannel.connect(vmServiceUri);
        final directVmService = VmService(
          channel.stream,
          (message) => channel.sink.add(message),
        );

        final vm = await directVmService.getVM();
        _logger.info('Direct connection - VM isolates: ${vm.isolates?.length}');

        if (vm.isolates?.isNotEmpty == true) {
          final isolate = vm.isolates!.first;
          _logger.info('Using direct connection isolate: ${isolate.id}');

          // Call screenshot extension directly
          final response = await directVmService.callServiceExtension(
            'ext.gh3.screenshot',
            isolateId: isolate.id!,
          );

          _logger.info('Direct connection screenshot response received');
          if (response.json != null &&
              response.json!['success'] == true &&
              response.json!['screenshot'] != null) {
            final base64Data = response.json!['screenshot'] as String;
            _logger.info(
                '✅ Direct connection screenshot success: ${base64Data.length} chars');

            // Save screenshot file for consistency
            try {
              final bytes = base64Decode(base64Data);
              final latestFile =
                  File('${app.projectPath}/latest_screenshot.png');
              await latestFile.writeAsBytes(bytes);
              _logger.info(
                  'Screenshot saved to: ${latestFile.path} (${bytes.length} bytes)');
            } catch (e) {
              _logger.warning('Failed to save screenshot file: $e');
            }

            directVmService.dispose();
            return base64Data;
          } else {
            _logger.warning(
                'Direct connection screenshot failed: ${response.json}');
          }
        }

        directVmService.dispose();
      } catch (e) {
        _logger.warning('Direct VM service connection failed: $e');
      }

      _logger.severe('=== ALL SCREENSHOT METHODS FAILED ===');
      throw Exception(
          'No screenshot methods available. Tried: VM Service extensions, Backup script fallback');
    } catch (e) {
      _logger.severe('=== SCREENSHOT DEBUG END ===');
      _logger.severe('Final error: $e');
      throw Exception('Failed to capture screenshot: $e');
    }
  }

  Future<Map<String, dynamic>> getWidgetTree(String appId) async {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    if (app.vmService == null || app.isolateId == null) {
      throw Exception('VM Service not connected for app $appId');
    }

    try {
      // First, try to get widget summary tree which is more reliable
      try {
        final response = await app.vmService!.callServiceExtension(
          'ext.flutter.inspector.getSelectedSummaryWidget',
          isolateId: app.isolateId,
          args: {
            'previousSelectionId': null,
            'isAlive': true,
          },
        );

        if (response.json != null && response.json!.isNotEmpty) {
          return response.json!;
        }
      } catch (e) {
        _logger.fine('Selected summary widget not available: $e');
      }

      // Fallback to root widget tree
      final response = await app.vmService!.callServiceExtension(
        'ext.flutter.inspector.getRootWidgetTree',
        isolateId: app.isolateId,
        args: {
          'isSummaryTree': true,
          'withPreviews': false,
        },
      );

      return response.json ?? {};
    } catch (e) {
      _logger.warning('Failed to get widget tree: $e');

      // Try a simpler approach - get basic widget info
      try {
        final response = await app.vmService!.callServiceExtension(
          'ext.flutter.inspector.getRootWidget',
          isolateId: app.isolateId,
        );
        return response.json ?? {};
      } catch (e2) {
        _logger.warning('All widget tree methods failed: $e2');
        throw Exception('Failed to get widget tree: $e');
      }
    }
  }

  List<String> getLogs(String appId, {int? count}) {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    if (count != null) {
      return app.getRecentLogs(count);
    }
    return app.logs;
  }

  Map<String, dynamic> getAppInfo(String appId) {
    final app = _apps[appId];
    if (app == null) {
      throw Exception('App $appId not found');
    }

    return {
      'id': appId,
      'state': app.state.name,
      'projectPath': app.projectPath,
      'targetFile': app.targetFile,
      'deviceId': app.deviceId,
      'vmServiceUri': app.vmServiceUri,
      'vmServicePort': app.vmServicePort,
      'ddsPort': app.ddsPort,
      'hasVmService': app.vmService != null,
      'logCount': app.logs.length,
    };
  }

  List<Map<String, dynamic>> listApps() {
    return _apps.entries
        .map((entry) => {
              'id': entry.key,
              'state': entry.value.state.name,
              'projectPath': entry.value.projectPath,
            })
        .toList();
  }

  Future<void> dispose() async {
    for (final appId in _apps.keys.toList()) {
      try {
        await stopApp(appId);
      } catch (e) {
        _logger.warning('Error stopping app $appId: $e');
      }
    }
    _apps.clear();
  }
}
