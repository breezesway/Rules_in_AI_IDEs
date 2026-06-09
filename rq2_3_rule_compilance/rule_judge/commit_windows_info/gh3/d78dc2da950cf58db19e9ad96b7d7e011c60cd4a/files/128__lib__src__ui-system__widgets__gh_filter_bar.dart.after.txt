import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_chip.dart';

/// A GitHub-styled filter bar with horizontal scrolling filter chips.
///
/// This widget provides a horizontal scrollable list of filter chips with
/// active/inactive states, count indicators, and clear all functionality.
/// It's commonly used for filtering repositories, issues, and other content.
class GHFilterBar extends StatelessWidget {
  /// List of filter items to display
  final List<GHFilterItem> filters;

  /// Callback when a filter is selected/deselected
  final Function(GHFilterItem)? onFilterChanged;

  /// Callback when clear all filters is tapped
  final VoidCallback? onClearAll;

  /// Whether to show the clear all button
  final bool showClearAll;

  /// Custom height for the filter bar
  final double? height;

  /// Custom padding around the filter bar
  final EdgeInsetsGeometry? padding;

  /// Whether to show filter counts
  final bool showCounts;

  const GHFilterBar({
    super.key,
    required this.filters,
    this.onFilterChanged,
    this.onClearAll,
    this.showClearAll = true,
    this.height,
    this.padding,
    this.showCounts = true,
  });

  bool get _hasActiveFilters => filters.any((filter) => filter.isActive);

  Widget _buildClearAllButton(BuildContext context) {
    return TextButton(
      onPressed: onClearAll,
      style: TextButton.styleFrom(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing8,
          vertical: GHTokens.spacing4,
        ),
        minimumSize: Size.zero,
        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
      ),
      child: Text(
        'Clear all',
        style: GHTokens.labelMedium.copyWith(
          color: Theme.of(context).colorScheme.primary,
        ),
      ),
    );
  }

  Widget _buildFilterChip(BuildContext context, GHFilterItem filter) {
    return GHChip(
      label: filter.label,
      isSelected: filter.isActive,
      count: showCounts ? filter.count : null,
      colorIndicator: filter.colorIndicator,
      onTap: () => onFilterChanged?.call(filter),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (filters.isEmpty) {
      return const SizedBox.shrink();
    }

    final List<Widget> children = [];

    if (showClearAll && _hasActiveFilters) {
      children.add(_buildClearAllButton(context));
    }

    for (final filter in filters) {
      children.add(_buildFilterChip(context, filter));
    }

    return Container(
      height: height ?? 48,
      padding: padding,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: GHTokens.spacing4),
        child: Row(
          children: children
              .map(
                (child) => Padding(
                  padding: const EdgeInsets.only(right: GHTokens.spacing8),
                  child: child,
                ),
              )
              .toList(),
        ),
      ),
    );
  }
}

/// A filter item for the filter bar
class GHFilterItem {
  /// The filter label
  final String label;

  /// Whether the filter is currently active
  final bool isActive;

  /// Optional count to display
  final int? count;

  /// Optional color indicator
  final Color? colorIndicator;

  /// Filter value for identification
  final String value;

  /// Filter category for grouping
  final String? category;

  const GHFilterItem({
    required this.label,
    required this.value,
    this.isActive = false,
    this.count,
    this.colorIndicator,
    this.category,
  });

  /// Create a copy of this filter item with updated properties
  GHFilterItem copyWith({
    String? label,
    String? value,
    bool? isActive,
    int? count,
    Color? colorIndicator,
    String? category,
  }) {
    return GHFilterItem(
      label: label ?? this.label,
      value: value ?? this.value,
      isActive: isActive ?? this.isActive,
      count: count ?? this.count,
      colorIndicator: colorIndicator ?? this.colorIndicator,
      category: category ?? this.category,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is GHFilterItem && other.value == value;
  }

  @override
  int get hashCode => value.hashCode;
}

/// A stateful filter bar that manages filter state internally
class GHFilterBarStateful extends StatefulWidget {
  /// Initial list of filter items
  final List<GHFilterItem> initialFilters;

  /// Callback when filters change
  final Function(List<GHFilterItem>)? onFiltersChanged;

  /// Whether to allow multiple active filters
  final bool allowMultiple;

  /// Whether to show the clear all button
  final bool showClearAll;

  /// Custom height for the filter bar
  final double? height;

  /// Custom padding around the filter bar
  final EdgeInsetsGeometry? padding;

  /// Whether to show filter counts
  final bool showCounts;

  const GHFilterBarStateful({
    super.key,
    required this.initialFilters,
    this.onFiltersChanged,
    this.allowMultiple = true,
    this.showClearAll = true,
    this.height,
    this.padding,
    this.showCounts = true,
  });

