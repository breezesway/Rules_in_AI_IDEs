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
import '../utils/color_utils.dart';

/// **REFERENCE IMPLEMENTATION** - Interactive Examples Screen
///
/// This screen serves as the primary reference implementation for advanced
/// interaction patterns and state management in the GH3 design system. It demonstrates:
///
/// - Complex state management with multiple interactive components
/// - Animation integration with proper duration and curves
/// - Error handling and state transitions
/// - Form input patterns with validation
/// - Real-world GitHub application scenarios
/// - Proper loading, empty, and error state implementations
///
/// **Usage as Reference:**
/// - Copy state management patterns from this file
/// - Follow the animation implementation approaches
/// - Use the error handling strategies demonstrated
/// - Maintain the same interaction feedback patterns
/// - Reference the form validation implementations
///
/// This screen demonstrates proper usage patterns and different configurations
/// of UI components with practical examples from the GitHub application context.
class InteractiveExamplesScreen extends StatefulWidget {
  const InteractiveExamplesScreen({super.key});

  @override
  State<InteractiveExamplesScreen> createState() =>
      _InteractiveExamplesScreenState();
}

class _InteractiveExamplesScreenState extends State<InteractiveExamplesScreen>
    with TickerProviderStateMixin {
  // State management for interactive examples
  final Set<String> _selectedFilters = {};
  String _searchQuery = '';
  String _repositoryName = '';
  String _repositoryDescription = '';
  bool _isPrivate = false;
  bool _isTemplate = false;
  bool _includeReadme = true;
  GHStatusType _issueStatus = GHStatusType.open;
  String _selectedLanguage = 'Dart';
  bool _isStarred = false;
  int _starCount = 1234;
  bool _isLoading = false;
  bool _showEmptyState = false;
  bool _showErrorState = false;
  String _errorType = 'network';

  // Animation controllers
  late AnimationController _fadeController;
  late AnimationController _slideController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    // REFERENCE PATTERN: Animation controllers for smooth UI transitions
    // Use 300ms for subtle animations, 500ms for more prominent transitions
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _slideController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _fadeAnimation = CurvedAnimation(
      parent: _fadeController,
      curve: Curves.easeInOut,
    );
    _slideAnimation =
        Tween<Offset>(begin: const Offset(0.0, 0.1), end: Offset.zero).animate(
          CurvedAnimation(parent: _slideController, curve: Curves.easeOutCubic),
        );
    _fadeController.forward();
    _slideController.forward();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    _slideController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // REFERENCE PATTERN: GHScreenTemplate with action buttons for screen controls
    return GHScreenTemplate(
      title: 'Interactive Component Examples',
      actions: [
        // REFERENCE PATTERN: Action buttons for screen-level interactions
        IconButton(
          icon: const Icon(Icons.refresh),
          onPressed: _resetAllStates,
          tooltip: 'Reset all states',
        ),
      ],
      body: SingleChildScrollView(
        // REFERENCE PATTERN: Standard screen padding using spacing tokens
        padding: const EdgeInsets.all(GHTokens.spacing16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionHeader(
              'Real-World Scenarios',
              'Interactive examples showing components in action',
            ),
            _buildScenarioSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader(
              'Repository Creation Flow',
              'Complete form interaction with validation',
            ),
            _buildRepositoryCreationSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader(
              'Issue Management',
              'Status transitions and filtering',
            ),
            _buildIssueManagementSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader(
              'Search & Filter Experience',
              'Advanced search with live filtering',
            ),
            _buildSearchFilterSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader(
              'State Transitions',
              'Loading, empty, and error state demonstrations',
            ),
            _buildStateTransitionsSection(),
            const SizedBox(height: GHTokens.spacing32),

            _buildSectionHeader(
              'Responsive Layouts',
              'Components adapting to different contexts',
            ),
            _buildResponsiveSection(),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title, String subtitle) {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: GHTokens.titleLarge),
          const SizedBox(height: GHTokens.spacing4),
          Text(
            subtitle,
            style: GHTokens.bodyMedium.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: GHTokens.spacing16),
        ],
      ),
    );
  }

  Widget _buildScenarioSection() {
    return SlideTransition(
      position: _slideAnimation,
      child: Column(
        children: [
          // Repository card with interactive star action
          GHCard(
            onTap: () => _showSnackBar('Repository opened'),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: ColorUtils.getLanguageColor(_selectedLanguage),
                        borderRadius: BorderRadius.circular(GHTokens.radius8),
                      ),
                      child: const Icon(Icons.code, color: Colors.white),
                    ),
                    const SizedBox(width: GHTokens.spacing12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text('flutter/', style: GHTokens.bodyMedium),
                              Text('awesome-ui', style: GHTokens.titleMedium),
                              const SizedBox(width: GHTokens.spacing8),
                              if (_isPrivate)
                                const GHStatusBadge(
                                  status: GHStatusType.draft,
                                  customLabel: 'Private',
                                ),
                            ],
                          ),
                          const SizedBox(height: GHTokens.spacing4),
                          Text(
                            'A collection of awesome Flutter UI components',
                            style: GHTokens.bodyMedium.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing16),
                Row(
                  children: [
                    GHChip(
                      label: _selectedLanguage,
                      colorIndicator: ColorUtils.getLanguageColor(
                        _selectedLanguage,
                      ),
                      isSelectable: false,
                    ),
                    const SizedBox(width: GHTokens.spacing8),
                    Icon(
                      Icons.star,
                      size: GHTokens.iconSize16,
                      color: _isStarred ? GHTokens.warning : null,
                    ),
                    const SizedBox(width: GHTokens.spacing4),
                    Text(_starCount.toString(), style: GHTokens.labelMedium),
                    const SizedBox(width: GHTokens.spacing16),
                    const Icon(Icons.fork_right, size: GHTokens.iconSize16),
                    const SizedBox(width: GHTokens.spacing4),
                    const Text('342', style: GHTokens.labelMedium),
                    const Spacer(),
                    GHButton(
                      label: _isStarred ? 'Starred' : 'Star',
                      icon: _isStarred ? Icons.star : Icons.star_border,
                      style: _isStarred
                          ? GHButtonStyle.secondary
                          : GHButtonStyle.primary,
                      onPressed: () {
                        setState(() {
                          _isStarred = !_isStarred;
                          _starCount += _isStarred ? 1 : -1;
                        });
                        _showSnackBar(
                          _isStarred
                              ? 'Repository starred!'
                              : 'Repository unstarred',
                        );
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
          const SizedBox(height: GHTokens.spacing16),

          // User profile card with follow action
          GHCard(
            child: GHListTile(
              leading: CircleAvatar(
                backgroundColor: Theme.of(context).colorScheme.primary,
                child: const Icon(Icons.person, color: Colors.white),
              ),
              title: const Text('Jane Developer'),
              subtitle: const Text('@janedev • 1.2k followers'),
              trailing: GHButton(
                label: 'Follow',
                style: GHButtonStyle.secondary,
                onPressed: () => _showSnackBar('Following user'),
              ),
              onTap: () => _showSnackBar('Profile opened'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRepositoryCreationSection() {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: GHCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Create a new repository', style: GHTokens.titleMedium),
            const SizedBox(height: GHTokens.spacing16),

            GHTextField(
              labelText: 'Repository name',
              hintText: 'my-awesome-project',
              helperText: 'Great repository names are short and memorable.',
              required: true,
              initialValue: _repositoryName,
              onChanged: (value) {
                setState(() {
                  _repositoryName = value;
                });
              },
              errorText: _repositoryName.contains(' ')
                  ? 'Repository names cannot contain spaces'
                  : null,
            ),
            const SizedBox(height: GHTokens.spacing16),

            GHTextField(
              labelText: 'Description',
              hintText: 'Short description of your repository',
              maxLines: 3,
              minLines: 2,
              initialValue: _repositoryDescription,
              onChanged: (value) {
                setState(() {
                  _repositoryDescription = value;
                });
              },
            ),
            const SizedBox(height: GHTokens.spacing16),

            Row(
              children: [
                Checkbox(
                  value: _isPrivate,
                  onChanged: (value) {
                    setState(() {
                      _isPrivate = value ?? false;
                    });
                  },
                ),
                Text('Private repository', style: GHTokens.bodyMedium),
                const SizedBox(width: GHTokens.spacing16),
                Checkbox(
                  value: _isTemplate,
                  onChanged: (value) {
                    setState(() {
                      _isTemplate = value ?? false;
                    });
                  },
                ),
                Text('Template repository', style: GHTokens.bodyMedium),
              ],
            ),
            const SizedBox(height: GHTokens.spacing16),

            Row(
              children: [
                Checkbox(
                  value: _includeReadme,
                  onChanged: (value) {
                    setState(() {
                      _includeReadme = value ?? true;
                    });
                  },
                ),
                Text('Initialize with README', style: GHTokens.bodyMedium),
              ],
            ),
            const SizedBox(height: GHTokens.spacing24),

            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                GHButton(
                  label: 'Cancel',
                  style: GHButtonStyle.secondary,
                  onPressed: () {
                    setState(() {
                      _repositoryName = '';
                      _repositoryDescription = '';
                      _isPrivate = false;
                      _isTemplate = false;
                      _includeReadme = true;
                    });
                  },
                ),
                const SizedBox(width: GHTokens.spacing12),
                GHButton(
                  label: 'Create repository',
                  icon: Icons.add,
                  onPressed:
                      _repositoryName.isNotEmpty &&
                          !_repositoryName.contains(' ')
                      ? () {
                          _showSnackBar(
                            'Repository "$_repositoryName" created!',
                          );
                        }
                      : null,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIssueManagementSection() {
    return Column(
      children: [
        // Issue status selector
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Issue Status', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing12),
              Row(
                children: [
                  Expanded(
                    child: RadioListTile<GHStatusType>(
                      title: const Text('Open'),
                      value: GHStatusType.open,
                      groupValue: _issueStatus,
                      onChanged: (value) {
                        setState(() {
                          _issueStatus = value!;
                        });
                      },
                    ),
                  ),
                  Expanded(
                    child: RadioListTile<GHStatusType>(
                      title: const Text('Closed'),
                      value: GHStatusType.closed,
                      groupValue: _issueStatus,
                      onChanged: (value) {
                        setState(() {
                          _issueStatus = value!;
                        });
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing16),

        // Issue card with dynamic status
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 300),
          child: GHCard(
            key: ValueKey(_issueStatus),
            onTap: () => _showSnackBar('Issue opened'),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(
                      _issueStatus == GHStatusType.open
                          ? Icons.error_outline
                          : Icons.check_circle_outline,
                      color: _issueStatus == GHStatusType.open
                          ? GHTokens.success
                          : GHTokens.error,
                      size: GHTokens.iconSize24,
                    ),
                    const SizedBox(width: GHTokens.spacing12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Add dark mode support #42',
                            style: GHTokens.titleMedium,
                          ),
                          const SizedBox(height: GHTokens.spacing4),
                          Text(
                            _issueStatus == GHStatusType.open
                                ? 'opened 2 hours ago by @johndoe'
                                : 'closed 1 hour ago by @janedoe',
                            style: GHTokens.bodyMedium.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                    GHStatusBadge(status: _issueStatus),
                  ],
                ),
                const SizedBox(height: GHTokens.spacing12),
                Wrap(
                  spacing: GHTokens.spacing8,
                  children: const [
                    GHChip(
                      label: 'enhancement',
                      colorIndicator: Colors.blue,
                      isSelectable: false,
                    ),
                    GHChip(
                      label: 'ui',
                      colorIndicator: Colors.purple,
                      isSelectable: false,
                    ),
                    GHChip(
                      label: 'priority:high',
                      colorIndicator: Colors.orange,
                      isSelectable: false,
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildSearchFilterSection() {
    final filteredLanguages = _searchQuery.isEmpty
        ? ColorUtils.getPopularLanguages()
        : ColorUtils.getPopularLanguages()
              .where(
                (lang) => (lang['language'] as String).toLowerCase().contains(
                  _searchQuery.toLowerCase(),
                ),
              )
              .toList();

    return Column(
      children: [
        // Search bar with live results
        GHSearchBar(
          hintText: 'Search programming languages...',
          onChanged: (value) {
            setState(() {
              _searchQuery = value;
            });
          },
          suffixIcon: _searchQuery.isNotEmpty ? Icons.clear : null,
          onSuffixIconTap: _searchQuery.isNotEmpty
              ? () {
                  setState(() {
                    _searchQuery = '';
                  });
                }
              : null,
        ),
        const SizedBox(height: GHTokens.spacing16),

        // Filter chips
        AnimatedContainer(
          duration: const Duration(milliseconds: 300),
          height: filteredLanguages.isEmpty ? 200 : null,
          child: filteredLanguages.isEmpty
              ? GHEmptyState(
                  icon: Icons.search_off,
                  title: 'No languages found',
                  subtitle: 'Try searching for "Java" or "Python"',
                  action: GHButton(
                    label: 'Clear search',
                    onPressed: () {
                      setState(() {
                        _searchQuery = '';
                      });
                    },
                  ),
                )
              : Wrap(
                  spacing: GHTokens.spacing8,
                  runSpacing: GHTokens.spacing8,
                  children: filteredLanguages.take(12).map((langInfo) {
                    final language = langInfo['language'] as String;
                    final color = langInfo['color'] as Color;
                    final isSelected = _selectedFilters.contains(language);

                    return GHChip(
                      label: language,
                      colorIndicator: color,
                      isSelected: isSelected,
                      onTap: () {
                        setState(() {
                          if (isSelected) {
                            _selectedFilters.remove(language);
                          } else {
                            _selectedFilters.add(language);
                          }
                        });
                      },
                    );
                  }).toList(),
                ),
        ),

        if (_selectedFilters.isNotEmpty) ...[
          const SizedBox(height: GHTokens.spacing16),
          GHCard.compact(
            child: Row(
              children: [
                Icon(
                  Icons.filter_list,
                  size: GHTokens.iconSize18,
                  color: Theme.of(context).colorScheme.primary,
                ),
                const SizedBox(width: GHTokens.spacing8),
                Text(
                  '${_selectedFilters.length} filters active',
                  style: GHTokens.bodyMedium,
                ),
                const Spacer(),
                TextButton(
                  onPressed: () {
                    setState(() {
                      _selectedFilters.clear();
                    });
                  },
                  child: const Text('Clear all'),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  Widget _buildStateTransitionsSection() {
    return Column(
      children: [
        // State selector
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('State Demonstration', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing12),
              Row(
                children: [
                  Expanded(
                    child: GHButton(
                      label: 'Loading',
                      icon: Icons.hourglass_empty,
                      style: _isLoading
                          ? GHButtonStyle.primary
                          : GHButtonStyle.secondary,
                      onPressed: () {
                        setState(() {
                          _isLoading = true;
                          _showEmptyState = false;
                          _showErrorState = false;
                        });
                        Future.delayed(const Duration(seconds: 3), () {
                          if (mounted) {
                            setState(() {
                              _isLoading = false;
                            });
                          }
                        });
                      },
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: GHButton(
                      label: 'Empty',
                      icon: Icons.inbox,
                      style: _showEmptyState
                          ? GHButtonStyle.primary
                          : GHButtonStyle.secondary,
                      onPressed: () {
                        setState(() {
                          _isLoading = false;
                          _showEmptyState = true;
                          _showErrorState = false;
                        });
                      },
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: GHButton(
                      label: 'Error',
                      icon: Icons.error_outline,
                      style: _showErrorState
                          ? GHButtonStyle.primary
                          : GHButtonStyle.secondary,
                      onPressed: () {
                        setState(() {
                          _isLoading = false;
                          _showEmptyState = false;
                          _showErrorState = true;
                        });
                      },
                    ),
                  ),
                ],
              ),
              if (_showErrorState) ...[
                const SizedBox(height: GHTokens.spacing12),
                SegmentedButton<String>(
                  segments: const [
                    ButtonSegment(
                      value: 'network',
                      label: Text('Network'),
                      icon: Icon(Icons.wifi_off),
                    ),
                    ButtonSegment(
                      value: 'permission',
                      label: Text('Permission'),
                      icon: Icon(Icons.lock),
                    ),
                    ButtonSegment(
                      value: 'rate',
                      label: Text('Rate Limit'),
                      icon: Icon(Icons.timer),
                    ),
                  ],
                  selected: {_errorType},
                  onSelectionChanged: (value) {
                    setState(() {
                      _errorType = value.first;
                    });
                  },
                ),
              ],
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing16),

        // State display
        AnimatedSwitcher(
          duration: const Duration(milliseconds: 300),
          child: GHCard(
            key: ValueKey(
              '$_isLoading-$_showEmptyState-$_showErrorState-$_errorType',
            ),
            child: SizedBox(
              height: 300,
              child: Center(
                child: _isLoading
                    ? const GHLoadingIndicator.large(
                        label: 'Loading repositories...',
                        centered: true,
                      )
                    : _showEmptyState
                    ? GHEmptyStates.noRepositories(
                        onCreateRepository: () {
                          _showSnackBar('Create repository clicked');
                        },
                      )
                    : _showErrorState
                    ? _buildErrorForType()
                    : _buildContentState(),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildErrorForType() {
    switch (_errorType) {
      case 'network':
        return GHErrorStates.networkError(
          onRetry: () {
            setState(() {
              _isLoading = true;
              _showErrorState = false;
            });
            Future.delayed(const Duration(seconds: 2), () {
              if (mounted) {
                setState(() {
                  _isLoading = false;
                });
              }
            });
          },
        );
      case 'permission':
        return GHErrorStates.forbiddenError(
          onRetry: () => _showSnackBar('Request access clicked'),
        );
      case 'rate':
        return GHErrorStates.rateLimitError(
          onRetry: () => _showSnackBar('Try again later clicked'),
        );
      default:
        return GHErrorStates.networkError(onRetry: () {});
    }
  }

  Widget _buildContentState() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(
          Icons.check_circle,
          size: 64,
          color: Theme.of(context).colorScheme.primary,
        ),
        const SizedBox(height: GHTokens.spacing16),
        Text('Content loaded successfully!', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing8),
        Text(
          'Your repositories are displayed here',
          style: GHTokens.bodyMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildResponsiveSection() {
    return Column(
      children: [
        // Card variants showcase
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Card Variants in Context', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing16),

              // Metrics row with tight cards
              Row(
                children: [
                  Expanded(
                    child: GHCard.tight(
                      elevation: 0,
                      child: Column(
                        children: [
                          Icon(
                            Icons.star,
                            color: GHTokens.warning,
                            size: GHTokens.iconSize24,
                          ),
                          const SizedBox(height: GHTokens.spacing4),
                          Text('12.5k', style: GHTokens.titleMedium),
                          Text(
                            'Stars',
                            style: GHTokens.labelSmall.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: GHCard.tight(
                      elevation: 0,
                      child: Column(
                        children: [
                          Icon(
                            Icons.fork_right,
                            color: Theme.of(context).colorScheme.primary,
                            size: GHTokens.iconSize24,
                          ),
                          const SizedBox(height: GHTokens.spacing4),
                          Text('3.2k', style: GHTokens.titleMedium),
                          Text(
                            'Forks',
                            style: GHTokens.labelSmall.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: GHTokens.spacing8),
                  Expanded(
                    child: GHCard.tight(
                      elevation: 0,
                      child: Column(
                        children: [
                          Icon(
                            Icons.bug_report,
                            color: GHTokens.success,
                            size: GHTokens.iconSize24,
                          ),
                          const SizedBox(height: GHTokens.spacing4),
                          Text('142', style: GHTokens.titleMedium),
                          Text(
                            'Issues',
                            style: GHTokens.labelSmall.copyWith(
                              color: Theme.of(
                                context,
                              ).colorScheme.onSurfaceVariant,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: GHTokens.spacing16),

        // Content template in action
        GHCard.zeroPadding(
          child: SizedBox(
            height: 400,
            child: GHContentTemplate(
              sections: [
                GHContentSection(
                  title: 'Repository Details',
                  content: Container(
                    padding: const EdgeInsets.all(GHTokens.spacing16),
                    child: GHContentMetadata(
                      items: [
                        const GHMetadataItem(
                          icon: Icons.code,
                          label: 'Language',
                          value: 'Dart',
                        ),
                        GHMetadataItem(
                          icon: Icons.balance,
                          label: 'License',
                          value: 'MIT',
                          onTap: () => _showSnackBar('License details'),
                        ),
                        const GHMetadataItem(
                          icon: Icons.schedule,
                          label: 'Updated',
                          value: '2 hours ago',
                        ),
                      ],
                    ),
                  ),
                ),
                GHContentSection(
                  title: 'Quick Actions',
                  content: Padding(
                    padding: const EdgeInsets.symmetric(
                      horizontal: GHTokens.spacing16,
                    ),
                    child: Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: () => _showSnackBar('Clone repository'),
                            icon: const Icon(Icons.download),
                            label: const Text('Clone'),
                          ),
                        ),
                        const SizedBox(width: GHTokens.spacing8),
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: () => _showSnackBar('Watch repository'),
                            icon: const Icon(Icons.visibility),
                            label: const Text('Watch'),
                          ),
                        ),
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

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
        action: SnackBarAction(label: 'OK', onPressed: () {}),
      ),
    );
  }

  void _resetAllStates() {
    setState(() {
      _selectedFilters.clear();
      _searchQuery = '';
      _repositoryName = '';
      _repositoryDescription = '';
      _isPrivate = false;
      _isTemplate = false;
      _includeReadme = true;
      _issueStatus = GHStatusType.open;
      _selectedLanguage = 'Dart';
      _isStarred = false;
      _starCount = 1234;
      _isLoading = false;
      _showEmptyState = false;
      _showErrorState = false;
      _errorType = 'network';
    });
    _fadeController.forward();
    _slideController.forward();
    _showSnackBar('All states reset to defaults');
  }
}
