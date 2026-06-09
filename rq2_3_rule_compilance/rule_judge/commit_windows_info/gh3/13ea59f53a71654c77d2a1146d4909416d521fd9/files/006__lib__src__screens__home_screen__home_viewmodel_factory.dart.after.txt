import 'package:injectable/injectable.dart';
import 'home_viewmodel.dart';
import '../../services/auth_service.dart';

@injectable
class HomeViewModelFactory {
  final AuthService _authService;

  HomeViewModelFactory(this._authService);

  HomeViewModel create() {
    return HomeViewModel(_authService);
  }
}
