import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Index from './Index';
import * as apiService from '../services/api';

// Mock the API service
vi.mock('../services/api', () => ({
  optimizePromptStream: vi.fn(),
  StreamChunk: {} // Mock the interface
}));

describe('Index Page', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('should render the main components correctly', () => {
    // given: The Index component
    
    // when: Rendering the component
    render(<Index />);
    
    // then: All main components should be visible
    expect(screen.getByText('Promptyoo-1')).toBeInTheDocument();
    expect(screen.getByText(/If you already know what to ask the AI/)).toBeInTheDocument();
    expect(screen.getByText('What Purpose you want AI to help you achieve?')).toBeInTheDocument();
    expect(screen.getByText('Provide us the prompt you are using currently for the purpose above')).toBeInTheDocument();
    expect(screen.getByText('Optimize Prompt')).toBeInTheDocument();
  });

  it('should optimize prompt when form is submitted', async () => {
    // given: A mocked stream controller
    const mockController = { abort: vi.fn() };
    const mockStreamFn = vi.fn().mockImplementation((data, callback) => {
      // Simulate successful streaming response
      callback({ chunk: 'Optimized', complete: false });
      callback({ chunk: ' prompt', complete: true, fullResponse: 'Optimized prompt' });
      return mockController;
    });
    
    (apiService.optimizePromptStream as any).mockImplementation(mockStreamFn);
    
    // when: Rendering the component and submitting the form
    render(<Index />);
    
    // Fill in the form fields
    const purposeInput = screen.getByLabelText(/What Purpose/i);
    const promptInput = screen.getByLabelText(/Provide us the prompt/i);
    
    fireEvent.change(purposeInput, { target: { value: 'Test purpose' } });
    fireEvent.change(promptInput, { target: { value: 'Test prompt' } });
    
    // Submit the form
    const submitButton = screen.getByText('Optimize Prompt');
    fireEvent.click(submitButton);
    
    // then: The API should be called and results displayed
    expect(apiService.optimizePromptStream).toHaveBeenCalledWith(
      expect.objectContaining({
        prompt: expect.stringContaining('Test purpose'),
        purpose: 'Test purpose'
      }),
      expect.any(Function)
    );
    
    // Check that the optimized result is displayed
    await waitFor(() => {
      expect(screen.getByDisplayValue('Optimized prompt')).toBeInTheDocument();
    });
  });

  it('should handle optimization errors', async () => {
    // given: A mocked stream controller that returns an error
    const mockController = { abort: vi.fn() };
    const mockStreamFn = vi.fn().mockImplementation((data, callback) => {
      // Simulate error response
      callback({ error: 'API Error', complete: true, chunk: '' });
      return mockController;
    });
    
    (apiService.optimizePromptStream as any).mockImplementation(mockStreamFn);
    
    // when: Rendering the component and submitting the form
    render(<Index />);
    
    // Fill in the form fields
    const purposeInput = screen.getByLabelText(/What Purpose/i);
    const promptInput = screen.getByLabelText(/Provide us the prompt/i);
    
    fireEvent.change(purposeInput, { target: { value: 'Test purpose' } });
    fireEvent.change(promptInput, { target: { value: 'Test prompt' } });
    
    // Submit the form
    const submitButton = screen.getByText('Optimize Prompt');
    fireEvent.click(submitButton);
    
    // then: The error should be displayed
    await waitFor(() => {
      // 使用更具体的选择器来找到错误消息
      const errorElements = screen.getAllByText('API Error');
      expect(errorElements.length).toBeGreaterThan(0);
    });
  });
}); 