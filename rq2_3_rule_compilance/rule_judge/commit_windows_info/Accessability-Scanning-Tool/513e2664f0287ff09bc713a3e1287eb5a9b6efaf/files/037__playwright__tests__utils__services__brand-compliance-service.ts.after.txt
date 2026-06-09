/**
 * Interface for color contrast results
 */
export interface ContrastResult {
  /** The contrast ratio */
  ratio: number;
  /** Whether it meets WCAG AA standards (4.5:1 for normal text) */
  meetsAA: boolean;
  /** Whether it meets WCAG AAA standards (7:1 for normal text) */
  meetsAAA: boolean;
  /** The foreground color */
  foreground: string;
  /** The background color */
  background: string;
}

/**
 * Interface for brand color validation results
 */
export interface BrandColorValidation {
  /** Whether all brand colors meet WCAG compliance */
  isCompliant: boolean;
  /** Individual color test results */
  colorTests: {
    colorName: string;
    onWhite: ContrastResult;
    onBlack: ContrastResult;
    recommendations: string[];
  }[];
  /** Summary of compliance status */
  summary: {
    totalColors: number;
    compliantColors: number;
    nonCompliantColors: number;
  };
}

/**
 * Singleton service for brand compliance validation
 * Ensures all brand colors maintain WCAG 2.1 AA compliance
 */
export class BrandComplianceService {
  private static instance: BrandComplianceService;

  // Brand colors from the rules
  private readonly BRAND_COLORS = {
    'Primary Purple': '#1e214d',
    'Primary Magenta': '#db0064',
    'Primary Yellow': '#fcc700',
    'Secondary Dark Purple': '#1b1532',
    'Secondary Orange': '#ff8a00',
    'Secondary Light Blue': '#ebf7fc',
    'Supporting Green': '#22b094',
    'Supporting Blue': '#00bcff',
  };

  // WCAG contrast ratio requirements
  private readonly WCAG_AA_NORMAL = 4.5;
  private readonly WCAG_AAA_NORMAL = 7.0;

  private constructor() {}

  /**
   * Gets the singleton instance of BrandComplianceService
   * @returns The singleton BrandComplianceService instance
   */
  static getInstance(): BrandComplianceService {
    if (!BrandComplianceService.instance) {
      BrandComplianceService.instance = new BrandComplianceService();
    }
    return BrandComplianceService.instance;
  }

  /**
   * Validates all brand colors for WCAG compliance
   * @returns BrandColorValidation with compliance results
   */
  validateBrandColors(): BrandColorValidation {
    const colorTests = Object.entries(this.BRAND_COLORS).map(([colorName, hexColor]) => {
      const onWhite = this.calculateContrast(hexColor, '#ffffff');
      const onBlack = this.calculateContrast(hexColor, '#000000');

      const recommendations: string[] = [];

      if (!onWhite.meetsAA && !onBlack.meetsAA) {
        recommendations.push(
          'Consider using this color only for large text or decorative elements'
        );
        recommendations.push(
          'Pair with a contrasting background color that meets WCAG AA standards'
        );
      } else if (!onWhite.meetsAA) {
        recommendations.push('Avoid using on white backgrounds for normal text');
        recommendations.push('Use with dark backgrounds or for large text only');
      } else if (!onBlack.meetsAA) {
        recommendations.push('Avoid using on black backgrounds for normal text');
        recommendations.push('Use with light backgrounds or for large text only');
      } else {
        recommendations.push('Meets WCAG AA standards - safe to use with proper backgrounds');
      }

      return {
        colorName,
        onWhite,
        onBlack,
        recommendations,
      };
    });

    const compliantColors = colorTests.filter(
      test => test.onWhite.meetsAA || test.onBlack.meetsAA
    ).length;

    const nonCompliantColors = colorTests.length - compliantColors;

    return {
      isCompliant: nonCompliantColors === 0,
      colorTests,
      summary: {
        totalColors: colorTests.length,
        compliantColors,
        nonCompliantColors,
      },
    };
  }

