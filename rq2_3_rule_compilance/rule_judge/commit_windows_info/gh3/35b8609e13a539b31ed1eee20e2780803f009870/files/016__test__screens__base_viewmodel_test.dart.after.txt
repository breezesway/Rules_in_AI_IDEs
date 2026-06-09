import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/screens/base_viewmodel.dart';

class TestViewModel extends DisposableViewModel {
  bool onDisposeCalled = false;
  int notifyCount = 0;

  @override
  void onDispose() {
    onDisposeCalled = true;
  }

  @override
  void notifyListeners() {
    if (!disposed) {
      notifyCount++;
    }
    super.notifyListeners();
  }

  void triggerNotify() {
    notifyListeners();
  }
}

void main() {
  group('DisposableViewModel', () {
    late TestViewModel viewModel;

    setUp(() {
      viewModel = TestViewModel();
    });

    test('should not be disposed initially', () {
      expect(viewModel.disposed, false);
    });

    test('should call onDispose when disposed', () {
      expect(viewModel.onDisposeCalled, false);

      viewModel.dispose();

      expect(viewModel.onDisposeCalled, true);
      expect(viewModel.disposed, true);
    });

    test('should not call onDispose multiple times', () {
      viewModel.dispose();
      expect(viewModel.onDisposeCalled, true);

      // Reset flag to test multiple dispose calls
      viewModel.onDisposeCalled = false;
      viewModel.dispose();

      expect(viewModel.onDisposeCalled, false);
    });

    test('should not notify listeners after disposal', () {
      // Add a listener to verify notifications work before disposal
      bool listenerCalled = false;
      viewModel.addListener(() {
        listenerCalled = true;
      });

      // Trigger notification before disposal
      viewModel.triggerNotify();
      expect(listenerCalled, true);
      expect(viewModel.notifyCount, 1);

      // Reset and dispose
      listenerCalled = false;
      final notifyCountBeforeDisposal = viewModel.notifyCount;
      viewModel.dispose();

      // Try to notify after disposal
      viewModel.triggerNotify();
      expect(listenerCalled, false);
      expect(
        viewModel.notifyCount,
        notifyCountBeforeDisposal,
      ); // Should not increment
    });

    test('should handle listeners properly during disposal', () {
      bool listenerCalled = false;
      void listener() {
        listenerCalled = true;
      }

      viewModel.addListener(listener);
      viewModel.dispose();

      // Should not throw when trying to notify after disposal
      expect(() => viewModel.triggerNotify(), returnsNormally);
      expect(listenerCalled, false);
    });
  });
}
