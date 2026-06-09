import '../base_viewmodel.dart';
import '../../services/auth_service.dart';

class HomeViewModel extends DisposableViewModel {
  // Note: _authService will be used in future implementations for real user data
  // ignore: unused_field
  final AuthService _authService;

  HomeViewModel(this._authService);

  // Current user data (placeholder - in real implementation would come from GraphQL)
  String? get currentUserName => 'GitHub User'; // Placeholder
  String? get currentUserLogin => 'githubuser'; // Placeholder
  String? get currentUserAvatar => null; // Placeholder

  @override
  void onDispose() {
    // Clean up resources if needed
  }
}
