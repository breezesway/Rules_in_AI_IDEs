import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'package:vm_service/vm_service.dart';
import 'package:web_socket_channel/io.dart';
import 'package:http/http.dart' as http;
import 'models/flutter_app.dart';

class FlutterController {
  final _logger = Logger('FlutterController');
  final Map<String, FlutterApp> _apps = {};
  
  FlutterController() {
    // Enable detailed logging
    Logger.root.level = Level.ALL;
    Logger.root.onRecord.listen((record) {
      print('${record.level.name}: ${record.time}: ${record.message}');
      if (record.error != null) {
        print('ERROR: ${record.error}');
      }
      if (record.stackTrace != null) {
        print('STACK: ${record.stackTrace}');
      }
    });
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
      if (existingApp.state == AppState.running || existingApp.state == AppState.starting) {
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
      
      // Start the process
      final process = await Process.start(
        command.first,
        command.skip(1).toList(),
        workingDirectory: projectPath,
        mode: ProcessStartMode.normal,
      );
      
      app.process = process;
      
      // Listen to stdout
      process.stdout.transform(utf8.decoder).listen((data) {
        app.addLog(data);
        _logger.fine('Flutter stdout: $data');
        
        // Look for VM service URL
        final vmServiceMatch = RegExp(r'VM Service[^\n]*at[:\s]+(http[^\s]+)').firstMatch(data);
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
      _logger.info('Connecting to VM Service via DDS at: $ddsUri');
      
      // Retry connection up to 3 times with delays
      VmService? vmService;
      for (int attempt = 1; attempt <= 3; attempt++) {
        try {
          final channel = IOWebSocketChannel.connect(ddsUri);
          vmService = VmService(
            channel.stream,
            (message) => channel.sink.add(message),
          );
          
          // Test the connection by getting VM info
          final vm = await vmService.getVM().timeout(Duration(seconds: 5));
          _logger.info('Connected to VM: ${vm.name} (attempt $attempt)');
          
          // Get main isolate
          if (vm.isolates?.isNotEmpty ?? false) {
            app.isolateId = vm.isolates!.first.id;
            _logger.info('Found isolate: ${app.isolateId}');
          }
          
          app.vmService = vmService;
          return; // Success!
          
        } catch (e) {
          _logger.warning('Connection attempt $attempt failed: $e');
          vmService?.dispose();
          
          if (attempt < 3) {
            await Future.delayed(Duration(milliseconds: 1000 * attempt));
          }
        }
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
      throw Exception('App $appId not found');
    }
    
    _logger.info('Screenshot request for app $appId - VM Service: ${app.vmService != null}, Isolate: ${app.isolateId}');
    
    if (app.vmService == null || app.isolateId == null) {
      throw Exception('VM Service not connected for app $appId');
    }
    
    try {
      // Try our custom gh3 screenshot extension first (RenderRepaintBoundary approach)
      try {
        _logger.info('Calling ext.gh3.screenshot extension...');
        final response = await app.vmService!.callServiceExtension(
          'ext.gh3.screenshot',
          isolateId: app.isolateId,
        );
        
        _logger.info('ext.gh3.screenshot response: ${response.json}');
        _logger.info('Response type: ${response.json.runtimeType}');
        _logger.info('Response keys: ${response.json?.keys.toList()}');
        
        if (response.json != null && response.json!.containsKey('result')) {
          final result = response.json!['result'];
          _logger.info('Result type: ${result.runtimeType}');
          _logger.info('Result content preview: ${result.toString().substring(0, 100)}...');
          
          // Handle different response formats
          String? resultString;
          if (result is String) {
            resultString = result;
            _logger.info('Got result as string, length: ${resultString.length}');
          } else if (result != null) {
            resultString = json.encode(result);
            _logger.info('Encoded result to string, length: ${resultString.length}');
          }
          
          if (resultString != null) {
            try {
              final responseData = json.decode(resultString);
              _logger.info('Decoded response data: ${responseData.keys.toList()}');
              if (responseData['success'] == true && responseData['screenshot'] != null) {
                final base64Data = responseData['screenshot'] as String;
                _logger.info('Screenshot captured via custom gh3 extension, size: ${base64Data.length}');
                
                // Save screenshot to file
                try {
                  final bytes = base64Decode(base64Data);
                  final timestamp = DateTime.now().millisecondsSinceEpoch;
                  final fileName = 'screenshot_${timestamp}.png';
                  final filePath = '${app.projectPath}/$fileName';
                  final file = File(filePath);
                  await file.writeAsBytes(bytes);
                  _logger.info('Screenshot saved to: $filePath (${bytes.length} bytes)');
                  
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
                _logger.warning('Response data missing success or screenshot field');
              }
            } catch (e) {
              _logger.severe('Failed to decode result string: $e');
            }
          } else {
            _logger.warning('Could not extract result string');
          }
        }
      } catch (e) {
        _logger.severe('Custom gh3 screenshot extension failed: $e');
        _logger.severe('Exception type: ${e.runtimeType}');
        if (e is Exception) {
          _logger.severe('Exception details: $e');
        }
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
          final isolate = await app.vmService!.getIsolate(vm.isolates!.first.id!);
          _logger.info('Available extensions: ${isolate.extensionRPCs}');
        }
      } catch (e) {
        _logger.fine('Could not list extensions: $e');
      }
      
      throw Exception('No screenshot extensions available. Available methods: RenderRepaintBoundary (ext.gh3.screenshot), Flutter Driver (ext.flutter.driver.screenshot)');
      
    } catch (e) {
      _logger.warning('Screenshot failed: $e');
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
    return _apps.entries.map((entry) => {
      'id': entry.key,
      'state': entry.value.state.name,
      'projectPath': entry.value.projectPath,
    }).toList();
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