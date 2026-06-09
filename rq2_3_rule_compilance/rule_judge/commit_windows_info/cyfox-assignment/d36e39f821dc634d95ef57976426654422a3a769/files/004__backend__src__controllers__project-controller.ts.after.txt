import { Request, Response } from 'express';
import * as projectService from '../services/project-service';
import { sendSuccess, sendCreated, sendNoContent } from '../utils/response';
import { asyncHandler } from '../middleware/error-handler';
import { CreateProjectRequest } from '../models/project';

/**
 * Get all projects
 * GET /api/projects
 */
export const getAllProjects = asyncHandler(async (_req: Request, res: Response) => {
  const projects = await projectService.getAllProjects();
  
  sendSuccess(res, projects, `Retrieved ${projects.length} projects`);
});

/**
 * Get project by ID
 * GET /api/projects/:id
 */
export const getProjectById = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['id']!);
  const project = await projectService.getProjectById(projectId);
  
  sendSuccess(res, project);
});

/**
 * Create new project
 * POST /api/projects
 */
export const createProject = asyncHandler(async (req: Request, res: Response) => {
  const projectData: CreateProjectRequest = req.body;
  const project = await projectService.createProject(projectData);
  
  sendCreated(res, project, 'Project created successfully');
});

/**
 * Update project
 * PUT /api/projects/:id
 */
export const updateProject = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['id']!);
  const updates: Partial<CreateProjectRequest> = req.body;
  
  const project = await projectService.updateProject(projectId, updates);
  
  sendSuccess(res, project, 'Project updated successfully');
});

/**
 * Delete project
 * DELETE /api/projects/:id
 */
export const deleteProject = asyncHandler(async (req: Request, res: Response) => {
  const projectId = parseInt(req.params['id']!);
  
  await projectService.deleteProject(projectId);
  
  sendNoContent(res);
});