import 'reflect-metadata';
import { EventEmitter } from 'events';
import { Response } from 'express';
import { DeepSeekService } from '../../services/deepseek.service';
import { OptimizePromptRequest } from '../../types/api';

// 模拟整个OpenAI模块
jest.mock('openai', () => {
  const mockCreateMethod = jest.fn();
  const MockOpenAI = jest.fn().mockImplementation(() => ({
    chat: {
      completions: {
        create: mockCreateMethod
      }
    }
  }));
  
  // 导出模拟方法以便测试可以访问
  (MockOpenAI as any).mockCreateMethod = mockCreateMethod;
  
  return {
    __esModule: true,
    default: MockOpenAI
  };
});

// 导入模拟的OpenAI
import OpenAI from 'openai';

// 获取模拟方法的引用
const mockCreateMethod = (OpenAI as any).mockCreateMethod;

describe('DeepSeekService', () => {
  let deepseekService: DeepSeekService;
  let mockResponse: Partial<Response> & EventEmitter;
  
  const testPrompt: OptimizePromptRequest = {
    prompt: 'Can you help me optimize this code?',
    systemPrompt: 'You are a helpful coding assistant.'
  };
  
  const mockCompletionResponse = {
    id: 'mock-id',
    choices: [{
      message: {
        content: 'I can help you optimize your code. Here are some suggestions...',
        role: 'assistant'
      }
    }]
  };
  
  beforeEach(() => {
    // 每次测试前重置模拟
    jest.clearAllMocks();
    
    // 模拟console.log以减少测试输出
    jest.spyOn(console, 'log').mockImplementation();
    jest.spyOn(console, 'error').mockImplementation();
    
    // 创建新的服务实例
    deepseekService = new DeepSeekService();
    
    // 创建模拟Response对象
    const emitter = new EventEmitter();
    mockResponse = {
      setHeader: jest.fn(),
      write: jest.fn(),
      end: jest.fn(),
      headersSent: false,
      on: emitter.on.bind(emitter),
      once: emitter.once.bind(emitter),
      emit: emitter.emit.bind(emitter)
    };
    
    // 默认响应
    mockCreateMethod.mockResolvedValue(mockCompletionResponse);
  });
  
  afterEach(() => {
    jest.restoreAllMocks();
  });
  
  describe('optimizePrompt', () => {
    it('should call API with correct parameters and return response', async () => {
      // 准备模拟响应
      mockCreateMethod.mockResolvedValueOnce(mockCompletionResponse);
      
      // 调用被测方法
      const result = await deepseekService.optimizePrompt(testPrompt);
      
      // 验证API调用参数
      expect(mockCreateMethod).toHaveBeenCalledWith({
        messages: [
          { role: 'system', content: testPrompt.systemPrompt },
          { role: 'user', content: testPrompt.prompt }
        ],
        model: expect.any(String)
      });
      
      // 验证结果
      expect(result).toBe(mockCompletionResponse.choices[0].message.content);
    });
    
    it('should use default system prompt if not provided', async () => {
      // 创建没有系统提示的请求
      const promptWithoutSystem: OptimizePromptRequest = {
        prompt: 'Can you help me optimize this code?'
      };
      
      // 调用被测方法
      await deepseekService.optimizePrompt(promptWithoutSystem);
      
      // 验证系统提示使用了默认值
      expect(mockCreateMethod).toHaveBeenCalledWith({
        messages: [
          { role: 'system', content: 'You are a helpful assistant.' },
          { role: 'user', content: promptWithoutSystem.prompt }
        ],
        model: expect.any(String)
      });
    });
    
    it('should handle API errors properly', async () => {
      // 设置API错误
      const testError = new Error('API rate limit exceeded');
      mockCreateMethod.mockRejectedValueOnce(testError);
      
      // 验证错误被正确传播
      await expect(deepseekService.optimizePrompt(testPrompt)).rejects.toThrow();
    });
  });
  
  describe('optimizePromptStream', () => {
    it('should properly handle streaming response', async () => {
      // 模拟流式响应
      const mockChunks = [
        { choices: [{ delta: { content: 'First' } }] },
        { choices: [{ delta: { content: ' chunk' } }] },
        { choices: [{ delta: { content: ' of text' } }] }
      ];
      
      // 创建异步迭代器
      mockCreateMethod.mockResolvedValueOnce({
        [Symbol.asyncIterator]: () => {
          let i = 0;
          return {
            next: async () => {
              if (i < mockChunks.length) {
                return { done: false, value: mockChunks[i++] };
              }
              return { done: true, value: undefined };
            }
          };
        }
      });
      
      // 调用被测方法
      await deepseekService.optimizePromptStream(testPrompt, mockResponse as Response);
      
      // 验证响应头
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Content-Type', 'text/event-stream');
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Cache-Control', 'no-cache');
      expect(mockResponse.setHeader).toHaveBeenCalledWith('Connection', 'keep-alive');
      
      // 验证每个数据块
      expect(mockResponse.write).toHaveBeenCalledTimes(4); // 3个数据块 + 完成消息
      
      // 验证完成消息
      const calls = (mockResponse.write as jest.Mock).mock.calls;
      const lastCall = calls[calls.length - 1][0];
      expect(lastCall).toContain('complete":true');
      expect(lastCall).toContain('First chunk of text');
      
      // 验证流关闭
      expect(mockResponse.end).toHaveBeenCalled();
    });
    
    it('should handle streaming errors properly', async () => {
      // 设置流错误
      const testError = new Error('Stream error');
      mockCreateMethod.mockRejectedValueOnce(testError);
      
      // 调用被测方法 (捕获错误)
      try {
        await deepseekService.optimizePromptStream(testPrompt, mockResponse as Response);
      } catch (error) {
        // 预期抛出错误
      }
      
      // 验证错误响应
      const calls = (mockResponse.write as jest.Mock).mock.calls;
      
      // 至少有一个调用包含error
      const hasErrorMessage = calls.some(call => 
        typeof call[0] === 'string' && call[0].includes('error')
      );
      
      expect(hasErrorMessage).toBeTruthy();
      expect(mockResponse.end).toHaveBeenCalled();
    });
    
    it('should handle client disconnect event', async () => {
      // 模拟流
      const mockChunks = [
        { choices: [{ delta: { content: 'First' } }] },
        { choices: [{ delta: { content: ' chunk' } }] }
      ];
      
      // 创建异步迭代器
      mockCreateMethod.mockResolvedValueOnce({
        [Symbol.asyncIterator]: () => {
          let i = 0;
          return {
            next: async () => {
              // 在第一个数据块后模拟断开连接
              if (i === 1) {
                setTimeout(() => {
                  mockResponse.emit('close');
                }, 10);
                // 等待事件处理
                await new Promise(resolve => setTimeout(resolve, 50));
              }
              
              if (i < mockChunks.length) {
                return { done: false, value: mockChunks[i++] };
              }
              return { done: true, value: undefined };
            }
          };
        }
      });
      
      // 调用被测方法
      await deepseekService.optimizePromptStream(testPrompt, mockResponse as Response);
      
      // 验证响应不包含完成消息
      const calls = (mockResponse.write as jest.Mock).mock.calls;
      const lastCall = calls[calls.length - 1][0];
      
      // 最后一个调用不应该包含完成标记
      expect(lastCall).not.toContain('complete":true,"fullResponse"');
    });
  });
}); 