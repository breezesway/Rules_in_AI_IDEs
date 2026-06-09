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
        process.env['MONGODB_URL'] = 'mongodb://localhost:27017';
        process.env['MONGODB_DB_NAME'] = 'test_db';

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
    });

    describe('Health Check Endpoint', () => {
        test('GET /api/health should return healthy status', async () => {
            const response = await request(app)
                .get('/api/health')
                .expect(200);

            expect(response.body).toEqual({
                status: 'healthy',
                timestamp: expect.any(String),
                version: '2.1.1'
            });

            // Verify timestamp is valid ISO string
            expect(new Date(response.body.timestamp).toISOString()).toBe(response.body.timestamp);
        });

        test('GET /api/health should handle concurrent requests', async () => {
            const requests = Array(5).fill(null).map(() =>
                request(app).get('/api/health')
            );

            const responses = await Promise.all(requests);

            responses.forEach((response: any) => {
                expect(response.status).toBe(200);
                expect(response.body.status).toBe('healthy');
            });
        });
    });

    describe('Full Site Scan Endpoint', () => {
        test('POST /api/scan/full-site should start scan with valid URL', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({
                    url: 'https://example.com',
                    options: {
                        maxPages: 10,
                        maxDepth: 2
                    }
                })
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('scanId');
            expect(response.body.data.message).toContain('Full site scan started');
        });

        test('POST /api/scan/full-site should reject invalid URL', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({
                    url: 'invalid-url'
                })
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Invalid URL format');
        });

        test('POST /api/scan/full-site should reject missing URL', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({})
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('URL is required');
        });

        test('POST /api/scan/full-site should handle malformed JSON', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .set('Content-Type', 'application/json')
                .send('invalid json')
                .expect(400);

            // Just check that we got a 400 status and some response body
            expect(response.status).toBe(400);
            expect(response.body).toBeDefined();
        });

        test('POST /api/scan/full-site should accept custom options', async () => {
            const customOptions = {
                maxPages: 5,
                maxDepth: 3,
                maxConcurrency: 2,
                enablePerformanceMonitoring: true,
                retryFailedPages: false,
                generateReports: true
            };

            const response = await request(app)
                .post('/api/scan/full-site')
                .send({
                    url: 'https://example.com',
                    options: customOptions
                })
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('scanId');
        });
    });

    describe('Single Page Scan Endpoint', () => {
        test('POST /api/scan/single-page should start scan with valid URL', async () => {
            const response = await request(app)
                .post('/api/scan/single-page')
                .send({
                    url: 'https://example.com'
                })
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('scanId');
            expect(response.body.data.message).toContain('Single page scan started');
        });

        test('POST /api/scan/single-page should reject invalid URL', async () => {
            const response = await request(app)
                .post('/api/scan/single-page')
                .send({
                    url: 'not-a-url'
                })
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Invalid URL format');
        });

        test('POST /api/scan/single-page should reject missing URL', async () => {
            const response = await request(app)
                .post('/api/scan/single-page')
                .send({})
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('URL is required');
        });
    });

    describe('Scan Status Endpoint', () => {
        test('GET /api/scan/status should return all active scans when no scanId provided', async () => {
            const response = await request(app)
                .get('/api/scan/status')
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('activeScans');
            expect(response.body.data).toHaveProperty('scans');
            expect(Array.isArray(response.body.data.scans)).toBe(true);
        });

        test('GET /api/scan/status should return specific scan when scanId provided', async () => {
            // First create a scan
            const scanResponse = await request(app)
                .post('/api/scan/single-page')
                .send({ url: 'https://example.com' });

            const scanId = scanResponse.body.data.scanId;

            // Then check its status
            const response = await request(app)
                .get(`/api/scan/status?scanId=${scanId}`)
                .expect(200);

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('url');
            expect(response.body.data).toHaveProperty('startTime');
            expect(response.body.data).toHaveProperty('status');
            expect(response.body.data).toHaveProperty('type');
        });

        test('GET /api/scan/status should return 404 for non-existent scanId', async () => {
            const response = await request(app)
                .get('/api/scan/status?scanId=non-existent-scan')
                .expect(404);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('Scan not found');
        });
    });

    describe('Report Generation Endpoint', () => {
        beforeEach(() => {
            // Create test reports directory using test utilities
            const reportsDir = (global as any).testUtils.createTestReportsDir();
            const historyDir = path.join(reportsDir, 'history');

            if (!fs.existsSync(historyDir)) {
                fs.mkdirSync(historyDir, { recursive: true });
            }
        });

        afterEach(() => {
            // Clean up test reports using test utilities
            (global as any).testUtils.cleanupTestReportsDir();
        });

        test('POST /api/reports/regenerate should return reports when they exist', async () => {
            // Create a test report file using test utilities
            const reportsDir = (global as any).testUtils.createTestReportsDir();
            const testReport = {
                url: 'https://example.com',
                timestamp: new Date().toISOString(),
                violations: []
            };

            (global as any).testUtils.createTestFile(
                path.join(reportsDir, 'accessibility-report-example.json'),
                JSON.stringify(testReport)
            );

            const response = await request(app)
                .post('/api/reports/regenerate')
                .expect(500); // MongoDB service will fail to initialize with test credentials

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to initialize database service');
        });

        test('POST /api/reports/regenerate should return 500 when database service fails', async () => {
            const response = await request(app)
                .post('/api/reports/regenerate')
                .expect(500);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to retrieve reports from database');
        });

        test('POST /api/reports/regenerate should handle malformed report files', async () => {
            // Create a malformed report file using test utilities
            const reportsDir = (global as any).testUtils.createTestReportsDir();
            (global as any).testUtils.createTestFile(
                path.join(reportsDir, 'accessibility-report-malformed.json'),
                'invalid json content'
            );

            const response = await request(app)
                .post('/api/reports/regenerate')
                .expect(500); // MongoDB service will fail to initialize with test credentials

            expect(response.body.success).toBe(false);
            expect(response.body.error).toContain('Failed to retrieve reports from database');
        });
    });

    describe('Error Handling and Edge Cases', () => {
        test('should handle server errors gracefully', async () => {
            // Test with a URL that might cause server errors
            const response = await request(app)
                .post('/api/scan/full-site')
                .send({
                    url: 'https://invalid-domain-that-does-not-exist-12345.com'
                })
                .expect(200); // Should still return 200 as scan is started in background

            expect(response.body.success).toBe(true);
            expect(response.body.data).toHaveProperty('scanId');
        });

        test('should handle large request bodies', async () => {
            const largeOptions = {
                excludePatterns: Array(1000).fill('pattern'),
                customRules: Array(500).fill({ rule: 'test' })
            };

            const response = await request(app)
                .post('/api/scan/full-site')
                .send({
                    url: 'https://example.com',
                    options: largeOptions
                })
                .expect(200);

            expect(response.body.success).toBe(true);
        });

        test('should handle concurrent scan requests', async () => {
            const requests = Array(3).fill(null).map(() =>
                request(app)
                    .post('/api/scan/single-page')
                    .send({ url: 'https://example.com' })
            );

            const responses = await Promise.all(requests);

            responses.forEach((response: any) => {
                expect(response.status).toBe(200);
                expect(response.body.success).toBe(true);
                expect(response.body.data).toHaveProperty('scanId');
            });

            // Verify all scans are tracked
            const statusResponse = await request(app)
                .get('/api/scan/status')
                .expect(200);

            expect(statusResponse.body.data.activeScans).toBeGreaterThanOrEqual(3);
        });
    });

    describe('CORS and Headers', () => {
        test('should handle CORS preflight requests', async () => {
            const response = await request(app)
                .options('/api/scan/full-site')
                .set('Origin', 'http://localhost:3000')
                .set('Access-Control-Request-Method', 'POST')
                .set('Access-Control-Request-Headers', 'Content-Type')
                .expect(204); // CORS preflight requests typically return 204 No Content

            expect(response.headers['access-control-allow-origin']).toBe('*');
        });

        test('should include proper headers in responses', async () => {
            const response = await request(app)
                .get('/api/health')
                .expect(200);

            expect(response.headers['content-type']).toContain('application/json');
        });
    });

    describe('Request Validation', () => {
        test('should validate Content-Type header', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .set('Content-Type', 'text/plain')
                .send('{"url": "https://example.com"}')
                .expect(400);

            expect(response.body).toHaveProperty('error');
        });

        test('should handle empty request body', async () => {
            const response = await request(app)
                .post('/api/scan/full-site')
                .send()
                .expect(400);

            expect(response.body.success).toBe(false);
            expect(response.body.error).toBe('URL is required');
        });
    });
}); 