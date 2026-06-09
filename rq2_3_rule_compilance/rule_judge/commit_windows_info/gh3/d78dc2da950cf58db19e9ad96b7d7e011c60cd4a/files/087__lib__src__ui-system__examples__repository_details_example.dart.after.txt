import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_content_template.dart';
import '../widgets/gh_entity_header.dart';
import '../widgets/gh_navigation_grid.dart';
import '../widgets/gh_content_metadata.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../state_widgets/gh_error_state.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Repository details example screen showing comprehensive repository information
/// with header, metadata, navigation, and README content.
class RepositoryDetailsExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  const RepositoryDetailsExample({
    super.key,
    required this.owner,
    required this.name,
  });

  @override
  State<RepositoryDetailsExample> createState() =>
      _RepositoryDetailsExampleState();
}

class _RepositoryDetailsExampleState extends State<RepositoryDetailsExample> {
  final FakeDataService _dataService = FakeDataService();
  FakeRepository? _repository;
  bool _isLoading = true;
  String? _error;

  // Action states
  bool _isStarred = false;
  bool _isWatched = false;
  bool _isForked = false;
  bool _actionInProgress = false;

  @override
  void initState() {
    super.initState();
    _loadRepositoryData();
  }

  Future<void> _loadRepositoryData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      // Simulate network delay (shorter for testing)
      await Future.delayed(const Duration(milliseconds: 500));

      // Simulate error for test cases
      if (widget.owner == 'test-owner' && widget.name == 'test-repo') {
        throw Exception('Simulated error for testing');
      }

      // Find repository by owner and name
      final repositories = _dataService.getRepositories(count: 50);
      final repo = repositories.firstWhere(
        (r) =>
            r.owner.toLowerCase() == widget.owner.toLowerCase() &&
            r.name.toLowerCase() == widget.name.toLowerCase(),
        orElse: () =>
            repositories.first.copyWith(owner: widget.owner, name: widget.name),
      );

      _repository = repo;

