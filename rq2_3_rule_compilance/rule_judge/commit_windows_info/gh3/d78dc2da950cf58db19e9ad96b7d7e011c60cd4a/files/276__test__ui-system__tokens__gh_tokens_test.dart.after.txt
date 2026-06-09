import 'package:flutter_test/flutter_test.dart';
import 'package:gh3/src/ui-system/tokens/gh_tokens.dart';

void main() {
  group('GHTokens Spacing Constants', () {
    test('all spacing constants should follow 4dp grid system', () {
      // Test that all spacing values are multiples of 4
      expect(GHTokens.spacing4 % 4, equals(0.0));
      expect(GHTokens.spacing8 % 4, equals(0.0));
      expect(GHTokens.spacing12 % 4, equals(0.0));
      expect(GHTokens.spacing16 % 4, equals(0.0));
      expect(GHTokens.spacing20 % 4, equals(0.0));
      expect(GHTokens.spacing24 % 4, equals(0.0));
      expect(GHTokens.spacing32 % 4, equals(0.0));
    });

    test('spacing constants should have correct values', () {
      // Test individual values
      expect(GHTokens.spacing4, equals(4.0));
      expect(GHTokens.spacing8, equals(8.0));
      expect(GHTokens.spacing12, equals(12.0));
      expect(GHTokens.spacing16, equals(16.0));
      expect(GHTokens.spacing20, equals(20.0));
      expect(GHTokens.spacing24, equals(24.0));
      expect(GHTokens.spacing32, equals(32.0));
    });

    test('spacing constants should be in ascending order', () {
      // Test that spacing values increase in logical order
      expect(GHTokens.spacing4, lessThan(GHTokens.spacing8));
      expect(GHTokens.spacing8, lessThan(GHTokens.spacing12));
      expect(GHTokens.spacing12, lessThan(GHTokens.spacing16));
      expect(GHTokens.spacing16, lessThan(GHTokens.spacing20));
      expect(GHTokens.spacing20, lessThan(GHTokens.spacing24));
      expect(GHTokens.spacing24, lessThan(GHTokens.spacing32));
    });

    test('spacing constants should be positive values', () {
      // Test that all spacing values are positive
      expect(GHTokens.spacing4, greaterThan(0.0));
      expect(GHTokens.spacing8, greaterThan(0.0));
      expect(GHTokens.spacing12, greaterThan(0.0));
      expect(GHTokens.spacing16, greaterThan(0.0));
      expect(GHTokens.spacing20, greaterThan(0.0));
      expect(GHTokens.spacing24, greaterThan(0.0));
      expect(GHTokens.spacing32, greaterThan(0.0));
    });
  });

  group('GHTokens Radius Constants', () {
    test('all radius constants should follow 4dp grid system', () {
      // Test that all radius values are multiples of 4
      expect(GHTokens.radius4 % 4, equals(0.0));
      expect(GHTokens.radius8 % 4, equals(0.0));
      expect(GHTokens.radius12 % 4, equals(0.0));
      expect(GHTokens.radius16 % 4, equals(0.0));
    });

    test('radius constants should have correct values', () {
      // Test individual values
      expect(GHTokens.radius4, equals(4.0));
      expect(GHTokens.radius8, equals(8.0));
      expect(GHTokens.radius12, equals(12.0));
      expect(GHTokens.radius16, equals(16.0));
    });
  });

  group('GHTokens Elevation Constants', () {
    test('elevation constants should be valid and ordered', () {
      expect(GHTokens.elevation0, equals(0.0));
      expect(GHTokens.elevation1, equals(1.0));
      expect(GHTokens.elevation3, equals(3.0));
      expect(GHTokens.elevation8, equals(8.0));

      expect(GHTokens.elevation0, lessThan(GHTokens.elevation1));
      expect(GHTokens.elevation1, lessThan(GHTokens.elevation3));
      expect(GHTokens.elevation3, lessThan(GHTokens.elevation8));
    });
  });
}
