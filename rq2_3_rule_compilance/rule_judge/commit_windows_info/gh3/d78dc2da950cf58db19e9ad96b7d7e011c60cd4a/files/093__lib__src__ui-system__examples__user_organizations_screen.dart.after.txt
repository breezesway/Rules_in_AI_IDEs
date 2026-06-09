import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../data/fake_data_service.dart';
import '../components/gh_card.dart';
import '../tokens/gh_tokens.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// User organizations screen showing organizations the user belongs to
class UserOrganizationsScreen extends StatefulWidget {
  final String username;

  const UserOrganizationsScreen({super.key, required this.username});

  @override
  State<UserOrganizationsScreen> createState() =>
      _UserOrganizationsScreenState();
}

class _UserOrganizationsScreenState extends State<UserOrganizationsScreen> {
  final FakeDataService _dataService = FakeDataService();
  late FakeUser _user;

  List<FakeOrganization> _organizations = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUserOrganizations();
  }

  void _loadUserOrganizations() async {
    setState(() {
      _isLoading = true;
    });

    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));

    // Find user
    final users = _dataService.getUsers();
    _user = users.firstWhere(
      (user) => user.login == widget.username,
      orElse: () => users.first,
    );

    // Get user's organizations
    _organizations = _user.organizations;

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: GHLoadingIndicator.large(
          label: 'Loading organizations...',
          centered: true,
        ),
      );
    }

    return GHScreenTemplate(
      title: '${_user.name ?? _user.login} / Organizations',
      body: _organizations.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.people_outline,
                    size: 64,
                    color: Colors.grey,
                  ),
                  const SizedBox(height: GHTokens.spacing16),
                  Text(
                    '${_user.login} isn\'t a member of any organizations',
                    style: GHTokens.headlineMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: GHTokens.spacing8),
                  Text(
                    'Organizations help manage repositories and teams',
                    style: GHTokens.bodyLarge.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            )
          : ListView.separated(
              padding: const EdgeInsets.symmetric(vertical: GHTokens.spacing16),
              itemCount: _organizations.length,
              separatorBuilder: (context, index) =>
                  const SizedBox(height: GHTokens.spacing12),
              itemBuilder: (context, index) =>
                  _buildOrganizationCard(_organizations[index]),
            ),
    );
  }

  Widget _buildOrganizationCard(FakeOrganization organization) {
    return GHCard(
      onTap: () {
        // Navigate to organization profile (placeholder for now)
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('View ${organization.name} organization')),
        );
      },
      child: Row(
        children: [
          // Organization avatar
          CircleAvatar(
            radius: 24,
            backgroundImage: NetworkImage(organization.avatarUrl),
            backgroundColor: Theme.of(
              context,
            ).colorScheme.surfaceContainerHighest,
          ),
          const SizedBox(width: GHTokens.spacing16),

          // Organization info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  organization.name,
                  style: GHTokens.titleMedium.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: GHTokens.spacing4),

                Text(
                  '@${organization.login}',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),

                if (organization.description != null) ...[
                  const SizedBox(height: GHTokens.spacing8),
                  Text(
                    organization.description!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],

                const SizedBox(height: GHTokens.spacing8),

                // Organization stats
                Row(
                  children: [
                    Icon(
                      Icons.folder_outlined,
                      size: 16,
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(
                      '${organization.publicRepos} repositories',
                      style: GHTokens.bodySmall.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),

                    const SizedBox(width: GHTokens.spacing16),

                    Icon(
                      Icons.people_outlined,
                      size: 16,
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(
                      '${organization.publicMembers} members',
                      style: GHTokens.bodySmall.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Chevron
          Icon(
            Icons.chevron_right,
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ],
      ),
    );
  }
}
