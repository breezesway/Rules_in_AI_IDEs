import 'dart:convert';
import 'dart:developer' as developer;
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';

class ScreenshotWrapper extends StatefulWidget {
  final Widget child;

  const ScreenshotWrapper({Key? key, required this.child}) : super(key: key);

  @override
  State<ScreenshotWrapper> createState() => _ScreenshotWrapperState();
}

class _ScreenshotWrapperState extends State<ScreenshotWrapper> {
  final GlobalKey _repaintBoundaryKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    debugPrint('ScreenshotWrapper initState called');
    _registerScreenshotExtension();
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
      developer.registerExtension('ext.gh3.screenshot', (
        method,
        parameters,
      ) async {
        try {
          // Capture screenshot on-demand when requested
          final screenshot = await _captureScreenshot();
          if (screenshot != null) {
            return developer.ServiceExtensionResponse.result(
              json.encode({
                'success': true,
                'screenshot': screenshot,
                'timestamp': DateTime.now().toIso8601String(),
                'format': 'png',
                'method': 'render_repaint_boundary',
              }),
            );
          } else {
            return developer.ServiceExtensionResponse.error(
              -32602, // kInvalidParams
              'Failed to capture screenshot',
            );
          }
        } catch (e) {
          return developer.ServiceExtensionResponse.error(
            -32603, // kInternalError
            'Screenshot error: $e',
          );
        }
      });

      debugPrint('Screenshot service extension registered: ext.gh3.screenshot');

      // Also register a simpler extension for testing
      developer.registerExtension('ext.gh3.test', (method, parameters) async {
        return developer.ServiceExtensionResponse.result(
          '{"test": "working", "mode": "on_demand"}',
        );
      });
    } catch (e) {
      debugPrint('Failed to setup service extension: $e');
    }
  }

  Future<String?> _captureScreenshot() async {
    try {
      final RenderRepaintBoundary? boundary =
          _repaintBoundaryKey.currentContext?.findRenderObject()
              as RenderRepaintBoundary?;

      if (boundary == null) {
        debugPrint('RenderRepaintBoundary not found');
        return null;
      }

      // Capture the image with high quality
      final ui.Image image = await boundary.toImage(pixelRatio: 2.0);
      final ByteData? byteData = await image.toByteData(
        format: ui.ImageByteFormat.png,
      );

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

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(key: _repaintBoundaryKey, child: widget.child);
  }
}
