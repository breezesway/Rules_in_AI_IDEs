import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/utils/number_formatter.dart';

void main() {
  group('NumberFormatter', () {
    group('formatCompact', () {
      test('should return number as string for values less than 1000', () {
        expect(NumberFormatter.formatCompact(0), equals('0'));
        expect(NumberFormatter.formatCompact(42), equals('42'));
        expect(NumberFormatter.formatCompact(999), equals('999'));
      });

      test('should format thousands with k suffix', () {
        expect(NumberFormatter.formatCompact(1000), equals('1k'));
        expect(NumberFormatter.formatCompact(1234), equals('1.2k'));
        expect(NumberFormatter.formatCompact(12345), equals('12.3k'));
        expect(NumberFormatter.formatCompact(123456), equals('123k'));
        expect(NumberFormatter.formatCompact(999999), equals('1000k'));
      });

      test('should format millions with M suffix', () {
        expect(NumberFormatter.formatCompact(1000000), equals('1M'));
        expect(NumberFormatter.formatCompact(1234567), equals('1.2M'));
        expect(NumberFormatter.formatCompact(12345678), equals('12.3M'));
        expect(NumberFormatter.formatCompact(123456789), equals('123M'));
      });

      test('should format billions with B suffix', () {
        expect(NumberFormatter.formatCompact(1000000000), equals('1B'));
        expect(NumberFormatter.formatCompact(1234567890), equals('1.2B'));
        expect(NumberFormatter.formatCompact(12345678901), equals('12.3B'));
      });

      test('should handle negative numbers', () {
        expect(NumberFormatter.formatCompact(-42), equals('-42'));
        expect(NumberFormatter.formatCompact(-1234), equals('-1.2k'));
        expect(NumberFormatter.formatCompact(-1234567), equals('-1.2M'));
      });
    });

    group('formatWithCommas', () {
      test('should add commas to large numbers', () {
        expect(NumberFormatter.formatWithCommas(1234), equals('1,234'));
        expect(NumberFormatter.formatWithCommas(1234567), equals('1,234,567'));
        expect(
          NumberFormatter.formatWithCommas(1234567890),
          equals('1,234,567,890'),
        );
      });

      test('should handle small numbers without commas', () {
        expect(NumberFormatter.formatWithCommas(123), equals('123'));
        expect(NumberFormatter.formatWithCommas(0), equals('0'));
      });

      test('should handle negative numbers', () {
        expect(NumberFormatter.formatWithCommas(-1234), equals('-1,234'));
        expect(
          NumberFormatter.formatWithCommas(-1234567),
          equals('-1,234,567'),
        );
      });
    });

    group('formatPercentage', () {
      test('should format decimal as percentage', () {
        expect(NumberFormatter.formatPercentage(0.1234), equals('12.3%'));
        expect(NumberFormatter.formatPercentage(0.5), equals('50%'));
        expect(NumberFormatter.formatPercentage(1.0), equals('100%'));
        expect(NumberFormatter.formatPercentage(0.0), equals('0%'));
      });

      test('should respect decimal places parameter', () {
        expect(
          NumberFormatter.formatPercentage(0.1234, decimalPlaces: 2),
          equals('12.34%'),
        );
        expect(
          NumberFormatter.formatPercentage(0.1234, decimalPlaces: 0),
          equals('12%'),
        );
      });
    });

    group('formatFileSize', () {
      test('should format bytes correctly', () {
        expect(NumberFormatter.formatFileSize(0), equals('0 B'));
        expect(NumberFormatter.formatFileSize(512), equals('512 B'));
        expect(NumberFormatter.formatFileSize(1023), equals('1023 B'));
      });

      test('should format kilobytes correctly', () {
        expect(NumberFormatter.formatFileSize(1024), equals('1 KB'));
        expect(NumberFormatter.formatFileSize(1536), equals('1.5 KB'));
        expect(NumberFormatter.formatFileSize(1048575), equals('1024.0 KB'));
      });

      test('should format megabytes correctly', () {
        expect(NumberFormatter.formatFileSize(1048576), equals('1 MB'));
        expect(NumberFormatter.formatFileSize(1572864), equals('1.5 MB'));
      });

      test('should format gigabytes correctly', () {
        expect(NumberFormatter.formatFileSize(1073741824), equals('1 GB'));
        expect(NumberFormatter.formatFileSize(1610612736), equals('1.5 GB'));
      });

      test('should handle negative file sizes', () {
        expect(NumberFormatter.formatFileSize(-1024), equals('-1 KB'));
      });
    });

    group('getSampleFormattedNumbers', () {
      test('should return a list of formatted numbers', () {
        final samples = NumberFormatter.getSampleFormattedNumbers();
        expect(samples, isA<List<String>>());
        expect(samples.length, greaterThan(0));
        expect(samples.every((sample) => sample.isNotEmpty), isTrue);
      });
    });

    group('getSampleGitHubStats', () {
      test('should return a list of GitHub statistics', () {
        final stats = NumberFormatter.getSampleGitHubStats();
        expect(stats, isA<List<Map<String, dynamic>>>());
        expect(stats.length, greaterThan(0));

        for (final stat in stats) {
          expect(stat.containsKey('label'), isTrue);
          expect(stat.containsKey('value'), isTrue);
          expect(stat.containsKey('formatted'), isTrue);
          expect(stat['label'], isA<String>());
          expect(stat['value'], isA<int>());
          expect(stat['formatted'], isA<String>());
        }
      });
    });
  });
}
