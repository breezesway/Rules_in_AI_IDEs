'use client';

import { cn } from '@/lib/utils';
import { getStatusFromScore } from '@/lib/utils/scores';

interface ScoreCircleProps {
  score: number;
  maxScore: number;
  size?: 'sm' | 'md' | 'lg';
}

const sizeClasses = {
  sm: 'w-24 h-24',
  md: 'w-32 h-32',
  lg: 'w-40 h-40',
};

const textSizeClasses = {
  sm: 'text-2xl',
  md: 'text-3xl',
  lg: 'text-4xl',
};

// Kleurenpallet voor cirkel en tekst
const statusColorClasses = {
  stroke: {
    success: 'stroke-green-500',
    warning: 'stroke-orange-500',
    danger: 'stroke-red-500',
  },
  text: {
    success: 'text-green-600 font-bold',
    warning: 'text-orange-600 font-bold',
    danger: 'text-red-600 font-bold',
  },
  background: {
    success: 'stroke-green-100',
    warning: 'stroke-orange-100',
    danger: 'stroke-red-100',
  },
};

export function ScoreCircle({ score, maxScore, size = 'md' }: ScoreCircleProps) {
  const percentage = Math.round((score / maxScore) * 100);
  const circumference = 2 * Math.PI * 45; // radius = 45
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  // Bepaal status met dezelfde functie die in de rest van de app wordt gebruikt
  const status = getStatusFromScore(percentage);

  return (
    <div className={cn('relative', sizeClasses[size])}>
      <svg className="w-full h-full" viewBox="0 0 100 100">
        {/* Achtergrond cirkel - kleur afhankelijk van status maar lichter */}
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          strokeWidth="8"
          className={statusColorClasses.background[status]}
        />

        {/* Score cirkel - kleur op basis van status */}
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          transform="rotate(-90 50 50)"
          className={statusColorClasses.stroke[status]}
        />
      </svg>

      {/* Score tekst met kleur op basis van status */}
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className={cn(textSizeClasses[size], statusColorClasses.text[status])}>
          {percentage}
        </span>
        <span className="text-xs text-gray-500 font-medium">punten</span>
      </div>
    </div>
  );
}
