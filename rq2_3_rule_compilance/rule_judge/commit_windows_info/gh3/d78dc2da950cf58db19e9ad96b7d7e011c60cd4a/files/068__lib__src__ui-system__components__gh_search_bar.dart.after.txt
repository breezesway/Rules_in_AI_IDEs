import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled search bar component with consistent design.
///
/// This component provides a search input field with GitHub-specific
/// styling, placeholder text, and search functionality.
class GHSearchBar extends StatefulWidget {
  /// Placeholder text to display when the search field is empty
  final String hintText;

  /// Callback when the search text changes
  final ValueChanged<String>? onChanged;

  /// Callback when the search is submitted
  final ValueChanged<String>? onSubmitted;

  /// Initial value for the search field
  final String? initialValue;

  /// Whether the search bar is enabled
  final bool enabled;

  /// Custom prefix icon
  final IconData? prefixIcon;

  /// Custom suffix icon
  final IconData? suffixIcon;

  /// Callback when suffix icon is tapped
  final VoidCallback? onSuffixIconTap;

  const GHSearchBar({
    super.key,
    required this.hintText,
    this.onChanged,
    this.onSubmitted,
    this.initialValue,
    this.enabled = true,
    this.prefixIcon,
    this.suffixIcon,
    this.onSuffixIconTap,
  });

  @override
  State<GHSearchBar> createState() => _GHSearchBarState();
}

class _GHSearchBarState extends State<GHSearchBar> {
  late final TextEditingController _controller;
  bool _hasText = false;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.initialValue);
    _hasText = _controller.text.isNotEmpty;
    _controller.addListener(_onTextChanged);
  }

  @override
  void dispose() {
    _controller.removeListener(_onTextChanged);
    _controller.dispose();
    super.dispose();
  }

  void _onTextChanged() {
    final hasText = _controller.text.isNotEmpty;
    if (hasText != _hasText) {
      setState(() {
        _hasText = hasText;
      });
    }
    widget.onChanged?.call(_controller.text);
  }

  void _clearText() {
    _controller.clear();
    widget.onChanged?.call('');
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Container(
      height: GHTokens.minTouchTarget,
      decoration: BoxDecoration(
        color: theme.colorScheme.surface,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        border: Border.all(color: theme.colorScheme.outline, width: 1),
      ),
      child: TextField(
        controller: _controller,
        enabled: widget.enabled,
        onSubmitted: widget.onSubmitted,
        style: GHTokens.bodyMedium,
        decoration: InputDecoration(
          hintText: widget.hintText,
          hintStyle: GHTokens.bodyMedium.copyWith(
            color: theme.colorScheme.onSurfaceVariant,
          ),
          prefixIcon: Icon(
            widget.prefixIcon ?? Icons.search,
            size: GHTokens.iconSize18,
            color: theme.colorScheme.onSurfaceVariant,
          ),
          suffixIcon: _buildSuffixIcon(theme),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing16,
            vertical: GHTokens.spacing12,
          ),
        ),
      ),
    );
  }

  Widget? _buildSuffixIcon(ThemeData theme) {
    if (widget.suffixIcon != null) {
      return IconButton(
        icon: Icon(
          widget.suffixIcon,
          size: GHTokens.iconSize18,
          color: theme.colorScheme.onSurfaceVariant,
        ),
        onPressed: widget.onSuffixIconTap,
        padding: const EdgeInsets.all(GHTokens.spacing8),
        constraints: const BoxConstraints(
          minWidth: GHTokens.iconSize32,
          minHeight: GHTokens.iconSize32,
        ),
      );
    }

    if (_hasText) {
      return IconButton(
        icon: Icon(
          Icons.clear,
          size: GHTokens.iconSize18,
          color: theme.colorScheme.onSurfaceVariant,
        ),
        onPressed: _clearText,
        padding: const EdgeInsets.all(GHTokens.spacing8),
        constraints: const BoxConstraints(
          minWidth: GHTokens.iconSize32,
          minHeight: GHTokens.iconSize32,
        ),
      );
    }

    return null;
  }
}
