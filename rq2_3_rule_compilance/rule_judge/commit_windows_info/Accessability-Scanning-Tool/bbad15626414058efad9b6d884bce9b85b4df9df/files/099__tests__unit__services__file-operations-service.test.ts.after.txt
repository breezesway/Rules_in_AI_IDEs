import { FileOperationsService, FileOperationResult } from '@/utils/services/file-operations-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import { SecurityValidationService } from '@/utils/services/security-validation-service';
import * as fs from 'fs';
import * as path from 'path';

// Mock fs module
jest.mock('fs');
jest.mock('path');

// Mock the services
jest.mock('@/utils/services/configuration-service');
jest.mock('@/utils/services/security-validation-service');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

describe('FileOperationsService', () => {
    let fileService: FileOperationsService;
    let mockConfigService: jest.Mocked<ConfigurationService>;
    let mockSecurityService: jest.Mocked<SecurityValidationService>;

    beforeEach(() => {
        // Reset all mocks
        jest.clearAllMocks();

        // Mock ConfigurationService
        mockConfigService = {
            get: jest.fn(),
            getConfiguration: jest.fn(),
            getAxeConfiguration: jest.fn(),
            getPa11yConfiguration: jest.fn(),
            getReportingConfiguration: jest.fn(),
            getCrawlingConfiguration: jest.fn(),
            updateConfiguration: jest.fn(),
        } as any;

        // Mock SecurityValidationService
        mockSecurityService = {
            validateUrl: jest.fn(),
            validateFilePath: jest.fn(),
            sanitizeInput: jest.fn(),
            validateUserInput: jest.fn(),
        } as any;

        // Mock the static getInstance methods
        (ConfigurationService.getInstance as jest.Mock).mockReturnValue(mockConfigService);
        (SecurityValidationService.getInstance as jest.Mock).mockReturnValue(mockSecurityService);

        // Mock path.resolve to return the input
        mockPath.resolve.mockImplementation((input) => input);

        // Reset the singleton instance to ensure fresh mocks
        (FileOperationsService as any).instance = undefined;
        
        // Get the service instance
        fileService = FileOperationsService.getInstance();
    });

    describe('Singleton Pattern', () => {
        test('should return the same instance when called multiple times', () => {
            const instance1 = FileOperationsService.getInstance();
            const instance2 = FileOperationsService.getInstance();
            expect(instance1).toBe(instance2);
        });

        test('should throw error when trying to instantiate directly', () => {
            expect(() => {
                new (FileOperationsService as any)();
            }).toThrow('Cannot instantiate FileOperationsService directly. Use getInstance() instead.');
        });
    });

    describe('ensureDirectoryExists', () => {
        test('should create directory when it does not exist', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/directory',
                
            });

            // Mock fs.existsSync to return false (directory doesn't exist)
            mockFs.existsSync.mockReturnValue(false);

            const result = fileService.ensureDirectoryExists('/test/directory');

            expect(result.success).toBe(true);
            expect(result.message).toContain('Directory created successfully');
            expect(result.filePath).toBe('/test/directory');
            expect(mockFs.mkdirSync).toHaveBeenCalledWith('/test/directory', { recursive: true });
        });

        test('should return success when directory already exists', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/directory',
                
            });

            // Mock fs.existsSync to return true (directory exists)
            mockFs.existsSync.mockReturnValue(true);

            const result = fileService.ensureDirectoryExists('/test/directory');

            expect(result.success).toBe(true);
            expect(result.message).toContain('Directory already exists');
            expect(result.filePath).toBe('/test/directory');
            expect(mockFs.mkdirSync).not.toHaveBeenCalled();
        });

        test('should fail when security validation fails', () => {
            // Mock security validation failure
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: false,
                
                error: 'Invalid path',
            });

            const result = fileService.ensureDirectoryExists('/invalid/path');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Security validation failed');
            expect(mockFs.mkdirSync).not.toHaveBeenCalled();
        });

        test('should handle fs.mkdirSync errors', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/directory',
                
            });

            // Mock fs.existsSync to return false
            mockFs.existsSync.mockReturnValue(false);

            // Mock fs.mkdirSync to throw an error
            mockFs.mkdirSync.mockImplementation(() => {
                throw new Error('Permission denied');
            });

            const result = fileService.ensureDirectoryExists('/test/directory');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Failed to create directory');
        });
    });

    describe('writeFile', () => {
        test('should write file successfully', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock ensureDirectoryExists success
            mockFs.existsSync.mockReturnValue(true);

            const result = fileService.writeFile('/test/file.txt', 'test content');

            expect(result.success).toBe(true);
            expect(result.message).toContain('File written successfully');
            expect(result.filePath).toBe('/test/file.txt');
            expect(mockFs.writeFileSync).toHaveBeenCalledWith('/test/file.txt', 'test content', 'utf8');
        });

        test('should fail when file path is empty', () => {
            const result = fileService.writeFile('', 'content');

            expect(result.success).toBe(false);
            expect(result.message).toBe('File path cannot be empty or null');
            expect(mockFs.writeFileSync).not.toHaveBeenCalled();
        });

        test('should fail when content is null', () => {
            const result = fileService.writeFile('/test/file.txt', null as any);

            expect(result.success).toBe(false);
            expect(result.message).toBe('Content cannot be null or undefined');
            expect(mockFs.writeFileSync).not.toHaveBeenCalled();
        });

        test('should fail when security validation fails', () => {
            // Mock security validation failure
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: false,
                
                error: 'Invalid path',
            });

            const result = fileService.writeFile('/invalid/file.txt', 'content');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Security validation failed');
            expect(mockFs.writeFileSync).not.toHaveBeenCalled();
        });

        test('should handle fs.writeFileSync errors', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock ensureDirectoryExists success
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.writeFileSync to throw an error
            mockFs.writeFileSync.mockImplementation(() => {
                throw new Error('Disk full');
            });

            const result = fileService.writeFile('/test/file.txt', 'content');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Failed to write file');
        });
    });

    describe('readFile', () => {
        test('should read file successfully', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.readFileSync to return content
            mockFs.readFileSync.mockReturnValue('file content');

            const result = fileService.readFile('/test/file.txt');

            expect(result.success).toBe(true);
            expect(result.message).toContain('File read successfully');
            expect(result.filePath).toBe('/test/file.txt');
            expect(result.content).toBe('file content');
            expect(mockFs.readFileSync).toHaveBeenCalledWith('/test/file.txt', 'utf8');
        });

        test('should fail when file path is empty', () => {
            const result = fileService.readFile('');

            expect(result.success).toBe(false);
            expect(result.message).toBe('File path cannot be empty or null');
            expect(mockFs.readFileSync).not.toHaveBeenCalled();
        });

        test('should fail when file does not exist', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return false
            mockFs.existsSync.mockReturnValue(false);

            const result = fileService.readFile('/test/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('File does not exist');
            expect(mockFs.readFileSync).not.toHaveBeenCalled();
        });

        test('should fail when security validation fails', () => {
            // Mock security validation failure
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: false,
                
                error: 'Invalid path',
            });

            const result = fileService.readFile('/invalid/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Security validation failed');
            expect(mockFs.readFileSync).not.toHaveBeenCalled();
        });

        test('should handle fs.readFileSync errors', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.readFileSync to throw an error
            mockFs.readFileSync.mockImplementation(() => {
                throw new Error('Permission denied');
            });

            const result = fileService.readFile('/test/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Failed to read file');
        });
    });

    describe('deleteFile', () => {
        test('should delete file successfully', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            const result = fileService.deleteFile('/test/file.txt');

            expect(result.success).toBe(true);
            expect(result.message).toContain('File deleted successfully');
            expect(result.filePath).toBe('/test/file.txt');
            expect(mockFs.unlinkSync).toHaveBeenCalledWith('/test/file.txt');
        });

        test('should fail when file path is empty', () => {
            const result = fileService.deleteFile('');

            expect(result.success).toBe(false);
            expect(result.message).toBe('File path cannot be empty or null');
            expect(mockFs.unlinkSync).not.toHaveBeenCalled();
        });

        test('should fail when file does not exist', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return false
            mockFs.existsSync.mockReturnValue(false);

            const result = fileService.deleteFile('/test/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('File does not exist');
            expect(mockFs.unlinkSync).not.toHaveBeenCalled();
        });

        test('should handle fs.unlinkSync errors', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.unlinkSync to throw an error
            mockFs.unlinkSync.mockImplementation(() => {
                throw new Error('Permission denied');
            });

            const result = fileService.deleteFile('/test/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Failed to delete file');
        });
    });

    describe('fileExists', () => {
        test('should return true when file exists', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            const result = fileService.fileExists('/test/file.txt');

            expect(result.success).toBe(true);
            expect(result.exists).toBe(true);
            expect(result.message).toContain('File exists');
        });

        test('should return false when file does not exist', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/test/file.txt',
                
            });

            // Mock fs.existsSync to return false
            mockFs.existsSync.mockReturnValue(false);

            const result = fileService.fileExists('/test/file.txt');

            expect(result.success).toBe(true);
            expect(result.exists).toBe(false);
            expect(result.message).toContain('File does not exist');
        });

        test('should fail when security validation fails', () => {
            // Mock security validation failure
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: false,
                
                error: 'Invalid path',
            });

            const result = fileService.fileExists('/invalid/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Security validation failed');
        });
    });



        describe('generateUniqueFilename', () => {
        test('should generate unique filename with timestamp', () => {
            const filename = fileService.generateUniqueFilename('test', 'txt');
            
            expect(filename).toMatch(/^test-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.txt$/);
        });

        test('should handle empty extension', () => {
            const filename = fileService.generateUniqueFilename('test', '');
            
            expect(filename).toMatch(/^test-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z\.$/);
        });
    });

        describe('generateUserFriendlyFilename', () => {
        test('should generate friendly filename from URL', () => {
            const filename = fileService.generateUserFriendlyFilename('https://example.com/page', 'report');
            
            expect(filename).toMatch(/^example-com-accessibility-report-\d{2}-\d{2}-\d{4},-\d{2}-\d{2}report$/);
        });

        test('should handle URL with special characters', () => {
            const filename = fileService.generateUserFriendlyFilename('https://example.com/page with spaces', 'report');
            
            expect(filename).toMatch(/^example-com-accessibility-report-\d{2}-\d{2}-\d{4},-\d{2}-\d{2}report$/);
        });

        test('should handle URL without suffix', () => {
            const filename = fileService.generateUserFriendlyFilename('https://example.com/page');
            
            expect(filename).toMatch(/^example-com-accessibility-report-\d{2}-\d{2}-\d{4},-\d{2}-\d{2}$/);
        });
    });

    describe('moveFile', () => {
        test('should move file successfully', () => {
            // Mock security validation success for both paths
            mockSecurityService.validateFilePath
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/source/file.txt',
                    
                })
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/destination/file.txt',
                    
                });

            // Mock fs.existsSync to return true for source, false for destination
            mockFs.existsSync
                .mockReturnValueOnce(true)  // source exists
                .mockReturnValueOnce(false); // destination doesn't exist

            // Mock path.dirname to return destination directory
            mockPath.dirname.mockReturnValue('/destination');

            // Mock ensureDirectoryExists to succeed
            const ensureDirSpy = jest.spyOn(fileService, 'ensureDirectoryExists').mockReturnValue({
                success: true,
                message: 'Directory created successfully',
                filePath: '/destination',
            });

            const result = fileService.moveFile('/source/file.txt', '/destination/file.txt');

            // Restore the original method
            ensureDirSpy.mockRestore();

            expect(result.success).toBe(true);
            expect(result.message).toContain('File moved successfully');
            expect(mockFs.renameSync).toHaveBeenCalledWith('/source/file.txt', '/destination/file.txt');
        });

        test('should fail when source file does not exist', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/source/file.txt',
                
            });

            // Mock fs.existsSync to return false
            mockFs.existsSync.mockReturnValue(false);

            const result = fileService.moveFile('/source/file.txt', '/destination/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Source file does not exist');
            expect(mockFs.renameSync).not.toHaveBeenCalled();
        });

        test('should handle fs.renameSync errors', () => {
            // Mock security validation success
            mockSecurityService.validateFilePath.mockReturnValue({
                isValid: true,
                sanitizedValue: '/source/file.txt',
                
            });

            // Mock fs.existsSync to return true
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.renameSync to throw an error
            mockFs.renameSync.mockImplementation(() => {
                throw new Error('Permission denied');
            });

            const result = fileService.moveFile('/source/file.txt', '/destination/file.txt');

            expect(result.success).toBe(false);
            expect(result.message).toContain('Failed to move file');
        });
    });

    describe('moveFilesByPattern', () => {
        test('should move files matching pattern successfully', () => {
            // Mock security validation success for both source and destination
            mockSecurityService.validateFilePath
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/source',
                    
                })
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/destination',
                    
                });

            // Mock fs.existsSync to return true for source directory
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.readdirSync to return file list
            mockFs.readdirSync.mockReturnValue(['file1.json', 'file2.txt', 'file3.json'] as any);

            // Mock fs.statSync to return file stats
            mockFs.statSync.mockReturnValue({
                isFile: () => true,
                isDirectory: () => false,
            } as any);

            // Mock path.join to return proper file paths
            mockPath.join.mockImplementation((...args) => args.join('/'));

            // Mock ensureDirectoryExists to succeed
            const ensureDirSpy = jest.spyOn(fileService, 'ensureDirectoryExists').mockReturnValue({
                success: true,
                message: 'Directory created successfully',
                filePath: '/destination',
            });

            // Mock the moveFile method to succeed
            const moveFileSpy = jest.spyOn(fileService, 'moveFile').mockReturnValue({
                success: true,
                message: 'File moved successfully',
                filePath: '/destination/file1.json',
            });

            const result = fileService.moveFilesByPattern('/source', '/destination', /\.json$/);

            // Restore the original methods
            ensureDirSpy.mockRestore();
            moveFileSpy.mockRestore();

            expect(result.success).toBe(true);
            expect(result.movedFiles).toEqual(['file1.json', 'file3.json']);
            expect(result.message).toContain('File move completed');

            // Restore the original method
            moveFileSpy.mockRestore();
        });

        test('should handle errors during file moves', () => {
            // Mock security validation success for both source and destination
            mockSecurityService.validateFilePath
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/source',
                    
                })
                .mockReturnValueOnce({
                    isValid: true,
                    sanitizedValue: '/destination',
                    
                });

            // Mock fs.existsSync to return true for source directory
            mockFs.existsSync.mockReturnValue(true);

            // Mock fs.readdirSync to return file list
            mockFs.readdirSync.mockReturnValue(['file1.json', 'file2.json'] as any);

            // Mock fs.statSync to return file stats
            mockFs.statSync.mockReturnValue({
                isFile: () => true,
                isDirectory: () => false,
            } as any);

            // Mock path.join to return proper file paths
            mockPath.join.mockImplementation((...args) => args.join('/'));

            // Mock ensureDirectoryExists to succeed
            const ensureDirSpy = jest.spyOn(fileService, 'ensureDirectoryExists').mockReturnValue({
                success: true,
                message: 'Directory created successfully',
                filePath: '/destination',
            });

            // Mock the moveFile method to succeed for first file, fail for second
            const moveFileSpy = jest.spyOn(fileService, 'moveFile')
                .mockReturnValueOnce({
                    success: true,
                    message: 'File moved successfully',
                    filePath: '/destination/file1.json',
                })
                .mockReturnValueOnce({
                    success: false,
                    message: 'Failed to move file2.json: Permission denied',
                });

            const result = fileService.moveFilesByPattern('/source', '/destination', /\.json$/);

            // Restore the original methods
            ensureDirSpy.mockRestore();
            moveFileSpy.mockRestore();

            expect(result.success).toBe(true);
            expect(result.movedFiles).toEqual(['file1.json']);
            expect(result.errors).toEqual(['Failed to move file2.json: Failed to move file2.json: Permission denied']);
        });
    });
}); 