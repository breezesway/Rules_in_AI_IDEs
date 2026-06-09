import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import PromptForm from './PromptForm';

describe('PromptForm', () => {
  it('renders the Optimize Prompt button', () => {
    // Mock the onOptimize function
    const mockOnOptimize = vi.fn();
    
    // Render the component
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={false} />);
    
    // Check if the button with text "Optimize Prompt" exists
    const optimizeButton = screen.getByText('Optimize Prompt');
    expect(optimizeButton).toBeInTheDocument();
  });

  it('shows loading indicator when optimizing', () => {
    // Mock the onOptimize function
    const mockOnOptimize = vi.fn();
    
    // Render the component with isOptimizing=true
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={true} />);
    
    // The button should be disabled when optimizing
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    
    // Check if the loading indicator is shown instead of "Optimize Prompt" text
    expect(screen.queryByText('Optimize Prompt')).not.toBeInTheDocument();
  });
}); 