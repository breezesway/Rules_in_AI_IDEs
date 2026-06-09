import 'dart:async';
import 'package:injectable/injectable.dart';

/// Service for handling timer operations like delays.
/// This allows for better testability by injecting mock implementations.
abstract class TimerService {
  /// Delays execution for the specified duration.
  ///
  /// [duration] - The duration to delay for.
  /// Returns a Future that completes after the specified duration.
  Future<void> delay(Duration duration);
}

/// Default implementation of TimerService using dart:async.
@LazySingleton(as: TimerService)
class DefaultTimerService implements TimerService {
  @override
  Future<void> delay(Duration duration) async {
    await Future.delayed(duration);
  }
}