  /**
   * Validates a specific color combination for WCAG compliance
   * @param foreground Foreground color (hex)
   * @param background Background color (hex)
   * @returns ContrastResult with compliance information
   */
  validateColorCombination(foreground: string, background: string): ContrastResult {
    return this.calculateContrast(foreground, background);
  }

  /**
   * Gets recommendations for safe color usage in accessibility testing reports
   * @returns Array of usage recommendations
   */
  getBrandColorUsageRecommendations(): string[] {
    const validation = this.validateBrandColors();
    const recommendations: string[] = [];

    recommendations.push('Brand Color Usage Guidelines for Accessibility Compliance:');
    recommendations.push('');

    validation.colorTests.forEach(test => {
      recommendations.push(
        `${test.colorName} (${this.BRAND_COLORS[test.colorName as keyof typeof this.BRAND_COLORS]}):`
      );
      test.recommendations.forEach(rec => recommendations.push(`  • ${rec}`));
      recommendations.push('');
    });

    if (!validation.isCompliant) {
      recommendations.push('⚠️  Some brand colors may not meet WCAG AA standards for normal text.');
      recommendations.push(
        '   Always test color combinations before use in accessibility reports.'
      );
      recommendations.push(
        '   Consider using these colors for large text, backgrounds, or decorative elements.'
      );
    }

    return recommendations;
  }

  /**
   * Calculates contrast ratio between two colors
   * @param foreground Foreground color (hex)
   * @param background Background color (hex)
   * @returns ContrastResult with ratio and compliance information
   */
  private calculateContrast(foreground: string, background: string): ContrastResult {
    const fgLuminance = this.getLuminance(foreground);
    const bgLuminance = this.getLuminance(background);

    const lighter = Math.max(fgLuminance, bgLuminance);
    const darker = Math.min(fgLuminance, bgLuminance);

    const ratio = (lighter + 0.05) / (darker + 0.05);

    return {
      ratio: Math.round(ratio * 100) / 100,
      meetsAA: ratio >= this.WCAG_AA_NORMAL,
      meetsAAA: ratio >= this.WCAG_AAA_NORMAL,
      foreground,
      background,
    };
  }

  /**
   * Calculates the relative luminance of a color
   * @param hexColor Color in hex format
   * @returns Relative luminance value
   */
  private getLuminance(hexColor: string): number {
    // Remove # if present
    const hex = hexColor.replace('#', '');

    // Convert to RGB
    const r = parseInt(hex.substr(0, 2), 16) / 255;
    const g = parseInt(hex.substr(2, 2), 16) / 255;
    const b = parseInt(hex.substr(4, 2), 16) / 255;

    // Apply gamma correction
    const rLinear = r <= 0.03928 ? r / 12.92 : Math.pow((r + 0.055) / 1.055, 2.4);
    const gLinear = g <= 0.03928 ? g / 12.92 : Math.pow((g + 0.055) / 1.055, 2.4);
    const bLinear = b <= 0.03928 ? b / 12.92 : Math.pow((b + 0.055) / 1.055, 2.4);

    // Calculate luminance
    return 0.2126 * rLinear + 0.7152 * gLinear + 0.0722 * bLinear;
  }

  /**
   * Gets brand colors that are safe to use with white backgrounds
   * @returns Array of color names and hex values
   */
  getSafeColorsForWhiteBackground(): Array<{ name: string; hex: string }> {
    const validation = this.validateBrandColors();
    return validation.colorTests
      .filter(test => test.onWhite.meetsAA)
      .map(test => ({
        name: test.colorName,
        hex: this.BRAND_COLORS[test.colorName as keyof typeof this.BRAND_COLORS],
      }));
  }

  /**
   * Gets brand colors that are safe to use with dark backgrounds
   * @returns Array of color names and hex values
   */
  getSafeColorsForDarkBackground(): Array<{ name: string; hex: string }> {
    const validation = this.validateBrandColors();
    return validation.colorTests
      .filter(test => test.onBlack.meetsAA)
      .map(test => ({
        name: test.colorName,
        hex: this.BRAND_COLORS[test.colorName as keyof typeof this.BRAND_COLORS],
      }));
  }
}
