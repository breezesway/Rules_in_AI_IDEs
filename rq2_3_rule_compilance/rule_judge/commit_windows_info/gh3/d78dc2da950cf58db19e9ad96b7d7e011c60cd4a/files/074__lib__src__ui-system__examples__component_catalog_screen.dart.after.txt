import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../components/gh_chip.dart';
import '../components/gh_list_tile.dart';
import '../components/gh_search_bar.dart';
import '../widgets/gh_status_badge.dart';
import '../components/gh_text_field.dart';
import '../state_widgets/gh_empty_state.dart';
import '../state_widgets/gh_error_state.dart';
import '../state_widgets/gh_loading_indicator.dart';
import '../layouts/gh_content_template.dart';
import '../layouts/gh_screen_template.dart';
import '../widgets/gh_content_metadata.dart';
import '../widgets/theme_toggle_button.dart';
import '../utils/color_utils.dart';

/// **REFERENCE IMPLEMENTATION** - Component Catalog Screen
///
/// This screen serves as the primary reference implementation for component usage
/// patterns in the GH3 design system. It demonstrates:
///
/// - Proper component instantiation and configuration
/// - Correct spacing using GHTokens constants
/// - State management patterns for interactive components
/// - GHScreenTemplate usage for consistent navigation
/// - Material Design 3 theming integration
///
/// **Usage as Reference:**
/// - Copy component examples from this file for new implementations
/// - Follow the spacing patterns demonstrated here
/// - Use the state management approaches shown in interactive sections
/// - Maintain the same component configuration patterns
///
/// This screen serves as an interactive component library where developers
/// can see all components in action with various configurations and states.
class ComponentCatalogScreen extends StatefulWidget {
  const ComponentCatalogScreen({super.key});

  @override
  State<ComponentCatalogScreen> createState() => _ComponentCatalogScreenState();
}

class _ComponentCatalogScreenState extends State<ComponentCatalogScreen> {
  bool _isButtonLoading = false;
  bool _chipSelected = false;
  String _searchText = '';
  String _textFieldValue = '';
  bool _showLoadingIndicator = false;

