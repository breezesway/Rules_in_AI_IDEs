import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';
import { BrandComplianceService } from '../../playwright/tests/utils/services/brand-compliance-service';

describe('BrandComplianceService', () => {
  let brandService: BrandComplianceService;

  beforeEach(() => {
    // Reset singleton instance before each test
    (BrandComplianceService as any).instance = undefined;
    brandService = BrandComplianceService.getInstance();
  });

  afterEach(() => {
    // Clean up singleton instance after each test
    (BrandComplianceService as any).instance = undefined;
  });

  describe('Singleton Pattern', () => {
    it('should return the same instance on multiple calls', () => {
      const instance1 = BrandComplianceService.getInstance();
      const instance2 = BrandComplianceService.getInstance();

      expect(instance1).toBe(instance2);
    });

    it('should not allow direct instantiation', () => {
      expect(() => new (BrandComplianceService as any)()).toThrow();
    });
  });

  describe('Brand Color Validation', () => {
    it('should validate all brand colors for WCAG compliance', () => {
      const validation = brandService.validateBrandColors();

      expect(validation).toHaveProperty('isCompliant');
      expect(validation).toHaveProperty('colorTests');
      expect(validation).toHaveProperty('summary');
      expect(validation.colorTests).toHaveLength(8); // 8 brand colors
      expect(validation.summary.totalColors).toBe(8);
    });

    it('should return detailed results for each brand color', () => {
      const validation = brandService.validateBrandColors();

      validation.colorTests.forEach(test => {
        expect(test).toHaveProperty('colorName');
        expect(test).toHaveProperty('onWhite');
        expect(test).toHaveProperty('onBlack');
        expect(test).toHaveProperty('recommendations');
        expect(Array.isArray(test.recommendations)).toBe(true);
      });
    });

    it('should include all expected brand colors', () => {
      const validation = brandService.validateBrandColors();
      const colorNames = validation.colorTests.map(test => test.colorName);

      expect(colorNames).toContain('Primary Purple');
      expect(colorNames).toContain('Primary Magenta');
      expect(colorNames).toContain('Primary Yellow');
      expect(colorNames).toContain('Secondary Dark Purple');
      expect(colorNames).toContain('Secondary Orange');
      expect(colorNames).toContain('Secondary Light Blue');
      expect(colorNames).toContain('Supporting Green');
      expect(colorNames).toContain('Supporting Blue');
    });

    it('should provide proper summary statistics', () => {
      const validation = brandService.validateBrandColors();

      expect(validation.summary.totalColors).toBe(8);
      expect(validation.summary.compliantColors).toBeGreaterThanOrEqual(0);
      expect(validation.summary.nonCompliantColors).toBeGreaterThanOrEqual(0);
      expect(validation.summary.compliantColors + validation.summary.nonCompliantColors).toBe(8);
    });
  });

  describe('Color Contrast Calculation', () => {
    it('should calculate contrast ratio for high contrast colors', () => {
      const result = brandService.calculateContrast('#000000', '#ffffff');

      expect(result.ratio).toBeCloseTo(21, 0); // Black on white has 21:1 contrast
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(true);
      expect(result.foreground).toBe('#000000');
      expect(result.background).toBe('#ffffff');
    });

    it('should calculate contrast ratio for same colors', () => {
      const result = brandService.calculateContrast('#ffffff', '#ffffff');

      expect(result.ratio).toBe(1);
      expect(result.meetsAA).toBe(false);
      expect(result.meetsAAA).toBe(false);
      expect(result.foreground).toBe('#ffffff');
      expect(result.background).toBe('#ffffff');
    });

    it('should handle 3-digit hex colors', () => {
      const result = brandService.calculateContrast('#000', '#fff');

      expect(result.ratio).toBeCloseTo(21, 0);
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(true);
    });

    it('should handle colors without # prefix', () => {
      const result = brandService.calculateContrast('000000', 'ffffff');

      expect(result.ratio).toBeCloseTo(21, 0);
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(true);
    });

    it('should handle mixed case hex colors', () => {
      const result = brandService.calculateContrast('#AbCdEf', '#123456');

      expect(result.ratio).toBeGreaterThan(0);
      expect(result.foreground).toBe('#AbCdEf');
      expect(result.background).toBe('#123456');
    });
  });

  describe('WCAG Compliance Levels', () => {
    it('should correctly identify AA compliance', () => {
      // Test a combination that should meet AA but not AAA
      const result = brandService.calculateContrast('#767676', '#ffffff');

      expect(result.ratio).toBeGreaterThanOrEqual(4.5);
      expect(result.ratio).toBeLessThan(7);
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(false);
    });

    it('should correctly identify AAA compliance', () => {
      // Test a combination that should meet AAA
      const result = brandService.calculateContrast('#595959', '#ffffff');

      expect(result.ratio).toBeGreaterThanOrEqual(7);
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(true);
    });

    it('should correctly identify non-compliant colors', () => {
      // Test a combination that should not meet AA
      const result = brandService.calculateContrast('#cccccc', '#ffffff');

      expect(result.ratio).toBeLessThan(4.5);
      expect(result.meetsAA).toBe(false);
      expect(result.meetsAAA).toBe(false);
    });
  });

  describe('Brand Color Recommendations', () => {
    it('should provide recommendations for non-compliant colors', () => {
      const validation = brandService.validateBrandColors();

      validation.colorTests.forEach(test => {
        expect(test.recommendations).toBeDefined();
        expect(Array.isArray(test.recommendations)).toBe(true);
        expect(test.recommendations.length).toBeGreaterThan(0);
      });
    });

    it('should provide appropriate recommendations for colors that meet AA on both backgrounds', () => {
      const validation = brandService.validateBrandColors();

      const compliantColors = validation.colorTests.filter(
        test => test.onWhite.meetsAA && test.onBlack.meetsAA
      );

      compliantColors.forEach(test => {
        expect(test.recommendations).toContain(
          'Meets WCAG AA standards - safe to use with proper backgrounds'
        );
      });
    });

    it('should provide appropriate recommendations for colors that only work on white', () => {
      const validation = brandService.validateBrandColors();

      const whiteOnlyColors = validation.colorTests.filter(
        test => test.onWhite.meetsAA && !test.onBlack.meetsAA
      );

      whiteOnlyColors.forEach(test => {
        expect(
          test.recommendations.some(rec => rec.includes('Avoid using on black backgrounds'))
        ).toBe(true);
      });
    });

    it('should provide appropriate recommendations for colors that only work on black', () => {
      const validation = brandService.validateBrandColors();

      const blackOnlyColors = validation.colorTests.filter(
        test => !test.onWhite.meetsAA && test.onBlack.meetsAA
      );

      blackOnlyColors.forEach(test => {
        expect(
          test.recommendations.some(rec => rec.includes('Avoid using on white backgrounds'))
        ).toBe(true);
      });
    });

    it('should provide appropriate recommendations for colors that work on neither background', () => {
      const validation = brandService.validateBrandColors();

      const nonCompliantColors = validation.colorTests.filter(
        test => !test.onWhite.meetsAA && !test.onBlack.meetsAA
      );

      nonCompliantColors.forEach(test => {
        expect(
          test.recommendations.some(rec =>
            rec.includes('Consider using this color only for large text')
          )
        ).toBe(true);
      });
    });
  });

  describe('Brand Color Configuration', () => {
    it('should have the correct brand colors defined', () => {
      const brandColors = (brandService as any).BRAND_COLORS;

      expect(brandColors['Primary Purple']).toBe('#1e214d');
      expect(brandColors['Primary Magenta']).toBe('#db0064');
      expect(brandColors['Primary Yellow']).toBe('#fcc700');
      expect(brandColors['Secondary Dark Purple']).toBe('#1b1532');
      expect(brandColors['Secondary Orange']).toBe('#ff8a00');
      expect(brandColors['Secondary Light Blue']).toBe('#ebf7fc');
      expect(brandColors['Supporting Green']).toBe('#22b094');
      expect(brandColors['Supporting Blue']).toBe('#00bcff');
    });

    it('should have the correct WCAG thresholds defined', () => {
      const wcagAANormal = (brandService as any).WCAG_AA_NORMAL;
      const wcagAAANormal = (brandService as any).WCAG_AAA_NORMAL;

      expect(wcagAANormal).toBe(4.5);
      expect(wcagAAANormal).toBe(7.0);
    });
  });

  describe('Color Validation Methods', () => {
    it('should validate hex color format', () => {
      expect(brandService.isValidHexColor('#000000')).toBe(true);
      expect(brandService.isValidHexColor('#fff')).toBe(true);
      expect(brandService.isValidHexColor('#AbCdEf')).toBe(true);
      expect(brandService.isValidHexColor('000000')).toBe(true);
      expect(brandService.isValidHexColor('fff')).toBe(true);
    });

    it('should reject invalid hex colors', () => {
      expect(brandService.isValidHexColor('#gggggg')).toBe(false);
      expect(brandService.isValidHexColor('#12345')).toBe(false);
      expect(brandService.isValidHexColor('#1234567')).toBe(false);
      expect(brandService.isValidHexColor('not-a-color')).toBe(false);
      expect(brandService.isValidHexColor('')).toBe(false);
      expect(brandService.isValidHexColor(null as any)).toBe(false);
    });

    it('should normalize hex colors', () => {
      expect(brandService.normalizeHexColor('#000000')).toBe('#000000');
      expect(brandService.normalizeHexColor('000000')).toBe('#000000');
      expect(brandService.normalizeHexColor('#fff')).toBe('#ffffff');
      expect(brandService.normalizeHexColor('fff')).toBe('#ffffff');
      expect(brandService.normalizeHexColor('#AbC')).toBe('#aabbcc');
    });
  });

  describe('RGB Conversion', () => {
    it('should convert hex to RGB correctly', () => {
      expect(brandService.hexToRgb('#000000')).toEqual({ r: 0, g: 0, b: 0 });
      expect(brandService.hexToRgb('#ffffff')).toEqual({ r: 255, g: 255, b: 255 });
      expect(brandService.hexToRgb('#ff0000')).toEqual({ r: 255, g: 0, b: 0 });
      expect(brandService.hexToRgb('#00ff00')).toEqual({ r: 0, g: 255, b: 0 });
      expect(brandService.hexToRgb('#0000ff')).toEqual({ r: 0, g: 0, b: 255 });
    });

    it('should handle 3-digit hex colors', () => {
      expect(brandService.hexToRgb('#000')).toEqual({ r: 0, g: 0, b: 0 });
      expect(brandService.hexToRgb('#fff')).toEqual({ r: 255, g: 255, b: 255 });
      expect(brandService.hexToRgb('#f0f')).toEqual({ r: 255, g: 0, b: 255 });
    });

    it('should return null for invalid hex colors', () => {
      expect(brandService.hexToRgb('#gggggg')).toBeNull();
      expect(brandService.hexToRgb('not-a-color')).toBeNull();
      expect(brandService.hexToRgb('')).toBeNull();
    });
  });

  describe('Luminance Calculation', () => {
    it('should calculate luminance for basic colors', () => {
      const blackLuminance = brandService.calculateLuminance({ r: 0, g: 0, b: 0 });
      const whiteLuminance = brandService.calculateLuminance({ r: 255, g: 255, b: 255 });

      expect(blackLuminance).toBe(0);
      expect(whiteLuminance).toBe(1);
    });

    it('should calculate luminance for color values', () => {
      const redLuminance = brandService.calculateLuminance({ r: 255, g: 0, b: 0 });
      const greenLuminance = brandService.calculateLuminance({ r: 0, g: 255, b: 0 });
      const blueLuminance = brandService.calculateLuminance({ r: 0, g: 0, b: 255 });

      expect(redLuminance).toBeGreaterThan(0);
      expect(redLuminance).toBeLessThan(1);
      expect(greenLuminance).toBeGreaterThan(redLuminance);
      expect(blueLuminance).toBeGreaterThan(0);
      expect(blueLuminance).toBeLessThan(redLuminance);
    });
  });

  describe('Performance', () => {
    it('should validate brand colors quickly', () => {
      const startTime = Date.now();

      for (let i = 0; i < 100; i++) {
        brandService.validateBrandColors();
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    });

    it('should calculate contrast quickly', () => {
      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        brandService.calculateContrast('#000000', '#ffffff');
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    });
  });

  describe('Edge Cases', () => {
    it('should handle uppercase hex colors', () => {
      const result = brandService.calculateContrast('#FFFFFF', '#000000');

      expect(result.ratio).toBeCloseTo(21, 0);
      expect(result.meetsAA).toBe(true);
      expect(result.meetsAAA).toBe(true);
    });

    it('should handle mixed case hex colors', () => {
      const result = brandService.calculateContrast('#AbCdEf', '#123456');

      expect(result.ratio).toBeGreaterThan(0);
      expect(result.foreground).toBe('#AbCdEf');
      expect(result.background).toBe('#123456');
    });

    it('should handle edge case contrast ratios', () => {
      // Colors that are very close to the AA threshold
      const result = brandService.calculateContrast('#767676', '#ffffff');

      expect(result.ratio).toBeGreaterThan(4.4);
      expect(result.ratio).toBeLessThan(4.6);
      expect(result.meetsAA).toBe(true);
    });
  });
});
