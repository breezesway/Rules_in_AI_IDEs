import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';
import 'package:gh3/src/init.dart';
import 'package:gh3/src/screens/app/gh3_app.dart';
import 'package:gh3/src/screens/home_screen/home_viewmodel.dart';
import 'package:gh3/src/screens/app/auth_viewmodel.dart';
import 'package:gh3/src/screens/user_details/user_details_viewmodel_factory.dart';
import 'package:gh3/src/services/auth_service.dart';
import 'package:gh3/src/services/github_auth_client.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  configureDependencies();

  // Get services from dependency injection
  final authService = getIt<AuthService>();
  final githubAuthClient = getIt<GithubAuthClient>();
  final homeViewModel = await GetIt.instance.getAsync<HomeViewModel>();
  final userDetailsViewModelFactory = getIt<UserDetailsViewModelFactory>();

  // Create ViewModels manually with their dependencies
  final authVM = AuthViewModel(authService);
  await authVM.init();

  runApp(
    Gh3App(
      authViewModel: authVM,
      authService: authService,
      githubAuthClient: githubAuthClient,
      homeViewModel: homeViewModel,
      userDetailsViewModelFactory: userDetailsViewModelFactory,
    ),
  );
}
