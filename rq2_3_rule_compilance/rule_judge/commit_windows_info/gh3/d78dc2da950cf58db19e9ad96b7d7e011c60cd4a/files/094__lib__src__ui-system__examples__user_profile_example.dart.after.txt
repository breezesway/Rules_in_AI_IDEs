import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../data/fake_data_service.dart';
import '../components/gh_card.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/number_formatter.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// User profile example screen showing comprehensive user information
/// with action-based navigation replacing tab navigation.
class UserProfileExample extends StatefulWidget {
  /// Username to display profile for
  final String username;

  const UserProfileExample({super.key, required this.username});

  @override
  State<UserProfileExample> createState() => _UserProfileExampleState();
}

class _UserProfileExampleState extends State<UserProfileExample> {
  final FakeDataService _dataService = FakeDataService();
  late FakeUser _user;
  bool _isLoading = true;
  bool _isFollowing = false;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  void _loadUserData() async {
    setState(() {
      _isLoading = true;
    });

    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));

    // Find user by username or use first user as fallback
    final users = _dataService.getUsers();
    _user = users.firstWhere(
      (user) => user.login == widget.username,
      orElse: () => users.first,
    );

    setState(() {
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return GHLoadingTransition(
      isLoading: _isLoading,
      loadingMessage: 'Loading user profile...',
      child: GHScreenTemplate(
        title: _user.name ?? _user.login,
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Share ${_user.login}\'s profile')),
              );
            },
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(SnackBar(content: Text('$value action')));
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'Block user',
                child: Text('Block user'),
              ),
              const PopupMenuItem(
                value: 'Report user',
                child: Text('Report user'),
              ),
            ],
          ),
        ],
        body: CustomScrollView(
          slivers: [
            // Scrolling app bar
            SliverAppBar(
              expandedHeight: 120.0,
              pinned: true,
              automaticallyImplyLeading: true,
              flexibleSpace: FlexibleSpaceBar(
                title: Text(_user.name ?? _user.login),
                titlePadding: const EdgeInsets.only(left: 56, bottom: 16),
                collapseMode: CollapseMode.parallax,
              ),
              backgroundColor: Theme.of(context).colorScheme.surface,
            ),

            // Content
            SliverToBoxAdapter(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: GHTokens.spacing16),

                  // User profile header (without title)
                  _buildUserHeader(),

                  const SizedBox(height: GHTokens.spacing16),

                  // Action buttons
                  _buildActionButtons(),

                  const SizedBox(height: GHTokens.spacing20),

                  // Action list
                  _buildActionsList(),

                  const SizedBox(height: GHTokens.spacing16),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUserHeader() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Large avatar
              CircleAvatar(
                radius: 40,
                backgroundImage: NetworkImage(_user.avatarUrl),
              ),
              const SizedBox(width: GHTokens.spacing16),

              // User info (without name - shown in app bar)
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '@${_user.login}',
                      style: GHTokens.bodyLarge.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),

          // Bio
          if (_user.bio != null) ...[
            const SizedBox(height: GHTokens.spacing12),
            Text(
              _user.bio!,
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurface,
              ),
            ),
          ],

          // Location and company
          if (_user.location != null || _user.company != null) ...[
            const SizedBox(height: GHTokens.spacing8),
            Row(
              children: [
                if (_user.location != null) ...[
                  Icon(
                    Icons.location_on_outlined,
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                  Text(
                    _user.location!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
                if (_user.location != null && _user.company != null)
                  const SizedBox(width: GHTokens.spacing16),
                if (_user.company != null) ...[
                  Icon(
                    Icons.business_outlined,
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                  Text(
                    _user.company!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ],
            ),
          ],

          // Statistics
          const SizedBox(height: GHTokens.spacing16),
          Row(
            children: [
              _buildStatItem('Repositories', _user.repositoryCount),
              const SizedBox(width: GHTokens.spacing24),
              _buildStatItem('Followers', _user.followerCount),
              const SizedBox(width: GHTokens.spacing24),
              _buildStatItem('Following', _user.followingCount),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, int count) {
    return GestureDetector(
      onTap: () {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('View $label')));
      },
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            NumberFormatter.formatCompact(count),
            style: GHTokens.titleMedium.copyWith(
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.onSurface,
            ),
          ),
          Text(
            label,
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButtons() {
    return Row(
      children: [
        Expanded(
          child: ElevatedButton.icon(
            onPressed: () {
              setState(() {
                _isFollowing = !_isFollowing;
              });
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(
                    _isFollowing
                        ? 'Following ${_user.login}'
                        : 'Unfollowed ${_user.login}',
                  ),
                ),
              );
            },
            icon: Icon(_isFollowing ? Icons.person_remove : Icons.person_add),
            label: Text(_isFollowing ? 'Unfollow' : 'Follow'),
            style: ElevatedButton.styleFrom(
              backgroundColor: _isFollowing
                  ? Theme.of(context).colorScheme.surfaceContainerHighest
                  : Theme.of(context).colorScheme.primary,
              foregroundColor: _isFollowing
                  ? Theme.of(context).colorScheme.onSurface
                  : Theme.of(context).colorScheme.onPrimary,
            ),
          ),
        ),
        const SizedBox(width: GHTokens.spacing8),
        OutlinedButton.icon(
          onPressed: () {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(SnackBar(content: Text('Message ${_user.login}')));
          },
          icon: const Icon(Icons.message_outlined),
          label: const Text('Message'),
        ),
      ],
    );
  }

  Widget _buildActionsList() {
    return Column(
      children: [
        GHCard(
          padding: EdgeInsets.zero,
          onTap: () {
            NavigationService.navigateToUserRepositories(widget.username);
          },
          child: ListTile(
            leading: const Icon(Icons.folder_outlined),
            title: const Text('Repositories'),
            subtitle: Text('${_user.repositoryCount} public repositories'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing8,
                    vertical: GHTokens.spacing4,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(
                      context,
                    ).colorScheme.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(GHTokens.radius12),
                  ),
                  child: Text(
                    '${_user.repositoryCount}',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                const Icon(Icons.chevron_right),
              ],
            ),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),

        GHCard(
          padding: EdgeInsets.zero,
          onTap: () {
            NavigationService.navigateToUserStarred(widget.username);
          },
          child: ListTile(
            leading: const Icon(Icons.star_outlined),
            title: const Text('Starred'),
            subtitle: const Text('Starred repositories'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing8,
                    vertical: GHTokens.spacing4,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(
                      context,
                    ).colorScheme.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(GHTokens.radius12),
                  ),
                  child: Text(
                    '${_user.starredCount ?? 0}',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                const Icon(Icons.chevron_right),
              ],
            ),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),

        GHCard(
          padding: EdgeInsets.zero,
          onTap: () {
            NavigationService.navigateToUserOrganizations(widget.username);
          },
          child: ListTile(
            leading: const Icon(Icons.people_outline),
            title: const Text('Organizations'),
            subtitle: const Text('Organizations you belong to'),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing8,
                    vertical: GHTokens.spacing4,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(
                      context,
                    ).colorScheme.surfaceContainerHighest,
                    borderRadius: BorderRadius.circular(GHTokens.radius12),
                  ),
                  child: Text(
                    '${_user.organizations.length}',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                const Icon(Icons.chevron_right),
              ],
            ),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),

        GHCard(
          padding: EdgeInsets.zero,
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Projects feature coming soon')),
            );
          },
          child: const ListTile(
            leading: Icon(Icons.dashboard_outlined),
            title: Text('Projects'),
            subtitle: Text('Organize your work with projects'),
            trailing: Icon(Icons.chevron_right),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),

        GHCard(
          padding: EdgeInsets.zero,
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Packages feature coming soon')),
            );
          },
          child: const ListTile(
            leading: Icon(Icons.inventory_2_outlined),
            title: Text('Packages'),
            subtitle: Text('Software packages you publish'),
            trailing: Icon(Icons.chevron_right),
          ),
        ),
      ],
    );
  }
}
