import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'flutter_controller.dart';
import 'screenshot_server.dart';

// Simplified MCP server base class for testing
abstract class MCPBase {
  final Map<String, dynamic> serverInfo;
  MCPBase({required this.serverInfo});
}

class FlutterAutomationMCPServer extends MCPBase {
  final _logger = Logger('FlutterAutomationMCPServer');
  late final FlutterController _controller;
  late final ScreenshotServer _screenshotServer;
  
  FlutterAutomationMCPServer() : super(
    serverInfo: {
      'name': 'flutter-automation',
      'version': '1.0.0',
    },
  ) {
    _controller = FlutterController();
    _screenshotServer = ScreenshotServer();
  }
  
  FlutterController get controller => _controller;
  
  // Simplified tool execution for testing
  Future<Map<String, dynamic>> executeTool(String toolName, Map<String, dynamic> params) async {
    try {
      switch (toolName) {
        case 'launch_app':
          final appId = params['appId'] as String;
          final projectPath = params['projectPath'] as String;
          final targetFile = params['targetFile'] as String?;
          final deviceId = params['deviceId'] as String?;
          final vmServicePort = params['vmServicePort'] as int? ?? 8182;
          final ddsPort = params['ddsPort'] as int? ?? 8181;
          
          final app = await _controller.launchApp(
            appId: appId,
            projectPath: projectPath,
            targetFile: targetFile,
            deviceId: deviceId,
            vmServicePort: vmServicePort,
            ddsPort: ddsPort,
          );
          
          return {
            'success': true,
            'message': 'App launched successfully',
            'appInfo': _controller.getAppInfo(appId),
          };
          
        case 'hot_reload':
          final appId = params['appId'] as String;
          await _controller.hotReload(appId);
          return {
            'success': true,
            'message': 'Hot reload completed',
          };
          
        case 'hot_restart':
          final appId = params['appId'] as String;
          await _controller.hotRestart(appId);
          return {
            'success': true,
            'message': 'Hot restart completed',
          };
          
        case 'stop_app':
          final appId = params['appId'] as String;
          await _controller.stopApp(appId);
          return {
            'success': true,
            'message': 'App stopped',
          };
          
        case 'capture_screenshot':
          final appId = params['appId'] as String;
          _logger.info('Received screenshot request for app: $appId');
          
          // Try VM service screenshot first
          try {
            _logger.info('Attempting VM service screenshot...');
            final screenshot = await _controller.captureScreenshot(appId);
            if (screenshot != null) {
              _logger.info('VM service screenshot successful, size: ${screenshot.length}');
              return {
                'success': true,
                'screenshot': screenshot,
                'format': 'base64',
                'method': 'vm_service',
              };
            }
          } catch (e) {
            _logger.warning('VM Service screenshot failed: $e');
          }
          
          // Fallback to screenshot server (RenderRepaintBoundary)
          _logger.info('Trying screenshot server fallback...');
          final latestScreenshot = _screenshotServer.getLatestScreenshot();
          if (latestScreenshot != null) {
            _logger.info('Screenshot server has screenshot, size: ${latestScreenshot.length}');
            return {
              'success': true,
              'screenshot': latestScreenshot,
              'format': 'base64',
              'method': 'render_repaint_boundary',
              'timestamp': _screenshotServer.getScreenshotTimestamp()?.toIso8601String(),
            };
          }
          
          _logger.warning('No screenshot available from any method');
          return {
            'success': false,
            'error': 'No screenshot available from any method',
          };
          
        case 'get_logs':
          final appId = params['appId'] as String;
          final count = params['count'] as int?;
          final logs = _controller.getLogs(appId, count: count);
          return {
            'success': true,
            'logs': logs,
            'count': logs.length,
          };
          
        case 'get_widget_tree':
          final appId = params['appId'] as String;
          final tree = await _controller.getWidgetTree(appId);
          return {
            'success': true,
            'widgetTree': tree,
          };
          
        case 'list_apps':
          final apps = _controller.listApps();
          return {
            'success': true,
            'apps': apps,
          };
          
        case 'get_app_info':
          final appId = params['appId'] as String;
          final info = _controller.getAppInfo(appId);
          return {
            'success': true,
            'appInfo': info,
          };
          
        default:
          throw Exception('Unknown tool: $toolName');
      }
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }
  
  // Simplified resource access for testing
  Future<String> getResource(String uri) async {
    try {
      switch (uri) {
        case 'devices://list':
          final result = await Process.run('flutter', ['devices', '--machine']);
          if (result.exitCode == 0) {
            final devices = json.decode(result.stdout);
            return json.encode({
              'devices': devices,
              'count': devices.length,
            });
          } else {
            return json.encode({
              'error': 'Failed to get devices: ${result.stderr}',
            });
          }
          
        case 'flutter://doctor':
          final result = await Process.run('flutter', ['doctor', '-v']);
          return result.stdout;
          
        default:
          throw Exception('Unknown resource: $uri');
      }
    } catch (e) {
      return json.encode({
        'error': 'Failed to get resource: $e',
      });
    }
  }
  
  Future<void> start() async {
    _logger.info('Starting Flutter Automation MCP Server');
    
    // Start the screenshot server
    try {
      await _screenshotServer.start(port: 3000);
    } catch (e) {
      _logger.warning('Failed to start screenshot server: $e');
    }
    
    // Listen for MCP protocol messages on stdin
    await for (final line in stdin.transform(utf8.decoder).transform(LineSplitter())) {
      if (line.trim().isEmpty) continue;
      
      try {
        final request = json.decode(line);
        final response = await _handleMCPRequest(request);
        if (response != null) {
          stdout.writeln(json.encode(response));
        }
      } catch (e) {
        _logger.severe('Error processing MCP request: $e');
        // Send error response
        final errorResponse = {
          'jsonrpc': '2.0',
          'id': null,
          'error': {
            'code': -32603,
            'message': 'Internal error: $e',
          },
        };
        stdout.writeln(json.encode(errorResponse));
      }
    }
  }
  
  Future<Map<String, dynamic>?> _handleMCPRequest(Map<String, dynamic> request) async {
    final method = request['method'] as String?;
    final params = request['params'] as Map<String, dynamic>? ?? {};
    final id = request['id'];
    
    switch (method) {
      case 'initialize':
        return {
          'jsonrpc': '2.0',
          'id': id,
          'result': {
            'protocolVersion': '2024-11-05',
            'capabilities': {
              'tools': {},
              'resources': {},
            },
            'serverInfo': serverInfo,
          },
        };
        
      case 'tools/list':
        return {
          'jsonrpc': '2.0',
          'id': id,
          'result': {
            'tools': [
              {
                'name': 'launch_app',
                'description': 'Launch a Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                    'projectPath': {'type': 'string'},
                    'targetFile': {'type': 'string'},
                    'deviceId': {'type': 'string'},
                    'vmServicePort': {'type': 'integer'},
                    'ddsPort': {'type': 'integer'},
                  },
                  'required': ['appId', 'projectPath'],
                },
              },
              {
                'name': 'hot_reload',
                'description': 'Perform hot reload on a running Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'hot_restart',
                'description': 'Perform hot restart on a running Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'stop_app',
                'description': 'Stop a running Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'capture_screenshot',
                'description': 'Capture screenshot of a running Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'get_logs',
                'description': 'Get logs from a Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                    'count': {'type': 'integer'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'get_widget_tree',
                'description': 'Get widget tree from a running Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
              {
                'name': 'list_apps',
                'description': 'List all managed Flutter apps',
                'inputSchema': {
                  'type': 'object',
                  'properties': {},
                },
              },
              {
                'name': 'get_app_info',
                'description': 'Get information about a specific Flutter app',
                'inputSchema': {
                  'type': 'object',
                  'properties': {
                    'appId': {'type': 'string'},
                  },
                  'required': ['appId'],
                },
              },
            ],
          },
        };
        
      case 'resources/list':
        return {
          'jsonrpc': '2.0',
          'id': id,
          'result': {
            'resources': [
              {
                'uri': 'devices://list',
                'name': 'Flutter Devices',
                'description': 'List of available Flutter devices',
                'mimeType': 'application/json',
              },
              {
                'uri': 'flutter://doctor',
                'name': 'Flutter Doctor',
                'description': 'Flutter doctor output',
                'mimeType': 'text/plain',
              },
            ],
          },
        };
        
      case 'tools/call':
        final toolName = params['name'] as String;
        final toolArgs = params['arguments'] as Map<String, dynamic>? ?? {};
        final result = await executeTool(toolName, toolArgs);
        
        return {
          'jsonrpc': '2.0',
          'id': id,
          'result': {
            'content': [
              {
                'type': 'text',
                'text': json.encode(result),
              },
            ],
          },
        };
        
      case 'resources/read':
        final uri = params['uri'] as String;
        final content = await getResource(uri);
        
        return {
          'jsonrpc': '2.0',
          'id': id,
          'result': {
            'contents': [
              {
                'uri': uri,
                'mimeType': 'application/json',
                'text': content,
              },
            ],
          },
        };
        
      case 'notifications/initialized':
        // No response needed for notifications
        return null;
        
      default:
        return {
          'jsonrpc': '2.0',
          'id': id,
          'error': {
            'code': -32601,
            'message': 'Method not found: $method',
          },
        };
    }
  }
  
  Future<void> stop() async {
    _logger.info('Stopping Flutter Automation MCP Server');
    await _controller.dispose();
    await _screenshotServer.stop();
  }
}