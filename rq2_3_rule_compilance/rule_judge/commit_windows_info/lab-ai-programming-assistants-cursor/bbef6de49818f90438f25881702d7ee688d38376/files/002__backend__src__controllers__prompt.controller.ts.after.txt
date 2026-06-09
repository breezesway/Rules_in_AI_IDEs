import { Request, Response } from 'express';
import deepseekServiceDefault from '../services/deepseek.service';
import type { IDeepSeekService } from '../services/deepseek.service';
import { OptimizePromptRequest } from '../types/api';
import { injectable, singleton, inject } from 'tsyringe';

export interface IPromptController {
  optimizePrompt(req: Request, res: Response): Promise<void>;
  streamOptimizePrompt(req: Request, res: Response): Promise<void>;
}

@injectable()
export class PromptController implements IPromptController {
  private deepseekService: IDeepSeekService;

  constructor(@inject("IDeepSeekService") deepseekService: IDeepSeekService) {
    this.deepseekService = deepseekService;
  }

  /**
   * Handle the request to optimize a prompt
   */
  async optimizePrompt(req: Request, res: Response): Promise<void> {
    try {
      const data = req.body as OptimizePromptRequest;
      
      if (!data.prompt) {
        res.status(400).json({ error: 'Prompt is required' });
        return;
      }
      
      const optimizedPrompt = await this.deepseekService.optimizePrompt(data);
      
      res.status(200).json({ optimizedPrompt });
    } catch (error: any) {
      console.error('Error in prompt optimization:', error);
      
      const statusCode = error.status || 500;
      const message = error.message || 'An error occurred while optimizing the prompt';
      
      res.status(statusCode).json({
        error: message,
        optimizedPrompt: null
      });
    }
  }

  /**
   * Handle streaming request to optimize a prompt
   */
  async streamOptimizePrompt(req: Request, res: Response): Promise<void> {
    try {
      const data = req.body as OptimizePromptRequest;
      
      if (!data.prompt) {
        res.status(400).json({ error: 'Prompt is required' });
        return;
      }
      
      console.log('Starting stream optimization for prompt');
      await this.deepseekService.optimizePromptStream(data, res);
      // Note: The response is handled within the service
      
    } catch (error: any) {
      console.error('Error in stream prompt optimization:', error);
      
      // If headers haven't been sent yet, send a JSON error
      if (!res.headersSent) {
        const statusCode = error.status || 500;
        const message = error.message || 'An error occurred while streaming the prompt optimization';
        
        res.status(statusCode).json({
          error: message,
          optimizedPrompt: null
        });
      }
    }
  }
}

@singleton()
export class PromptControllerSingleton extends PromptController {
  constructor(@inject("IDeepSeekService") deepseekService: IDeepSeekService) {
    super(deepseekService);
  }
}

// Export a default instance for backward compatibility
class DefaultPromptController extends PromptController {
  constructor() {
    // Use the imported default service instance
    super(deepseekServiceDefault);
  }
}

export default new DefaultPromptController(); 