/// Utility class for formatting numbers in GitHub-style compact format.
///
/// This class provides methods to format large numbers into human-readable
/// compact strings like "1.2k", "45.2k", "3.4M", etc.
class NumberFormatter {
  // Private constructor to prevent instantiation
  const NumberFormatter._();

  /// Formats a number into a compact string representation.
  ///
  /// Examples:
  /// - 42 → "42"
  /// - 1,234 → "1.2k"
  /// - 45,678 → "45.7k"
  /// - 1,234,567 → "1.2M"
  /// - 2,500,000,000 → "2.5B"
  static String formatCompact(int number) {
    if (number < 0) {
      return '-${formatCompact(-number)}';
    }

    if (number < 1000) {
      return number.toString();
    } else if (number < 1000000) {
      final k = number / 1000;
      if (k >= 100) {
        return '${k.round()}k';
      } else if (k % 1 == 0) {
        return '${k.toInt()}k';
      } else {
        return '${k.toStringAsFixed(1)}k';
      }
    } else if (number < 1000000000) {
      final m = number / 1000000;
      if (m >= 100) {
        return '${m.round()}M';
      } else if (m % 1 == 0) {
        return '${m.toInt()}M';
      } else {
        return '${m.toStringAsFixed(1)}M';
      }
    } else {
      final b = number / 1000000000;
      if (b >= 100) {
        return '${b.round()}B';
      } else if (b % 1 == 0) {
        return '${b.toInt()}B';
      } else {
        return '${b.toStringAsFixed(1)}B';
      }
    }
  }

  /// Formats a number with thousands separators.
  ///
  /// Examples:
  /// - 1234 → "1,234"
  /// - 1234567 → "1,234,567"
  static String formatWithCommas(int number) {
    if (number < 0) {
      return '-${formatWithCommas(-number)}';
    }

    final str = number.toString();
    final result = StringBuffer();

    for (int i = 0; i < str.length; i++) {
      if (i > 0 && (str.length - i) % 3 == 0) {
        result.write(',');
      }
      result.write(str[i]);
    }

    return result.toString();
  }

  /// Formats a number as a percentage.
  ///
  /// Examples:
  /// - 0.1234 → "12.3%"
  /// - 0.5 → "50%"
  /// - 1.0 → "100%"
  static String formatPercentage(double value, {int decimalPlaces = 1}) {
    final percentage = value * 100;
    if (percentage % 1 == 0) {
      return '${percentage.toInt()}%';
    } else {
      return '${percentage.toStringAsFixed(decimalPlaces)}%';
    }
  }

  /// Formats file size in bytes to human-readable format.
  ///
  /// Examples:
  /// - 1024 → "1 KB"
  /// - 1048576 → "1 MB"
  /// - 1073741824 → "1 GB"
  static String formatFileSize(int bytes) {
    if (bytes < 0) {
      return '-${formatFileSize(-bytes)}';
    }

    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    double size = bytes.toDouble();
    int unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }

    if (size % 1 == 0) {
      return '${size.toInt()} ${units[unitIndex]}';
    } else {
      return '${size.toStringAsFixed(1)} ${units[unitIndex]}';
    }
  }

  /// Returns a list of sample formatted numbers for demonstration.
  static List<String> getSampleFormattedNumbers() {
    return [
      formatCompact(42),
      formatCompact(123),
      formatCompact(1234),
      formatCompact(12345),
      formatCompact(123456),
      formatCompact(1234567),
      formatCompact(12345678),
      formatCompact(123456789),
      formatCompact(1234567890),
    ];
  }

  /// Returns a list of sample GitHub-style statistics for demonstration.
  static List<Map<String, dynamic>> getSampleGitHubStats() {
    return [
      {'label': 'stars', 'value': 218000, 'formatted': formatCompact(218000)},
      {'label': 'forks', 'value': 45200, 'formatted': formatCompact(45200)},
      {'label': 'watchers', 'value': 8900, 'formatted': formatCompact(8900)},
      {'label': 'issues', 'value': 1234, 'formatted': formatCompact(1234)},
      {'label': 'pull requests', 'value': 567, 'formatted': formatCompact(567)},
      {'label': 'commits', 'value': 89012, 'formatted': formatCompact(89012)},
      {
        'label': 'contributors',
        'value': 2345,
        'formatted': formatCompact(2345),
      },
      {'label': 'releases', 'value': 89, 'formatted': formatCompact(89)},
      {
        'label': 'downloads',
        'value': 5600000,
        'formatted': formatCompact(5600000),
      },
      {'label': 'followers', 'value': 12300, 'formatted': formatCompact(12300)},
      {'label': 'following', 'value': 456, 'formatted': formatCompact(456)},
      {'label': 'repositories', 'value': 234, 'formatted': formatCompact(234)},
    ];
  }
}
