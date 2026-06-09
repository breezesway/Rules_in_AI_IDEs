import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { FileOperationsService } from '@/utils/services/file-operations-service';
import { SecurityValidationService } from '@/utils/services/security-validation-service';
import fs from 'fs';
import path from 'path';

describe('Service Integration Tests', () => {
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;
    let fileService: FileOperationsService;
    let securityService: SecurityValidationService;
    let testDir: string;
    let testFile: string;

    beforeAll(() => {
        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();
        fileService = FileOperationsService.getInstance();
        securityService = SecurityValidationService.getInstance();

        testDir = (global as any).testUtils.createTempDir();
        testFile = path.join(testDir, 'test-integration.txt');
    });

    beforeEach(async () => {
        // Set up test database environment
        (global as any).testUtils.database.setupTestEnvironment();

        // Clean up any existing test data before each test
        await (global as any).testUtils.database.cleanupTestData();

        // Clean up test directory
        if (fs.existsSync(testDir)) {
            fs.rmSync(testDir, { recursive: true, force: true });
        }
        fs.mkdirSync(testDir, { recursive: true });
    });

    afterEach(async () => {
        // Clean up test data after each test
        await (global as any).testUtils.database.cleanupTestData();

        // Verify cleanup was successful
        await (global as any).testUtils.database.verifyCleanup();
    });

    afterAll(() => {
        // Clean up test directory
        if (fs.existsSync(testDir)) {
            fs.rmSync(testDir, { recursive: true, force: true });
        }
    });

    describe('Service Singleton Pattern', () => {
        test('should return same instances for all services', () => {
            const errorHandler1 = ErrorHandlerService.getInstance();
            const errorHandler2 = ErrorHandlerService.getInstance();
            expect(errorHandler1).toBe(errorHandler2);

            const configService1 = ConfigurationService.getInstance();
            const configService2 = ConfigurationService.getInstance();
            expect(configService1).toBe(configService2);

            const fileService1 = FileOperationsService.getInstance();
            const fileService2 = FileOperationsService.getInstance();
            expect(fileService1).toBe(fileService2);

            const securityService1 = SecurityValidationService.getInstance();
            const securityService2 = SecurityValidationService.getInstance();
            expect(securityService1).toBe(securityService2);
        });
    });

    describe('Error Handler Service Integration', () => {
        test('should handle errors consistently across services', () => {
            const testError = new Error('Test error message');

            const result1 = errorHandler.handleError(testError, 'Service 1 context');
            const result2 = errorHandler.handleError(testError, 'Service 2 context');

            expect(result1.success).toBe(false);
            expect(result2.success).toBe(false);
            expect(result1.message).toContain('Service 1 context');
            expect(result2.message).toContain('Service 2 context');
        });

        test('should log errors with proper context', () => {
            const testError = new Error('Integration test error');
            const result = errorHandler.handleError(testError, 'Integration test context');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Integration test context');
            expect(result.data).toBeNull();
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

        test('should handle nested configuration', () => {
            const nestedKey = 'integration.nested.test';
            const nestedValue = { key: 'value', number: 42 };

            configService.set(nestedKey, nestedValue);
            const retrievedValue = configService.get(nestedKey);

            expect(retrievedValue).toEqual(nestedValue);
        });
    });

    describe('File Operations Service Integration', () => {
        test('should create and read files consistently', async () => {
            const testContent = 'Integration test content';
            const testFilePath = path.join(testDir, 'integration-test.txt');

            // Create file
            const createResult = await fileService.writeFile(testFilePath, testContent);
            expect(createResult.success).toBe(true);

            // Read file
            const readResult = await fileService.readFile(testFilePath);
            expect(readResult.success).toBe(true);
            expect(readResult.data).toBe(testContent);
        });

        test('should handle file operations with error handling', async () => {
            const nonExistentFile = path.join(testDir, 'non-existent.txt');

            const readResult = await fileService.readFile(nonExistentFile);
            expect(readResult.success).toBe(false);
            expect(readResult.message).toContain('File not found');
        });

        test('should create directories and list contents', async () => {
            const subDir = path.join(testDir, 'subdirectory');
            const testFile = path.join(subDir, 'test.txt');

            // Create directory
            const mkdirResult = await fileService.createDirectory(subDir);
            expect(mkdirResult.success).toBe(true);

            // Create file in subdirectory
            await fileService.writeFile(testFile, 'test content');

            // List directory contents
            const listResult = await fileService.listDirectory(subDir);
            expect(listResult.success).toBe(true);
            expect(listResult.data).toContain('test.txt');
        });
    });

    describe('Security Validation Service Integration', () => {
        test('should validate URLs consistently', () => {
            const validUrls = [
                'https://example.com',
                'http://localhost:3000',
                'https://subdomain.example.co.uk/path?param=value'
            ];

            const invalidUrls = [
                'invalid-url',
                'ftp://example.com',
                'javascript:alert("xss")'
            ];

            validUrls.forEach(url => {
                const result = securityService.validateUrl(url);
                expect(result.success).toBe(true);
            });

            invalidUrls.forEach(url => {
                const result = securityService.validateUrl(url);
                expect(result.success).toBe(false);
            });
        });

        test('should validate file paths securely', () => {
            const validPaths = [
                './test-file.txt',
                '../relative/path/file.json',
                '/absolute/path/file.pdf'
            ];

            const invalidPaths = [
                '../../../etc/passwd',
                'C:\\Windows\\System32\\config\\SAM',
                '/etc/shadow'
            ];

            validPaths.forEach(filePath => {
                const result = securityService.validateFilePath(filePath);
                expect(result.success).toBe(true);
            });

            invalidPaths.forEach(filePath => {
                const result = securityService.validateFilePath(filePath);
                expect(result.success).toBe(false);
            });
        });

        test('should sanitize user input', () => {
            const maliciousInputs = [
                '<script>alert("xss")</script>',
                'javascript:alert("xss")',
                'data:text/html,<script>alert("xss")</script>',
                'onload="alert(\'xss\')"'
            ];

            maliciousInputs.forEach(input => {
                const result = securityService.sanitizeInput(input);
                expect(result.success).toBe(true);
                expect(result.data).not.toContain('<script>');
                expect(result.data).not.toContain('javascript:');
                expect(result.data).not.toContain('onload=');
            });
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
            }
        });
    });

    describe('Error Recovery and Resilience', () => {
        test('should recover from file system errors', async () => {
            const invalidPath = '/invalid/path/that/does/not/exist/file.txt';

            const result = await fileService.writeFile(invalidPath, 'test content');
            expect(result.success).toBe(false);

            // Should still be able to write to valid path
            const validPath = path.join(testDir, 'recovery-test.txt');
            const recoveryResult = await fileService.writeFile(validPath, 'recovery content');
            expect(recoveryResult.success).toBe(true);
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
    });
}); 