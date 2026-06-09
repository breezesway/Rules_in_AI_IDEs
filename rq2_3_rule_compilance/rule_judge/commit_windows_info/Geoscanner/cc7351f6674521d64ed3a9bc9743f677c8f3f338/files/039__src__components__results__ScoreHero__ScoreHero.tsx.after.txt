import { motion } from 'framer-motion';
import { ScoreCircle } from '@/components/atoms/score-circle';
import { getStatusFromScore } from '@/lib/utils/scores';

export interface ScoreHeroProps {
  score: number;
  maxScore?: number;
  url: string;
  date?: string;
  previousScore?: number;
  totalModules?: number;
  completedModules?: number;
}

const getScoreLabel = (score: number): string => {
  if (score >= 80) return 'Excellent';
  if (score >= 60) return 'Goed';
  if (score >= 40) return 'Aandacht Nodig';
  return 'Actie Vereist';
};

const formatDate = (dateStr?: string): string => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('nl-NL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const ScoreHero = ({
  score,
  maxScore = 100,
  url,
  date,
  previousScore,
  totalModules,
  completedModules,
}: ScoreHeroProps) => {
  const scoreLabel = getScoreLabel(score);
  const formattedDate = formatDate(date);
  const status = getStatusFromScore(score);

  // Bepaal de tekstkleur op basis van status
  const textColorClasses = {
    success: 'text-green-600',
    warning: 'text-orange-600',
    danger: 'text-red-600',
  };

  return (
    <motion.div
      className="score-hero"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex flex-col items-center space-y-4">
        <div className="w-40 h-40">
          <ScoreCircle score={score} maxScore={maxScore} size="lg" />
        </div>

        <div className="text-center">
          <h2 className={`text-2xl font-bold ${textColorClasses[status]}`}>{scoreLabel}</h2>

          {previousScore !== undefined && (
            <p className="text-sm text-gray-600 mt-1">
              Vorige score: {previousScore}%
              {score > previousScore && (
                <span className="ml-2 text-green-600 font-medium">↑ {score - previousScore}%</span>
              )}
              {score < previousScore && (
                <span className="ml-2 text-red-600 font-medium">↓ {previousScore - score}%</span>
              )}
            </p>
          )}

          {totalModules !== undefined && completedModules !== undefined && (
            <p className="text-sm text-gray-600 mt-2">
              <span className="font-medium">
                {completedModules} van {totalModules} modules
              </span>
            </p>
          )}
        </div>

        <div className="text-center">
          <p className="text-sm font-medium text-gray-700">{url}</p>
          {date && <p className="text-xs text-gray-500 mt-1">Gescand op: {formattedDate}</p>}
        </div>
      </div>
    </motion.div>
  );
};
