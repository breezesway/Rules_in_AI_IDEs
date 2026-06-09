import { Router } from 'express';
import * as bugController from '../controllers/bug-controller';
import { validate } from '../middleware/validation';
import {
  validateCreateBug,
  validateUpdateBug,
  validateBugParams,
  validateProjectParam,
  validateBugFilters,
} from '../validators/bug-validators';

const router = Router();

/**
 * @route   GET /api/projects/:projectId/bugs/statistics
 * @desc    Get bug statistics for a project
 * @access  Public
 * @note    This route must come before /:bugId to avoid conflicts
 */
router.get('/:projectId/bugs/statistics', 
  validate(validateProjectParam), 
  bugController.getBugStatistics
);

/**
 * @route   GET /api/projects/:projectId/bugs
 * @desc    Get all bugs for a project with optional filtering and sorting
 * @access  Public
 */
router.get('/:projectId/bugs', 
  validate(validateBugFilters), 
  bugController.getBugsByProject
);

/**
 * @route   GET /api/projects/:projectId/bugs/:bugId
 * @desc    Get bug by ID
 * @access  Public
 */
router.get('/:projectId/bugs/:bugId', 
  validate(validateBugParams), 
  bugController.getBugById
);

/**
 * @route   POST /api/projects/:projectId/bugs
 * @desc    Create new bug
 * @access  Public
 */
router.post('/:projectId/bugs', 
  validate(validateCreateBug), 
  bugController.createBug
);

/**
 * @route   PUT /api/projects/:projectId/bugs/:bugId
 * @desc    Update bug
 * @access  Public
 */
router.put('/:projectId/bugs/:bugId', 
  validate(validateUpdateBug), 
  bugController.updateBug
);

/**
 * @route   DELETE /api/projects/:projectId/bugs/:bugId
 * @desc    Delete bug
 * @access  Public
 */
router.delete('/:projectId/bugs/:bugId', 
  validate(validateBugParams), 
  bugController.deleteBug
);

export default router;