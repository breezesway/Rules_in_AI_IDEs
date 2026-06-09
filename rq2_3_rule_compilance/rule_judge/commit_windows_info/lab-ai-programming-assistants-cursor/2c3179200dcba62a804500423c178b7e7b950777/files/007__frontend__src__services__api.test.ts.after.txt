import { describe, it, expect, vi, beforeEach } from 'vitest';
import { optimizePrompt, optimizePromptStream } from './api';

// Mock fetch
global.fetch = vi.fn();

describe('API Service', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  describe('optimizePrompt', () => {
    it('should successfully optimize a prompt', async () => {
      // given: A successful API response
      const mockResponse = {
        optimizedPrompt: 'Optimized version of the prompt'
      };
      
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      // when: Calling the optimizePrompt function
      const result = await optimizePrompt({
        prompt: 'Original prompt',
        purpose: 'Some purpose'
      });

      // then: It should return the optimized prompt
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:5001/api/prompt/optimize',
        expect.objectContaining({
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            prompt: 'Original prompt',
            purpose: 'Some purpose'
          })
        })
      );
    });

    it('should handle API errors', async () => {
      // given: An API error response
      const errorMessage = 'API error occurred';
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: errorMessage })
      });

      // when: Calling the optimizePrompt function
      const result = await optimizePrompt({
        prompt: 'Original prompt',
        purpose: 'Some purpose'
      });

      // then: It should return an error object
      expect(result).toEqual({
        optimizedPrompt: '',
        error: errorMessage
      });
    });
  });

  describe('optimizePromptStream', () => {
    it('should handle streaming responses', async () => {
      // given: A mock readable stream and reader
      const mockReader = {
        read: vi.fn()
          .mockResolvedValueOnce({ done: false, value: new TextEncoder().encode('data: {"chunk":"Chunk1","complete":false}\n\n') })
          .mockResolvedValueOnce({ done: false, value: new TextEncoder().encode('data: {"chunk":"Chunk2","complete":true,"fullResponse":"Full response"}\n\n') })
          .mockResolvedValueOnce({ done: true })
      };
      
      const mockBody = {
        getReader: () => mockReader
      };
      
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        body: mockBody
      });

      // when: Calling the optimizePromptStream function
      const onChunk = vi.fn();
      optimizePromptStream({
        prompt: 'Streaming prompt',
        purpose: 'Some purpose'
      }, onChunk);

      // Allow streaming to process
      await new Promise(resolve => setTimeout(resolve, 100));

      // then: The onChunk callback should be called with each chunk
      expect(onChunk).toHaveBeenCalledTimes(2);
      expect(onChunk).toHaveBeenNthCalledWith(1, {
        chunk: 'Chunk1',
        complete: false
      });
      expect(onChunk).toHaveBeenNthCalledWith(2, {
        chunk: 'Chunk2',
        complete: true,
        fullResponse: 'Full response'
      });
    });

    it('should handle stream errors', async () => {
      // given: A fetch that throws an error
      global.fetch = vi.fn().mockRejectedValueOnce(new Error('Stream error'));

      // when: Calling the optimizePromptStream function
      const onChunk = vi.fn();
      optimizePromptStream({
        prompt: 'Stream error prompt',
        purpose: 'Some purpose'
      }, onChunk);

      // Allow error handling to process
      await new Promise(resolve => setTimeout(resolve, 100));

      // then: The onChunk callback should be called with the error
      expect(onChunk).toHaveBeenCalledWith({
        chunk: '',
        complete: true,
        error: 'Stream error'
      });
    });
  });
}); 