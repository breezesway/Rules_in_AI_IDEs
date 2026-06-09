import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../utils/date_formatter.dart';
import '../utils/number_formatter.dart';
import '../utils/color_utils.dart';

/// A GitHub-styled repository card with complete metadata display.
///
/// This widget displays repository information including owner/name,
/// description, language, star/fork counts, and last updated timestamp.
/// It follows the Widget-GraphQL separation pattern with explicit fields
/// and factory constructors.
class GHRepositoryCard extends StatelessWidget {
  /// Repository owner username
  final String owner;

  /// Repository name
  final String name;

  /// Repository description
  final String? description;

  /// Primary programming language
  final String? language;

  /// Custom color for the language indicator
  final Color? languageColor;

  /// Number of stars
  final int starCount;

  /// Number of forks
  final int forkCount;

  /// Last updated timestamp
  final DateTime lastUpdated;

  /// Whether the repository is private
  final bool isPrivate;

  /// Callback when the card is tapped
  final VoidCallback? onTap;

  /// Whether to show the star button
  final bool showStarButton;

  /// Whether the repository is starred by the current user
  final bool isStarred;

  /// Callback when the star button is tapped
  final VoidCallback? onStarTap;

  const GHRepositoryCard({
    super.key,
    required this.owner,
    required this.name,
    this.description,
    this.language,
    this.languageColor,
    required this.starCount,
    required this.forkCount,
    required this.lastUpdated,
    this.isPrivate = false,
    this.onTap,
    this.showStarButton = false,
    this.isStarred = false,
    this.onStarTap,
  });

  /// Factory constructor for GraphQL integration
  ///
  /// This follows the Widget-GraphQL separation pattern by accepting
  /// a GraphQL fragment and extracting the required fields.
  factory GHRepositoryCard.fromGraphQL({
    Key? key,
    required Map<String, dynamic> fragment,
    VoidCallback? onTap,
    bool showStarButton = false,
    bool isStarred = false,
    VoidCallback? onStarTap,
  }) {
    return GHRepositoryCard(
      key: key,
      owner: fragment['owner']['login'] as String,
      name: fragment['name'] as String,
      description: fragment['description'] as String?,
      language: fragment['primaryLanguage']?['name'] as String?,
      languageColor: fragment['primaryLanguage']?['color'] != null
          ? Color(
              int.parse(
                    (fragment['primaryLanguage']['color'] as String).substring(
                      1,
                    ),
                    radix: 16,
                  ) +
                  0xFF000000,
            )
          : null,
      starCount: fragment['stargazerCount'] as int,
      forkCount: fragment['forkCount'] as int,
      lastUpdated: DateTime.parse(fragment['updatedAt'] as String),
      isPrivate: fragment['isPrivate'] as bool? ?? false,
      onTap: onTap,
      showStarButton: showStarButton,
      isStarred: isStarred,
      onStarTap: onStarTap,
    );
  }

  /// Factory constructor for fake data integration
  ///
  /// This creates a repository card from fake data for demo purposes.
  factory GHRepositoryCard.fromFakeRepository(
    dynamic fakeRepository, {
    Key? key,
    VoidCallback? onTap,
    bool showStarButton = false,
    bool isStarred = false,
    VoidCallback? onStarTap,
  }) {
    return GHRepositoryCard(
      key: key,
      owner: fakeRepository.owner,
      name: fakeRepository.name,
      description: fakeRepository.description,
      language: fakeRepository.language,
      languageColor: ColorUtils.getLanguageColor(fakeRepository.language),
      starCount: fakeRepository.starCount,
      forkCount: fakeRepository.forkCount,
      lastUpdated: fakeRepository.lastUpdated,
      isPrivate: fakeRepository.isPrivate,
      onTap: onTap,
      showStarButton: showStarButton,
      isStarred: isStarred,
      onStarTap: onStarTap,
    );
  }

  Widget _buildPrivacyIndicator(BuildContext context) {
    if (!isPrivate) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing4,
        vertical: 2,
      ),
      decoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).colorScheme.outline),
        borderRadius: BorderRadius.circular(GHTokens.radius4),
      ),
      child: Text(
        'Private',
        style: GHTokens.labelMedium.copyWith(
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
      ),
    );
  }

  Widget _buildLanguageIndicator(BuildContext context) {
    if (language == null) return const SizedBox.shrink();

    final color = languageColor ?? ColorUtils.getLanguageColor(language!);

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: GHTokens.spacing4),
        Text(
          language!,
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildStatItem(BuildContext context, IconData icon, int count) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          icon,
          size: 16,
          color: Theme.of(context).colorScheme.onSurfaceVariant,
        ),
        const SizedBox(width: GHTokens.spacing4),
        Text(
          NumberFormatter.formatCompact(count),
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildStarButton(BuildContext context) {
    if (!showStarButton) return const SizedBox.shrink();

    return IconButton(
      onPressed: onStarTap,
      icon: Icon(
        isStarred ? Icons.star : Icons.star_border,
        size: 20,
        color: isStarred
            ? GHTokens.warning
            : Theme.of(context).colorScheme.onSurfaceVariant,
      ),
      constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
      padding: const EdgeInsets.all(GHTokens.spacing4),
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
          // Repository name and privacy indicator
          Row(
            children: [
              Expanded(
                child: Text(
                  '$owner/$name',
                  style: GHTokens.titleMedium.copyWith(
                    color: theme.colorScheme.primary,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: GHTokens.spacing8),
              _buildPrivacyIndicator(context),
              _buildStarButton(context),
            ],
          ),

          // Description
          if (description != null && description!.isNotEmpty) ...[
            const SizedBox(height: GHTokens.spacing4),
            Text(
              description!,
              style: GHTokens.bodyMedium.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ],

          const SizedBox(height: GHTokens.spacing12),

          // Metadata row
          Row(
            children: [
              // Language indicator
              _buildLanguageIndicator(context),
              if (language != null) const SizedBox(width: GHTokens.spacing16),

              // Star count
              _buildStatItem(context, Icons.star_border, starCount),
              const SizedBox(width: GHTokens.spacing16),

              // Fork count
              _buildStatItem(context, Icons.fork_right, forkCount),

              const Spacer(),

              // Last updated
              Text(
                'Updated ${DateFormatter.formatRelative(lastUpdated)}',
                style: GHTokens.labelMedium.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
