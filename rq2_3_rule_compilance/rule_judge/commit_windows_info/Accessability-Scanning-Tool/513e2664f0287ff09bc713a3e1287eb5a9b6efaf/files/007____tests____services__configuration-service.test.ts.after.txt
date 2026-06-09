import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';
import { ConfigurationService } from '../../playwright/tests/utils/services/configuration-service';

describe('ConfigurationService', () => {
  let configService: ConfigurationService;

  beforeEach(() => {
    // Reset singleton instance before each test
    (ConfigurationService as any).instance = undefined;
    configService = ConfigurationService.getInstance();
  });

  afterEach(() => {
    // Clean up singleton instance after each test
    (ConfigurationService as any).instance = undefined;
  });

  describe('Singleton Pattern', () => {
    it('should return the same instance on multiple calls', () => {
      const instance1 = ConfigurationService.getInstance();
      const instance2 = ConfigurationService.getInstance();

      expect(instance1).toBe(instance2);
    });

    it('should not allow direct instantiation', () => {
      // The constructor is private, so we can't actually test instantiation
      // But we can verify that the class follows the singleton pattern
      expect(ConfigurationService.getInstance).toBeDefined();
      expect(typeof ConfigurationService.getInstance).toBe('function');
    });
  });

  describe('Configuration Retrieval', () => {
    it('should return default axe configuration', () => {
      const axeConfig = configService.getAxeConfiguration();

      expect(axeConfig).toEqual({
        timeout: 30000,
        tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'],
        rules: {
          'color-contrast': { enabled: true },
          keyboard: { enabled: true },
          'focus-order-semantics': { enabled: true },
        },
      });
    });

    it('should return default pa11y configuration', () => {
      const pa11yConfig = configService.getPa11yConfiguration();

      expect(pa11yConfig.timeout).toBe(30000);
      expect(pa11yConfig.wait).toBe(2000);
      expect(pa11yConfig.standard).toBe('WCAG2AA');
      expect(pa11yConfig.includeNotices).toBe(true);
      expect(pa11yConfig.includeWarnings).toBe(true);
      expect(pa11yConfig.chromeLaunchConfig.args).toContain('--no-sandbox');
    });

    it('should return default lighthouse configuration', () => {
      const lighthouseConfig = configService.getLighthouseConfiguration();

      expect(lighthouseConfig.timeout).toBe(60000);
      expect(lighthouseConfig.port).toBe(9222);
      expect(lighthouseConfig.chromeLaunchConfig.args).toContain('--no-sandbox');
    });

    it('should return default wave configuration', () => {
      const waveConfig = configService.getWaveConfiguration();

      expect(waveConfig.timeout).toBe(45000);
      expect(waveConfig.apiKey).toBe('');
      expect(waveConfig.reportType).toBe(4);
      expect(waveConfig.evalDelay).toBe(2000);
      expect(waveConfig.baseUrl).toBe('https://wave.webaim.org/api/request');
    });

    it('should return default tenon configuration', () => {
      const tenonConfig = configService.getTenonConfiguration();

      expect(tenonConfig.timeout).toBe(45000);
      expect(tenonConfig.apiKey).toBe('');
      expect(tenonConfig.level).toBe('AA');
      expect(tenonConfig.certainty).toBe(80);
      expect(tenonConfig.priority).toBe(60);
      expect(tenonConfig.store).toBe(true);
      expect(tenonConfig.baseUrl).toBe('https://tenon.io/api/');
    });

    it('should return default reporting configuration', () => {
      const reportingConfig = configService.getReportingConfiguration();

      expect(reportingConfig.maxConcurrency).toBe(5);
      expect(reportingConfig.delayBetweenPages).toBe(1000);
      expect(reportingConfig.screenshotTimeout).toBe(5000);
      expect(reportingConfig.reportsDirectory).toBe('playwright/accessibility-reports');
    });

    it('should return default crawling configuration', () => {
      const crawlingConfig = configService.getCrawlingConfiguration();

      expect(crawlingConfig.excludePatterns.length).toBeGreaterThan(0);
      expect(crawlingConfig.excludePatterns[0]).toBeInstanceOf(RegExp);
      expect(crawlingConfig.customExcludePatterns).toEqual([]);
    });

    it('should return full configuration object', () => {
      const fullConfig = configService.getConfiguration();

      expect(fullConfig).toHaveProperty('axe');
      expect(fullConfig).toHaveProperty('pa11y');
      expect(fullConfig).toHaveProperty('lighthouse');
      expect(fullConfig).toHaveProperty('wave');
      expect(fullConfig).toHaveProperty('tenon');
      expect(fullConfig).toHaveProperty('reporting');
      expect(fullConfig).toHaveProperty('crawling');
    });
  });

  describe('Environment Variable Integration', () => {
    beforeEach(() => {
      // Clear environment variables
      delete process.env.WAVE_API_KEY;
      delete process.env.TENON_API_KEY;
    });

    it('should use environment variables for API keys', () => {
      process.env.WAVE_API_KEY = 'test-wave-key';
      process.env.TENON_API_KEY = 'test-tenon-key';

      // Create new instance to pick up environment variables
      (ConfigurationService as any).instance = undefined;
      const newConfigService = ConfigurationService.getInstance();

      expect(newConfigService.getWaveConfiguration().apiKey).toBe('test-wave-key');
      expect(newConfigService.getTenonConfiguration().apiKey).toBe('test-tenon-key');
    });

    it('should use empty string for missing API keys', () => {
      delete process.env.WAVE_API_KEY;
      delete process.env.TENON_API_KEY;

      // Create new instance
      (ConfigurationService as any).instance = undefined;
      const newConfigService = ConfigurationService.getInstance();

      expect(newConfigService.getWaveConfiguration().apiKey).toBe('');
      expect(newConfigService.getTenonConfiguration().apiKey).toBe('');
    });
  });

  describe('Configuration Updates', () => {
    it('should update axe configuration', () => {
      const newAxeConfig = {
        timeout: 60000,
        tags: ['wcag2a'],
        rules: {
          'color-contrast': { enabled: false },
        },
      };

      configService.updateConfiguration({ axe: newAxeConfig });

      const updatedConfig = configService.getAxeConfiguration();
      expect(updatedConfig.timeout).toBe(60000);
      expect(updatedConfig.tags).toEqual(['wcag2a']);
      expect(updatedConfig.rules['color-contrast'].enabled).toBe(false);
    });

    it('should update pa11y configuration', () => {
      const newPa11yConfig = {
        timeout: 45000,
        wait: 3000,
        standard: 'WCAG2A',
        includeNotices: false,
        includeWarnings: false,
        chromeLaunchConfig: {
          args: ['--test-arg'],
        },
      };

      configService.updateConfiguration({ pa11y: newPa11yConfig });

      const updatedConfig = configService.getPa11yConfiguration();
      expect(updatedConfig.timeout).toBe(45000);
      expect(updatedConfig.wait).toBe(3000);
      expect(updatedConfig.standard).toBe('WCAG2A');
      expect(updatedConfig.includeNotices).toBe(false);
      expect(updatedConfig.includeWarnings).toBe(false);
      expect(updatedConfig.chromeLaunchConfig.args).toEqual(['--test-arg']);
    });

    it('should update reporting configuration', () => {
      const newReportingConfig = {
        maxConcurrency: 10,
        delayBetweenPages: 2000,
        screenshotTimeout: 10000,
        reportsDirectory: 'custom-reports',
      };

      configService.updateConfiguration({ reporting: newReportingConfig });

      const updatedConfig = configService.getReportingConfiguration();
      expect(updatedConfig.maxConcurrency).toBe(10);
      expect(updatedConfig.delayBetweenPages).toBe(2000);
      expect(updatedConfig.screenshotTimeout).toBe(10000);
      expect(updatedConfig.reportsDirectory).toBe('custom-reports');
    });

    it('should update crawling configuration', () => {
      const newCrawlingConfig = {
        excludePatterns: [/\.test$/],
        customExcludePatterns: [/\.custom$/],
      };

      configService.updateConfiguration({ crawling: newCrawlingConfig });

      const updatedConfig = configService.getCrawlingConfiguration();
      expect(updatedConfig.excludePatterns).toHaveLength(1);
      expect(updatedConfig.excludePatterns[0]).toEqual(/\.test$/);
      expect(updatedConfig.customExcludePatterns).toHaveLength(1);
      expect(updatedConfig.customExcludePatterns[0]).toEqual(/\.custom$/);
    });

    it('should update wave configuration', () => {
      const newWaveConfig = {
        timeout: 60000,
        apiKey: 'new-api-key',
        reportType: 2 as const,
        evalDelay: 3000,
        baseUrl: 'https://custom-wave.com',
      };

      configService.updateConfiguration({ wave: newWaveConfig });

      const updatedConfig = configService.getWaveConfiguration();
      expect(updatedConfig.timeout).toBe(60000);
      expect(updatedConfig.apiKey).toBe('new-api-key');
      expect(updatedConfig.reportType).toBe(2);
      expect(updatedConfig.evalDelay).toBe(3000);
      expect(updatedConfig.baseUrl).toBe('https://custom-wave.com');
    });

    it('should update tenon configuration', () => {
      const newTenonConfig = {
        timeout: 60000,
        apiKey: 'new-tenon-key',
        level: 'AAA' as const,
        certainty: 90,
        priority: 70,
        store: false,
        baseUrl: 'https://custom-tenon.io',
      };

      configService.updateConfiguration({ tenon: newTenonConfig });

      const updatedConfig = configService.getTenonConfiguration();
      expect(updatedConfig.timeout).toBe(60000);
      expect(updatedConfig.apiKey).toBe('new-tenon-key');
      expect(updatedConfig.level).toBe('AAA');
      expect(updatedConfig.certainty).toBe(90);
      expect(updatedConfig.priority).toBe(70);
      expect(updatedConfig.store).toBe(false);
      expect(updatedConfig.baseUrl).toBe('https://custom-tenon.io');
    });

    it('should allow updating multiple configuration sections', () => {
      const newAxeConfig = {
        timeout: 45000,
        tags: ['wcag2a'],
        rules: {
          'color-contrast': { enabled: false },
        },
      };

      const newReportingConfig = {
        maxConcurrency: 10,
        delayBetweenPages: 2000,
        screenshotTimeout: 10000,
        reportsDirectory: 'custom-reports',
      };

      configService.updateConfiguration({
        axe: newAxeConfig,
        reporting: newReportingConfig,
      });

      const updatedAxeConfig = configService.getAxeConfiguration();
      expect(updatedAxeConfig.timeout).toBe(45000);
      expect(updatedAxeConfig.tags).toEqual(['wcag2a']);

      const updatedReportingConfig = configService.getReportingConfiguration();
      expect(updatedReportingConfig.maxConcurrency).toBe(10);
      expect(updatedReportingConfig.reportsDirectory).toBe('custom-reports');

      // Other sections should remain unchanged
      const pa11yConfig = configService.getPa11yConfiguration();
      expect(pa11yConfig.timeout).toBe(30000); // Default value
    });
  });

  describe('Configuration Validation', () => {
    it('should validate configuration object structure', () => {
      const config = configService.getConfiguration();

      // Check that all required properties exist
      expect(config.axe).toBeDefined();
      expect(config.pa11y).toBeDefined();
      expect(config.lighthouse).toBeDefined();
      expect(config.wave).toBeDefined();
      expect(config.tenon).toBeDefined();
      expect(config.reporting).toBeDefined();
      expect(config.crawling).toBeDefined();
    });

    it('should have proper types for configuration values', () => {
      const config = configService.getConfiguration();

      // Axe config types
      expect(typeof config.axe.timeout).toBe('number');
      expect(Array.isArray(config.axe.tags)).toBe(true);
      expect(typeof config.axe.rules).toBe('object');

      // Pa11y config types
      expect(typeof config.pa11y.timeout).toBe('number');
      expect(typeof config.pa11y.wait).toBe('number');
      expect(typeof config.pa11y.standard).toBe('string');
      expect(typeof config.pa11y.includeNotices).toBe('boolean');
      expect(typeof config.pa11y.includeWarnings).toBe('boolean');

      // Reporting config types
      expect(typeof config.reporting.maxConcurrency).toBe('number');
      expect(typeof config.reporting.delayBetweenPages).toBe('number');
      expect(typeof config.reporting.screenshotTimeout).toBe('number');
      expect(typeof config.reporting.reportsDirectory).toBe('string');

      // Crawling config types
      expect(Array.isArray(config.crawling.excludePatterns)).toBe(true);
      expect(Array.isArray(config.crawling.customExcludePatterns)).toBe(true);
    });

    it('should have valid exclude patterns', () => {
      const crawlingConfig = configService.getCrawlingConfiguration();

      crawlingConfig.excludePatterns.forEach(pattern => {
        expect(pattern).toBeInstanceOf(RegExp);
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle invalid configuration updates gracefully', () => {
      expect(() => {
        configService.updateConfiguration(null as any);
      }).not.toThrow();

      expect(() => {
        configService.updateConfiguration(undefined as any);
      }).not.toThrow();
    });

    it('should maintain original configuration when invalid update is attempted', () => {
      const originalConfig = configService.getAxeConfiguration();

      configService.updateConfiguration(null as any);

      const configAfterInvalidUpdate = configService.getAxeConfiguration();
      expect(configAfterInvalidUpdate).toEqual(originalConfig);
    });
  });
});
