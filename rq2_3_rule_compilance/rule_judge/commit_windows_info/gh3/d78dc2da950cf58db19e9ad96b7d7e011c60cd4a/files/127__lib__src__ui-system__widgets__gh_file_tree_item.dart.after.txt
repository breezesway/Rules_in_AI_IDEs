import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../utils/date_formatter.dart';
import '../utils/number_formatter.dart';

/// File type enumeration for different file and folder types
enum GHFileType {
  directory,
  file,
  image,
  markdown,
  code,
  config,
  data,
  archive,
  executable,
}

/// A GitHub-styled file tree item for file browser functionality.
///
/// This widget displays file/folder information including appropriate icons,
/// name, last commit message, file size, and author information. It follows
/// the Widget-GraphQL separation pattern with explicit fields and factory constructors.
class GHFileTreeItem extends StatelessWidget {
  /// File or folder name
  final String name;

  /// File type for appropriate icon selection
  final GHFileType type;

  /// Last commit message
  final String lastCommitMessage;

  /// Last modified timestamp
  final DateTime lastModified;

  /// Author of the last commit
  final String author;

  /// File size in bytes (null for directories)
  final int? size;

  /// Callback when the item is tapped
  final VoidCallback? onTap;

  /// Whether this item is currently selected
  final bool isSelected;

  /// Custom icon override
  final IconData? customIcon;

  /// Whether to show the commit message
  final bool showCommitMessage;

  /// Whether to show file size
  final bool showSize;

  const GHFileTreeItem({
    super.key,
    required this.name,
    required this.type,
    required this.lastCommitMessage,
    required this.lastModified,
    required this.author,
    this.size,
    this.onTap,
    this.isSelected = false,
    this.customIcon,
    this.showCommitMessage = true,
    this.showSize = true,
  });

  /// Factory constructor for GraphQL integration
  ///
  /// This follows the Widget-GraphQL separation pattern by accepting
  /// a GraphQL fragment and extracting the required fields.
  factory GHFileTreeItem.fromGraphQL({
    Key? key,
    required Map<String, dynamic> fragment,
    VoidCallback? onTap,
    bool isSelected = false,
    IconData? customIcon,
    bool showCommitMessage = true,
    bool showSize = true,
  }) {
    return GHFileTreeItem(
      key: key,
      name: fragment['name'] as String,
      type: _mapTypeFromString(fragment['type'] as String),
      lastCommitMessage: fragment['lastCommit']['message'] as String,
      lastModified: DateTime.parse(
        fragment['lastCommit']['committedDate'] as String,
      ),
      author: fragment['lastCommit']['author']['name'] as String,
      size: fragment['size'] as int?,
      onTap: onTap,
      isSelected: isSelected,
      customIcon: customIcon,
      showCommitMessage: showCommitMessage,
      showSize: showSize,
    );
  }

  static GHFileType _mapTypeFromString(String type) {
    switch (type.toLowerCase()) {
      case 'tree':
      case 'directory':
        return GHFileType.directory;
      case 'blob':
      case 'file':
      default:
        return GHFileType.file;
    }
  }

  /// Determine file type from file extension
  static GHFileType getFileTypeFromName(String fileName) {
    final extension = fileName.split('.').last.toLowerCase();

    switch (extension) {
      case 'md':
      case 'markdown':
      case 'rst':
        return GHFileType.markdown;
      case 'dart':
      case 'js':
      case 'ts':
      case 'jsx':
      case 'tsx':
      case 'py':
      case 'java':
      case 'kt':
      case 'swift':
      case 'go':
      case 'rs':
      case 'cpp':
      case 'c':
      case 'h':
      case 'cs':
      case 'php':
      case 'rb':
      case 'scala':
        return GHFileType.code;
      case 'json':
      case 'yaml':
      case 'yml':
      case 'xml':
      case 'toml':
      case 'ini':
      case 'conf':
      case 'config':
        return GHFileType.config;
      case 'png':
      case 'jpg':
      case 'jpeg':
      case 'gif':
      case 'svg':
      case 'webp':
      case 'ico':
        return GHFileType.image;
      case 'csv':
      case 'tsv':
      case 'sql':
      case 'db':
        return GHFileType.data;
      case 'zip':
      case 'tar':
      case 'gz':
      case 'rar':
      case '7z':
        return GHFileType.archive;
      case 'exe':
      case 'bin':
      case 'app':
      case 'deb':
      case 'rpm':
        return GHFileType.executable;
      default:
        return GHFileType.file;
    }
  }

  IconData _getFileIcon() {
    if (customIcon != null) return customIcon!;

    switch (type) {
      case GHFileType.directory:
        return Icons.folder;
      case GHFileType.markdown:
        return Icons.description;
      case GHFileType.code:
        return Icons.code;
      case GHFileType.config:
        return Icons.settings;
      case GHFileType.image:
        return Icons.image;
      case GHFileType.data:
        return Icons.table_chart;
      case GHFileType.archive:
        return Icons.archive;
      case GHFileType.executable:
        return Icons.launch;
      case GHFileType.file:
        return Icons.insert_drive_file;
    }
  }

