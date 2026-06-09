import { Request, Response, NextFunction } from 'express';
import { ValidationResult } from 'express-validator';
import { AppError, ValidationError } from '../utils/errors';
import { sendError } from '../utils/response';

/**
 * Global error handling middleware
 */
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Don't handle if response already sent
  if (res.headersSent) {
    return next(err);
  }

  // Handle different types of errors
  if (err instanceof AppError) {
    sendError(res, err);
    return;
  }

  // Handle PostgreSQL errors
  if (err.name === 'error' && (err as any).code) {
    const pgError = err as any;
    
    switch (pgError.code) {
      case '23505': // Unique violation
        sendError(res, new AppError('Resource already exists', 409, 'CONFLICT'));
        return;
      case '23503': // Foreign key violation
        sendError(res, new AppError('Referenced resource not found', 400, 'FOREIGN_KEY_ERROR'));
        return;
      case '23502': // Not null violation
        sendError(res, new AppError('Required field missing', 400, 'REQUIRED_FIELD_MISSING'));
        return;
      default:
        console.error('PostgreSQL Error:', pgError);
        sendError(res, new AppError('Database error', 500, 'DATABASE_ERROR'));
        return;
    }
  }

  // Handle validation errors from express-validator
  if (err.name === 'ValidationError') {
    sendError(res, err as ValidationError);
    return;
  }

  // Handle unexpected errors
  console.error('Unexpected Error:', {
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    body: req.body,
    params: req.params,
    query: req.query,
  });

  sendError(res, new AppError('Internal server error', 500, 'INTERNAL_ERROR'));
}

/**
 * Handle 404 errors
 */
export function notFoundHandler(req: Request, res: Response): void {
  sendError(res, new AppError(`Route ${req.originalUrl} not found`, 404, 'ROUTE_NOT_FOUND'));
}

/**
 * Async error wrapper
 */
export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction): void => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}