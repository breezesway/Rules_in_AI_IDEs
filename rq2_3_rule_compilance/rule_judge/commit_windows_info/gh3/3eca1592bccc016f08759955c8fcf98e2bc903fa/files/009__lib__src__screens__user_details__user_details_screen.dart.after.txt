import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'user_details_viewmodel.dart';

class UserDetailsScreen extends StatefulWidget {
  final UserDetailsViewModel viewModel;

  const UserDetailsScreen({super.key, required this.viewModel});

  @override
  State<UserDetailsScreen> createState() => _UserDetailsScreenState();
}

class _UserDetailsScreenState extends State<UserDetailsScreen> {
  late final UserDetailsViewModel _viewModel;

  void _onViewModelChanged() => setState(() {});

  @override
  void initState() {
    super.initState();
    _viewModel = widget.viewModel;
    _viewModel.addListener(_onViewModelChanged);
    _viewModel.init();
  }

  @override
  void dispose() {
    _viewModel.removeListener(_onViewModelChanged);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leading: BackButton(
          onPressed: () {
            if (Navigator.of(context).canPop()) {
              Navigator.of(context).pop();
            } else {
              context.go('/');
            }
          },
        ),
        title: const Text('User Details'),
      ),
      body: Center(
        child: _viewModel.isLoading
            ? const CircularProgressIndicator()
            : Text(
                'User: ${_viewModel.login}',
                style: Theme.of(context).textTheme.headlineMedium,
              ),
      ),
    );
  }
}
