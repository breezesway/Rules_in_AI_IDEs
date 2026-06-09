import { afterEach, beforeEach, describe, expect, it } from '@jest/globals';
import { SecurityValidationService } from '../../playwright/tests/utils/services/security-validation-service';

describe('SecurityValidationService', () => {
  let securityService: SecurityValidationService;

  beforeEach(() => {
    // Reset singleton instance before each test
    (SecurityValidationService as any).instance = undefined;
    securityService = SecurityValidationService.getInstance();
  });

  afterEach(() => {
    // Clean up singleton instance after each test
    (SecurityValidationService as any).instance = undefined;
  });

  describe('Singleton Pattern', () => {
    it('should return the same instance on multiple calls', () => {
      const instance1 = SecurityValidationService.getInstance();
      const instance2 = SecurityValidationService.getInstance();

      expect(instance1).toBe(instance2);
    });

    it('should not allow direct instantiation', () => {
      expect(() => new (SecurityValidationService as any)()).toThrow();
    });
  });

  describe('URL Validation', () => {
    describe('Valid URLs', () => {
      it('should validate standard HTTP URLs', () => {
        const result = securityService.validateUrl('http://example.com');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('http://example.com');
        expect(result.error).toBeUndefined();
      });

      it('should validate standard HTTPS URLs', () => {
        const result = securityService.validateUrl('https://example.com');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com');
        expect(result.error).toBeUndefined();
      });

      it('should validate URLs with paths', () => {
        const result = securityService.validateUrl('https://example.com/path/to/page');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com/path/to/page');
      });

      it('should validate URLs with query parameters', () => {
        const result = securityService.validateUrl('https://example.com/page?param=value');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com/page?param=value');
      });

      it('should validate URLs with ports', () => {
        const result = securityService.validateUrl('https://example.com:8080/path');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com:8080/path');
      });

      it('should validate localhost URLs when allowed', () => {
        const result = securityService.validateUrl('http://localhost:3000', true);

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('http://localhost:3000');
      });

      it('should validate IP addresses when allowed', () => {
        const result = securityService.validateUrl('http://192.168.1.1', true);

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('http://192.168.1.1');
      });
    });

    describe('Invalid URLs', () => {
      it('should reject empty URLs', () => {
        const result = securityService.validateUrl('');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('URL cannot be empty');
      });

      it('should reject null URLs', () => {
        const result = securityService.validateUrl(null as any);

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('URL cannot be empty');
      });

      it('should reject undefined URLs', () => {
        const result = securityService.validateUrl(undefined as any);

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('URL cannot be empty');
      });

      it('should reject URLs with invalid protocols', () => {
        const result = securityService.validateUrl('ftp://example.com');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe(
          "Protocol 'ftp:' is not allowed. Only HTTP and HTTPS are permitted."
        );
      });

      it('should reject javascript URLs', () => {
        const result = securityService.validateUrl('javascript:alert("xss")');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe(
          "Protocol 'javascript:' is not allowed. Only HTTP and HTTPS are permitted."
        );
      });

      it('should reject data URLs', () => {
        const result = securityService.validateUrl('data:text/html,<script>alert("xss")</script>');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe(
          "Protocol 'data:' is not allowed. Only HTTP and HTTPS are permitted."
        );
      });

      it('should reject localhost URLs by default', () => {
        const result = securityService.validateUrl('http://localhost:3000');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe("Domain 'localhost' is not allowed for security reasons.");
      });

      it('should reject 127.0.0.1 URLs by default', () => {
        const result = securityService.validateUrl('http://127.0.0.1:8080');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe("Domain '127.0.0.1' is not allowed for security reasons.");
      });

      it('should reject malformed URLs', () => {
        const result = securityService.validateUrl('not-a-url');

        expect(result.isValid).toBe(false);
        expect(result.error).toContain('Invalid URL format');
      });

      it('should reject URLs with suspicious patterns', () => {
        const result = securityService.validateUrl('https://example.com/../../../etc/passwd');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('URL contains suspicious patterns that may pose security risks.');
      });
    });

    describe('URL Sanitization', () => {
      it('should remove fragments from URLs', () => {
        const result = securityService.validateUrl('https://example.com/page#fragment');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com/page');
      });

      it('should trim whitespace from URLs', () => {
        const result = securityService.validateUrl('  https://example.com  ');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com');
      });

      it('should handle URLs with both query params and fragments', () => {
        const result = securityService.validateUrl('https://example.com/page?param=value#fragment');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe('https://example.com/page?param=value');
      });
    });
  });

  describe('File Path Validation', () => {
    describe('Valid File Paths', () => {
      it('should validate simple file paths', () => {
        const result = securityService.validateFilePath('report.pdf');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('report.pdf'));
      });

      it('should validate file paths with allowed extensions', () => {
        const validExtensions = ['.json', '.html', '.pdf', '.txt', '.md', '.png', '.jpg', '.jpeg'];

        validExtensions.forEach(ext => {
          const result = securityService.validateFilePath(`file${ext}`);
          expect(result.isValid).toBe(true);
        });
      });

      it('should validate file paths within base directory', () => {
        const result = securityService.validateFilePath('reports/report.pdf', '/app/reports');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('reports/report.pdf'));
      });

      it('should validate nested file paths', () => {
        const result = securityService.validateFilePath('folder/subfolder/file.txt');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('folder/subfolder/file.txt'));
      });
    });

    describe('Invalid File Paths', () => {
      it('should reject empty file paths', () => {
        const result = securityService.validateFilePath('');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('File path cannot be empty');
      });

      it('should reject null file paths', () => {
        const result = securityService.validateFilePath(null as any);

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('File path cannot be empty');
      });

      it('should reject file paths with directory traversal', () => {
        const dangerousPaths = [
          '../../../etc/passwd',
          '..\\..\\windows\\system32',
          './../../sensitive',
        ];

        dangerousPaths.forEach(path => {
          const result = securityService.validateFilePath(path);
          expect(result.isValid).toBe(false);
          expect(result.error).toBe(
            'File path contains directory traversal patterns which are not allowed.'
          );
        });
      });

      it('should reject file paths with blocked system paths', () => {
        const blockedPaths = [
          '/etc/passwd',
          '/var/log/auth.log',
          'C:\\Windows\\System32',
          '/root/.ssh/id_rsa',
        ];

        blockedPaths.forEach(path => {
          const result = securityService.validateFilePath(path);
          expect(result.isValid).toBe(false);
          expect(result.error).toBe('File path contains blocked system paths.');
        });
      });

      it('should reject file paths with disallowed extensions', () => {
        const dangerousExtensions = ['.exe', '.bat', '.sh', '.php', '.asp'];

        dangerousExtensions.forEach(ext => {
          const result = securityService.validateFilePath(`file${ext}`);
          expect(result.isValid).toBe(false);
          expect(result.error).toBe(`File extension '${ext}' is not allowed.`);
        });
      });

      it('should reject file paths outside base directory', () => {
        const result = securityService.validateFilePath('/tmp/outside.txt', '/app/reports');

        expect(result.isValid).toBe(false);
        expect(result.error).toBe('File path is outside the allowed base directory.');
      });
    });

    describe('Path Sanitization', () => {
      it('should resolve relative paths', () => {
        const result = securityService.validateFilePath('./reports/report.pdf');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('reports/report.pdf'));
      });

      it('should normalize path separators', () => {
        const result = securityService.validateFilePath('reports\\subfolder\\file.txt');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('reports/subfolder/file.txt'));
      });

      it('should trim whitespace from paths', () => {
        const result = securityService.validateFilePath('  reports/file.txt  ');

        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(expect.stringContaining('reports/file.txt'));
      });
    });
  });

  describe('User Input Validation', () => {
    it('should validate safe user input', () => {
      const safeInputs = ['normal text', 'user@example.com', 'My Report Title', '123-456-7890'];

      safeInputs.forEach(input => {
        const result = securityService.validateUserInput(input);
        expect(result.isValid).toBe(true);
        expect(result.sanitizedValue).toBe(input);
      });
    });

    it('should reject user input with script tags', () => {
      const result = securityService.validateUserInput('<script>alert("xss")</script>');

      expect(result.isValid).toBe(false);
      expect(result.error).toBe(
        'User input contains potentially dangerous HTML or script content.'
      );
    });

    it('should reject user input with HTML tags', () => {
      const result = securityService.validateUserInput('<div onclick="alert(1)">Click me</div>');

      expect(result.isValid).toBe(false);
      expect(result.error).toBe(
        'User input contains potentially dangerous HTML or script content.'
      );
    });

    it('should reject user input with SQL injection patterns', () => {
      const sqlInjectionPatterns = [
        "'; DROP TABLE users; --",
        "' OR '1'='1",
        "1' UNION SELECT * FROM users--",
      ];

      sqlInjectionPatterns.forEach(pattern => {
        const result = securityService.validateUserInput(pattern);
        expect(result.isValid).toBe(false);
        expect(result.error).toBe(
          'User input contains potentially dangerous SQL injection patterns.'
        );
      });
    });

    it('should handle empty user input', () => {
      const result = securityService.validateUserInput('');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe('');
    });

    it('should sanitize user input by escaping dangerous characters', () => {
      const result = securityService.validateUserInput('John & Jane <friends>');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe('John &amp; Jane &lt;friends&gt;');
    });
  });

  describe('Security Configuration', () => {
    it('should have proper allowed protocols configuration', () => {
      const allowedProtocols = (securityService as any).ALLOWED_PROTOCOLS;

      expect(allowedProtocols).toContain('http:');
      expect(allowedProtocols).toContain('https:');
      expect(allowedProtocols).toHaveLength(2);
    });

    it('should have proper blocked domains configuration', () => {
      const blockedDomains = (securityService as any).BLOCKED_DOMAINS;

      expect(blockedDomains).toContain('localhost');
      expect(blockedDomains).toContain('127.0.0.1');
      expect(blockedDomains).toContain('0.0.0.0');
      expect(blockedDomains).toContain('::1');
    });

    it('should have proper allowed file extensions configuration', () => {
      const allowedExtensions = (securityService as any).ALLOWED_FILE_EXTENSIONS;

      expect(allowedExtensions).toContain('.json');
      expect(allowedExtensions).toContain('.html');
      expect(allowedExtensions).toContain('.pdf');
      expect(allowedExtensions).toContain('.txt');
      expect(allowedExtensions).toContain('.md');
      expect(allowedExtensions).toContain('.png');
      expect(allowedExtensions).toContain('.jpg');
      expect(allowedExtensions).toContain('.jpeg');
    });

    it('should have proper blocked paths configuration', () => {
      const blockedPaths = (securityService as any).BLOCKED_PATHS;

      expect(blockedPaths).toContain('../');
      expect(blockedPaths).toContain('..\\');
      expect(blockedPaths).toContain('/etc/');
      expect(blockedPaths).toContain('/var/');
      expect(blockedPaths).toContain('/root/');
      expect(blockedPaths).toContain('/home/');
      expect(blockedPaths).toContain('C:\\Windows\\');
      expect(blockedPaths).toContain('C:\\Users\\');
    });
  });

  describe('Edge Cases', () => {
    it('should handle very long URLs', () => {
      const longUrl = `https://example.com/${'a'.repeat(2000)}`;

      const result = securityService.validateUrl(longUrl);

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe(longUrl);
    });

    it('should handle URLs with special characters', () => {
      const result = securityService.validateUrl('https://example.com/path%20with%20spaces');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe('https://example.com/path%20with%20spaces');
    });

    it('should handle file paths with Unicode characters', () => {
      const result = securityService.validateFilePath('文件.txt');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe(expect.stringContaining('文件.txt'));
    });

    it('should handle mixed case extensions', () => {
      const result = securityService.validateFilePath('file.PDF');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe(expect.stringContaining('file.PDF'));
    });

    it('should handle URLs with international domain names', () => {
      const result = securityService.validateUrl('https://例え.テスト');

      expect(result.isValid).toBe(true);
      expect(result.sanitizedValue).toBe('https://例え.テスト');
    });
  });

  describe('Performance', () => {
    it('should validate URLs quickly', () => {
      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        securityService.validateUrl(`https://example${i}.com`);
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    });

    it('should validate file paths quickly', () => {
      const startTime = Date.now();

      for (let i = 0; i < 1000; i++) {
        securityService.validateFilePath(`file${i}.txt`);
      }

      const endTime = Date.now();
      const duration = endTime - startTime;

      expect(duration).toBeLessThan(1000); // Should complete in less than 1 second
    });
  });
});
