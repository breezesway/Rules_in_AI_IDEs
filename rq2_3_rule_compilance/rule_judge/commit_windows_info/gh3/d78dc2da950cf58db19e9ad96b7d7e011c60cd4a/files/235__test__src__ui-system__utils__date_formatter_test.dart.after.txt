import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/utils/date_formatter.dart';

void main() {
  group('DateFormatter', () {
    late DateTime now;

    setUp(() {
      now = DateTime.now();
    });

    group('formatRelative', () {
      test('should return "Just now" for times less than 1 minute ago', () {
        final dateTime = now.subtract(const Duration(seconds: 30));
        expect(DateFormatter.formatRelative(dateTime), equals('Just now'));
      });

      test('should return minutes for times less than 1 hour ago', () {
        final dateTime = now.subtract(const Duration(minutes: 5));
        expect(DateFormatter.formatRelative(dateTime), equals('5 minutes ago'));

        final oneMinute = now.subtract(const Duration(minutes: 1));
        expect(DateFormatter.formatRelative(oneMinute), equals('1 minute ago'));
      });

      test('should return hours for times less than 1 day ago', () {
        final dateTime = now.subtract(const Duration(hours: 3));
        expect(DateFormatter.formatRelative(dateTime), equals('3 hours ago'));

        final oneHour = now.subtract(const Duration(hours: 1));
        expect(DateFormatter.formatRelative(oneHour), equals('1 hour ago'));
      });

      test('should return days for times less than 1 week ago', () {
        final dateTime = now.subtract(const Duration(days: 3));
        expect(DateFormatter.formatRelative(dateTime), equals('3 days ago'));

        final oneDay = now.subtract(const Duration(days: 1));
        expect(DateFormatter.formatRelative(oneDay), equals('1 day ago'));
      });

      test('should return weeks for times less than 1 month ago', () {
        final dateTime = now.subtract(const Duration(days: 14));
        expect(DateFormatter.formatRelative(dateTime), equals('2 weeks ago'));

        final oneWeek = now.subtract(const Duration(days: 7));
        expect(DateFormatter.formatRelative(oneWeek), equals('Last week'));
      });

      test('should return months for times less than 1 year ago', () {
        final dateTime = now.subtract(const Duration(days: 60));
        expect(DateFormatter.formatRelative(dateTime), equals('2 months ago'));

        final oneMonth = now.subtract(const Duration(days: 30));
        expect(DateFormatter.formatRelative(oneMonth), equals('Last month'));
      });

      test('should return years for times more than 1 year ago', () {
        final dateTime = now.subtract(const Duration(days: 730));
        expect(DateFormatter.formatRelative(dateTime), equals('2 years ago'));

        final oneYear = now.subtract(const Duration(days: 365));
        expect(DateFormatter.formatRelative(oneYear), equals('Last year'));
      });
    });

    group('formatRelativeShort', () {
      test('should return short format for various time periods', () {
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(seconds: 30)),
          ),
          equals('now'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(minutes: 5)),
          ),
          equals('5m'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(hours: 3)),
          ),
          equals('3h'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(days: 2)),
          ),
          equals('2d'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(days: 14)),
          ),
          equals('2w'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(days: 60)),
          ),
          equals('2mo'),
        );
        expect(
          DateFormatter.formatRelativeShort(
            now.subtract(const Duration(days: 730)),
          ),
          equals('2y'),
        );
      });
    });

    group('formatAbsolute', () {
      test('should format date in absolute format', () {
        final dateTime = DateTime(2024, 3, 15);
        expect(DateFormatter.formatAbsolute(dateTime), equals('Mar 15, 2024'));

        final dateTime2 = DateTime(2023, 12, 1);
        expect(DateFormatter.formatAbsolute(dateTime2), equals('Dec 1, 2023'));
      });
    });

    group('formatDetailed', () {
      test('should format date with time in detailed format', () {
        final dateTime = DateTime(2024, 3, 15, 14, 30);
        expect(
          DateFormatter.formatDetailed(dateTime),
          equals('Mar 15, 2024 at 2:30 PM'),
        );

        final dateTime2 = DateTime(2023, 12, 1, 9, 15);
        expect(
          DateFormatter.formatDetailed(dateTime2),
          equals('Dec 1, 2023 at 9:15 AM'),
        );

        final midnight = DateTime(2024, 1, 1, 0, 0);
        expect(
          DateFormatter.formatDetailed(midnight),
          equals('Jan 1, 2024 at 12:00 AM'),
        );
      });
    });

    group('getSampleRelativeDates', () {
      test('should return a list of sample relative dates', () {
        final samples = DateFormatter.getSampleRelativeDates();
        expect(samples, isA<List<String>>());
        expect(samples.length, greaterThan(0));
        expect(samples.every((sample) => sample.isNotEmpty), isTrue);
      });
    });
  });
}