  @override
  State<GHFilterBarStateful> createState() => _GHFilterBarStatefulState();
}

class _GHFilterBarStatefulState extends State<GHFilterBarStateful> {
  late List<GHFilterItem> _filters;

  @override
  void initState() {
    super.initState();
    _filters = List.from(widget.initialFilters);
  }

  void _handleFilterChanged(GHFilterItem filter) {
    setState(() {
      final index = _filters.indexWhere((f) => f.value == filter.value);
      if (index != -1) {
        if (!widget.allowMultiple && !filter.isActive) {
          // Deactivate all other filters
          _filters = _filters.map((f) => f.copyWith(isActive: false)).toList();
        }
        _filters[index] = _filters[index].copyWith(isActive: !filter.isActive);
      }
    });
    widget.onFiltersChanged?.call(_filters);
  }

  void _handleClearAll() {
    setState(() {
      _filters = _filters.map((f) => f.copyWith(isActive: false)).toList();
    });
    widget.onFiltersChanged?.call(_filters);
  }

  @override
  Widget build(BuildContext context) {
    return GHFilterBar(
      filters: _filters,
      onFilterChanged: _handleFilterChanged,
      onClearAll: _handleClearAll,
      showClearAll: widget.showClearAll,
      height: widget.height,
      padding: widget.padding,
      showCounts: widget.showCounts,
    );
  }
}

/// Predefined filter items for common GitHub filtering scenarios
class GHFilterItems {
  const GHFilterItems._();

  /// Issue status filters
  static List<GHFilterItem> issueStatus({
    int openCount = 0,
    int closedCount = 0,
  }) {
    return [
      GHFilterItem(
        label: 'Open',
        value: 'open',
        count: openCount,
        isActive: true,
      ),
      GHFilterItem(label: 'Closed', value: 'closed', count: closedCount),
    ];
  }

  /// Pull request status filters
  static List<GHFilterItem> pullRequestStatus({
    int openCount = 0,
    int closedCount = 0,
    int mergedCount = 0,
    int draftCount = 0,
  }) {
    return [
      GHFilterItem(
        label: 'Open',
        value: 'open',
        count: openCount,
        isActive: true,
      ),
      GHFilterItem(label: 'Closed', value: 'closed', count: closedCount),
      GHFilterItem(label: 'Merged', value: 'merged', count: mergedCount),
      GHFilterItem(label: 'Draft', value: 'draft', count: draftCount),
    ];
  }

  /// Repository type filters
  static List<GHFilterItem> repositoryType({
    int allCount = 0,
    int sourcesCount = 0,
    int forksCount = 0,
    int archivedCount = 0,
  }) {
    return [
      GHFilterItem(label: 'All', value: 'all', count: allCount, isActive: true),
      GHFilterItem(label: 'Sources', value: 'sources', count: sourcesCount),
      GHFilterItem(label: 'Forks', value: 'forks', count: forksCount),
      GHFilterItem(label: 'Archived', value: 'archived', count: archivedCount),
    ];
  }

  /// Programming language filters
  static List<GHFilterItem> languages(Map<String, int> languageCounts) {
    return languageCounts.entries.map((entry) {
      return GHFilterItem(
        label: entry.key,
        value: entry.key.toLowerCase(),
        count: entry.value,
        colorIndicator: _getLanguageColor(entry.key),
        category: 'language',
      );
    }).toList();
  }

  /// User type filters
  static List<GHFilterItem> userType({
    int allCount = 0,
    int usersCount = 0,
    int organizationsCount = 0,
  }) {
    return [
      GHFilterItem(label: 'All', value: 'all', count: allCount, isActive: true),
      GHFilterItem(label: 'Users', value: 'users', count: usersCount),
      GHFilterItem(
        label: 'Organizations',
        value: 'organizations',
        count: organizationsCount,
      ),
    ];
  }

  /// Time-based filters
  static List<GHFilterItem> timeRange() {
    return [
      const GHFilterItem(label: 'Today', value: 'today'),
      const GHFilterItem(label: 'This week', value: 'week'),
      const GHFilterItem(label: 'This month', value: 'month'),
      const GHFilterItem(label: 'This year', value: 'year'),
    ];
  }

  static Color _getLanguageColor(String language) {
    // Simple color mapping - in a real app, this would use ColorUtils
    const colors = {
      'JavaScript': Color(0xFFF1E05A),
      'Dart': Color(0xFF00B4AB),
      'Python': Color(0xFF3572A5),
      'Swift': Color(0xFFFA7343),
      'TypeScript': Color(0xFF2B7489),
      'Java': Color(0xFFB07219),
      'Go': Color(0xFF00ADD8),
      'Rust': Color(0xFFDEA584),
    };
    return colors[language] ?? const Color(0xFF858585);
  }
}
