import { Request, Response, NextFunction } from 'express';
import { validationResult, ValidationChain } from 'express-validator';
import { ValidationError } from '../utils/errors';

/**
 * Middleware to handle validation results
 */
export function handleValidationErrors(
  req: Request,
  _res: Response,
  next: NextFunction
): void {
  const errors = validationResult(req);
  
  if (!errors.isEmpty()) {
    const validationErrors = errors.array().map(error => ({
      field: error.type === 'field' ? (error as any).path : 'unknown',
      message: error.msg,
      value: error.type === 'field' ? (error as any).value : undefined,
    }));

    const errorMessage = validationErrors
      .map(err => `${err.field}: ${err.message}`)
      .join(', ');

    throw new ValidationError(errorMessage, validationErrors);
  }
  
  next();
}

/**
 * Create validation middleware chain
 */
export function validate(validations: ValidationChain[]) {
  return [...validations, handleValidationErrors];
}