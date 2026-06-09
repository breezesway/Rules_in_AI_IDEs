import * as fs from 'fs';
import * as path from 'path';
import { ConfigurationService } from './configuration-service';

export interface FileOperationResult {
    success: boolean;
    message: string;
    filePath?: string;
}

export class FileOperationsService {
    private static instance: FileOperationsService;
    private config = ConfigurationService.getInstance();

    private constructor() { }

    static getInstance(): FileOperationsService {
        if (!FileOperationsService.instance) {
            FileOperationsService.instance = new FileOperationsService();
        }
        return FileOperationsService.instance;
    }

    /**
     * Ensures a directory exists, creating it if necessary
     */
    ensureDirectoryExists(directoryPath: string): FileOperationResult {
        try {
            const fullPath = path.resolve(directoryPath);
            if (!fs.existsSync(fullPath)) {
                fs.mkdirSync(fullPath, { recursive: true });
            }
            return {
                success: true,
                message: `Directory ensured: ${fullPath}`,
                filePath: fullPath,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to ensure directory: ${error}`,
            };
        }
    }

    /**
     * Writes content to a file with error handling
     */
    writeFile(filePath: string, content: string): FileOperationResult {
        try {
            const fullPath = path.resolve(filePath);
            const directory = path.dirname(fullPath);

            // Ensure directory exists
            const dirResult = this.ensureDirectoryExists(directory);
            if (!dirResult.success) {
                return dirResult;
            }

            fs.writeFileSync(fullPath, content, 'utf8');
            return {
                success: true,
                message: `File written successfully: ${fullPath}`,
                filePath: fullPath,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to write file: ${error}`,
            };
        }
    }

    /**
     * Reads a file with error handling
     */
    readFile(filePath: string): FileOperationResult & { content?: string } {
        try {
            const fullPath = path.resolve(filePath);

            if (!fs.existsSync(fullPath)) {
                return {
                    success: false,
                    message: `File does not exist: ${fullPath}`,
                };
            }

            const content = fs.readFileSync(fullPath, 'utf8');
            return {
                success: true,
                message: `File read successfully: ${fullPath}`,
                filePath: fullPath,
                content,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to read file: ${error}`,
            };
        }
    }

    /**
     * Deletes a file with error handling
     */
    deleteFile(filePath: string): FileOperationResult {
        try {
            const fullPath = path.resolve(filePath);

            if (!fs.existsSync(fullPath)) {
                return {
                    success: true,
                    message: `File does not exist (already deleted): ${fullPath}`,
                };
            }

            fs.unlinkSync(fullPath);
            return {
                success: true,
                message: `File deleted successfully: ${fullPath}`,
                filePath: fullPath,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to delete file: ${error}`,
            };
        }
    }

    /**
     * Cleans up old report files based on age
     */
    cleanupOldReports(maxAgeInDays: number = 7): FileOperationResult {
        try {
            const reportsDir = path.resolve(this.config.getReportingConfiguration().reportsDirectory);

            if (!fs.existsSync(reportsDir)) {
                return {
                    success: true,
                    message: 'Reports directory does not exist, no cleanup needed',
                };
            }

            const files = fs.readdirSync(reportsDir);
            const cutoffDate = new Date(Date.now() - maxAgeInDays * 24 * 60 * 60 * 1000);
            let deletedCount = 0;

            for (const file of files) {
                const filePath = path.join(reportsDir, file);
                const stats = fs.statSync(filePath);

                if (stats.mtime < cutoffDate) {
                    if (stats.isDirectory()) {
                        fs.rmSync(filePath, { recursive: true, force: true });
                    } else {
                        fs.unlinkSync(filePath);
                    }
                    deletedCount++;
                }
            }

            return {
                success: true,
                message: `Cleanup completed: ${deletedCount} old files/directories removed`,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to cleanup old reports: ${error}`,
            };
        }
    }

    /**
     * Generates a unique filename with timestamp
     */
    generateUniqueFilename(baseName: string, extension: string): string {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        return `${baseName}-${timestamp}.${extension}`;
    }

    /**
     * Generates a user-friendly filename from a URL
     */
    generateUserFriendlyFilename(url: string, suffix: string = ''): string {
        try {
            const parsedUrl = new URL(url);
            let domain = parsedUrl.hostname.replace(/^www\./, '');

            // Replace dots with dashes for readability
            domain = domain.replace(/\./g, '-');

            // Add timestamp
            const now = new Date();
            const timestamp = now.toLocaleDateString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            }).replace(/[\/\s:]/g, '-');

            return `${domain}-accessibility-report-${timestamp}${suffix}`;
        } catch (error) {
            // Fallback to timestamp-based naming
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            return `accessibility-report-${timestamp}${suffix}`;
        }
    }

    /**
     * Gets the reports directory path
     */
    getReportsDirectory(): string {
        return path.resolve(this.config.getReportingConfiguration().reportsDirectory);
    }

    /**
     * Lists files in the reports directory
     */
    listReportFiles(): FileOperationResult & { files?: string[] } {
        try {
            const reportsDir = this.getReportsDirectory();

            if (!fs.existsSync(reportsDir)) {
                return {
                    success: true,
                    message: 'Reports directory does not exist',
                    files: [],
                };
            }

            const files = fs.readdirSync(reportsDir);
            return {
                success: true,
                message: `Found ${files.length} files in reports directory`,
                files,
            };
        } catch (error) {
            return {
                success: false,
                message: `Failed to list report files: ${error}`,
            };
        }
    }
} 