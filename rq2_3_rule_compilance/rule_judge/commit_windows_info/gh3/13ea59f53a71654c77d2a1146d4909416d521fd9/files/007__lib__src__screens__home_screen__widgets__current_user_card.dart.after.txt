import 'package:flutter/material.dart';

class CurrentUserCard extends StatelessWidget {
  final String? name;
  final String? login;
  final String? avatarUrl;

  const CurrentUserCard({super.key, this.name, this.login, this.avatarUrl});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundImage: avatarUrl != null ? NetworkImage(avatarUrl!) : null,
          child: avatarUrl == null ? const Icon(Icons.person) : null,
        ),
        title: Text(name ?? 'User'),
        subtitle: Text('@${login ?? 'username'}'),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: null, // Placeholder - no navigation initially
      ),
    );
  }
}
