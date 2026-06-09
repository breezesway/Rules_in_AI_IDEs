import 'package:injectable/injectable.dart';
import 'package:gh3/src/services/auth_service.dart';
import '../base_viewmodel.dart';

/// ViewModel exposing AuthService init and login state for GoRouter refresh/redirect.
@lazySingleton
class AuthViewModel extends DisposableViewModel {
  final AuthService _authService;
  bool loading = true;
  bool loggedIn = false;

  AuthViewModel(this._authService);

  Future<void> init() async {
    await _authService.init();
    loggedIn = _authService.isLoggedIn;
    loading = false;
    notifyListeners();
  }

  Future<void> logout() async {
    await _authService.logout();
    loggedIn = false;
    notifyListeners();
  }

  /// Update the logged in state (called by other components when auth state changes)
  void updateAuthState() {
    loggedIn = _authService.isLoggedIn;
    notifyListeners();
  }

  @override
  void onDispose() {
    loading = true;
    loggedIn = false;
  }
}
