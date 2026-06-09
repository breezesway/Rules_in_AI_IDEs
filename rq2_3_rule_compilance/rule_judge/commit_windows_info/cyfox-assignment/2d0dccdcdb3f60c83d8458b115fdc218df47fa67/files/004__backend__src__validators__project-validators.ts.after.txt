import { body, param } from 'express-validator';

/**
 * Validation rules for creating a project
 */
export const validateCreateProject = [
  body('name')
    .trim()
    .isLength({ min: 1, max: 255 })
    .withMessage('Project name must be between 1 and 255 characters')
    .matches(/^[a-zA-Z0-9\s\-_.,!?()]+$/)
    .withMessage('Project name contains invalid characters'),
];

/**
 * Validation rules for updating a project
 */
export const validateUpdateProject = [
  param('id')
    .isInt({ min: 1 })
    .withMessage('Project ID must be a positive integer'),
  body('name')
    .optional()
    .trim()
    .isLength({ min: 1, max: 255 })
    .withMessage('Project name must be between 1 and 255 characters')
    .matches(/^[a-zA-Z0-9\s\-_.,!?()]+$/)
    .withMessage('Project name contains invalid characters'),
];

/**
 * Validation rules for project ID parameter
 */
export const validateProjectId = [
  param('id')
    .isInt({ min: 1 })
    .withMessage('Project ID must be a positive integer'),
];