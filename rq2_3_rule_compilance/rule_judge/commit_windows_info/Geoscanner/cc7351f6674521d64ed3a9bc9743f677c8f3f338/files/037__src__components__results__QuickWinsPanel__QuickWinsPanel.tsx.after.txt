import { useState } from 'react';
import { motion } from 'framer-motion';
import { Copy, Check } from 'lucide-react';
import { QuickWin } from '@/lib/types/results';
import { useClipboard } from '@/lib/utils/clipboard';
import { getStatusColor, getImpactColor } from '@/lib/utils/scores';

interface QuickWinsPanelProps {
  quickWins: QuickWin[];
}

export const QuickWinsPanel = ({ quickWins }: QuickWinsPanelProps) => {
  const [selectedQuickWin, setSelectedQuickWin] = useState<string | null>(null);
  const { copyToClipboard, isCopied } = useClipboard();

  const toggleQuickWin = (id: string) => {
    setSelectedQuickWin(prev => (prev === id ? null : id));
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Wins</h2>
      <div className="space-y-4">
        {quickWins.map(quickWin => (
          <motion.div
            key={quickWin.id}
            className="border rounded-lg p-4 hover:shadow-md transition-shadow"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={{ scale: 1.02 }}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1 cursor-pointer" onClick={() => toggleQuickWin(quickWin.id)}>
                <h3 className="text-lg font-medium text-gray-900">{quickWin.title}</h3>
                <p className="text-sm text-gray-600 mt-1">{quickWin.description}</p>
                <div className="mt-2 flex items-center space-x-2">
                  <span
                    className={`px-2 py-1 rounded-full text-xs font-medium ${getImpactColor(
                      quickWin.impact
                    )}`}
                  >
                    {quickWin.impact}
                  </span>
                  <span className="text-sm text-gray-500">
                    Geschatte tijd: {quickWin.estimatedTime}
                  </span>
                </div>
              </div>
              <button
                onClick={e => {
                  e.stopPropagation();
                  copyToClipboard(quickWin.id, quickWin.code);
                }}
                className="p-2 text-gray-500 hover:text-gray-700"
              >
                {isCopied(quickWin.id) ? (
                  <Check className="h-5 w-5 text-green-500" />
                ) : (
                  <Copy className="h-5 w-5" />
                )}
              </button>
            </div>
            {selectedQuickWin === quickWin.id && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-4"
              >
                <pre className="bg-gray-50 p-4 rounded-md overflow-x-auto">
                  <code>{quickWin.code}</code>
                </pre>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};
