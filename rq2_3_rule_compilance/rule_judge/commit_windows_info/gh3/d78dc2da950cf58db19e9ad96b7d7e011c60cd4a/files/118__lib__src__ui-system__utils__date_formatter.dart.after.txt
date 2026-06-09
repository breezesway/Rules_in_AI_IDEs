/// Utility class for formatting dates in GitHub-style relative format.
///
/// This class provides methods to format DateTime objects into human-readable
/// relative time strings like "2 hours ago", "3 days ago", etc.
class DateFormatter {
  // Private constructor to prevent instantiation
  const DateFormatter._();

  /// Formats a DateTime into a relative time string.
  ///
  /// Examples:
  /// - "Just now" (< 1 minute)
  /// - "2 minutes ago"
  /// - "3 hours ago"
  /// - "5 days ago"
  /// - "Last week"
  /// - "2 months ago"
  /// - "Last year"
  static String formatRelative(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inSeconds < 60) {
      return 'Just now';
    } else if (difference.inMinutes < 60) {
      final minutes = difference.inMinutes;
      return minutes == 1 ? '1 minute ago' : '$minutes minutes ago';
    } else if (difference.inHours < 24) {
      final hours = difference.inHours;
      return hours == 1 ? '1 hour ago' : '$hours hours ago';
    } else if (difference.inDays < 7) {
      final days = difference.inDays;
      return days == 1 ? '1 day ago' : '$days days ago';
    } else if (difference.inDays < 30) {
      final weeks = (difference.inDays / 7).floor();
      return weeks == 1 ? 'Last week' : '$weeks weeks ago';
    } else if (difference.inDays < 365) {
      final months = (difference.inDays / 30).floor();
      return months == 1 ? 'Last month' : '$months months ago';
    } else {
      final years = (difference.inDays / 365).floor();
      return years == 1 ? 'Last year' : '$years years ago';
    }
  }

  /// Formats a DateTime into a short relative time string.
  ///
  /// Examples:
  /// - "now" (< 1 minute)
  /// - "2m"
  /// - "3h"
  /// - "5d"
  /// - "2w"
  /// - "3mo"
  /// - "1y"
  static String formatRelativeShort(DateTime dateTime) {
    final now = DateTime.now();
    final difference = now.difference(dateTime);

    if (difference.inSeconds < 60) {
      return 'now';
    } else if (difference.inMinutes < 60) {
      return '${difference.inMinutes}m';
    } else if (difference.inHours < 24) {
      return '${difference.inHours}h';
    } else if (difference.inDays < 7) {
      return '${difference.inDays}d';
    } else if (difference.inDays < 30) {
      final weeks = (difference.inDays / 7).floor();
      return '${weeks}w';
    } else if (difference.inDays < 365) {
      final months = (difference.inDays / 30).floor();
      return '${months}mo';
    } else {
      final years = (difference.inDays / 365).floor();
      return '${years}y';
    }
  }

  /// Formats a DateTime into an absolute date string.
  ///
  /// Examples:
  /// - "Jan 15, 2024"
  /// - "Dec 3, 2023"
  static String formatAbsolute(DateTime dateTime) {
    const months = [
      'Jan',
      'Feb',
      'Mar',
      'Apr',
      'May',
      'Jun',
      'Jul',
      'Aug',
      'Sep',
      'Oct',
      'Nov',
      'Dec',
    ];

    final month = months[dateTime.month - 1];
    final day = dateTime.day;
    final year = dateTime.year;

    return '$month $day, $year';
  }

  /// Formats a DateTime into a detailed timestamp.
  ///
  /// Examples:
  /// - "Jan 15, 2024 at 2:30 PM"
  /// - "Dec 3, 2023 at 9:15 AM"
  static String formatDetailed(DateTime dateTime) {
    final absoluteDate = formatAbsolute(dateTime);
    final hour = dateTime.hour;
    final minute = dateTime.minute.toString().padLeft(2, '0');
    final period = hour >= 12 ? 'PM' : 'AM';
    final displayHour = hour == 0 ? 12 : (hour > 12 ? hour - 12 : hour);

    return '$absoluteDate at $displayHour:$minute $period';
  }

  /// Returns a list of sample relative date strings for demonstration.
  static List<String> getSampleRelativeDates() {
    final now = DateTime.now();
    return [
      formatRelative(now.subtract(const Duration(seconds: 30))),
      formatRelative(now.subtract(const Duration(minutes: 5))),
      formatRelative(now.subtract(const Duration(minutes: 45))),
      formatRelative(now.subtract(const Duration(hours: 2))),
      formatRelative(now.subtract(const Duration(hours: 8))),
      formatRelative(now.subtract(const Duration(days: 1))),
      formatRelative(now.subtract(const Duration(days: 3))),
      formatRelative(now.subtract(const Duration(days: 8))),
      formatRelative(now.subtract(const Duration(days: 21))),
      formatRelative(now.subtract(const Duration(days: 45))),
      formatRelative(now.subtract(const Duration(days: 120))),
      formatRelative(now.subtract(const Duration(days: 400))),
    ];
  }
}
