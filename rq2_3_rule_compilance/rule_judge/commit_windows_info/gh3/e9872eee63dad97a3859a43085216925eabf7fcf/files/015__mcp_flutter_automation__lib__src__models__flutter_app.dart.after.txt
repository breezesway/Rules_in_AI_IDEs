import 'dart:io';
import 'package:vm_service/vm_service.dart';

enum AppState {
  notStarted,
  starting,
  running,
  stopped,
  error,
}

class FlutterApp {
  final String projectPath;
  final String? targetFile;
  final String? deviceId;
  final int vmServicePort;
  final int ddsPort;
  
  Process? _process;
  VmService? _vmService;
  AppState _state = AppState.notStarted;
  final List<String> _logs = [];
  final int maxLogLines = 1000;
  
  String? _vmServiceUri;
  String? _isolateId;
  
  FlutterApp({
    required this.projectPath,
    this.targetFile,
    this.deviceId,
    this.vmServicePort = 8182,
    this.ddsPort = 8181,
  });
  
  Process? get process => _process;
  VmService? get vmService => _vmService;
  AppState get state => _state;
  List<String> get logs => List.unmodifiable(_logs);
  String? get vmServiceUri => _vmServiceUri;
  String? get isolateId => _isolateId;
  
  set process(Process? proc) => _process = proc;
  set vmService(VmService? service) => _vmService = service;
  set state(AppState newState) => _state = newState;
  set vmServiceUri(String? uri) => _vmServiceUri = uri;
  set isolateId(String? id) => _isolateId = id;
  
  void addLog(String log) {
    _logs.add(log);
    if (_logs.length > maxLogLines) {
      _logs.removeAt(0);
    }
  }
  
  void clearLogs() {
    _logs.clear();
  }
  
  List<String> getRecentLogs(int count) {
    if (_logs.length <= count) {
      return List.from(_logs);
    }
    return _logs.sublist(_logs.length - count);
  }
}