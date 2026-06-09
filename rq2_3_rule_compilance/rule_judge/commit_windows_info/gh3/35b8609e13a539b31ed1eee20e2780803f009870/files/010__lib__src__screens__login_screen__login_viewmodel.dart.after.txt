import 'dart:async';
import '../../services/github_auth_client.dart';
import '../../services/auth_service.dart';
import '../app/auth_viewmodel.dart';
import '../base_viewmodel.dart';

/// ViewModel for handling GitHub device-flow login UI.
class LoginViewModel extends DisposableViewModel {
  final GithubAuthClient _authClient;
  final AuthService _authService;
  final AuthViewModel _authViewModel;

  LoginViewModel(this._authClient, this._authService, this._authViewModel);

  bool _isLoading = false;
  String? _userCode;
  String? _errorMessage;

  /// Whether a login flow is in progress.
  bool get isLoading => _isLoading;

  /// The user code to show for device login.
  String? get userCode => _userCode;

  /// Any error message encountered during login.
  String? get errorMessage => _errorMessage;

  /// Whether the user has successfully authorized.
  bool get isAuthorized => _authService.isLoggedIn;

  /// Starts the device-login flow: creates a device code, then delegates to AuthService.
  Future<void> login() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      // Request a device code and user code for UI display
      final deviceResult = await _authClient.createDeviceCode(
        AuthService.requiredScopes,
      );
      _userCode = deviceResult.userCode;
      _isLoading = false;
      notifyListeners();

      // Delegate the actual login (polling) to AuthService
      await _authService.loginWithDeviceCode(deviceResult.deviceCode);

      // Update global auth state when login succeeds
      _authViewModel.updateAuthState();
      notifyListeners(); // Update UI when AuthService completes
    } catch (e) {
      _isLoading = false;
      if (e is GithubAuthException) {
        _errorMessage = e.message;
      } else {
        _errorMessage = e.toString();
      }
      notifyListeners();
    }
  }

  @override
  void onDispose() {
    // Clear sensitive data
    _userCode = null;
    _errorMessage = null;
    _isLoading = false;
  }
}

// TODO: Add login_viewmodel.graphql and generated files if GraphQL is used for login.
