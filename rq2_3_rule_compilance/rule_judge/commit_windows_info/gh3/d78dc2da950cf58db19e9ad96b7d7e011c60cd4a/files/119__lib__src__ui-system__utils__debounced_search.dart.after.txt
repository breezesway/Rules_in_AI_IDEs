import 'dart:async';

/// A utility class for implementing debounced search functionality.
///
/// This class helps prevent excessive API calls or expensive operations
/// by delaying the execution of a search function until the user has
/// stopped typing for a specified duration.
class DebouncedSearch {
  /// The duration to wait before executing the search
  final Duration delay;

  /// The search function to execute
  final Function(String query) onSearch;

  /// Timer for debouncing
  Timer? _debounceTimer;

  /// The last query that was searched
  String _lastQuery = '';

  DebouncedSearch({
    required this.onSearch,
    this.delay = const Duration(milliseconds: 300),
  });

  /// Execute a search with debouncing
  void search(String query) {
    // Cancel the previous timer if it exists
    _debounceTimer?.cancel();

    // Don't search if the query hasn't changed
    if (query == _lastQuery) return;

    // If query is empty, execute immediately
    if (query.isEmpty) {
      _lastQuery = query;
      onSearch(query);
      return;
    }

    // Set up a new timer
    _debounceTimer = Timer(delay, () {
      _lastQuery = query;
      onSearch(query);
    });
  }

  /// Cancel any pending search
  void cancel() {
    _debounceTimer?.cancel();
    _debounceTimer = null;
  }

  /// Dispose of the debounced search
  void dispose() {
    cancel();
  }
}

/// A mixin that provides debounced search functionality to widgets
mixin DebouncedSearchMixin {
  DebouncedSearch? _debouncedSearch;

  /// Initialize debounced search
  void initDebouncedSearch({
    required Function(String query) onSearch,
    Duration delay = const Duration(milliseconds: 300),
  }) {
    _debouncedSearch = DebouncedSearch(onSearch: onSearch, delay: delay);
  }

  /// Perform a debounced search
  void debouncedSearch(String query) {
    _debouncedSearch?.search(query);
  }

  /// Dispose of debounced search resources
  void disposeDebouncedSearch() {
    _debouncedSearch?.dispose();
    _debouncedSearch = null;
  }
}
