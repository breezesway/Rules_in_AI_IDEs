import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';

class ScreenshotServer {
  final _logger = Logger('ScreenshotServer');
  HttpServer? _server;
  String? _latestScreenshot;
  DateTime? _screenshotTimestamp;
  
  Future<void> start({int port = 3000}) async {
    try {
      _server = await HttpServer.bind(InternetAddress.loopbackIPv4, port);
      _logger.info('Screenshot server started on http://127.0.0.1:$port');
      
      _server!.listen((HttpRequest request) async {
        await _handleRequest(request);
      });
    } catch (e) {
      _logger.severe('Failed to start screenshot server: $e');
      rethrow;
    }
  }
  
  Future<void> _handleRequest(HttpRequest request) async {
    try {
      // Add CORS headers
      request.response.headers.add('Access-Control-Allow-Origin', '*');
      request.response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
      request.response.headers.add('Access-Control-Allow-Headers', 'Content-Type');
      
      if (request.method == 'OPTIONS') {
        request.response.statusCode = 200;
        await request.response.close();
        return;
      }
      
      if (request.uri.path == '/screenshot' && request.method == 'POST') {
        await _handleScreenshotUpload(request);
      } else if (request.uri.path == '/screenshot' && request.method == 'GET') {
        await _handleScreenshotDownload(request);
      } else if (request.uri.path == '/health' && request.method == 'GET') {
        await _handleHealthCheck(request);
      } else {
        request.response.statusCode = 404;
        request.response.write('Not Found');
        await request.response.close();
      }
    } catch (e) {
      _logger.warning('Request handling error: $e');
      request.response.statusCode = 500;
      request.response.write('Internal Server Error');
      await request.response.close();
    }
  }
  
  Future<void> _handleScreenshotUpload(HttpRequest request) async {
    try {
      final body = await utf8.decoder.bind(request).join();
      final data = json.decode(body);
      
      _latestScreenshot = data['image'] as String?;
      _screenshotTimestamp = DateTime.parse(data['timestamp'] as String);
      
      _logger.info('Screenshot received: ${_latestScreenshot?.length ?? 0} bytes at $_screenshotTimestamp');
      
      request.response.statusCode = 200;
      request.response.headers.contentType = ContentType.json;
      request.response.write(json.encode({
        'success': true,
        'message': 'Screenshot received',
        'timestamp': _screenshotTimestamp?.toIso8601String(),
      }));
      await request.response.close();
    } catch (e) {
      _logger.warning('Screenshot upload error: $e');
      request.response.statusCode = 400;
      request.response.write('Bad Request');
      await request.response.close();
    }
  }
  
  Future<void> _handleScreenshotDownload(HttpRequest request) async {
    try {
      if (_latestScreenshot == null) {
        request.response.statusCode = 404;
        request.response.headers.contentType = ContentType.json;
        request.response.write(json.encode({
          'error': 'No screenshot available',
        }));
        await request.response.close();
        return;
      }
      
      request.response.statusCode = 200;
      request.response.headers.contentType = ContentType.json;
      request.response.write(json.encode({
        'success': true,
        'image': _latestScreenshot,
        'timestamp': _screenshotTimestamp?.toIso8601String(),
        'format': 'png',
      }));
      await request.response.close();
    } catch (e) {
      _logger.warning('Screenshot download error: $e');
      request.response.statusCode = 500;
      request.response.write('Internal Server Error');
      await request.response.close();
    }
  }
  
  Future<void> _handleHealthCheck(HttpRequest request) async {
    request.response.statusCode = 200;
    request.response.headers.contentType = ContentType.json;
    request.response.write(json.encode({
      'status': 'healthy',
      'hasScreenshot': _latestScreenshot != null,
      'lastScreenshot': _screenshotTimestamp?.toIso8601String(),
    }));
    await request.response.close();
  }
  
  String? getLatestScreenshot() => _latestScreenshot;
  DateTime? getScreenshotTimestamp() => _screenshotTimestamp;
  
  Future<void> stop() async {
    if (_server != null) {
      await _server!.close();
      _logger.info('Screenshot server stopped');
    }
  }
}