      // Initialize action states (simulated user preferences)
      _isStarred = false;
      _isWatched = false;
      _isForked = false;

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _error = 'Failed to load repository details';
      });
    }
  }

  Future<void> _onStarTap() async {
    if (_actionInProgress) return;

    setState(() {
      _actionInProgress = true;
      _isStarred = !_isStarred;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 500));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              _isStarred
                  ? 'Starred ${widget.owner}/${widget.name}'
                  : 'Unstarred ${widget.owner}/${widget.name}',
            ),
          ),
        );
      }
    } catch (e) {
      // Rollback on error
      setState(() {
        _isStarred = !_isStarred;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Action failed. Please try again.')),
        );
      }
    } finally {
      setState(() {
        _actionInProgress = false;
      });
    }
  }

  Future<void> _onWatchTap() async {
    if (_actionInProgress) return;

    setState(() {
      _actionInProgress = true;
      _isWatched = !_isWatched;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 500));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              _isWatched
                  ? 'Watching ${widget.owner}/${widget.name}'
                  : 'Unwatched ${widget.owner}/${widget.name}',
            ),
          ),
        );
      }
    } catch (e) {
      // Rollback on error
      setState(() {
        _isWatched = !_isWatched;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Action failed. Please try again.')),
        );
      }
    } finally {
      setState(() {
        _actionInProgress = false;
      });
    }
  }

  Future<void> _onForkTap() async {
    if (_actionInProgress) return;

    setState(() {
      _actionInProgress = true;
      _isForked = true;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 800));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Forked ${widget.owner}/${widget.name}')),
        );
      }
    } catch (e) {
      // Rollback on error
      setState(() {
        _isForked = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Fork failed. Please try again.')),
        );
      }
    } finally {
      setState(() {
        _actionInProgress = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.owner}/${widget.name}')),
        body: GHErrorStates.repositoryLoadError(onRetry: _loadRepositoryData),
      );
    }

    return GHLoadingTransition(
      isLoading: _isLoading,
      loadingMessage: 'Loading repository...',
      child: GHScreenTemplate(
        title: '${widget.owner}/${widget.name}',
        actions: [
          IconButton(
            icon: const Icon(Icons.share),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Share ${widget.owner}/${widget.name}')),
              );
            },
          ),
          PopupMenuButton<String>(
            onSelected: (value) {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(SnackBar(content: Text('$value action')));
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'Pin repository',
                child: Text('Pin repository'),
              ),
              const PopupMenuItem(
                value: 'Add to list',
                child: Text('Add to list'),
              ),
              const PopupMenuItem(
                value: 'Report repository',
                child: Text('Report repository'),
              ),
            ],
          ),
        ],
        body: RefreshIndicator(
          onRefresh: _loadRepositoryData,
          child: GHContentTemplate(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(vertical: GHTokens.spacing16),
            sections: [
              // Repository header section
              GHContentSection(content: _buildRepositoryHeader()),

              // Action buttons section
              GHContentSection(content: _buildActionButtons()),

              // Repository metadata section
              GHContentSection(
                title: 'About',
                content: _buildRepositoryMetadata(),
              ),

              // Navigation section
              GHContentSection(
                title: 'Explore',
                content: _buildNavigationGrid(),
              ),

              // README section
              GHContentSection(
                title: 'README.md',
                content: _buildReadmeSection(),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildRepositoryHeader() {
    final repository = _repository;
    if (repository == null) {
      return const SizedBox.shrink();
    }

    return GHEntityHeader(
      title: '${widget.owner}/${widget.name}',
      subtitle: repository.description,
      avatar: CircleAvatar(
        radius: 24,
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
        child: Icon(
          repository.isPrivate ? Icons.lock : Icons.folder,
          color: Theme.of(context).colorScheme.onPrimaryContainer,
        ),
      ),
      stats: GHEntityStats.repository(
        stars: repository.starCount,
        forks: repository.forkCount,
        watchers: repository.starCount ~/ 10,
        language: repository.language,
      ),
      isPrivate: repository.isPrivate,
    );
  }

  Widget _buildActionButtons() {
    return Row(
      children: [
        Expanded(
          child: GHButton(
            label: _isStarred ? 'Starred' : 'Star',
            icon: _isStarred ? Icons.star : Icons.star_border,
            style: _isStarred ? GHButtonStyle.secondary : GHButtonStyle.primary,
            isLoading: _actionInProgress,
            onPressed: _onStarTap,
          ),
        ),
        const SizedBox(width: GHTokens.spacing8),

        Expanded(
          child: GHButton(
            label: _isWatched ? 'Watching' : 'Watch',
            icon: _isWatched ? Icons.visibility : Icons.visibility_outlined,
            style: GHButtonStyle.secondary,
            isLoading: _actionInProgress,
            onPressed: _onWatchTap,
          ),
        ),
        const SizedBox(width: GHTokens.spacing8),

        Expanded(
          child: GHButton(
            label: _isForked ? 'Forked' : 'Fork',
            icon: Icons.fork_right,
            style: GHButtonStyle.secondary,
            isLoading: _actionInProgress,
            onPressed: _onForkTap,
          ),
        ),
      ],
    );
  }

  Widget _buildRepositoryMetadata() {
    final repository = _repository;
    if (repository == null) {
      return const SizedBox.shrink();
    }

    // Build metadata items list
    final List<GHMetadataItem> metadataItems = [];

    // Website
    if (repository.homepage != null) {
      metadataItems.add(
        GHMetadataItem(
          icon: Icons.link,
          label: 'Website',
          value: repository.homepage!,
          isLink: true,
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text('Open ${repository.homepage}')),
            );
          },
        ),
      );
    }

    // License
    if (repository.license != null) {
      metadataItems.add(
        GHMetadataItem(
          icon: Icons.balance,
          label: 'License',
          value: repository.license!,
          onTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('View license details')),
            );
          },
        ),
      );
    }

    // Last updated
    metadataItems.add(
      GHMetadataItem(
        icon: Icons.schedule,
        label: 'Updated',
        value: DateFormatter.formatRelative(repository.lastUpdated),
      ),
    );

    // Created date
    if (repository.createdAt != null) {
      metadataItems.add(
        GHMetadataItem(
          icon: Icons.calendar_today,
          label: 'Created',
          value: DateFormatter.formatRelative(repository.createdAt!),
        ),
      );
    }

    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Topics using chips
          if (repository.topics.isNotEmpty) ...[
            GHMetadataChips(
              title: 'Topics',
              items: repository.topics
                  .map(
                    (topic) => GHMetadataItem(
                      label: topic,
                      value: topic,
                      onTap: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Search topic: $topic')),
                        );
                      },
                    ),
                  )
                  .toList(),
            ),
            if (metadataItems.isNotEmpty)
              const SizedBox(height: GHTokens.spacing16),
          ],

          // Repository metadata
          if (metadataItems.isNotEmpty) GHContentMetadata(items: metadataItems),
        ],
      ),
    );
  }

  Widget _buildNavigationGrid() {
    final repository = _repository;
    if (repository == null) {
      return const SizedBox.shrink();
    }

    return GHCard(
      child: GHNavigationGrid.twoByTwo(
        items: GHNavigationItems.repository(
          issues: repository.issues.length,
          pullRequests: repository.issues.where((i) => i.isPullRequest).length,
          actions: 12, // Simulated actions count
          onCodeTap: () {
            NavigationService.navigateToRepositoryTree(
              widget.owner,
              widget.name,
            );
          },
          onIssuesTap: () {
            NavigationService.navigateToIssues(widget.owner, widget.name);
          },
          onPullRequestsTap: () {
            NavigationService.navigateToPulls(widget.owner, widget.name);
          },
          onActionsTap: () {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Navigate to Actions')),
            );
          },
        ),
      ),
    );
  }

  Widget _buildReadmeSection() {
    final repository = _repository;
    if (repository == null) {
      return const SizedBox.shrink();
    }

    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(GHTokens.spacing16),
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '# ${widget.name}',
                  style: GHTokens.titleLarge.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: GHTokens.spacing12),

                Text(
                  repository.description,
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
                const SizedBox(height: GHTokens.spacing16),

                Text(
                  '## Installation\n\n```bash\nnpm install ${widget.name}\n```\n\n## Usage\n\nThis is a sample README content for demonstration purposes. In a real implementation, this would be rendered from actual markdown content.',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing16),
          TextButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(
                context,
              ).showSnackBar(const SnackBar(content: Text('View full README')));
            },
            icon: const Icon(Icons.open_in_full),
            label: const Text('View full README'),
          ),
        ],
      ),
    );
  }
}
