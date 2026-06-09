import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../widgets/gh_user_card.dart';
import '../widgets/gh_navigation_grid.dart';
import '../widgets/gh_repository_card.dart';
import '../data/fake_data_service.dart';
import '../components/gh_card.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../state_widgets/gh_empty_state.dart';

/// Home screen example showing authenticated GitHub dashboard
class HomeScreenExample extends StatefulWidget {
  const HomeScreenExample({super.key});

  @override
  State<HomeScreenExample> createState() => _HomeScreenExampleState();
}

class _HomeScreenExampleState extends State<HomeScreenExample> {
  final FakeDataService _dataService = FakeDataService();

  @override
  Widget build(BuildContext context) {
    final currentUser = _dataService.getUsers(count: 1).first;
    final trendingRepos = _dataService.getRepositories(count: 5);

    return GHScreenTemplate(
      title: "GitHub",
      showBackButton: false,
      actions: [
        IconButton(
          icon: const Icon(Icons.notifications_outlined),
          onPressed: () {
            // Navigate to notifications - placeholder for now
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Notifications feature coming soon'),
              ),
            );
          },
        ),
        IconButton(
          icon: CircleAvatar(
            radius: 16,
            backgroundImage: NetworkImage(currentUser.avatarUrl),
          ),
          onPressed: () {
            NavigationService.navigateToUser(currentUser.login);
          },
        ),
      ],
      body: GHListTemplate(
        searchHint: "Search repositories, users, issues...",
        onRefresh: _handleRefresh,
        onSearch: _handleSearch,
        children: [
          // User profile summary
          GHUserCard.fromFakeUser(
            currentUser,
            onTap: () {
              NavigationService.navigateToUser(currentUser.login);
            },
          ),

          const SizedBox(height: GHTokens.spacing20),

          // Quick actions grid
          _buildQuickActionsSection(currentUser),

          const SizedBox(height: GHTokens.spacing20),

          // Recent activity feed
          _buildActivitySection(),

          const SizedBox(height: GHTokens.spacing20),

          // Trending repositories
          _buildTrendingSection(trendingRepos),
        ],
      ),
    );
  }

  Widget _buildQuickActionsSection(FakeUser user) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing12),
          child: Text('Quick Actions', style: GHTokens.titleLarge),
        ),
        const SizedBox(height: GHTokens.spacing12),
        GHNavigationGrid(
          items: [
            GHNavigationItem(
              icon: Icons.star_outline,
              title: 'Starred',
              description: 'Your starred repositories',
              badge: '45',
              onTap: () {
                NavigationService.navigateToStarred();
              },
            ),
            GHNavigationItem(
              icon: Icons.folder_outlined,
              title: 'Repositories',
              description: 'Your repositories',
              badge: '${user.repositoryCount}',
              onTap: () {
                NavigationService.navigateToUser(user.login);
              },
            ),
            GHNavigationItem(
              icon: Icons.people_outline,
              title: 'Organizations',
              description: 'Your organizations',
              badge: '${user.organizations.length}',
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Organizations feature coming soon'),
                  ),
                );
              },
            ),
            GHNavigationItem(
              icon: Icons.notifications_outlined,
              title: 'Notifications',
              description: 'Recent notifications',
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Notifications feature coming soon'),
                  ),
                );
              },
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActivitySection() {
    final activities = _dataService.getActivityFeed(count: 5);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing12),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Recent Activity', style: GHTokens.titleLarge),
              TextButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Full activity view coming soon'),
                    ),
                  );
                },
                child: const Text('View all'),
              ),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing12),

        if (activities.isEmpty)
          GHEmptyStates.noActivity(
            onExplore: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Explore GitHub feature coming soon'),
                ),
              );
            },
          )
        else
          ...activities.map(
            (activity) => Padding(
              padding: const EdgeInsets.only(bottom: GHTokens.spacing8),
              child: _buildActivityItem(activity),
            ),
          ),
      ],
    );
  }

  Widget _buildActivityItem(FakeActivity activity) {
    return GHCard.zeroPadding(
      child: ListTile(
        leading: CircleAvatar(
          radius: 16,
          backgroundImage: NetworkImage(activity.actorAvatarUrl),
        ),
        title: Text(
          activity.title,
          style: GHTokens.bodyMedium,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: activity.description != null
            ? Text(
                activity.description!,
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              )
            : null,
        trailing: Text(
          _formatActivityTime(activity.createdAt),
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
        onTap: () {
          if (activity.repositoryOwner != null &&
              activity.repositoryName != null) {
            NavigationService.navigateToRepository(
              activity.repositoryOwner!,
              activity.repositoryName!,
            );
          }
        },
      ),
    );
  }

  String _formatActivityTime(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h';
    } else if (difference.inDays < 7) {
      return '${difference.inDays}d';
    } else {
      return '${(difference.inDays / 7).floor()}w';
    }
  }

  Widget _buildTrendingSection(List<FakeRepository> repos) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing12),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Trending Today', style: GHTokens.titleLarge),
              TextButton(
                onPressed: () {
                  NavigationService.navigateToTrending();
                },
                child: const Text('See all'),
              ),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing12),

        // Add trending period selector
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing12),
          child: Row(
            children: [
              _buildTrendingPeriodChip('Today', true),
              const SizedBox(width: GHTokens.spacing8),
              _buildTrendingPeriodChip('This week', false),
              const SizedBox(width: GHTokens.spacing8),
              _buildTrendingPeriodChip('This month', false),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing12),

        ...repos.map(
          (repo) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing12),
            child: GHRepositoryCard.fromFakeRepository(
              repo,
              showStarButton: true,
              onTap: () {
                NavigationService.navigateToRepository(repo.owner, repo.name);
              },
              onStarTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Starred ${repo.owner}/${repo.name}')),
                );
              },
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildTrendingPeriodChip(String label, bool isSelected) {
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        if (selected) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Showing trending repositories for: $label'),
            ),
          );
        }
      },
      selectedColor: Theme.of(context).colorScheme.primaryContainer,
      checkmarkColor: Theme.of(context).colorScheme.primary,
    );
  }

  Future<void> _handleRefresh() async {
    // Simulate network delay
    await Future.delayed(const Duration(seconds: 1));

    if (mounted) {
      setState(() {
        // Refresh completed
      });
    }
  }

  void _handleSearch(String query) {
    if (query.isNotEmpty) {
      NavigationService.navigateToSearch();
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Searching for: $query')));
    }
  }
}
