import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../widgets/gh_repository_card.dart';
import '../data/fake_data_service.dart';
import '../components/gh_chip.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// User repositories screen showing a user's repositories with filtering and search
class UserRepositoriesScreen extends StatefulWidget {
  final String username;

  const UserRepositoriesScreen({super.key, required this.username});

  @override
  State<UserRepositoriesScreen> createState() => _UserRepositoriesScreenState();
}

class _UserRepositoriesScreenState extends State<UserRepositoriesScreen> {
  final FakeDataService _dataService = FakeDataService();
  late FakeUser _user;

  List<FakeRepository> _allRepositories = [];
  List<FakeRepository> _filteredRepositories = [];
  String _searchQuery = '';
  String _selectedFilter = 'All';
  bool _isLoading = true;

  final List<String> _filterOptions = [
    'All',
    'Public',
    'Private',
    'Forks',
    'Archived',
  ];

  @override
  void initState() {
    super.initState();
    _loadUserRepositories();
  }

  void _loadUserRepositories() async {
    setState(() {
      _isLoading = true;
    });

    // Simulate network delay
    await Future.delayed(const Duration(milliseconds: 500));

    // Find user and get their repositories
    final users = _dataService.getUsers();
    _user = users.firstWhere(
      (user) => user.login == widget.username,
      orElse: () => users.first,
    );

    // Get user's repositories (simulated)
    _allRepositories = _dataService
        .getRepositories(count: _user.repositoryCount)
        .where((repo) => repo.owner == _user.login)
        .toList();
    if (_allRepositories.isEmpty) {
      // Fallback: use some random repositories
      _allRepositories = _dataService.getRepositories(count: 5);
    }
    _filteredRepositories = List.from(_allRepositories);

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

  void _onFilterChanged(String filter) {
    setState(() {
      _selectedFilter = filter;
      _applyFilters();
    });
  }

  void _applyFilters() {
    var filtered = List<FakeRepository>.from(_allRepositories);

    // Apply search filter
    if (_searchQuery.isNotEmpty) {
      filtered = filtered
          .where(
            (repo) =>
                repo.name.toLowerCase().contains(_searchQuery.toLowerCase()) ||
                repo.description.toLowerCase().contains(
                  _searchQuery.toLowerCase(),
                ),
          )
          .toList();
    }

    // Apply category filter
    switch (_selectedFilter) {
      case 'Public':
        filtered = filtered.where((repo) => !repo.isPrivate).toList();
        break;
      case 'Private':
        filtered = filtered.where((repo) => repo.isPrivate).toList();
        break;
      case 'Forks':
        filtered = filtered.where((repo) => repo.isFork).toList();
        break;
      case 'Archived':
        filtered = filtered.where((repo) => repo.isArchived).toList();
        break;
      // 'All' shows everything
    }

    _filteredRepositories = filtered;
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: GHLoadingIndicator.large(
          label: 'Loading repositories...',
          centered: true,
        ),
      );
    }

    return GHScreenTemplate(
      title: '${_user.name ?? _user.login} / Repositories',
      body: GHListTemplate(
        filters: _filterOptions.map((filter) {
          final count = filter == 'All'
              ? _allRepositories.length
              : _getFilterCount(filter);

          return GHChip(
            label: '$filter ($count)',
            isSelected: _selectedFilter == filter,
            onTap: () => _onFilterChanged(filter),
          );
        }).toList(),
        onSearch: _performSearch,
        searchHint: 'Search repositories...',
        emptyState: Column(
          children: [
            const Icon(Icons.folder_outlined, size: 64, color: Colors.grey),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              _searchQuery.isNotEmpty || _selectedFilter != 'All'
                  ? 'No repositories match your filters'
                  : '${_user.login} doesn\'t have any public repositories yet',
              style: GHTokens.headlineMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            if (_searchQuery.isNotEmpty || _selectedFilter != 'All') ...[
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'Try adjusting your search or filter criteria',
                style: GHTokens.bodyLarge.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
        children: _filteredRepositories
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

  int _getFilterCount(String filter) {
    switch (filter) {
      case 'Public':
        return _allRepositories.where((repo) => !repo.isPrivate).length;
      case 'Private':
        return _allRepositories.where((repo) => repo.isPrivate).length;
      case 'Forks':
        return _allRepositories.where((repo) => repo.isFork).length;
      case 'Archived':
        return _allRepositories.where((repo) => repo.isArchived).length;
      default:
        return _allRepositories.length;
    }
  }
}
