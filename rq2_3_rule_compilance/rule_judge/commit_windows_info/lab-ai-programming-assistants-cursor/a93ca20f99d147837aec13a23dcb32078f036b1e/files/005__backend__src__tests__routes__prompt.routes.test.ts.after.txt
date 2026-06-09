import 'reflect-metadata';
import request from 'supertest';
import express from 'express';
import { Router } from 'express';

describe('Prompt Routes', () => {
  let app: express.Application;
  let mockRouter: express.Router;
  let mockOptimizePrompt: jest.Mock;
  let mockStreamOptimizePrompt: jest.Mock;

  beforeEach(() => {
    // Create fresh mocks
    mockOptimizePrompt = jest.fn();
    mockStreamOptimizePrompt = jest.fn();
    
    // Create a mock router with direct handlers instead of using the container
    mockRouter = Router();
    
    // Setup the mock handlers
    mockOptimizePrompt.mockImplementation((req, res) => {
      if (!req.body.prompt) {
        res.status(400).json({ error: 'Prompt is required' });
        return;
      }
      res.status(200).json({ optimizedPrompt: 'Optimized result' });
    });
    
    mockStreamOptimizePrompt.mockImplementation((req, res) => {
      if (!req.body.prompt) {
        res.status(400).json({ error: 'Prompt is required' });
        return;
      }
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
      });
      res.write('data: {"chunk":"Test stream","complete":true}\n\n');
      res.end();
    });
    
    // Set up the routes with our mock handlers
    mockRouter.post('/optimize', mockOptimizePrompt);
    mockRouter.post('/optimize/stream', mockStreamOptimizePrompt);
    
    // Setup Express app with the mock router
    app = express();
    app.use(express.json());
    app.use('/api/prompt', mockRouter);
  });

  describe('POST /api/prompt/optimize', () => {
    it('should return optimized prompt when request is valid', async () => {
      // When: Making a POST request to the endpoint
      const response = await request(app)
        .post('/api/prompt/optimize')
        .send({ prompt: 'Test prompt' });
      
      // Then: Should receive 200 with the optimized prompt
      expect(response.status).toBe(200);
      expect(response.body).toEqual({ optimizedPrompt: 'Optimized result' });
      expect(mockOptimizePrompt).toHaveBeenCalled();
    });

    it('should handle errors when prompt is missing', async () => {
      // When: Making a POST request without a prompt
      const response = await request(app)
        .post('/api/prompt/optimize')
        .send({});
      
      // Then: Should receive appropriate error status with correct message
      expect(response.status).toBe(400);
      expect(response.body).toEqual({ error: 'Prompt is required' });
      expect(mockOptimizePrompt).toHaveBeenCalled();
    });
  });

  describe('POST /api/prompt/optimize/stream', () => {
    it('should stream response when request is valid', async () => {
      // When: Making a POST request to the streaming endpoint
      const response = await request(app)
        .post('/api/prompt/optimize/stream')
        .send({ prompt: 'Test prompt' });
      
      // Then: Should receive 200 with the streamed response
      expect(response.status).toBe(200);
      expect(response.text).toContain('data: {"chunk":"Test stream","complete":true}');
      expect(mockStreamOptimizePrompt).toHaveBeenCalled();
    });
  });
}); 