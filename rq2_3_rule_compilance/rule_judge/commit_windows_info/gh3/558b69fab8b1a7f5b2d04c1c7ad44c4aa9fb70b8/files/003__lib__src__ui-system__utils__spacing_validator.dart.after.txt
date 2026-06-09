import '../tokens/gh_tokens.dart';

/// Utility class to validate that spacing values follow the 4dp grid system.
///
/// This validator helps ensure design system compliance by checking that
/// all spacing values are multiples of 4dp and use predefined tokens.
class SpacingValidator {
  /// Standard 4dp grid spacing values that are allowed
  static const List<double> _allowedSpacing = [
    GHTokens.spacing4, // 4dp
    GHTokens.spacing8, // 8dp
    GHTokens.spacing12, // 12dp
    GHTokens.spacing16, // 16dp
    GHTokens.spacing20, // 20dp
    GHTokens.spacing24, // 24dp
    GHTokens.spacing32, // 32dp
  ];

  /// Checks if a spacing value is compliant with the 4dp grid system
  static bool isValidSpacing(double spacing) {
    return _allowedSpacing.contains(spacing);
  }

  /// Checks if a spacing value is a multiple of 4
  static bool isMultipleOfFour(double spacing) {
    return spacing % 4 == 0;
  }

  /// Gets the nearest valid spacing value for a given input
  static double getNearestValidSpacing(double spacing) {
    if (isValidSpacing(spacing)) {
      return spacing;
    }

    // Find the closest valid spacing
    double closest = _allowedSpacing.first;
    double minDifference = (spacing - closest).abs();

    for (final validSpacing in _allowedSpacing) {
      final difference = (spacing - validSpacing).abs();
      if (difference < minDifference) {
        minDifference = difference;
        closest = validSpacing;
      }
    }

    return closest;
  }

  /// Gets all allowed spacing values
  static List<double> getAllowedSpacingValues() {
    return List.unmodifiable(_allowedSpacing);
  }

  /// Validates that a spacing value follows design standards
  static SpacingValidationResult validateSpacing(double spacing) {
    if (isValidSpacing(spacing)) {
      return SpacingValidationResult(
        isValid: true,
        inputValue: spacing,
        suggestedValue: spacing,
        message: 'Spacing follows design system standards',
      );
    }

    if (isMultipleOfFour(spacing)) {
      final nearest = getNearestValidSpacing(spacing);
      return SpacingValidationResult(
        isValid: false,
        inputValue: spacing,
        suggestedValue: nearest,
        message:
            'Spacing is a multiple of 4dp but not in allowed tokens. Use ${nearest}dp instead.',
      );
    }

    final nearest = getNearestValidSpacing(spacing);
    return SpacingValidationResult(
      isValid: false,
      inputValue: spacing,
      suggestedValue: nearest,
      message:
          'Spacing does not follow 4dp grid. Use ${nearest}dp for standards compliance.',
    );
  }
}

/// Result of spacing validation containing validation status and suggestions
class SpacingValidationResult {
  /// Whether the spacing value is valid
  final bool isValid;

  /// The original input spacing value
  final double inputValue;

  /// The suggested spacing value for compliance
  final double suggestedValue;

  /// Human-readable validation message
  final String message;

  const SpacingValidationResult({
    required this.isValid,
    required this.inputValue,
    required this.suggestedValue,
    required this.message,
  });

  @override
  String toString() {
    return 'SpacingValidationResult(isValid: $isValid, input: ${inputValue}dp, '
        'suggested: ${suggestedValue}dp, message: "$message")';
  }
}

/// Extension on double to provide spacing validation methods
extension SpacingValidation on double {
  /// Validates this spacing value against design standards
  SpacingValidationResult validate() {
    return SpacingValidator.validateSpacing(this);
  }

  /// Returns true if this spacing value follows design standards
  bool isValidSpacing() {
    return SpacingValidator.isValidSpacing(this);
  }

  /// Returns the nearest valid spacing value
  double toValidSpacing() {
    return SpacingValidator.getNearestValidSpacing(this);
  }
}
