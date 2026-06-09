import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../components/gh_card.dart';
import '../components/gh_chip.dart';
import '../widgets/gh_filter_bar.dart';
import '../widgets/gh_status_badge.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../utils/debounced_search.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Issues list example screen showing repository issues with filtering and search
class IssuesListExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  const IssuesListExample({super.key, required this.owner, required this.name});

  @override
  State<IssuesListExample> createState() => _IssuesListExampleState();
}

class _IssuesListExampleState extends State<IssuesListExample> {
  final FakeDataService _dataService = FakeDataService();
  late final DebouncedSearch _search;

  List<FakeIssue> _allIssues = [];
  List<FakeIssue> _filteredIssues = [];
  bool _isLoading = true;
  String _searchQuery = '';
  String _statusFilter = 'open'; // open, closed, all
  String _labelFilter = 'all';
  final String _assigneeFilter = 'all';
  String _sortBy = 'created'; // created, updated, comments

  final List<String> _availableLabels = [
    'bug',
    'enhancement',
    'documentation',
    'help wanted',
    'good first issue',
    'question',
  ];

  @override
  void initState() {
    super.initState();
    _search = DebouncedSearch(onSearch: _onSearch);
    _loadIssues();
  }

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  Future<void> _loadIssues() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 600));

      _allIssues = _dataService.getIssues(count: 25);
      _applyFilters();

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _onSearch(String query) {
    setState(() {
      _searchQuery = query;
    });
    _applyFilters();
  }

  void _applyFilters() {
    var filtered = List<FakeIssue>.from(_allIssues);

    // Apply status filter
    switch (_statusFilter) {
      case 'open':
        filtered = filtered
            .where((issue) => issue.status == GHStatusType.open)
            .toList();
        break;
      case 'closed':
        filtered = filtered
            .where((issue) => issue.status == GHStatusType.closed)
            .toList();
        break;
      case 'all':
      default:
        // Keep all issues
        break;
    }

    // Apply label filter
    if (_labelFilter != 'all') {
      filtered = filtered
          .where(
            (issue) => issue.labels.any(
              (label) =>
                  label.toLowerCase().contains(_labelFilter.toLowerCase()),
            ),
          )
          .toList();
    }

    // Apply assignee filter
    if (_assigneeFilter != 'all') {
      filtered = filtered
          .where(
            (issue) =>
                issue.assignee?.toLowerCase() == _assigneeFilter.toLowerCase(),
          )
          .toList();
    }

    // Apply search filter
    if (_searchQuery.isNotEmpty) {
      filtered = filtered.where((issue) {
        final query = _searchQuery.toLowerCase();
        return issue.title.toLowerCase().contains(query) ||
            issue.body.toLowerCase().contains(query) ||
            issue.labels.any((label) => label.toLowerCase().contains(query)) ||
            issue.authorLogin.toLowerCase().contains(query);
      }).toList();
    }

    // Apply sorting
    switch (_sortBy) {
      case 'created':
        filtered.sort((a, b) => b.createdAt.compareTo(a.createdAt));
        break;
      case 'updated':
        filtered.sort(
          (a, b) => (b.updatedAt ?? b.createdAt).compareTo(
            a.updatedAt ?? a.createdAt,
          ),
        );
        break;
      case 'comments':
        filtered.sort((a, b) => b.commentCount.compareTo(a.commentCount));
        break;
    }

    _filteredIssues = filtered;
  }

  void _onStatusFilterChanged(String status) {
    setState(() {
      _statusFilter = status;
    });
    _applyFilters();
  }

  void _onLabelFilterChanged(String label) {
    setState(() {
      _labelFilter = label;
    });
    _applyFilters();
  }

  void _onSortChanged(String sortBy) {
    setState(() {
      _sortBy = sortBy;
    });
    _applyFilters();
  }

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Issues',
      actions: [
        IconButton(
          icon: const Icon(Icons.add),
          onPressed: () {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(const SnackBar(content: Text('Create new issue')));
          },
          tooltip: 'New issue',
        ),
        PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'labels':
                _showLabelsDialog();
                break;
              case 'milestones':
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('View milestones')),
                );
                break;
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'labels', child: Text('Manage labels')),
            const PopupMenuItem(
              value: 'milestones',
              child: Text('View milestones'),
            ),
          ],
        ),
      ],
      body: _isLoading
          ? const GHLoadingIndicator.large(
              label: 'Loading issues...',
              centered: true,
            )
          : GHListTemplate(
              searchHint: 'Search issues...',
              onRefresh: _loadIssues,
              onSearch: (query) => _search.search(query),
              filters: [
                // Status filter
                GHFilterBar(
                  filters: [
                    GHFilterItem(
                      label: 'Open',
                      value: 'open',
                      count: _allIssues
                          .where((i) => i.status == GHStatusType.open)
                          .length,
                      isActive: _statusFilter == 'open',
                      colorIndicator: Theme.of(context).colorScheme.primary,
                    ),
                    GHFilterItem(
                      label: 'Closed',
                      value: 'closed',
                      count: _allIssues
                          .where((i) => i.status == GHStatusType.closed)
                          .length,
                      isActive: _statusFilter == 'closed',
                      colorIndicator: Colors.purple,
                    ),
                    GHFilterItem(
                      label: 'All',
                      value: 'all',
                      count: _allIssues.length,
                      isActive: _statusFilter == 'all',
                    ),
                  ],
                  onFilterChanged: (filter) =>
                      _onStatusFilterChanged(filter.value),
                  onClearAll: () => _onStatusFilterChanged('open'),
                ),

                // Label filter
                if (_availableLabels.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: GHTokens.spacing16,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Labels:',
                          style: GHTokens.labelMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                          ),
                        ),
                        const SizedBox(height: GHTokens.spacing8),
                        SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          child: Row(
                            children: [
                              GHChip(
                                label: 'All',
                                isSelected: _labelFilter == 'all',
                                onTap: () => _onLabelFilterChanged('all'),
                              ),
                              const SizedBox(width: GHTokens.spacing8),
                              ..._availableLabels.map(
                                (label) => Padding(
                                  padding: const EdgeInsets.only(
                                    right: GHTokens.spacing8,
                                  ),
                                  child: GHChip(
                                    label: label,
                                    isSelected: _labelFilter == label,
                                    onTap: () => _onLabelFilterChanged(label),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),

                // Sort options
                Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing16,
                  ),
                  child: Row(
                    children: [
                      Text(
                        'Sort:',
                        style: GHTokens.labelMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(width: GHTokens.spacing8),
                      Expanded(
                        child: SingleChildScrollView(
                          scrollDirection: Axis.horizontal,
                          child: Row(
                            children: [
                              GHChip(
                                label: 'Newest',
                                isSelected: _sortBy == 'created',
                                onTap: () => _onSortChanged('created'),
                              ),
                              const SizedBox(width: GHTokens.spacing8),
                              GHChip(
                                label: 'Recently updated',
                                isSelected: _sortBy == 'updated',
                                onTap: () => _onSortChanged('updated'),
                              ),
                              const SizedBox(width: GHTokens.spacing8),
                              GHChip(
                                label: 'Most commented',
                                isSelected: _sortBy == 'comments',
                                onTap: () => _onSortChanged('comments'),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              children: _filteredIssues.isEmpty
                  ? [_buildEmptyState()]
                  : _filteredIssues
                        .map((issue) => _buildIssueCard(issue))
                        .toList(),
            ),
    );
  }

  Widget _buildEmptyState() {
    return GHCard(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing24),
        child: Column(
          children: [
            Icon(
              _searchQuery.isNotEmpty
                  ? Icons.search_off
                  : Icons.bug_report_outlined,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              _searchQuery.isNotEmpty
                  ? 'No issues found'
                  : 'No issues match your filters',
              style: GHTokens.titleMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              _searchQuery.isNotEmpty
                  ? 'Try adjusting your search terms'
                  : 'Try changing your filters or create a new issue',
              style: GHTokens.bodyMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            if (_searchQuery.isEmpty) ...[
              const SizedBox(height: GHTokens.spacing16),
              ElevatedButton.icon(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Create new issue')),
                  );
                },
                icon: const Icon(Icons.add),
                label: const Text('New issue'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildIssueCard(FakeIssue issue) {
    return GHCard(
      child: InkWell(
        onTap: () {
          NavigationService.navigateToIssue(
            widget.owner,
            widget.name,
            issue.number,
          );
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Issue header
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  GHStatusBadge(
                    status: issue.status,
                    size: GHStatusBadgeSize.small,
                  ),
                  const SizedBox(width: GHTokens.spacing8),

                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          issue.title,
                          style: GHTokens.titleMedium.copyWith(
                            color: Theme.of(context).colorScheme.onSurface,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        const SizedBox(height: GHTokens.spacing4),

                        // Issue metadata
                        Row(
                          children: [
                            Text(
                              '#${issue.number}',
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Text(
                              ' opened ${DateFormatter.formatRelative(issue.createdAt)} by ',
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                              ),
                            ),
                            Text(
                              issue.authorLogin,
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(context).colorScheme.primary,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  // Comment count
                  if (issue.commentCount > 0) ...[
                    const SizedBox(width: GHTokens.spacing8),
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
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.comment_outlined,
                            size: 14,
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                          ),
                          const SizedBox(width: GHTokens.spacing4),
                          Text(
                            issue.commentCount.toString(),
                            style: GHTokens.labelMedium.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ],
              ),

              // Issue body preview
              if (issue.body.isNotEmpty) ...[
                const SizedBox(height: GHTokens.spacing8),
                Text(
                  issue.body,
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],

              // Labels and assignee
              if (issue.labels.isNotEmpty || issue.assignee != null) ...[
                const SizedBox(height: GHTokens.spacing12),
                Row(
                  children: [
                    // Labels
                    if (issue.labels.isNotEmpty)
                      Expanded(
                        child: Wrap(
                          spacing: GHTokens.spacing4,
                          runSpacing: GHTokens.spacing4,
                          children: issue.labels.take(3).map((label) {
                            return Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: GHTokens.spacing8,
                                vertical: GHTokens.spacing4,
                              ),
                              decoration: BoxDecoration(
                                color: _getLabelColor(label),
                                borderRadius: BorderRadius.circular(
                                  GHTokens.radius12,
                                ),
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
                      ),

                    // Assignee
                    if (issue.assignee != null) ...[
                      const SizedBox(width: GHTokens.spacing8),
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          CircleAvatar(
                            radius: 10,
                            backgroundColor: Theme.of(
                              context,
                            ).colorScheme.primaryContainer,
                            child: Text(
                              issue.assignee![0].toUpperCase(),
                              style: TextStyle(
                                fontSize: 10,
                                color: Theme.of(
                                  context,
                                ).colorScheme.onPrimaryContainer,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                          const SizedBox(width: GHTokens.spacing4),
                          Text(
                            issue.assignee!,
                            style: GHTokens.labelMedium.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
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

  void _showLabelsDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Repository Labels'),
        content: SizedBox(
          width: double.maxFinite,
          height: 300,
          child: ListView(
            children: _availableLabels.map((label) {
              return ListTile(
                leading: Container(
                  width: 16,
                  height: 16,
                  decoration: BoxDecoration(
                    color: _getLabelColor(label),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
                title: Text(label),
                subtitle: Text(
                  '${_allIssues.where((i) => i.labels.contains(label)).length} issues',
                ),
                onTap: () {
                  Navigator.of(context).pop();
                  _onLabelFilterChanged(label);
                },
              );
            }).toList(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
