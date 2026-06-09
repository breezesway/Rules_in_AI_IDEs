import { afterEach, beforeEach, describe, expect, it, jest } from '@jest/globals';
import { FileOperationsService } from '../../playwright/tests/utils/services/file-operations-service';
import * as fs from 'fs';
import * as path from 'path';

// Mock the fs module
jest.mock('fs');
jest.mock('path');

describe('FileOperationsService', () => {
  let fileService: FileOperationsService;
  let mockFs: any;
  let mockPath: any;

  beforeEach(() => {
    // Reset singleton instance before each test
    (FileOperationsService as any).instance = undefined;
    fileService = FileOperationsService.getInstance();

    // Get mocked modules
    mockFs = jest.mocked(fs);
    mockPath = jest.mocked(path);

    // Setup default mocks
    mockPath.resolve.mockImplementation((...args) => args.join('/'));
    mockPath.dirname.mockImplementation(filePath => filePath.split('/').slice(0, -1).join('/'));
    mockPath.extname.mockImplementation(filePath => {
      const parts = filePath.split('.');
      return parts.length > 1 ? `.${parts.pop()}` : '';
    });
  });

  afterEach(() => {
    // Clean up singleton instance after each test
    (FileOperationsService as any).instance = undefined;
    jest.clearAllMocks();
  });

  describe('Singleton Pattern', () => {
    it('should return the same instance on multiple calls', () => {
      const instance1 = FileOperationsService.getInstance();
      const instance2 = FileOperationsService.getInstance();

      expect(instance1).toBe(instance2);
    });

    it('should not allow direct instantiation', () => {
      expect(() => new (FileOperationsService as any)()).toThrow();
    });
  });

  describe('File Writing Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.writeFileSync.mockImplementation(() => {});
      mockFs.mkdirSync.mockImplementation(() => {});
    });

    it('should write file successfully', () => {
      const filePath = 'test/report.pdf';
      const content = 'test content';

      const result = fileService.writeFile(filePath, content);

      expect(result.success).toBe(true);
      expect(result.message).toContain('File written successfully');
      expect(result.filePath).toBe(filePath);
      expect(mockFs.writeFileSync).toHaveBeenCalledWith(filePath, content, 'utf8');
    });

    it('should create directory if it does not exist', () => {
      mockFs.existsSync.mockReturnValue(false);

      const filePath = 'test/new-folder/report.pdf';
      const content = 'test content';

      const result = fileService.writeFile(filePath, content);

      expect(result.success).toBe(true);
      expect(mockFs.mkdirSync).toHaveBeenCalledWith('test/new-folder', { recursive: true });
      expect(mockFs.writeFileSync).toHaveBeenCalledWith(filePath, content, 'utf8');
    });

    it('should handle file write errors', () => {
      const error = new Error('Permission denied');
      mockFs.writeFileSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.writeFile('test/report.pdf', 'content');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to write file');
      expect(result.message).toContain('Permission denied');
    });

    it('should handle directory creation errors', () => {
      mockFs.existsSync.mockReturnValue(false);
      mockFs.mkdirSync.mockImplementation(() => {
        throw new Error('Cannot create directory');
      });

      const result = fileService.writeFile('test/new-folder/report.pdf', 'content');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to create directory');
    });

    it('should reject files with invalid paths', () => {
      const result = fileService.writeFile('../../../etc/passwd', 'malicious content');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });

    it('should reject files with invalid extensions', () => {
      const result = fileService.writeFile('malicious.exe', 'malicious content');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('File Reading Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.readFileSync.mockReturnValue('file content');
    });

    it('should read file successfully', () => {
      const filePath = 'test/report.pdf';

      const result = fileService.readFile(filePath);

      expect(result.success).toBe(true);
      expect(result.content).toBe('file content');
      expect(result.filePath).toBe(filePath);
      expect(mockFs.readFileSync).toHaveBeenCalledWith(filePath, 'utf8');
    });

    it('should handle non-existent files', () => {
      mockFs.existsSync.mockReturnValue(false);

      const result = fileService.readFile('non-existent.txt');

      expect(result.success).toBe(false);
      expect(result.message).toContain('File does not exist');
    });

    it('should handle file read errors', () => {
      const error = new Error('Permission denied');
      mockFs.readFileSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.readFile('test/report.pdf');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to read file');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject reading files with invalid paths', () => {
      const result = fileService.readFile('../../../etc/passwd');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });

    it('should reject reading files with invalid extensions', () => {
      const result = fileService.readFile('malicious.exe');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('File Deletion Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.unlinkSync.mockImplementation(() => {});
    });

    it('should delete file successfully', () => {
      const filePath = 'test/report.pdf';

      const result = fileService.deleteFile(filePath);

      expect(result.success).toBe(true);
      expect(result.message).toContain('File deleted successfully');
      expect(result.filePath).toBe(filePath);
      expect(mockFs.unlinkSync).toHaveBeenCalledWith(filePath);
    });

    it('should handle non-existent files during deletion', () => {
      mockFs.existsSync.mockReturnValue(false);

      const result = fileService.deleteFile('non-existent.txt');

      expect(result.success).toBe(false);
      expect(result.message).toContain('File does not exist');
    });

    it('should handle file deletion errors', () => {
      const error = new Error('Permission denied');
      mockFs.unlinkSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.deleteFile('test/report.pdf');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to delete file');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject deleting files with invalid paths', () => {
      const result = fileService.deleteFile('../../../etc/passwd');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('Directory Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(false);
      mockFs.mkdirSync.mockImplementation(() => {});
    });

    it('should create directory successfully', () => {
      const dirPath = 'test/new-directory';

      const result = fileService.ensureDirectoryExists(dirPath);

      expect(result.success).toBe(true);
      expect(result.message).toContain('Directory created successfully');
      expect(result.filePath).toBe(dirPath);
      expect(mockFs.mkdirSync).toHaveBeenCalledWith(dirPath, { recursive: true });
    });

    it('should handle existing directory', () => {
      mockFs.existsSync.mockReturnValue(true);

      const result = fileService.ensureDirectoryExists('test/existing-directory');

      expect(result.success).toBe(true);
      expect(result.message).toContain('Directory already exists');
      expect(mockFs.mkdirSync).not.toHaveBeenCalled();
    });

    it('should handle directory creation errors', () => {
      const error = new Error('Permission denied');
      mockFs.mkdirSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.ensureDirectoryExists('test/new-directory');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to create directory');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject creating directories with invalid paths', () => {
      const result = fileService.ensureDirectoryExists('../../../etc/malicious');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('File Listing Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.readdirSync.mockReturnValue(['file1.txt', 'file2.pdf', 'subfolder']);
      mockFs.statSync.mockReturnValue({ isDirectory: () => false });
    });

    it('should list files successfully', () => {
      const dirPath = 'test/directory';

      const result = fileService.listFiles(dirPath);

      expect(result.success).toBe(true);
      expect(result.files).toEqual(['file1.txt', 'file2.pdf', 'subfolder']);
      expect(result.filePath).toBe(dirPath);
      expect(mockFs.readdirSync).toHaveBeenCalledWith(dirPath);
    });

    it('should handle non-existent directories', () => {
      mockFs.existsSync.mockReturnValue(false);

      const result = fileService.listFiles('non-existent-directory');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Directory does not exist');
    });

    it('should handle directory listing errors', () => {
      const error = new Error('Permission denied');
      mockFs.readdirSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.listFiles('test/directory');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to list directory');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject listing directories with invalid paths', () => {
      const result = fileService.listFiles('../../../etc');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });

    it('should filter files by extension', () => {
      const result = fileService.listFiles('test/directory', '.pdf');

      expect(result.success).toBe(true);
      expect(result.files).toEqual(['file2.pdf']);
    });
  });

  describe('File Existence Checking', () => {
    it('should check file existence correctly', () => {
      mockFs.existsSync.mockReturnValue(true);

      const result = fileService.fileExists('test/report.pdf');

      expect(result.success).toBe(true);
      expect(result.exists).toBe(true);
      expect(mockFs.existsSync).toHaveBeenCalledWith('test/report.pdf');
    });

    it('should handle non-existent files', () => {
      mockFs.existsSync.mockReturnValue(false);

      const result = fileService.fileExists('non-existent.txt');

      expect(result.success).toBe(true);
      expect(result.exists).toBe(false);
    });

    it('should handle file existence check errors', () => {
      const error = new Error('Permission denied');
      mockFs.existsSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.fileExists('test/report.pdf');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to check file existence');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject checking files with invalid paths', () => {
      const result = fileService.fileExists('../../../etc/passwd');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('File Statistics', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.statSync.mockReturnValue({
        size: 1024,
        isDirectory: () => false,
        isFile: () => true,
        mtime: new Date('2023-01-01'),
        ctime: new Date('2023-01-01'),
      });
    });

    it('should get file statistics successfully', () => {
      const filePath = 'test/report.pdf';

      const result = fileService.getFileStats(filePath);

      expect(result.success).toBe(true);
      expect(result.stats).toEqual({
        size: 1024,
        isDirectory: false,
        isFile: true,
        mtime: new Date('2023-01-01'),
        ctime: new Date('2023-01-01'),
      });
      expect(mockFs.statSync).toHaveBeenCalledWith(filePath);
    });

    it('should handle non-existent files', () => {
      mockFs.existsSync.mockReturnValue(false);

      const result = fileService.getFileStats('non-existent.txt');

      expect(result.success).toBe(false);
      expect(result.message).toContain('File does not exist');
    });

    it('should handle file statistics errors', () => {
      const error = new Error('Permission denied');
      mockFs.statSync.mockImplementation(() => {
        throw error;
      });

      const result = fileService.getFileStats('test/report.pdf');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Failed to get file statistics');
      expect(result.message).toContain('Permission denied');
    });

    it('should reject getting statistics for files with invalid paths', () => {
      const result = fileService.getFileStats('../../../etc/passwd');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('Cleanup Operations', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.readdirSync.mockReturnValue(['old-report-1.pdf', 'old-report-2.pdf', 'keep-this.txt']);
      mockFs.statSync.mockReturnValue({
        mtime: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day old
        isDirectory: () => false,
      });
      mockFs.unlinkSync.mockImplementation(() => {});
    });

    it('should cleanup old files successfully', () => {
      const dirPath = 'test/reports';
      const maxAge = 1000 * 60 * 60 * 12; // 12 hours

      const result = fileService.cleanupOldFiles(dirPath, maxAge);

      expect(result.success).toBe(true);
      expect(result.deletedFiles).toEqual(['old-report-1.pdf', 'old-report-2.pdf']);
      expect(result.message).toContain('Cleanup completed');
      expect(mockFs.unlinkSync).toHaveBeenCalledTimes(2);
    });

    it('should handle cleanup with file pattern', () => {
      const result = fileService.cleanupOldFiles('test/reports', 1000 * 60 * 60 * 12, /report/);

      expect(result.success).toBe(true);
      expect(result.deletedFiles).toEqual(['old-report-1.pdf', 'old-report-2.pdf']);
      expect(mockFs.unlinkSync).toHaveBeenCalledTimes(2);
    });

    it('should handle cleanup errors gracefully', () => {
      mockFs.unlinkSync.mockImplementation(() => {
        throw new Error('Permission denied');
      });

      const result = fileService.cleanupOldFiles('test/reports', 1000 * 60 * 60 * 12);

      expect(result.success).toBe(true);
      expect(result.deletedFiles).toEqual([]);
      expect(result.errors).toHaveLength(2);
      expect(result.message).toContain('Cleanup completed with errors');
    });

    it('should reject cleanup with invalid directory paths', () => {
      const result = fileService.cleanupOldFiles('../../../etc', 1000);

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
    });
  });

  describe('Security Integration', () => {
    it('should validate file paths before operations', () => {
      const dangerousPaths = [
        '../../../etc/passwd',
        '/etc/shadow',
        'C:\\Windows\\System32\\config\\sam',
        '..\\..\\windows\\system32',
      ];

      dangerousPaths.forEach(path => {
        expect(fileService.writeFile(path, 'content').success).toBe(false);
        expect(fileService.readFile(path).success).toBe(false);
        expect(fileService.deleteFile(path).success).toBe(false);
        expect(fileService.fileExists(path).success).toBe(false);
      });
    });

    it('should validate file extensions before operations', () => {
      const dangerousExtensions = ['malicious.exe', 'script.bat', 'payload.sh', 'trojan.php'];

      dangerousExtensions.forEach(fileName => {
        expect(fileService.writeFile(fileName, 'content').success).toBe(false);
        expect(fileService.readFile(fileName).success).toBe(false);
        expect(fileService.deleteFile(fileName).success).toBe(false);
        expect(fileService.fileExists(fileName).success).toBe(false);
      });
    });

    it('should allow operations on valid files', () => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.writeFileSync.mockImplementation(() => {});
      mockFs.readFileSync.mockReturnValue('content');

      const validFiles = [
        'report.pdf',
        'data.json',
        'page.html',
        'readme.txt',
        'document.md',
        'image.png',
        'photo.jpg',
      ];

      validFiles.forEach(fileName => {
        expect(fileService.writeFile(fileName, 'content').success).toBe(true);
        expect(fileService.readFile(fileName).success).toBe(true);
        expect(fileService.fileExists(fileName).success).toBe(true);
      });
    });
  });

  describe('Error Handling', () => {
    it('should handle null and undefined inputs gracefully', () => {
      expect(fileService.writeFile(null as any, 'content').success).toBe(false);
      expect(fileService.writeFile('file.txt', null as any).success).toBe(false);
      expect(fileService.readFile(undefined as any).success).toBe(false);
      expect(fileService.deleteFile(null as any).success).toBe(false);
    });

    it('should handle empty string inputs gracefully', () => {
      expect(fileService.writeFile('', 'content').success).toBe(false);
      expect(fileService.readFile('').success).toBe(false);
      expect(fileService.deleteFile('').success).toBe(false);
    });

    it('should provide meaningful error messages', () => {
      const result = fileService.writeFile('../invalid/path.txt', 'content');

      expect(result.success).toBe(false);
      expect(result.message).toContain('Security validation failed');
      expect(result.message).toContain('directory traversal');
    });
  });

  describe('Performance', () => {
    beforeEach(() => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.writeFileSync.mockImplementation(() => {});
      mockFs.readFileSync.mockReturnValue('content');
    });

    it('should handle multiple file operations efficiently', () => {
      const startTime = Date.now();

      for (let i = 0; i < 100; i++) {
        fileService.writeFile(`file-${i}.txt`, `content-${i}`);
        fileService.readFile(`file-${i}.txt`);
        fileService.fileExists(`file-${i}.txt`);
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    });
  });
});
