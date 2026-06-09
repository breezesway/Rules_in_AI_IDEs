import 'reflect-metadata';
import { mock, mockDeep, MockProxy } from 'jest-mock-extended';
import OpenAI from 'openai';
import { DeepSeekService } from '../../services/deepseek.service';
import type { OptimizePromptRequest } from '../../types/api';
import { Response } from 'express';

describe('DeepSeekService', () => {
  // Create a mock OpenAI client with proper structure
  let mockOpenAI: MockProxy<OpenAI>;

  // Create an instance of the service with the mock
  let deepseekService: DeepSeekService;
  let mockResponse: jest.Mocked<Response>;

  // Test data
  const testPrompt: OptimizePromptRequest = {
    prompt: 'Can you help me optimize this code?',
    systemPrompt: 'You are a helpful coding assistant.'
  };

  // Expected response from the API
  const expectedApiResponse = {
    id: 'mock-completion-id',
    choices: [
      {
        message: {
          content: 'I can help you optimize your code. Here are some suggestions...',
          role: 'assistant'
        },
        index: 0,
        logprobs: null,
        finish_reason: 'stop'
      }
    ],
    created: Date.now(),
    model: 'deepseek-chat',
    object: 'chat.completion',
    usage: {
      prompt_tokens: 50,
      completion_tokens: 60,
      total_tokens: 110
    }
  };

  beforeEach(() => {
    // Create a fresh mock for each test
    mockOpenAI = mockDeep<OpenAI>();

    // Set up mock response for streaming tests
    mockResponse = {
      setHeader: jest.fn(),
      write: jest.fn(),
      end: jest.fn(),
      headersSent: false
    } as any;

    // Cast to 'any' to avoid TypeScript errors with the chat structure
    (mockOpenAI as any).chat = {
      completions: {
        create: jest.fn().mockResolvedValue(expectedApiResponse)
      }
    };

    // Create a new service instance for each test
    deepseekService = new DeepSeekService(mockOpenAI);
  });

  describe('optimizePrompt', () => {
    it('should call DeepSeek API with correct parameters and return the response', async () => {
      // Call the method being tested
      const result = await deepseekService.optimizePrompt(testPrompt);

      // Verify that the API was called with the expected parameters
      expect((mockOpenAI as any).chat.completions.create).toHaveBeenCalledWith({
        messages: [
          { role: 'system', content: testPrompt.systemPrompt },
          { role: 'user', content: testPrompt.prompt }
        ],
        model: 'deepseek-chat'
      });

      // Verify the result matches the expected API response content
      expect(result).toBe(expectedApiResponse.choices[0].message.content);
    });

    it('should use default system prompt if not provided', async () => {
      // Create a prompt without a system prompt
      const promptWithoutSystem: OptimizePromptRequest = {
        prompt: 'Can you help me optimize this code?'
      };

      // Call the method
      await deepseekService.optimizePrompt(promptWithoutSystem);

      // Verify the system prompt is the default
      expect((mockOpenAI as any).chat.completions.create).toHaveBeenCalledWith({
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          { role: 'user', content: promptWithoutSystem.prompt }
        ],
        model: 'deepseek-chat'
      });
    });

    it('should handle API errors properly', async () => {
      // Set up the mock to throw an error
      const errorMessage = 'API rate limit exceeded';
      (mockOpenAI as any).chat.completions.create.mockRejectedValueOnce(new Error(errorMessage));

      // Call the method and expect it to throw
      await expect(deepseekService.optimizePrompt(testPrompt)).rejects.toThrow(errorMessage);
    });
  });
  
  describe('optimizePromptStream', () => {
    it('should properly handle streaming response', async () => {
      // Given: Mock stream implementation
      const mockStream = [
        { choices: [{ delta: { content: 'First' } }] },
        { choices: [{ delta: { content: ' chunk' } }] },
        { choices: [{ delta: { content: ' of text' } }] }
      ];
      (mockOpenAI as any).chat.completions.create.mockResolvedValue({
        [Symbol.asyncIterator]: jest.fn().mockImplementation(() => {
          let i = 0;
          return {
            next: () => {
              if (i < mockStream.length) {
                return Promise.resolve({ done: false, value: mockStream[i++] });
              }
              return Promise.resolve({ done: true });
            }
          };
        })
      });
      
      // When: Calling the stream method
      await deepseekService.optimizePromptStream(testPrompt, mockResponse);
      
      // Then: Response headers should be set correctly
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Content-Type', 'text/event-stream');
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Cache-Control', 'no-cache');
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Connection', 'keep-alive');
      
      // Then: Should write each chunk to the response
      expect(mockResponse.write).toHaveBeenCalledTimes(4); // 3 chunks + completion message
      expect(mockResponse.write).toHaveBeenNthCalledWith(
        1, 
        `data: ${JSON.stringify({ chunk: 'First', complete: false })}\n\n`
      );
      expect(mockResponse.write).toHaveBeenNthCalledWith(
        2, 
        `data: ${JSON.stringify({ chunk: ' chunk', complete: false })}\n\n`
      );
      expect(mockResponse.write).toHaveBeenNthCalledWith(
        3, 
        `data: ${JSON.stringify({ chunk: ' of text', complete: false })}\n\n`
      );
      
      // Then: Should send completion message
      expect(mockResponse.write).toHaveBeenLastCalledWith(
        `data: ${JSON.stringify({ chunk: "", complete: true, fullResponse: "First chunk of text" })}\n\n`
      );
      expect(mockResponse.end).toHaveBeenCalled();
    });

    it('should handle streaming errors properly', async () => {
      // Given: A streaming error
      const testError = new Error('Stream error');
      (mockOpenAI as any).chat.completions.create.mockRejectedValue(testError);
      
      // When: Calling the stream method
      await expect(deepseekService.optimizePromptStream(testPrompt, mockResponse)).rejects.toThrow('Stream error');
      
      // Then: Should send error to client and end response
      expect(mockResponse.write).toHaveBeenCalledWith(
        `data: ${JSON.stringify({ error: 'Error processing stream', complete: true })}\n\n`
      );
      expect(mockResponse.end).toHaveBeenCalled();
    });
  });
}); 