import 'package:flutter/material.dart';

/// Utility class for programming language colors and color-related functions.
///
/// This class provides colors for popular programming languages based on
/// GitHub's language color scheme, along with utility functions for color manipulation.
class ColorUtils {
  // Private constructor to prevent instantiation
  const ColorUtils._();

  /// Map of programming language names to their associated colors
  static const Map<String, Color> languageColors = {
    'JavaScript': Color(0xFFF1E05A),
    'Dart': Color(0xFF00B4AB),
    'Python': Color(0xFF3572A5),
    'Swift': Color(0xFFFA7343),
    'TypeScript': Color(0xFF2B7489),
    'Java': Color(0xFFB07219),
    'C++': Color(0xFFF34B7D),
    'Go': Color(0xFF00ADD8),
    'Rust': Color(0xFFDEA584),
    'Kotlin': Color(0xFFA97BFF),
    'C#': Color(0xFF239120),
    'Ruby': Color(0xFF701516),
    'PHP': Color(0xFF4F5D95),
    'Shell': Color(0xFF89E051),
    'HTML': Color(0xFFE34C26),
    'CSS': Color(0xFF1572B6),
    'Vue': Color(0xFF4FC08D),
    'React': Color(0xFF61DAFB),
    'Angular': Color(0xFFDD0031),
    'Node.js': Color(0xFF339933),
    'C': Color(0xFF555555),
    'Objective-C': Color(0xFF438EFF),
    'Scala': Color(0xFFDC322F),
    'R': Color(0xFF198CE7),
    'MATLAB': Color(0xFFE16737),
  };

  /// Default color for unknown languages
  static const Color defaultLanguageColor = Color(0xFF858585);

  /// Gets the color associated with a programming language.
  ///
  /// Returns the default color if the language is not found.
  static Color getLanguageColor(String language) {
    return languageColors[language] ?? defaultLanguageColor;
  }

  /// Gets a list of all supported programming languages.
  ///
  /// Returns the languages sorted alphabetically.
  static List<String> getSupportedLanguages() {
    return languageColors.keys.toList()..sort();
  }

  /// Gets a list of language-color pairs for demonstration.
  static List<Map<String, dynamic>> getLanguageColorPairs() {
    return languageColors.entries
        .map(
          (entry) => {
            'language': entry.key,
            'color': entry.value,
            'hex':
                '#${entry.value.toARGB32().toRadixString(16).substring(2).toUpperCase()}',
          },
        )
        .toList()
      ..sort(
        (a, b) => (a['language'] as String).compareTo(b['language'] as String),
      );
  }

  /// Determines if a color is light or dark.
  ///
  /// Uses the relative luminance formula to determine brightness.
  /// Returns true if the color is considered light.
  static bool isLightColor(Color color) {
    final luminance =
        (0.299 * (color.r * 255.0).round() +
            0.587 * (color.g * 255.0).round() +
            0.114 * (color.b * 255.0).round()) /
        255;
    return luminance > 0.5;
  }

  /// Gets the appropriate text color (black or white) for a given background color.
  ///
  /// Returns white for dark backgrounds and black for light backgrounds.
  static Color getContrastingTextColor(Color backgroundColor) {
    return isLightColor(backgroundColor) ? Colors.black : Colors.white;
  }

  /// Converts a Color to its hexadecimal string representation.
  ///
  /// Examples:
  /// - Color(0xFFFF0000) → "#FF0000"
  /// - Color(0xFF00FF00) → "#00FF00"
  static String colorToHex(Color color) {
    return '#${color.toARGB32().toRadixString(16).substring(2).toUpperCase()}';
  }

  /// Converts a hexadecimal string to a Color.
  ///
  /// Supports formats: "#RRGGBB", "#AARRGGBB", "RRGGBB", "AARRGGBB"
  /// Returns null if the string is invalid.
  static Color? hexToColor(String hex) {
    try {
      String cleanHex = hex.replaceAll('#', '');

      if (cleanHex.length == 6) {
        cleanHex = 'FF$cleanHex'; // Add full opacity
      }

      if (cleanHex.length == 8) {
        return Color(int.parse(cleanHex, radix: 16));
      }

      return null;
    } catch (e) {
      return null;
    }
  }

  /// Creates a lighter version of the given color.
  ///
  /// The [amount] parameter should be between 0.0 and 1.0.
  static Color lighten(Color color, double amount) {
    assert(amount >= 0.0 && amount <= 1.0);

    final hsl = HSLColor.fromColor(color);
    final lightness = (hsl.lightness + amount).clamp(0.0, 1.0);

    return hsl.withLightness(lightness).toColor();
  }

  /// Creates a darker version of the given color.
  ///
  /// The [amount] parameter should be between 0.0 and 1.0.
  static Color darken(Color color, double amount) {
    assert(amount >= 0.0 && amount <= 1.0);

    final hsl = HSLColor.fromColor(color);
    final lightness = (hsl.lightness - amount).clamp(0.0, 1.0);

    return hsl.withLightness(lightness).toColor();
  }

  /// Creates a color with the specified opacity.
  ///
  /// The [opacity] parameter should be between 0.0 and 1.0.
  static Color withOpacity(Color color, double opacity) {
    assert(opacity >= 0.0 && opacity <= 1.0);
    return color.withValues(alpha: opacity);
  }

  /// Gets popular programming languages with their colors for demonstration.
  static List<Map<String, dynamic>> getPopularLanguages() {
    const popularLanguages = [
      'JavaScript',
      'Python',
      'Java',
      'TypeScript',
      'C#',
      'PHP',
      'C++',
      'Go',
      'Rust',
      'Swift',
      'Kotlin',
      'Dart',
    ];

    return popularLanguages
        .map(
          (language) => {
            'language': language,
            'color': getLanguageColor(language),
            'hex': colorToHex(getLanguageColor(language)),
          },
        )
        .toList();
  }
}
