import 'package:flutter/foundation.dart';

/// ViewModel for handling user details screen logic.
class UserDetailsViewModel extends ChangeNotifier {
  final String _login;

  UserDetailsViewModel(this._login);

  /// The user login being displayed.
  String get login => _login;

  bool _isLoading = false;

  /// Whether data is currently being loaded.
  bool get isLoading => _isLoading;

  /// Initialize the view model and load user data.
  Future<void> init() async {
    _isLoading = true;
    notifyListeners();

    // TODO: Load user details from GraphQL API
    // This is a placeholder implementation
    await Future.delayed(const Duration(milliseconds: 500));

    _isLoading = false;
    notifyListeners();
  }
}
