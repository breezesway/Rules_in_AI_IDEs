import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/utils/color_utils.dart';

void main() {
  group('ColorUtils', () {
    group('getLanguageColor', () {
      test('should return correct colors for known languages', () {
        expect(
          ColorUtils.getLanguageColor('JavaScript'),
          equals(const Color(0xFFF1E05A)),
        );
        expect(
          ColorUtils.getLanguageColor('Dart'),
          equals(const Color(0xFF00B4AB)),
        );
        expect(
          ColorUtils.getLanguageColor('Python'),
          equals(const Color(0xFF3572A5)),
        );
        expect(
          ColorUtils.getLanguageColor('Swift'),
          equals(const Color(0xFFFA7343)),
        );
      });

      test('should return default color for unknown languages', () {
        expect(
          ColorUtils.getLanguageColor('UnknownLanguage'),
          equals(ColorUtils.defaultLanguageColor),
        );
        expect(
          ColorUtils.getLanguageColor(''),
          equals(ColorUtils.defaultLanguageColor),
        );
      });

      test('should be case sensitive', () {
        expect(
          ColorUtils.getLanguageColor('javascript'),
          equals(ColorUtils.defaultLanguageColor),
        );
        expect(
          ColorUtils.getLanguageColor('DART'),
          equals(ColorUtils.defaultLanguageColor),
        );
      });
    });

    group('getSupportedLanguages', () {
      test('should return a sorted list of supported languages', () {
        final languages = ColorUtils.getSupportedLanguages();
        expect(languages, isA<List<String>>());
        expect(languages.length, greaterThan(0));

        // Check if sorted
        final sortedLanguages = List<String>.from(languages)..sort();
        expect(languages, equals(sortedLanguages));

        // Check if contains expected languages
        expect(languages, contains('JavaScript'));
        expect(languages, contains('Dart'));
        expect(languages, contains('Python'));
      });
    });

    group('getLanguageColorPairs', () {
      test('should return language-color pairs with hex values', () {
        final pairs = ColorUtils.getLanguageColorPairs();
        expect(pairs, isA<List<Map<String, dynamic>>>());
        expect(pairs.length, greaterThan(0));

        for (final pair in pairs) {
          expect(pair.containsKey('language'), isTrue);
          expect(pair.containsKey('color'), isTrue);
          expect(pair.containsKey('hex'), isTrue);
          expect(pair['language'], isA<String>());
          expect(pair['color'], isA<Color>());
          expect(pair['hex'], isA<String>());
          expect(pair['hex'], startsWith('#'));
        }
      });
    });

    group('isLightColor', () {
      test('should correctly identify light colors', () {
        expect(ColorUtils.isLightColor(Colors.white), isTrue);
        expect(ColorUtils.isLightColor(Colors.yellow), isTrue);
        expect(ColorUtils.isLightColor(const Color(0xFFFFFFFF)), isTrue);
      });

      test('should correctly identify dark colors', () {
        expect(ColorUtils.isLightColor(Colors.black), isFalse);
        expect(ColorUtils.isLightColor(Colors.blue), isFalse);
        expect(ColorUtils.isLightColor(const Color(0xFF000000)), isFalse);
      });
    });

    group('getContrastingTextColor', () {
      test('should return black for light backgrounds', () {
        expect(
          ColorUtils.getContrastingTextColor(Colors.white),
          equals(Colors.black),
        );
        expect(
          ColorUtils.getContrastingTextColor(Colors.yellow),
          equals(Colors.black),
        );
      });

      test('should return white for dark backgrounds', () {
        expect(
          ColorUtils.getContrastingTextColor(Colors.black),
          equals(Colors.white),
        );
        expect(
          ColorUtils.getContrastingTextColor(Colors.blue),
          equals(Colors.white),
        );
      });
    });

    group('colorToHex', () {
      test('should convert colors to hex strings', () {
        expect(
          ColorUtils.colorToHex(const Color(0xFFFF0000)),
          equals('#FF0000'),
        );
        expect(
          ColorUtils.colorToHex(const Color(0xFF0000FF)),
          equals('#0000FF'),
        );
        expect(
          ColorUtils.colorToHex(const Color(0xFF00FF00)),
          equals('#00FF00'),
        );
      });
    });

    group('hexToColor', () {
      test('should convert hex strings to colors', () {
        expect(
          ColorUtils.hexToColor('#FF0000'),
          equals(const Color(0xFFFF0000)),
        );
        expect(
          ColorUtils.hexToColor('FF0000'),
          equals(const Color(0xFFFF0000)),
        );
        expect(
          ColorUtils.hexToColor('#FFFF0000'),
          equals(const Color(0xFFFF0000)),
        );
        expect(
          ColorUtils.hexToColor('FFFF0000'),
          equals(const Color(0xFFFF0000)),
        );
      });

      test('should return null for invalid hex strings', () {
        expect(ColorUtils.hexToColor('invalid'), isNull);
        expect(ColorUtils.hexToColor('#GG0000'), isNull);
        expect(ColorUtils.hexToColor('#FF00'), isNull);
        expect(ColorUtils.hexToColor(''), isNull);
      });
    });

    group('lighten', () {
      test('should create lighter versions of colors', () {
        final originalColor = Colors.blue;
        final lighterColor = ColorUtils.lighten(originalColor, 0.2);

        final originalHsl = HSLColor.fromColor(originalColor);
        final lighterHsl = HSLColor.fromColor(lighterColor);

        expect(lighterHsl.lightness, greaterThan(originalHsl.lightness));
      });

      test('should clamp lightness to valid range', () {
        final color = ColorUtils.lighten(Colors.white, 0.5);
        final hsl = HSLColor.fromColor(color);
        expect(hsl.lightness, lessThanOrEqualTo(1.0));
      });
    });

    group('darken', () {
      test('should create darker versions of colors', () {
        final originalColor = Colors.blue;
        final darkerColor = ColorUtils.darken(originalColor, 0.2);

        final originalHsl = HSLColor.fromColor(originalColor);
        final darkerHsl = HSLColor.fromColor(darkerColor);

        expect(darkerHsl.lightness, lessThan(originalHsl.lightness));
      });

      test('should clamp lightness to valid range', () {
        final color = ColorUtils.darken(Colors.black, 0.5);
        final hsl = HSLColor.fromColor(color);
        expect(hsl.lightness, greaterThanOrEqualTo(0.0));
      });
    });

    group('withOpacity', () {
      test('should create colors with specified opacity', () {
        final color = ColorUtils.withOpacity(const Color(0xFFFF0000), 0.5);
        expect(color.a, closeTo(0.5, 0.01));
      });

      test('should preserve original color properties', () {
        final originalColor = const Color(0xFF0000FF);
        final transparentColor = ColorUtils.withOpacity(originalColor, 0.3);

        expect(
          (transparentColor.r * 255.0).round(),
          equals((originalColor.r * 255.0).round()),
        );
        expect(
          (transparentColor.g * 255.0).round(),
          equals((originalColor.g * 255.0).round()),
        );
        expect(
          (transparentColor.b * 255.0).round(),
          equals((originalColor.b * 255.0).round()),
        );
        expect(transparentColor.a, closeTo(0.3, 0.01));
      });
    });

    group('getPopularLanguages', () {
      test('should return popular languages with colors and hex values', () {
        final languages = ColorUtils.getPopularLanguages();
        expect(languages, isA<List<Map<String, dynamic>>>());
        expect(languages.length, greaterThan(0));

        for (final lang in languages) {
          expect(lang.containsKey('language'), isTrue);
          expect(lang.containsKey('color'), isTrue);
          expect(lang.containsKey('hex'), isTrue);
          expect(lang['language'], isA<String>());
          expect(lang['color'], isA<Color>());
          expect(lang['hex'], isA<String>());
        }

        // Check for some expected popular languages
        final languageNames = languages
            .map((l) => l['language'] as String)
            .toList();
        expect(languageNames, contains('JavaScript'));
        expect(languageNames, contains('Python'));
        expect(languageNames, contains('Dart'));
      });
    });
  });
}
