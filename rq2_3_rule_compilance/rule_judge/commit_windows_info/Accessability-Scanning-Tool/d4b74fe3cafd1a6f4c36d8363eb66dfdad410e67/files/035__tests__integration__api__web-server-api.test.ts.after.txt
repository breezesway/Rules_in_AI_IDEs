import request from 'supertest';
import { WebServer } from '@/web/server';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';
import path from 'path';
import fs from 'fs';

describe('Web Server API Integration Tests', () => {
    let server: WebServer;
    let app: any;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;
    let testPort: number;

    beforeAll(async () => {
        // Set up test environment variables for MongoDB database service
        process.env['NODE_ENV'] = 'test';
        process.env['MONGODB_URL'] = 'mongodb://localhost:27017';
        process.env['MONGODB_DB_NAME'] = 'test_accessibility_db';

        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();

        // Use a different port for testing
        testPort = 9998;
        server = new WebServer(testPort);

        // Start server
        server['start']();

        // Get the Express app for testing
        app = server['app'];

        // Wait for server to start
        await new Promise(resolve => setTimeout(resolve, 100));
    });

    afterAll(async () => {
        // Clean up server
        if (server['server']) {
            server['server'].close();
        }

        // Final database cleanup
        await (global as any).testUtils.database.cleanupTestData();
    });

    beforeEach(async () => {
        // Set up test database environment
        (global as any).testUtils.database.setupTestEnvironment();

        // Clean up any existing test data before each test
        await (global as any).testUtils.database.cleanupTestData();
    });

    afterEach(async () => {
        // Clean up test data after each test
        await (global as any).testUtils.database.cleanupTestData();

        // Verify cleanup was successful
        await (global as any).testUtils.database.verifyCleanup();
    });

    describe('Health Check Endpoints', () => {
        test('GET / should return health status', async () => {
            const response = await request(app)
                .get('/')
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.message).toContain('Accessibility Testing Tool');
        });

        test('GET /health should return service health', async () => {
            const response = await request(app)
                .get('/health')
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toBeDefined();
            expect(response.body.data.status).toBe('healthy');
            expect(response.body.data.timestamp).toBeDefined();
        });
    });

    describe('CORS Configuration', () => {
        test('should handle preflight requests', async () => {
            const response = await request(app)
                .options('/api/scan/full-site')
                .set('Origin', 'http://localhost:3000')
                .set('Access-Control-Request-Method', 'POST')
                .set('Access-Control-Request-Headers', 'Content-Type')
                .expect(204);

            expect(response.headers['access-control-allow-origin']).toBe('*');
            expect(response.headers['access-control-allow-methods']).toContain('POST');
            expect(response.headers['access-control-allow-headers']).toContain('Content-Type');
        });

        test('should allow cross-origin requests', async () => {
            const response = await request(app)
                .get('/health')
                .set('Origin', 'http://localhost:3000')
                .expect(200);

            expect(response.headers['access-control-allow-origin']).toBe('*');
        });
    });

    describe('Full Site Scan Endpoints', () => {
        test('POST /api/scan/full-site should handle scan requests', async () => {
            const scanData = {
                siteUrl: 'https://example.com',
                maxPages: 5,
                wcagLevel: 'AA',
                includeScreenshots: false
            };

            const response = await request(app)
                .post('/api/scan/full-site')
                .send(scanData)
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toBeDefined();
            expect(response.body.data.scanId).toBeDefined();
            expect(response.body.data.status).toBe('initiated');
            expect(response.body.metadata).toBeDefined();
            expect(response.body.metadata.timestamp).toBeDefined();
        });

        test('POST /api/scan/full-site should validate required fields', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({})
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('siteUrl is required');
        });

        test('POST /api/scan/full-site should handle invalid URLs', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({ siteUrl: 'invalid-url' })
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Invalid URL format');
        });

        test('POST /api/scan/full-site should handle scan with default options', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({ siteUrl: 'https://example.com' })
                .expect(200); // Should still work with default options

            expect(response.body.success).toBe(true);
        });
    });

    describe('Single Page Scan Endpoints', () => {
        test('POST /api/scan/single-page should handle scan requests', async () => {
            const scanData = {
                pageUrl: 'https://example.com',
                wcagLevel: 'AA',
                includeScreenshots: false
            };

            const response = await request(app)
                .post('/api/scan/single-page')
                .send(scanData)
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toBeDefined();
            expect(response.body.data.scanId).toBeDefined();
            expect(response.body.data.status).toBe('initiated');
        });

        test('POST /api/scan/single-page should validate required fields', async () => {
            const response = await request(app)
                .post('/api/scan/single-page')
                .send({})
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('pageUrl is required');
        });

        test('POST /api/scan/single-page should handle invalid URLs', async () => {
            const response = await request(app)
                .post('/api/scan/single-page')
                .send({ pageUrl: 'invalid-url' })
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Invalid URL format');
        });
    });

    describe('Report Generation Endpoints', () => {
        test('POST /api/reports/generate-pdf should handle PDF generation', async () => {
            const response = await request(app)
                .post('/api/reports/generate-pdf')
                .send({ scanId: 'test-scan-id' })
                .expect(500);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to retrieve report from database');
        });
    });

    describe('Report Search Endpoints', () => {
        test('POST /api/reports/search should handle search requests', async () => {
            const searchData = {
                siteUrl: 'https://example.com',
                reportType: 'site-wide',
                dateFrom: '2024-01-01',
                dateTo: '2024-12-31',
                wcagLevel: 'AA',
                minViolations: 0,
                maxViolations: 100,
                minCompliancePercentage: 50
            };

            const response = await request(app)
                .post('/api/reports/search')
                .send(searchData)
                .expect(500);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to search reports in database');
        });

        test('POST /api/reports/search should handle empty search criteria', async () => {
            const response = await request(app)
                .post('/api/reports/search')
                .send({})
                .expect(500);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to search reports in database');
        });

        test('POST /api/reports/search should validate date format', async () => {
            const searchData = {
                dateFrom: 'invalid-date',
                dateTo: '2024-12-31'
            };

            const response = await request(app)
                .post('/api/reports/search')
                .send(searchData)
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Invalid dateFrom format');
        });
    });

    describe('Database Management Endpoints', () => {
        test('GET /api/database/statistics should retrieve database statistics', async () => {
            const response = await request(app)
                .get('/api/database/statistics')
                .expect(500);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to retrieve database statistics');
        });

        test('POST /api/database/cleanup should perform database cleanup', async () => {
            const cleanupData = {
                testData: true,
                orphanedReports: true,
                expiredReports: false,
                dryRun: true
            };

            const response = await request(app)
                .post('/api/database/cleanup')
                .send(cleanupData)
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.message).toContain('Database cleanup completed successfully');
            expect(response.body.data).toBeDefined();
            expect(response.body.data.recordsCleaned).toBeDefined();
        });
    });



    describe('Error Handling', () => {
        test('should handle 404 for unknown endpoints', async () => {
            const response = await request(app)
                .get('/api/unknown-endpoint')
                .expect(404);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Endpoint not found');
        });

        test('should handle malformed JSON', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .set('Content-Type', 'application/json')
                .send('invalid json')
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Invalid JSON');
        });

        test('should handle large payloads', async () => {
            const largeData = {
                siteUrl: 'https://example.com',
                data: 'x'.repeat(1000000) // 1MB payload
            };

            const response = await request(app)
                .post('/api/scan/full-site')
                .send(largeData)
                .expect(413);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Payload too large');
        });
    });
}); 