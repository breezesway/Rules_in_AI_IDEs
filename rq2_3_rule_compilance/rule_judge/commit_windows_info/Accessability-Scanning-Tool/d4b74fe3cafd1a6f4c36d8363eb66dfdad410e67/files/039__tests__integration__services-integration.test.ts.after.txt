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

    beforeEach(async () => {
        // Clear any existing instances to ensure fresh state
        (ErrorHandlerService as any).instance = undefined;
        (ConfigurationService as any).instance = undefined;
        (SecurityValidationService as any).instance = undefined;
        (FileOperationsService as any).instance = undefined;

        // Set up test database environment
        (global as any).testUtils.database.setupTestEnvironment();

        // Clean up any existing test data before each test
        await (global as any).testUtils.database.cleanupTestData();

        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();
        securityService = SecurityValidationService.getInstance();
        fileService = FileOperationsService.getInstance();
    });

    afterEach(async () => {
        // Clean up test data after each test
        await (global as any).testUtils.database.cleanupTestData();

        // Verify cleanup was successful
        await (global as any).testUtils.database.verifyCleanup();
    });

    describe('Service Singleton Pattern', () => {
        test('should return same instances for all services', () => {
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
        });

        test('should maintain singleton pattern across multiple calls', () => {
            const instances = [];

            for (let i = 0; i < 5; i++) {
                instances.push({
                    errorHandler: ErrorHandlerService.getInstance(),
                    configService: ConfigurationService.getInstance(),
                    securityService: SecurityValidationService.getInstance(),
                    fileService: FileOperationsService.getInstance()
                });
            }

            // All instances should be the same
            for (let i = 1; i < instances.length; i++) {
                expect(instances[i].errorHandler).toBe(instances[0].errorHandler);
                expect(instances[i].configService).toBe(instances[0].configService);
                expect(instances[i].securityService).toBe(instances[0].securityService);
                expect(instances[i].fileService).toBe(instances[0].fileService);
            }
        });
    });

    describe('Error Handler Service Integration', () => {
        test('should handle errors consistently across services', () => {
            const testError = new Error('Integration test error');

            const result1 = errorHandler.handleError(testError, 'Service 1 context');
            const result2 = errorHandler.handleError(testError, 'Service 2 context');

            expect(result1.success).toBe(false);
            expect(result2.success).toBe(false);
            expect(result1.message).toContain('Service 1 context');
            expect(result2.message).toContain('Service 2 context');
        });

        test('should provide consistent error result structure', () => {
            const testError = new Error('Test error message');
            const result = errorHandler.handleError(testError, 'Test context');

            expect(result).toHaveProperty('success');
            expect(result).toHaveProperty('message');
            expect(result).toHaveProperty('data');
            expect(result.success).toBe(false);
            expect(result.message).toContain('Test context');
            expect(result.data).toBeNull();
        });

        test('should handle different error types consistently', () => {
            const errorTypes = [
                new Error('Standard error'),
                new TypeError('Type error'),
                new ReferenceError('Reference error'),
                'String error',
                { custom: 'error object' }
            ];

            errorTypes.forEach(error => {
                const result = errorHandler.handleError(error, 'Error type test');
                expect(result.success).toBe(false);
                expect(result.message).toContain('Error type test');
                expect(result.data).toBeNull();
            });
        });
    });

    describe('Configuration Service Integration', () => {
        test('should persist configuration across service calls', () => {
            const testKey = 'integration.test.key';
            const testValue = 'integration-test-value';

            configService.set(testKey, testValue);
            const retrievedValue = configService.get(testKey);

            expect(retrievedValue).toBe(testValue);
        });

        test('should handle configuration with default values', () => {
            const nonExistentKey = 'non.existent.key';
            const defaultValue = 'default-value';

            const result = configService.get(nonExistentKey, defaultValue);
            expect(result).toBe(defaultValue);
        });

        test('should handle nested configuration objects', () => {
            const nestedConfig = {
                database: {
                    host: 'localhost',
                    port: 27017,
                    name: 'test_db'
                },
                api: {
                    timeout: 5000,
                    retries: 3
                }
            };

            configService.set('app.config', nestedConfig);
            const retrievedConfig = configService.get('app.config');

            expect(retrievedConfig).toEqual(nestedConfig);
            expect(retrievedConfig.database.host).toBe('localhost');
            expect(retrievedConfig.api.timeout).toBe(5000);
        });

        test('should handle configuration updates', () => {
            const testKey = 'update.test.key';
            const initialValue = 'initial-value';
            const updatedValue = 'updated-value';

            configService.set(testKey, initialValue);
            expect(configService.get(testKey)).toBe(initialValue);

            configService.set(testKey, updatedValue);
            expect(configService.get(testKey)).toBe(updatedValue);
        });
    });

    describe('Security Validation Service Integration', () => {
        test('should validate URLs consistently', () => {
            const validUrls = [
                'https://example.com',
                'http://localhost:3000',
                'https://subdomain.example.co.uk/path?param=value',
                'https://api.example.com/v1/endpoint'
            ];

            const invalidUrls = [
                'invalid-url',
                'ftp://example.com',
                'javascript:alert("xss")',
                'data:text/html,<script>alert("xss")</script>'
            ];

            validUrls.forEach(url => {
                const result = securityService.validateUrl(url);
                expect(result.success).toBe(true);
                expect(result.data).toBe(url);
            });

            invalidUrls.forEach(url => {
                const result = securityService.validateUrl(url);
                expect(result.success).toBe(false);
                expect(result.message).toContain('Invalid URL');
            });
        });

        test('should validate file paths securely', () => {
            const validPaths = [
                './test-file.txt',
                '../relative/path/file.json',
                '/absolute/path/file.pdf',
                'C:\\Windows\\System32\\legitimate\\file.txt'
            ];

            const invalidPaths = [
                '../../../etc/passwd',
                'C:\\Windows\\System32\\config\\SAM',
                '/etc/shadow',
                '..\\..\\..\\Windows\\System32\\config\\SAM'
            ];

            validPaths.forEach(filePath => {
                const result = securityService.validateFilePath(filePath);
                expect(result.success).toBe(true);
                expect(result.data).toBe(filePath);
            });

            invalidPaths.forEach(filePath => {
                const result = securityService.validateFilePath(filePath);
                expect(result.success).toBe(false);
                expect(result.message).toContain('Invalid file path');
            });
        });

        test('should sanitize user input', () => {
            const maliciousInputs = [
                '<script>alert("xss")</script>',
                'javascript:alert("xss")',
                'data:text/html,<script>alert("xss")</script>',
                'onload="alert(\'xss\')"',
                '<img src="x" onerror="alert(\'xss\')">'
            ];

            maliciousInputs.forEach(input => {
                const result = securityService.sanitizeInput(input);
                expect(result.success).toBe(true);
                expect(result.data).not.toContain('<script>');
                expect(result.data).not.toContain('javascript:');
                expect(result.data).not.toContain('onload=');
                expect(result.data).not.toContain('onerror=');
            });
        });
    });

    describe('File Operations Service Integration', () => {
        test('should create and read files consistently', async () => {
            const testContent = 'Integration test content';
            const testFilePath = './test-integration-file.txt';

            // Create file
            const createResult = await fileService.writeFile(testFilePath, testContent);
            expect(createResult.success).toBe(true);

            // Read file
            const readResult = await fileService.readFile(testFilePath);
            expect(readResult.success).toBe(true);
            expect(readResult.data).toBe(testContent);

            // Clean up
            await fileService.deleteFile(testFilePath);
        });

        test('should handle file operations with error handling', async () => {
            const nonExistentFile = './non-existent-file.txt';

            const readResult = await fileService.readFile(nonExistentFile);
            expect(readResult.success).toBe(false);
            expect(readResult.message).toContain('File not found');
        });

        test('should create directories and list contents', async () => {
            const testDir = './test-integration-dir';
            const testFile = `${testDir}/test.txt`;

            // Create directory
            const mkdirResult = await fileService.createDirectory(testDir);
            expect(mkdirResult.success).toBe(true);

            // Create file in directory
            await fileService.writeFile(testFile, 'test content');

            // List directory contents
            const listResult = await fileService.listDirectory(testDir);
            expect(listResult.success).toBe(true);
            expect(listResult.data).toContain('test.txt');

            // Clean up
            await fileService.deleteFile(testFile);
            await fileService.deleteDirectory(testDir);
        });

        test('should handle file operations with security validation', async () => {
            const safePath = './safe-test-file.txt';
            const dangerousPath = '../../../etc/passwd';

            // Validate safe path
            const safeValidation = securityService.validateFilePath(safePath);
            expect(safeValidation.success).toBe(true);

            // Validate dangerous path
            const dangerousValidation = securityService.validateFilePath(dangerousPath);
            expect(dangerousValidation.success).toBe(false);

            // Only proceed with safe path
            if (safeValidation.success) {
                const writeResult = await fileService.writeFile(safePath, 'safe content');
                expect(writeResult.success).toBe(true);

                // Clean up
                await fileService.deleteFile(safePath);
            }
        });
    });

    describe('Cross-Service Communication', () => {
        test('should handle errors across multiple services', async () => {
            const testError = new Error('Cross-service error');

            // Simulate error in file service
            const fileResult = await fileService.readFile('non-existent-file.txt');
            expect(fileResult.success).toBe(false);

            // Error should be handled by error handler service
            const errorResult = errorHandler.handleError(fileResult.error || new Error('File read failed'), 'File service error');
            expect(errorResult.success).toBe(false);
            expect(errorResult.message).toContain('File service error');
        });

        test('should use configuration across services', async () => {
            const testConfig = {
                maxFileSize: 1024,
                allowedExtensions: ['.txt', '.json'],
                timeout: 5000
            };

            // Set configuration
            configService.set('file.operations', testConfig);

            // Use configuration in file service
            const config = configService.get('file.operations', {});
            expect(config.maxFileSize).toBe(1024);
            expect(config.allowedExtensions).toContain('.txt');

            // Use configuration in security service
            const urlValidation = securityService.validateUrl('https://example.com');
            expect(urlValidation.success).toBe(true);
        });

        test('should validate security across services', async () => {
            const testUrl = 'https://example.com';
            const testFilePath = './test-file.txt';

            // Validate URL
            const urlValidation = securityService.validateUrl(testUrl);
            expect(urlValidation.success).toBe(true);

            // Validate file path
            const pathValidation = securityService.validateFilePath(testFilePath);
            expect(pathValidation.success).toBe(true);

            // Use validated data in file service
            if (urlValidation.success && pathValidation.success) {
                const fileResult = await fileService.writeFile(testFilePath, `URL: ${testUrl}`);
                expect(fileResult.success).toBe(true);

                // Clean up
                await fileService.deleteFile(testFilePath);
            }
        });
    });

    describe('Error Recovery and Resilience', () => {
        test('should recover from file system errors', async () => {
            const invalidPath = '/invalid/path/that/does/not/exist/file.txt';

            const result = await fileService.writeFile(invalidPath, 'test content');
            expect(result.success).toBe(false);

            // Should still be able to write to valid path
            const validPath = './recovery-test.txt';
            const recoveryResult = await fileService.writeFile(validPath, 'recovery content');
            expect(recoveryResult.success).toBe(true);

            // Clean up
            await fileService.deleteFile(validPath);
        });

        test('should handle configuration errors gracefully', () => {
            const invalidKey = null;
            const defaultValue = 'default';

            const result = configService.get(invalidKey as any, defaultValue);
            expect(result).toBe(defaultValue);
        });

        test('should maintain service state after errors', () => {
            const testKey = 'error.recovery.test';
            const testValue = 'recovery-value';

            // Set value
            configService.set(testKey, testValue);

            // Simulate error
            const errorResult = errorHandler.handleError(new Error('Test error'), 'Error recovery test');
            expect(errorResult.success).toBe(false);

            // Configuration should still be intact
            const retrievedValue = configService.get(testKey);
            expect(retrievedValue).toBe(testValue);
        });

        test('should handle security validation failures gracefully', () => {
            const maliciousUrl = 'javascript:alert("xss")';
            const maliciousPath = '../../../etc/passwd';

            const urlResult = securityService.validateUrl(maliciousUrl);
            expect(urlResult.success).toBe(false);

            const pathResult = securityService.validateFilePath(maliciousPath);
            expect(pathResult.success).toBe(false);

            // Services should still function with valid inputs
            const validUrl = 'https://example.com';
            const validPath = './safe-file.txt';

            const validUrlResult = securityService.validateUrl(validUrl);
            expect(validUrlResult.success).toBe(true);

            const validPathResult = securityService.validateFilePath(validPath);
            expect(validPathResult.success).toBe(true);
        });
    });

    describe('Performance and Resource Management', () => {
        test('should handle multiple concurrent operations', async () => {
            const operations = [];
            const fileCount = 5;

            for (let i = 0; i < fileCount; i++) {
                const filePath = `./concurrent-test-${i}.txt`;
                operations.push(
                    fileService.writeFile(filePath, `content ${i}`)
                );
            }

            const results = await Promise.all(operations);
            results.forEach(result => {
                expect(result.success).toBe(true);
            });

            // Clean up
            for (let i = 0; i < fileCount; i++) {
                await fileService.deleteFile(`./concurrent-test-${i}.txt`);
            }
        });

        test('should handle large configuration objects', () => {
            const largeConfig = {
                database: {
                    connections: Array(100).fill(null).map((_, i) => ({
                        id: i,
                        host: `host-${i}.example.com`,
                        port: 27017 + i,
                        name: `db-${i}`
                    }))
                },
                api: {
                    endpoints: Array(50).fill(null).map((_, i) => ({
                        path: `/api/v1/endpoint-${i}`,
                        method: 'GET',
                        timeout: 5000 + i
                    }))
                }
            };

            configService.set('large.config', largeConfig);
            const retrievedConfig = configService.get('large.config');

            expect(retrievedConfig).toEqual(largeConfig);
            expect(retrievedConfig.database.connections).toHaveLength(100);
            expect(retrievedConfig.api.endpoints).toHaveLength(50);
        });

        test('should handle rapid configuration changes', () => {
            const testKey = 'rapid.config.test';
            const iterations = 100;

            for (let i = 0; i < iterations; i++) {
                configService.set(testKey, `value-${i}`);
                const retrievedValue = configService.get(testKey);
                expect(retrievedValue).toBe(`value-${i}`);
            }
        });
    });
}); 