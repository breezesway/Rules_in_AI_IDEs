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

/// Pull requests list example screen showing repository PRs with filtering
class PullsListExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  const PullsListExample({super.key, required this.owner, required this.name});

  @override
  State<PullsListExample> createState() => _PullsListExampleState();
}

class _PullsListExampleState extends State<PullsListExample> {
  final FakeDataService _dataService = FakeDataService();
  late final DebouncedSearch _search;

  List<FakeIssue> _allPulls = [];
  List<FakeIssue> _filteredPulls = [];
  bool _isLoading = true;
  String _searchQuery = '';
  String _statusFilter = 'open'; // open, closed, merged, all
  String _reviewFilter =
      'all'; // all, approved, changes_requested, review_required
  String _sortBy = 'created'; // created, updated, popularity

  @override
  void initState() {
    super.initState();
    _search = DebouncedSearch(onSearch: _onSearch);
    _loadPulls();
  }

  @override
  void dispose() {
    _search.dispose();
    super.dispose();
  }

  Future<void> _loadPulls() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 600));

      // Get only pull requests (issues with isPullRequest = true)
      final allIssues = _dataService.getIssues(count: 30);
      _allPulls = allIssues.where((issue) => issue.isPullRequest).toList();
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
    var filtered = List<FakeIssue>.from(_allPulls);

    // Apply status filter
    switch (_statusFilter) {
      case 'open':
        filtered = filtered
            .where((pr) => pr.status == GHStatusType.open)
            .toList();
        break;
      case 'closed':
        filtered = filtered
            .where((pr) => pr.status == GHStatusType.closed)
            .toList();
        break;
      case 'merged':
        filtered = filtered
            .where((pr) => pr.status == GHStatusType.merged)
            .toList();
        break;
      case 'all':
      default:
        // Keep all PRs
        break;
    }

    // Apply review filter (simulated based on labels)
    switch (_reviewFilter) {
      case 'approved':
        filtered = filtered
            .where(
              (pr) => pr.labels.any(
                (label) => label.toLowerCase().contains('approved'),
              ),
            )
            .toList();
        break;
      case 'changes_requested':
        filtered = filtered
            .where(
              (pr) => pr.labels.any(
                (label) => label.toLowerCase().contains('changes'),
              ),
            )
            .toList();
        break;
      case 'review_required':
        filtered = filtered
            .where(
              (pr) => pr.labels.any(
                (label) => label.toLowerCase().contains('review'),
              ),
            )
            .toList();
        break;
      case 'all':
      default:
        // Keep all PRs
        break;
    }

    // Apply search filter
    if (_searchQuery.isNotEmpty) {
      filtered = filtered.where((pr) {
        final query = _searchQuery.toLowerCase();
        return pr.title.toLowerCase().contains(query) ||
            pr.body.toLowerCase().contains(query) ||
            pr.labels.any((label) => label.toLowerCase().contains(query)) ||
            pr.authorLogin.toLowerCase().contains(query);
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
      case 'popularity':
        filtered.sort((a, b) => b.commentCount.compareTo(a.commentCount));
        break;
    }

    _filteredPulls = filtered;
  }

  void _onStatusFilterChanged(String status) {
    setState(() {
      _statusFilter = status;
    });
    _applyFilters();
  }

  void _onReviewFilterChanged(String review) {
    setState(() {
      _reviewFilter = review;
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
      title: 'Pull requests',
      actions: [
        IconButton(
          icon: const Icon(Icons.add),
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Create new pull request')),
            );
          },
          tooltip: 'New pull request',
        ),
        PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'compare':
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Compare branches')),
                );
                break;
              case 'drafts':
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(const SnackBar(content: Text('View draft PRs')));
                break;
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(
              value: 'compare',
              child: Text('Compare branches'),
            ),
            const PopupMenuItem(value: 'drafts', child: Text('Draft PRs')),
          ],
        ),
      ],
      body: _isLoading
          ? const GHLoadingIndicator.large(
              label: 'Loading pull requests...',
              centered: true,
            )
          : GHListTemplate(
              searchHint: 'Search pull requests...',
              onRefresh: _loadPulls,
              onSearch: (query) => _search.search(query),
              filters: [
                // Status filter
                GHFilterBar(
                  filters: [
                    GHFilterItem(
                      label: 'Open',
                      value: 'open',
                      count: _allPulls
                          .where((pr) => pr.status == GHStatusType.open)
                          .length,
                      isActive: _statusFilter == 'open',
                      colorIndicator: Theme.of(context).colorScheme.primary,
                    ),
                    GHFilterItem(
                      label: 'Closed',
                      value: 'closed',
                      count: _allPulls
                          .where((pr) => pr.status == GHStatusType.closed)
                          .length,
                      isActive: _statusFilter == 'closed',
                      colorIndicator: Colors.red,
                    ),
                    GHFilterItem(
                      label: 'Merged',
                      value: 'merged',
                      count: _allPulls
                          .where((pr) => pr.status == GHStatusType.merged)
                          .length,
                      isActive: _statusFilter == 'merged',
                      colorIndicator: Colors.purple,
                    ),
                    GHFilterItem(
                      label: 'All',
                      value: 'all',
                      count: _allPulls.length,
                      isActive: _statusFilter == 'all',
                    ),
                  ],
                  onFilterChanged: (filter) =>
                      _onStatusFilterChanged(filter.value),
                  onClearAll: () => _onStatusFilterChanged('open'),
                ),

                // Review status filter
                Padding(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing16,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Review status:',
                        style: GHTokens.labelMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                      const SizedBox(height: GHTokens.spacing8),
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: [
                            GHChip(
                              label: 'All',
                              isSelected: _reviewFilter == 'all',
                              onTap: () => _onReviewFilterChanged('all'),
                            ),
                            const SizedBox(width: GHTokens.spacing8),
                            GHChip(
                              label: 'Approved',
                              isSelected: _reviewFilter == 'approved',
                              onTap: () => _onReviewFilterChanged('approved'),
                            ),
                            const SizedBox(width: GHTokens.spacing8),
                            GHChip(
                              label: 'Changes requested',
                              isSelected: _reviewFilter == 'changes_requested',
                              onTap: () =>
                                  _onReviewFilterChanged('changes_requested'),
                            ),
                            const SizedBox(width: GHTokens.spacing8),
                            GHChip(
                              label: 'Review required',
                              isSelected: _reviewFilter == 'review_required',
                              onTap: () =>
                                  _onReviewFilterChanged('review_required'),
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
                                isSelected: _sortBy == 'popularity',
                                onTap: () => _onSortChanged('popularity'),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              children: _filteredPulls.isEmpty
                  ? [_buildEmptyState()]
                  : _filteredPulls
                        .map((pr) => _buildPullRequestCard(pr))
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
                  : Icons.merge_type_outlined,
              size: 64,
              color: Colors.grey,
            ),
            const SizedBox(height: GHTokens.spacing16),
            Text(
              _searchQuery.isNotEmpty
                  ? 'No pull requests found'
                  : 'No pull requests match your filters',
              style: GHTokens.titleMedium.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ),
            const SizedBox(height: GHTokens.spacing8),
            Text(
              _searchQuery.isNotEmpty
                  ? 'Try adjusting your search terms'
                  : 'Try changing your filters or create a new pull request',
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
                    const SnackBar(content: Text('Create new pull request')),
                  );
                },
                icon: const Icon(Icons.add),
                label: const Text('New pull request'),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildPullRequestCard(FakeIssue pr) {
    return GHCard(
      child: InkWell(
        onTap: () {
          NavigationService.navigateToPull(
            widget.owner,
            widget.name,
            pr.number,
          );
        },
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // PR header
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  GHStatusBadge(
                    status: pr.status,
                    size: GHStatusBadgeSize.small,
                  ),
                  const SizedBox(width: GHTokens.spacing8),

                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          pr.title,
                          style: GHTokens.titleMedium.copyWith(
                            color: Theme.of(context).colorScheme.onSurface,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        const SizedBox(height: GHTokens.spacing4),

                        // PR metadata
                        Row(
                          children: [
                            Text(
                              '#${pr.number}',
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Text(
                              ' by ',
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                              ),
                            ),
                            Text(
                              pr.authorLogin,
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(context).colorScheme.primary,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                            Text(
                              ' was ${pr.status == GHStatusType.merged ? 'merged' : 'opened'} ${DateFormatter.formatRelative(pr.createdAt)}',
                              style: GHTokens.bodyMedium.copyWith(
                                color: Theme.of(
                                  context,
                                ).colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),

                  // Review indicators and comment count
                  Column(
                    children: [
                      // Review status indicators
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          if (pr.labels.any((l) => l.contains('approved')))
                            Container(
                              width: 16,
                              height: 16,
                              decoration: const BoxDecoration(
                                color: Colors.green,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.check,
                                size: 12,
                                color: Colors.white,
                              ),
                            ),
                          if (pr.labels.any((l) => l.contains('changes')))
                            Container(
                              width: 16,
                              height: 16,
                              decoration: const BoxDecoration(
                                color: Colors.red,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.close,
                                size: 12,
                                color: Colors.white,
                              ),
                            ),
                          if (pr.labels.any((l) => l.contains('review')))
                            Container(
                              width: 16,
                              height: 16,
                              decoration: const BoxDecoration(
                                color: Colors.orange,
                                shape: BoxShape.circle,
                              ),
                              child: const Icon(
                                Icons.remove,
                                size: 12,
                                color: Colors.white,
                              ),
                            ),
                        ],
                      ),

                      // Comment count
                      if (pr.commentCount > 0) ...[
                        const SizedBox(height: GHTokens.spacing4),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: GHTokens.spacing8,
                            vertical: GHTokens.spacing4,
                          ),
                          decoration: BoxDecoration(
                            color: Theme.of(
                              context,
                            ).colorScheme.surfaceContainerHighest,
                            borderRadius: BorderRadius.circular(
                              GHTokens.radius12,
                            ),
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
                                pr.commentCount.toString(),
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
                ],
              ),

              // PR body preview
              if (pr.body.isNotEmpty) ...[
                const SizedBox(height: GHTokens.spacing8),
                Text(
                  pr.body,
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],

              // Branch info and labels
              const SizedBox(height: GHTokens.spacing12),
              Row(
                children: [
                  // Branch info
                  Expanded(
                    child: Row(
                      children: [
                        Icon(
                          Icons.merge_type,
                          size: 16,
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        const SizedBox(width: GHTokens.spacing4),
                        Text(
                          'feature-branch',
                          style: GHTokens.bodyMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                            fontFamily: 'monospace',
                          ),
                        ),
                        Icon(
                          Icons.arrow_forward,
                          size: 16,
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        Text(
                          'main',
                          style: GHTokens.bodyMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                            fontFamily: 'monospace',
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Labels
                  if (pr.labels.isNotEmpty)
                    Wrap(
                      spacing: GHTokens.spacing4,
                      children: pr.labels.take(2).map((label) {
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
                ],
              ),
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
      case 'approved':
        return Colors.green.shade100;
      case 'changes':
        return Colors.red.shade100;
      case 'review':
        return Colors.orange.shade100;
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
      case 'approved':
        return Colors.green.shade800;
      case 'changes':
        return Colors.red.shade800;
      case 'review':
        return Colors.orange.shade800;
      default:
        return Colors.grey.shade800;
    }
  }
}
