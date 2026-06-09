import { Request, Response } from 'express';
import * as bugService from '../services/bug-service';
import { sendSuccess, sendCreated, sendNoContent } from '../utils/response';
import { asyncHandler } from '../middleware/error-handler';
import { CreateBugRequest, UpdateBugRequest, BugFilters } from '../models/bug';

/**
 * Get all bugs for a project
 * GET /api/projects/:projectId/bugs
 */
export const getBugsByProject = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  
  const filters: BugFilters = {
    severity: req.query['severity'] as any,
    status: req.query['status'] as any,
    sortBy: req.query['sortBy'] as any,
    sortOrder: req.query['sortOrder'] as any,
  };

  const bugs = await bugService.getBugsByProject(projectId, filters);
  
  sendSuccess(res, bugs, `Retrieved ${bugs.length} bugs for project ${projectId}`);
});

/**
 * Get bug by ID
 * GET /api/projects/:projectId/bugs/:bugId
 */
export const getBugById = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  const bugId = parseInt(req.params['bugId']!);
  
  const bug = await bugService.getBugById(projectId, bugId);
  
  sendSuccess(res, bug);
});

/**
 * Create new bug
 * POST /api/projects/:projectId/bugs
 */
export const createBug = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  const bugData: CreateBugRequest = req.body;
  
  const bug = await bugService.createBug(projectId, bugData);
  
  sendCreated(res, bug, 'Bug created successfully');
});

/**
 * Update bug
 * PUT /api/projects/:projectId/bugs/:bugId
 */
export const updateBug = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  const bugId = parseInt(req.params['bugId']!);
  const updates: UpdateBugRequest = req.body;
  
  const bug = await bugService.updateBug(projectId, bugId, updates);
  
  sendSuccess(res, bug, 'Bug updated successfully');
});

/**
 * Delete bug
 * DELETE /api/projects/:projectId/bugs/:bugId
 */
export const deleteBug = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  const bugId = parseInt(req.params['bugId']!);
  
  await bugService.deleteBug(projectId, bugId);
  
  sendNoContent(res);
});

/**
 * Get bug statistics for a project
 * GET /api/projects/:projectId/bugs/statistics
 */
export const getBugStatistics = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['projectId']!);
  
  const statistics = await bugService.getBugStatistics(projectId);
  
  sendSuccess(res, statistics, `Retrieved bug statistics for project ${projectId}`);
});