import * as path from 'path';
import { URL } from 'url';

/**
 * Interface for security validation results
 */
export interface SecurityValidationResult {
  /** Whether the validation passed */
  isValid: boolean;
  /** Error message if validation failed */
  error?: string;
  /** Sanitized/normalized value if applicable */
  sanitizedValue?: string;
}

/**
 * Singleton service for security validations across the application
 * Provides centralized security checks for URLs, file paths, and user input
 */
export class SecurityValidationService {
  private static instance: SecurityValidationService;

  // Security configuration
  private readonly ALLOWED_PROTOCOLS = ['http:', 'https:'];
  private readonly BLOCKED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '::1',
    // Add other internal/blocked domains as needed
  ];
  private readonly ALLOWED_FILE_EXTENSIONS = [
    '.json',
    '.html',
    '.pdf',
    '.txt',
    '.md',
    '.png',
    '.jpg',
    '.jpeg',
  ];
  private readonly BLOCKED_PATHS = [
    '../',
    '..\\',
    '/etc/',
    '/var/',
    '/root/',
    '/home/',
    'C:\\Windows\\',
    'C:\\Users\\',
  ];

  private constructor() {
    // Private constructor to enforce singleton pattern
    if (SecurityValidationService.instance) {
      throw new Error(
        'Cannot instantiate SecurityValidationService directly. Use getInstance() instead.'
      );
    }
  }

  /**
   * Gets the singleton instance of SecurityValidationService
   * @returns The singleton SecurityValidationService instance
   */
  static getInstance(): SecurityValidationService {
    if (!SecurityValidationService.instance) {
      SecurityValidationService.instance = new SecurityValidationService();
    }
    return SecurityValidationService.instance;
  }

  /**
   * Validates a URL for security issues
   * @param url The URL to validate
   * @param allowLocalhost Whether to allow localhost URLs (default: false)
   * @returns SecurityValidationResult with validation status
   */
  validateUrl(url: string, allowLocalhost: boolean = false): SecurityValidationResult {
    try {
      // Basic format validation
      if (!url || typeof url !== 'string' || url.trim().length === 0) {
        return {
          isValid: false,
          error: 'URL cannot be empty',
        };
      }

      // Normalize and parse URL
      const normalizedUrl = url.trim();
      const urlObj = new URL(normalizedUrl);

      // Protocol validation
      if (!this.ALLOWED_PROTOCOLS.includes(urlObj.protocol)) {
        return {
          isValid: false,
          error: `Protocol '${urlObj.protocol}' is not allowed. Only HTTP and HTTPS are permitted.`,
        };
      }

      // Hostname validation
      if (!allowLocalhost && this.isBlockedDomain(urlObj.hostname)) {
        return {
          isValid: false,
          error: `Domain '${urlObj.hostname}' is not allowed for security reasons.`,
        };
      }

      // Check for suspicious URL patterns
      if (this.containsSuspiciousUrlPatterns(normalizedUrl)) {
        return {
          isValid: false,
          error: 'URL contains suspicious patterns that may pose security risks.',
        };
      }

      // Sanitize URL (remove fragments, clean query params)
      const sanitizedUrl = this.sanitizeUrl(urlObj);

      return {
        isValid: true,
        sanitizedValue: sanitizedUrl,
      };
    } catch (error) {
      return {
        isValid: false,
        error: `Invalid URL format: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  }

  /**
   * Validates a file path for security issues (directory traversal, etc.)
   * @param filePath The file path to validate
   * @param baseDir The base directory that files should be contained within
   * @param isDirectory Whether the path is a directory (skips file extension validation)
   * @returns SecurityValidationResult with validation status
   */
  validateFilePath(
    filePath: string,
    baseDir?: string,
    isDirectory: boolean = false
  ): SecurityValidationResult {
    try {
      // Basic validation
      if (!filePath || typeof filePath !== 'string' || filePath.trim().length === 0) {
        return {
          isValid: false,
          error: 'File path cannot be empty',
        };
      }

      const normalizedPath = filePath.trim();

      // Check for directory traversal attempts
      if (this.containsDirectoryTraversal(normalizedPath)) {
        return {
          isValid: false,
          error: 'File path contains directory traversal patterns which are not allowed.',
        };
      }

      // Check for blocked path patterns
      if (this.containsBlockedPaths(normalizedPath)) {
        return {
          isValid: false,
          error: 'File path contains blocked system paths.',
        };
      }

      // Resolve and validate the path
      const resolvedPath = path.resolve(normalizedPath);

      // If base directory is specified, ensure the resolved path is within it
      if (baseDir) {
        const resolvedBaseDir = path.resolve(baseDir);
        const normalizedBaseDir = resolvedBaseDir.replace(/\\/g, '/');
        const normalizedResolvedPath = resolvedPath.replace(/\\/g, '/');

        if (!normalizedResolvedPath.startsWith(normalizedBaseDir)) {
          return {
            isValid: false,
            error: 'File path is outside the allowed base directory.',
          };
        }
      }

      // Validate file extension if it has one (skip for directories)
      if (!isDirectory) {
        const ext = path.extname(resolvedPath).toLowerCase();
        if (ext && !this.ALLOWED_FILE_EXTENSIONS.includes(ext)) {
          return {
            isValid: false,
            error: `File extension '${ext}' is not allowed.`,
          };
        }
      }

      // Return the normalized path (not fully resolved) for better test compatibility
      const normalizedSanitizedPath = normalizedPath.replace(/\\/g, '/');

      return {
        isValid: true,
        sanitizedValue: normalizedSanitizedPath,
      };
    } catch (error) {
      return {
        isValid: false,
        error: `Invalid file path: ${error instanceof Error ? error.message : 'Unknown error'}`,
      };
    }
  }

  /**
   * Sanitizes user input to prevent injection attacks
   * @param input The input string to sanitize
   * @returns SecurityValidationResult with sanitized input
   */
  sanitizeInput(input: string): SecurityValidationResult {
    if (!input || typeof input !== 'string') {
      return {
        isValid: false,
        error: 'Input must be a non-empty string',
      };
    }

    // Remove potentially dangerous characters and patterns
    let sanitized = input
      .replace(/[<>\"']/g, '') // Remove HTML/XML characters
      .replace(/javascript:/gi, '') // Remove javascript: protocol
      .replace(/data:/gi, '') // Remove data: protocol
      .replace(/vbscript:/gi, '') // Remove vbscript: protocol
      .replace(/on\w+\s*=/gi, '') // Remove event handlers
      .trim();

    // Limit length to prevent buffer overflow attempts
    if (sanitized.length > 2048) {
      sanitized = sanitized.substring(0, 2048);
    }

    return {
      isValid: true,
      sanitizedValue: sanitized,
    };
  }

  /**
   * Checks if a domain is in the blocked list
   * @param hostname The hostname to check
   * @returns True if the domain is blocked
   */
  private isBlockedDomain(hostname: string): boolean {
    const lowerHostname = hostname.toLowerCase();
    return this.BLOCKED_DOMAINS.some(
      blocked => lowerHostname === blocked || lowerHostname.endsWith(`.${blocked}`)
    );
  }

  /**
   * Checks for suspicious URL patterns
   * @param url The URL to check
   * @returns True if suspicious patterns are found
   */
  private containsSuspiciousUrlPatterns(url: string): boolean {
    const suspiciousPatterns = [
      /javascript:/i,
      /data:/i,
      /vbscript:/i,
      /file:/i,
      /ftp:/i,
      /%2e%2e%2f/i, // URL encoded ../
      /%2e%2e%5c/i, // URL encoded ..\
      /\.\.%2f/i, // Mixed encoding ../
      /\.\.%5c/i, // Mixed encoding ..\
      /\.\.\//i, // Direct directory traversal
      /\.\.\\/i, // Direct directory traversal
    ];

    return suspiciousPatterns.some(pattern => pattern.test(url));
  }

  /**
   * Checks for directory traversal patterns in file paths
   * @param filePath The file path to check
   * @returns True if directory traversal patterns are found
   */
  private containsDirectoryTraversal(filePath: string): boolean {
    const traversalPatterns = [
      /\.\./,
      /%2e%2e/i,
      /\.%2e/i,
      /%2e\./i,
      /\.\.%2f/i,
      /%2e%2e%2f/i,
      /\.\.%5c/i,
      /%2e%2e%5c/i,
    ];

    return traversalPatterns.some(pattern => pattern.test(filePath));
  }

  /**
   * Checks for blocked system paths
   * @param filePath The file path to check
   * @returns True if blocked paths are found
   */
  private containsBlockedPaths(filePath: string): boolean {
    const lowerPath = filePath.toLowerCase();
    return this.BLOCKED_PATHS.some(blocked => lowerPath.includes(blocked.toLowerCase()));
  }

  /**
   * Validates user input for security issues
   * @param input The user input to validate
   * @returns SecurityValidationResult with validation status
   */
  validateUserInput(input: string): SecurityValidationResult {
    try {
      // Handle empty input
      if (!input || typeof input !== 'string') {
        return {
          isValid: true,
          sanitizedValue: '',
        };
      }

      // Check for script tags
      const scriptPattern = /<script[^>]*>.*?<\/script>/gi;
      if (scriptPattern.test(input)) {
        return {
          isValid: false,
          error: 'User input contains potentially dangerous script tags.',
        };
      }

      // Check for HTML tags with event handlers
      const htmlEventPattern = /<[^>]*on\w+\s*=/gi;
      if (htmlEventPattern.test(input)) {
        return {
          isValid: false,
          error: 'User input contains potentially dangerous HTML event handlers.',
        };
      }

      // Check for SQL injection patterns
      const sqlPatterns = [
        /(\bselect\b|\binsert\b|\bupdate\b|\bdelete\b|\bdrop\b|\bcreate\b|\balter\b).*(\bfrom\b|\binto\b|\bset\b|\bwhere\b|\btable\b)/gi,
        /(\bunion\b|\bjoin\b).*(\bselect\b|\bfrom\b)/gi,
        /(\bor\b|\band\b).*(\b1\s*=\s*1\b|\b1\s*=\s*0\b)/gi,
        /(\bexec\b|\bexecute\b).*(\bsp_\b|\bxp_\b)/gi,
      ];

      for (const pattern of sqlPatterns) {
        if (pattern.test(input)) {
          return {
            isValid: false,
            error: 'User input contains potentially dangerous SQL injection patterns.',
          };
        }
      }

      // Sanitize input by escaping dangerous characters
      const sanitizedInput = input
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\//g, '&#x2F;');

      return {
        isValid: true,
        sanitizedValue: sanitizedInput,
      };
    } catch {
      return {
        isValid: false,
        error: 'Failed to validate user input due to an unexpected error.',
      };
    }
  }

  /**
   * Sanitizes a URL by removing potentially dangerous elements
   * @param urlObj The parsed URL object
   * @returns Sanitized URL string
   */
  private sanitizeUrl(urlObj: URL): string {
    // Remove fragment
    urlObj.hash = '';

    // Remove dangerous query parameters
    const dangerousParams = ['script', 'javascript', 'vbscript', 'data'];
    dangerousParams.forEach(param => {
      urlObj.searchParams.delete(param);
    });

    // Remove trailing slash for consistency (including root path for domain-only URLs)
    let result = urlObj.toString();
    if (result.endsWith('/') && !result.includes('?')) {
      // Only remove trailing slash if there are no query parameters
      result = result.slice(0, -1);
    }

    return result;
  }
}
