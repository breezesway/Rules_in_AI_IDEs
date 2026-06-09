import 'package:flutter/material.dart';

/// Centralized design tokens for the GitHub mobile application.
///
/// This class provides all design tokens including colors, typography, spacing,
/// and other visual properties used throughout the application. All tokens are
/// compile-time constants for optimal performance.
class GHTokens {
  // Private constructor to prevent instantiation
  const GHTokens._();

  // ==========================================================================
  // COLORS - GitHub Brand
  // ==========================================================================

  /// Primary GitHub brand color
  static const Color primary = Color(0xFF0969DA);

  /// Color to use on top of primary color
  static const Color onPrimary = Color(0xFFFFFFFF);

  /// Container color for primary elements
  static const Color primaryContainer = Color(0xFFDDE6F4);

  /// Color to use on top of primary container
  static const Color onPrimaryContainer = Color(0xFF0A1929);

  // ==========================================================================
  // GITHUB SEMANTIC COLORS
  // ==========================================================================

  /// Success color - used for open issues, success states
  static const Color success = Color(0xFF1A7F37);

  /// Warning color - used for warnings, pending states
  static const Color warning = Color(0xFFBF8700);

  /// Error color - used for closed issues, error states
  static const Color error = Color(0xFFCF222E);

  /// Merged color - used for merged PRs
  static const Color merged = Color(0xFF8250DF);

  /// Draft color - used for draft PRs, disabled states
  static const Color draft = Color(0xFF656D76);

  // ==========================================================================
  // TYPOGRAPHY SCALE
  // ==========================================================================

  /// Headline Large - 32sp, titles and hero text
  static const TextStyle headlineLarge = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w400,
    height: 1.25,
  );

  /// Headline Medium - 28sp, screen titles
  static const TextStyle headlineMedium = TextStyle(
    fontSize: 28,
    fontWeight: FontWeight.w400,
    height: 1.29,
  );

  /// Title Large - 22sp, section headers
  static const TextStyle titleLarge = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.w500,
    height: 1.27,
  );

  /// Title Medium - 16sp, card titles
  static const TextStyle titleMedium = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    height: 1.5,
  );

  /// Title Small - 14sp, small headers
  static const TextStyle titleSmall = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    height: 1.43,
  );

  /// Body Large - 16sp, primary content
  static const TextStyle bodyLarge = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 1.5,
  );

  /// Body Medium - 14sp, secondary content
  static const TextStyle bodyMedium = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.43,
  );

  /// Body Small - 12sp, small body text
  static const TextStyle bodySmall = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w400,
    height: 1.33,
  );

  /// Label Large - 14sp, button text
  static const TextStyle labelLarge = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    height: 1.43,
  );

  /// Label Medium - 12sp, metadata and captions
  static const TextStyle labelMedium = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w500,
    height: 1.33,
  );

  /// Label Small - 10sp, small labels and badges
  static const TextStyle labelSmall = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.w500,
    height: 1.4,
  );

  // ==========================================================================
  // SPACING SYSTEM
  // ==========================================================================

  /// Micro spacing - 4dp (icon gaps, very small gaps)
  static const double spacing4 = 4.0;

  /// Small spacing - 8dp (chip gaps)
  static const double spacing8 = 8.0;

  /// Medium spacing - 12dp (section padding)
  static const double spacing12 = 12.0;

  /// Standard spacing - 16dp (card padding)
  static const double spacing16 = 16.0;

  /// Large spacing - 20dp (section margins)
  static const double spacing20 = 20.0;

  /// XL spacing - 24dp (screen padding)
  static const double spacing24 = 24.0;

  /// XXL spacing - 32dp (major sections)
  static const double spacing32 = 32.0;

  // ==========================================================================
  // BORDER RADIUS
  // ==========================================================================

  /// Small radius - 4dp
  static const double radius4 = 4.0;

  /// Standard radius - 8dp
  static const double radius8 = 8.0;

  /// Medium radius - 12dp
  static const double radius12 = 12.0;

  /// Large radius - 16dp
  static const double radius16 = 16.0;

  // ==========================================================================
  // ELEVATION
  // ==========================================================================

  /// No elevation
  static const double elevation0 = 0.0;

  /// Low elevation - cards, buttons
  static const double elevation1 = 1.0;

  /// Medium elevation - dialogs, menus
  static const double elevation3 = 3.0;

  /// High elevation - navigation drawer
  static const double elevation8 = 8.0;

  // ==========================================================================
  // TOUCH TARGETS
  // ==========================================================================

  /// Minimum touch target size for accessibility
  static const double minTouchTarget = 48.0;

  /// Standard icon size
  static const double iconSize16 = 16.0;
  static const double iconSize18 = 18.0;
  static const double iconSize24 = 24.0;
  static const double iconSize32 = 32.0;
  static const double iconSize48 = 48.0;
}
