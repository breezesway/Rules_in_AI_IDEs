export interface TestConfiguration {
    axe: {
        timeout: number;
        tags: string[];
        rules: Record<string, { enabled: boolean }>;
    };
    pa11y: {
        timeout: number;
        wait: number;
        standard: string;
        includeNotices: boolean;
        includeWarnings: boolean;
        chromeLaunchConfig: {
            args: string[];
        };
    };
    lighthouse: {
        timeout: number;
        port: number;
        chromeLaunchConfig: {
            args: string[];
        };
    };
    reporting: {
        maxConcurrency: number;
        delayBetweenPages: number;
        screenshotTimeout: number;
        reportsDirectory: string;
    };
}

export class ConfigurationService {
    private static instance: ConfigurationService;
    private config: TestConfiguration;

    private constructor() {
        this.config = this.getDefaultConfiguration();
    }

    static getInstance(): ConfigurationService {
        if (!ConfigurationService.instance) {
            ConfigurationService.instance = new ConfigurationService();
        }
        return ConfigurationService.instance;
    }

    getConfiguration(): TestConfiguration {
        return this.config;
    }

    getAxeConfiguration() {
        return this.config.axe;
    }

    getPa11yConfiguration() {
        return this.config.pa11y;
    }

    getLighthouseConfiguration() {
        return this.config.lighthouse;
    }

    getReportingConfiguration() {
        return this.config.reporting;
    }

    updateConfiguration(updates: Partial<TestConfiguration>): void {
        this.config = { ...this.config, ...updates };
    }

    private getDefaultConfiguration(): TestConfiguration {
        return {
            axe: {
                timeout: 30000,
                tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'],
                rules: {
                    'color-contrast': { enabled: true },
                    'keyboard': { enabled: true },
                    'focus-order-semantics': { enabled: true },
                },
            },
            pa11y: {
                timeout: 30000,
                wait: 2000,
                standard: 'WCAG2AA',
                includeNotices: true,
                includeWarnings: true,
                chromeLaunchConfig: {
                    args: [
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-extensions',
                        '--disable-default-apps',
                        '--disable-sync',
                        '--memory-pressure-off',
                        '--max_old_space_size=2048',
                        '--single-process',
                    ],
                },
            },
            lighthouse: {
                timeout: 60000,
                port: 9222,
                chromeLaunchConfig: {
                    args: [
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-extensions',
                        '--disable-default-apps',
                        '--disable-sync',
                        '--memory-pressure-off',
                        '--max_old_space_size=2048',
                    ],
                },
            },
            reporting: {
                maxConcurrency: 5,
                delayBetweenPages: 1000,
                screenshotTimeout: 5000,
                reportsDirectory: 'playwright/accessibility-reports',
            },
        };
    }
} 