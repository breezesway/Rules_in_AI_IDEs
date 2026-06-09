import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { QuickWinsPanel } from './QuickWinsPanel';

const mockQuickWins = [
  {
    id: '1',
    title: 'Test Quick Win',
    description: 'Test Description',
    impact: 'high' as const,
    module: 'Test Module',
    codeSnippet: 'console.log("test");',
  },
  {
    id: '2',
    title: 'Another Quick Win',
    description: 'Another Description',
    impact: 'medium' as const,
    module: 'Another Module',
  },
];

describe('QuickWinsPanel', () => {
  it('renders quick wins correctly', () => {
    render(<QuickWinsPanel quickWins={mockQuickWins} />);

    expect(screen.getByText('Quick Wins')).toBeInTheDocument();
    expect(screen.getByText('Test Quick Win')).toBeInTheDocument();
    expect(screen.getByText('Another Quick Win')).toBeInTheDocument();
  });

  it('displays impact labels correctly', () => {
    render(<QuickWinsPanel quickWins={mockQuickWins} />);

    expect(screen.getByText('Hoge Impact')).toBeInTheDocument();
    expect(screen.getByText('Gemiddelde Impact')).toBeInTheDocument();
  });

  it('shows code snippet when available', () => {
    render(<QuickWinsPanel quickWins={mockQuickWins} />);

    expect(screen.getByText('console.log("test");')).toBeInTheDocument();
  });

  it('handles copy functionality', async () => {
    const mockClipboard = {
      writeText: jest.fn().mockImplementation(() => Promise.resolve()),
    };
    Object.assign(navigator, {
      clipboard: mockClipboard,
    });

    render(<QuickWinsPanel quickWins={mockQuickWins} />);

    const copyButton = screen.getByTitle('Kopieer code');
    fireEvent.click(copyButton);

    expect(mockClipboard.writeText).toHaveBeenCalledWith('console.log("test");');
    expect(screen.getByText('Gekopieerd!')).toBeInTheDocument();
  });

  it('displays module information', () => {
    render(<QuickWinsPanel quickWins={mockQuickWins} />);

    expect(screen.getByText('Test Module')).toBeInTheDocument();
    expect(screen.getByText('Another Module')).toBeInTheDocument();
  });
});
