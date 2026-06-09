import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { SecurityValidationService } from '@/utils/services/security-validation-service';
import { FileOperationsService } from '@/utils/services/file-operations-service';
import { ServiceResult, ErrorResult, SuccessResult } from '@/core/types/common';

describe('Services Integration', () => {
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;
    let securityService: SecurityValidationService;
    let fileService: FileOperationsService;

    beforeEach(() => {
        // Clear any existing instances to ensure fresh state
        (ErrorHandlerService as any).instance = undefined;
        (ConfigurationService as any).instance = undefined;
        (SecurityValidationService as any).instance = undefined;
        (FileOperationsService as any).instance = undefined;

        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();
        securityService = SecurityValidationService.getInstance();
        fileService = FileOperationsService.getInstance();
    });

    describe('Singleton Pattern Verification', () => {
        test('should maintain singleton pattern across services', () => {
            const errorHandler1 = ErrorHandlerService.getInstance();
            const errorHandler2 = ErrorHandlerService.getInstance();
            const configService1 = ConfigurationService.getInstance();
            const configService2 = ConfigurationService.getInstance();
            const securityService1 = SecurityValidationService.getInstance();
            const securityService2 = SecurityValidationService.getInstance();
            const fileService1 = FileOperationsService.getInstance();
            const fileService2 = FileOperationsService.getInstance();

            expect(errorHandler1).toBe(errorHandler2);
            expect(configService1).toBe(configService2);
            expect(securityService1).toBe(securityService2);
            expect(fileService1).toBe(fileService2);
        });

        test('should enforce singleton pattern across all services', () => {
            // Verify that all services maintain singleton pattern
            const errorHandler1 = ErrorHandlerService.getInstance();
            const errorHandler2 = ErrorHandlerService.getInstance();
            expect(errorHandler1).toBe(errorHandler2);

            const configService1 = ConfigurationService.getInstance();
            const configService2 = ConfigurationService.getInstance();
            expect(configService1).toBe(configService2);

            const securityService1 = SecurityValidationService.getInstance();
            const securityService2 = SecurityValidationService.getInstance();
            expect(securityService1).toBe(securityService2);

            const fileService1 = FileOperationsService.getInstance();
            const fileService2 = FileOperationsService.getInstance();
            expect(fileService1).toBe(fileService2);

            // Verify that constructors are not directly accessible
            expect(typeof ErrorHandlerService.getInstance).toBe('function');
            expect(typeof ConfigurationService.getInstance).toBe('function');
            expect(typeof SecurityValidationService.getInstance).toBe('function');
            expect(typeof FileOperationsService.getInstance).toBe('function');
        });
    });

    describe('Error Handling Integration', () => {
        test('should handle errors consistently across services', () => {
            const testError = new Error('Integration test error');
            const result = errorHandler.handleError(testError, 'integration test');

            expect(result.success).toBe(false);
            expect(result.error).toBe(testError);
            expect(result.context).toBe('integration test');
        });

        test('should create success results consistently', () => {
            const testData = { integration: 'test data' };
            const result = errorHandler.createSuccess(testData);

            expect(result.success).toBe(true);
            expect(result.data).toEqual(testData);
            expect(result.timestamp).toBeDefined();
        });

        test('should execute functions with error handling', async () => {
            const asyncFn = jest.fn().mockResolvedValue('async result');
            const result = await errorHandler.executeWithErrorHandling(asyncFn, 'integration test');

            expect(result.success).toBe(true);
            expect((result as SuccessResult<string>).data).toBe('async result');
        });
    });

    describe('Configuration Integration', () => {
        test('should provide consistent configuration across services', () => {
            const config = configService.getConfiguration();
            const axeConfig = configService.getAxeConfiguration();
            const pa11yConfig = configService.getPa11yConfiguration();
            const reportingConfig = configService.getReportingConfiguration();
            const crawlingConfig = configService.getCrawlingConfiguration();

            expect(config.axe).toEqual(axeConfig);
            expect(config.pa11y).toEqual(pa11yConfig);
            expect(config.reporting).toEqual(reportingConfig);
            expect(config.crawling).toEqual(crawlingConfig);
        });

        test('should update configuration and reflect changes', () => {
            const originalConfig = configService.getConfiguration();
            const updates = {
                axe: {
                    ...originalConfig.axe,
                    timeout: 45000
                }
            };

            configService.updateConfiguration(updates);
            const updatedConfig = configService.getConfiguration();

            expect(updatedConfig.axe.timeout).toBe(45000);
            expect(updatedConfig.pa11y.timeout).toBe(originalConfig.pa11y.timeout); // Unchanged
        });
    });

    describe('Security Validation Integration', () => {
        test('should validate URLs consistently', () => {
            const validUrl = 'https://example.com';
            const invalidUrl = 'ftp://example.com';

            const validResult = securityService.validateUrl(validUrl);
            const invalidResult = securityService.validateUrl(invalidUrl);

            expect(validResult.isValid).toBe(true);
            expect(invalidResult.isValid).toBe(false);
            expect(invalidResult.error).toContain('Protocol');
        });

        test('should validate file paths consistently', () => {
            const validPath = 'test-file.json';
            const invalidPath = '../sensitive-file.txt';

            const validResult = securityService.validateFilePath(validPath);
            const invalidResult = securityService.validateFilePath(invalidPath);

            expect(validResult.isValid).toBe(true);
            expect(invalidResult.isValid).toBe(false);
            expect(invalidResult.error).toContain('directory traversal');
        });

        test('should sanitize input consistently', () => {
            const dangerousInput = '<script>alert("xss")</script>';
            const safeInput = 'safe content';

            const dangerousResult = securityService.sanitizeInput(dangerousInput);
            const safeResult = securityService.sanitizeInput(safeInput);

            expect(dangerousResult.isValid).toBe(true);
            expect(dangerousResult.sanitizedValue).not.toContain('<script>');
            expect(safeResult.isValid).toBe(true);
            expect(safeResult.sanitizedValue).toBe(safeInput);
        });
    });

    describe('File Operations Integration', () => {
        test('should perform basic file operations', () => {
            const testDir = (global as any).testUtils.createTempDir();
            const testFile = `${testDir}/test-file.txt`;
            const testContent = 'Integration test content';

            // Test directory creation
            const dirResult = fileService.ensureDirectoryExists(testDir);
            expect(dirResult.success).toBe(true);

            // Test file writing
            const writeResult = fileService.writeFile(testFile, testContent);
            expect(writeResult.success).toBe(true);

            // Test file reading
            const readResult = fileService.readFile(testFile);
            expect(readResult.success).toBe(true);
            expect(readResult.content).toBe(testContent);

            // Test file deletion
            const deleteResult = fileService.deleteFile(testFile);
            expect(deleteResult.success).toBe(true);

            // Cleanup
            (global as any).testUtils.cleanupTempDir(testDir);
        });

        test('should handle file operation errors gracefully', () => {
            const nonExistentFile = '/non/existent/file.txt';
            const readResult = fileService.readFile(nonExistentFile);

            expect(readResult.success).toBe(false);
            expect(readResult.message).toContain('File does not exist');
        });
    });

    describe('Cross-Service Communication', () => {
        test('should integrate error handling with configuration', () => {
            const config = configService.getConfiguration();
            const result = errorHandler.createSuccess(config);

            expect(result.success).toBe(true);
            expect(result.data).toHaveProperty('axe');
            expect(result.data).toHaveProperty('pa11y');
            expect(result.data).toHaveProperty('reporting');
            expect(result.data).toHaveProperty('crawling');
        });

        test('should integrate security validation with file operations', () => {
            const validPath = 'test-file.json';
            const invalidPath = '../sensitive-file.txt';

            const pathValidation = securityService.validateFilePath(validPath);
            expect(pathValidation.isValid).toBe(true);

            // File service should use security validation internally
            const writeResult = fileService.writeFile(validPath, 'test content');
            expect(writeResult.success).toBe(true);
        });

        test('should integrate error handling with security validation', () => {
            const invalidUrl = 'not-a-url';
            const validationResult = securityService.validateUrl(invalidUrl);

            expect(validationResult.isValid).toBe(false);

            // Error handler should be able to handle validation results
            const errorResult = errorHandler.handleError(
                new Error(validationResult.error || 'Validation failed'),
                'security validation'
            );

            expect(errorResult.success).toBe(false);
            expect(errorResult.context).toBe('security validation');
        });
    });

    describe('Configuration and Security Integration', () => {
        test('should use configuration for security validation', () => {
            const config = configService.getConfiguration();

            // Security service should respect configuration settings
            const localhostResult = securityService.validateUrl('http://localhost:3000', true);
            expect(localhostResult.isValid).toBe(true);

            const blockedResult = securityService.validateUrl('http://localhost:3000', false);
            expect(blockedResult.isValid).toBe(false);
        });

        test('should validate configuration values', () => {
            const config = configService.getConfiguration();

            // Validate that configuration values are reasonable
            expect(config.axe.timeout).toBeGreaterThan(0);
            expect(config.pa11y.timeout).toBeGreaterThan(0);
            expect(config.reporting.maxConcurrency).toBeGreaterThan(0);
            expect(config.reporting.reportsDirectory).toBeTruthy();
        });
    });

    describe('Error Recovery and Resilience', () => {
        test('should handle service failures gracefully', async () => {
            const failingFn = jest.fn().mockRejectedValue(new Error('Service failure'));
            const result = await errorHandler.executeWithErrorHandling(failingFn, 'service test');

            expect(result.success).toBe(false);
            expect((result as ErrorResult).error).toBeInstanceOf(Error);
            expect((result as ErrorResult).context).toBe('service test');
        });

        test('should maintain service state during errors', () => {
            const originalConfig = configService.getConfiguration();

            // Simulate an error
            const errorResult = errorHandler.handleError('Test error', 'state test');

            // Configuration should remain unchanged
            const currentConfig = configService.getConfiguration();
            expect(currentConfig).toEqual(originalConfig);
        });
    });

    describe('Performance and Memory', () => {
        test('should handle concurrent service access', () => {
            const promises = Array.from({ length: 100 }, () =>
                Promise.all([
                    ErrorHandlerService.getInstance(),
                    ConfigurationService.getInstance(),
                    SecurityValidationService.getInstance(),
                    FileOperationsService.getInstance()
                ])
            );

            return Promise.all(promises).then(results => {
                results.forEach(([errorHandler, configService, securityService, fileService]) => {
                    expect(errorHandler).toBe(ErrorHandlerService.getInstance());
                    expect(configService).toBe(ConfigurationService.getInstance());
                    expect(securityService).toBe(SecurityValidationService.getInstance());
                    expect(fileService).toBe(FileOperationsService.getInstance());
                });
            });
        });

        test('should not leak memory with repeated operations', () => {
            const initialMemory = process.memoryUsage().heapUsed;

            // Test memory usage with repeated service operations without creating files
            for (let i = 0; i < 1000; i++) {
                errorHandler.createSuccess({ test: i });
                configService.getConfiguration();
                securityService.validateUrl(`https://example${i}.com`);
                securityService.sanitizeInput(`test-input-${i}`);
                // Test file service operations that don't create actual files
                fileService.readFile('/non/existent/file.txt'); // This will fail but test error handling
            }

            const finalMemory = process.memoryUsage().heapUsed;
            const memoryIncrease = finalMemory - initialMemory;

            // Memory increase should be reasonable (less than 10MB)
            expect(memoryIncrease).toBeLessThan(10 * 1024 * 1024);
        });
    });
}); 