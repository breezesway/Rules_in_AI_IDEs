import 'dart:async';
import '../data/fake_data_service.dart';
import 'debounced_search.dart';

/// Search service that provides debounced search functionality
/// across different content types with pagination support.
class SearchService {
  final FakeDataService _dataService = FakeDataService();
  final StreamController<SearchResults> _resultsController =
      StreamController<SearchResults>.broadcast();
  late final DebouncedSearch _debouncedSearch;

  /// Stream of search results
  Stream<SearchResults> get results => _resultsController.stream;

  /// Current search query
  String _currentQuery = '';
  String get currentQuery => _currentQuery;

  /// Current search filters
  SearchFilters _currentFilters = SearchFilters();
  SearchFilters get currentFilters => _currentFilters;

  SearchService() {
    _debouncedSearch = DebouncedSearch(
      onSearch: _performSearch,
      delay: const Duration(milliseconds: 300),
    );
  }

  /// Perform a search with debouncing
  void search(String query, {SearchFilters? filters}) {
    _currentQuery = query;
    if (filters != null) {
      _currentFilters = filters;
    }
    _debouncedSearch.search(query);
  }

  /// Update search filters without changing the query
  void updateFilters(SearchFilters filters) {
    _currentFilters = filters;
    _performSearch(_currentQuery);
  }

  /// Clear search results
  void clear() {
    _currentQuery = '';
    _currentFilters = SearchFilters();
    _resultsController.add(SearchResults.empty());
  }

  /// Perform the actual search
  void _performSearch(String query) {
    if (query.isEmpty) {
      _resultsController.add(SearchResults.empty());
      return;
    }

    // Simulate loading state
    _resultsController.add(SearchResults.loading());

    // Simulate network delay
    Future.delayed(const Duration(milliseconds: 100), () {
      try {
        final results = _executeSearch(query, _currentFilters);
        _resultsController.add(results);
      } catch (error) {
        _resultsController.add(SearchResults.error(error.toString()));
      }
    });
  }

  /// Execute the search with filters
  SearchResults _executeSearch(String query, SearchFilters filters) {
    final repositories = _searchRepositories(query, filters);
    final users = _searchUsers(query, filters);
    final issues = _searchIssues(query, filters);

    return SearchResults(
      query: query,
      repositories: repositories,
      users: users,
      issues: issues,
      isLoading: false,
    );
  }

  /// Search repositories with filters
  List<dynamic> _searchRepositories(String query, SearchFilters filters) {
    var results = _dataService.searchRepositories(query);

    // Apply filters
    if (filters.language != null) {
      results = results.where((r) => r.language == filters.language).toList();
    }
    if (filters.minStars != null) {
      results = results.where((r) => r.starCount >= filters.minStars!).toList();
    }
    if (filters.isPrivate != null) {
      results = results.where((r) => r.isPrivate == filters.isPrivate).toList();
    }
    if (filters.topics != null && filters.topics!.isNotEmpty) {
      results = results
          .where(
            (r) => filters.topics!.any((topic) => r.topics.contains(topic)),
          )
          .toList();
    }

    // Apply sorting
    if (filters.sortBy != null) {
      results = _dataService.sortRepositories(
        results,
        filters.sortBy!,
        ascending: filters.ascending,
      );
    }

    return results;
  }

  /// Search users with filters
  List<dynamic> _searchUsers(String query, SearchFilters filters) {
    var results = _dataService.searchUsers(query);

    // Apply filters
    if (filters.location != null) {
      results = results
          .where(
            (u) => u.location?.toLowerCase() == filters.location!.toLowerCase(),
          )
          .toList();
    }
    if (filters.company != null) {
      results = results
          .where(
            (u) => u.company?.toLowerCase() == filters.company!.toLowerCase(),
          )
          .toList();
    }
    if (filters.minFollowers != null) {
      results = results
          .where((u) => u.followerCount >= filters.minFollowers!)
          .toList();
    }

    return results;
  }

  /// Search issues with filters
  List<dynamic> _searchIssues(String query, SearchFilters filters) {
    var results = _dataService.searchIssues(query);

    // Apply filters
    if (filters.issueStatus != null) {
      results = results.where((i) => i.status == filters.issueStatus).toList();
    }
    if (filters.labels != null && filters.labels!.isNotEmpty) {
      results = results
          .where(
            (i) => filters.labels!.any((label) => i.labels.contains(label)),
          )
          .toList();
    }
    if (filters.assignee != null) {
      results = results
          .where((i) => i.assigneeLogin == filters.assignee)
          .toList();
    }

    return results;
  }

  /// Get available filter options
  Map<String, List<String>> getFilterOptions() {
    return _dataService.getFilterOptions();
  }

  /// Dispose of resources
  void dispose() {
    _debouncedSearch.dispose();
    _resultsController.close();
  }
}

/// Search results container
class SearchResults {
  final String query;
  final List<dynamic> repositories;
  final List<dynamic> users;
  final List<dynamic> issues;
  final bool isLoading;
  final String? error;

  const SearchResults({
    required this.query,
    required this.repositories,
    required this.users,
    required this.issues,
    this.isLoading = false,
    this.error,
  });

  /// Create empty search results
  factory SearchResults.empty() {
    return const SearchResults(
      query: '',
      repositories: [],
      users: [],
      issues: [],
    );
  }

  /// Create loading search results
  factory SearchResults.loading() {
    return const SearchResults(
      query: '',
      repositories: [],
      users: [],
      issues: [],
      isLoading: true,
    );
  }

  /// Create error search results
  factory SearchResults.error(String error) {
    return SearchResults(
      query: '',
      repositories: [],
      users: [],
      issues: [],
      error: error,
    );
  }

  /// Get total result count
  int get totalCount => repositories.length + users.length + issues.length;

  /// Check if results are empty
  bool get isEmpty => totalCount == 0 && !isLoading && error == null;
}

/// Search filters configuration
class SearchFilters {
  final String? language;
  final int? minStars;
  final bool? isPrivate;
  final List<String>? topics;
  final String? location;
  final String? company;
  final int? minFollowers;
  final dynamic issueStatus;
  final List<String>? labels;
  final String? assignee;
  final String? sortBy;
  final bool ascending;

  const SearchFilters({
    this.language,
    this.minStars,
    this.isPrivate,
    this.topics,
    this.location,
    this.company,
    this.minFollowers,
    this.issueStatus,
    this.labels,
    this.assignee,
    this.sortBy,
    this.ascending = false,
  });

  /// Create a copy with updated values
  SearchFilters copyWith({
    String? language,
    int? minStars,
    bool? isPrivate,
    List<String>? topics,
    String? location,
    String? company,
    int? minFollowers,
    dynamic issueStatus,
    List<String>? labels,
    String? assignee,
    String? sortBy,
    bool? ascending,
  }) {
    return SearchFilters(
      language: language ?? this.language,
      minStars: minStars ?? this.minStars,
      isPrivate: isPrivate ?? this.isPrivate,
      topics: topics ?? this.topics,
      location: location ?? this.location,
      company: company ?? this.company,
      minFollowers: minFollowers ?? this.minFollowers,
      issueStatus: issueStatus ?? this.issueStatus,
      labels: labels ?? this.labels,
      assignee: assignee ?? this.assignee,
      sortBy: sortBy ?? this.sortBy,
      ascending: ascending ?? this.ascending,
    );
  }
}
