import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/utils/spacing_validator.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('SpacingValidator', () {
    group('isValidSpacing', () {
      testWidgets('returns true for valid spacing values', (tester) async {
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing4), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing8), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing12), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing16), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing20), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing24), isTrue);
        expect(SpacingValidator.isValidSpacing(GHTokens.spacing32), isTrue);
      });

      testWidgets('returns false for invalid spacing values', (tester) async {
        expect(SpacingValidator.isValidSpacing(5.0), isFalse);
        expect(SpacingValidator.isValidSpacing(15.0), isFalse);
        expect(SpacingValidator.isValidSpacing(23.0), isFalse);
        expect(SpacingValidator.isValidSpacing(31.0), isFalse);
      });
    });

    group('isMultipleOfFour', () {
      testWidgets('returns true for multiples of 4', (tester) async {
        expect(SpacingValidator.isMultipleOfFour(4.0), isTrue);
        expect(SpacingValidator.isMultipleOfFour(8.0), isTrue);
        expect(SpacingValidator.isMultipleOfFour(12.0), isTrue);
        expect(SpacingValidator.isMultipleOfFour(16.0), isTrue);
        expect(SpacingValidator.isMultipleOfFour(28.0), isTrue);
      });

      testWidgets('returns false for non-multiples of 4', (tester) async {
        expect(SpacingValidator.isMultipleOfFour(3.0), isFalse);
        expect(SpacingValidator.isMultipleOfFour(5.0), isFalse);
        expect(SpacingValidator.isMultipleOfFour(7.0), isFalse);
        expect(SpacingValidator.isMultipleOfFour(15.0), isFalse);
      });
    });

    group('getNearestValidSpacing', () {
      testWidgets('returns same value for valid spacing', (tester) async {
        expect(
          SpacingValidator.getNearestValidSpacing(GHTokens.spacing16),
          equals(GHTokens.spacing16),
        );
        expect(
          SpacingValidator.getNearestValidSpacing(GHTokens.spacing24),
          equals(GHTokens.spacing24),
        );
      });

      testWidgets('returns nearest valid spacing for invalid values', (
        tester,
      ) async {
        expect(
          SpacingValidator.getNearestValidSpacing(6.0),
          equals(GHTokens.spacing4),
        );
        expect(
          SpacingValidator.getNearestValidSpacing(10.0),
          equals(GHTokens.spacing8),
        );
        expect(
          SpacingValidator.getNearestValidSpacing(14.0),
          equals(GHTokens.spacing12),
        );
        expect(
          SpacingValidator.getNearestValidSpacing(18.0),
          equals(GHTokens.spacing16),
        );
        expect(
          SpacingValidator.getNearestValidSpacing(22.0),
          equals(GHTokens.spacing20),
        );
      });
    });

    group('validateSpacing', () {
      testWidgets('returns valid result for allowed spacing', (tester) async {
        final result = SpacingValidator.validateSpacing(GHTokens.spacing16);

        expect(result.isValid, isTrue);
        expect(result.inputValue, equals(GHTokens.spacing16));
        expect(result.suggestedValue, equals(GHTokens.spacing16));
        expect(result.message, contains('standards'));
      });

      testWidgets('returns invalid result with suggestion for 4dp multiple', (
        tester,
      ) async {
        final result = SpacingValidator.validateSpacing(
          28.0,
        ); // Multiple of 4 but not in tokens

        expect(result.isValid, isFalse);
        expect(result.inputValue, equals(28.0));
        expect(
          result.suggestedValue,
          equals(GHTokens.spacing24),
        ); // Nearest valid (24 is closer than 32)
        expect(result.message, contains('multiple of 4dp'));
        expect(result.message, contains('24.0dp'));
      });

      testWidgets('returns invalid result for non-4dp values', (tester) async {
        final result = SpacingValidator.validateSpacing(
          15.0,
        ); // Not multiple of 4

        expect(result.isValid, isFalse);
        expect(result.inputValue, equals(15.0));
        expect(
          result.suggestedValue,
          equals(GHTokens.spacing16),
        ); // Nearest valid
        expect(result.message, contains('does not follow 4dp grid'));
        expect(result.message, contains('16.0dp'));
      });
    });

    group('getAllowedSpacingValues', () {
      testWidgets('returns immutable list of allowed values', (tester) async {
        final allowedValues = SpacingValidator.getAllowedSpacingValues();

        expect(allowedValues, contains(GHTokens.spacing4));
        expect(allowedValues, contains(GHTokens.spacing8));
        expect(allowedValues, contains(GHTokens.spacing16));
        expect(allowedValues, contains(GHTokens.spacing32));

        // Should be immutable
        expect(() => allowedValues.add(100.0), throwsUnsupportedError);
      });
    });
  });

  group('SpacingValidationResult', () {
    testWidgets('has correct string representation', (tester) async {
      const result = SpacingValidationResult(
        isValid: false,
        inputValue: 15.0,
        suggestedValue: 16.0,
        message: 'Test message',
      );

      final stringRep = result.toString();
      expect(stringRep, contains('isValid: false'));
      expect(stringRep, contains('input: 15.0dp'));
      expect(stringRep, contains('suggested: 16.0dp'));
      expect(stringRep, contains('Test message'));
    });
  });

  group('SpacingValidation extension', () {
    testWidgets('validate() returns correct result', (tester) async {
      final result = 15.0.validate();

      expect(result.isValid, isFalse);
      expect(result.inputValue, equals(15.0));
      expect(result.suggestedValue, equals(16.0));
    });

    testWidgets('isValidSpacing() returns correct boolean', (tester) async {
      expect(GHTokens.spacing16.isValidSpacing(), isTrue);
      expect(15.0.isValidSpacing(), isFalse);
    });

    testWidgets('toValidSpacing() returns nearest valid value', (tester) async {
      expect(GHTokens.spacing16.toValidSpacing(), equals(GHTokens.spacing16));
      expect(15.0.toValidSpacing(), equals(16.0));
      expect(10.0.toValidSpacing(), equals(8.0));
    });
  });
}
