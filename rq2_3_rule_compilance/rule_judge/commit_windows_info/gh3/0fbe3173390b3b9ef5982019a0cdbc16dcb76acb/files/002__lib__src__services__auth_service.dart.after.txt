import 'package:injectable/injectable.dart';
// Removed direct SharedPreferences usage; using ITokenStorage
import 'github_auth_client.dart';
import 'token_storage.dart';
import 'scope_service.dart';
import 'timer_service.dart';

@lazySingleton
class AuthService {
  final GithubAuthClient _authClient;
  final ITokenStorage _tokenStorage;
  final IScopeService _scopeService;
  final TimerService _timerService;
  // Scopes required for GitHub operations
  static const List<String> requiredScopes = ['repo', 'read:user'];
  String? _accessToken;

  AuthService(
    this._authClient,
    this._tokenStorage,
    this._scopeService,
    this._timerService,
  );

  /// Initialize service: load token from storage and validate.
  Future<void> init() async {
    try {
      // Load existing token
      final token = await _tokenStorage.getToken();
      if (token != null) {
        final valid = await _checkTokenValid(token);
        if (valid) {
          _accessToken = token;
        } else {
          try {
            await _tokenStorage.deleteToken();
          } catch (_) {
            // Ignore delete errors during cleanup
          }
        }
      }
    } catch (_) {
      // If token storage fails, start with no token
      _accessToken = null;
    }
  }

  Future<bool> _checkTokenValid(String token) async {
    // Validate token by fetching associated scopes
    try {
      final scopes = await _scopeService.getScopesFromAccessToken(token);
      return requiredScopes.every((scope) => scopes.contains(scope));
    } catch (_) {
      return false;
    }
  }

  // Scopes are fetched via IScopeService

  /// Current access token.
  String? get accessToken => _accessToken;

  /// Whether user is logged in.
  bool get isLoggedIn => _accessToken != null;

  /// Perform login flow: request device code, poll for token, and store it.
  Future<String> login() async {
    // Initiate device flow with required scopes
    final device = await _authClient.createDeviceCode(requiredScopes);

    while (true) {
      try {
        final token = await _authClient.createAccessTokenFromDeviceCode(
          device.deviceCode,
        );
        _accessToken = token;
        await _tokenStorage.saveToken(token);
        return token;
      } on AuthorizationPendingException {
        await _timerService.delay(const Duration(seconds: 5));
      } on SlowDownException {
        await _timerService.delay(const Duration(seconds: 10));
      }
    }
  }

  /// Perform login flow with an existing device code (for UI separation).
  Future<String> loginWithDeviceCode(String deviceCode) async {
    while (true) {
      try {
        final token = await _authClient.createAccessTokenFromDeviceCode(
          deviceCode,
        );
        _accessToken = token;
        await _tokenStorage.saveToken(token);
        return token;
      } on AuthorizationPendingException {
        await _timerService.delay(const Duration(seconds: 5));
      } on SlowDownException {
        await _timerService.delay(const Duration(seconds: 10));
      }
    }
  }

  /// Logout and clear stored token.
  Future<void> logout() async {
    _accessToken = null;
    await _tokenStorage.deleteToken();
  }
}
