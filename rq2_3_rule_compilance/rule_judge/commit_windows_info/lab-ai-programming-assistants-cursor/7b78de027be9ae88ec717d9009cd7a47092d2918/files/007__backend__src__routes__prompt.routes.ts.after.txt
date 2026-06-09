import { Router } from 'express';
import { container } from '../container';
import type { IPromptController } from '../controllers/prompt.controller';

const router = Router();
const promptController = container.resolve<IPromptController>("IPromptController");

/**
 * @route POST /api/prompt/optimize
 * @desc Optimize a prompt using DeepSeek API
 * @access Public
 */
router.post('/optimize', promptController.optimizePrompt.bind(promptController));

/**
 * @route POST /api/prompt/optimize/stream
 * @desc Optimize a prompt using DeepSeek API with streaming response
 * @access Public
 */
router.post('/optimize/stream', promptController.streamOptimizePrompt.bind(promptController));

export default router; 