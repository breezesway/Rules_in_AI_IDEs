import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ModuleOverview } from './ModuleOverview';

const mockModules = [
  {
    id: '1',
    name: 'Test Module 1',
    score: 75,
    maxScore: 100,
    status: 'success' as const,
    lastUpdated: '2024-03-20',
  },
  {
    id: '2',
    name: 'Test Module 2',
    score: 45,
    maxScore: 100,
    status: 'warning' as const,
    lastUpdated: '2024-03-19',
  },
  {
    id: '3',
    name: 'Test Module 3',
    score: 0,
    maxScore: 100,
    status: 'danger' as const,
    lastUpdated: '2024-03-18',
  },
];

describe('ModuleOverview', () => {
  it('renders modules in grid layout by default', () => {
    render(<ModuleOverview modules={mockModules} />);

    expect(screen.getByText('Module Overzicht')).toBeInTheDocument();
    expect(screen.getByText('Test Module 1')).toBeInTheDocument();
    expect(screen.getByText('Test Module 2')).toBeInTheDocument();
    expect(screen.getByText('Test Module 3')).toBeInTheDocument();
  });

  it('displays correct status labels', () => {
    render(<ModuleOverview modules={mockModules} />);

    expect(screen.getByText('Voltooid')).toBeInTheDocument();
    expect(screen.getByText('In Uitvoering')).toBeInTheDocument();
    expect(screen.getByText('Niet Gestart')).toBeInTheDocument();
  });

  it('shows module scores correctly', () => {
    render(<ModuleOverview modules={mockModules} />);

    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('45%')).toBeInTheDocument();
    expect(screen.getByText('0%')).toBeInTheDocument();
  });

  it('formats dates correctly', () => {
    render(<ModuleOverview modules={mockModules} />);

    expect(screen.getByText('Laatste update: 20 maart 2024')).toBeInTheDocument();
    expect(screen.getByText('Laatste update: 19 maart 2024')).toBeInTheDocument();
    expect(screen.getByText('Laatste update: 18 maart 2024')).toBeInTheDocument();
  });

  it('switches between grid and list layout', () => {
    const { rerender } = render(<ModuleOverview modules={mockModules} />);

    // Check initial grid layout
    expect(screen.getByText('Grid')).toHaveClass('bg-blue-500');
    expect(screen.getByText('Lijst')).toHaveClass('bg-gray-100');

    // Switch to list layout
    rerender(<ModuleOverview modules={mockModules} layout="list" />);
    expect(screen.getByText('Grid')).toHaveClass('bg-gray-100');
    expect(screen.getByText('Lijst')).toHaveClass('bg-blue-500');
  });

  it('renders radar chart with correct data', () => {
    render(<ModuleOverview modules={mockModules} />);

    expect(screen.getByText('Module Prestaties')).toBeInTheDocument();
    // Check if radar chart container is present
    expect(screen.getByRole('img', { name: /radar chart/i })).toBeInTheDocument();
  });
});
