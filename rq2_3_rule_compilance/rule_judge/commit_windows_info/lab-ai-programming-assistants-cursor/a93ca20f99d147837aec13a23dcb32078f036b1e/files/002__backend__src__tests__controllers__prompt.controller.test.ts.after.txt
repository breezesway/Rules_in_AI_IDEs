import 'reflect-metadata';
import { mock, mockDeep, MockProxy } from 'jest-mock-extended';
import { Request, Response } from 'express';
import { PromptController } from '../../controllers/prompt.controller';
import type { IDeepSeekService } from '../../services/deepseek.service';

describe('PromptController', () => {
  let mockDeepSeekService: MockProxy<IDeepSeekService>;
  let promptController: PromptController;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;

  beforeEach(() => {
    // Given: Mock dependencies
    mockDeepSeekService = mockDeep<IDeepSeekService>();
    promptController = new PromptController(mockDeepSeekService);
    
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn(),
      headersSent: false
    };
  });

  describe('optimizePrompt', () => {
    it('should return 200 with optimized prompt when request is valid', async () => {
      // Given: Valid request body and successful service response
      mockRequest = {
        body: { prompt: 'Test prompt', systemPrompt: 'Test system' }
      };
      mockDeepSeekService.optimizePrompt.mockResolvedValue('Optimized result');
      
      // When: Calling the controller method
      await promptController.optimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should return 200 with the optimized prompt
      expect(mockResponse.status).toHaveBeenCalledWith(200);
      expect(mockResponse.json).toHaveBeenCalledWith({ optimizedPrompt: 'Optimized result' });
      expect(mockDeepSeekService.optimizePrompt).toHaveBeenCalledWith({
        prompt: 'Test prompt',
        systemPrompt: 'Test system'
      });
    });

    it('should return 400 when prompt is missing', async () => {
      // Given: Request with missing prompt
      mockRequest = {
        body: { systemPrompt: 'Test system' }
      };
      
      // When: Calling the controller method
      await promptController.optimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should return 400 with error message
      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith({ error: 'Prompt is required' });
      expect(mockDeepSeekService.optimizePrompt).not.toHaveBeenCalled();
    });

    it('should handle service errors properly', async () => {
      // Given: Valid request but service throws error
      mockRequest = {
        body: { prompt: 'Test prompt' }
      };
      const testError = new Error('Service error');
      testError.status = 503;
      mockDeepSeekService.optimizePrompt.mockRejectedValue(testError);
      
      // When: Calling the controller method
      await promptController.optimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should return error status with message
      expect(mockResponse.status).toHaveBeenCalledWith(503);
      expect(mockResponse.json).toHaveBeenCalledWith({
        error: 'Service error',
        optimizedPrompt: null
      });
    });
  });

  describe('streamOptimizePrompt', () => {
    it('should call service stream method when request is valid', async () => {
      // Given: Valid request body
      mockRequest = {
        body: { prompt: 'Test prompt' }
      };
      mockDeepSeekService.optimizePromptStream.mockResolvedValue();
      
      // When: Calling the controller stream method
      await promptController.streamOptimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should call service with request and response
      expect(mockDeepSeekService.optimizePromptStream).toHaveBeenCalledWith(
        { prompt: 'Test prompt' },
        mockResponse
      );
    });

    it('should return 400 when prompt is missing for stream', async () => {
      // Given: Request with missing prompt
      mockRequest = {
        body: { systemPrompt: 'Test system' }
      };
      
      // When: Calling the controller stream method
      await promptController.streamOptimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should return 400 with error message
      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith({ error: 'Prompt is required' });
      expect(mockDeepSeekService.optimizePromptStream).not.toHaveBeenCalled();
    });

    it('should handle service stream errors when headers not sent', async () => {
      // Given: Valid request but service throws error, headers not sent
      mockRequest = {
        body: { prompt: 'Test prompt' }
      };
      const testError = new Error('Stream service error');
      testError.status = 503;
      mockDeepSeekService.optimizePromptStream.mockRejectedValue(testError);
      
      // When: Calling the controller stream method
      await promptController.streamOptimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should return error status with message
      expect(mockResponse.status).toHaveBeenCalledWith(503);
      expect(mockResponse.json).toHaveBeenCalledWith({
        error: 'Stream service error',
        optimizedPrompt: null
      });
    });

    it('should not attempt to send headers if already sent during error', async () => {
      // Given: Valid request but service throws error, headers already sent
      mockRequest = {
        body: { prompt: 'Test prompt' }
      };
      mockResponse.headersSent = true;
      const testError = new Error('Stream service error');
      mockDeepSeekService.optimizePromptStream.mockRejectedValue(testError);
      
      // When: Calling the controller stream method
      await promptController.streamOptimizePrompt(mockRequest as Request, mockResponse as Response);
      
      // Then: Should not attempt to send response since headers already sent
      expect(mockResponse.status).not.toHaveBeenCalled();
      expect(mockResponse.json).not.toHaveBeenCalled();
    });
  });
}); 