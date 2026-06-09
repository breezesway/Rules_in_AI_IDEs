import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ScoreHero } from './ScoreHero';

describe('ScoreHero', () => {
  it('renders score correctly', () => {
    render(
      <ScoreHero score={75} totalModules={10} completedModules={7} url="https://voorbeeld.nl" />
    );

    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('Goed')).toBeInTheDocument();
  });

  it('shows previous score when provided', () => {
    render(
      <ScoreHero
        score={80}
        previousScore={70}
        totalModules={10}
        completedModules={8}
        url="https://voorbeeld.nl"
      />
    );

    expect(screen.getByText('Vorige score: 70%')).toBeInTheDocument();
    expect(screen.getByText('↑ 10%')).toBeInTheDocument();
  });

  it('displays correct progress', () => {
    render(
      <ScoreHero score={60} totalModules={5} completedModules={3} url="https://voorbeeld.nl" />
    );

    expect(screen.getByText('3 van 5 modules')).toBeInTheDocument();
  });

  it('shows correct score label based on score', () => {
    const { rerender } = render(
      <ScoreHero score={85} totalModules={10} completedModules={8} url="https://voorbeeld.nl" />
    );
    expect(screen.getByText('Excellent')).toBeInTheDocument();

    rerender(
      <ScoreHero score={35} totalModules={10} completedModules={3} url="https://voorbeeld.nl" />
    );
    expect(screen.getByText('Actie Vereist')).toBeInTheDocument();
  });
});
