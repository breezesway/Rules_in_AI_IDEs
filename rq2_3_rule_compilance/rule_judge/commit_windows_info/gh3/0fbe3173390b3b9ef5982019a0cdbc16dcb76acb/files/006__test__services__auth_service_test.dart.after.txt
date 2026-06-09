import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/token_storage.dart';
import 'package:gh3/src/services/scope_service.dart';
import 'package:gh3/src/services/timer_service.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'auth_service_test.mocks.dart';

@GenerateMocks([GithubAuthClient, IScopeService, TimerService, ITokenStorage])
void main() {
  group('AuthService', () {
    late AuthService authService;
    late MockGithubAuthClient fakeAuthClient;
    late MockIScopeService fakeScopeService;
    late MockTimerService fakeTimerService;
    late ITokenStorage tokenStorage;

    setUp(() async {
      SharedPreferences.setMockInitialValues({});
      fakeAuthClient = MockGithubAuthClient();
      fakeScopeService = MockIScopeService();
      fakeTimerService = MockTimerService();
      tokenStorage = PrefsTokenStorage();
      authService = AuthService(
        fakeAuthClient,
        tokenStorage,
        fakeScopeService,
        fakeTimerService,
      );
    });

    test('init sets accessToken when scopes present', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenAnswer((_) async => ['repo', 'read:user']);

      await authService.init();

      expect(authService.accessToken, 'token1');
      expect(authService.isLoggedIn, isTrue);
    });

    test('init clears token when scopes missing', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenAnswer((_) async => ['read:user']);

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
    });

    test('login completes and stores token', () async {
      when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
        (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
      );
      when(
        fakeAuthClient.createAccessTokenFromDeviceCode(any),
      ).thenAnswer((_) async => 'new_token');

      final token = await authService.login();

      expect(token, 'new_token');
      expect(authService.accessToken, 'new_token');

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('github_access_token'), 'new_token');
    });

    test('logout clears token', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenAnswer((_) async => ['repo', 'read:user']);

      await authService.init();
      await authService.logout();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('github_access_token'), isNull);
    });

    test('init handles scope service exception gracefully', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenThrow(Exception('Network error'));

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('github_access_token'), isNull);
    });

    test('init handles null token correctly', () async {
      SharedPreferences.setMockInitialValues({});

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
      verifyNever(fakeScopeService.getScopesFromAccessToken(any));
    });

    test('loginWithDeviceCode completes and stores token', () async {
      when(
        fakeAuthClient.createAccessTokenFromDeviceCode(any),
      ).thenAnswer((_) async => 'new_token');

      final token = await authService.loginWithDeviceCode('device_code');

      expect(token, 'new_token');
      expect(authService.accessToken, 'new_token');

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('github_access_token'), 'new_token');
    });

    test('loginWithDeviceCode handles AuthorizationPendingException', () async {
      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount == 1) {
          throw AuthorizationPendingException();
        } else {
          return 'success_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.loginWithDeviceCode('device_code');

      expect(token, 'success_token');
      verify(fakeTimerService.delay(const Duration(seconds: 5))).called(1);
    });

    test('loginWithDeviceCode handles SlowDownException', () async {
      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount == 1) {
          throw SlowDownException();
        } else {
          return 'success_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.loginWithDeviceCode('device_code');

      expect(token, 'success_token');
      verify(fakeTimerService.delay(const Duration(seconds: 10))).called(1);
    });

    test('login handles multiple authorization pending exceptions', () async {
      when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
        (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
      );

      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount <= 3) {
          throw AuthorizationPendingException();
        } else {
          return 'success_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.login();

      expect(token, 'success_token');
      verify(fakeTimerService.delay(const Duration(seconds: 5))).called(3);
    });

    test('login handles mixed exception types', () async {
      when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
        (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
      );

      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount == 1) {
          throw AuthorizationPendingException();
        } else if (callCount == 2) {
          throw SlowDownException();
        } else {
          return 'mixed_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.login();

      expect(token, 'mixed_token');
      verify(fakeTimerService.delay(const Duration(seconds: 5))).called(1);
      verify(fakeTimerService.delay(const Duration(seconds: 10))).called(1);
    });

    test('init clears token when scope service throws exception', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenThrow(Exception('Scope validation failed'));

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getString('github_access_token'), isNull);
    });

    test('checkTokenValid returns false for insufficient scopes', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenAnswer((_) async => ['read:user']); // Missing 'repo' scope

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
    });

    test('checkTokenValid returns false for empty scopes', () async {
      SharedPreferences.setMockInitialValues({'github_access_token': 'token1'});
      when(
        fakeScopeService.getScopesFromAccessToken(any),
      ).thenAnswer((_) async => []); // No scopes

      await authService.init();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
    });

    test(
      'checkTokenValid returns true when all required scopes present with extras',
      () async {
        SharedPreferences.setMockInitialValues({
          'github_access_token': 'token1',
        });
        when(fakeScopeService.getScopesFromAccessToken(any)).thenAnswer(
          (_) async => ['repo', 'read:user', 'write:repo_hook'],
        ); // Extra scope

        await authService.init();

        expect(authService.accessToken, 'token1');
        expect(authService.isLoggedIn, isTrue);
      },
    );

    test('logout when not logged in does not throw', () async {
      expect(authService.isLoggedIn, isFalse);

      await authService.logout();

      expect(authService.accessToken, isNull);
      expect(authService.isLoggedIn, isFalse);
    });

    group('error handling during login flow', () {
      test('login propagates AccessDeniedException', () async {
        when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
          (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
        );
        when(
          fakeAuthClient.createAccessTokenFromDeviceCode(any),
        ).thenThrow(AccessDeniedException());

        expect(
          () => authService.login(),
          throwsA(isA<AccessDeniedException>()),
        );
      });

      test('login propagates GithubNonRecoverableException', () async {
        when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
          (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
        );
        when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenThrow(
          GithubNonRecoverableException('invalid_grant', 'Device code expired'),
        );

        expect(
          () => authService.login(),
          throwsA(isA<GithubNonRecoverableException>()),
        );
      });

      test('loginWithDeviceCode propagates AccessDeniedException', () async {
        when(
          fakeAuthClient.createAccessTokenFromDeviceCode(any),
        ).thenThrow(AccessDeniedException());

        expect(
          () => authService.loginWithDeviceCode('device_code'),
          throwsA(isA<AccessDeniedException>()),
        );
      });

      test(
        'loginWithDeviceCode propagates GithubNonRecoverableException',
        () async {
          when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenThrow(
            GithubNonRecoverableException(
              'expired_token',
              'Device code has expired',
            ),
          );

          expect(
            () => authService.loginWithDeviceCode('device_code'),
            throwsA(isA<GithubNonRecoverableException>()),
          );
        },
      );
    });

    group('token storage error handling', () {
      late MockITokenStorage mockTokenStorage;

      setUp(() {
        mockTokenStorage = MockITokenStorage();
        authService = AuthService(
          fakeAuthClient,
          mockTokenStorage,
          fakeScopeService,
          fakeTimerService,
        );
      });

      test('init handles token storage read errors', () async {
        when(mockTokenStorage.getToken()).thenThrow(Exception('Storage error'));

        await authService.init();

        expect(authService.accessToken, isNull);
        expect(authService.isLoggedIn, isFalse);
      });

      test('init handles token storage delete errors during cleanup', () async {
        when(
          mockTokenStorage.getToken(),
        ).thenAnswer((_) async => 'invalid_token');
        when(
          fakeScopeService.getScopesFromAccessToken(any),
        ).thenThrow(Exception('Invalid token'));
        when(
          mockTokenStorage.deleteToken(),
        ).thenThrow(Exception('Delete failed'));

        // Should not throw, but handle the error gracefully
        await authService.init();

        expect(authService.accessToken, isNull);
        expect(authService.isLoggedIn, isFalse);
        verify(mockTokenStorage.deleteToken()).called(1);
      });

      test('login handles token storage save errors', () async {
        when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
          (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
        );
        when(
          fakeAuthClient.createAccessTokenFromDeviceCode(any),
        ).thenAnswer((_) async => 'new_token');
        when(
          mockTokenStorage.saveToken(any),
        ).thenThrow(Exception('Save failed'));

        expect(() => authService.login(), throwsA(isA<Exception>()));
      });

      test('logout handles token storage delete errors', () async {
        when(
          mockTokenStorage.deleteToken(),
        ).thenThrow(Exception('Delete failed'));

        expect(() => authService.logout(), throwsA(isA<Exception>()));
      });
    });

    test('login uses TimerService for AuthorizationPendingException', () async {
      when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
        (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
      );

      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount == 1) {
          throw AuthorizationPendingException();
        } else {
          return 'success_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.login();

      expect(token, 'success_token');
      verify(fakeTimerService.delay(const Duration(seconds: 5))).called(1);
    });

    test('login uses TimerService for SlowDownException', () async {
      when(fakeAuthClient.createDeviceCode(any)).thenAnswer(
        (_) async => GithubDeviceCodeResult(deviceCode: 'dc', userCode: 'uc'),
      );

      int callCount = 0;
      when(fakeAuthClient.createAccessTokenFromDeviceCode(any)).thenAnswer((
        _,
      ) async {
        callCount++;
        if (callCount == 1) {
          throw SlowDownException();
        } else {
          return 'success_token';
        }
      });
      when(fakeTimerService.delay(any)).thenAnswer((_) async {});

      final token = await authService.login();

      expect(token, 'success_token');
      verify(fakeTimerService.delay(const Duration(seconds: 10))).called(1);
    });
  });
}
