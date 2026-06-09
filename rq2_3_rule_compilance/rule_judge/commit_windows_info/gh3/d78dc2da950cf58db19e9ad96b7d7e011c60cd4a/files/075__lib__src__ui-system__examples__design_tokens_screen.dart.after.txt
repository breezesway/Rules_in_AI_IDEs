import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';
import '../layouts/gh_screen_template.dart';
import '../utils/color_utils.dart';

/// **REFERENCE IMPLEMENTATION** - Design Tokens Screen
///
/// This screen serves as the definitive reference implementation for design token
/// usage and theming patterns in the GH3 design system. It demonstrates:
///
/// - Proper GHTokens constant usage for all design values
/// - Theme-aware color implementations
/// - Typography scale application
/// - Spacing system demonstrations
/// - Icon sizing and usage patterns
/// - Semantic color mapping (success, warning, error)
///
/// **Usage as Reference:**
/// - Copy token usage patterns for consistent styling
/// - Follow the theme-aware color implementations
/// - Use the demonstrated typography patterns
/// - Reference spacing usage throughout the file
/// - Maintain semantic color meanings shown here
///
/// This screen serves as a visual reference for developers and designers
/// to see all available design tokens in action.
class DesignTokensScreen extends StatefulWidget {
  const DesignTokensScreen({super.key});

  @override
  State<DesignTokensScreen> createState() => _DesignTokensScreenState();
}

class _DesignTokensScreenState extends State<DesignTokensScreen> {
  bool _isDarkMode = false;

