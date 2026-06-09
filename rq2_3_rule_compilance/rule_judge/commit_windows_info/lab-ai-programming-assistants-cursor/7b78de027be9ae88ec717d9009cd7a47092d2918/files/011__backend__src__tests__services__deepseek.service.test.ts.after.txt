import 'reflect-metadata';
import { mock, mockDeep, MockProxy } from 'jest-mock-extended';
import OpenAI from 'openai';
import { DeepSeekService } from '../../services/deepseek.service';
import type { OptimizePromptRequest } from '../../types/api';

describe('DeepSeekService', () => {
  // Create a mock OpenAI client with proper structure
  let mockOpenAI: MockProxy<OpenAI> & {
    chat: {
      completions: {
        create: jest.Mock;
      };
    };
  };

  // Create an instance of the service with the mock
  let deepseekService: DeepSeekService;

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
    mockOpenAI = mockDeep<OpenAI>() as MockProxy<OpenAI> & {
      chat: {
        completions: {
          create: jest.Mock;
        };
      };
    };

    // Manually set up the nested structure needed for the test
    mockOpenAI.chat = {
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
      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
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
      expect(mockOpenAI.chat.completions.create).toHaveBeenCalledWith({
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
      mockOpenAI.chat.completions.create.mockRejectedValueOnce(new Error(errorMessage));

      // Call the method and expect it to throw
      await expect(deepseekService.optimizePrompt(testPrompt)).rejects.toThrow(errorMessage);
    });
  });
}); 