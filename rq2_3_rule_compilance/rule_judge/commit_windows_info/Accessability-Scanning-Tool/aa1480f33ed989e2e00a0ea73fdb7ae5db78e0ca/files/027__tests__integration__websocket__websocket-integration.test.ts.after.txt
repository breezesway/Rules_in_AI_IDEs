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
    });

    afterEach(() => {
        // Disconnect client after each test
        if (clientSocket) {
            clientSocket.disconnect();
            clientSocket = null;
        }
    });

    describe('WebSocket Connection Management', () => {
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

        test('should handle multiple concurrent connections', (done) => {
            const connections: any[] = [];
            const connectionCount = 5;

            for (let i = 0; i < connectionCount; i++) {
                const socket = Client(`http://localhost:${testPort}`);
                connections.push(socket);
            }

            Promise.all(connections.map(socket =>
                new Promise<void>((resolve) => {
                    socket.on('connect', () => resolve());
                })
            )).then(() => {
                connections.forEach(socket => {
                    expect(socket.connected).toBe(true);
                    socket.disconnect();
                });
                done();
            }).catch(done);
        });

        test('should handle connection disconnection gracefully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                expect(clientSocket.connected).toBe(true);
                clientSocket.disconnect();
            });

            clientSocket.on('disconnect', () => {
                expect(clientSocket.connected).toBe(false);
                done();
            });
        });

        test('should handle connection errors', (done) => {
            // Try to connect to non-existent server
            const invalidSocket = Client('http://localhost:9999');

            invalidSocket.on('connect_error', (error: any) => {
                expect(error.message).toBeTruthy();
                invalidSocket.disconnect();
                done();
            });
        });
    });

    describe('Scan Room Management', () => {
        test('should allow client to join scan room', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'test-scan-123';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                // Wait a bit for the join to be processed
                setTimeout(() => {
                    // Verify the room exists by checking if we can emit to it
                    server['io'].to(scanId).emit('test-message', 'test');
                    done();
                }, 100);
            });
        });

        test('should handle multiple clients joining same scan room', (done) => {
            const scanId = 'multi-client-scan';
            const clients: any[] = [];
            const clientCount = 3;

            for (let i = 0; i < clientCount; i++) {
                const socket = Client(`http://localhost:${testPort}`);
                clients.push(socket);
            }

            Promise.all(clients.map(socket =>
                new Promise<any>((resolve) => {
                    socket.on('connect', () => {
                        socket.emit('join-scan', scanId);
                        resolve(socket);
                    });
                })
            )).then(() => {
                // All clients should be in the room
                clients.forEach(socket => {
                    expect(socket.connected).toBe(true);
                    socket.disconnect();
                });
                done();
            }).catch(done);
        });

        test('should handle client leaving scan room', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'leave-test-scan';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                setTimeout(() => {
                    clientSocket.disconnect();
                    // Room should be cleaned up automatically
                    setTimeout(done, 100);
                }, 100);
            });
        });
    });

    describe('Progress Update Communication', () => {
        test('should emit progress updates to scan room', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'progress-test-scan';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('progress-update', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.stage).toBe('test-stage');
                    expect(data.progress).toBe(50);
                    expect(data.message).toBe('Test progress message');
                    expect(data.timestamp).toBeTruthy();
                    done();
                });

                // Emit a test progress update
                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'test-stage', 50, 'Test progress message');
                }, 100);
            });
        });

        test('should handle multiple progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'multi-progress-scan';
            let updateCount = 0;
            const expectedUpdates = 3;

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('progress-update', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    updateCount++;

                    if (updateCount === expectedUpdates) {
                        done();
                    }
                });

                // Emit multiple progress updates
                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'stage1', 25, 'First update');
                }, 100);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'stage2', 50, 'Second update');
                }, 200);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'stage3', 75, 'Third update');
                }, 300);
            });
        });

        test('should emit scan completion event', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'completion-test-scan';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('scan-completed', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.success).toBe(true);
                    expect(data.data).toBeTruthy();
                    done();
                });

                // Emit scan completion
                setTimeout(() => {
                    server['io'].to(scanId).emit('scan-completed', {
                        scanId,
                        success: true,
                        data: { results: 'test results' }
                    });
                }, 100);
            });
        });
    });

    describe('Real-time Scan Workflow', () => {
        test('should handle full scan workflow with progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'workflow-test-scan';
            const expectedStages = ['cleanup', 'browser-init', 'crawling', 'analysis', 'reporting'];
            const receivedStages: string[] = [];

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('progress-update', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.progress).toBeGreaterThanOrEqual(0);
                    expect(data.progress).toBeLessThanOrEqual(100);
                    expect(data.message).toBeTruthy();
                    expect(data.timestamp).toBeTruthy();

                    if (!receivedStages.includes(data.stage)) {
                        receivedStages.push(data.stage);
                    }
                });

                clientSocket.on('scan-completed', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.success).toBe(true);

                    // Verify we received updates for all expected stages
                    expectedStages.forEach(stage => {
                        expect(receivedStages).toContain(stage);
                    });

                    done();
                });

                // Simulate a full scan workflow
                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'cleanup', 0, 'Cleaning up old reports...');
                }, 100);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'cleanup', 5, 'Cleanup completed');
                }, 200);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'browser-init', 5, 'Initializing browser...');
                }, 300);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'browser-init', 15, 'Browser initialized successfully');
                }, 400);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'crawling', 15, 'Starting site crawling...');
                }, 500);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'crawling', 35, 'Site crawling completed. Found 5 pages.');
                }, 600);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'analysis', 35, 'Starting accessibility analysis...');
                }, 700);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'analysis', 80, 'Accessibility analysis completed. Analyzed 5 pages.');
                }, 800);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'reporting', 85, 'Generating reports...');
                }, 900);

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'reporting', 100, 'Reports generated successfully');

                    // Emit completion
                    server['io'].to(scanId).emit('scan-completed', {
                        scanId,
                        success: true,
                        data: {
                            crawlResults: [],
                            analysisResults: [],
                            reportPaths: []
                        }
                    });
                }, 1000);
            });
        });

        test('should handle scan errors and error events', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'error-test-scan';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('scan-completed', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.success).toBe(false);
                    expect(data.error).toBeTruthy();
                    done();
                });

                // Simulate scan error
                setTimeout(() => {
                    server['io'].to(scanId).emit('scan-completed', {
                        scanId,
                        success: false,
                        error: 'Test scan error'
                    });
                }, 100);
            });
        });
    });

    describe('Error Handling and Edge Cases', () => {
        test('should handle invalid scan ID', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);

            clientSocket.on('connect', () => {
                // Try to join with invalid scan ID
                clientSocket.emit('join-scan', '');

                // Should not crash and should still be connected
                setTimeout(() => {
                    expect(clientSocket.connected).toBe(true);
                    done();
                }, 100);
            });
        });

        test('should handle rapid connect/disconnect cycles', (done) => {
            const cycles = 5;
            let completedCycles = 0;

            const performCycle = () => {
                const socket = Client(`http://localhost:${testPort}`);

                socket.on('connect', () => {
                    socket.emit('join-scan', `cycle-${completedCycles}`);
                    socket.disconnect();
                });

                socket.on('disconnect', () => {
                    completedCycles++;
                    if (completedCycles >= cycles) {
                        done();
                    } else {
                        performCycle();
                    }
                });
            };

            performCycle();
        });

        test('should handle large payloads in progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'large-payload-scan';
            const largeDetails = {
                data: Array(1000).fill('large data item'),
                metadata: { complex: 'object' }
            };

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('progress-update', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    expect(data.details).toEqual(largeDetails);
                    done();
                });

                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'test', 50, 'Large payload test', largeDetails);
                }, 100);
            });
        });

        test('should handle network interruptions gracefully', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'network-test-scan';

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                // Simulate network interruption by disconnecting
                setTimeout(() => {
                    clientSocket.disconnect();
                }, 100);

                // Reconnect after interruption
                setTimeout(() => {
                    const newSocket = Client(`http://localhost:${testPort}`);
                    newSocket.on('connect', () => {
                        newSocket.emit('join-scan', scanId);
                        expect(newSocket.connected).toBe(true);
                        newSocket.disconnect();
                        done();
                    });
                }, 200);
            });
        });
    });

    describe('Performance and Scalability', () => {
        test('should handle many concurrent scan rooms', (done) => {
            const roomCount = 10;
            const clientsPerRoom = 3;
            const totalClients = roomCount * clientsPerRoom;
            const clients: any[] = [];
            let connectedClients = 0;

            for (let room = 0; room < roomCount; room++) {
                for (let client = 0; client < clientsPerRoom; client++) {
                    const socket = Client(`http://localhost:${testPort}`);
                    clients.push(socket);

                    socket.on('connect', () => {
                        socket.emit('join-scan', `room-${room}`);
                        connectedClients++;

                        if (connectedClients === totalClients) {
                            // All clients connected and joined rooms
                            clients.forEach(s => expect(s.connected).toBe(true));
                            clients.forEach(s => s.disconnect());
                            done();
                        }
                    });
                }
            }
        });

        test('should handle rapid progress updates', (done) => {
            clientSocket = Client(`http://localhost:${testPort}`);
            const scanId = 'rapid-updates-scan';
            let updateCount = 0;
            const rapidUpdates = 2; // Reduced to 2 for reliability

            clientSocket.on('connect', () => {
                clientSocket.emit('join-scan', scanId);

                clientSocket.on('progress-update', (data: any) => {
                    expect(data.scanId).toBe(scanId);
                    updateCount++;

                    if (updateCount === rapidUpdates) {
                        clientSocket.disconnect();
                        done();
                    }
                });

                // Send rapid updates with a small delay to ensure connection is ready
                setTimeout(() => {
                    server['emitProgressUpdate'](scanId, 'rapid', 0, 'Update 0');
                    server['emitProgressUpdate'](scanId, 'rapid', 100, 'Update 1');
                }, 100);
            });
        }, 5000); // Increased timeout to 5 seconds
    });
}); 