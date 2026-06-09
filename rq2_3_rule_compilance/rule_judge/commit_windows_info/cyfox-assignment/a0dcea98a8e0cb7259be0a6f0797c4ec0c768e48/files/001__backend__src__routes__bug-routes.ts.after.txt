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
 * @swagger
 * /projects/{projectId}/bugs/statistics:
 *   get:
 *     summary: Get bug statistics for a project
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *     responses:
 *       200:
 *         description: Bug statistics
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   type: object
 *                   properties:
 *                     totalBugs:
 *                       type: integer
 *                       example: 10
 *                     byStatus:
 *                       type: object
 *                       properties:
 *                         open:
 *                           type: integer
 *                           example: 3
 *                         in_progress:
 *                           type: integer
 *                           example: 2
 *                         resolved:
 *                           type: integer
 *                           example: 3
 *                         closed:
 *                           type: integer
 *                           example: 2
 *                     bySeverity:
 *                       type: object
 *                       properties:
 *                         low:
 *                           type: integer
 *                           example: 2
 *                         medium:
 *                           type: integer
 *                           example: 3
 *                         high:
 *                           type: integer
 *                           example: 3
 *                         critical:
 *                           type: integer
 *                           example: 2
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.get('/:projectId/bugs/statistics', 
  validate(validateProjectParam), 
  bugController.getBugStatistics
);

/**
 * @swagger
 * /projects/{projectId}/bugs:
 *   get:
 *     summary: Get all bugs for a project with optional filtering and sorting
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [open, in_progress, resolved, closed]
 *         description: Filter bugs by status
 *       - in: query
 *         name: severity
 *         schema:
 *           type: string
 *           enum: [low, medium, high, critical]
 *         description: Filter bugs by severity
 *       - in: query
 *         name: sort
 *         schema:
 *           type: string
 *           enum: [created_at, severity, status]
 *         description: Sort field
 *       - in: query
 *         name: order
 *         schema:
 *           type: string
 *           enum: [asc, desc]
 *         description: Sort order
 *     responses:
 *       200:
 *         description: List of bugs
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/Bug'
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.get('/:projectId/bugs', 
  validate(validateBugFilters), 
  bugController.getBugsByProject
);

/**
 * @swagger
 * /projects/{projectId}/bugs/{bugId}:
 *   get:
 *     summary: Get bug by ID
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *       - in: path
 *         name: bugId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Bug ID
 *     responses:
 *       200:
 *         description: Bug details
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/Bug'
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.get('/:projectId/bugs/:bugId', 
  validate(validateBugParams), 
  bugController.getBugById
);

/**
 * @swagger
 * /projects/{projectId}/bugs:
 *   post:
 *     summary: Create a new bug
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - title
 *               - severity
 *               - status
 *             properties:
 *               title:
 *                 type: string
 *                 description: Bug title
 *                 example: "Login button not working"
 *               description:
 *                 type: string
 *                 description: Bug description
 *                 example: "The login button on the homepage doesn't respond when clicked"
 *               severity:
 *                 type: string
 *                 enum: [low, medium, high, critical]
 *                 description: Bug severity
 *                 example: "high"
 *               status:
 *                 type: string
 *                 enum: [open, in_progress, resolved, closed]
 *                 description: Bug status
 *                 example: "open"
 *     responses:
 *       201:
 *         description: Bug created successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/Bug'
 *       400:
 *         $ref: '#/components/responses/BadRequest'
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.post('/:projectId/bugs', 
  validate(validateCreateBug), 
  bugController.createBug
);

/**
 * @swagger
 * /projects/{projectId}/bugs/{bugId}:
 *   put:
 *     summary: Update a bug
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *       - in: path
 *         name: bugId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Bug ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               title:
 *                 type: string
 *                 description: Bug title
 *                 example: "Updated bug title"
 *               description:
 *                 type: string
 *                 description: Bug description
 *                 example: "Updated bug description"
 *               severity:
 *                 type: string
 *                 enum: [low, medium, high, critical]
 *                 description: Bug severity
 *                 example: "medium"
 *               status:
 *                 type: string
 *                 enum: [open, in_progress, resolved, closed]
 *                 description: Bug status
 *                 example: "in_progress"
 *     responses:
 *       200:
 *         description: Bug updated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 data:
 *                   $ref: '#/components/schemas/Bug'
 *       400:
 *         $ref: '#/components/responses/BadRequest'
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.put('/:projectId/bugs/:bugId', 
  validate(validateUpdateBug), 
  bugController.updateBug
);

/**
 * @swagger
 * /projects/{projectId}/bugs/{bugId}:
 *   delete:
 *     summary: Delete a bug
 *     tags: [Bugs]
 *     parameters:
 *       - in: path
 *         name: projectId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Project ID
 *       - in: path
 *         name: bugId
 *         required: true
 *         schema:
 *           type: integer
 *         description: Bug ID
 *     responses:
 *       200:
 *         description: Bug deleted successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: "Bug deleted successfully"
 *       404:
 *         $ref: '#/components/responses/NotFound'
 *       500:
 *         $ref: '#/components/responses/ServerError'
 */
router.delete('/:projectId/bugs/:bugId', 
  validate(validateBugParams), 
  bugController.deleteBug
);

export default router;