  Color _getFileIconColor(BuildContext context) {
    final theme = Theme.of(context);

    switch (type) {
      case GHFileType.directory:
        return theme.colorScheme.primary;
      case GHFileType.markdown:
        return Colors.blue;
      case GHFileType.code:
        return Colors.green;
      case GHFileType.config:
        return Colors.orange;
      case GHFileType.image:
        return Colors.purple;
      case GHFileType.data:
        return Colors.teal;
      case GHFileType.archive:
        return Colors.brown;
      case GHFileType.executable:
        return Colors.red;
      case GHFileType.file:
        return theme.colorScheme.onSurfaceVariant;
    }
  }

  Widget _buildFileSize(BuildContext context) {
    if (!showSize || size == null || type == GHFileType.directory) {
      return const SizedBox.shrink();
    }

    return Text(
      NumberFormatter.formatFileSize(size!),
      style: GHTokens.labelMedium.copyWith(
        color: Theme.of(context).colorScheme.onSurfaceVariant,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final fileIcon = _getFileIcon();
    final iconColor = _getFileIconColor(context);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(GHTokens.radius4),
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing12,
          vertical: GHTokens.spacing8,
        ),
        decoration: isSelected
            ? BoxDecoration(
                color: theme.colorScheme.primaryContainer.withValues(
                  alpha: 0.3,
                ),
                borderRadius: BorderRadius.circular(GHTokens.radius4),
              )
            : null,
        child: Row(
          children: [
            // File icon
            Icon(fileIcon, size: GHTokens.iconSize24, color: iconColor),
            const SizedBox(width: GHTokens.spacing12),

            // File info
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // File name
                  Text(
                    name,
                    style: GHTokens.bodyLarge.copyWith(
                      color: theme.colorScheme.onSurface,
                      fontWeight: type == GHFileType.directory
                          ? FontWeight.w500
                          : FontWeight.normal,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),

                  // Commit message and metadata
                  if (showCommitMessage) ...[
                    const SizedBox(height: 2),
                    Row(
                      children: [
                        Expanded(
                          child: Text(
                            lastCommitMessage,
                            style: GHTokens.bodyMedium.copyWith(
                              color: theme.colorScheme.onSurfaceVariant,
                            ),
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                        const SizedBox(width: GHTokens.spacing8),
                        _buildFileSize(context),
                      ],
                    ),
                    const SizedBox(height: 2),
                    Text(
                      '$author • ${DateFormatter.formatRelative(lastModified)}',
                      style: GHTokens.labelMedium.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ],
              ),
            ),

            // Chevron for directories
            if (type == GHFileType.directory) ...[
              const SizedBox(width: GHTokens.spacing8),
              Icon(
                Icons.chevron_right,
                size: GHTokens.iconSize16,
                color: theme.colorScheme.onSurfaceVariant,
              ),
            ],
          ],
        ),
      ),
    );
  }
}

/// A compact version of the file tree item for smaller spaces
class GHFileTreeItemCompact extends StatelessWidget {
  /// File or folder name
  final String name;

  /// File type for appropriate icon selection
  final GHFileType type;

  /// File size in bytes (null for directories)
  final int? size;

  /// Callback when the item is tapped
  final VoidCallback? onTap;

  /// Whether this item is currently selected
  final bool isSelected;

  const GHFileTreeItemCompact({
    super.key,
    required this.name,
    required this.type,
    this.size,
    this.onTap,
    this.isSelected = false,
  });

  IconData _getFileIcon() {
    switch (type) {
      case GHFileType.directory:
        return Icons.folder;
      case GHFileType.markdown:
        return Icons.description;
      case GHFileType.code:
        return Icons.code;
      case GHFileType.config:
        return Icons.settings;
      case GHFileType.image:
        return Icons.image;
      case GHFileType.data:
        return Icons.table_chart;
      case GHFileType.archive:
        return Icons.archive;
      case GHFileType.executable:
        return Icons.launch;
      case GHFileType.file:
        return Icons.insert_drive_file;
    }
  }

  Color _getFileIconColor(BuildContext context) {
    final theme = Theme.of(context);

    switch (type) {
      case GHFileType.directory:
        return theme.colorScheme.primary;
      case GHFileType.markdown:
        return Colors.blue;
      case GHFileType.code:
        return Colors.green;
      case GHFileType.config:
        return Colors.orange;
      case GHFileType.image:
        return Colors.purple;
      case GHFileType.data:
        return Colors.teal;
      case GHFileType.archive:
        return Colors.brown;
      case GHFileType.executable:
        return Colors.red;
      case GHFileType.file:
        return theme.colorScheme.onSurfaceVariant;
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final fileIcon = _getFileIcon();
    final iconColor = _getFileIconColor(context);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(GHTokens.radius4),
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing8,
          vertical: GHTokens.spacing4,
        ),
        decoration: isSelected
            ? BoxDecoration(
                color: theme.colorScheme.primaryContainer.withValues(
                  alpha: 0.3,
                ),
                borderRadius: BorderRadius.circular(GHTokens.radius4),
              )
            : null,
        child: Row(
          children: [
            Icon(fileIcon, size: GHTokens.iconSize16, color: iconColor),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: Text(
                name,
                style: GHTokens.bodyMedium.copyWith(
                  color: theme.colorScheme.onSurface,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            if (size != null && type != GHFileType.directory) ...[
              const SizedBox(width: GHTokens.spacing8),
              Text(
                NumberFormatter.formatFileSize(size!),
                style: GHTokens.labelMedium.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
