import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../components/gh_card.dart';
import '../components/gh_button.dart';
import '../components/gh_chip.dart';
import '../components/gh_text_field.dart';
import '../state_widgets/gh_empty_state.dart';
import '../state_widgets/gh_error_state.dart';
import '../state_widgets/gh_loading_indicator.dart';
import '../layouts/gh_screen_template.dart';

/// Interactive demo screen for comprehensive component state management.
///
/// This screen provides interactive controls to demonstrate various
/// component states, loading scenarios, and user interactions.
class InteractiveComponentDemoScreen extends StatefulWidget {
  const InteractiveComponentDemoScreen({super.key});

  @override
  State<InteractiveComponentDemoScreen> createState() =>
      _InteractiveComponentDemoScreenState();
}

class _InteractiveComponentDemoScreenState
    extends State<InteractiveComponentDemoScreen> {
  // State management variables
  bool _isButtonLoading = false;
  bool _showLoadingState = false;
  bool _showErrorState = false;
  bool _showEmptyState = false;
  bool _isChipSelected = false;
  String _textFieldValue = '';
  String _selectedDemo = 'buttons';

  // Demo scenarios
  final List<String> _demoOptions = [
    'buttons',
    'forms',
    'states',
    'interactions',
  ];

  @override
  Widget build(BuildContext context) {
    return GHScreenTemplate(
      title: 'Interactive Demo Controls',
      body: Column(
        children: [
          // Demo selector
          _buildDemoSelector(),
          const SizedBox(height: GHTokens.spacing20),

          // Interactive content
          Expanded(child: _buildSelectedDemo()),
        ],
      ),
    );
  }

  Widget _buildDemoSelector() {
    return GHCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Demo Categories', style: GHTokens.titleMedium),
          const SizedBox(height: GHTokens.spacing12),

          Wrap(
            spacing: GHTokens.spacing8,
            children: _demoOptions
                .map(
                  (option) => GHChip(
                    label: _getDemoLabel(option),
                    isSelected: _selectedDemo == option,
                    onTap: () {
                      setState(() {
                        _selectedDemo = option;
                      });
                    },
                  ),
                )
                .toList(),
          ),
        ],
      ),
    );
  }

  String _getDemoLabel(String option) {
    switch (option) {
      case 'buttons':
        return 'Button States';
      case 'forms':
        return 'Form Components';
      case 'states':
        return 'App States';
      case 'interactions':
        return 'User Interactions';
      default:
        return option;
    }
  }

  Widget _buildSelectedDemo() {
    switch (_selectedDemo) {
      case 'buttons':
        return _buildButtonDemo();
      case 'forms':
        return _buildFormDemo();
      case 'states':
        return _buildStateDemo();
      case 'interactions':
        return _buildInteractionDemo();
      default:
        return _buildButtonDemo();
    }
  }

  Widget _buildButtonDemo() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Controls section
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Button State Controls', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing12),

                GHButton(
                  label: _isButtonLoading ? 'Stop Loading' : 'Start Loading',
                  style: GHButtonStyle.secondary,
                  onPressed: () {
                    setState(() {
                      _isButtonLoading = !_isButtonLoading;
                    });
                  },
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing20),

          // Button examples
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Button Variants', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing16),

                // Primary buttons
                Text('Primary Buttons', style: GHTokens.labelLarge),
                const SizedBox(height: GHTokens.spacing8),

                Wrap(
                  spacing: GHTokens.spacing8,
                  runSpacing: GHTokens.spacing8,
                  children: [
                    GHButton(
                      label: 'Normal',
                      style: GHButtonStyle.primary,
                      onPressed: () => _showSnackBar('Primary button pressed'),
                    ),
                    GHButton(
                      label: 'Loading',
                      style: GHButtonStyle.primary,
                      isLoading: _isButtonLoading,
                      onPressed: _isButtonLoading
                          ? null
                          : () => _showSnackBar('Loading button pressed'),
                    ),
                    GHButton(
                      label: 'Disabled',
                      style: GHButtonStyle.primary,
                      onPressed: null,
                    ),
                    GHButton(
                      label: 'With Icon',
                      style: GHButtonStyle.primary,
                      icon: Icons.star,
                      onPressed: () => _showSnackBar('Icon button pressed'),
                    ),
                  ],
                ),

                const SizedBox(height: GHTokens.spacing20),

                // Secondary buttons
                Text('Secondary Buttons', style: GHTokens.labelLarge),
                const SizedBox(height: GHTokens.spacing8),

                Wrap(
                  spacing: GHTokens.spacing8,
                  runSpacing: GHTokens.spacing8,
                  children: [
                    GHButton(
                      label: 'Normal',
                      style: GHButtonStyle.secondary,
                      onPressed: () =>
                          _showSnackBar('Secondary button pressed'),
                    ),
                    GHButton(
                      label: 'Loading',
                      style: GHButtonStyle.secondary,
                      isLoading: _isButtonLoading,
                      onPressed: _isButtonLoading
                          ? null
                          : () => _showSnackBar('Loading button pressed'),
                    ),
                    GHButton(
                      label: 'Disabled',
                      style: GHButtonStyle.secondary,
                      onPressed: null,
                    ),
                    GHButton(
                      label: 'With Icon',
                      style: GHButtonStyle.secondary,
                      icon: Icons.share,
                      onPressed: () => _showSnackBar('Share button pressed'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFormDemo() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Form controls
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Form Component Controls', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing12),

                Text(
                  'Current value: "$_textFieldValue"',
                  style: GHTokens.bodyMedium,
                ),
                const SizedBox(height: GHTokens.spacing8),

                GHButton(
                  label: 'Clear Field',
                  style: GHButtonStyle.secondary,
                  onPressed: () {
                    setState(() {
                      _textFieldValue = '';
                    });
                  },
                ),
              ],
            ),
          ),

          const SizedBox(height: GHTokens.spacing20),

          // Form examples
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Form Components', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing16),

                // Text fields
                GHTextField(
                  labelText: 'Username',
                  hintText: 'Enter your username',
                  initialValue: _textFieldValue,
                  onChanged: (value) {
                    setState(() {
                      _textFieldValue = value;
                    });
                  },
                ),

                const SizedBox(height: GHTokens.spacing16),

                GHTextField(
                  labelText: 'Email',
                  hintText: 'Enter your email',
                  keyboardType: TextInputType.emailAddress,
                  onChanged: (value) {},
                ),

                const SizedBox(height: GHTokens.spacing16),

                GHTextField(
                  labelText: 'Password',
                  hintText: 'Enter your password',
                  obscureText: true,
                  onChanged: (value) {},
                ),

                const SizedBox(height: GHTokens.spacing20),

                // Chips
                Text('Interactive Chips', style: GHTokens.labelLarge),
                const SizedBox(height: GHTokens.spacing8),

                Wrap(
                  spacing: GHTokens.spacing8,
                  children: [
                    GHChip(
                      label: 'Selectable',
                      isSelected: _isChipSelected,
                      onTap: () {
                        setState(() {
                          _isChipSelected = !_isChipSelected;
                        });
                      },
                    ),
                    GHChip(
                      label: 'Non-selectable',
                      isSelectable: false,
                      onTap: () => _showSnackBar('Non-selectable chip tapped'),
                    ),
                    GHChip(
                      label: 'With Count',
                      count: 42,
                      onTap: () => _showSnackBar('Count chip tapped'),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStateDemo() {
    return Column(
      children: [
        // State controls
        GHCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('App State Controls', style: GHTokens.titleMedium),
              const SizedBox(height: GHTokens.spacing12),

              Wrap(
                spacing: GHTokens.spacing8,
                children: [
                  GHButton(
                    label: 'Normal',
                    style:
                        _showLoadingState || _showErrorState || _showEmptyState
                        ? GHButtonStyle.secondary
                        : GHButtonStyle.primary,
                    onPressed: () {
                      setState(() {
                        _showLoadingState = false;
                        _showErrorState = false;
                        _showEmptyState = false;
                      });
                    },
                  ),
                  GHButton(
                    label: 'Loading',
                    style: _showLoadingState
                        ? GHButtonStyle.primary
                        : GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _showLoadingState = true;
                        _showErrorState = false;
                        _showEmptyState = false;
                      });
                    },
                  ),
                  GHButton(
                    label: 'Error',
                    style: _showErrorState
                        ? GHButtonStyle.primary
                        : GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _showLoadingState = false;
                        _showErrorState = true;
                        _showEmptyState = false;
                      });
                    },
                  ),
                  GHButton(
                    label: 'Empty',
                    style: _showEmptyState
                        ? GHButtonStyle.primary
                        : GHButtonStyle.secondary,
                    onPressed: () {
                      setState(() {
                        _showLoadingState = false;
                        _showErrorState = false;
                        _showEmptyState = true;
                      });
                    },
                  ),
                ],
              ),
            ],
          ),
        ),

        const SizedBox(height: GHTokens.spacing20),

        // State demonstration
        Expanded(child: GHCard(child: _buildCurrentState())),
      ],
    );
  }

  Widget _buildCurrentState() {
    if (_showLoadingState) {
      return const Center(
        child: GHLoadingIndicator.large(
          label: 'Loading repositories...',
          centered: true,
        ),
      );
    }

    if (_showErrorState) {
      return GHErrorState(
        title: 'Failed to Load Data',
        message:
            'Unable to fetch repositories. Please check your connection and try again.',
        onRetry: () {
          setState(() {
            _showErrorState = false;
            _showLoadingState = true;
          });

          // Simulate loading
          Future.delayed(const Duration(seconds: 2), () {
            if (mounted) {
              setState(() {
                _showLoadingState = false;
              });
            }
          });
        },
      );
    }

    if (_showEmptyState) {
      return GHEmptyState(
        icon: Icons.folder_open,
        title: 'No Repositories Found',
        subtitle:
            'You don\'t have any repositories yet. Create your first repository to get started.',
        action: GHButton(
          label: 'Create Repository',
          style: GHButtonStyle.primary,
          icon: Icons.add,
          onPressed: () {
            setState(() {
              _showEmptyState = false;
            });
            _showSnackBar('Repository creation started');
          },
        ),
      );
    }

    // Normal state
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.check_circle, size: 64, color: GHTokens.success),
        const SizedBox(height: GHTokens.spacing16),
        Text('Normal Content State', style: GHTokens.titleLarge),
        const SizedBox(height: GHTokens.spacing8),
        Text(
          'This represents the normal, loaded state of the application.',
          style: GHTokens.bodyMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildInteractionDemo() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          GHCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Interactive Elements', style: GHTokens.titleMedium),
                const SizedBox(height: GHTokens.spacing16),

                // Tappable cards
                Text('Tappable Cards', style: GHTokens.labelLarge),
                const SizedBox(height: GHTokens.spacing8),

                GHCard(
                  onTap: () => _showSnackBar('Card 1 tapped'),
                  child: ListTile(
                    leading: const Icon(Icons.folder),
                    title: const Text('Interactive Card 1'),
                    subtitle: const Text('Tap to see interaction feedback'),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                ),

                const SizedBox(height: GHTokens.spacing8),

                GHCard(
                  onTap: () => _showSnackBar('Card 2 tapped'),
                  child: ListTile(
                    leading: const Icon(Icons.star),
                    title: const Text('Interactive Card 2'),
                    subtitle: const Text('Another tappable card example'),
                    trailing: const Icon(Icons.chevron_right),
                  ),
                ),

                const SizedBox(height: GHTokens.spacing20),

                // Interactive feedback
                Text('Interaction Feedback', style: GHTokens.labelLarge),
                const SizedBox(height: GHTokens.spacing8),

                Row(
                  children: [
                    Expanded(
                      child: GHButton(
                        label: 'Show Success',
                        style: GHButtonStyle.secondary,
                        onPressed: () =>
                            _showSnackBar('✅ Success message', isSuccess: true),
                      ),
                    ),
                    const SizedBox(width: GHTokens.spacing8),
                    Expanded(
                      child: GHButton(
                        label: 'Show Error',
                        style: GHButtonStyle.secondary,
                        onPressed: () =>
                            _showSnackBar('❌ Error message', isError: true),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: GHTokens.spacing8),

                Row(
                  children: [
                    Expanded(
                      child: GHButton(
                        label: 'Show Info',
                        style: GHButtonStyle.secondary,
                        onPressed: () =>
                            _showSnackBar('ℹ️ Information message'),
                      ),
                    ),
                    const SizedBox(width: GHTokens.spacing8),
                    Expanded(
                      child: GHButton(
                        label: 'Show Warning',
                        style: GHButtonStyle.secondary,
                        onPressed: () => _showSnackBar(
                          '⚠️ Warning message',
                          isWarning: true,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  void _showSnackBar(
    String message, {
    bool isSuccess = false,
    bool isError = false,
    bool isWarning = false,
  }) {
    Color backgroundColor;
    Color textColor;

    if (isSuccess) {
      backgroundColor = GHTokens.success;
      textColor = Colors.white;
    } else if (isError) {
      backgroundColor = GHTokens.error;
      textColor = Colors.white;
    } else if (isWarning) {
      backgroundColor = GHTokens.warning;
      textColor = Colors.white;
    } else {
      backgroundColor = Theme.of(context).colorScheme.inverseSurface;
      textColor = Theme.of(context).colorScheme.onInverseSurface;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message, style: TextStyle(color: textColor)),
        backgroundColor: backgroundColor,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 2),
      ),
    );
  }
}
