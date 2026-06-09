import { WebServer } from '@/web/server';
import { io as Client } from 'socket.io-client';
import { ErrorHandlerService } from '@/utils/services/error-handler-service';
import { ConfigurationService } from '@/utils/services/configuration-service';

describe('WebSocket Integration Tests', () => {
    let server: WebServer;
    let errorHandler: ErrorHandlerService;
    let configService: ConfigurationService;
    let testPort: number;
    let clientSocket: any;

    beforeAll(async () => {
        // Set up test environment variables for MongoDB database service
        process.env['NODE_ENV'] = 'test';
        process.env['MONGODB_URL'] = 'mongodb://localhost:27017';
        process.env['MONGODB_DB_NAME'] = 'test_accessibility_db';

        errorHandler = ErrorHandlerService.getInstance();
        configService = ConfigurationService.getInstance();

        // Use a different port for testing
        testPort = 3002;
        server = new WebServer(testPort);

        // Start server
        server['start']();

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
        // Disconnect client after each test
        if (clientSocket) {
            clientSocket.disconnect();
            clientSocket = null;
        }

        // Clean up test data after each test
        await (global as any).testUtils.database.cleanupTestData();

        // Verify cleanup was successful
        await (global as any).testUtils.database.verifyCleanup();
    });

    describe('WebSocket Connection', () => {
        test('should establish WebSocket connection successfully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                expect(clientSocket.connected).toBe(true);
                done();
            });

            clientSocket.on('connect_error', (error: any) => {
                done.fail(`Connection failed: ${error.message}`);
            });
        });

        test('should handle connection errors gracefully', (done) => {
            // Try to connect to non-existent server
            const invalidSocket = Client('http://localhost:9999');

            invalidSocket.on('connect_error', (error: any) => {
                expect(error.message).toBeDefined();
                invalidSocket.disconnect();
                done();
            });

            // Timeout after 5 seconds
            setTimeout(() => {
                invalidSocket.disconnect();
                done.fail('Connection error timeout');
            }, 5000);
        });
    });

    describe('Real-time Communication', () => {
        test('should emit scan progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Emit a test progress update
                clientSocket.emit('scan-progress', {
                    scanId: 'test-scan-123',
                    progress: 50,
                    message: 'Processing page 5 of 10'
                });
            });

            clientSocket.on('progress-update', (data: any) => {
                expect(data.scanId).toBe('test-scan-123');
                expect(data.progress).toBe(50);
                expect(data.message).toBe('Processing page 5 of 10');
                done();
            });
        });

        test('should handle multiple concurrent connections', (done) => {
            const connections: any[] = [];
            const connectionCount = 3;
            let connectedCount = 0;

            for (let i = 0; i < connectionCount; i++) {
                const socket = Client(`http://localhost:${testPort}`);
                connections.push(socket);

                socket.on('connect', () => {
                    connectedCount++;
                    if (connectedCount === connectionCount) {
                        // All connections established
                        connections.forEach(conn => conn.disconnect());
                        done();
                    }
                });
            }

            // Timeout after 10 seconds
            setTimeout(() => {
                connections.forEach(conn => conn.disconnect());
                done.fail('Multiple connections timeout');
            }, 10000);
        });

        test('should handle rapid progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const updates: any[] = [];

            clientSocket.on('connect', () => {
                // Send rapid progress updates
                for (let i = 0; i < 10; i++) {
                    setTimeout(() => {
                        clientSocket.emit('scan-progress', {
                            scanId: 'rapid-test',
                            progress: i * 10,
                            message: `Update ${i + 1}`
                        });
                    }, i * 50);
                }
            });

            clientSocket.on('progress-update', (data: any) => {
                updates.push(data);
                if (updates.length === 10) {
                    expect(updates.length).toBe(10);
                    expect(updates[9].progress).toBe(90);
                    done();
                }
            });

            // Timeout after 10 seconds
            setTimeout(() => {
                done.fail('Rapid updates timeout');
            }, 10000);
        });
    });

    describe('Error Handling', () => {
        test('should handle malformed messages gracefully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Send malformed message
                clientSocket.emit('scan-progress', 'invalid-data');
            });

            clientSocket.on('error', (error: any) => {
                expect(error).toBeDefined();
                done();
            });

            // Timeout after 5 seconds
            setTimeout(() => {
                done.fail('Error handling timeout');
            }, 5000);
        });

        test('should handle disconnection gracefully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                clientSocket.disconnect();
            });

            clientSocket.on('disconnect', () => {
                expect(clientSocket.connected).toBe(false);
                done();
            });
        });

        test('should handle server shutdown gracefully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Simulate server shutdown by closing the server
                if (server['server']) {
                    server['server'].close();
                }
            });

            clientSocket.on('disconnect', () => {
                expect(clientSocket.connected).toBe(false);
                done();
            });

            // Timeout after 5 seconds
            setTimeout(() => {
                done.fail('Server shutdown timeout');
            }, 5000);
        });
    });

    describe('Performance Testing', () => {
        test('should handle high-frequency message sending', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const messageCount = 100;
            let receivedCount = 0;

            clientSocket.on('connect', () => {
                // Send high-frequency messages
                for (let i = 0; i < messageCount; i++) {
                    clientSocket.emit('scan-progress', {
                        scanId: 'performance-test',
                        progress: i,
                        message: `Message ${i}`
                    });
                }
            });

            clientSocket.on('progress-update', (data: any) => {
                receivedCount++;
                if (receivedCount === messageCount) {
                    expect(receivedCount).toBe(messageCount);
                    done();
                }
            });

            // Timeout after 15 seconds
            setTimeout(() => {
                done.fail('Performance test timeout');
            }, 15000);
        });

        test('should maintain connection under load', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            let isConnected = true;

            clientSocket.on('connect', () => {
                // Send messages continuously for 5 seconds
                const interval = setInterval(() => {
                    if (!isConnected) {
                        clearInterval(interval);
                        return;
                    }

                    clientSocket.emit('scan-progress', {
                        scanId: 'load-test',
                        progress: Math.random() * 100,
                        message: 'Load test message'
                    });
                }, 100);

                // Stop after 5 seconds
                setTimeout(() => {
                    clearInterval(interval);
                    expect(clientSocket.connected).toBe(true);
                    done();
                }, 5000);
            });

            clientSocket.on('disconnect', () => {
                isConnected = false;
            });
        });
    });

    describe('Message Validation', () => {
        test('should validate message structure', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Send message with missing required fields
                clientSocket.emit('scan-progress', {
                    scanId: 'test-scan'
                    // Missing progress and message
                });
            });

            clientSocket.on('error', (error: any) => {
                expect(error).toBeDefined();
                done();
            });

            // Timeout after 5 seconds
            setTimeout(() => {
                done.fail('Message validation timeout');
            }, 5000);
        });

        test('should handle large message payloads', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Send large payload
                const largePayload = {
                    scanId: 'large-payload-test',
                    progress: 50,
                    message: 'x'.repeat(10000), // 10KB message
                    data: Array(1000).fill('test-data') // Additional large data
                };

                clientSocket.emit('scan-progress', largePayload);
            });

            clientSocket.on('progress-update', (data: any) => {
                expect(data.scanId).toBe('large-payload-test');
                expect(data.message.length).toBe(10000);
                done();
            });

            // Timeout after 10 seconds
            setTimeout(() => {
                done.fail('Large payload timeout');
            }, 10000);
        });
    });

    describe('Connection Management', () => {
        test('should handle reconnection attempts', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`, {
                reconnection: true,
                reconnectionAttempts: 3,
                reconnectionDelay: 1000
            });

            let disconnectCount = 0;
            let reconnectCount = 0;

            clientSocket.on('connect', () => {
                if (disconnectCount === 0) {
                    // First connection - disconnect to trigger reconnection
                    clientSocket.disconnect();
                    disconnectCount++;
                } else {
                    // Reconnection successful
                    reconnectCount++;
                    expect(reconnectCount).toBeGreaterThan(0);
                    done();
                }
            });

            clientSocket.on('disconnect', () => {
                disconnectCount++;
            });

            // Timeout after 15 seconds
            setTimeout(() => {
                done.fail('Reconnection timeout');
            }, 15000);
        });

        test('should handle connection timeout', (done) => {
            // Try to connect to non-existent server with timeout
            const timeoutSocket = Client('http://localhost:9999', {
                timeout: 2000
            });

            timeoutSocket.on('connect_error', (error: any) => {
                expect(error.message).toBeDefined();
                timeoutSocket.disconnect();
                done();
            });

            // Timeout after 10 seconds
            setTimeout(() => {
                timeoutSocket.disconnect();
                done.fail('Connection timeout test failed');
            }, 10000);
        });
    });
}); 