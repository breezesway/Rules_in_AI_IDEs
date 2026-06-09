import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import OptimizedResult from './OptimizedResult';
import * as toast from '@/components/ui/use-toast';

vi.mock('@/components/ui/use-toast', () => ({
  useToast: vi.fn()
}));

describe('OptimizedResult', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    (toast.useToast as any).mockReturnValue({
      toast: vi.fn()
    });
    
    // Properly mock clipboard
    vi.spyOn(navigator.clipboard, 'writeText').mockImplementation(() => Promise.resolve());
  });

  it('shows placeholder when no optimized prompt is provided', () => {
    // given: No optimized prompt
    
    // when: Rendering the component with null optimized prompt
    render(<OptimizedResult optimizedPrompt={null} />);
    
    // then: The placeholder text should be displayed
    expect(screen.getByText(/Your optimized prompt will be displayed here/i)).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /copy/i })).not.toBeInTheDocument();
  });

  it('displays the optimized prompt when provided', () => {
    // given: An optimized prompt
    const optimizedPrompt = 'This is an optimized prompt';
    
    // when: Rendering the component with the optimized prompt
    render(<OptimizedResult optimizedPrompt={optimizedPrompt} />);
    
    // then: The optimized prompt should be displayed in the textarea
    const textarea = screen.getByRole('textbox');
    expect(textarea).toHaveValue(optimizedPrompt);
    
    // Copy button should be visible
    expect(screen.getByRole('button', { name: /copy/i })).toBeInTheDocument();
  });

  it('copies text to clipboard when copy button is clicked', () => {
    // given: An optimized prompt
    const optimizedPrompt = 'This is an optimized prompt';
    const mockToast = vi.fn();
    (toast.useToast as any).mockReturnValue({
      toast: mockToast
    });
    
    // when: Rendering the component and clicking the copy button
    render(<OptimizedResult optimizedPrompt={optimizedPrompt} />);
    
    const copyButton = screen.getByRole('button', { name: /copy/i });
    fireEvent.click(copyButton);
    
    // then: The navigator.clipboard.writeText should be called with the prompt
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith(optimizedPrompt);
    expect(mockToast).toHaveBeenCalledWith(expect.objectContaining({
      title: 'Copied to clipboard'
    }));
  });

  it('displays error messages when provided', () => {
    // given: An error message
    const errorMessage = 'An error occurred';
    
    // when: Rendering the component with an error
    render(<OptimizedResult optimizedPrompt={null} error={errorMessage} />);
    
    // then: The error message should be displayed
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
    expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
  });

  it('shows streaming indicator when isStreaming is true', () => {
    // given: Streaming state is true
    const optimizedPrompt = 'This is streaming content';
    
    // when: Rendering the component with isStreaming=true
    render(<OptimizedResult optimizedPrompt={optimizedPrompt} isStreaming={true} />);
    
    // then: The streaming indicator should be visible
    expect(screen.getByText(/Response streaming.../i)).toBeInTheDocument();
    
    // Copy button should not be visible during streaming
    expect(screen.queryByRole('button', { name: /copy/i })).not.toBeInTheDocument();
  });
}); 