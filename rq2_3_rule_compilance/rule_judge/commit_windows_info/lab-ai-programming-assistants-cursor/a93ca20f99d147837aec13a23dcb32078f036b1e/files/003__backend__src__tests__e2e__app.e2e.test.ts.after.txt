import 'reflect-metadata';
import request from 'supertest';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import promptRoutes from '../../routes/prompt.routes';
import errorHandler from '../../middleware/error.middleware';
import '../../container';

// Mock OpenAI client
jest.mock('openai', () => {
  const mockOpenAI = {
    chat: {
      completions: {
        create: jest.fn()
      }
    }
  };
  
  return jest.fn(() => mockOpenAI);
});

describe('Express App E2E Tests', () => {
  let app: express.Application;
  // Create a separate server that we can close in afterAll
  let server: any;
  
  beforeAll(() => {
    // Given: Setup Express app similar to index.ts
    dotenv.config();
    app = express();
    
    // Middleware
    app.use(helmet());
    app.use(cors());
    app.use(express.json());
    
    // Routes
    app.use('/api/prompt', promptRoutes);
    app.get('/health', (req, res) => {
      res.status(200).json({ status: 'ok' });
    });
    
    // Error handling
    app.use(errorHandler);
    
    // Start a server we can close later
    server = app.listen(0); // Use port 0 to get a random available port
  });
  
  afterAll((done) => {
    // Clean up by closing the server
    if (server) {
      server.close(done);
    } else {
      done();
    }
  });
  
  describe('Health Check Endpoint', () => {
    it('should return 200 OK with status', async () => {
      // When: Making a GET request to the health endpoint
      const response = await request(app).get('/health');
      
      // Then: Should receive 200 with status OK
      expect(response.status).toBe(200);
      expect(response.body).toEqual({ status: 'ok' });
    });
  });
  
  describe('Non-existent Route', () => {
    it('should return 404 for non-existent routes', async () => {
      // When: Making a GET request to a non-existent route
      const response = await request(app).get('/non-existent-route');
      
      // Then: Should receive 404
      expect(response.status).toBe(404);
    });
  });
}); 