import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_custom_tabs/flutter_custom_tabs.dart';
import 'package:flutter_octicons/flutter_octicons.dart';
import 'login_viewmodel.dart';

class LoginScreen extends StatefulWidget {
  final LoginViewModel viewModel;

  const LoginScreen({super.key, required this.viewModel});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  late final LoginViewModel _viewModel;

  void _onViewModelChanged() => setState(() {});

  Future<void> login() async {
    await _viewModel.login();
  }

  @override
  void initState() {
    super.initState();
    _viewModel = widget.viewModel;
    _viewModel.addListener(_onViewModelChanged);
  }

  @override
  void dispose() {
    _viewModel.removeListener(_onViewModelChanged);
    _viewModel.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final userCode = _viewModel.userCode;
    final isLoading = _viewModel.isLoading;
    final error = _viewModel.errorMessage;

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (error != null)
              Text(
                error,
                style: TextStyle(color: Theme.of(context).colorScheme.error),
              ),
            userCode != null
                ? buildUserCode(userCode)
                : buildSignInButton(isLoading),
          ],
        ),
      ),
    );
  }

  Widget buildSignInButton(bool isLoading) {
    return ElevatedButton.icon(
      onPressed: isLoading ? null : login,
      icon: isLoading
          ? const SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(),
            )
          : const Icon(OctIcons.mark_github_16),
      label: const Text('Sign in with GitHub'),
    );
  }

  Widget buildUserCode(String userCode) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        Text('Your user code is: $userCode'),
        const Text(
          'Please visit github.com/login/device and enter the user code',
        ),
        ElevatedButton(
          onPressed: () {
            Clipboard.setData(ClipboardData(text: userCode));
            _launchUrl(context, 'https://github.com/login/device');
          },
          child: Text('Copy and Open browser'),
        ),
      ],
    );
  }

  void _launchUrl(BuildContext context, String url) async {
    final theme = Theme.of(context);
    try {
      await launchUrl(
        Uri.parse(url),
        customTabsOptions: CustomTabsOptions(
          colorSchemes: CustomTabsColorSchemes.defaults(
            toolbarColor: theme.colorScheme.surface,
          ),
          shareState: CustomTabsShareState.on,
          urlBarHidingEnabled: true,
          showTitle: true,
          closeButton: CustomTabsCloseButton(
            icon: CustomTabsCloseButtonIcons.back,
          ),
        ),
        safariVCOptions: SafariViewControllerOptions(
          preferredBarTintColor: theme.colorScheme.surface,
          preferredControlTintColor: theme.colorScheme.onSurface,
          barCollapsingEnabled: true,
          dismissButtonStyle: SafariViewControllerDismissButtonStyle.close,
        ),
      );
    } catch (e) {
      // If the URL launch fails, an exception will be thrown. (For example, if no browser app is installed on the Android device.)
      debugPrint(e.toString());
    }
  }
}
