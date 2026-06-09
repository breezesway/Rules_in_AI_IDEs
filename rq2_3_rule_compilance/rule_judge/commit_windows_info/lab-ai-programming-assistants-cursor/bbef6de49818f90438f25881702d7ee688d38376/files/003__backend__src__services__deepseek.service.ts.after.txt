import OpenAI from "openai";
import { OptimizePromptRequest } from "../types/api";
import { Response } from "express";
import { singleton, injectable } from "tsyringe";
import { getEnv, getNumericEnv } from "../utils/env";

// API configuration with fallbacks and default values
const DEEPSEEK_API_KEY = getEnv("DEEPSEEK_API_KEY", {
  fallbackKeys: ["OPENAI_API_KEY"],
  // Don't set required: true to allow DI to work without immediately throwing
});

const DEEPSEEK_API_BASE_URL = getEnv("DEEPSEEK_API_BASE_URL", {
  default: 'https://api.deepseek.com'
});

const DEEPSEEK_TIMEOUT_MS = getNumericEnv("DEEPSEEK_TIMEOUT_MS", {
  default: 30000,
  min: 1000
});

// Must be a non-undefined string to satisfy OpenAI client type requirements
const DEFAULT_MODEL = getEnv("DEEPSEEK_DEFAULT_MODEL", {
  default: 'deepseek-chat'
}) as string;

// This check is for development/testing purposes only - we handle this more gracefully in production
if (process.env.NODE_ENV === 'development' && !DEEPSEEK_API_KEY) {
  console.warn("Warning: DEEPSEEK_API_KEY or OPENAI_API_KEY is not set in environment variables. API calls will fail.");
}

/**
 * Standardized API error with additional context
 */
export class DeepSeekApiError extends Error {
  constructor(
    message: string, 
    public readonly statusCode?: number,
    public readonly originalError?: any
  ) {
    super(message);
    this.name = 'DeepSeekApiError';
  }
}

// Define the interface for the DeepSeekService
export interface IDeepSeekService {
  /**
   * Optimize a prompt using DeepSeek API (non-streaming)
   * @param data The request data containing prompt and optional system prompt
   * @returns Promise with the optimized prompt
   * @throws DeepSeekApiError on API failures
   */
  optimizePrompt(data: OptimizePromptRequest): Promise<string>;
  
  /**
   * Optimize a prompt using DeepSeek API with streaming response
   * @param data The request data containing prompt and optional system prompt
   * @param res Express Response object to stream results
   * @returns Promise that resolves when streaming is complete
   */
  optimizePromptStream(data: OptimizePromptRequest, res: Response): Promise<void>;
}

// Initialize OpenAI client with DeepSeek configuration
const createOpenAIClient = (apiKey?: string) => {
  const key = apiKey || DEEPSEEK_API_KEY;
  
  if (!key) {
    throw new DeepSeekApiError(
      "API key not provided. Set DEEPSEEK_API_KEY or OPENAI_API_KEY in environment variables.",
      401
    );
  }
  
  // Create client with explicit configuration to avoid env var detection issues
  return new OpenAI({
    baseURL: DEEPSEEK_API_BASE_URL,
    apiKey: key,
    timeout: DEEPSEEK_TIMEOUT_MS,
    maxRetries: 2,
    dangerouslyAllowBrowser: false, // Server-side only
  });
};

@injectable()
export class DeepSeekService implements IDeepSeekService {
  private openaiClient: OpenAI | null = null;
  
  constructor() {
    // Defer client creation until first use to avoid initialization errors during DI setup
  }
  
  /**
   * Get or initialize the OpenAI client
   */
  private getClient(): OpenAI {
    if (!this.openaiClient) {
      try {
        this.openaiClient = createOpenAIClient(DEEPSEEK_API_KEY);
      } catch (error) {
        console.error("Failed to initialize OpenAI client:", error);
        throw error;
      }
    }
    return this.openaiClient;
  }

  /**
   * Validates input data for the optimize prompt requests
   * @throws Error if validation fails
   */
  private validateRequestData(data: OptimizePromptRequest): void {
    if (!data.prompt || typeof data.prompt !== 'string' || data.prompt.trim() === '') {
      throw new Error('Prompt is required and must be a non-empty string');
    }
    
    if (data.systemPrompt && typeof data.systemPrompt !== 'string') {
      throw new Error('System prompt must be a string if provided');
    }
  }

