import { Request, Response, NextFunction } from 'express';
import { errorHandler } from '../../middleware/error.middleware';

describe('Error Middleware', () => {
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = jest.fn();

  beforeEach(() => {
    // Given: Setup mock request and response
    mockRequest = {};
    mockResponse = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn(),
      statusCode: 200
    };
    
    // Store original NODE_ENV
    process.env.NODE_ENV = 'development';
  });

  it('should return 500 status code when response status is 200', () => {
    // Given: Error object and response with 200 status
    const testError = new Error('Test error');
    mockResponse.statusCode = 200;
    
    // When: Calling error handler
    errorHandler(testError, mockRequest as Request, mockResponse as Response, nextFunction);
    
    // Then: Should set status to 500 and return error details
    expect(mockResponse.status).toHaveBeenCalledWith(500);
    expect(mockResponse.json).toHaveBeenCalledWith({
      message: 'Test error',
      stack: testError.stack
    });
  });

  it('should preserve status code when not 200', () => {
    // Given: Error object and response with non-200 status
    const testError = new Error('Not found error');
    mockResponse.statusCode = 404;
    
    // When: Calling error handler
    errorHandler(testError, mockRequest as Request, mockResponse as Response, nextFunction);
    
    // Then: Should preserve status code and return error details
    expect(mockResponse.status).toHaveBeenCalledWith(404);
    expect(mockResponse.json).toHaveBeenCalledWith({
      message: 'Not found error',
      stack: testError.stack
    });
  });

  it('should hide stack trace in production environment', () => {
    // Given: Production environment
    process.env.NODE_ENV = 'production';
    const testError = new Error('Production error');
    
    // When: Calling error handler
    errorHandler(testError, mockRequest as Request, mockResponse as Response, nextFunction);
    
    // Then: Should hide the actual stack trace
    expect(mockResponse.json).toHaveBeenCalled();
    const callArgs = mockResponse.json.mock.calls[0][0];
    expect(callArgs.message).toBe('Production error');
    expect(callArgs.stack).not.toBe(testError.stack);
    // Verify it's a non-empty string but not the actual stack trace
    expect(typeof callArgs.stack).toBe('string');
    expect(callArgs.stack.length).toBeLessThan(10);
  });
}); 