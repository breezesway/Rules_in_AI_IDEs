import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class UserDetailsScreen extends StatelessWidget {
  final String login;
  const UserDetailsScreen({Key? key, required this.login}) : super(key: key);

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
        child: Text(
          'User: $login',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
    );
  }
} 