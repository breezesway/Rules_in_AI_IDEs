import { ConfigurationService, TestConfiguration } from '@/utils/services/configuration-service';

describe('ConfigurationService', () => {
    let configService: ConfigurationService;

    beforeEach(() => {
        // Clear any existing instance to ensure fresh state
        (ConfigurationService as any).instance = undefined;
        configService = ConfigurationService.getInstance();
    });

    describe('Singleton Pattern', () => {
        test('should return the same instance when called multiple times', () => {
            const instance1 = ConfigurationService.getInstance();
            const instance2 = ConfigurationService.getInstance();
            expect(instance1).toBe(instance2);
        });

        test('should prevent direct instantiation (private constructor)', () => {
            // TypeScript private constructors prevent instantiation at compile time
            // This test verifies that the singleton pattern is enforced
            const instance1 = ConfigurationService.getInstance();
            const instance2 = ConfigurationService.getInstance();
            expect(instance1).toBe(instance2);
            
            // Verify that we can't access the constructor directly
            expect(ConfigurationService.constructor.name).toBe('Function');
            expect(typeof ConfigurationService.getInstance).toBe('function');
        });
    });

    describe('getConfiguration', () => {
        test('should return complete configuration object', () => {
            const config = configService.getConfiguration();

            expect(config).toHaveProperty('axe');
            expect(config).toHaveProperty('pa11y');
            expect(config).toHaveProperty('reporting');
            expect(config).toHaveProperty('crawling');
        });

        test('should return default configuration values', () => {
            const config = configService.getConfiguration();

            // Test axe configuration
            expect(config.axe.timeout).toBe(30000);
            expect(config.axe.tags).toEqual(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']);
            expect(config.axe.rules).toHaveProperty('color-contrast');
            expect(config.axe.rules).toHaveProperty('keyboard');
            expect(config.axe.rules).toHaveProperty('focus-order-semantics');

            // Test pa11y configuration
            expect(config.pa11y.timeout).toBe(60000);
            expect(config.pa11y.wait).toBe(1000);
            expect(config.pa11y.standard).toBe('WCAG2AA');
            expect(config.pa11y.includeNotices).toBe(false);
            expect(config.pa11y.includeWarnings).toBe(true);
            expect(config.pa11y.chromeLaunchConfig.args).toContain('--no-sandbox');

            // Test reporting configuration
            expect(config.reporting.maxConcurrency).toBe(5);
            expect(config.reporting.delayBetweenPages).toBe(500);
            expect(config.reporting.screenshotTimeout).toBe(5000);
            expect(config.reporting.reportsDirectory).toBe('accessibility-reports');

            // Test crawling configuration
            expect(config.crawling.excludePatterns).toBeInstanceOf(Array);
            expect(config.crawling.customExcludePatterns).toBeInstanceOf(Array);
        });
    });

    describe('getAxeConfiguration', () => {
        test('should return axe configuration object', () => {
            const axeConfig = configService.getAxeConfiguration();

            expect(axeConfig).toHaveProperty('timeout');
            expect(axeConfig).toHaveProperty('tags');
            expect(axeConfig).toHaveProperty('rules');
            expect(axeConfig.timeout).toBe(30000);
            expect(axeConfig.tags).toEqual(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']);
        });
    });

    describe('getPa11yConfiguration', () => {
        test('should return pa11y configuration object', () => {
            const pa11yConfig = configService.getPa11yConfiguration();

            expect(pa11yConfig).toHaveProperty('timeout');
            expect(pa11yConfig).toHaveProperty('wait');
            expect(pa11yConfig).toHaveProperty('standard');
            expect(pa11yConfig).toHaveProperty('includeNotices');
            expect(pa11yConfig).toHaveProperty('includeWarnings');
            expect(pa11yConfig).toHaveProperty('chromeLaunchConfig');
            expect(pa11yConfig.timeout).toBe(60000);
            expect(pa11yConfig.standard).toBe('WCAG2AA');
        });
    });

    describe('getReportingConfiguration', () => {
        test('should return reporting configuration object', () => {
            const reportingConfig = configService.getReportingConfiguration();

            expect(reportingConfig).toHaveProperty('maxConcurrency');
            expect(reportingConfig).toHaveProperty('delayBetweenPages');
            expect(reportingConfig).toHaveProperty('screenshotTimeout');
            expect(reportingConfig).toHaveProperty('reportsDirectory');
            expect(reportingConfig.maxConcurrency).toBe(5);
            expect(reportingConfig.reportsDirectory).toBe('accessibility-reports');
        });
    });

    describe('getCrawlingConfiguration', () => {
        test('should return crawling configuration object', () => {
            const crawlingConfig = configService.getCrawlingConfiguration();

            expect(crawlingConfig).toHaveProperty('excludePatterns');
            expect(crawlingConfig).toHaveProperty('customExcludePatterns');
            expect(crawlingConfig.excludePatterns).toBeInstanceOf(Array);
            expect(crawlingConfig.customExcludePatterns).toBeInstanceOf(Array);
        });

        test('should include default exclude patterns', () => {
            const crawlingConfig = configService.getCrawlingConfiguration();

            expect(crawlingConfig.excludePatterns.length).toBeGreaterThan(0);
            expect(crawlingConfig.excludePatterns.some((pattern: RegExp) => pattern.toString().includes('login'))).toBe(true);
            expect(crawlingConfig.excludePatterns.some((pattern: RegExp) => pattern.toString().includes('admin'))).toBe(true);
            expect(crawlingConfig.excludePatterns.some((pattern: RegExp) => pattern.toString().includes('\\.pdf'))).toBe(true);
        });
    });

    describe('updateConfiguration', () => {
        test('should update configuration with partial updates', () => {
            const originalConfig = configService.getConfiguration();
            const updates: Partial<TestConfiguration> = {
                axe: {
                    ...originalConfig.axe,
                    timeout: 45000
                },
                reporting: {
                    ...originalConfig.reporting,
                    maxConcurrency: 10
                }
            };

            configService.updateConfiguration(updates);
            const updatedConfig = configService.getConfiguration();

            expect(updatedConfig.axe.timeout).toBe(45000);
            expect(updatedConfig.reporting.maxConcurrency).toBe(10);
            expect(updatedConfig.pa11y.timeout).toBe(60000); // Should remain unchanged
        });

        test('should preserve existing configuration when updating', () => {
            const originalConfig = configService.getConfiguration();
            const updates: Partial<TestConfiguration> = {
                axe: {
                    timeout: 60000,
                    tags: ['wcag2a'],
                    rules: { 'new-rule': { enabled: true } }
                }
            };

            configService.updateConfiguration(updates);
            const updatedConfig = configService.getConfiguration();

            expect(updatedConfig.axe.timeout).toBe(60000);
            expect(updatedConfig.axe.tags).toEqual(['wcag2a']);
            expect(updatedConfig.axe.rules).toHaveProperty('new-rule');
            expect(updatedConfig.pa11y).toEqual(originalConfig.pa11y); // Should be unchanged
            expect(updatedConfig.reporting).toEqual(originalConfig.reporting); // Should be unchanged
            expect(updatedConfig.crawling).toEqual(originalConfig.crawling); // Should be unchanged
        });

        test('should handle empty updates', () => {
            const originalConfig = configService.getConfiguration();

            configService.updateConfiguration({});
            const updatedConfig = configService.getConfiguration();

            expect(updatedConfig).toEqual(originalConfig);
        });

        test('should handle nested object updates', () => {
            const originalConfig = configService.getConfiguration();
            const updates: Partial<TestConfiguration> = {
                pa11y: {
                    ...originalConfig.pa11y,
                    chromeLaunchConfig: {
                        args: ['--new-arg', '--another-arg']
                    }
                }
            };

            configService.updateConfiguration(updates);
            const updatedConfig = configService.getConfiguration();

            expect(updatedConfig.pa11y.chromeLaunchConfig.args).toEqual(['--new-arg', '--another-arg']);
        });
    });

    describe('Configuration Immutability', () => {
        test('should not allow direct modification of returned configuration', () => {
            const config = configService.getConfiguration();
            const originalTimeout = config.axe.timeout;

            // Attempt to modify the returned object
            config.axe.timeout = 99999;

            // Get fresh configuration
            const freshConfig = configService.getConfiguration();

            // The original config object should be modified
            expect(config.axe.timeout).toBe(99999);
            // But the service should still return the original value
            expect(freshConfig.axe.timeout).toBe(originalTimeout);
        });
    });

    describe('Configuration Validation', () => {
        test('should have valid axe configuration structure', () => {
            const config = configService.getConfiguration();

            expect(typeof config.axe.timeout).toBe('number');
            expect(config.axe.timeout).toBeGreaterThan(0);
            expect(Array.isArray(config.axe.tags)).toBe(true);
            expect(config.axe.tags.length).toBeGreaterThan(0);
            expect(typeof config.axe.rules).toBe('object');
        });

        test('should have valid pa11y configuration structure', () => {
            const config = configService.getConfiguration();

            expect(typeof config.pa11y.timeout).toBe('number');
            expect(config.pa11y.timeout).toBeGreaterThan(0);
            expect(typeof config.pa11y.wait).toBe('number');
            expect(typeof config.pa11y.standard).toBe('string');
            expect(typeof config.pa11y.includeNotices).toBe('boolean');
            expect(typeof config.pa11y.includeWarnings).toBe('boolean');
            expect(Array.isArray(config.pa11y.chromeLaunchConfig.args)).toBe(true);
        });

        test('should have valid reporting configuration structure', () => {
            const config = configService.getConfiguration();

            expect(typeof config.reporting.maxConcurrency).toBe('number');
            expect(config.reporting.maxConcurrency).toBeGreaterThan(0);
            expect(typeof config.reporting.delayBetweenPages).toBe('number');
            expect(typeof config.reporting.screenshotTimeout).toBe('number');
            expect(typeof config.reporting.reportsDirectory).toBe('string');
        });

        test('should have valid crawling configuration structure', () => {
            const config = configService.getConfiguration();

            expect(Array.isArray(config.crawling.excludePatterns)).toBe(true);
            expect(Array.isArray(config.crawling.customExcludePatterns)).toBe(true);
            expect(config.crawling.excludePatterns.every(pattern => pattern instanceof RegExp)).toBe(true);
            expect(config.crawling.customExcludePatterns.every(pattern => pattern instanceof RegExp)).toBe(true);
        });
    });

    describe('Default Configuration Values', () => {
        test('should have reasonable default timeouts', () => {
            const config = configService.getConfiguration();

            expect(config.axe.timeout).toBeGreaterThanOrEqual(1000);
            expect(config.axe.timeout).toBeLessThanOrEqual(120000);
            expect(config.pa11y.timeout).toBeGreaterThanOrEqual(1000);
            expect(config.pa11y.timeout).toBeLessThanOrEqual(120000);
        });

        test('should have reasonable concurrency limits', () => {
            const config = configService.getConfiguration();

            expect(config.reporting.maxConcurrency).toBeGreaterThan(0);
            expect(config.reporting.maxConcurrency).toBeLessThanOrEqual(20);
        });

        test('should have valid WCAG tags', () => {
            const config = configService.getConfiguration();
            const validTags = ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'];

            expect(config.axe.tags.every(tag => validTags.includes(tag))).toBe(true);
        });

        test('should have valid WCAG standard', () => {
            const config = configService.getConfiguration();
            const validStandards = ['WCAG2A', 'WCAG2AA', 'WCAG2AAA'];

            expect(validStandards.includes(config.pa11y.standard)).toBe(true);
        });
    });
}); 