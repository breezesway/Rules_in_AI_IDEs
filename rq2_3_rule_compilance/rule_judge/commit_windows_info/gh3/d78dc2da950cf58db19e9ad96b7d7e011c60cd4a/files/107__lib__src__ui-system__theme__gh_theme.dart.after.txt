import 'package:flutter/material.dart';
import '../tokens/gh_tokens.dart';

/// GitHub-themed Material Design 3 theme configuration.
///
/// This class provides light and dark theme configurations that integrate
/// GitHub brand colors with Material Design 3 theming system.
class GHTheme {
  // Private constructor to prevent instantiation
  const GHTheme._();

  /// Light theme configuration with GitHub brand colors
  static ThemeData lightTheme() {
    final colorScheme =
        ColorScheme.fromSeed(
          seedColor: GHTokens.primary,
          brightness: Brightness.light,
        ).copyWith(
          primary: GHTokens.primary,
          onPrimary: GHTokens.onPrimary,
          primaryContainer: GHTokens.primaryContainer,
          onPrimaryContainer: GHTokens.onPrimaryContainer,
          error: GHTokens.error,
        );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _buildTextTheme(colorScheme),
      cardTheme: _buildCardTheme(colorScheme),
      elevatedButtonTheme: _buildElevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _buildOutlinedButtonTheme(colorScheme),
      chipTheme: _buildChipTheme(colorScheme),
      inputDecorationTheme: _buildInputDecorationTheme(colorScheme),
      appBarTheme: _buildAppBarTheme(colorScheme),
      listTileTheme: _buildListTileTheme(colorScheme),
    );
  }

  /// Dark theme configuration with GitHub brand colors
  static ThemeData darkTheme() {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: GHTokens.primary,
      brightness: Brightness.dark,
    ).copyWith(primary: GHTokens.primary, error: GHTokens.error);

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: _buildTextTheme(colorScheme),
      cardTheme: _buildCardTheme(colorScheme),
      elevatedButtonTheme: _buildElevatedButtonTheme(colorScheme),
      outlinedButtonTheme: _buildOutlinedButtonTheme(colorScheme),
      chipTheme: _buildChipTheme(colorScheme),
      inputDecorationTheme: _buildInputDecorationTheme(colorScheme),
      appBarTheme: _buildAppBarTheme(colorScheme),
      listTileTheme: _buildListTileTheme(colorScheme),
    );
  }

  /// Build text theme using GitHub typography tokens
  static TextTheme _buildTextTheme(ColorScheme colorScheme) {
    return TextTheme(
      headlineLarge: GHTokens.headlineLarge.copyWith(
        color: colorScheme.onSurface,
      ),
      headlineMedium: GHTokens.headlineMedium.copyWith(
        color: colorScheme.onSurface,
      ),
      titleLarge: GHTokens.titleLarge.copyWith(color: colorScheme.onSurface),
      titleMedium: GHTokens.titleMedium.copyWith(color: colorScheme.onSurface),
      bodyLarge: GHTokens.bodyLarge.copyWith(color: colorScheme.onSurface),
      bodyMedium: GHTokens.bodyMedium.copyWith(
        color: colorScheme.onSurfaceVariant,
      ),
      labelLarge: GHTokens.labelLarge.copyWith(color: colorScheme.onSurface),
      labelMedium: GHTokens.labelMedium.copyWith(
        color: colorScheme.onSurfaceVariant,
      ),
    );
  }

  /// Build card theme with GitHub styling
  static CardThemeData _buildCardTheme(ColorScheme colorScheme) {
    return CardThemeData(
      elevation: GHTokens.elevation1,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      margin: const EdgeInsets.all(GHTokens.spacing4),
    );
  }

  /// Build elevated button theme
  static ElevatedButtonThemeData _buildElevatedButtonTheme(
    ColorScheme colorScheme,
  ) {
    return ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        minimumSize: const Size(88, GHTokens.minTouchTarget),
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing16,
          vertical: GHTokens.spacing12,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(GHTokens.radius8),
        ),
        textStyle: GHTokens.labelLarge,
      ),
    );
  }

  /// Build outlined button theme
  static OutlinedButtonThemeData _buildOutlinedButtonTheme(
    ColorScheme colorScheme,
  ) {
    return OutlinedButtonThemeData(
      style: OutlinedButton.styleFrom(
        minimumSize: const Size(88, GHTokens.minTouchTarget),
        padding: const EdgeInsets.symmetric(
          horizontal: GHTokens.spacing16,
          vertical: GHTokens.spacing12,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(GHTokens.radius8),
        ),
        textStyle: GHTokens.labelLarge,
      ),
    );
  }

  /// Build chip theme
  static ChipThemeData _buildChipTheme(ColorScheme colorScheme) {
    return ChipThemeData(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius16),
      ),
      labelStyle: GHTokens.labelMedium,
      padding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing8,
        vertical: GHTokens.spacing4,
      ),
    );
  }

  /// Build input decoration theme
  static InputDecorationTheme _buildInputDecorationTheme(
    ColorScheme colorScheme,
  ) {
    return InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        borderSide: BorderSide(color: colorScheme.outline),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        borderSide: BorderSide(color: colorScheme.primary, width: 2),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(GHTokens.radius8),
        borderSide: BorderSide(color: colorScheme.error),
      ),
      contentPadding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing16,
        vertical: GHTokens.spacing12,
      ),
      hintStyle: GHTokens.bodyMedium.copyWith(
        color: colorScheme.onSurfaceVariant,
      ),
    );
  }

  /// Build app bar theme
  static AppBarTheme _buildAppBarTheme(ColorScheme colorScheme) {
    return AppBarTheme(
      elevation: GHTokens.elevation0,
      centerTitle: false,
      titleTextStyle: GHTokens.titleLarge.copyWith(
        color: colorScheme.onSurface,
      ),
      iconTheme: IconThemeData(
        color: colorScheme.onSurface,
        size: GHTokens.iconSize24,
      ),
      actionsIconTheme: IconThemeData(
        color: colorScheme.onSurface,
        size: GHTokens.iconSize24,
      ),
    );
  }

  /// Build list tile theme
  static ListTileThemeData _buildListTileTheme(ColorScheme colorScheme) {
    return ListTileThemeData(
      contentPadding: const EdgeInsets.symmetric(
        horizontal: GHTokens.spacing16,
        vertical: GHTokens.spacing8,
      ),
      titleTextStyle: GHTokens.bodyLarge.copyWith(color: colorScheme.onSurface),
      subtitleTextStyle: GHTokens.bodyMedium.copyWith(
        color: colorScheme.onSurfaceVariant,
      ),
      iconColor: colorScheme.onSurfaceVariant,
      minVerticalPadding: GHTokens.spacing8,
    );
  }
}
