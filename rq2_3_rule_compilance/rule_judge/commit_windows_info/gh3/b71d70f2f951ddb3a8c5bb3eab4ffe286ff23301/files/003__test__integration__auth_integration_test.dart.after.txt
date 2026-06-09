import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/services/github_auth_client.dart';
import 'package:gh3/src/services/token_storage.dart';
import 'package:gh3/src/services/scope_service.dart';
import 'package:gh3/src/services/timer_service.dart';

@GenerateMocks([http.Client])
import 'auth_integration_test.mocks.dart';

void main() {
  group('Authentication Integration Tests', () {
    late AuthService authService;
    late MockClient mockHttpClient;
    late GithubAuthClient authClient;
    late ITokenStorage tokenStorage;
    late IScopeService scopeService;
    late TimerService timerService;

    setUp(() async {
      SharedPreferences.setMockInitialValues({});

      mockHttpClient = MockClient();
      authClient = GithubAuthClient(mockHttpClient, 'test_client_id');
      tokenStorage = PrefsTokenStorage();
      scopeService = ScopeService(mockHttpClient);
      timerService = DefaultTimerService();

      authService = AuthService(
        authClient,
        tokenStorage,
        scopeService,
        timerService,
      );
    });

    group('OAuth Device Flow Integration', () {
      test(
        'complete device flow authentication stores token and validates scopes',
        () async {
          // Mock device code request
          when(
            mockHttpClient.post(
              Uri.https('github.com', '/login/device/code', {
                'client_id': 'test_client_id',
                'scope': 'repo read:user',
              }),
              headers: anyNamed('headers'),
              body: anyNamed('body'),
            ),
          ).thenAnswer(
            (_) async => http.Response(
              '{"device_code": "test_device_code", "user_code": "TEST123"}',
              200,
            ),
          );

          // Mock token polling - first pending, then success
          when(
            mockHttpClient.post(
              Uri.https('github.com', '/login/oauth/access_token', {
                'client_id': 'test_client_id',
                'device_code': 'test_device_code',
                'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
              }),
              headers: anyNamed('headers'),
              body: anyNamed('body'),
            ),
          ).thenAnswer(
            (_) async => http.Response(
              '{"access_token": "integration_test_token"}',
              200,
            ),
          );

          // Mock scope validation
          when(
            mockHttpClient.get(
              Uri.parse('https://api.github.com/applications/token/scopes'),
              headers: {
                'Authorization': 'token integration_test_token',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'gh3-flutter-app',
              },
            ),
          ).thenAnswer(
            (_) async => http.Response(
              '{}',
              200,
              headers: {'x-oauth-scopes': 'repo, read:user'},
            ),
          );

          // Perform login
          final token = await authService.login();

          // Verify token received and stored
          expect(token, 'integration_test_token');
          expect(authService.accessToken, 'integration_test_token');
          expect(authService.isLoggedIn, isTrue);

          // Verify token persisted
          final prefs = await SharedPreferences.getInstance();
          expect(
            prefs.getString('github_access_token'),
            'integration_test_token',
          );

          // Verify service can be reinitialized with stored token
          final newAuthService = AuthService(
            authClient,
            tokenStorage,
            scopeService,
            timerService,
          );

          await newAuthService.init();
          expect(newAuthService.accessToken, 'integration_test_token');
          expect(newAuthService.isLoggedIn, isTrue);
        },
      );

      test('device flow with authorization pending then success', () async {
        // Mock device code request
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/device/code', {
              'client_id': 'test_client_id',
              'scope': 'repo read:user',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{"device_code": "pending_device_code", "user_code": "PEND123"}',
            200,
          ),
        );

        // Mock token polling - authorization pending, then success
        int pollCount = 0;
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/oauth/access_token', {
              'client_id': 'test_client_id',
              'device_code': 'pending_device_code',
              'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer((_) async {
          pollCount++;
          if (pollCount == 1) {
            return http.Response('{"error": "authorization_pending"}', 200);
          } else {
            return http.Response('{"access_token": "delayed_token"}', 200);
          }
        });

        // Mock scope validation
        when(
          mockHttpClient.get(
            Uri.parse('https://api.github.com/applications/token/scopes'),
            headers: {
              'Authorization': 'token delayed_token',
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'gh3-flutter-app',
            },
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{}',
            200,
            headers: {'x-oauth-scopes': 'repo, read:user'},
          ),
        );

        final stopwatch = Stopwatch()..start();
        final token = await authService.login();
        stopwatch.stop();

        expect(token, 'delayed_token');
        expect(authService.isLoggedIn, isTrue);
        // Verify there was a delay (should be at least 5 seconds due to authorization pending)
        expect(stopwatch.elapsedMilliseconds, greaterThan(4000));
      });

      test('device flow with slow down then success', () async {
        // Mock device code request
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/device/code', {
              'client_id': 'test_client_id',
              'scope': 'repo read:user',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{"device_code": "slow_device_code", "user_code": "SLOW123"}',
            200,
          ),
        );

        // Mock token polling - slow down, then success
        int pollCount = 0;
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/oauth/access_token', {
              'client_id': 'test_client_id',
              'device_code': 'slow_device_code',
              'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer((_) async {
          pollCount++;
          if (pollCount == 1) {
            return http.Response('{"error": "slow_down"}', 200);
          } else {
            return http.Response('{"access_token": "slow_token"}', 200);
          }
        });

        // Mock scope validation
        when(
          mockHttpClient.get(
            Uri.parse('https://api.github.com/applications/token/scopes'),
            headers: {
              'Authorization': 'token slow_token',
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'gh3-flutter-app',
            },
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{}',
            200,
            headers: {'x-oauth-scopes': 'repo, read:user'},
          ),
        );

        final stopwatch = Stopwatch()..start();
        final token = await authService.login();
        stopwatch.stop();

        expect(token, 'slow_token');
        expect(authService.isLoggedIn, isTrue);
        // Verify there was a longer delay (should be at least 10 seconds due to slow down)
        expect(stopwatch.elapsedMilliseconds, greaterThan(9000));
      });
    });

    group('Token Persistence Integration', () {
      test('valid token is restored on service restart', () async {
        // Set up a valid token in SharedPreferences
        SharedPreferences.setMockInitialValues({
          'github_access_token': 'persisted_token',
        });

        // Mock scope validation for the persisted token
        when(
          mockHttpClient.get(
            Uri.parse('https://api.github.com/applications/token/scopes'),
            headers: {
              'Authorization': 'token persisted_token',
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'gh3-flutter-app',
            },
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{}',
            200,
            headers: {'x-oauth-scopes': 'repo, read:user'},
          ),
        );

        // Initialize service
        await authService.init();

        // Verify token is restored
        expect(authService.accessToken, 'persisted_token');
        expect(authService.isLoggedIn, isTrue);
      });

      test('invalid token is cleared on service restart', () async {
        // Set up an invalid token in SharedPreferences
        SharedPreferences.setMockInitialValues({
          'github_access_token': 'invalid_token',
        });

        // Mock scope validation failure for the invalid token
        when(
          mockHttpClient.get(
            Uri.parse('https://api.github.com/applications/token/scopes'),
            headers: {
              'Authorization': 'token invalid_token',
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'gh3-flutter-app',
            },
          ),
        ).thenAnswer(
          (_) async => http.Response('{"message": "Bad credentials"}', 401),
        );

        // Initialize service
        await authService.init();

        // Verify invalid token is cleared
        expect(authService.accessToken, isNull);
        expect(authService.isLoggedIn, isFalse);

        // Verify token is removed from storage
        final prefs = await SharedPreferences.getInstance();
        expect(prefs.getString('github_access_token'), isNull);
      });

      test(
        'token with insufficient scopes is cleared on service restart',
        () async {
          // Set up a token with insufficient scopes in SharedPreferences
          SharedPreferences.setMockInitialValues({
            'github_access_token': 'insufficient_token',
          });

          // Mock scope validation with insufficient scopes
          when(
            mockHttpClient.get(
              Uri.parse('https://api.github.com/applications/token/scopes'),
              headers: {
                'Authorization': 'token insufficient_token',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'gh3-flutter-app',
              },
            ),
          ).thenAnswer(
            (_) async => http.Response(
              '{}',
              200,
              headers: {'x-oauth-scopes': 'read:user'}, // Missing 'repo' scope
            ),
          );

          // Initialize service
          await authService.init();

          // Verify insufficient token is cleared
          expect(authService.accessToken, isNull);
          expect(authService.isLoggedIn, isFalse);

          // Verify token is removed from storage
          final prefs = await SharedPreferences.getInstance();
          expect(prefs.getString('github_access_token'), isNull);
        },
      );
    });

    group('Authentication State Changes Integration', () {
      test('logout clears token and prevents access', () async {
        // Set up authenticated state
        SharedPreferences.setMockInitialValues({
          'github_access_token': 'logout_token',
        });

        // Mock scope validation
        when(
          mockHttpClient.get(
            Uri.parse('https://api.github.com/applications/token/scopes'),
            headers: {
              'Authorization': 'token logout_token',
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'gh3-flutter-app',
            },
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{}',
            200,
            headers: {'x-oauth-scopes': 'repo, read:user'},
          ),
        );

        // Initialize and verify authenticated
        await authService.init();
        expect(authService.isLoggedIn, isTrue);

        // Perform logout
        await authService.logout();

        // Verify state is cleared
        expect(authService.accessToken, isNull);
        expect(authService.isLoggedIn, isFalse);

        // Verify token is removed from storage
        final prefs = await SharedPreferences.getInstance();
        expect(prefs.getString('github_access_token'), isNull);

        // Verify new service instance shows logged out state
        final newAuthService = AuthService(
          authClient,
          tokenStorage,
          scopeService,
          timerService,
        );
        await newAuthService.init();
        expect(newAuthService.isLoggedIn, isFalse);
      });
    });

    group('Error Recovery Integration', () {
      test(
        'service recovers from network errors during initialization',
        () async {
          // Set up a token that causes network error during validation
          SharedPreferences.setMockInitialValues({
            'github_access_token': 'network_error_token',
          });

          // Mock network error during scope validation
          when(
            mockHttpClient.get(
              Uri.parse('https://api.github.com/applications/token/scopes'),
              headers: {
                'Authorization': 'token network_error_token',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'gh3-flutter-app',
              },
            ),
          ).thenThrow(Exception('Network unreachable'));

          // Initialize service - should handle error gracefully
          await authService.init();

          // Verify service handles error gracefully
          expect(authService.accessToken, isNull);
          expect(authService.isLoggedIn, isFalse);

          // Verify token is cleaned up from storage
          final prefs = await SharedPreferences.getInstance();
          expect(prefs.getString('github_access_token'), isNull);
        },
      );

      test('service continues to function after login failure', () async {
        // Mock device code request success
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/device/code', {
              'client_id': 'test_client_id',
              'scope': 'repo read:user',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer(
          (_) async => http.Response(
            '{"device_code": "fail_device_code", "user_code": "FAIL123"}',
            200,
          ),
        );

        // Mock token polling failure
        when(
          mockHttpClient.post(
            Uri.https('github.com', '/login/oauth/access_token', {
              'client_id': 'test_client_id',
              'device_code': 'fail_device_code',
              'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            }),
            headers: anyNamed('headers'),
            body: anyNamed('body'),
          ),
        ).thenAnswer(
          (_) async => http.Response('{"error": "access_denied"}', 200),
        );

        // Attempt login - should fail
        expect(
          () => authService.login(),
          throwsA(isA<AccessDeniedException>()),
        );

        // Verify service state remains clean
        expect(authService.accessToken, isNull);
        expect(authService.isLoggedIn, isFalse);

        // Verify no token is stored
        final prefs = await SharedPreferences.getInstance();
        expect(prefs.getString('github_access_token'), isNull);
      });
    });
  });
}
