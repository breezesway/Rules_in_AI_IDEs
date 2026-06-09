import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import {
  AxeTestOptions,
  AxeTestRunner,
} from '../../playwright/tests/utils/runners/axe-test-runner';
import { AxeResults } from 'axe-core';

// Mock dependencies
jest.mock('@axe-core/playwright');
jest.mock('axe-core');

describe('AxeTestRunner', () => {
  let axeRunner: AxeTestRunner;
  let mockPage: any;
  let mockAxeBuilder: any;
  let mockConfigService: any;
  let mockErrorHandler: any;

  beforeEach(() => {
    // Mock Page object
    mockPage = {
      url: jest.fn().mockReturnValue('https://example.com'),
      addScriptTag: jest.fn(),
      goto: jest.fn(),
      waitForLoadState: jest.fn(),
      evaluate: jest.fn(),
      locator: jest.fn(),
      content: jest.fn(),
      title: jest.fn(),
      screenshot: jest.fn(),
      browserName: 'chromium',
      viewportInfo: '1200x800',
    };

    // Mock AxeBuilder
    mockAxeBuilder = {
      withTags: jest.fn().mockReturnThis(),
      withRules: jest.fn().mockReturnThis(),
      disableRules: jest.fn().mockReturnThis(),
      include: jest.fn().mockReturnThis(),
      exclude: jest.fn().mockReturnThis(),
      analyze: jest.fn().mockResolvedValue({
        violations: [],
        passes: [],
        incomplete: [],
        inapplicable: [],
        timestamp: new Date().toISOString(),
        url: 'https://example.com',
      }),
    };

    // Mock ConfigurationService
    mockConfigService = {
      getAxeConfiguration: jest.fn().mockReturnValue({
        timeout: 30000,
        tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'],
        rules: {
          'color-contrast': { enabled: true },
          keyboard: { enabled: true },
          'focus-order-semantics': { enabled: true },
        },
      }),
    };

    // Mock ErrorHandlerService
    mockErrorHandler = {
      executeWithErrorHandling: jest.fn().mockImplementation(async fn => {
        try {
          const result = await fn();
          return { success: true, data: result };
        } catch (error) {
          return { success: false, error: error.message };
        }
      }),
      withTimeout: jest.fn().mockImplementation(async (promise, _timeout, _context) => {
        try {
          const result = await promise;
          return { success: true, data: result };
        } catch (error) {
          return { success: false, error: error.message };
        }
      }),
      logInfo: jest.fn(),
      logSuccess: jest.fn(),
      logWarning: jest.fn(),
      createSuccess: jest.fn().mockImplementation(data => ({ success: true, data })),
    };

    // Mock the imports
    const { AxeBuilder } = require('@axe-core/playwright');
    AxeBuilder.mockImplementation(() => mockAxeBuilder);

    // Create test instance
    axeRunner = new AxeTestRunner(mockPage);
    (axeRunner as any).config = mockConfigService;
    (axeRunner as any).errorHandler = mockErrorHandler;

    // Ensure config is properly set
    mockConfigService.getAxeConfiguration.mockReturnValue({
      timeout: 30000,
      tags: ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa'],
      rules: {
        'color-contrast': { enabled: true },
        keyboard: { enabled: true },
        'focus-order-semantics': { enabled: true },
      },
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Basic Analysis', () => {
    it('should run basic axe analysis', async () => {
      const mockResults: AxeResults = {
        violations: [
          {
            id: 'color-contrast',
            impact: 'serious',
            description: 'Color contrast violation',
            help: 'Ensure sufficient color contrast',
            helpUrl: 'https://example.com/help',
            tags: ['wcag2aa'],
            nodes: [],
          },
        ],
        passes: [],
        incomplete: [],
        inapplicable: [],
        timestamp: new Date().toISOString(),
        url: 'https://example.com',
      };

      mockAxeBuilder.analyze.mockResolvedValue(mockResults);

      const result = await axeRunner.runAnalysis();

      expect(mockErrorHandler.withTimeout).toHaveBeenCalled();
      expect(mockAxeBuilder.analyze).toHaveBeenCalled();
      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResults);
    });

    it('should handle axe analysis errors', async () => {
      const error = new Error('Axe analysis failed');
      mockAxeBuilder.analyze.mockRejectedValue(error);

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Axe analysis failed');
    });

    it('should use default configuration when no options provided', async () => {
      await axeRunner.runAnalysis();

      expect(mockConfigService.getAxeConfiguration).toHaveBeenCalled();
      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith([
        'wcag2a',
        'wcag2aa',
        'wcag21aa',
        'wcag22aa',
      ]);
    });
  });

  describe('Custom Options', () => {
    it('should apply custom tags', async () => {
      const options: AxeTestOptions = {
        tags: ['wcag2a', 'best-practice'],
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['wcag2a', 'best-practice']);
    });

    it('should apply custom rules', async () => {
      const options: AxeTestOptions = {
        rules: {
          'color-contrast': { enabled: true },
          keyboard: { enabled: false },
        },
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(['color-contrast']);
      expect(mockAxeBuilder.disableRules).toHaveBeenCalledWith(['keyboard']);
    });

    it('should apply include selectors', async () => {
      const options: AxeTestOptions = {
        include: ['main', '#content'],
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.include).toHaveBeenCalledWith(['main', '#content']);
    });

    it('should apply exclude selectors', async () => {
      const options: AxeTestOptions = {
        exclude: ['footer', '.ads'],
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.exclude).toHaveBeenCalledWith(['footer', '.ads']);
    });

    it('should handle multiple custom options', async () => {
      const options: AxeTestOptions = {
        tags: ['wcag2aa'],
        rules: { 'color-contrast': { enabled: true } },
        include: ['main'],
        exclude: ['footer'],
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['wcag2aa']);
      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(['color-contrast']);
      expect(mockAxeBuilder.include).toHaveBeenCalledWith(['main']);
      expect(mockAxeBuilder.exclude).toHaveBeenCalledWith(['footer']);
    });
  });

  describe('DevTools Analysis', () => {
    it('should run DevTools-enhanced analysis', async () => {
      const result = await axeRunner.runDevToolsAnalysis();

      expect(mockPage.addScriptTag).toHaveBeenCalledWith({
        content: expect.stringContaining('axeDevToolsMode = true'),
      });
      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['wcag2a', 'wcag2aa', 'wcag21aa']);
      expect(result.success).toBe(true);
    });

    it('should enable shadow DOM analysis in DevTools mode', async () => {
      await axeRunner.runDevToolsAnalysis();

      expect(mockPage.addScriptTag).toHaveBeenCalledWith({
        content: expect.stringContaining('shadowdom: true'),
      });
    });

    it('should configure enhanced rules in DevTools mode', async () => {
      await axeRunner.runDevToolsAnalysis();

      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(
        expect.arrayContaining([
          'color-contrast',
          'color-contrast-enhanced',
          'focus-order-semantics',
          'landmark-contentinfo-is-top-level',
          'aria-allowed-attr',
          'aria-required-attr',
        ])
      );
    });
  });

  describe('Comprehensive Analysis', () => {
    it('should run comprehensive analysis with all rules', async () => {
      const result = await axeRunner.runComprehensiveAnalysis();

      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith([
        'wcag2a',
        'wcag2aa',
        'wcag21aa',
        'wcag22aa',
      ]);
      expect(result.success).toBe(true);
    });

    it('should run comprehensive DevTools analysis', async () => {
      const result = await axeRunner.runComprehensiveDevToolsAnalysis();

      expect(mockPage.addScriptTag).toHaveBeenCalledWith({
        content: expect.stringContaining('axeDevToolsMode = true'),
      });
      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith([
        'wcag2a',
        'wcag2aa',
        'wcag21aa',
        'wcag21aaa',
        'best-practice',
        'experimental',
      ]);
      expect(result.success).toBe(true);
    });
  });

  describe('Experimental Analysis', () => {
    it('should run experimental rules analysis', async () => {
      const result = await axeRunner.runExperimentalAnalysis();

      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['experimental']);
      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(
        expect.arrayContaining([
          'autocomplete-valid',
          'avoid-inline-spacing',
          'css-orientation-lock',
          'focus-order-semantics',
          'hidden-content',
          'label-content-name-mismatch',
        ])
      );
      expect(result.success).toBe(true);
    });
  });

  describe('Error Handling', () => {
    it('should handle page script injection errors', async () => {
      mockPage.addScriptTag.mockRejectedValue(new Error('Script injection failed'));

      const result = await axeRunner.runDevToolsAnalysis();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Script injection failed');
    });

    it('should handle axe builder configuration errors', async () => {
      mockAxeBuilder.withTags.mockImplementation(() => {
        throw new Error('Invalid tags');
      });

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid tags');
    });

    it('should handle analysis timeout', async () => {
      mockAxeBuilder.analyze.mockImplementation(() => {
        return new Promise((_, reject) => {
          setTimeout(() => reject(new Error('Analysis timeout')), 100);
        });
      });

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(false);
      expect(result.error).toBe('Analysis timeout');
    });
  });

  describe('Configuration Integration', () => {
    it('should use configuration service for default settings', async () => {
      await axeRunner.runAnalysis();

      expect(mockConfigService.getAxeConfiguration).toHaveBeenCalled();
    });

    it('should override configuration with custom options', async () => {
      const customOptions: AxeTestOptions = {
        tags: ['custom-tag'],
        rules: { 'custom-rule': { enabled: true } },
      };

      await axeRunner.runAnalysis(customOptions);

      expect(mockAxeBuilder.withTags).toHaveBeenCalledWith(['custom-tag']);
      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(['custom-rule']);
    });

    it('should handle missing configuration gracefully', async () => {
      mockConfigService.getAxeConfiguration.mockReturnValue(null);

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
    });
  });

  describe('Page Context', () => {
    it('should work with different page URLs', async () => {
      mockPage.url.mockReturnValue('https://different-site.com');

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
      expect(mockPage.url).toHaveBeenCalled();
    });

    it('should handle page navigation states', async () => {
      mockPage.url.mockReturnValue('about:blank');

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
    });
  });

  describe('Results Processing', () => {
    it('should return complete axe results', async () => {
      const mockResults: AxeResults = {
        violations: [
          {
            id: 'color-contrast',
            impact: 'serious',
            description: 'Color contrast violation',
            help: 'Ensure sufficient color contrast',
            helpUrl: 'https://example.com/help',
            tags: ['wcag2aa'],
            nodes: [
              {
                target: ['button'],
                html: '<button>Click me</button>',
                impact: 'serious',
                any: [],
                all: [],
                none: [],
              },
            ],
          },
        ],
        passes: [
          {
            id: 'document-title',
            impact: null,
            description: 'Document has title',
            help: 'Document has title',
            helpUrl: 'https://example.com/help',
            tags: ['wcag2a'],
            nodes: [],
          },
        ],
        incomplete: [],
        inapplicable: [],
        timestamp: new Date().toISOString(),
        url: 'https://example.com',
      };

      mockAxeBuilder.analyze.mockResolvedValue(mockResults);

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
      expect(result.data).toEqual(mockResults);
      expect(result.data.violations).toHaveLength(1);
      expect(result.data.passes).toHaveLength(1);
      expect(result.data.violations[0].id).toBe('color-contrast');
    });

    it('should handle empty results', async () => {
      const mockResults: AxeResults = {
        violations: [],
        passes: [],
        incomplete: [],
        inapplicable: [],
        timestamp: new Date().toISOString(),
        url: 'https://example.com',
      };

      mockAxeBuilder.analyze.mockResolvedValue(mockResults);

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
      expect(result.data.violations).toHaveLength(0);
      expect(result.data.passes).toHaveLength(0);
    });

    it('should preserve result metadata', async () => {
      const timestamp = new Date().toISOString();
      const mockResults: AxeResults = {
        violations: [],
        passes: [],
        incomplete: [],
        inapplicable: [],
        timestamp,
        url: 'https://example.com',
      };

      mockAxeBuilder.analyze.mockResolvedValue(mockResults);

      const result = await axeRunner.runAnalysis();

      expect(result.success).toBe(true);
      expect(result.data.timestamp).toBe(timestamp);
      expect(result.data.url).toBe('https://example.com');
    });
  });

  describe('Performance', () => {
    it('should handle multiple concurrent analyses', async () => {
      const promises = Array.from({ length: 5 }, () => axeRunner.runAnalysis());

      const results = await Promise.all(promises);

      results.forEach(result => {
        expect(result.success).toBe(true);
      });
      expect(mockAxeBuilder.analyze).toHaveBeenCalledTimes(5);
    });

    it('should complete analysis within reasonable time', async () => {
      const startTime = Date.now();

      await axeRunner.runAnalysis();

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(5000); // Should complete within 5 seconds
    });
  });

  describe('Edge Cases', () => {
    it('should handle null page object', async () => {
      const nullPageRunner = new AxeTestRunner(null as any);
      (nullPageRunner as any).config = mockConfigService;
      (nullPageRunner as any).errorHandler = mockErrorHandler;

      const result = await nullPageRunner.runAnalysis();

      expect(result.success).toBe(false);
    });

    it('should handle invalid rule configurations', async () => {
      const options: AxeTestOptions = {
        rules: {
          'invalid-rule': { enabled: true },
        },
      };

      // Mock axe builder to throw error for invalid rule
      mockAxeBuilder.withRules.mockImplementation(() => {
        throw new Error('Invalid rule: invalid-rule');
      });

      const result = await axeRunner.runAnalysis(options);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Invalid rule: invalid-rule');
    });

    it('should handle empty options object', async () => {
      const result = await axeRunner.runAnalysis({});

      expect(result.success).toBe(true);
      expect(mockConfigService.getAxeConfiguration).toHaveBeenCalled();
    });

    it('should handle partial rule configurations', async () => {
      const options: AxeTestOptions = {
        rules: {
          'color-contrast': { enabled: true },
          keyboard: { enabled: false },
        },
      };

      await axeRunner.runAnalysis(options);

      expect(mockAxeBuilder.withRules).toHaveBeenCalledWith(['color-contrast']);
      expect(mockAxeBuilder.disableRules).toHaveBeenCalledWith(['keyboard']);
    });
  });
});
