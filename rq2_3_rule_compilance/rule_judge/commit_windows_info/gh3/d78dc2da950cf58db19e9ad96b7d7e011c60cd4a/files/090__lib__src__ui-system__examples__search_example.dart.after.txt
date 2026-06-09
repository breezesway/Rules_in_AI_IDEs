import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../components/gh_card.dart';
import '../components/gh_chip.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../utils/debounced_search.dart';
import '../state_widgets/gh_empty_state.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Global search example screen with categorized results
class SearchExample extends StatefulWidget {
  /// Initial search query (optional)
  final String? initialQuery;

  const SearchExample({super.key, this.initialQuery});

  @override
  State<SearchExample> createState() => _SearchExampleState();
}

class _SearchExampleState extends State<SearchExample>
    with TickerProviderStateMixin {
  final FakeDataService _dataService = FakeDataService();
  late final DebouncedSearch _search;
  late final TabController _tabController;
  final TextEditingController _searchController = TextEditingController();
  final FocusNode _searchFocusNode = FocusNode();

  List<FakeRepository> _repositoryResults = [];
  List<FakeUser> _userResults = [];
  List<FakeIssue> _issueResults = [];
  List<FakeFile> _codeResults = [];

  bool _isSearching = false;
  String _currentQuery = '';
  int _currentTabIndex = 0;
  bool _showAdvancedFilters = false;

  // Advanced search filters
  String _languageFilter = 'all';
  String _starsFilter = 'all'; // all, 0, 10, 100, 1000
  String _forksFilter = 'all'; // all, 0, 10, 100
  String _createdFilter = 'all'; // all, today, week, month, year
  String _sortBy = 'relevance'; // relevance, stars, forks, updated

  // Search history and saved searches
  List<String> _searchHistory = [];
  List<Map<String, dynamic>> _savedSearches = [];
  bool _showSearchHistory = false;

  // Search suggestions (will be replaced by actual history)
  List<String> _recentSearches = [
    'flutter',
    'react native',
    'vue.js',
    'typescript',
    'dart',
  ];

  final List<String> _popularSearches = [
    'awesome',
    'machine learning',
    'web framework',
    'mobile app',
    'API',
    'microservices',
  ];

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
    'c++',
  ];

  final List<Map<String, String>> _starsOptions = [
    {'label': 'Any', 'value': 'all'},
    {'label': '1+', 'value': '1'},
    {'label': '10+', 'value': '10'},
    {'label': '100+', 'value': '100'},
    {'label': '1000+', 'value': '1000'},
  ];

  final List<Map<String, String>> _forksOptions = [
    {'label': 'Any', 'value': 'all'},
    {'label': '1+', 'value': '1'},
    {'label': '10+', 'value': '10'},
    {'label': '100+', 'value': '100'},
  ];

  final List<Map<String, String>> _createdOptions = [
    {'label': 'Any time', 'value': 'all'},
    {'label': 'Today', 'value': 'today'},
    {'label': 'This week', 'value': 'week'},
    {'label': 'This month', 'value': 'month'},
    {'label': 'This year', 'value': 'year'},
  ];

  final List<Map<String, String>> _sortOptions = [
    {'label': 'Best match', 'value': 'relevance'},
    {'label': 'Most stars', 'value': 'stars'},
    {'label': 'Most forks', 'value': 'forks'},
    {'label': 'Recently updated', 'value': 'updated'},
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _search = DebouncedSearch(onSearch: _performSearch);

    _loadSearchHistory();
    _loadSavedSearches();

    if (widget.initialQuery != null) {
      _searchController.text = widget.initialQuery!;
      _performSearch(widget.initialQuery!);
    }

    _tabController.addListener(() {
      setState(() {
        _currentTabIndex = _tabController.index;
      });
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _search.dispose();
    _searchController.dispose();
    _searchFocusNode.dispose();
    super.dispose();
  }

  Future<void> _performSearch(String query) async {
    if (query.trim().isEmpty) {
      setState(() {
        _currentQuery = '';
        _repositoryResults = [];
        _userResults = [];
        _issueResults = [];
        _codeResults = [];
        _isSearching = false;
      });
      return;
    }

    // Add to search history
    _addToSearchHistory(query.trim());

    setState(() {
      _isSearching = true;
      _currentQuery = query;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 400));

      final repositories = _dataService.getRepositories(count: 50);
      final users = _dataService.getUsers(count: 30);
      final issues = _dataService.getIssues(count: 40);
      final files = _dataService.getFiles(count: 20);

      final queryLower = query.toLowerCase();

      setState(() {
        // Search repositories with advanced filters
        var filteredRepos = repositories.where(
          (repo) =>
              repo.name.toLowerCase().contains(queryLower) ||
              repo.description.toLowerCase().contains(queryLower) ||
              repo.language.toLowerCase().contains(queryLower) ||
              repo.owner.toLowerCase().contains(queryLower),
        );

        // Apply advanced filters
        filteredRepos = _applyAdvancedFilters(filteredRepos);

        _repositoryResults = filteredRepos.take(20).toList();

        // Search users
        _userResults = users
            .where(
              (user) =>
                  user.login.toLowerCase().contains(queryLower) ||
                  (user.name?.toLowerCase().contains(queryLower) ?? false) ||
                  (user.bio?.toLowerCase().contains(queryLower) ?? false),
            )
            .take(15)
            .toList();

        // Search issues
        _issueResults = issues
            .where(
              (issue) =>
                  issue.title.toLowerCase().contains(queryLower) ||
                  issue.body.toLowerCase().contains(queryLower) ||
                  issue.labels.any(
                    (label) => label.toLowerCase().contains(queryLower),
                  ),
            )
            .take(25)
            .toList();

        // Search code files
        _codeResults = files
            .where(
              (file) =>
                  file.name.toLowerCase().contains(queryLower) ||
                  file.lastCommitMessage.toLowerCase().contains(queryLower) ||
                  (file.content?.toLowerCase().contains(queryLower) ?? false),
            )
            .take(15)
            .toList();

        _isSearching = false;
      });
    } catch (e) {
      setState(() {
        _isSearching = false;
      });
    }
  }

  Iterable<FakeRepository> _applyAdvancedFilters(
    Iterable<FakeRepository> repos,
  ) {
    var filtered = repos;

    // Language filter
    if (_languageFilter != 'all') {
      filtered = filtered.where(
        (repo) => repo.language.toLowerCase() == _languageFilter.toLowerCase(),
      );
    }

    // Stars filter
    if (_starsFilter != 'all') {
      final minStars = int.parse(_starsFilter);
      filtered = filtered.where((repo) => repo.starCount >= minStars);
    }

    // Forks filter
    if (_forksFilter != 'all') {
      final minForks = int.parse(_forksFilter);
      filtered = filtered.where((repo) => repo.forkCount >= minForks);
    }

    // Created date filter
    if (_createdFilter != 'all') {
      final now = DateTime.now();
      DateTime cutoffDate;

      switch (_createdFilter) {
        case 'today':
          cutoffDate = DateTime(now.year, now.month, now.day);
          break;
        case 'week':
          cutoffDate = now.subtract(const Duration(days: 7));
          break;
        case 'month':
          cutoffDate = DateTime(now.year, now.month - 1, now.day);
          break;
        case 'year':
          cutoffDate = DateTime(now.year - 1, now.month, now.day);
          break;
        default:
          cutoffDate = DateTime(1970); // Very old date
      }

      filtered = filtered.where((repo) => repo.lastUpdated.isAfter(cutoffDate));
    }

    // Apply sorting
    final sortedList = filtered.toList();
    switch (_sortBy) {
      case 'stars':
        sortedList.sort((a, b) => b.starCount.compareTo(a.starCount));
        break;
      case 'forks':
        sortedList.sort((a, b) => b.forkCount.compareTo(a.forkCount));
        break;
      case 'updated':
        sortedList.sort((a, b) => b.lastUpdated.compareTo(a.lastUpdated));
        break;
      case 'relevance':
      default:
        // Keep original order for relevance
        break;
    }

    return sortedList;
  }

  void _onSuggestionTap(String suggestion) {
    _searchController.text = suggestion;
    _search.search(suggestion);
    _searchFocusNode.unfocus();
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Search',
      actions: [
        if (_currentQuery.isNotEmpty)
          IconButton(
            icon: const Icon(Icons.bookmark_add_outlined),
            onPressed: _saveCurrentSearch,
            tooltip: 'Save search',
          ),
      ],
      body: Column(
        children: [
          // Search input section
          Container(
            padding: const EdgeInsets.all(GHTokens.spacing16),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              border: Border(
                bottom: BorderSide(
                  color: Theme.of(
                    context,
                  ).colorScheme.outline.withValues(alpha: 0.2),
                ),
              ),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Search bar
                TextField(
                  controller: _searchController,
                  focusNode: _searchFocusNode,
                  decoration: InputDecoration(
                    hintText: 'Search repositories, users, issues, code...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        if (_searchController.text.isNotEmpty)
                          IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              _performSearch('');
                            },
                          ),
                        IconButton(
                          icon: Icon(
                            _showSearchHistory
                                ? Icons.history_toggle_off
                                : Icons.history,
                          ),
                          onPressed: () {
                            setState(() {
                              _showSearchHistory = !_showSearchHistory;
                            });
                          },
                          tooltip: 'Search history',
                        ),
                      ],
                    ),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(GHTokens.radius8),
                    ),
                  ),
                  onChanged: (value) {
                    setState(() {});
                    _search.search(value);
                  },
                  onSubmitted: _performSearch,
                ),

                // Advanced filters toggle
                Row(
                  children: [
                    TextButton.icon(
                      onPressed: () {
                        setState(() {
                          _showAdvancedFilters = !_showAdvancedFilters;
                        });
                      },
                      icon: Icon(
                        _showAdvancedFilters
                            ? Icons.expand_less
                            : Icons.expand_more,
                      ),
                      label: Text(
                        _showAdvancedFilters ? 'Hide filters' : 'Show filters',
                      ),
                    ),
                    const Spacer(),
                    if (_hasActiveFilters())
                      TextButton(
                        onPressed: _clearAllFilters,
                        child: const Text('Clear all'),
                      ),
                  ],
                ),

                // Advanced filters
                if (_showAdvancedFilters) ...[
                  const SizedBox(height: GHTokens.spacing12),
                  _buildAdvancedFilters(),
                ],

                // Search history overlay
                if (_showSearchHistory && _currentQuery.isEmpty) ...[
                  const SizedBox(height: GHTokens.spacing16),
                  _buildSearchHistoryOverlay(),
                ],

                // Search suggestions (when not searching and no results)
                if (_currentQuery.isEmpty &&
                    !_isSearching &&
                    !_showSearchHistory) ...[
                  const SizedBox(height: GHTokens.spacing16),
                  _buildSearchSuggestions(),
                ],
              ],
            ),
          ),

          // Results section
          if (_currentQuery.isNotEmpty || _isSearching)
            Expanded(
              child: GHLoadingTransition(
                isLoading: _isSearching,
                loadingMessage: 'Searching...',
                useScaleTransition: true,
                child: _buildSearchResults(),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildSearchSuggestions() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Recent searches
        if (_recentSearches.isNotEmpty) ...[
          Text(
            'Recent searches',
            style: GHTokens.labelMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: GHTokens.spacing8),
          Wrap(
            spacing: GHTokens.spacing8,
            runSpacing: GHTokens.spacing8,
            children: _recentSearches.map((search) {
              return GHChip(
                label: search,
                onTap: () => _onSuggestionTap(search),
              );
            }).toList(),
          ),
          const SizedBox(height: GHTokens.spacing16),
        ],

        // Popular searches
        Text(
          'Popular searches',
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          children: _popularSearches.map((search) {
            return GHChip(label: search, onTap: () => _onSuggestionTap(search));
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildSearchResults() {
    final totalResults =
        _repositoryResults.length +
        _userResults.length +
        _issueResults.length +
        _codeResults.length;

    if (totalResults == 0) {
      return _buildEmptyState();
    }

    return Column(
      children: [
        // Results summary and tabs
        Container(
          padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: GHTokens.spacing12),
              Text(
                '$totalResults results for "$_currentQuery"',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              const SizedBox(height: GHTokens.spacing12),
            ],
          ),
        ),

        // Category tabs
        TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: [
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.folder_outlined, size: 16),
                  const SizedBox(width: GHTokens.spacing4),
                  Text('Repositories'),
                  if (_repositoryResults.isNotEmpty) ...[
                    const SizedBox(width: GHTokens.spacing4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Text(
                        _repositoryResults.length.toString(),
                        style: GHTokens.labelSmall.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onPrimaryContainer,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.person_outline, size: 16),
                  const SizedBox(width: GHTokens.spacing4),
                  Text('Users'),
                  if (_userResults.isNotEmpty) ...[
                    const SizedBox(width: GHTokens.spacing4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Text(
                        _userResults.length.toString(),
                        style: GHTokens.labelSmall.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onPrimaryContainer,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.bug_report_outlined, size: 16),
                  const SizedBox(width: GHTokens.spacing4),
                  Text('Issues'),
                  if (_issueResults.isNotEmpty) ...[
                    const SizedBox(width: GHTokens.spacing4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Text(
                        _issueResults.length.toString(),
                        style: GHTokens.labelSmall.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onPrimaryContainer,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
            Tab(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.code, size: 16),
                  const SizedBox(width: GHTokens.spacing4),
                  Text('Code'),
                  if (_codeResults.isNotEmpty) ...[
                    const SizedBox(width: GHTokens.spacing4),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Text(
                        _codeResults.length.toString(),
                        style: GHTokens.labelSmall.copyWith(
                          color: Theme.of(
                            context,
                          ).colorScheme.onPrimaryContainer,
                        ),
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),

        // Tab content
        Expanded(
          child: TabBarView(
            controller: _tabController,
            children: [
              _buildRepositoryResults(),
              _buildUserResults(),
              _buildIssueResults(),
              _buildCodeResults(),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.search_off,
              size: 64,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              'No results found for "$_currentQuery"',
              style: GHTokens.titleMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: GHTokens.spacing12),
            Text(
              _getEmptyStateMessage(),
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: GHTokens.spacing24),

            // Suggestions
            _buildEmptyStateSuggestions(),

            const SizedBox(height: GHTokens.spacing24),

            // Action buttons
            Wrap(
              spacing: GHTokens.spacing12,
              runSpacing: GHTokens.spacing12,
              alignment: WrapAlignment.center,
              children: [
                ElevatedButton.icon(
                  onPressed: () {
                    NavigationService.navigateToTrending();
                  },
                  icon: const Icon(Icons.trending_up),
                  label: const Text('Browse Trending'),
                ),
                OutlinedButton.icon(
                  onPressed: _clearAllFilters,
                  icon: const Icon(Icons.clear_all),
                  label: const Text('Clear Filters'),
                ),
                if (_hasActiveFilters())
                  TextButton.icon(
                    onPressed: () {
                      setState(() {
                        _showAdvancedFilters = true;
                      });
                    },
                    icon: const Icon(Icons.tune),
                    label: const Text('Adjust Filters'),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  String _getEmptyStateMessage() {
    if (_hasActiveFilters()) {
      return 'Try adjusting your filters or search terms. You can also browse trending repositories to discover new projects.';
    }

    return 'We couldn\'t find any repositories, users, issues, or code matching your search. Try different keywords or browse trending content.';
  }

  Widget _buildEmptyStateSuggestions() {
    final suggestions = _getSearchSuggestions();

    if (suggestions.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      children: [
        Text(
          'Try searching for:',
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: GHTokens.spacing12),
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          alignment: WrapAlignment.center,
          children: suggestions.map((suggestion) {
            return GHChip(
              label: suggestion,
              onTap: () => _onSuggestionTap(suggestion),
            );
          }).toList(),
        ),
      ],
    );
  }

  List<String> _getSearchSuggestions() {
    // Return contextual suggestions based on current tab
    switch (_currentTabIndex) {
      case 0: // Repositories
        return [
          'awesome',
          'framework',
          'library',
          'boilerplate',
          'tutorial',
          'machine learning',
        ];
      case 1: // Users
        return [
          'developer',
          'maintainer',
          'contributor',
          'google',
          'microsoft',
          'facebook',
        ];
      case 2: // Issues
        return [
          'bug',
          'enhancement',
          'help wanted',
          'good first issue',
          'documentation',
        ];
      case 3: // Code
        return [
          'function',
          'class',
          'interface',
          'component',
          'util',
          'helper',
        ];
      default:
        return _popularSearches;
    }
  }

  Widget _buildRepositoryResults() {
    if (_repositoryResults.isEmpty) {
      return GHEmptyStates.noSearchResults(
        query: _currentQuery,
        onClearSearch: () {
          _searchController.clear();
          _performSearch('');
        },
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _repositoryResults.length,
      itemBuilder: (context, index) {
        final repo = _repositoryResults[index];
        return _buildRepositoryCard(repo);
      },
    );
  }

  Widget _buildUserResults() {
    if (_userResults.isEmpty) {
      return GHEmptyStates.noSearchResults(
        query: _currentQuery,
        onClearSearch: () {
          _searchController.clear();
          _performSearch('');
        },
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _userResults.length,
      itemBuilder: (context, index) {
        final user = _userResults[index];
        return _buildUserCard(user);
      },
    );
  }

  Widget _buildIssueResults() {
    if (_issueResults.isEmpty) {
      return GHEmptyStates.noSearchResults(
        query: _currentQuery,
        onClearSearch: () {
          _searchController.clear();
          _performSearch('');
        },
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _issueResults.length,
      itemBuilder: (context, index) {
        final issue = _issueResults[index];
        return _buildIssueCard(issue);
      },
    );
  }

  Widget _buildCodeResults() {
    if (_codeResults.isEmpty) {
      return GHEmptyStates.noSearchResults(
        query: _currentQuery,
        onClearSearch: () {
          _searchController.clear();
          _performSearch('');
        },
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      itemCount: _codeResults.length,
      itemBuilder: (context, index) {
        final file = _codeResults[index];
        return _buildCodeCard(file);
      },
    );
  }

  Widget _buildRepositoryCard(FakeRepository repo) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          NavigationService.navigateToRepository(repo.owner, repo.name);
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
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
                  Row(
                    children: [
                      Icon(
                        Icons.star_border,
                        size: 16,
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                      const SizedBox(width: GHTokens.spacing4),
                      Text(
                        repo.starCount.toString(),
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
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
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const Spacer(),
                  Text(
                    'Updated ${DateFormatter.formatRelative(repo.lastUpdated)}',
                    style: GHTokens.bodyMedium.copyWith(
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

  Widget _buildUserCard(FakeUser user) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          NavigationService.navigateToUser(user.login);
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Row(
            children: [
              CircleAvatar(
                radius: 24,
                backgroundImage: NetworkImage(user.avatarUrl),
              ),
              const SizedBox(width: GHTokens.spacing12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      user.login,
                      style: GHTokens.titleMedium.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    if (user.name != null) ...[
                      const SizedBox(height: GHTokens.spacing4),
                      Text(
                        user.name!,
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                    if (user.bio != null) ...[
                      const SizedBox(height: GHTokens.spacing4),
                      Text(
                        user.bio!,
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
              Column(
                children: [
                  Text(
                    '${user.login.length * 42}', // Simple algorithm for fake followers
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

  Widget _buildIssueCard(FakeIssue issue) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          // TODO: Navigate to issue - need repository context
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Navigate to issue #${issue.number}')),
          );
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    issue.isPullRequest
                        ? Icons.merge_type
                        : Icons.bug_report_outlined,
                    size: 16,
                    color: _getStatusColor(issue.status),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      issue.title,
                      style: GHTokens.titleMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurface,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing8),
              Row(
                children: [
                  Text(
                    '#${issue.number}',
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  Text(
                    ' opened ${DateFormatter.formatRelative(issue.createdAt)} by ${issue.authorLogin}',
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
              if (issue.labels.isNotEmpty) ...[
                const SizedBox(height: GHTokens.spacing8),
                Wrap(
                  spacing: GHTokens.spacing8,
                  children: issue.labels.take(3).map((label) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        color: _getLabelColor(label),
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Text(
                        label,
                        style: GHTokens.labelSmall.copyWith(
                          color: _getLabelTextColor(label),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildCodeCard(FakeFile file) {
    return GHCard(
      margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
      child: InkWell(
        onTap: () {
          // TODO: Navigate to file - need repository context
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Navigate to file: ${file.name}')),
          );
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    _getFileIcon(file.type),
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: Text(
                      file.name,
                      style: GHTokens.titleMedium.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                        fontWeight: FontWeight.w500,
                        fontFamily: 'monospace',
                      ),
                    ),
                  ),
                  if (file.size != null)
                    Text(
                      _formatFileSize(file.size!),
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                file.lastCommitMessage,
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'Modified ${DateFormatter.formatRelative(file.lastModified)} by ${file.author}',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ),
      ),
    );
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

  Color _getStatusColor(dynamic status) {
    // Handle different status types
    return Theme.of(context).colorScheme.primary;
  }

  Color _getLabelColor(String label) {
    switch (label.toLowerCase()) {
      case 'bug':
        return Colors.red.shade100;
      case 'enhancement':
        return Colors.blue.shade100;
      case 'documentation':
        return Colors.green.shade100;
      case 'help wanted':
        return Colors.orange.shade100;
      case 'good first issue':
        return Colors.purple.shade100;
      case 'question':
        return Colors.yellow.shade100;
      default:
        return Colors.grey.shade100;
    }
  }

  Color _getLabelTextColor(String label) {
    switch (label.toLowerCase()) {
      case 'bug':
        return Colors.red.shade800;
      case 'enhancement':
        return Colors.blue.shade800;
      case 'documentation':
        return Colors.green.shade800;
      case 'help wanted':
        return Colors.orange.shade800;
      case 'good first issue':
        return Colors.purple.shade800;
      case 'question':
        return Colors.yellow.shade800;
      default:
        return Colors.grey.shade800;
    }
  }

  IconData _getFileIcon(dynamic type) {
    return Icons.insert_drive_file;
  }

  String _formatFileSize(int bytes) {
    if (bytes < 1024) return '${bytes}B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)}KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)}MB';
  }

  Widget _buildAdvancedFilters() {
    return Container(
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Advanced filters',
            style: GHTokens.titleSmall.copyWith(
              color: Theme.of(context).colorScheme.onSurface,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: GHTokens.spacing16),

          // Language filter
          _buildFilterSection(
            title: 'Language',
            options: _languages
                .map(
                  (lang) => {
                    'label': lang == 'all'
                        ? 'Any language'
                        : lang.toUpperCase(),
                    'value': lang,
                  },
                )
                .toList(),
            selectedValue: _languageFilter,
            onChanged: (value) {
              setState(() {
                _languageFilter = value;
              });
              if (_currentQuery.isNotEmpty) {
                _performSearch(_currentQuery);
              }
            },
          ),

          const SizedBox(height: GHTokens.spacing16),

          // Stars filter
          _buildFilterSection(
            title: 'Stars',
            options: _starsOptions,
            selectedValue: _starsFilter,
            onChanged: (value) {
              setState(() {
                _starsFilter = value;
              });
              if (_currentQuery.isNotEmpty) {
                _performSearch(_currentQuery);
              }
            },
          ),

          const SizedBox(height: GHTokens.spacing16),

          // Forks filter
          _buildFilterSection(
            title: 'Forks',
            options: _forksOptions,
            selectedValue: _forksFilter,
            onChanged: (value) {
              setState(() {
                _forksFilter = value;
              });
              if (_currentQuery.isNotEmpty) {
                _performSearch(_currentQuery);
              }
            },
          ),

          const SizedBox(height: GHTokens.spacing16),

          // Created date filter
          _buildFilterSection(
            title: 'Created',
            options: _createdOptions,
            selectedValue: _createdFilter,
            onChanged: (value) {
              setState(() {
                _createdFilter = value;
              });
              if (_currentQuery.isNotEmpty) {
                _performSearch(_currentQuery);
              }
            },
          ),

          const SizedBox(height: GHTokens.spacing16),

          // Sort filter
          _buildFilterSection(
            title: 'Sort by',
            options: _sortOptions,
            selectedValue: _sortBy,
            onChanged: (value) {
              setState(() {
                _sortBy = value;
              });
              if (_currentQuery.isNotEmpty) {
                _performSearch(_currentQuery);
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildFilterSection({
    required String title,
    required List<Map<String, String>> options,
    required String selectedValue,
    required Function(String) onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          children: options.map((option) {
            return GHChip(
              label: option['label']!,
              isSelected: selectedValue == option['value'],
              onTap: () => onChanged(option['value']!),
            );
          }).toList(),
        ),
      ],
    );
  }

  bool _hasActiveFilters() {
    return _languageFilter != 'all' ||
        _starsFilter != 'all' ||
        _forksFilter != 'all' ||
        _createdFilter != 'all' ||
        _sortBy != 'relevance';
  }

  void _clearAllFilters() {
    setState(() {
      _languageFilter = 'all';
      _starsFilter = 'all';
      _forksFilter = 'all';
      _createdFilter = 'all';
      _sortBy = 'relevance';
    });
    if (_currentQuery.isNotEmpty) {
      _performSearch(_currentQuery);
    }
  }

  void _loadSearchHistory() {
    // In a real app, this would load from persistent storage
    _searchHistory = [
      'flutter ui components',
      'dart async programming',
      'react hooks',
      'machine learning python',
      'typescript generics',
    ];
    _recentSearches = _searchHistory.take(5).toList();
  }

  void _loadSavedSearches() {
    // In a real app, this would load from persistent storage
    _savedSearches = [
      {
        'name': 'Flutter Widgets',
        'query': 'flutter widget',
        'filters': {'language': 'dart', 'stars': '100', 'created': 'year'},
        'savedAt': DateTime.now().subtract(const Duration(days: 2)),
      },
      {
        'name': 'ML Libraries',
        'query': 'machine learning',
        'filters': {'language': 'python', 'stars': '1000', 'created': 'all'},
        'savedAt': DateTime.now().subtract(const Duration(days: 5)),
      },
    ];
  }

  void _addToSearchHistory(String query) {
    if (_searchHistory.contains(query)) {
      _searchHistory.remove(query);
    }
    _searchHistory.insert(0, query);

    // Keep only last 20 searches
    if (_searchHistory.length > 20) {
      _searchHistory = _searchHistory.take(20).toList();
    }

    _recentSearches = _searchHistory.take(5).toList();

    // In a real app, save to persistent storage here
  }

  void _saveCurrentSearch() {
    if (_currentQuery.isEmpty) return;

    showDialog(
      context: context,
      builder: (context) {
        String searchName = '';
        return AlertDialog(
          title: const Text('Save Search'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Search name',
                  hintText: 'Enter a name for this search',
                ),
                onChanged: (value) => searchName = value,
                autofocus: true,
              ),
              const SizedBox(height: GHTokens.spacing16),
              Text(
                'Query: "$_currentQuery"',
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
              if (_hasActiveFilters()) ...[
                const SizedBox(height: GHTokens.spacing8),
                Text(
                  'With current filters applied',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () {
                if (searchName.isNotEmpty) {
                  _savedSearches.insert(0, {
                    'name': searchName,
                    'query': _currentQuery,
                    'filters': {
                      'language': _languageFilter,
                      'stars': _starsFilter,
                      'forks': _forksFilter,
                      'created': _createdFilter,
                      'sort': _sortBy,
                    },
                    'savedAt': DateTime.now(),
                  });

                  // Keep only last 10 saved searches
                  if (_savedSearches.length > 10) {
                    _savedSearches = _savedSearches.take(10).toList();
                  }

                  setState(() {});
                  Navigator.of(context).pop();

                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Search saved successfully')),
                  );
                }
              },
              child: const Text('Save'),
            ),
          ],
        );
      },
    );
  }

  void _loadSavedSearch(Map<String, dynamic> savedSearch) {
    _searchController.text = savedSearch['query'];

    final filters = savedSearch['filters'] as Map<String, dynamic>;
    setState(() {
      _languageFilter = filters['language'] ?? 'all';
      _starsFilter = filters['stars'] ?? 'all';
      _forksFilter = filters['forks'] ?? 'all';
      _createdFilter = filters['created'] ?? 'all';
      _sortBy = filters['sort'] ?? 'relevance';
      _showSearchHistory = false;
    });

    _performSearch(savedSearch['query']);
  }

  void _deleteSavedSearch(int index) {
    setState(() {
      _savedSearches.removeAt(index);
    });
  }

  void _clearSearchHistory() {
    setState(() {
      _searchHistory.clear();
      _recentSearches.clear();
    });
  }

  Widget _buildSearchHistoryOverlay() {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          Padding(
            padding: const EdgeInsets.all(GHTokens.spacing16),
            child: Row(
              children: [
                Icon(
                  Icons.history,
                  size: 20,
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Text(
                  'Search History',
                  style: GHTokens.titleMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                const Spacer(),
                if (_searchHistory.isNotEmpty)
                  TextButton(
                    onPressed: _clearSearchHistory,
                    child: const Text('Clear all'),
                  ),
              ],
            ),
          ),

          const Divider(height: 1),

          // Recent searches
          if (_searchHistory.isNotEmpty) ...[
            Padding(
              padding: const EdgeInsets.all(GHTokens.spacing16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Recent searches',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: GHTokens.spacing8),
                  ...(_searchHistory.take(10).map((search) {
                    return ListTile(
                      dense: true,
                      leading: const Icon(Icons.history, size: 16),
                      title: Text(search, style: GHTokens.bodyMedium),
                      onTap: () => _onSuggestionTap(search),
                      trailing: IconButton(
                        icon: const Icon(Icons.close, size: 16),
                        onPressed: () {
                          setState(() {
                            _searchHistory.remove(search);
                            _recentSearches = _searchHistory.take(5).toList();
                          });
                        },
                      ),
                    );
                  })),
                ],
              ),
            ),
          ],

          // Saved searches
          if (_savedSearches.isNotEmpty) ...[
            const Divider(height: 1),
            Padding(
              padding: const EdgeInsets.all(GHTokens.spacing16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Saved searches',
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: GHTokens.spacing8),
                  ...(_savedSearches.map((savedSearch) {
                    return ListTile(
                      dense: true,
                      leading: const Icon(Icons.bookmark, size: 16),
                      title: Text(
                        savedSearch['name'],
                        style: GHTokens.bodyMedium.copyWith(
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      subtitle: Text(
                        '"${savedSearch['query']}"',
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                      onTap: () => _loadSavedSearch(savedSearch),
                      trailing: IconButton(
                        icon: const Icon(Icons.delete_outline, size: 16),
                        onPressed: () {
                          final index = _savedSearches.indexOf(savedSearch);
                          _deleteSavedSearch(index);
                        },
                      ),
                    );
                  })),
                ],
              ),
            ),
          ],

          // Empty state
          if (_searchHistory.isEmpty && _savedSearches.isEmpty)
            Padding(
              padding: const EdgeInsets.all(GHTokens.spacing24),
              child: Center(
                child: Column(
                  children: [
                    Icon(
                      Icons.history,
                      size: 48,
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(height: GHTokens.spacing8),
                    Text(
                      'No search history yet',
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
