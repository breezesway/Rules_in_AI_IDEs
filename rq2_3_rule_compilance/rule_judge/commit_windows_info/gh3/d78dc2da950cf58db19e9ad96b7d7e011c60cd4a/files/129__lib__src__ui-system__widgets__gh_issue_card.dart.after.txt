import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import 'gh_status_badge.dart';
import '../components/gh_chip.dart';
import '../utils/date_formatter.dart';
import '../utils/color_utils.dart';

/// A GitHub-styled issue/PR card with status and metadata display.
///
/// This widget displays issue information including number, title, status,
/// labels, author, timestamp, and comment count. It follows the Widget-GraphQL
/// separation pattern with explicit fields and factory constructors.
class GHIssueCard extends StatelessWidget {
  /// Issue number
  final int number;

  /// Issue title
  final String title;

  /// Issue status (open, closed, merged, draft)
  final GHStatusType status;

  /// List of label names
  final List<String> labels;

  /// Author username
  final String authorLogin;

  /// Author avatar URL
  final String? authorAvatarUrl;

  /// Issue creation timestamp
  final DateTime createdAt;

  /// Number of comments
  final int commentCount;

  /// Assignee username
  final String? assigneeLogin;

  /// Assignee avatar URL
  final String? assigneeAvatarUrl;

  /// Callback when the card is tapped
  final VoidCallback? onTap;

  /// Maximum number of labels to display
  final int maxLabels;

  /// Whether to show the assignee
  final bool showAssignee;

  const GHIssueCard({
    super.key,
    required this.number,
    required this.title,
    required this.status,
    this.labels = const [],
    required this.authorLogin,
    this.authorAvatarUrl,
    required this.createdAt,
    this.commentCount = 0,
    this.assigneeLogin,
    this.assigneeAvatarUrl,
    this.onTap,
    this.maxLabels = 3,
    this.showAssignee = true,
  });

  /// Factory constructor for GraphQL integration
  ///
  /// This follows the Widget-GraphQL separation pattern by accepting
  /// a GraphQL fragment and extracting the required fields.
  factory GHIssueCard.fromGraphQL({
    Key? key,
    required Map<String, dynamic> fragment,
    VoidCallback? onTap,
    int maxLabels = 3,
    bool showAssignee = true,
  }) {
    return GHIssueCard(
      key: key,
      number: fragment['number'] as int,
      title: fragment['title'] as String,
      status: _mapStatusFromString(fragment['state'] as String),
      labels: (fragment['labels']['nodes'] as List<dynamic>)
          .map((label) => label['name'] as String)
          .toList(),
      authorLogin: fragment['author']?['login'] as String? ?? 'unknown',
      authorAvatarUrl: fragment['author']?['avatarUrl'] as String?,
      createdAt: DateTime.parse(fragment['createdAt'] as String),
      commentCount: fragment['comments']['totalCount'] as int? ?? 0,
      assigneeLogin:
          (fragment['assignees']['nodes'] as List<dynamic>).isNotEmpty
          ? fragment['assignees']['nodes'][0]['login'] as String?
          : null,
      assigneeAvatarUrl:
          (fragment['assignees']['nodes'] as List<dynamic>).isNotEmpty
          ? fragment['assignees']['nodes'][0]['avatarUrl'] as String?
          : null,
      onTap: onTap,
      maxLabels: maxLabels,
      showAssignee: showAssignee,
    );
  }

  static GHStatusType _mapStatusFromString(String state) {
    switch (state.toLowerCase()) {
      case 'open':
        return GHStatusType.open;
      case 'closed':
        return GHStatusType.closed;
      case 'merged':
        return GHStatusType.merged;
      case 'draft':
        return GHStatusType.draft;
      default:
        return GHStatusType.open;
    }
  }

  Widget _buildAvatar(
    BuildContext context,
    String? avatarUrl,
    String login, {
    double radius = 12,
  }) {
    if (avatarUrl != null && avatarUrl.isNotEmpty) {
      return CircleAvatar(
        radius: radius,
        backgroundImage: NetworkImage(avatarUrl),
      );
    }

    return CircleAvatar(
      radius: radius,
      backgroundColor: Theme.of(context).colorScheme.surfaceContainerHighest,
      child: Icon(
        Icons.person,
        size: radius,
        color: Theme.of(context).colorScheme.onSurfaceVariant,
      ),
    );
  }

  Widget _buildCommentCount(BuildContext context) {
    if (commentCount == 0) return const SizedBox.shrink();

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          Icons.comment_outlined,
          size: 16,
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
        const SizedBox(width: GHTokens.spacing4),
        Text(
          commentCount.toString(),
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildLabels(BuildContext context) {
    if (labels.isEmpty) return const SizedBox.shrink();

    final displayLabels = labels.take(maxLabels).toList();
    final hasMoreLabels = labels.length > maxLabels;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: GHTokens.spacing8),
        Wrap(
          spacing: GHTokens.spacing4,
          runSpacing: GHTokens.spacing4,
          children: [
            ...displayLabels.map(
              (label) => GHChip(
                label: label,
                size: GHChipSize.small,
                backgroundColor: ColorUtils.getLanguageColor(
                  label,
                ).withValues(alpha: 0.1),
                textColor: ColorUtils.getLanguageColor(label),
              ),
            ),
            if (hasMoreLabels)
              GHChip(
                label: '+${labels.length - maxLabels}',
                size: GHChipSize.small,
                backgroundColor: Theme.of(
                  context,
                ).colorScheme.surfaceContainerHighest,
                textColor: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return GHCard(
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Issue number, status, and comment count
          Row(
            children: [
              GHStatusBadge(status: status),
              const SizedBox(width: GHTokens.spacing8),
              Text(
                '#$number',
                style: GHTokens.labelMedium.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
              const Spacer(),
              _buildCommentCount(context),
            ],
          ),

          const SizedBox(height: GHTokens.spacing8),

          // Issue title
          Text(
            title,
            style: GHTokens.titleMedium.copyWith(
              color: theme.colorScheme.onSurface,
            ),
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),

          // Labels
          _buildLabels(context),

          const SizedBox(height: GHTokens.spacing12),

          // Author and metadata
          Row(
            children: [
              // Author avatar
              _buildAvatar(context, authorAvatarUrl, authorLogin),
              const SizedBox(width: GHTokens.spacing8),

              // Author and timestamp
              Expanded(
                child: Text(
                  '$authorLogin opened ${DateFormatter.formatRelative(createdAt)}',
                  style: GHTokens.labelMedium.copyWith(
                    color: theme.colorScheme.onSurfaceVariant,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),

              // Assignee avatar
              if (showAssignee && assigneeAvatarUrl != null) ...[
                const SizedBox(width: GHTokens.spacing8),
                Tooltip(
                  message: 'Assigned to $assigneeLogin',
                  child: _buildAvatar(
                    context,
                    assigneeAvatarUrl,
                    assigneeLogin ?? '',
                  ),
                ),
              ],
            ],
          ),
        ],
      ),
    );
  }
}
