import 'package:ferry/ferry.dart';
import 'package:injectable/injectable.dart';
import 'home_viewmodel.dart';

@injectable
class HomeViewModelFactory {
  final Client _ferryClient;

  HomeViewModelFactory(this._ferryClient);

  HomeViewModel create() {
    return HomeViewModel(_ferryClient);
  }
}
