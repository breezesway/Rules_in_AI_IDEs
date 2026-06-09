import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled text field component with consistent form styling.
///
/// This component provides a text input field with GitHub-specific
/// styling, validation states, and proper accessibility support.
class GHTextField extends StatefulWidget {
  /// The label text to display above the field
  final String? labelText;

  /// Placeholder text to display when the field is empty
  final String? hintText;

  /// Help text to display below the field
  final String? helperText;

  /// Error text to display when validation fails
  final String? errorText;

  /// Initial value for the text field
  final String? initialValue;

  /// Callback when the text changes
  final ValueChanged<String>? onChanged;

  /// Callback when the field is submitted
  final ValueChanged<String>? onSubmitted;

  /// Whether the field is enabled
  final bool enabled;

  /// Whether the field is required
  final bool required;

  /// Whether to obscure the text (for passwords)
  final bool obscureText;

  /// Maximum number of lines (null for unlimited)
  final int? maxLines;

  /// Minimum number of lines
  final int minLines;

  /// Custom prefix icon
  final IconData? prefixIcon;

  /// Custom suffix icon
  final IconData? suffixIcon;

  /// Callback when suffix icon is tapped
  final VoidCallback? onSuffixIconTap;

  /// Text input type
  final TextInputType keyboardType;

  const GHTextField({
    super.key,
    this.labelText,
    this.hintText,
    this.helperText,
    this.errorText,
    this.initialValue,
    this.onChanged,
    this.onSubmitted,
    this.enabled = true,
    this.required = false,
    this.obscureText = false,
    this.maxLines = 1,
    this.minLines = 1,
    this.prefixIcon,
    this.suffixIcon,
    this.onSuffixIconTap,
    this.keyboardType = TextInputType.text,
  });

  @override
  State<GHTextField> createState() => _GHTextFieldState();
}

class _GHTextFieldState extends State<GHTextField> {
  late final TextEditingController _controller;
  bool _obscureText = false;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.initialValue);
    _obscureText = widget.obscureText;
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _toggleObscureText() {
    setState(() {
      _obscureText = !_obscureText;
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final hasError = widget.errorText != null;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (widget.labelText != null) ...[
          Row(
            children: [
              Text(
                widget.labelText!,
                style: GHTokens.labelLarge.copyWith(
                  color: theme.colorScheme.onSurface,
                ),
              ),
              if (widget.required) ...[
                const SizedBox(width: GHTokens.spacing4),
                Text(
                  '*',
                  style: GHTokens.labelLarge.copyWith(
                    color: theme.colorScheme.error,
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: GHTokens.spacing8),
        ],
        TextField(
          controller: _controller,
          enabled: widget.enabled,
          obscureText: _obscureText,
          maxLines: widget.maxLines,
          minLines: widget.minLines,
          keyboardType: widget.keyboardType,
          onChanged: widget.onChanged,
          onSubmitted: widget.onSubmitted,
          style: GHTokens.bodyMedium,
          decoration: InputDecoration(
            hintText: widget.hintText,
            hintStyle: GHTokens.bodyMedium.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
            prefixIcon: widget.prefixIcon != null
                ? Icon(
                    widget.prefixIcon,
                    size: GHTokens.iconSize18,
                    color: theme.colorScheme.onSurfaceVariant,
                  )
                : null,
            suffixIcon: _buildSuffixIcon(theme),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
              borderSide: BorderSide(
                color: hasError
                    ? theme.colorScheme.error
                    : theme.colorScheme.outline,
              ),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
              borderSide: BorderSide(
                color: hasError
                    ? theme.colorScheme.error
                    : theme.colorScheme.primary,
                width: 2,
              ),
            ),
            errorBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(GHTokens.radius8),
              borderSide: BorderSide(color: theme.colorScheme.error),
            ),
            contentPadding: const EdgeInsets.symmetric(
              horizontal: GHTokens.spacing16,
              vertical: GHTokens.spacing12,
            ),
          ),
        ),
        if (widget.errorText != null) ...[
          const SizedBox(height: GHTokens.spacing4),
          Text(
            widget.errorText!,
            style: GHTokens.labelMedium.copyWith(
              color: theme.colorScheme.error,
            ),
          ),
        ] else if (widget.helperText != null) ...[
          const SizedBox(height: GHTokens.spacing4),
          Text(
            widget.helperText!,
            style: GHTokens.labelMedium.copyWith(
              color: theme.colorScheme.onSurfaceVariant,
            ),
          ),
        ],
      ],
    );
  }

  Widget? _buildSuffixIcon(ThemeData theme) {
    if (widget.obscureText) {
      return IconButton(
        icon: Icon(
          _obscureText ? Icons.visibility : Icons.visibility_off,
          size: GHTokens.iconSize18,
          color: theme.colorScheme.onSurfaceVariant,
        ),
        onPressed: _toggleObscureText,
        padding: const EdgeInsets.all(GHTokens.spacing8),
        constraints: const BoxConstraints(
          minWidth: GHTokens.iconSize32,
          minHeight: GHTokens.iconSize32,
        ),
      );
    }

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

    return null;
  }
}
