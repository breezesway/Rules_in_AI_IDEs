# Complete Component Library Design

## Overview

This design implements all missing components referenced in the UI system standards, providing comprehensive state management components, card variants, and layout templates. The solution completes the design system with professional-grade components for empty states, error handling, and flexible content layouts.

## State Management Components

### GHEmptyState Component

```dart
class GHEmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? action;
  final double iconSize;
  final Color? iconColor;

  const GHEmptyState({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    this.action,
    this.iconSize = 64.0,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: iconSize,
              color: iconColor ?? theme.colorScheme.onSurfaceVariant,
            ),
            const SizedBox(height: GHTokens.spacing16),
            
            Text(
              title,
              style: GHTokens.headlineMedium.copyWith(
                color: theme.colorScheme.onSurface,
              ),
              textAlign: TextAlign.center,
            ),
            
            if (subtitle != null) ...[
              const SizedBox(height: GHTokens.spacing8),
              Text(
                subtitle!,
                style: GHTokens.bodyLarge.copyWith(
                  color: theme.colorScheme.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
            ],
            
            if (action != null) ...[
              const SizedBox(height: GHTokens.spacing24),
              action!,
            ],
          ],
        ),
      ),
    );
  }
}
```

### GHErrorState Component

```dart
class GHErrorState extends StatelessWidget {
  final String title;
  final String message;
  final VoidCallback? onRetry;
  final String retryLabel;
  final IconData icon;
  final bool isLoading;

  const GHErrorState({
    super.key,
    this.title = 'Something went wrong',
    required this.message,
    this.onRetry,
    this.retryLabel = 'Retry',
    this.icon = Icons.error_outline,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(GHTokens.spacing32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 64.0,
              color: theme.colorScheme.error,
            ),
            const SizedBox(height: GHTokens.spacing16),
            
            Text(
              title,
              style: GHTokens.headlineMedium.copyWith(
                color: theme.colorScheme.onSurface,
              ),
              textAlign: TextAlign.center,
            ),
            
            const SizedBox(height: GHTokens.spacing8),
            Text(
              message,
              style: GHTokens.bodyLarge.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
            
            if (onRetry != null) ...[
              const SizedBox(height: GHTokens.spacing24),
              GHButton(
                label: retryLabel,
                onPressed: isLoading ? null : onRetry,
                isLoading: isLoading,
                icon: Icons.refresh,
                style: GHButtonStyle.primary,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

### Enhanced GHLoadingIndicator

```dart
class GHLoadingIndicator extends StatelessWidget {
  final String? message;
  final double size;
  final Color? color;
  final bool showMessage;

  const GHLoadingIndicator({
    super.key,
    this.message,
    this.size = 24.0,
    this.color,
    this.showMessage = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(
            width: size,
            height: size,
            child: CircularProgressIndicator(
              color: color ?? theme.colorScheme.primary,
              strokeWidth: 2.0,
            ),
          ),
          
          if (showMessage && message != null) ...[
            const SizedBox(height: GHTokens.spacing16),
            Text(
              message!,
              style: GHTokens.bodyMedium.copyWith(
                color: theme.colorScheme.onSurfaceVariant,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ],
      ),
    );
  }
}
```

## Card System Enhancement

### Enhanced GHCard with Variants

```dart
class GHCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry? padding;
  final VoidCallback? onTap;
  final double? elevation;
  final Color? backgroundColor;
  final BorderRadius? borderRadius;

  const GHCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(GHTokens.spacing16),
    this.onTap,
    this.elevation,
    this.backgroundColor,
    this.borderRadius,
  });

  // Compact variant - for lists and secondary content
  const GHCard.compact({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
    double? elevation,
    Color? backgroundColor,
    BorderRadius? borderRadius,
  }) : this(
         key: key,
         child: child,
         padding: const EdgeInsets.all(GHTokens.spacing12),
         onTap: onTap,
         elevation: elevation,
         backgroundColor: backgroundColor,
         borderRadius: borderRadius,
       );

  // Tight variant - for dense content
  const GHCard.tight({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
    double? elevation,
    Color? backgroundColor,
    BorderRadius? borderRadius,
  }) : this(
         key: key,
         child: child,
         padding: const EdgeInsets.all(GHTokens.spacing8),
         onTap: onTap,
         elevation: elevation,
         backgroundColor: backgroundColor,
         borderRadius: borderRadius,
       );

  // Zero padding variant - for content with own padding
  const GHCard.zeroPadding({
    Key? key,
    required Widget child,
    VoidCallback? onTap,
    double? elevation,
    Color? backgroundColor,
    BorderRadius? borderRadius,
  }) : this(
         key: key,
         child: child,
         padding: EdgeInsets.zero,
         onTap: onTap,
         elevation: elevation,
         backgroundColor: backgroundColor,
         borderRadius: borderRadius,
       );

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final effectiveBorderRadius = borderRadius ?? 
      BorderRadius.circular(GHTokens.radius8);

    return Card(
      elevation: elevation ?? 1.0,
      color: backgroundColor ?? theme.colorScheme.surface,
      shape: RoundedRectangleBorder(borderRadius: effectiveBorderRadius),
      child: InkWell(
        onTap: onTap,
        borderRadius: effectiveBorderRadius,
        child: Padding(
          padding: padding ?? EdgeInsets.zero,
          child: child,
        ),
      ),
    );
  }
}
```

## Layout Templates

### GHContentTemplate Implementation

```dart
class GHContentTemplate extends StatelessWidget {
  final List<GHContentSection> sections;
  final GHContentMetadata? metadata;
  final Widget? header;
  final EdgeInsetsGeometry? padding;

