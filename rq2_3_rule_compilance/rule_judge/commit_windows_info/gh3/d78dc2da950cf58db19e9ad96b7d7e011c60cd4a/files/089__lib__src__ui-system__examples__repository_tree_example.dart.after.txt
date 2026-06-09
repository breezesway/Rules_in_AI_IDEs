import 'package:flutter/material.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../components/gh_card.dart';
import '../components/gh_chip.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../state_widgets/gh_error_state.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Repository tree example screen showing file and folder navigation
/// with breadcrumb navigation and file metadata.
class RepositoryTreeExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  /// Current path in the repository
  final String? path;

  const RepositoryTreeExample({
    super.key,
    required this.owner,
    required this.name,
    this.path,
  });

  @override
  State<RepositoryTreeExample> createState() => _RepositoryTreeExampleState();
}

class _RepositoryTreeExampleState extends State<RepositoryTreeExample> {
  final FakeDataService _dataService = FakeDataService();
  FakeRepository? _repository;
  List<FakeFile> _currentFiles = [];
  bool _isLoading = true;
  String? _error;
  String _currentPath = '';
  List<String> _pathSegments = [];

  @override
  void initState() {
    super.initState();
    _currentPath = widget.path ?? '';
    _pathSegments = _currentPath.isEmpty ? [] : _currentPath.split('/');
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

      // Load files for current path
      _currentFiles = _dataService.getRepositoryFiles(
        widget.owner,
        widget.name,
        path: _currentPath,
      );

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _error = 'Failed to load repository files';
      });
    }
  }

  void _navigateToPath(String newPath) {
    NavigationService.navigateToRepositoryTree(
      widget.owner,
      widget.name,
      path: newPath,
    );
  }

  void _navigateToFile(FakeFile file) {
    if (file.isDirectory) {
      final newPath = _currentPath.isEmpty
          ? file.name
          : '$_currentPath/${file.name}';
      _navigateToPath(newPath);
    } else {
      NavigationService.navigateToRepositoryFile(
        widget.owner,
        widget.name,
        filePath: _currentPath.isEmpty
            ? file.name
            : '$_currentPath/${file.name}',
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.owner}/${widget.name}')),
        body: const GHLoadingIndicator.large(
          label: 'Loading repository files...',
          centered: true,
        ),
      );
    }

    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: Text('${widget.owner}/${widget.name}')),
        body: GHErrorStates.repositoryLoadError(onRetry: _loadRepositoryData),
      );
    }

    final title = _currentPath.isEmpty
        ? '${widget.owner}/${widget.name}'
        : _pathSegments.last;

    return GHScreenTemplate(
      title: title,
      actions: [
        IconButton(
          icon: const Icon(Icons.download_outlined),
          onPressed: () {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(
                  'Download ${_currentPath.isEmpty ? 'repository' : _pathSegments.last}',
                ),
              ),
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
              value: 'Clone repository',
              child: Text('Clone repository'),
            ),
            const PopupMenuItem(value: 'Find file', child: Text('Find file')),
            const PopupMenuItem(value: 'Go to line', child: Text('Go to line')),
          ],
        ),
      ],
      body: RefreshIndicator(
        onRefresh: _loadRepositoryData,
        child: Column(
          children: [
            // Breadcrumb navigation
            _buildBreadcrumbNavigation(),

            // Repository info header
            _buildRepositoryHeader(),

            // File tree content
            Expanded(child: _buildFileTree()),
          ],
        ),
      ),
    );
  }

  Widget _buildBreadcrumbNavigation() {
    if (_pathSegments.isEmpty) {
      return const SizedBox.shrink();
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(GHTokens.spacing16),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        border: Border(
          bottom: BorderSide(
            color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
            width: 1,
          ),
        ),
      ),
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: [
            // Repository root
            GestureDetector(
              onTap: () => _navigateToPath(''),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.folder_outlined,
                    size: 16,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                  Text(
                    widget.name,
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.primary,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ],
              ),
            ),

            // Path segments
            ...List.generate(_pathSegments.length, (index) {
              final segment = _pathSegments[index];
              final isLast = index == _pathSegments.length - 1;
              final pathToSegment = _pathSegments.take(index + 1).join('/');

              return Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    Icons.chevron_right,
                    size: 16,
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                  GestureDetector(
                    onTap: isLast ? null : () => _navigateToPath(pathToSegment),
                    child: Text(
                      segment,
                      style: GHTokens.bodyMedium.copyWith(
                        color: isLast
                            ? Theme.of(context).colorScheme.onSurface
                            : Theme.of(context).colorScheme.primary,
                        decoration: isLast ? null : TextDecoration.underline,
                        fontWeight: isLast ? FontWeight.w500 : null,
                      ),
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing4),
                ],
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildRepositoryHeader() {
    final repository = _repository;
    if (repository == null) {
      return const SizedBox.shrink();
    }

    return GHCard(
      margin: const EdgeInsets.all(GHTokens.spacing16),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  repository.isPrivate ? Icons.lock : Icons.folder,
                  size: 20,
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: Text(
                    '${widget.owner}/${widget.name}',
                    style: GHTokens.titleMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                    ),
                  ),
                ),
                GHChip(
                  label: repository.language,
                  backgroundColor: Theme.of(
                    context,
                  ).colorScheme.primaryContainer,
                  textColor: Theme.of(context).colorScheme.onPrimaryContainer,
                ),
              ],
            ),

            if (repository.description.isNotEmpty) ...[
              const SizedBox(height: GHTokens.spacing8),
              Text(
                repository.description,
                style: GHTokens.bodyMedium.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],

            const SizedBox(height: GHTokens.spacing12),
            Row(
              children: [
                _buildStatChip(
                  Icons.star_border,
                  repository.starCount.toString(),
                ),
                const SizedBox(width: GHTokens.spacing8),
                _buildStatChip(
                  Icons.fork_right,
                  repository.forkCount.toString(),
                ),
                const SizedBox(width: GHTokens.spacing8),
                _buildStatChip(
                  Icons.schedule,
                  DateFormatter.formatRelative(repository.lastUpdated),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatChip(IconData icon, String text) {
    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing8,
        vertical: GHTokens.spacing4,
      ),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(GHTokens.radius12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 14,
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
          const SizedBox(width: GHTokens.spacing4),
          Text(
            text,
            style: GHTokens.labelMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFileTree() {
    if (_currentFiles.isEmpty) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(GHTokens.spacing24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.folder_open_outlined, size: 64, color: Colors.grey),
              SizedBox(height: GHTokens.spacing16),
              Text(
                'This directory is empty',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
              ),
              SizedBox(height: GHTokens.spacing8),
              Text(
                'No files or folders found',
                style: TextStyle(color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    return GHListTemplate(
      padding: EdgeInsets.zero,
      children: _currentFiles.map((file) {
        return _buildFileItem(file);
      }).toList(),
    );
  }

  Widget _buildFileItem(FakeFile file) {
    final isDirectory = file.isDirectory;
    final icon = isDirectory ? Icons.folder_outlined : _getFileIcon(file.name);

    return GHCard(
      margin: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing16,
        vertical: GHTokens.spacing4,
      ),
      child: InkWell(
        onTap: () => _navigateToFile(file),
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        child: Padding(
          padding: const EdgeInsets.all(GHTokens.spacing12),
          child: Row(
            children: [
              Icon(
                icon,
                size: 20,
                color: isDirectory
                    ? Theme.of(context).colorScheme.primary
                    : Theme.of(context).colorScheme.onSurfaceVariant,
              ),
              const SizedBox(width: GHTokens.spacing12),

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      file.name,
                      style: GHTokens.bodyLarge.copyWith(
                        color: Theme.of(context).colorScheme.onSurface,
                        fontWeight: isDirectory ? FontWeight.w500 : null,
                      ),
                    ),
                    if (file.lastCommitMessage.isNotEmpty) ...[
                      const SizedBox(height: 2),
                      Text(
                        file.lastCommitMessage,
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ],
                  ],
                ),
              ),

              const SizedBox(width: GHTokens.spacing8),
              Column(
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  if (file.author.isNotEmpty)
                    Text(
                      file.author,
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  if (true)
                    Text(
                      DateFormatter.formatRelative(file.lastModified),
                      style: GHTokens.bodyMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                ],
              ),

              const SizedBox(width: GHTokens.spacing8),
              Icon(
                Icons.chevron_right,
                size: 16,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getFileIcon(String fileName) {
    final extension = fileName.split('.').last.toLowerCase();

    switch (extension) {
      case 'dart':
        return Icons.code;
      case 'js':
      case 'ts':
      case 'jsx':
      case 'tsx':
        return Icons.javascript;
      case 'py':
        return Icons.code;
      case 'java':
      case 'kt':
        return Icons.code;
      case 'swift':
        return Icons.code;
      case 'rs':
        return Icons.code;
      case 'go':
        return Icons.code;
      case 'md':
      case 'txt':
        return Icons.description_outlined;
      case 'json':
      case 'yaml':
      case 'yml':
        return Icons.data_object;
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'svg':
        return Icons.image_outlined;
      case 'pdf':
        return Icons.picture_as_pdf_outlined;
      case 'zip':
      case 'tar':
      case 'gz':
        return Icons.archive_outlined;
      default:
        return Icons.insert_drive_file_outlined;
    }
  }
}
