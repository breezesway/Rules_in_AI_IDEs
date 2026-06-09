import 'package:flutter/foundation.dart';

/// Base class for ViewModels that provides disposal pattern for proper resource cleanup.
abstract class DisposableViewModel extends ChangeNotifier {
  bool _disposed = false;

  /// Whether this ViewModel has been disposed.
  bool get disposed => _disposed;

  @override
  void dispose() {
    if (_disposed) return;

    _disposed = true;
    onDispose();
    super.dispose();
  }

  /// Override this method to perform custom cleanup logic.
  /// This is called before the ViewModel is disposed.
  void onDispose() {}

  @override
  void notifyListeners() {
    if (!_disposed) {
      super.notifyListeners();
    }
  }

  @override
  void addListener(VoidCallback listener) {
    if (!_disposed) {
      super.addListener(listener);
    }
  }

  @override
  void removeListener(VoidCallback listener) {
    if (!_disposed) {
      super.removeListener(listener);
    }
  }
}
