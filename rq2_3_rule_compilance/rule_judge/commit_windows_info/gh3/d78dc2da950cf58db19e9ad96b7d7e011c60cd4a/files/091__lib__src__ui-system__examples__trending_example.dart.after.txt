import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../components/gh_card.dart';
import '../components/gh_chip.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Trending and discovery example screen
class TrendingExample extends StatefulWidget {
  const TrendingExample({super.key});

  @override
  State<TrendingExample> createState() => _TrendingExampleState();
}

class _TrendingExampleState extends State<TrendingExample>
    with TickerProviderStateMixin {
  final FakeDataService _dataService = FakeDataService();
  late final TabController _tabController;

  List<FakeRepository> _trendingRepos = [];
  List<FakeUser> _trendingDevelopers = [];
  List<String> _trendingTopics = [];
  List<String> _featuredTopics = [];

  bool _isLoading = true;
  String _timePeriod = 'today'; // today, week, month
  String _language = 'all'; // all, dart, javascript, python, etc.

  final List<String> _timePeriods = ['today', 'week', 'month'];
  final List<String> _languages = [
    'all',
    'dart',
    'javascript',
    'typescript',
    'python',
    'java',
    'swift',
    'kotlin',
    'rust',
    'go',
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadTrendingData();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadTrendingData() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 600));

      final allRepos = _dataService.getRepositories(count: 50);
      final allUsers = _dataService.getUsers(count: 30);

      // Filter and sort repositories by "trending" criteria
      _trendingRepos = _filterAndSortRepos(allRepos);

      // Get trending developers (high activity users)
      _trendingDevelopers = _getTrendingDevelopers(allUsers);

      // Generate trending topics
      _trendingTopics = _generateTrendingTopics();

      // Generate featured topics with descriptions
      _featuredTopics = _generateFeaturedTopics();

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  List<FakeRepository> _filterAndSortRepos(List<FakeRepository> repos) {
    var filtered = repos.where((repo) {
      if (_language != 'all') {
        return repo.language.toLowerCase() == _language.toLowerCase();
      }
      return true;
    }).toList();

    // Sort by a combination of stars and recency for "trending"
    filtered.sort((a, b) {
      final aScore = _calculateTrendingScore(a);
      final bScore = _calculateTrendingScore(b);
      return bScore.compareTo(aScore);
    });

    return filtered.take(25).toList();
  }

  double _calculateTrendingScore(FakeRepository repo) {
    final daysSinceUpdate = DateTime.now().difference(repo.lastUpdated).inDays;
    final recencyBonus = (30 - daysSinceUpdate).clamp(0, 30) / 30.0;

    switch (_timePeriod) {
      case 'today':
        return repo.starCount * (recencyBonus * 2) + repo.forkCount * 0.5;
      case 'week':
        return repo.starCount * (recencyBonus * 1.5) + repo.forkCount * 0.3;
      case 'month':
        return repo.starCount * recencyBonus + repo.forkCount * 0.2;
      default:
        return repo.starCount.toDouble();
    }
  }

  List<FakeUser> _getTrendingDevelopers(List<FakeUser> users) {
    // Sort users by a combination of followers and activity
    users.sort((a, b) {
      final aScore =
          a.login.length * 100 +
          (a.bio?.length ?? 0) * 5; // Mock activity score
      final bScore = b.login.length * 100 + (b.bio?.length ?? 0) * 5;
      return bScore.compareTo(aScore);
    });

    return users.take(15).toList();
  }

  List<String> _generateTrendingTopics() {
    return [
      'machine-learning',
      'web-development',
      'mobile-app',
      'cloud-computing',
      'blockchain',
      'data-science',
      'cybersecurity',
      'devops',
      'artificial-intelligence',
      'open-source',
      'microservices',
      'serverless',
    ];
  }

  List<String> _generateFeaturedTopics() {
    return [
      'awesome',
      'framework',
      'library',
      'tutorial',
      'boilerplate',
      'api',
      'backend',
      'frontend',
      'fullstack',
      'database',
      'testing',
      'deployment',
    ];
  }

  void _onTimePeriodChanged(String period) {
    setState(() {
      _timePeriod = period;
    });
    _loadTrendingData();
  }

  void _onLanguageChanged(String language) {
    setState(() {
      _language = language;
    });
    _loadTrendingData();
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Trending',
      actions: [
        PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'refresh':
                _loadTrendingData();
                break;
              case 'customize':
                _showCustomizeDialog();
                break;
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'refresh', child: Text('Refresh')),
            const PopupMenuItem(value: 'customize', child: Text('Customize')),
          ],
        ),
      ],
      body: _isLoading
          ? const GHLoadingIndicator.large(
              label: 'Loading trending repositories...',
              centered: true,
            )
          : Column(
              children: [
                // Filters section
                _buildFiltersSection(),

                // Tabs section
                Expanded(
                  child: Column(
                    children: [
                      TabBar(
                        controller: _tabController,
                        tabs: const [
                          Tab(
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.trending_up, size: 16),
                                SizedBox(width: 4),
                                Text('Repositories'),
                              ],
                            ),
                          ),
                          Tab(
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.person_outline, size: 16),
                                SizedBox(width: 4),
                                Text('Developers'),
                              ],
                            ),
                          ),
                          Tab(
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.tag, size: 16),
                                SizedBox(width: 4),
                                Text('Topics'),
                              ],
                            ),
                          ),
                        ],
                      ),
                      Expanded(
                        child: TabBarView(
                          controller: _tabController,
                          children: [
                            _buildRepositoriesTab(),
                            _buildDevelopersTab(),
                            _buildTopicsTab(),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
    );
  }

  Widget _buildFiltersSection() {
    return Container(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border(
          bottom: BorderSide(
            color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Time period filter
          Row(
            children: [
              Text(
                'Time:',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(width: GHTokens.spacing8),
              Expanded(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _timePeriods.map((period) {
                      return Padding(
                        padding: const EdgeInsets.only(
                          right: GHTokens.spacing8,
                        ),
                        child: GHChip(
                          label: _getTimePeriodLabel(period),
                          isSelected: _timePeriod == period,
                          onTap: () => _onTimePeriodChanged(period),
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: GHTokens.spacing12),

          // Language filter
          Row(
            children: [
              Text(
                'Language:',
                style: GHTokens.labelMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(width: GHTokens.spacing8),
              Expanded(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _languages.map((language) {
                      return Padding(
                        padding: const EdgeInsets.only(
                          right: GHTokens.spacing8,
                        ),
                        child: GHChip(
                          label: _getLanguageLabel(language),
                          isSelected: _language == language,
                          onTap: () => _onLanguageChanged(language),
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildRepositoriesTab() {
    if (_trendingRepos.isEmpty) {
      return const Center(child: Text('No trending repositories found'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _trendingRepos.length,
      itemBuilder: (context, index) {
        final repo = _trendingRepos[index];
        return _buildTrendingRepositoryCard(repo, index + 1);
      },
    );
  }

  Widget _buildDevelopersTab() {
    if (_trendingDevelopers.isEmpty) {
      return const Center(child: Text('No trending developers found'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _trendingDevelopers.length,
      itemBuilder: (context, index) {
        final developer = _trendingDevelopers[index];
        return _buildTrendingDeveloperCard(developer, index + 1);
      },
    );
  }

  Widget _buildTopicsTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Trending topics
          Text(
            'Trending topics',
            style: GHTokens.titleMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: GHTokens.spacing12),
          Wrap(
            spacing: GHTokens.spacing8,
            runSpacing: GHTokens.spacing8,
            children: _trendingTopics.map((topic) {
              return _buildTopicCard(topic, true);
            }).toList(),
          ),

          const SizedBox(height: GHTokens.spacing24),

          // Featured topics
          Text(
            'Featured topics',
            style: GHTokens.titleMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: GHTokens.spacing12),
          ...(_featuredTopics.map((topic) => _buildFeaturedTopicCard(topic))),
        ],
      ),
    );
  }

  Widget _buildTrendingRepositoryCard(FakeRepository repo, int rank) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          NavigationService.navigateToRepository(repo.owner, repo.name);
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Ranking
              Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  color: _getRankColor(rank),
                  borderRadius: BorderRadius.circular(GHTokens.radius16),
                ),
                child: Center(
                  child: Text(
                    rank.toString(),
                    style: GHTokens.labelMedium.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),

              const SizedBox(width: GHTokens.spacing12),

              // Repository details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          repo.isPrivate ? Icons.lock : Icons.folder_outlined,
                          size: 16,
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        const SizedBox(width: GHTokens.spacing8),
                        Expanded(
                          child: Text(
                            '${repo.owner}/${repo.name}',
                            style: GHTokens.titleMedium.copyWith(
                              color: Theme.of(context).colorScheme.primary,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: GHTokens.spacing8),

                    Text(
                      repo.description,
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),

                    const SizedBox(height: GHTokens.spacing8),

                    Row(
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: _getLanguageColor(repo.language),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: GHTokens.spacing8),
                        Text(
                          repo.language,
                          style: GHTokens.bodyMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                          ),
                        ),

                        const SizedBox(width: GHTokens.spacing16),

                        Icon(
                          Icons.star_border,
                          size: 16,
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        const SizedBox(width: GHTokens.spacing4),
                        Text(
                          _formatStarCount(repo.starCount),
                          style: GHTokens.bodyMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                          ),
                        ),

                        const SizedBox(width: GHTokens.spacing16),

                        Icon(
                          Icons.trending_up,
                          size: 16,
                          color: GHTokens.success,
                        ),
                        const SizedBox(width: GHTokens.spacing4),
                        Text(
                          '+${(rank * 123) % 1000}',
                          style: GHTokens.bodyMedium.copyWith(
                            color: GHTokens.success,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTrendingDeveloperCard(FakeUser developer, int rank) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          NavigationService.navigateToUser(developer.login);
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Row(
            children: [
              // Ranking
              Container(
                width: 32,
                height: 32,
                decoration: BoxDecoration(
                  color: _getRankColor(rank),
                  borderRadius: BorderRadius.circular(GHTokens.radius16),
                ),
                child: Center(
                  child: Text(
                    rank.toString(),
                    style: GHTokens.labelMedium.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ),

              const SizedBox(width: GHTokens.spacing12),

              // Avatar
              CircleAvatar(
                radius: 24,
                backgroundImage: NetworkImage(developer.avatarUrl),
              ),

              const SizedBox(width: GHTokens.spacing12),

              // Developer details
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      developer.login,
                      style: GHTokens.titleMedium.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),

                    if (developer.name != null) ...[
                      const SizedBox(height: GHTokens.spacing4),
                      Text(
                        developer.name!,
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],

                    if (developer.bio != null) ...[
                      const SizedBox(height: GHTokens.spacing4),
                      Text(
                        developer.bio!,
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ],
                ),
              ),

              // Stats
              Column(
                children: [
                  Text(
                    '${developer.login.length * 42}',
                    style: GHTokens.labelMedium.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  Text(
                    'followers',
                    style: GHTokens.labelSmall.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTopicCard(String topic, bool isTrending) {
    return GestureDetector(
      onTap: () {
        NavigationService.navigateToSearch(query: topic);
      },
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing12,
          vertical: GHTokens.spacing8,
        ),
        decoration: BoxDecoration(
          color: Theme.of(
            context,
          ).colorScheme.primaryContainer.withValues(alpha: 0.3),
          borderRadius: BorderRadius.circular(GHTokens.radius16),
          border: Border.all(
            color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.3),
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (isTrending) ...[
              Icon(Icons.trending_up, size: 14, color: GHTokens.success),
              const SizedBox(width: GHTokens.spacing4),
            ],
            Text(
              topic,
              style: GHTokens.labelMedium.copyWith(
                color: Theme.of(context).colorScheme.primary,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFeaturedTopicCard(String topic) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing8),
      child: InkWell(
        onTap: () {
          NavigationService.navigateToSearch(query: topic);
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Row(
            children: [
              Container(
                padding: const EdgeInsets.all(GHTokens.spacing8),
                decoration: BoxDecoration(
                  color: Theme.of(
                    context,
                  ).colorScheme.primaryContainer.withValues(alpha: 0.3),
                  borderRadius: BorderRadius.circular(GHTokens.radius8),
                ),
                child: Icon(
                  Icons.tag,
                  size: 20,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),

              const SizedBox(width: GHTokens.spacing12),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      topic,
                      style: GHTokens.titleMedium.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: GHTokens.spacing4),
                    Text(
                      _getTopicDescription(topic),
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),

              Icon(
                Icons.arrow_forward_ios,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _showCustomizeDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Customize Trending'),
        content: const Text(
          'Feature coming soon! You\'ll be able to customize which languages and topics you want to see trending.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  String _getTimePeriodLabel(String period) {
    switch (period) {
      case 'today':
        return 'Today';
      case 'week':
        return 'This Week';
      case 'month':
        return 'This Month';
      default:
        return period;
    }
  }

  String _getLanguageLabel(String language) {
    return language == 'all' ? 'All Languages' : language.toUpperCase();
  }

  Color _getRankColor(int rank) {
    if (rank <= 3) return const Color(0xFFFFD700); // Gold
    if (rank <= 10) return Theme.of(context).colorScheme.primary;
    return Theme.of(context).colorScheme.secondary;
  }

  Color _getLanguageColor(String language) {
    switch (language.toLowerCase()) {
      case 'dart':
        return const Color(0xFF0175C2);
      case 'javascript':
        return const Color(0xFFF1E05A);
      case 'typescript':
        return const Color(0xFF3178C6);
      case 'python':
        return const Color(0xFF3572A5);
      case 'java':
        return const Color(0xFFB07219);
      case 'swift':
        return const Color(0xFFFA7343);
      case 'kotlin':
        return const Color(0xFFA97BFF);
      case 'rust':
        return const Color(0xFFDEA584);
      case 'go':
        return const Color(0xFF00ADD8);
      case 'c++':
        return const Color(0xFFF34B7D);
      default:
        return Colors.grey;
    }
  }

  String _formatStarCount(int count) {
    if (count >= 1000000) return '${(count / 1000000).toStringAsFixed(1)}M';
    if (count >= 1000) return '${(count / 1000).toStringAsFixed(1)}k';
    return count.toString();
  }

  String _getTopicDescription(String topic) {
    switch (topic) {
      case 'awesome':
        return 'Curated lists of awesome resources and tools';
      case 'framework':
        return 'Application frameworks and development tools';
      case 'library':
        return 'Reusable code libraries and packages';
      case 'tutorial':
        return 'Learning resources and step-by-step guides';
      case 'boilerplate':
        return 'Template projects and starter code';
      case 'api':
        return 'APIs, REST services, and integrations';
      case 'backend':
        return 'Server-side development and architecture';
      case 'frontend':
        return 'User interface and client-side development';
      case 'fullstack':
        return 'Complete application development';
      case 'database':
        return 'Data storage and management solutions';
      case 'testing':
        return 'Testing frameworks and quality assurance';
      case 'deployment':
        return 'DevOps, CI/CD, and deployment tools';
      default:
        return 'Explore repositories tagged with $topic';
    }
  }
}
