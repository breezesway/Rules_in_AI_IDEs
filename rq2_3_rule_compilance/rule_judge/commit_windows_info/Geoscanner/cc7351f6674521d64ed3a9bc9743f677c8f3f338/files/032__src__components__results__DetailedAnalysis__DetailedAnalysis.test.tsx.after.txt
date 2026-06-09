import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { DetailedAnalysis } from './DetailedAnalysis';

const mockSections = [
  {
    id: 'section1',
    title: 'Test Section 1',
    description: 'Test Description 1',
    codeSnippets: [
      {
        id: 'snippet1',
        language: 'javascript',
        code: 'console.log("test");',
        description: 'Test Code Snippet 1',
      },
    ],
    currentScore: 60,
    predictedScore: 80,
  },
  {
    id: 'section2',
    title: 'Test Section 2',
    description: 'Test Description 2',
    codeSnippets: [
      {
        id: 'snippet2',
        language: 'typescript',
        code: 'const test: string = "test";',
        description: 'Test Code Snippet 2',
      },
    ],
    currentScore: 40,
    predictedScore: 30,
  },
];

describe('DetailedAnalysis', () => {
  beforeEach(() => {
    // Mock clipboard API
    Object.assign(navigator, {
      clipboard: {
        writeText: jest.fn().mockImplementation(() => Promise.resolve()),
      },
    });
  });

  it('renders all sections', () => {
    render(<DetailedAnalysis sections={mockSections} />);

    expect(screen.getByText('Test Section 1')).toBeInTheDocument();
    expect(screen.getByText('Test Section 2')).toBeInTheDocument();
  });

  it('expands and collapses sections when clicked', () => {
    render(<DetailedAnalysis sections={mockSections} />);

    // Initially sections should be collapsed
    expect(screen.queryByText('Test Code Snippet 1')).not.toBeInTheDocument();

    // Click to expand first section
    fireEvent.click(screen.getByText('Test Section 1'));
    expect(screen.getByText('Test Code Snippet 1')).toBeInTheDocument();

    // Click to collapse
    fireEvent.click(screen.getByText('Test Section 1'));
    expect(screen.queryByText('Test Code Snippet 1')).not.toBeInTheDocument();
  });

  it('copies code to clipboard when copy button is clicked', async () => {
    render(<DetailedAnalysis sections={mockSections} />);

    // Expand section
    fireEvent.click(screen.getByText('Test Section 1'));

    // Click copy button
    const copyButton = screen.getByRole('button', { name: /copy/i });
    fireEvent.click(copyButton);

    // Check if clipboard API was called
    expect(navigator.clipboard.writeText).toHaveBeenCalledWith('console.log("test");');
  });

  it('displays score improvements correctly', () => {
    render(<DetailedAnalysis sections={mockSections} />);

    // Expand first section
    fireEvent.click(screen.getByText('Test Section 1'));

    // Check positive improvement
    expect(screen.getByText('+33%')).toBeInTheDocument();

    // Expand second section
    fireEvent.click(screen.getByText('Test Section 2'));

    // Check negative improvement
    expect(screen.getByText('-25%')).toBeInTheDocument();
  });

  it('shows code snippets with syntax highlighting', () => {
    render(<DetailedAnalysis sections={mockSections} />);

    // Expand section
    fireEvent.click(screen.getByText('Test Section 1'));

    // Check if code is displayed
    expect(screen.getByText('console.log("test");')).toBeInTheDocument();
  });
});
