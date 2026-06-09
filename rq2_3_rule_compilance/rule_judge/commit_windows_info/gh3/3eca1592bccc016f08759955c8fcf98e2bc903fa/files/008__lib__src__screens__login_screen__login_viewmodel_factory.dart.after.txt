import 'package:injectable/injectable.dart';
import '../../services/github_auth_client.dart';
import '../../services/auth_service.dart';
import '../app/auth_viewmodel.dart';
import 'login_viewmodel.dart';

/// Factory for creating LoginViewModel instances with proper dependency injection.
@injectable
class LoginViewModelFactory {
  final GithubAuthClient _authClient;
  final AuthService _authService;
  final AuthViewModel _authViewModel;

  LoginViewModelFactory(
    this._authClient,
    this._authService,
    this._authViewModel,
  );

  /// Creates a new LoginViewModel instance with injected dependencies.
  LoginViewModel create() {
    return LoginViewModel(_authClient, _authService, _authViewModel);
  }
}
