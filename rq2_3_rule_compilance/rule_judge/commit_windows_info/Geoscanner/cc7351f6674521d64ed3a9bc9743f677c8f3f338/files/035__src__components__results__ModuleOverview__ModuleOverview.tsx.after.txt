import { motion } from 'framer-motion';
import { Module } from '@/lib/types/results';
import { getStatusColor, getStatusLabel, getStatusFromScore } from '@/lib/utils/scores';
import { ModuleRadarChart } from '@/components/molecules/radar-chart';

// Lokale implementatie van formatDate functie
const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('nl-NL', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
};

// Helper functie om achtergrondkleur te bepalen op basis van status
const getProgressBarColor = (status: 'success' | 'warning' | 'danger'): string => {
  switch (status) {
    case 'success':
      return 'bg-green-500';
    case 'warning':
      return 'bg-orange-500';
    case 'danger':
      return 'bg-red-500';
    default:
      return 'bg-blue-500';
  }
};

interface ModuleOverviewProps {
  modules: Module[];
  layout?: 'grid' | 'list';
}

export const ModuleOverview = ({ modules, layout = 'grid' }: ModuleOverviewProps) => {
  return (
    <motion.div
      className="module-overview"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-900">Module Overzicht</h2>
        <div className="flex space-x-2">
          <button
            className={`px-3 py-1 rounded-md ${
              layout === 'grid' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
            onClick={() =>
              layout === 'list' &&
              window.dispatchEvent(new CustomEvent('change-layout', { detail: 'grid' }))
            }
          >
            Grid
          </button>
          <button
            className={`px-3 py-1 rounded-md ${
              layout === 'list' ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'
            }`}
            onClick={() =>
              layout === 'grid' &&
              window.dispatchEvent(new CustomEvent('change-layout', { detail: 'list' }))
            }
          >
            Lijst
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {modules.map(module => {
          // Bereken percentage score en bepaal status op basis daarvan
          const percentageScore = Math.round((module.score / module.maxScore) * 100);
          const calculatedStatus = getStatusFromScore(percentageScore);
          const progressBarColor = getProgressBarColor(calculatedStatus);

          return (
            <motion.div
              key={module.id}
              className="module-card bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3 }}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-gray-900">{module.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Laatste update: {formatDate(module.lastUpdated)}
                  </p>
                </div>
                <span
                  className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                    calculatedStatus
                  )}`}
                >
                  {getStatusLabel(calculatedStatus)}
                </span>
              </div>
              <div className="mt-4">
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">Score</span>
                  <span className="font-bold">{percentageScore}%</span>
                </div>
                <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full ${progressBarColor}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${percentageScore}%` }}
                    transition={{ duration: 1, ease: 'easeOut' }}
                  />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Module Prestaties</h3>
        <div className="bg-white p-4 rounded-lg shadow border border-gray-100">
          <ModuleRadarChart modules={modules} />
        </div>
      </div>
    </motion.div>
  );
};
