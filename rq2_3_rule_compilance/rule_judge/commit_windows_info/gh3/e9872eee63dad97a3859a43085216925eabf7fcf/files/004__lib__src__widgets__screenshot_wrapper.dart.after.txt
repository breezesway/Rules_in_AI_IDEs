import 'dart:async';
import 'dart:convert';
import 'dart:developer' as developer;
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

class ScreenshotWrapper extends StatefulWidget {
  final Widget child;
  
  const ScreenshotWrapper({
    Key? key,
    required this.child,
  }) : super(key: key);

  @override
  State<ScreenshotWrapper> createState() => _ScreenshotWrapperState();
}

class _ScreenshotWrapperState extends State<ScreenshotWrapper> {
  final GlobalKey _repaintBoundaryKey = GlobalKey();
  String? _latestScreenshot;
  DateTime? _screenshotTimestamp;
  
  @override
  void initState() {
    super.initState();
    debugPrint('ScreenshotWrapper initState called');
    _registerScreenshotExtension();
    
    // Auto-capture screenshot every 5 seconds and store in memory
    Timer.periodic(Duration(seconds: 5), (timer) {
      _captureAndStoreScreenshot();
    });
    debugPrint('ScreenshotWrapper initState completed');
  }

  void _registerScreenshotExtension() {
    // Register a custom service extension for screenshots
    try {
      debugPrint('Starting screenshot extension registration...');
      // Register immediately - no need to wait for frame callback
      _setupServiceExtension();
      debugPrint('Screenshot extension registration completed');
    } catch (e) {
      debugPrint('ERROR: Failed to register screenshot extension: $e');
    }
  }

  void _setupServiceExtension() {
    try {
      // Register service extension for screenshot capture
      developer.registerExtension(
        'ext.gh3.screenshot',
        (method, parameters) async {
          try {
            // Return the latest stored screenshot
            if (_latestScreenshot != null) {
              return developer.ServiceExtensionResponse.result(json.encode({
                'success': true,
                'screenshot': _latestScreenshot,
                'timestamp': _screenshotTimestamp?.toIso8601String(),
                'format': 'png',
                'method': 'render_repaint_boundary',
              }));
            } else {
              return developer.ServiceExtensionResponse.error(
                -32602, // kInvalidParams
                'No screenshot available yet',
              );
            }
          } catch (e) {
            return developer.ServiceExtensionResponse.error(
              -32603, // kInternalError
              'Screenshot error: $e',
            );
          }
        },
      );
      
      debugPrint('Screenshot service extension registered: ext.gh3.screenshot');
      
      // Also register a simpler extension for testing
      developer.registerExtension(
        'ext.gh3.test',
        (method, parameters) async {
          return developer.ServiceExtensionResponse.result('{"test": "working", "hasScreenshot": ${_latestScreenshot != null}}');
        },
      );
      
    } catch (e) {
      debugPrint('Failed to setup service extension: $e');
    }
  }

  Future<String?> _captureScreenshot() async {
    try {
      final RenderRepaintBoundary? boundary = 
          _repaintBoundaryKey.currentContext?.findRenderObject() as RenderRepaintBoundary?;
      
      if (boundary == null) {
        debugPrint('RenderRepaintBoundary not found');
        return null;
      }

      // Capture the image with high quality
      final ui.Image image = await boundary.toImage(pixelRatio: 2.0);
      final ByteData? byteData = await image.toByteData(format: ui.ImageByteFormat.png);
      
      if (byteData == null) {
        debugPrint('Failed to convert image to bytes');
        return null;
      }

      final Uint8List pngBytes = byteData.buffer.asUint8List();
      final String base64Image = base64Encode(pngBytes);
      
      debugPrint('Screenshot captured: ${pngBytes.length} bytes');
      return base64Image;
    } catch (e) {
      debugPrint('Screenshot capture failed: $e');
      return null;
    }
  }

  Future<void> _captureAndStoreScreenshot() async {
    try {
      final screenshot = await _captureScreenshot();
      if (screenshot != null) {
        setState(() {
          _latestScreenshot = screenshot;
          _screenshotTimestamp = DateTime.now();
        });
        debugPrint('Screenshot stored in memory: ${screenshot.length} characters at $_screenshotTimestamp');
      }
    } catch (e) {
      debugPrint('Auto screenshot failed: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      key: _repaintBoundaryKey,
      child: widget.child,
    );
  }
}

