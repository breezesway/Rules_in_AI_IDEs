import { Router } from 'express';
import * as projectController from '../controllers/project-controller';
import { validate } from '../middleware/validation';
import {
  validateCreateProject,
  validateUpdateProject,
  validateProjectId,
} from '../validators/project-validators';

const router = Router();

/**
 * @route   GET /api/projects
 * @desc    Get all projects with bug counts
 * @access  Public
 */
router.get('/', projectController.getAllProjects);

/**
 * @route   GET /api/projects/:id
 * @desc    Get project by ID
 * @access  Public
 */
router.get('/:id', validate(validateProjectId), projectController.getProjectById);

/**
 * @route   POST /api/projects
 * @desc    Create new project
 * @access  Public
 */
router.post('/', validate(validateCreateProject), projectController.createProject);

/**
 * @route   PUT /api/projects/:id
 * @desc    Update project
 * @access  Public
 */
router.put('/:id', validate(validateUpdateProject), projectController.updateProject);

/**
 * @route   DELETE /api/projects/:id
 * @desc    Delete project
 * @access  Public
 */
router.delete('/:id', validate(validateProjectId), projectController.deleteProject);

export default router;