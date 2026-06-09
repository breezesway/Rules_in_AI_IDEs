import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../layouts/gh_screen_template.dart';
import '../layouts/gh_list_template.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../widgets/gh_status_badge.dart';
import '../data/fake_data_service.dart';
import '../tokens/gh_tokens.dart';
import '../navigation/navigation_service.dart';
import '../utils/date_formatter.dart';
import '../state_widgets/gh_loading_indicator.dart';

/// Issue detail example screen showing comprehensive issue information with comments
class IssueDetailExample extends StatefulWidget {
  /// Repository owner
  final String owner;

  /// Repository name
  final String name;

  /// Issue number
  final int number;

  const IssueDetailExample({
    super.key,
    required this.owner,
    required this.name,
    required this.number,
  });

  @override
  State<IssueDetailExample> createState() => _IssueDetailExampleState();
}

class _IssueDetailExampleState extends State<IssueDetailExample> {
  final FakeDataService _dataService = FakeDataService();
  final TextEditingController _commentController = TextEditingController();
  final FocusNode _commentFocusNode = FocusNode();

  late FakeIssue _issue;
  List<FakeComment> _comments = [];
  bool _isLoading = true;
  bool _isSubmittingComment = false;
  bool _isUpdatingIssue = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadIssueData();
  }

  @override
  void dispose() {
    _commentController.dispose();
    _commentFocusNode.dispose();
    super.dispose();
  }

  Future<void> _loadIssueData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      // Simulate network delay
      await Future.delayed(const Duration(milliseconds: 700));

      // Find issue by number or create a fake one
      final issues = _dataService.getIssues(count: 50);
      _issue = issues.firstWhere(
        (issue) => issue.number == widget.number,
        orElse: () => issues.first.copyWith(number: widget.number),
      );

      // Load comments for this issue
      _comments = _dataService.getIssueComments(widget.number);

      setState(() {
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
        _error = 'Failed to load issue details';
      });
    }
  }

  Future<void> _toggleIssueStatus() async {
    if (_isUpdatingIssue) return;

    setState(() {
      _isUpdatingIssue = true;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 500));

      final newStatus = _issue.status == GHStatusType.open
          ? GHStatusType.closed
          : GHStatusType.open;

      setState(() {
        _issue = _issue.copyWith(status: newStatus);
        _isUpdatingIssue = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Issue ${newStatus == GHStatusType.closed ? 'closed' : 'reopened'}',
            ),
          ),
        );
      }
    } catch (e) {
      setState(() {
        _isUpdatingIssue = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to update issue status')),
        );
      }
    }
  }

  Future<void> _submitComment() async {
    if (_commentController.text.trim().isEmpty || _isSubmittingComment) return;

    setState(() {
      _isSubmittingComment = true;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(milliseconds: 600));

      final newComment = FakeComment(
        id: _comments.length + 1,
        body: _commentController.text.trim(),
        authorLogin: 'current-user',
        authorAvatarUrl: 'https://github.com/current-user.png',
        createdAt: DateTime.now(),
        reactions: [],
      );

      setState(() {
        _comments.add(newComment);
        _issue = _issue.copyWith(commentCount: _issue.commentCount + 1);
        _isSubmittingComment = false;
      });

      _commentController.clear();
      _commentFocusNode.unfocus();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Comment added successfully')),
        );
      }
    } catch (e) {
      setState(() {
        _isSubmittingComment = false;
      });

      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(const SnackBar(content: Text('Failed to add comment')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('Issue #${widget.number}')),
        body: const GHLoadingIndicator.large(
          label: 'Loading issue...',
          centered: true,
        ),
      );
    }

    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: Text('Issue #${widget.number}')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: Theme.of(context).colorScheme.error,
              ),
              const SizedBox(height: GHTokens.spacing16),
              Text(
                _error!,
                style: GHTokens.titleMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: GHTokens.spacing24),
              ElevatedButton(
                onPressed: _loadIssueData,
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    return GHScreenTemplate(
      title: 'Issue #${widget.number}',
      actions: [
        IconButton(
          icon: const Icon(Icons.link),
          onPressed: () async {
            final url =
                'https://github.com/${widget.owner}/${widget.name}/issues/${widget.number}';
            await Clipboard.setData(ClipboardData(text: url));
            if (mounted && context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Issue URL copied to clipboard')),
              );
            }
          },
          tooltip: 'Copy link',
        ),
        PopupMenuButton<String>(
          onSelected: (value) {
            switch (value) {
              case 'edit':
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(const SnackBar(content: Text('Edit issue')));
                break;
              case 'pin':
                ScaffoldMessenger.of(
                  context,
                ).showSnackBar(const SnackBar(content: Text('Pin issue')));
                break;
              case 'subscribe':
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Subscribe to notifications')),
                );
                break;
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'edit', child: Text('Edit issue')),
            const PopupMenuItem(value: 'pin', child: Text('Pin issue')),
            const PopupMenuItem(value: 'subscribe', child: Text('Subscribe')),
          ],
        ),
      ],
      body: RefreshIndicator(
        onRefresh: _loadIssueData,
        child: Column(
          children: [
            Expanded(
              child: GHListTemplate(
                padding: EdgeInsets.zero,
                children: [
                  // Issue header
                  _buildIssueHeader(),

                  // Issue body
                  _buildIssueBody(),

                  // Comments
                  ..._comments.map((comment) => _buildComment(comment)),
                ],
              ),
            ),

            // Comment input
            _buildCommentInput(),
          ],
        ),
      ),
    );
  }

  Widget _buildIssueHeader() {
    return GHCard(
      margin: const EdgeInsets.all(GHTokens.spacing16),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status and title
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GHStatusBadge(
                  status: _issue.status,
                  size: GHStatusBadgeSize.medium,
                ),
                const SizedBox(width: GHTokens.spacing12),

                Expanded(
                  child: Text(
                    _issue.title,
                    style: GHTokens.titleLarge.copyWith(
                      color: Theme.of(context).colorScheme.onSurface,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing12),

            // Issue metadata
            Row(
              children: [
                Text(
                  '#${_issue.number}',
                  style: GHTokens.bodyLarge.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Text(
                  ' opened ${DateFormatter.formatRelative(_issue.createdAt)} by ',
                  style: GHTokens.bodyLarge.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
                GestureDetector(
                  onTap: () {
                    NavigationService.navigateToUser(_issue.authorLogin);
                  },
                  child: Text(
                    _issue.authorLogin,
                    style: GHTokens.bodyLarge.copyWith(
                      color: Theme.of(context).colorScheme.primary,
                      fontWeight: FontWeight.w500,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ),
              ],
            ),

            // Labels
            if (_issue.labels.isNotEmpty) ...[
              const SizedBox(height: GHTokens.spacing12),
              Wrap(
                spacing: GHTokens.spacing8,
                runSpacing: GHTokens.spacing8,
                children: _issue.labels.map((label) {
                  return Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: GHTokens.spacing8,
                      vertical: GHTokens.spacing4,
                    ),
                    decoration: BoxDecoration(
                      color: _getLabelColor(label),
                      borderRadius: BorderRadius.circular(GHTokens.radius12),
                    ),
                    child: Text(
                      label,
                      style: GHTokens.labelMedium.copyWith(
                        color: _getLabelTextColor(label),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],

            // Assignee and metadata
            if (_issue.assignee != null) ...[
              const SizedBox(height: GHTokens.spacing12),
              Row(
                children: [
                  CircleAvatar(
                    radius: 16,
                    backgroundColor: Theme.of(
                      context,
                    ).colorScheme.primaryContainer,
                    child: Text(
                      _issue.assignee![0].toUpperCase(),
                      style: TextStyle(
                        fontSize: 14,
                        color: Theme.of(context).colorScheme.onPrimaryContainer,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Text(
                    'Assigned to ${_issue.assignee}',
                    style: GHTokens.bodyMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
            ],

            // Action buttons
            const SizedBox(height: GHTokens.spacing16),
            Row(
              children: [
                Expanded(
                  child: GHButton(
                    label: _issue.status == GHStatusType.open
                        ? 'Close issue'
                        : 'Reopen issue',
                    icon: _issue.status == GHStatusType.open
                        ? Icons.close
                        : Icons.refresh,
                    style: _issue.status == GHStatusType.open
                        ? GHButtonStyle.secondary
                        : GHButtonStyle.primary,
                    isLoading: _isUpdatingIssue,
                    onPressed: _toggleIssueStatus,
                  ),
                ),
                const SizedBox(width: GHTokens.spacing8),
                Expanded(
                  child: GHButton(
                    label: 'Edit issue',
                    icon: Icons.edit,
                    style: GHButtonStyle.secondary,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Edit issue')),
                      );
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIssueBody() {
    return GHCard(
      margin: const EdgeInsets.fromLTRB(
        GHTokens.spacing16,
        0,
        GHTokens.spacing16,
        GHTokens.spacing16,
      ),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Author header
            Row(
              children: [
                CircleAvatar(
                  radius: 16,
                  backgroundImage: NetworkImage(_issue.authorAvatarUrl),
                ),
                const SizedBox(width: GHTokens.spacing8),

                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        _issue.authorLogin,
                        style: GHTokens.bodyMedium.copyWith(
                          fontWeight: FontWeight.w500,
                          color: Theme.of(context).colorScheme.onSurface,
                        ),
                      ),
                      Text(
                        DateFormatter.formatRelative(_issue.createdAt),
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                  ),
                ),

                IconButton(
                  icon: const Icon(Icons.more_vert),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Issue options')),
                    );
                  },
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing12),

            // Issue content
            Text(
              _issue.body.isNotEmpty ? _issue.body : 'No description provided.',
              style: GHTokens.bodyLarge.copyWith(
                color: Theme.of(context).colorScheme.onSurface,
              ),
            ),

            // Reactions
            if (_issue.reactions.isNotEmpty) ...[
              const SizedBox(height: GHTokens.spacing12),
              Wrap(
                spacing: GHTokens.spacing8,
                children: _issue.reactions.map((reaction) {
                  return GestureDetector(
                    onTap: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('${reaction.emoji} reaction')),
                      );
                    },
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Theme.of(context).colorScheme.outline,
                        ),
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(reaction.emoji),
                          const SizedBox(width: GHTokens.spacing4),
                          Text(
                            reaction.count.toString(),
                            style: GHTokens.labelSmall,
                          ),
                        ],
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildComment(FakeComment comment) {
    return GHCard(
      margin: const EdgeInsets.fromLTRB(
        GHTokens.spacing16,
        0,
        GHTokens.spacing16,
        GHTokens.spacing16,
      ),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Comment header
            Row(
              children: [
                CircleAvatar(
                  radius: 16,
                  backgroundImage: NetworkImage(comment.authorAvatarUrl),
                ),
                const SizedBox(width: GHTokens.spacing8),

                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Text(
                            comment.authorLogin,
                            style: GHTokens.bodyMedium.copyWith(
                              fontWeight: FontWeight.w500,
                              color: Theme.of(context).colorScheme.onSurface,
                            ),
                          ),
                          if (comment.authorLogin == _issue.authorLogin) ...[
                            const SizedBox(width: GHTokens.spacing8),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: GHTokens.spacing4,
                                vertical: 1,
                              ),
                              decoration: BoxDecoration(
                                color: Theme.of(
                                  context,
                                ).colorScheme.primaryContainer,
                                borderRadius: BorderRadius.circular(
                                  GHTokens.radius4,
                                ),
                              ),
                              child: Text(
                                'Author',
                                style: GHTokens.labelSmall.copyWith(
                                  color: Theme.of(
                                    context,
                                  ).colorScheme.onPrimaryContainer,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                          ],
                        ],
                      ),
                      Text(
                        DateFormatter.formatRelative(comment.createdAt),
                        style: GHTokens.bodyMedium.copyWith(
                          color: Theme.of(context).colorScheme.onSurfaceVariant,
                        ),
                      ),
                    ],
                  ),
                ),

                IconButton(
                  icon: const Icon(Icons.more_vert),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Comment options')),
                    );
                  },
                ),
              ],
            ),

            const SizedBox(height: GHTokens.spacing12),

            // Comment content
            Text(
              comment.body,
              style: GHTokens.bodyLarge.copyWith(
                color: Theme.of(context).colorScheme.onSurface,
              ),
            ),

            // Comment reactions
            if (comment.reactions.isNotEmpty) ...[
              const SizedBox(height: GHTokens.spacing12),
              Wrap(
                spacing: GHTokens.spacing8,
                children: comment.reactions.map((reaction) {
                  return GestureDetector(
                    onTap: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('${reaction.emoji} reaction')),
                      );
                    },
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: GHTokens.spacing8,
                        vertical: GHTokens.spacing4,
                      ),
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Theme.of(context).colorScheme.outline,
                        ),
                        borderRadius: BorderRadius.circular(GHTokens.radius12),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(reaction.emoji),
                          const SizedBox(width: GHTokens.spacing4),
                          Text(
                            reaction.count.toString(),
                            style: GHTokens.labelSmall,
                          ),
                        ],
                      ),
                    ),
                  );
                }).toList(),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildCommentInput() {
    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
        border: Border(
          top: BorderSide(
            color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
            width: 1,
          ),
        ),
      ),
      child: Padding(
        padding: EdgeInsets.only(
          left: GHTokens.spacing16,
          right: GHTokens.spacing16,
          top: GHTokens.spacing12,
          bottom: MediaQuery.of(context).viewInsets.bottom + GHTokens.spacing12,
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            CircleAvatar(
              radius: 16,
              backgroundColor: Theme.of(context).colorScheme.primaryContainer,
              child: Text(
                'U',
                style: TextStyle(
                  color: Theme.of(context).colorScheme.onPrimaryContainer,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            const SizedBox(width: GHTokens.spacing12),

            Expanded(
              child: TextField(
                controller: _commentController,
                focusNode: _commentFocusNode,
                maxLines: null,
                textCapitalization: TextCapitalization.sentences,
                decoration: InputDecoration(
                  hintText: 'Write a comment...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(GHTokens.radius8),
                  ),
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing12,
                    vertical: GHTokens.spacing8,
                  ),
                ),
                onSubmitted: (_) => _submitComment(),
              ),
            ),

            const SizedBox(width: GHTokens.spacing8),

            IconButton.filled(
              onPressed:
                  _commentController.text.trim().isEmpty || _isSubmittingComment
                  ? null
                  : _submitComment,
              icon: _isSubmittingComment
                  ? SizedBox(
                      width: 16,
                      height: 16,
                      child: GHLoadingIndicator.small(
                        color: Theme.of(context).colorScheme.onPrimary,
                      ),
                    )
                  : const Icon(Icons.send),
              tooltip: 'Add comment',
            ),
          ],
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
}