  void _toggleTheme() {
    setState(() {
      _isDarkMode = !_isDarkMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Theme(
      data: _isDarkMode
          ? ThemeData.dark(useMaterial3: true)
          : ThemeData.light(useMaterial3: true),
      child: GHScreenTemplate(
        title: 'Design Tokens',
        actions: [
          IconButton(
            icon: Icon(_isDarkMode ? Icons.light_mode : Icons.dark_mode),
            onPressed: _toggleTheme,
            tooltip: _isDarkMode
                ? 'Switch to Light Mode'
                : 'Switch to Dark Mode',
          ),
        ],
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(GHTokens.spacing16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildSectionHeader('GitHub Brand Colors'),
              _buildBrandColorsSection(),
              const SizedBox(height: GHTokens.spacing32),

              _buildSectionHeader('GitHub Semantic Colors'),
              _buildSemanticColorsSection(),
              const SizedBox(height: GHTokens.spacing32),

              _buildSectionHeader('Typography Scale'),
              _buildTypographySection(),
              const SizedBox(height: GHTokens.spacing32),

              _buildSectionHeader('Spacing System'),
              _buildSpacingSection(),
              const SizedBox(height: GHTokens.spacing32),

              _buildSectionHeader('Programming Language Colors'),
              _buildLanguageColorsSection(),
              const SizedBox(height: GHTokens.spacing32),

              _buildSectionHeader('Border Radius & Elevation'),
              _buildRadiusElevationSection(),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: GHTokens.spacing16),
      child: Text(title, style: GHTokens.titleLarge),
    );
  }

  Widget _buildBrandColorsSection() {
    final brandColors = [
      {
        'name': 'Primary',
        'color': GHTokens.primary,
        'description': 'Main GitHub brand color',
      },
      {
        'name': 'On Primary',
        'color': GHTokens.onPrimary,
        'description': 'Text on primary color',
      },
      {
        'name': 'Primary Container',
        'color': GHTokens.primaryContainer,
        'description': 'Container using primary color',
      },
      {
        'name': 'On Primary Container',
        'color': GHTokens.onPrimaryContainer,
        'description': 'Text on primary container',
      },
    ];

    return Wrap(
      spacing: GHTokens.spacing16,
      runSpacing: GHTokens.spacing16,
      children: brandColors
          .map(
            (colorInfo) => _buildColorCard(
              colorInfo['name'] as String,
              colorInfo['color'] as Color,
              description: colorInfo['description'] as String,
            ),
          )
          .toList(),
    );
  }

  Widget _buildSemanticColorsSection() {
    final semanticColors = [
      {
        'name': 'Success',
        'color': GHTokens.success,
        'description': 'Open issues, success states',
      },
      {
        'name': 'Warning',
        'color': GHTokens.warning,
        'description': 'Warnings, pending states',
      },
      {
        'name': 'Error',
        'color': GHTokens.error,
        'description': 'Closed issues, error states',
      },
      {
        'name': 'Merged',
        'color': GHTokens.merged,
        'description': 'Merged pull requests',
      },
      {
        'name': 'Draft',
        'color': GHTokens.draft,
        'description': 'Draft PRs, disabled states',
      },
    ];

    return Wrap(
      spacing: GHTokens.spacing16,
      runSpacing: GHTokens.spacing16,
      children: semanticColors
          .map(
            (colorInfo) => _buildColorCard(
              colorInfo['name'] as String,
              colorInfo['color'] as Color,
              description: colorInfo['description'] as String,
            ),
          )
          .toList(),
    );
  }

  Widget _buildColorCard(String name, Color color, {String? description}) {
    final hexColor = ColorUtils.colorToHex(color);
    final textColor = ColorUtils.getContrastingTextColor(color);

    return Container(
      width: 160,
      height: 140,
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        border: Border.all(
          color: Theme.of(context).colorScheme.outline.withValues(alpha: 0.2),
        ),
      ),
      padding: const EdgeInsets.all(GHTokens.spacing12),
      child: ClipRect(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(name, style: GHTokens.labelLarge.copyWith(color: textColor)),
            const SizedBox(height: GHTokens.spacing4),
            Text(
              hexColor,
              style: GHTokens.labelMedium.copyWith(
                color: textColor.withValues(alpha: 0.8),
              ),
            ),
            if (description != null) ...[
              const SizedBox(height: GHTokens.spacing4),
              Text(
                description,
                style: GHTokens.labelMedium.copyWith(
                  color: textColor.withValues(alpha: 0.7),
                  fontSize: 10,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildTypographySection() {
    final typographyStyles = [
      {
        'name': 'Headline Large',
        'style': GHTokens.headlineLarge,
        'size': '32sp',
      },
      {
        'name': 'Headline Medium',
        'style': GHTokens.headlineMedium,
        'size': '28sp',
      },
      {'name': 'Title Large', 'style': GHTokens.titleLarge, 'size': '22sp'},
      {'name': 'Title Medium', 'style': GHTokens.titleMedium, 'size': '16sp'},
      {'name': 'Body Large', 'style': GHTokens.bodyLarge, 'size': '16sp'},
      {'name': 'Body Medium', 'style': GHTokens.bodyMedium, 'size': '14sp'},
      {'name': 'Label Large', 'style': GHTokens.labelLarge, 'size': '14sp'},
      {'name': 'Label Medium', 'style': GHTokens.labelMedium, 'size': '12sp'},
    ];

    return Column(
      children: typographyStyles.map((typeInfo) {
        return Container(
          width: double.infinity,
          margin: const EdgeInsets.only(bottom: GHTokens.spacing16),
          padding: const EdgeInsets.all(GHTokens.spacing16),
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
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Text(
                    typeInfo['name'] as String,
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                  const Spacer(),
                  Text(
                    typeInfo['size'] as String,
                    style: GHTokens.labelMedium.copyWith(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: GHTokens.spacing8),
              Text(
                'The quick brown fox jumps over the lazy dog',
                style: typeInfo['style'] as TextStyle,
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildSpacingSection() {
    final spacingValues = [
      {
        'name': 'spacing4',
        'value': GHTokens.spacing4,
        'usage': 'Micro spacing (icon gaps)',
      },
      {
        'name': 'spacing8',
        'value': GHTokens.spacing8,
        'usage': 'Small spacing (chip gaps)',
      },
      {
        'name': 'spacing12',
        'value': GHTokens.spacing12,
        'usage': 'Medium spacing (section padding)',
      },
      {
        'name': 'spacing16',
        'value': GHTokens.spacing16,
        'usage': 'Standard spacing (card padding)',
      },
      {
        'name': 'spacing20',
        'value': GHTokens.spacing20,
        'usage': 'Large spacing (section margins)',
      },
      {
        'name': 'spacing24',
        'value': GHTokens.spacing24,
        'usage': 'XL spacing (screen padding)',
      },
      {
        'name': 'spacing32',
        'value': GHTokens.spacing32,
        'usage': 'XXL spacing (major sections)',
      },
    ];

    return Column(
      children: spacingValues.map((spacingInfo) {
        final value = spacingInfo['value'] as double;
        return Container(
          width: double.infinity,
          margin: const EdgeInsets.only(bottom: GHTokens.spacing12),
          padding: const EdgeInsets.all(GHTokens.spacing16),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: BorderRadius.circular(GHTokens.radius8),
            border: Border.all(
              color: Theme.of(
                context,
              ).colorScheme.outline.withValues(alpha: 0.2),
            ),
          ),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${spacingInfo['name']} (${value.toInt()}dp)',
                      style: GHTokens.labelLarge,
                    ),
                    const SizedBox(height: GHTokens.spacing4),
                    Text(
                      spacingInfo['usage'] as String,
                      style: GHTokens.labelMedium.copyWith(
                        color: Theme.of(context).colorScheme.onSurfaceVariant,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                width: value,
                height: 24,
                decoration: BoxDecoration(
                  color: GHTokens.primary,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildLanguageColorsSection() {
    final languages = ColorUtils.getPopularLanguages();

    return Wrap(
      spacing: GHTokens.spacing8,
      runSpacing: GHTokens.spacing8,
      children: languages.map((langInfo) {
        final color = langInfo['color'] as Color;
        final language = langInfo['language'] as String;

        return Container(
          padding: const EdgeInsets.symmetric(
            horizontal: GHTokens.spacing12,
            vertical: GHTokens.spacing8,
          ),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: BorderRadius.circular(GHTokens.radius16),
            border: Border.all(
              color: Theme.of(
                context,
              ).colorScheme.outline.withValues(alpha: 0.2),
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(color: color, shape: BoxShape.circle),
              ),
              const SizedBox(width: GHTokens.spacing8),
              Text(language, style: GHTokens.labelMedium),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildRadiusElevationSection() {
    return Column(
      children: [
        // Border Radius Examples
        Text('Border Radius', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing16),
        Row(
          children: [
            _buildRadiusExample('radius4', GHTokens.radius4),
            const SizedBox(width: GHTokens.spacing16),
            _buildRadiusExample('radius8', GHTokens.radius8),
            const SizedBox(width: GHTokens.spacing16),
            _buildRadiusExample('radius12', GHTokens.radius12),
            const SizedBox(width: GHTokens.spacing16),
            _buildRadiusExample('radius16', GHTokens.radius16),
          ],
        ),
        const SizedBox(height: GHTokens.spacing24),

        // Elevation Examples
        Text('Elevation', style: GHTokens.titleMedium),
        const SizedBox(height: GHTokens.spacing16),
        Row(
          children: [
            _buildElevationExample('elevation0', GHTokens.elevation0),
            const SizedBox(width: GHTokens.spacing16),
            _buildElevationExample('elevation1', GHTokens.elevation1),
            const SizedBox(width: GHTokens.spacing16),
            _buildElevationExample('elevation3', GHTokens.elevation3),
            const SizedBox(width: GHTokens.spacing16),
            _buildElevationExample('elevation8', GHTokens.elevation8),
          ],
        ),
      ],
    );
  }

  Widget _buildRadiusExample(String name, double radius) {
    return Column(
      children: [
        Container(
          width: 60,
          height: 60,
          decoration: BoxDecoration(
            color: GHTokens.primary,
            borderRadius: BorderRadius.circular(radius),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
        Text(name, style: GHTokens.labelMedium),
        Text(
          '${radius.toInt()}dp',
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }

  Widget _buildElevationExample(String name, double elevation) {
    return Column(
      children: [
        Material(
          elevation: elevation,
          borderRadius: BorderRadius.circular(GHTokens.radius8),
          child: Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              borderRadius: BorderRadius.circular(GHTokens.radius8),
            ),
          ),
        ),
        const SizedBox(height: GHTokens.spacing8),
        Text(name, style: GHTokens.labelMedium),
        Text(
          '${elevation.toInt()}dp',
          style: GHTokens.labelMedium.copyWith(
            color: Theme.of(context).colorScheme.onSurfaceVariant,
          ),
        ),
      ],
    );
  }
}
