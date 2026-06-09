import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../widgets/gh_repository_card.dart';
import '../data/fake_data_service.dart';
import '../components/gh_chip.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// User starred repositories screen showing repositories starred by the user
class UserStarredScreen extends StatefulWidget {
  final String username;

  const UserStarredScreen({super.key, required this.username});

  @override
  State<UserStarredScreen> createState() => _UserStarredScreenState();
}

class _UserStarredScreenState extends State<UserStarredScreen> {
  final FakeDataService _dataService = FakeDataService();
  late FakeUser _user;

  List<FakeRepository> _allStarredRepos = [];
  List<FakeRepository> _filteredStarredRepos = [];
  String _searchQuery = '';
  String _selectedLanguage = 'All';
  bool _isLoading = true;

  final List<String> _languageOptions = [
    'All',
    'Dart',
    'JavaScript',
    'Python',
    'Go',
    'Rust',
  ];

  @override
  void initState() {
    super.initState();
    _loadStarredRepositories();
  }

  void _loadStarredRepositories() async {
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

    // Get starred repositories (simulated - using random repos for demo)
    final allRepos = _dataService.getRepositories();
    _allStarredRepos = allRepos.take(8).toList(); // Simulate starred repos
    _filteredStarredRepos = List.from(_allStarredRepos);

    setState(() {
      _isLoading = false;
    });
  }

  void _performSearch(String query) {
    setState(() {
      _searchQuery = query;
      _applyFilters();
    });
  }

  void _onLanguageChanged(String language) {
    setState(() {
      _selectedLanguage = language;
      _applyFilters();
    });
  }

  void _applyFilters() {
    var filtered = List<FakeRepository>.from(_allStarredRepos);

    // Apply search filter
    if (_searchQuery.isNotEmpty) {
      filtered = filtered
          .where(
            (repo) =>
                repo.name.toLowerCase().contains(_searchQuery.toLowerCase()) ||
                repo.description.toLowerCase().contains(
                  _searchQuery.toLowerCase(),
                ) ||
                repo.owner.toLowerCase().contains(_searchQuery.toLowerCase()),
          )
          .toList();
    }

    // Apply language filter
    if (_selectedLanguage != 'All') {
      filtered = filtered
          .where((repo) => repo.language == _selectedLanguage)
          .toList();
    }

    _filteredStarredRepos = filtered;
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: GHLoadingIndicator.large(
          label: 'Loading starred repositories...',
          centered: true,
        ),
      );
    }

    return GHScreenTemplate(
      title: '${_user.name ?? _user.login} / Starred',
      body: GHListTemplate(
        filters: _languageOptions.map((language) {
          final count = language == 'All'
              ? _allStarredRepos.length
              : _allStarredRepos
                    .where((repo) => repo.language == language)
                    .length;

          return GHChip(
            label: '$language ($count)',
            isSelected: _selectedLanguage == language,
            onTap: () => _onLanguageChanged(language),
          );
        }).toList(),
        onSearch: _performSearch,
        searchHint: 'Search starred repositories...',
        emptyState: Column(
          children: [
            const Icon(Icons.star_outlined, size: 64, color: Colors.grey),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              _searchQuery.isNotEmpty || _selectedLanguage != 'All'
                  ? 'No starred repositories match your filters'
                  : '${_user.login} hasn\'t starred any repositories yet',
              style: GHTokens.headlineMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            if (_searchQuery.isNotEmpty || _selectedLanguage != 'All') ...[
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'Try adjusting your search or language filter',
                style: GHTokens.bodyLarge.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
            ] else ...[
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'Star repositories to see them here',
                style: GHTokens.bodyLarge.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
        children: _filteredStarredRepos
            .map(
              (repository) => GHRepositoryCard(
                owner: repository.owner,
                name: repository.name,
                description: repository.description,
                language: repository.language,
                starCount: repository.starCount,
                forkCount: repository.forkCount,
                lastUpdated: repository.lastUpdated,
                isPrivate: repository.isPrivate,
                showStarButton: true,
                isStarred: true, // All repos in starred screen are starred
                onTap: () => NavigationService.navigateToRepository(
                  repository.owner,
                  repository.name,
                ),
              ),
            )
            .toList(),
      ),
    );
  }
}
