import 'dart:io';
import 'dart:convert';
import 'dart:async';
import 'package:test/test.dart';
import 'package:vm_service/vm_service.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

/// Test utilities for Flutter Automation MCP Server
class TestUtils {
  /// Creates a temporary directory for testing
  static Directory createTempDir() {
    final tempDir = Directory.systemTemp.createTempSync('flutter_automation_test_');
    addTearDown(() {
      if (tempDir.existsSync()) {
        tempDir.deleteSync(recursive: true);
      }
    });
    return tempDir;
  }
  
  /// Creates a mock Flutter project structure
  static Directory createMockFlutterProject({String? name}) {
    final projectName = name ?? 'test_flutter_app';
    final projectDir = createTempDir();
    final libDir = Directory('${projectDir.path}/lib');
    libDir.createSync();
    
    // Create pubspec.yaml
    final pubspecFile = File('${projectDir.path}/pubspec.yaml');
    pubspecFile.writeAsStringSync('''
name: $projectName
description: A test Flutter application
version: 1.0.0+1

environment:
  sdk: ^3.0.0
  flutter: ">=3.0.0"

dependencies:
  flutter:
    sdk: flutter

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
''');
    
    // Create main.dart
    final mainFile = File('${libDir.path}/main.dart');
    mainFile.writeAsStringSync('''
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Test Flutter App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Test Flutter App Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '\$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
''');
    
    return projectDir;
  }
  
  /// Creates a mock VM service response
  static Map<String, dynamic> createMockVmResponse({
    String? version,
    List<String>? isolateIds,
  }) {
    return {
      'type': 'VM',
      'name': 'vm',
      'architectureBits': 64,
      'hostCPU': 'arm64',
      'operatingSystem': 'macos',
      'targetCPU': 'arm64',
      'version': version ?? '3.8.1 (stable)',
      'pid': 12345,
      'startTime': DateTime.now().millisecondsSinceEpoch,
      'isolates': isolateIds?.map((id) => {
        'type': '@Isolate',
        'id': id,
        'number': id.split('/').last,
        'name': 'main',
        'isSystemIsolate': false,
      }).toList() ?? [
        {
          'type': '@Isolate',
          'id': 'isolates/123456789',
          'number': '123456789',
          'name': 'main',
          'isSystemIsolate': false,
        }
      ],
    };
  }
  
  /// Creates a mock screenshot response
  static Map<String, dynamic> createMockScreenshotResponse() {
    // Create a simple base64 encoded 1x1 pixel PNG
    final pngBytes = [
      0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, // PNG signature
      0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, // IHDR chunk
      0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, // 1x1 dimensions
      0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
      0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41, // IDAT chunk
      0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
      0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
      0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, // IEND chunk
      0x42, 0x60, 0x82
    ];
    
    return {
      'type': 'Success',
      'screenshot': base64Encode(pngBytes),
    };
  }
  
  /// Creates a mock widget tree response
  static Map<String, dynamic> createMockWidgetTreeResponse() {
    return {
      'type': 'Success',
      'result': {
        'objectGroupName': 'group-1',
        'valueId': 'inspector-0',
        'type': 'DiagnosticsNode',
        'description': 'MyApp',
        'name': 'widget',
        'children': [
          {
            'objectGroupName': 'group-1',
            'valueId': 'inspector-1',
            'type': 'DiagnosticsNode',
            'description': 'MaterialApp',
            'name': 'child',
            'children': [
              {
                'objectGroupName': 'group-1',
                'valueId': 'inspector-2',
                'type': 'DiagnosticsNode',
                'description': 'MyHomePage',
                'name': 'home',
                'children': [],
              }
            ],
          }
        ],
      },
    };
  }
  
  /// Waits for a condition to be true with timeout
  static Future<void> waitForCondition(
    bool Function() condition, {
    Duration timeout = const Duration(seconds: 5),
    Duration pollInterval = const Duration(milliseconds: 100),
  }) async {
    final stopwatch = Stopwatch()..start();
    
    while (!condition() && stopwatch.elapsed < timeout) {
      await Future.delayed(pollInterval);
    }
    
    if (!condition()) {
      throw TimeoutException('Condition not met within $timeout', timeout);
    }
  }
  
  /// Creates a mock process that outputs specific lines
  static Map<String, dynamic> createMockProcessInfo({
    List<String>? stdoutLines,
    List<String>? stderrLines,
    int exitCode = 0,
  }) {
    return {
      'stdoutLines': stdoutLines ?? [],
      'stderrLines': stderrLines ?? [],
      'exitCode': exitCode,
    };
  }
}

/// Custom matchers for testing
class CustomMatchers {
  /// Matcher for checking if a string contains VM service URL
  static Matcher containsVmServiceUrl() {
    return predicate<String>(
      (value) => RegExp(r'VM Service[^\n]*at[:\s]+(http[^\s]+)').hasMatch(value),
      'contains VM service URL',
    );
  }
  
  /// Matcher for checking base64 encoded images
  static Matcher isBase64Image() {
    return predicate<String>(
      (value) {
        try {
          final decoded = base64Decode(value);
          // Check if it starts with PNG signature
          return decoded.length > 8 && 
                 decoded[0] == 0x89 && 
                 decoded[1] == 0x50 && 
                 decoded[2] == 0x4E && 
                 decoded[3] == 0x47;
        } catch (e) {
          return false;
        }
      },
      'is base64 encoded PNG image',
    );
  }
}

/// Test data constants
class TestData {
  static const String sampleVmServiceOutput = '''
Flutter run key commands.
r Hot reload. 🔥🔥🔥
R Hot restart.
h List all available interactive commands.
d Detach (terminate "flutter run" but leave application running).
c Clear the screen
q Quit (terminate the application on the device).

A Dart VM Service on iPhone is available at: http://127.0.0.1:8181/abc123def456/
The Flutter DevTools debugger and profiler on iPhone is available at:
http://127.0.0.1:9103?uri=http://127.0.0.1:8181/abc123def456/
''';

  static const String sampleErrorOutput = '''
══╡ EXCEPTION CAUGHT BY WIDGETS LIBRARY ╞════════════════════════════════════════
The following assertion was thrown building MyWidget:
RenderFlex overflowed by 42.0 pixels on the right.
════════════════════════════════════════════════════════════════════════════════
''';

  static const String sampleFlutterDevicesJson = '''
[
  {
    "id": "chrome",
    "name": "Chrome",
    "platform": "web-javascript",
    "emulator": false
  },
  {
    "id": "00008120-001471901EE0201E",
    "name": "iPhone 14 Pro Max",
    "platform": "ios",
    "emulator": false
  }
]
''';
}