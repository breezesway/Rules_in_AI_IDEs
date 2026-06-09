import 'package:injectable/injectable.dart';
import 'package:get_it/get_it.dart';
import './init.config.dart';

final getIt = GetIt.instance;
@InjectableInit(
  // initializerName: 'init', // default
  // preferRelativeImports: true, // default
  // asExtension: true, // default
)
void configureDependencies() {
  // Enable multiple registrations for the same interface type
  getIt.enableRegisteringMultipleInstancesOfOneType();
  
  // Initialize generated dependency graph (includes AuthViewModel)
  getIt.init();
}
