import { describe, it, expect, vi, beforeEach } from 'vitest';
import { optimizePrompt } from './api';

// 不使用MSW进行此集成测试，改为直接模拟fetch API
describe('API Service', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    // 清除模拟
    vi.restoreAllMocks();
  });

  it('should fetch optimized prompt from API', async () => {
    // given: 模拟fetch成功响应
    const mockResponse = {
      optimizedPrompt: 'Mocked optimized prompt response'
    };
    
    const fetchSpy = vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    } as Response);
    
    // when: 调用optimizePrompt函数
    const result = await optimizePrompt({
      prompt: 'Test prompt',
      purpose: 'Test purpose'
    });
    
    // then: 应返回模拟的响应
    expect(result).toEqual(mockResponse);
    expect(fetchSpy).toHaveBeenCalledWith(
      'http://localhost:5001/api/prompt/optimize',
      expect.objectContaining({
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          prompt: 'Test prompt',
          purpose: 'Test purpose'
        })
      })
    );
  });

  it('should handle API errors correctly', async () => {
    // given: 模拟fetch错误响应
    const errorMessage = 'Server error';
    
    vi.spyOn(global, 'fetch').mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: errorMessage })
    } as Response);
    
    // when: 调用optimizePrompt函数
    const result = await optimizePrompt({
      prompt: 'Error test',
      purpose: 'Error purpose'
    });
    
    // then: 应返回错误信息
    expect(result).toEqual({
      optimizedPrompt: '',
      error: errorMessage
    });
  });
}); 