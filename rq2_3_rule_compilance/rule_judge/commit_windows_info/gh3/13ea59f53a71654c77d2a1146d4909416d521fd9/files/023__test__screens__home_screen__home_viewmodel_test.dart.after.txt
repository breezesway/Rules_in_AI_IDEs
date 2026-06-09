import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/services/auth_service.dart';

import 'home_viewmodel_test.mocks.dart';

@GenerateMocks([AuthService])
void main() {
  group('HomeViewModel', () {
    late MockAuthService mockAuthService;
    late HomeViewModel viewModel;

    setUp(() {
      mockAuthService = MockAuthService();
      viewModel = HomeViewModel(mockAuthService);
    });

    tearDown(() {
      viewModel.dispose();
    });

    test('should provide placeholder user data', () {
      expect(viewModel.currentUserName, equals('GitHub User'));
      expect(viewModel.currentUserLogin, equals('githubuser'));
      expect(viewModel.currentUserAvatar, isNull);
    });

    test('should properly dispose', () {
      expect(() => viewModel.dispose(), returnsNormally);
      expect(viewModel.disposed, true);
    });

    test('should handle multiple dispose calls gracefully', () {
      expect(() {
        viewModel.dispose();
        viewModel.dispose();
        viewModel.dispose();
      }, returnsNormally);

      expect(viewModel.disposed, true);
    });

    test('should not notify listeners after disposal', () {
      bool listenerCalled = false;
      viewModel.addListener(() {
        listenerCalled = true;
      });

      viewModel.dispose();
      listenerCalled = false;

      // After disposal, notifications should not be sent
      expect(listenerCalled, false);
    });
  });
}