  /**
   * Optimize a prompt using DeepSeek API (non-streaming)
   */
  async optimizePrompt(data: OptimizePromptRequest): Promise<string> {
    try {
      this.validateRequestData(data);
      const systemMessage = data.systemPrompt || "You are a helpful assistant.";
      
      const completion = await this.getClient().chat.completions.create({
        messages: [
          { role: "system", content: systemMessage },
          { role: "user", content: data.prompt }
        ],
        model: DEFAULT_MODEL,
      });

      if (!completion.choices[0]?.message?.content) {
        throw new DeepSeekApiError('Received empty response from DeepSeek API', 500);
      }

      return completion.choices[0].message.content;
    } catch (error: any) {
      // Handle OpenAI specific errors
      if (error.name === 'APIError') {
        console.error(`DeepSeek API Error (${error.status}):`, error.message);
        throw new DeepSeekApiError(
          `DeepSeek API Error: ${error.message}`,
          error.status,
          error
        );
      }
      
      // Handle timeout errors
      if (error.name === 'AbortError') {
        console.error('DeepSeek API request timed out');
        throw new DeepSeekApiError('DeepSeek API request timed out', 504, error);
      }
      
      // Handle validation errors
      if (error instanceof Error && !error.name.includes('DeepSeekApiError')) {
        console.error('Validation error:', error.message);
        throw new DeepSeekApiError(error.message, 400, error);
      }
      
      // Pass through DeepSeekApiError or rethrow as generic error
      if (!(error instanceof DeepSeekApiError)) {
        console.error("Unexpected error calling DeepSeek API:", error);
        throw new DeepSeekApiError('Unexpected error processing request', 500, error);
      }
      
      throw error;
    }
  }

  /**
   * Optimize a prompt using DeepSeek API with streaming response
   */
  async optimizePromptStream(data: OptimizePromptRequest, res: Response): Promise<void> {
    let streamClosed = false;
    
    // Handle response close event
    res.on('close', () => {
      streamClosed = true;
      console.log('Client connection closed - stream terminated');
    });
    
    try {
      this.validateRequestData(data);
      const systemMessage = data.systemPrompt || "You are a helpful assistant.";
      
      // Set up SSE headers
      res.setHeader('Content-Type', 'text/event-stream');
      res.setHeader('Cache-Control', 'no-cache');
      res.setHeader('Connection', 'keep-alive');
      
      // Create streaming request to DeepSeek API
      const stream = await this.getClient().chat.completions.create({
        messages: [
          { role: "system", content: systemMessage },
          { role: "user", content: data.prompt }
        ],
        model: DEFAULT_MODEL,
        stream: true,
      });
      
      let completeResponse = "";
      
      console.log("Stream started");

      // Process each chunk from the stream
      for await (const chunk of stream) {
        if (streamClosed) break;
        
        const content = chunk.choices[0]?.delta?.content || "";
        if (content) {
          completeResponse += content;
          
          // Send the chunk to the client
          res.write(`data: ${JSON.stringify({ chunk: content, complete: false })}\n\n`);
        }
      }
      
      console.log("Stream completed");
      
      // Send completion message only if stream is still open
      if (!streamClosed) {
        res.write(`data: ${JSON.stringify({ chunk: "", complete: true, fullResponse: completeResponse })}\n\n`);
        res.end();
      }
    } catch (error: any) {
      console.error("Error streaming from DeepSeek API:", error);
      
      // Only send error if stream is still open
      if (!streamClosed) {
        // Format error message based on error type
        let errorMessage = 'Error processing stream';
        let statusCode = 500;
        
        if (error.name === 'APIError') {
          errorMessage = `DeepSeek API Error: ${error.message}`;
          statusCode = error.status || 500;
        } else if (error.name === 'AbortError') {
          errorMessage = 'DeepSeek API request timed out';
          statusCode = 504;
        } else if (error.message && !error.name.includes('DeepSeekApiError')) {
          errorMessage = error.message;
          statusCode = 400;
        }
        
        // Send detailed error to client
        res.write(`data: ${JSON.stringify({ 
          error: errorMessage,
          statusCode,
          complete: true 
        })}\n\n`);
        res.end();
      }
      
      throw new DeepSeekApiError(
        error.message || 'Unknown streaming error',
        error.status || 500,
        error
      );
    }
  }
}

// Export a singleton instance
@singleton()
export class DeepSeekServiceSingleton extends DeepSeekService {
  constructor() {
    super();
  }
}

// Create an instance for default export (for backward compatibility and testing)
const defaultServiceInstance = new DeepSeekService();

export default defaultServiceInstance; 