  @override
  Widget build(BuildContext context) {
    // REFERENCE PATTERN: Always use GHScreenTemplate for consistent screen structure
    return GHScreenTemplate(
      title: 'Component Catalog',
      actions: const [ThemeToggleButton()],
      body: SingleChildScrollView(
        // REFERENCE PATTERN: Use GHTokens spacing constants for all padding/margins
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionHeader('GHCard Component'),
            _buildCardSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHButton Component'),
            _buildButtonSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHChip Component'),
            _buildChipSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHListTile Component'),
            _buildListTileSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHSearchBar Component'),
            _buildSearchBarSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHStatusBadge Component'),
            _buildStatusBadgeSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHTextField Component'),
            _buildTextFieldSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHEmptyState Component'),
            _buildEmptyStateSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHErrorState Component'),
            _buildErrorStateSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHLoadingIndicator Component'),
            _buildLoadingIndicatorSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHCard Variants'),
            _buildCardVariantsSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHContentTemplate Component'),
            _buildContentTemplateSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader('GHContentMetadata Component'),
            _buildContentMetadataSection(),
          ],
        ),
      ),
    );
  }

  // REFERENCE PATTERN: Helper method for consistent section headers
  Widget _buildSectionHeader(String title) {
    return Padding(
      // REFERENCE PATTERN: Use specific spacing tokens instead of arbitrary values
      padding: const EdgeInsets.only(bottom: GHTokens.spacing16),
      // REFERENCE PATTERN: Use GHTokens typography constants for consistent text styling
      child: Text(title, style: GHTokens.titleLarge),
    );
  }

  Widget _buildCardSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Basic Cards', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // REFERENCE PATTERN: Basic card with standard content layout
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // REFERENCE PATTERN: Always use GHTokens for typography
              Text('Basic Card', style: GHTokens.titleMedium),
              // REFERENCE PATTERN: Use spacing tokens for consistent vertical spacing
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This is a basic card with default styling and padding.',
                style: GHTokens.bodyMedium,
              ),
            ],
          ),
        ),

        // REFERENCE PATTERN: Consistent spacing between components
        const SizedBox(height: GHTokens.spacing16),

        // REFERENCE PATTERN: Interactive card with tap handler and visual feedback
        GHCard(
          onTap: () {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(const SnackBar(content: Text('Card tapped!')));
          },
          child: Row(
            children: [
              Icon(
                Icons.touch_app,
                color: Theme.of(context).colorScheme.primary,
                size: GHTokens.iconSize24,
              ),
              const SizedBox(width: GHTokens.spacing12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Interactive Card', style: GHTokens.titleMedium),
                    const SizedBox(height: GHTokens.spacing4),
                    Text(
                      'Tap this card to see the interaction feedback.',
                      style: GHTokens.bodyMedium,
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.chevron_right,
                color: Theme.of(context).colorScheme.onSurfaceVariant,
                size: GHTokens.iconSize18,
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Custom elevation card
        GHCard(
          elevation: GHTokens.elevation3,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Elevated Card', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This card has higher elevation (3dp) for more prominence.',
                style: GHTokens.bodyMedium,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildButtonSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Button States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Primary buttons
        Wrap(
          spacing: GHTokens.spacing12,
          runSpacing: GHTokens.spacing12,
          children: [
            GHButton(
              label: 'Star',
              icon: Icons.star_border,
              onPressed: () => _showSnackBar('Star button pressed'),
            ),
            GHButton(
              label: 'Watch',
              icon: Icons.visibility,
              onPressed: () => _showSnackBar('Watch button pressed'),
            ),
            GHButton(
              label: 'Fork',
              icon: Icons.fork_right,
              onPressed: () => _showSnackBar('Fork button pressed'),
            ),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Secondary buttons
        Wrap(
          spacing: GHTokens.spacing12,
          runSpacing: GHTokens.spacing12,
          children: [
            GHButton(
              label: 'Follow',
              style: GHButtonStyle.secondary,
              icon: Icons.person_add,
              onPressed: () => _showSnackBar('Follow button pressed'),
            ),
            GHButton(
              label: 'Clone',
              style: GHButtonStyle.secondary,
              icon: Icons.download,
              onPressed: () => _showSnackBar('Clone button pressed'),
            ),
            GHButton(
              label: 'Subscribe',
              style: GHButtonStyle.secondary,
              icon: Icons.notifications,
              onPressed: () => _showSnackBar('Subscribe button pressed'),
            ),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Loading and disabled states
        Row(
          children: [
            GHButton(
              label: 'Loading',
              isLoading: _isButtonLoading,
              onPressed: () {
                setState(() {
                  _isButtonLoading = true;
                });
                Future.delayed(const Duration(seconds: 2), () {
                  if (mounted) {
                    setState(() {
                      _isButtonLoading = false;
                    });
                  }
                });
              },
            ),
            const SizedBox(width: GHTokens.spacing12),
            const GHButton(label: 'Disabled', onPressed: null),
          ],
        ),
      ],
    );
  }

  Widget _buildChipSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Filter Chips', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Basic chips
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          children: [
            GHChip(
              label: 'Open',
              count: 23,
              isSelected: _chipSelected,
              onTap: () {
                setState(() {
                  _chipSelected = !_chipSelected;
                });
              },
            ),
            const GHChip(label: 'Closed', count: 145),
            const GHChip(label: 'bug', colorIndicator: Colors.red, count: 12),
            const GHChip(
              label: 'enhancement',
              colorIndicator: Colors.blue,
              count: 8,
            ),
            const GHChip(
              label: 'documentation',
              colorIndicator: Colors.green,
              count: 5,
            ),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        Text('Language Chips', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Language chips
        Wrap(
          spacing: GHTokens.spacing8,
          runSpacing: GHTokens.spacing8,
          children: ColorUtils.getPopularLanguages().take(8).map((langInfo) {
            return GHChip(
              label: langInfo['language'] as String,
              colorIndicator: langInfo['color'] as Color,
              isSelectable: false,
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildListTileSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('List Items', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        Container(
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: BorderRadius.circular(GHTokens.radius8),
            border: Border.all(
              color: Theme.of(
                context,
              ).colorScheme.outline.withValues(alpha: 0.2),
            ),
          ),
          child: Column(
            children: [
              GHListTile(
                leading: CircleAvatar(
                  backgroundColor: Theme.of(context).colorScheme.primary,
                  child: const Icon(Icons.person, color: Colors.white),
                ),
                title: const Text('John Doe'),
                subtitle: const Text('@johndoe • Joined 2 years ago'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showSnackBar('User tapped'),
              ),
              Divider(
                height: 1,
                color: Theme.of(
                  context,
                ).colorScheme.outline.withValues(alpha: 0.2),
              ),
              GHListTile(
                leading: Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: ColorUtils.getLanguageColor('JavaScript'),
                    borderRadius: BorderRadius.circular(GHTokens.radius8),
                  ),
                  child: const Icon(Icons.code, color: Colors.white),
                ),
                title: const Text('awesome-project'),
                subtitle: const Text('A really awesome JavaScript project'),
                trailing: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      Icons.star,
                      size: GHTokens.iconSize16,
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(
                      '1.2k',
                      style: GHTokens.labelMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
                onTap: () => _showSnackBar('Repository tapped'),
              ),
              Divider(
                height: 1,
                color: Theme.of(
                  context,
                ).colorScheme.outline.withValues(alpha: 0.2),
              ),
              GHListTile(
                leading: Icon(
                  Icons.bug_report,
                  color: GHTokens.error,
                  size: GHTokens.iconSize24,
                ),
                title: const Text('Fix critical bug in authentication'),
                subtitle: const Text(
                  'Issue #123 • opened 2 hours ago by @alice',
                ),
                trailing: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: GHTokens.spacing8,
                    vertical: GHTokens.spacing4,
                  ),
                  decoration: BoxDecoration(
                    color: GHTokens.error.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(GHTokens.radius12),
                  ),
                  child: Text(
                    'Open',
                    style: GHTokens.labelMedium.copyWith(color: GHTokens.error),
                  ),
                ),
                onTap: () => _showSnackBar('Issue tapped'),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildSearchBarSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Search Inputs', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHSearchBar(
          hintText: 'Search repositories, users, issues...',
          onChanged: (value) {
            setState(() {
              _searchText = value;
            });
          },
          onSubmitted: (value) => _showSnackBar('Search submitted: $value'),
        ),

        const SizedBox(height: GHTokens.spacing16),

        GHSearchBar(
          hintText: 'Search with custom icon',
          prefixIcon: Icons.filter_list,
          suffixIcon: Icons.tune,
          onSuffixIconTap: () => _showSnackBar('Filter options tapped'),
          onChanged: (value) {},
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHSearchBar(hintText: 'Disabled search bar', enabled: false),

        if (_searchText.isNotEmpty) ...[
          const SizedBox(height: GHTokens.spacing12),
          Text(
            'Search text: "$_searchText"',
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildStatusBadgeSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Status Indicators', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        Wrap(
          spacing: GHTokens.spacing12,
          runSpacing: GHTokens.spacing12,
          children: const [
            GHStatusBadge(status: GHStatusType.open),
            GHStatusBadge(status: GHStatusType.closed),
            GHStatusBadge(status: GHStatusType.merged),
            GHStatusBadge(status: GHStatusType.draft),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        Text('Custom Status Labels', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        const Wrap(
          spacing: GHTokens.spacing12,
          runSpacing: GHTokens.spacing12,
          children: [
            GHStatusBadge(
              status: GHStatusType.open,
              customLabel: 'In Progress',
            ),
            GHStatusBadge(status: GHStatusType.merged, customLabel: 'Approved'),
            GHStatusBadge(
              status: GHStatusType.draft,
              customLabel: 'Pending Review',
            ),
            GHStatusBadge(status: GHStatusType.closed, customLabel: 'Rejected'),
          ],
        ),

        const SizedBox(height: GHTokens.spacing16),

        Text('Without Icons', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        const Wrap(
          spacing: GHTokens.spacing12,
          runSpacing: GHTokens.spacing12,
          children: [
            GHStatusBadge(status: GHStatusType.open),
            GHStatusBadge(status: GHStatusType.closed),
            GHStatusBadge(status: GHStatusType.merged),
            GHStatusBadge(status: GHStatusType.draft),
          ],
        ),
      ],
    );
  }

  Widget _buildTextFieldSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Form Inputs', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHTextField(
          labelText: 'Repository Name',
          hintText: 'Enter repository name',
          helperText: 'Choose a unique name for your repository',
          required: true,
          onChanged: (value) {
            setState(() {
              _textFieldValue = value;
            });
          },
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHTextField(
          labelText: 'Description',
          hintText: 'Brief description of your repository',
          maxLines: 3,
          minLines: 3,
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHTextField(
          labelText: 'Password',
          hintText: 'Enter your password',
          obscureText: true,
          prefixIcon: Icons.lock,
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHTextField(
          labelText: 'Email',
          hintText: 'Enter your email address',
          keyboardType: TextInputType.emailAddress,
          prefixIcon: Icons.email,
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHTextField(
          labelText: 'Error State',
          hintText: 'This field has an error',
          errorText: 'This field is required',
          prefixIcon: Icons.error,
        ),

        const SizedBox(height: GHTokens.spacing16),

        const GHTextField(
          labelText: 'Disabled Field',
          hintText: 'This field is disabled',
          enabled: false,
          initialValue: 'Disabled value',
        ),

        if (_textFieldValue.isNotEmpty) ...[
          const SizedBox(height: GHTokens.spacing12),
          Text(
            'Repository name: "$_textFieldValue"',
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildEmptyStateSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Basic Empty States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Repository empty state
        GHCard(
          child: Column(
            children: [
              GHEmptyStates.noRepositories(
                onCreateRepository: () =>
                    _showSnackBar('Create repository tapped'),
              ),
              const SizedBox(height: GHTokens.spacing16),
              const Divider(),
              const SizedBox(height: GHTokens.spacing16),

              // Activity empty state
              GHEmptyStates.noActivity(
                onExplore: () => _showSnackBar('Explore repositories tapped'),
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Search Empty States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHEmptyStates.noSearchResults(
            query: 'flutter-advanced-ui',
            onClearSearch: () => _showSnackBar('Clear search tapped'),
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Context-Specific Empty States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            children: [
              // Issues empty state
              GHEmptyStates.noIssues(
                onCreateIssue: () => _showSnackBar('Create issue tapped'),
              ),
              const SizedBox(height: GHTokens.spacing16),
              const Divider(),
              const SizedBox(height: GHTokens.spacing16),

              // Notifications empty state
              GHEmptyStates.noNotifications(),
              const SizedBox(height: GHTokens.spacing16),
              const Divider(),
              const SizedBox(height: GHTokens.spacing16),

              // Stars empty state
              GHEmptyStates.noStarredRepos(
                onExplore: () => _showSnackBar('Explore repositories tapped'),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildErrorStateSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Basic Error States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Network error
        GHCard(
          child: GHErrorStates.networkError(
            onRetry: () => _showSnackBar('Network retry tapped'),
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Repository Error States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHErrorStates.repositoryLoadError(
            onRetry: () => _showSnackBar('Repository retry tapped'),
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Permission Error States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHErrorStates.forbiddenError(
            onRetry: () => _showSnackBar('Request access tapped'),
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Additional Error States', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            children: [
              // Search error
              GHErrorStates.searchError(
                query: 'flutter-ui-toolkit',
                onRetry: () => _showSnackBar('Search retry tapped'),
              ),
              const SizedBox(height: GHTokens.spacing16),
              const Divider(),
              const SizedBox(height: GHTokens.spacing16),

              // Authentication error
              GHErrorStates.authenticationError(
                onRetry: () => _showSnackBar('Sign in again tapped'),
              ),
              const SizedBox(height: GHTokens.spacing16),
              const Divider(),
              const SizedBox(height: GHTokens.spacing16),

              // Rate limit error
              GHErrorStates.rateLimitError(
                onRetry: () => _showSnackBar('Try again later tapped'),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildLoadingIndicatorSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Basic Loading Indicators', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Column(
                    children: [
                      const GHLoadingIndicator(),
                      const SizedBox(height: GHTokens.spacing8),
                      Text('Default', style: GHTokens.labelMedium),
                    ],
                  ),
                  Column(
                    children: [
                      const GHLoadingIndicator.large(),
                      const SizedBox(height: GHTokens.spacing8),
                      Text('Large', style: GHTokens.labelMedium),
                    ],
                  ),
                  Column(
                    children: [
                      const GHLoadingIndicator.small(),
                      const SizedBox(height: GHTokens.spacing8),
                      Text('Small', style: GHTokens.labelMedium),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Loading with Messages', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            children: [
              const GHLoadingIndicator.large(
                label: 'Loading repositories...',
                centered: true,
              ),
              const SizedBox(height: GHTokens.spacing24),
              const Divider(),
              const SizedBox(height: GHTokens.spacing24),
              const GHLoadingIndicator.large(
                label: 'Processing request...',
                centered: true,
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Interactive Example', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            children: [
              ElevatedButton(
                onPressed: () async {
                  setState(() => _showLoadingIndicator = true);
                  await Future.delayed(const Duration(seconds: 2));
                  setState(() => _showLoadingIndicator = false);
                  _showSnackBar('Loading completed!');
                },
                child: const Text('Trigger Loading'),
              ),
              const SizedBox(height: GHTokens.spacing16),
              if (_showLoadingIndicator) ...[
                const GHLoadingIndicator.large(
                  label: 'Loading data...',
                  centered: true,
                ),
              ] else ...[
                Text(
                  'Click the button to see loading indicator',
                  style: GHTokens.bodyMedium.copyWith(
                    color: Theme.of(context).colorScheme.onSurfaceVariant,
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildCardVariantsSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Card Padding Variants', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Default card
        GHCard(
          onTap: () => _showSnackBar('Default card tapped'),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Default Card (16dp padding)', style: GHTokens.titleSmall),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This is the standard card with 16dp padding for general content. Click to test interaction.',
                style: GHTokens.bodyMedium,
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Compact card
        GHCard.compact(
          onTap: () => _showSnackBar('Compact card tapped'),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Compact Card (12dp padding)', style: GHTokens.titleSmall),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This is a compact card with 12dp padding for secondary content. Perfect for lists.',
                style: GHTokens.bodyMedium,
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Tight card
        GHCard.tight(
          onTap: () => _showSnackBar('Tight card tapped'),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Tight Card (8dp padding)', style: GHTokens.titleSmall),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'This is a tight card with 8dp padding for dense content like metrics.',
                style: GHTokens.bodyMedium,
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Zero padding card with ListTile
        GHCard.zeroPadding(
          child: Column(
            children: [
              ListTile(
                leading: const Icon(Icons.person),
                title: const Text('Zero Padding Card'),
                subtitle: const Text(
                  'Perfect for ListTile and self-padded content',
                ),
                trailing: const Icon(Icons.chevron_right),
                onTap: () =>
                    _showSnackBar('ListTile in zero padding card tapped'),
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.settings),
                title: const Text('Another Item'),
                subtitle: const Text('Shows how multiple items work together'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showSnackBar('Second item tapped'),
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Card Usage Examples', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        Row(
          children: [
            Expanded(
              child: GHCard.tight(
                child: Column(
                  children: [
                    Text('1.2k', style: GHTokens.titleLarge),
                    Text('Stars', style: GHTokens.labelMedium),
                  ],
                ),
              ),
            ),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: GHCard.tight(
                child: Column(
                  children: [
                    Text('456', style: GHTokens.titleLarge),
                    Text('Forks', style: GHTokens.labelMedium),
                  ],
                ),
              ),
            ),
            const SizedBox(width: GHTokens.spacing8),
            Expanded(
              child: GHCard.tight(
                child: Column(
                  children: [
                    Text('89', style: GHTokens.titleLarge),
                    Text('Issues', style: GHTokens.labelMedium),
                  ],
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildContentTemplateSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Content Template Example', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        // Content template in a card for better visibility
        GHCard.zeroPadding(
          child: SizedBox(
            height: 400,
            child: GHContentTemplate(
              sections: [
                GHContentSection(
                  title: 'Repository Header',
                  content: Container(
                    padding: const EdgeInsets.all(GHTokens.spacing16),
                    decoration: BoxDecoration(
                      color: Theme.of(
                        context,
                      ).colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(GHTokens.radius8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('flutter/flutter', style: GHTokens.titleMedium),
                        const SizedBox(height: GHTokens.spacing4),
                        Text(
                          'Flutter makes it easy to build beautiful UIs.',
                          style: GHTokens.bodyMedium.copyWith(
                            color: Theme.of(
                              context,
                            ).colorScheme.onSurfaceVariant,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                GHContentSection(
                  title: 'Actions',
                  content: Row(
                    children: [
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () => _showSnackBar('Star tapped'),
                          icon: const Icon(Icons.star_border),
                          label: const Text('Star'),
                        ),
                      ),
                      const SizedBox(width: GHTokens.spacing8),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () => _showSnackBar('Fork tapped'),
                          icon: const Icon(Icons.fork_right),
                          label: const Text('Fork'),
                        ),
                      ),
                    ],
                  ),
                ),
                GHContentSection(
                  title: 'Statistics',
                  content: Container(
                    padding: const EdgeInsets.all(GHTokens.spacing12),
                    decoration: BoxDecoration(
                      color: Theme.of(
                        context,
                      ).colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(GHTokens.radius4),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _buildStat('155k', 'Stars'),
                        _buildStat('25.2k', 'Forks'),
                        _buildStat('3.8k', 'Issues'),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildStat(String value, String label) {
    return Column(
      children: [
        Text(value, style: GHTokens.titleMedium),
        Text(
          label,
          style: GHTokens.labelSmall.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildContentMetadataSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Standard Metadata', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHContentMetadata(
            title: 'Repository Information',
            items: [
              const GHMetadataItem(
                icon: Icons.person,
                label: 'Owner',
                value: 'flutter',
              ),
              const GHMetadataItem(
                icon: Icons.schedule,
                label: 'Updated',
                value: '2 hours ago',
              ),
              GHMetadataItem(
                icon: Icons.link,
                label: 'Website',
                value: 'flutter.dev',
                isLink: true,
                onTap: () => _showSnackBar('Website tapped'),
              ),
              GHMetadataItem(
                icon: Icons.balance,
                label: 'License',
                value: 'BSD-3-Clause',
                onTap: () => _showSnackBar('License tapped'),
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Metadata with Dividers', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHContentMetadata(
            showDividers: true,
            items: const [
              GHMetadataItem(
                icon: Icons.folder,
                label: 'Size',
                value: '124.5 MB',
              ),
              GHMetadataItem(
                icon: Icons.code,
                label: 'Language',
                value: 'Dart',
              ),
              GHMetadataItem(
                icon: Icons.bug_report,
                label: 'Issues',
                value: '3,847 open',
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Metadata Chips', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              GHMetadataChips(
                title: 'Topics',
                items: const [
                  GHMetadataItem(
                    icon: Icons.mobile_friendly,
                    label: 'mobile',
                    value: 'mobile',
                  ),
                  GHMetadataItem(icon: Icons.web, label: 'web', value: 'web'),
                  GHMetadataItem(
                    icon: Icons.desktop_mac,
                    label: 'desktop',
                    value: 'desktop',
                  ),
                  GHMetadataItem(
                    icon: Icons.code,
                    label: 'ui-toolkit',
                    value: 'ui-toolkit',
                  ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing16),
              GHMetadataChips(
                title: 'Technologies',
                items: const [
                  GHMetadataItem(label: 'dart', value: 'Dart'),
                  GHMetadataItem(label: 'flutter', value: 'Flutter'),
                  GHMetadataItem(label: 'material', value: 'Material Design'),
                  GHMetadataItem(label: 'cupertino', value: 'Cupertino'),
                ],
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing16),
        Text('Interactive Metadata', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing12),

        GHCard(
          child: GHContentMetadata(
            items: [
              GHMetadataItem(
                icon: Icons.link,
                label: 'Homepage',
                value: 'flutter.dev',
                isLink: true,
                onTap: () => _showSnackBar('Homepage link tapped'),
              ),
              GHMetadataItem(
                icon: Icons.bug_report,
                label: 'Report Issue',
                value: 'Submit a bug report',
                onTap: () => _showSnackBar('Report issue tapped'),
              ),
              GHMetadataItem(
                icon: Icons.help,
                label: 'Documentation',
                value: 'View docs',
                onTap: () => _showSnackBar('Documentation tapped'),
              ),
            ],
          ),
        ),
      ],
    );
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), duration: const Duration(seconds: 2)),
    );
  }
}
