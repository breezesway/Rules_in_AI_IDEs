import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../utils/number_formatter.dart';

/// A GitHub-styled user card with profile statistics.
///
/// This widget displays user information including avatar, name, username,
/// bio, and repository/follower statistics. It follows the Widget-GraphQL
/// separation pattern with explicit fields and factory constructors.
class GHUserCard extends StatelessWidget {
  /// User login/username
  final String login;

  /// User display name
  final String? name;

  /// User bio/description
  final String? bio;

  /// User avatar URL
  final String avatarUrl;

  /// Number of public repositories
  final int repositoryCount;

  /// Number of followers
  final int followerCount;

  /// Number of users being followed
  final int followingCount;

  /// Callback when the card is tapped
  final VoidCallback? onTap;

  /// Whether to show the follow button
  final bool showFollowButton;

  /// Whether the user is being followed
  final bool isFollowing;

  /// Callback when the follow button is tapped
  final VoidCallback? onFollowTap;

  /// Avatar size
  final double avatarSize;

  /// Whether to show statistics
  final bool showStats;

  const GHUserCard({
    super.key,
    required this.login,
    this.name,
    this.bio,
    required this.avatarUrl,
    required this.repositoryCount,
    required this.followerCount,
    required this.followingCount,
    this.onTap,
    this.showFollowButton = false,
    this.isFollowing = false,
    this.onFollowTap,
    this.avatarSize = 48.0,
    this.showStats = true,
  });

  /// Factory constructor for GraphQL integration
  ///
  /// This follows the Widget-GraphQL separation pattern by accepting
  /// a GraphQL fragment and extracting the required fields.
  factory GHUserCard.fromGraphQL({
    Key? key,
    required Map<String, dynamic> fragment,
    VoidCallback? onTap,
    bool showFollowButton = false,
    bool isFollowing = false,
    VoidCallback? onFollowTap,
    double avatarSize = 48.0,
    bool showStats = true,
  }) {
    return GHUserCard(
      key: key,
      login: fragment['login'] as String,
      name: fragment['name'] as String?,
      bio: fragment['bio'] as String?,
      avatarUrl: fragment['avatarUrl'] as String,
      repositoryCount: fragment['repositories']['totalCount'] as int? ?? 0,
      followerCount: fragment['followers']['totalCount'] as int? ?? 0,
      followingCount: fragment['following']['totalCount'] as int? ?? 0,
      onTap: onTap,
      showFollowButton: showFollowButton,
      isFollowing: isFollowing,
      onFollowTap: onFollowTap,
      avatarSize: avatarSize,
      showStats: showStats,
    );
  }

  /// Factory constructor for fake data integration
  ///
  /// This creates a user card from fake data for demo purposes.
  factory GHUserCard.fromFakeUser(
    dynamic fakeUser, {
    Key? key,
    VoidCallback? onTap,
    bool showFollowButton = false,
    bool isFollowing = false,
    VoidCallback? onFollowTap,
    double avatarSize = 48.0,
    bool showStats = true,
  }) {
    return GHUserCard(
      key: key,
      login: fakeUser.login,
      name: fakeUser.name,
      bio: fakeUser.bio,
      avatarUrl: fakeUser.avatarUrl,
      repositoryCount: fakeUser.repositoryCount,
      followerCount: fakeUser.followerCount,
      followingCount: fakeUser.followingCount,
      onTap: onTap,
      showFollowButton: showFollowButton,
      isFollowing: isFollowing,
      onFollowTap: onFollowTap,
      avatarSize: avatarSize,
      showStats: showStats,
    );
  }

  Widget _buildAvatar(BuildContext context) {
    return CircleAvatar(
      radius: avatarSize / 2,
      backgroundImage: NetworkImage(avatarUrl),
      onBackgroundImageError: (exception, stackTrace) {
        // Handle image loading error
      },
      child: avatarUrl.isEmpty
          ? Icon(
              Icons.person,
              size: avatarSize / 2,
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            )
          : null,
    );
  }

  Widget _buildStat(BuildContext context, String label, int count) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(
          NumberFormatter.formatCompact(count),
          style: GHTokens.labelLarge.copyWith(
            fontWeight: FontWeight.w600,
            color: Theme.of(context).colorScheme.onSurface,
          ),
        ),
        Text(
          label,
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildFollowButton(BuildContext context) {
    if (!showFollowButton) return const SizedBox.shrink();

    return SizedBox(
      height: 32,
      child: OutlinedButton(
        onPressed: onFollowTap,
        style: OutlinedButton.styleFrom(
          padding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing12,
            vertical: GHTokens.spacing4,
          ),
          minimumSize: Size.zero,
          tapTargetSize: MaterialTapTargetSize.shrinkWrap,
        ),
        child: Text(
          isFollowing ? 'Unfollow' : 'Follow',
          style: GHTokens.labelMedium,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return GHCard(
      onTap: onTap,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Avatar
          _buildAvatar(context),
          const SizedBox(width: GHTokens.spacing12),

          // User info
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Name and username
                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          if (name != null && name!.isNotEmpty) ...[
                            Text(
                              name!,
                              style: GHTokens.titleMedium.copyWith(
                                color: theme.colorScheme.onSurface,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            const SizedBox(height: 2),
                            Text(
                              '@$login',
                              style: GHTokens.bodyMedium.copyWith(
                                color: theme.colorScheme.onSurfaceVariant,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ] else ...[
                            Text(
                              login,
                              style: GHTokens.titleMedium.copyWith(
                                color: theme.colorScheme.onSurface,
                              ),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                          ],
                        ],
                      ),
                    ),
                    _buildFollowButton(context),
                  ],
                ),

                // Bio
                if (bio != null && bio!.isNotEmpty) ...[
                  const SizedBox(height: GHTokens.spacing4),
                  Text(
                    bio!,
                    style: GHTokens.bodyMedium.copyWith(
                      color: theme.colorScheme.onSurfaceVariant,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],

                // Statistics
                if (showStats) ...[
                  const SizedBox(height: GHTokens.spacing8),
                  Row(
                    children: [
                      _buildStat(context, 'Repos', repositoryCount),
                      const SizedBox(width: GHTokens.spacing16),
                      _buildStat(context, 'Followers', followerCount),
                      const SizedBox(width: GHTokens.spacing16),
                      _buildStat(context, 'Following', followingCount),
                    ],
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}

/// A compact version of the user card for smaller spaces
class GHUserCardCompact extends StatelessWidget {
  /// User login/username
  final String login;

  /// User display name
  final String? name;

  /// User avatar URL
  final String avatarUrl;

  /// Callback when the card is tapped
  final VoidCallback? onTap;

  const GHUserCardCompact({
    super.key,
    required this.login,
    this.name,
    required this.avatarUrl,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(GHTokens.radius8),
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing8),
        child: Row(
          children: [
            CircleAvatar(radius: 16, backgroundImage: NetworkImage(avatarUrl)),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (name != null && name!.isNotEmpty) ...[
                    Text(
                      name!,
                      style: GHTokens.bodyMedium.copyWith(
                        color: theme.colorScheme.onSurface,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      '@$login',
                      style: GHTokens.labelMedium.copyWith(
                        color: theme.colorScheme.onSurfaceVariant,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ] else ...[
                    Text(
                      login,
                      style: GHTokens.bodyMedium.copyWith(
                        color: theme.colorScheme.onSurface,
                        fontWeight: FontWeight.w500,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
