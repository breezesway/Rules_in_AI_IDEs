import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../widgets/gh_repository_card.dart';
import '../widgets/gh_issue_card.dart';
import '../widgets/gh_user_card.dart';
import '../widgets/gh_file_tree_item.dart';
import '../widgets/gh_entity_header.dart';
import '../widgets/gh_navigation_grid.dart';
import '../widgets/gh_filter_bar.dart';
import '../widgets/gh_status_badge.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';

/// GitHub widgets showcase screen demonstrating all GitHub-specific widgets.
///
/// This screen displays realistic examples of repositories, issues, users,
/// and other GitHub content widgets with proper styling and interactions.
class GitHubWidgetsScreen extends StatefulWidget {
  const GitHubWidgetsScreen({super.key});

  @override
  State<GitHubWidgetsScreen> createState() => _GitHubWidgetsScreenState();
}

class _GitHubWidgetsScreenState extends State<GitHubWidgetsScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final FakeDataService _dataService = FakeDataService();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'GitHub Widgets',
      showBackButton: false,
      bottom: TabBar(
        controller: _tabController,
        tabs: const [
          Tab(text: 'Repositories'),
          Tab(text: 'Issues'),
          Tab(text: 'Users'),
          Tab(text: 'Files'),
          Tab(text: 'Headers'),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildRepositoriesTab(),
          _buildIssuesTab(),
          _buildUsersTab(),
          _buildFilesTab(),
          _buildHeadersTab(),
        ],
      ),
    );
  }

  Widget _buildRepositoriesTab() {
    final repositories = _dataService.getRepositories(count: 20);

    return GHListTemplate(
      searchHint: 'Search repositories...',
      filters: [
        GHFilterBar(
          filters: GHFilterItems.repositoryType(
            allCount: repositories.length,
            sourcesCount: repositories
                .where((r) => !r.name.contains('fork'))
                .length,
            forksCount: repositories
                .where((r) => r.name.contains('fork'))
                .length,
            archivedCount: 2,
          ),
          onFilterChanged: (filter) {
            _showSnackBar('Filter changed: ${filter.label}');
          },
          onClearAll: () {
            _showSnackBar('Cleared all filters');
          },
        ),
      ],
      onSearch: (query) {
        // TODO: Implement search functionality
      },
      onRefresh: () async {
        // TODO: Implement refresh functionality
        await Future.delayed(const Duration(seconds: 1));
      },
      children: repositories.map((repo) {
        return GHRepositoryCard(
          owner: repo.owner,
          name: repo.name,
          description: repo.description,
          language: repo.language,
          starCount: repo.starCount,
          forkCount: repo.forkCount,
          lastUpdated: repo.lastUpdated,
          isPrivate: repo.isPrivate,
          showStarButton: true,
          onTap: () {
            _showSnackBar('Tapped ${repo.owner}/${repo.name}');
          },
          onStarTap: () {
            _showSnackBar('Starred ${repo.owner}/${repo.name}');
          },
        );
      }).toList(),
    );
  }

  Widget _buildIssuesTab() {
    final issues = _dataService.getIssues(count: 30);
    final openIssues = issues
        .where((i) => i.status == GHStatusType.open)
        .length;
    final closedIssues = issues
        .where((i) => i.status == GHStatusType.closed)
        .length;

    return GHListTemplate(
      searchHint: 'Search issues...',
      filters: [
        GHFilterBar(
          filters: GHFilterItems.issueStatus(
            openCount: openIssues,
            closedCount: closedIssues,
          ),
          onFilterChanged: (filter) {
            _showSnackBar('Filter changed: ${filter.label}');
          },
          onClearAll: () {
            _showSnackBar('Cleared all filters');
          },
        ),
      ],
      onSearch: (query) {
        // TODO: Implement search functionality
      },
      onRefresh: () async {
        // TODO: Implement refresh functionality
        await Future.delayed(const Duration(seconds: 1));
      },
      children: issues.map((issue) {
        return GHIssueCard(
          number: issue.number,
          title: issue.title,
          status: issue.status,
          labels: issue.labels,
          authorLogin: issue.authorLogin,
          authorAvatarUrl: issue.authorAvatarUrl,
          createdAt: issue.createdAt,
          commentCount: issue.commentCount,
          assigneeLogin: issue.assigneeLogin,
          assigneeAvatarUrl: issue.assigneeAvatarUrl,
          onTap: () {
            _showSnackBar('Tapped issue #${issue.number}');
          },
        );
      }).toList(),
    );
  }

  Widget _buildUsersTab() {
    final users = _dataService.getUsers(count: 20);

    return GHListTemplate(
      searchHint: 'Search users...',
      onSearch: (query) {
        // TODO: Implement search functionality
      },
      onRefresh: () async {
        // TODO: Implement refresh functionality
        await Future.delayed(const Duration(seconds: 1));
      },
      children: users.map((user) {
        return GHUserCard(
          login: user.login,
          name: user.name,
          bio: user.bio,
          avatarUrl: user.avatarUrl,
          repositoryCount: user.repositoryCount,
          followerCount: user.followerCount,
          followingCount: user.followingCount,
          showFollowButton: true,
          onTap: () {
            _showSnackBar('Tapped user ${user.login}');
          },
          onFollowTap: () {
            _showSnackBar('Followed ${user.login}');
          },
        );
      }).toList(),
    );
  }

  Widget _buildFilesTab() {
    final files = _dataService.getFiles(count: 20);

    return GHListTemplate(
      searchHint: 'Search files...',
      onSearch: (query) {
        // TODO: Implement search functionality
      },
      onRefresh: () async {
        // TODO: Implement refresh functionality
        await Future.delayed(const Duration(seconds: 1));
      },
      children: files.map((file) {
        return GHFileTreeItem(
          name: file.name,
          type: file.type,
          lastCommitMessage: file.lastCommitMessage,
          lastModified: file.lastModified,
          author: file.author,
          size: file.size,
          onTap: () {
            _showSnackBar('Tapped ${file.name}');
          },
        );
      }).toList(),
    );
  }

  Widget _buildHeadersTab() {
    final repositories = _dataService.getRepositories(count: 3);
    final users = _dataService.getUsers(count: 2);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Repository headers
          Text('Repository Headers', style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing16),

          ...repositories.map((repo) {
            return Column(
              children: [
                GHEntityHeader(
                  title: '${repo.owner}/${repo.name}',
                  subtitle: repo.description,
                  avatar: CircleAvatar(
                    radius: 20,
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    child: Icon(
                      Icons.folder,
                      color: Theme.of(context).colorScheme.onPrimary,
                    ),
                  ),
                  stats: GHEntityStats.repository(
                    stars: repo.starCount,
                    forks: repo.forkCount,
                    watchers: repo.starCount ~/ 10,
                    language: repo.language,
                  ),
                  isPrivate: repo.isPrivate,
                  actions: [
                    OutlinedButton.icon(
                      onPressed: () => _showSnackBar('Starred ${repo.name}'),
                      icon: const Icon(Icons.star_border),
                      label: const Text('Star'),
                    ),
                    OutlinedButton.icon(
                      onPressed: () => _showSnackBar('Watched ${repo.name}'),
                      icon: const Icon(Icons.visibility),
                      label: const Text('Watch'),
                    ),
                    OutlinedButton.icon(
                      onPressed: () => _showSnackBar('Forked ${repo.name}'),
                      icon: const Icon(Icons.fork_right),
                      label: const Text('Fork'),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing16),

                // Navigation grid for repository
                GHNavigationGrid.twoByTwo(
                  items: GHNavigationItems.repository(
                    issues: 23,
                    pullRequests: 5,
                    actions: 12,
                    onCodeTap: () => _showSnackBar('Navigate to Code'),
                    onIssuesTap: () => _showSnackBar('Navigate to Issues'),
                    onPullRequestsTap: () => _showSnackBar('Navigate to PRs'),
                    onActionsTap: () => _showSnackBar('Navigate to Actions'),
                  ),
                ),
                const SizedBox(height: GHTokens.spacing24),
              ],
            );
          }),

          // User headers
          Text('User Headers', style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing16),

          ...users.map((user) {
            return Column(
              children: [
                GHEntityHeader(
                  title: user.name ?? user.login,
                  subtitle: user.bio,
                  avatar: CircleAvatar(
                    radius: 20,
                    backgroundColor: Theme.of(context).colorScheme.secondary,
                    child: Icon(
                      Icons.person,
                      color: Theme.of(context).colorScheme.onSecondary,
                    ),
                  ),
                  stats: GHEntityStats.user(
                    repositories: user.repositoryCount,
                    followers: user.followerCount,
                    following: user.followingCount,
                  ),
                  actions: [
                    ElevatedButton.icon(
                      onPressed: () => _showSnackBar('Followed ${user.login}'),
                      icon: const Icon(Icons.person_add),
                      label: const Text('Follow'),
                    ),
                    OutlinedButton.icon(
                      onPressed: () => _showSnackBar('Message ${user.login}'),
                      icon: const Icon(Icons.message),
                      label: const Text('Message'),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing16),

                // Navigation grid for user
                GHNavigationGrid.twoByTwo(
                  items: GHNavigationItems.userDashboard(
                    repositories: user.repositoryCount,
                    starred: user.repositoryCount ~/ 2,
                    organizations: 3,
                    onRepositoriesTap: () =>
                        _showSnackBar('Navigate to Repositories'),
                    onStarredTap: () => _showSnackBar('Navigate to Starred'),
                    onOrganizationsTap: () =>
                        _showSnackBar('Navigate to Organizations'),
                    onSettingsTap: () => _showSnackBar('Navigate to Settings'),
                  ),
                ),
                const SizedBox(height: GHTokens.spacing24),
              ],
            );
          }),
        ],
      ),
    );
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), duration: const Duration(seconds: 2)),
    );
  }
}

/// A simple demo app to showcase the GitHub widgets
class GitHubWidgetsApp extends StatelessWidget {
  const GitHubWidgetsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GitHub Widgets Demo',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: GHTokens.primary,
          brightness: Brightness.light,
        ),
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: GHTokens.primary,
          brightness: Brightness.dark,
        ),
      ),
      home: const GitHubWidgetsScreen(),
    );
  }
}