  const GHContentTemplate({
    super.key,
    required this.sections,
    this.metadata,
    this.header,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: padding ?? const EdgeInsets.all(GHTokens.spacing16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (header != null) ...[
            header!,
            const SizedBox(height: GHTokens.spacing20),
          ],
          
          if (metadata != null) ...[
            _buildMetadata(context, metadata!),
            const SizedBox(height: GHTokens.spacing20),
          ],
          
          ...sections.map((section) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing20),
            child: _buildSection(context, section),
          )),
        ],
      ),
    );
  }

  Widget _buildSection(BuildContext context, GHContentSection section) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (section.title != null) ...[
          Text(
            section.title!,
            style: GHTokens.titleLarge,
          ),
          const SizedBox(height: GHTokens.spacing12),
        ],
        
        section.content,
      ],
    );
  }

  Widget _buildMetadata(BuildContext context, GHContentMetadata metadata) {
    return GHCard.compact(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (metadata.title != null) ...[
            Text(
              metadata.title!,
              style: GHTokens.titleMedium,
            ),
            const SizedBox(height: GHTokens.spacing8),
          ],
          
          ...metadata.items.map((item) => Padding(
            padding: const EdgeInsets.only(bottom: GHTokens.spacing4),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${item.label}: ',
                  style: GHTokens.bodyMedium.copyWith(
                    fontWeight: FontWeight.w500,
                  ),
                ),
                Expanded(
                  child: Text(
                    item.value,
                    style: GHTokens.bodyMedium,
                  ),
                ),
              ],
            ),
          )),
        ],
      ),
    );
  }
}

class GHContentSection {
  final String? title;
  final Widget content;

  const GHContentSection({
    this.title,
    required this.content,
  });
}

class GHContentMetadata {
  final String? title;
  final List<GHMetadataItem> items;

  const GHContentMetadata({
    this.title,
    required this.items,
  });
}

class GHMetadataItem {
  final String label;
  final String value;

  const GHMetadataItem({
    required this.label,
    required this.value,
  });
}
```

## Component Integration Patterns

### Empty State Usage

```dart
// Repository list with empty state
Widget _buildRepositoryList() {
  if (repositories.isEmpty) {
    return GHEmptyState(
      icon: Icons.folder_outlined,
      title: 'No repositories found',
      subtitle: 'Try adjusting your search criteria or create a new repository',
      action: GHButton(
        label: 'Clear filters',
        onPressed: _clearFilters,
        style: GHButtonStyle.secondary,
      ),
    );
  }
  
  return ListView.separated(
    itemCount: repositories.length,
    separatorBuilder: (context, index) => 
      const SizedBox(height: GHTokens.spacing12),
    itemBuilder: (context, index) => 
      GHRepositoryCard.fromRepository(repositories[index]),
  );
}
```

### Error State with Retry

```dart
// Network error handling
Widget _buildContent() {
  if (error != null) {
    return GHErrorState(
      title: 'Unable to load repositories',
      message: 'Please check your internet connection and try again.',
      onRetry: _retryLoad,
      isLoading: isRetrying,
    );
  }
  
  if (isLoading) {
    return const GHLoadingIndicator(
      message: 'Loading repositories...',
    );
  }
  
  return _buildRepositoryList();
}
```

### Content Template Usage

```dart
// Article or documentation screen
Widget _buildDocumentationScreen() {
  return GHContentTemplate(
    header: GHEntityHeader(
      title: 'API Documentation',
      subtitle: 'Comprehensive guide to the GitHub API',
    ),
    metadata: GHContentMetadata(
      title: 'Document Info',
      items: [
        GHMetadataItem(label: 'Last updated', value: '2 days ago'),
        GHMetadataItem(label: 'Version', value: 'v1.2.0'),
        GHMetadataItem(label: 'Contributors', value: '12'),
      ],
    ),
    sections: [
      GHContentSection(
        title: 'Getting Started',
        content: _buildGettingStartedContent(),
      ),
      GHContentSection(
        title: 'Authentication',
        content: _buildAuthenticationContent(),
      ),
      GHContentSection(
        title: 'Rate Limiting',
        content: _buildRateLimitingContent(),
      ),
    ],
  );
}
```

This design provides a complete component library that handles all major UI states and content organization patterns, ensuring consistent user experiences across the application.