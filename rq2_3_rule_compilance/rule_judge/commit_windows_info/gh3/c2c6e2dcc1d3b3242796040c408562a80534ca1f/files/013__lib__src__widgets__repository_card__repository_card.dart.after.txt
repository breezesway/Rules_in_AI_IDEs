import 'package:flutter/material.dart';
import '__generated__/repository_card.data.gql.dart';

class RepositoryCard extends StatelessWidget {
  final GRepositoryCardFragment repository;
  final VoidCallback? onTap;

  const RepositoryCard({super.key, required this.repository, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListTile(
        title: Text(
          repository.name,
          style: const TextStyle(fontWeight: FontWeight.bold),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (repository.description != null &&
                repository.description!.isNotEmpty) ...[
              Text(
                repository.description!,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[600]),
              ),
              const SizedBox(height: 8),
            ],
            Row(
              children: [
                if (repository.primaryLanguage != null) ...[
                  Container(
                    width: 12,
                    height: 12,
                    decoration: BoxDecoration(
                      color: _parseColor(repository.primaryLanguage!.color),
                      shape: BoxShape.circle,
                    ),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    repository.primaryLanguage!.name,
                    style: TextStyle(color: Colors.grey[600], fontSize: 12),
                  ),
                  const SizedBox(width: 16),
                ],
                Icon(Icons.star, size: 16, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(
                  '${repository.stargazerCount}',
                  style: TextStyle(color: Colors.grey[600], fontSize: 12),
                ),
                const SizedBox(width: 16),
                Icon(Icons.call_split, size: 16, color: Colors.grey[600]),
                const SizedBox(width: 4),
                Text(
                  '${repository.forkCount}',
                  style: TextStyle(color: Colors.grey[600], fontSize: 12),
                ),
              ],
            ),
          ],
        ),
        onTap: onTap,
      ),
    );
  }

  Color _parseColor(String? colorHex) {
    if (colorHex == null || colorHex.isEmpty) {
      return Colors.grey;
    }

    try {
      // Remove # if present and parse as hex
      final hex = colorHex.replaceFirst('#', '');
      return Color(int.parse('FF$hex', radix: 16));
    } catch (e) {
      return Colors.grey;
    }
  }
}
