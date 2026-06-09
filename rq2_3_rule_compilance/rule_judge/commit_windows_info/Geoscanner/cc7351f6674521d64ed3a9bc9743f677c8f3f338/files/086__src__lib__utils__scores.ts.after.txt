import { Status, Impact } from '@/lib/types/results';

export const calculateScoreImprovement = (current: number, predicted: number) => {
  const improvement = predicted - current;
  return {
    value: improvement,
    isPositive: improvement > 0,
    percentage: Math.abs(Math.round((improvement / current) * 100)),
  };
};

export const calculateModuleProgress = (totalActions: number, completedActions: number): number => {
  if (totalActions === 0) return 0;
  return Math.round((completedActions / totalActions) * 100);
};

export const getStatusFromScore = (score: number): 'success' | 'warning' | 'danger' => {
  if (score >= 80) return 'success';
  if (score >= 40) return 'warning';
  return 'danger';
};

export const getStatusColor = (status: Status): string => {
  switch (status) {
    case 'success':
      return 'bg-green-100 text-green-800';
    case 'warning':
      return 'bg-orange-100 text-orange-800';
    case 'danger':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

export const getImpactColor = (impact: Impact): string => {
  switch (impact) {
    case 'high':
      return 'bg-green-100 text-green-800'; // High impact is positief
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'; // Medium impact als attentie
    case 'low':
      return 'bg-blue-100 text-blue-800'; // Low impact als informatief
    default:
      // In case of an unknown impact, provide a fallback style
      const exhaustiveCheck: never = impact;
      return 'bg-gray-100 text-gray-800';
  }
};

export const getStatusLabel = (status: Status): string => {
  switch (status) {
    case 'success':
      return 'Goed';
    case 'warning':
      return 'Aandacht Nodig';
    case 'danger':
      return 'Actie Vereist';
    default:
      return 'Onbekend';
  }
};
