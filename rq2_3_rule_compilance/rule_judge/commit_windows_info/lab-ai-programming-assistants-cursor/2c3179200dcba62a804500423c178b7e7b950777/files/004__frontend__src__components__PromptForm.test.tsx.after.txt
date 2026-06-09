import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import PromptForm from './PromptForm';

describe('PromptForm', () => {
  it('renders the form with default values', () => {
    // given: Default props for the component
    const mockOnOptimize = vi.fn();
    
    // when: Rendering the component
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={false} />);
    
    // then: Default values should be present
    const purposeInput = screen.getByLabelText(/What Purpose/i);
    const promptInput = screen.getByLabelText(/Provide us the prompt/i);
    
    expect(purposeInput).toHaveValue('Find popular prompt optimization tools');
    expect(promptInput).toHaveValue('Recommend some prompt optimization tools');
    expect(screen.getByText('Optimize Prompt')).toBeInTheDocument();
  });

  it('calls onOptimize when form is submitted', async () => {
    // given: A mock onOptimize function
    const mockOnOptimize = vi.fn();
    const user = userEvent.setup();
    
    // when: Rendering the component and submitting the form
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={false} />);
    
    // Change input values
    const purposeInput = screen.getByLabelText(/What Purpose/i);
    const promptInput = screen.getByLabelText(/Provide us the prompt/i);
    
    await user.clear(purposeInput);
    await user.type(purposeInput, 'New purpose');
    
    await user.clear(promptInput);
    await user.type(promptInput, 'New prompt');
    
    // Submit the form
    const submitButton = screen.getByText('Optimize Prompt');
    await user.click(submitButton);
    
    // then: The onOptimize callback should be called with the form values
    expect(mockOnOptimize).toHaveBeenCalledWith('New purpose', 'New prompt');
  });
  
  it('shows loading indicator when optimizing', () => {
    // given: isOptimizing is true
    const mockOnOptimize = vi.fn();
    
    // when: Rendering the component with isOptimizing=true
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={true} />);
    
    // then: The button should be disabled and show loading indicator
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    
    // Check if the loading indicator is shown instead of "Optimize Prompt" text
    expect(screen.queryByText('Optimize Prompt')).not.toBeInTheDocument();
    
    // Check if the warning alert is displayed
    expect(screen.getByText(/Prompt optimization can take up to 1 minute/i)).toBeInTheDocument();
  });
  
  it('disables the submit button when inputs are empty', async () => {
    // given: Empty form inputs
    const mockOnOptimize = vi.fn();
    const user = userEvent.setup();
    
    // when: Rendering the component and clearing the inputs
    render(<PromptForm onOptimize={mockOnOptimize} isOptimizing={false} />);
    
    const purposeInput = screen.getByLabelText(/What Purpose/i);
    const promptInput = screen.getByLabelText(/Provide us the prompt/i);
    
    await user.clear(purposeInput);
    await user.clear(promptInput);
    
    // then: The submit button should be disabled
    const submitButton = screen.getByText('Optimize Prompt');
    expect(submitButton).toBeDisabled();
  });
}); 