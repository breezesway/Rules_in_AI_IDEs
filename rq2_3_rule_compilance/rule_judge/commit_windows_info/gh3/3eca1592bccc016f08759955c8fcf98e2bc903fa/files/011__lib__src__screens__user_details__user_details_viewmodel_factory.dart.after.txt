import 'package:injectable/injectable.dart';
import 'user_details_viewmodel.dart';

/// Factory for creating UserDetailsViewModel instances with proper dependency injection.
@injectable
class UserDetailsViewModelFactory {
  UserDetailsViewModelFactory();

  /// Creates a new UserDetailsViewModel instance for the specified user login.
  UserDetailsViewModel create(String login) {
    return UserDetailsViewModel(login);
  }
}
