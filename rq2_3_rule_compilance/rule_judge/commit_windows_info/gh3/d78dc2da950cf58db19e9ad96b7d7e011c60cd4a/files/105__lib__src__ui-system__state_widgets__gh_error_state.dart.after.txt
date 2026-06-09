import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// A GitHub-styled error state widget with title, message, and retry functionality.
///
/// This widget provides a consistent way to display error states across
/// the application with proper spacing, typography, and retry capabilities.
class GHErrorState extends StatelessWidget {
  /// The main error title
  final String title;

  /// Descriptive error message
  final String message;

  /// Optional retry callback
  final VoidCallback? onRetry;

  /// Whether the retry operation is currently loading
  final bool isRetrying;

  /// Custom icon to display (defaults to error icon)
  final IconData? icon;

  /// Custom icon size (defaults to 64x64dp)
  final double? iconSize;

  /// Custom icon color
  final Color? iconColor;

  /// Custom title style
  final TextStyle? titleStyle;

  /// Custom message style
  final TextStyle? messageStyle;

  /// Whether to center the content
  final bool centered;

  /// Custom padding around the content
  final EdgeInsetsGeometry? padding;

  /// Text for the retry button (defaults to "Retry")
  final String retryButtonText;

  const GHErrorState({
    super.key,
    required this.title,
    required this.message,
    this.onRetry,
    this.isRetrying = false,
    this.icon,
    this.iconSize,
    this.iconColor,
    this.titleStyle,
    this.messageStyle,
    this.centered = true,
    this.padding,
    this.retryButtonText = 'Retry',
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    final content = Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Error Icon
        Icon(
          icon ?? Icons.error_outline,
          size: iconSize ?? 64.0,
          color: iconColor ?? theme.colorScheme.error,
        ),

        const SizedBox(height: GHTokens.spacing16),

        // Error Title
        Text(
          title,
          style:
              titleStyle ??
              GHTokens.headlineMedium.copyWith(
                color: theme.colorScheme.onSurface,
              ),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: GHTokens.spacing8),

        // Error Message
        Text(
          message,
          style:
              messageStyle ??
              GHTokens.bodyMedium.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
          textAlign: TextAlign.center,
        ),

        // Retry Button
        if (onRetry != null) ...[
          const SizedBox(height: GHTokens.spacing24),
          ElevatedButton.icon(
            onPressed: isRetrying ? null : onRetry,
            icon: isRetrying
                ? SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(
                        theme.colorScheme.onPrimary,
                      ),
                    ),
                  )
                : const Icon(Icons.refresh),
            label: Text(isRetrying ? 'Retrying...' : retryButtonText),
          ),
        ],
      ],
    );

    if (centered) {
      return Padding(
        padding: padding ?? const EdgeInsets.all(GHTokens.spacing24),
        child: Center(child: content),
      );
    }

    return Padding(
      padding: padding ?? const EdgeInsets.all(GHTokens.spacing24),
      child: content,
    );
  }
}

/// Predefined error state configurations for common error scenarios.
class GHErrorStates {
  const GHErrorStates._();

  /// Network connection error
  static GHErrorState networkError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.wifi_off_outlined,
      title: 'Connection Error',
      message:
          'Unable to connect to GitHub. Please check your internet connection and try again.',
      onRetry: onRetry,
    );
  }

  /// Server error (5xx)
  static GHErrorState serverError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.cloud_off_outlined,
      title: 'Server Error',
      message:
          'GitHub servers are currently experiencing issues. Please try again in a few moments.',
      onRetry: onRetry,
    );
  }

  /// Not found error (404)
  static GHErrorState notFoundError({
    String? resourceType,
    VoidCallback? onRetry,
  }) {
    final resource = resourceType ?? 'resource';
    return GHErrorState(
      icon: Icons.search_off_outlined,
      title:
          '${resource.substring(0, 1).toUpperCase()}${resource.substring(1)} Not Found',
      message:
          'The $resource you\'re looking for doesn\'t exist or has been moved.',
      onRetry: onRetry,
    );
  }

  /// Forbidden error (403)
  static GHErrorState forbiddenError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.lock_outlined,
      title: 'Access Denied',
      message:
          'You don\'t have permission to access this resource. Please check your access rights.',
      onRetry: onRetry,
    );
  }

  /// Rate limit exceeded error
  static GHErrorState rateLimitError({
    DateTime? resetTime,
    VoidCallback? onRetry,
  }) {
    String message =
        'You\'ve exceeded the API rate limit. Please wait before making more requests.';
    if (resetTime != null) {
      final now = DateTime.now();
      final difference = resetTime.difference(now);
      if (difference.isNegative) {
        message = 'Rate limit should be reset now. You can try again.';
      } else {
        final minutes = difference.inMinutes;
        final seconds = difference.inSeconds % 60;
        if (minutes > 0) {
          message = 'Rate limit will reset in ${minutes}m ${seconds}s.';
        } else {
          message = 'Rate limit will reset in ${seconds}s.';
        }
      }
    }

    return GHErrorState(
      icon: Icons.hourglass_empty_outlined,
      title: 'Rate Limit Exceeded',
      message: message,
      onRetry: onRetry,
    );
  }

  /// Authentication error
  static GHErrorState authenticationError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.person_off_outlined,
      title: 'Authentication Required',
      message: 'Please sign in to access this content.',
      onRetry: onRetry,
      retryButtonText: 'Sign In',
    );
  }

  /// Repository loading error
  static GHErrorState repositoryLoadError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.folder_off_outlined,
      title: 'Unable to Load Repository',
      message: 'There was a problem loading the repository. Please try again.',
      onRetry: onRetry,
    );
  }

  /// Issues loading error
  static GHErrorState issuesLoadError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.bug_report_outlined,
      title: 'Unable to Load Issues',
      message: 'There was a problem loading the issues. Please try again.',
      onRetry: onRetry,
    );
  }

  /// Pull requests loading error
  static GHErrorState pullRequestsLoadError({VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.merge_type_outlined,
      title: 'Unable to Load Pull Requests',
      message:
          'There was a problem loading the pull requests. Please try again.',
      onRetry: onRetry,
    );
  }

  /// Search error
  static GHErrorState searchError({String? query, VoidCallback? onRetry}) {
    return GHErrorState(
      icon: Icons.search_off_outlined,
      title: 'Search Failed',
      message: query != null
          ? 'Unable to search for "$query". Please try again.'
          : 'Search request failed. Please try again.',
      onRetry: onRetry,
    );
  }

  /// Generic error with custom message
  static GHErrorState genericError({
    required String title,
    required String message,
    IconData? icon,
    VoidCallback? onRetry,
    String retryButtonText = 'Retry',
  }) {
    return GHErrorState(
      icon: icon ?? Icons.error_outline,
      title: title,
      message: message,
      onRetry: onRetry,
      retryButtonText: retryButtonText,
    );
  }
}
