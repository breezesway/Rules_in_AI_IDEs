import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, ChevronDown, ChevronUp } from 'lucide-react';
import { AnalysisSection } from '@/lib/types/results';
import { useClipboard } from '@/lib/utils/clipboard';
import { calculateScoreImprovement } from '@/lib/utils/scores';

interface DetailedAnalysisProps {
  sections: AnalysisSection[];
}

export const DetailedAnalysis = ({ sections }: DetailedAnalysisProps) => {
  const [expandedSections, setExpandedSections] = useState<string[]>([]);
  const { copyToClipboard, isCopied } = useClipboard();

  const toggleSection = (sectionId: string) => {
    setExpandedSections(prev =>
      prev.includes(sectionId) ? prev.filter(id => id !== sectionId) : [...prev, sectionId]
    );
  };

  return (
    <div className="space-y-6">
      {sections.map(section => (
        <motion.div
          key={section.id}
          className="bg-white rounded-lg shadow-md overflow-hidden"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <button
            className="w-full px-6 py-4 flex justify-between items-center hover:bg-gray-50"
            onClick={() => toggleSection(section.id)}
          >
            <div className="flex-1 text-left">
              <h3 className="text-lg font-semibold text-gray-900">{section.title}</h3>
              <p className="text-sm text-gray-600 mt-1">{section.description}</p>
            </div>
            {expandedSections.includes(section.id) ? (
              <ChevronUp className="h-5 w-5 text-gray-500" />
            ) : (
              <ChevronDown className="h-5 w-5 text-gray-500" />
            )}
          </button>

          <AnimatePresence>
            {expandedSections.includes(section.id) && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="px-6 pb-4"
              >
                <div className="space-y-4">
                  {section.codeSnippets.map(snippet => (
                    <div key={snippet.id} className="relative">
                      <div className="flex justify-between items-center mb-2">
                        <p className="text-sm text-gray-700">{snippet.description}</p>
                        <button
                          onClick={() => copyToClipboard(snippet.id, snippet.code)}
                          className="p-2 text-gray-500 hover:text-gray-700"
                        >
                          {isCopied(snippet.id) ? (
                            <span className="text-green-500">Gekopieerd!</span>
                          ) : (
                            <Copy className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                      <SyntaxHighlighter
                        language={snippet.language}
                        style={vscDarkPlus}
                        className="rounded-md"
                      >
                        {snippet.code}
                      </SyntaxHighlighter>
                    </div>
                  ))}

                  <div className="mt-4 p-4 bg-gray-50 rounded-md">
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Score Voorspelling</h4>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-gray-600">Huidige Score</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {section.currentScore}%
                        </p>
                      </div>
                      <div className="text-center">
                        <p className="text-sm text-gray-600">Voorspelde Verbetering</p>
                        <p
                          className={`text-lg font-semibold ${
                            calculateScoreImprovement(section.currentScore, section.predictedScore)
                              .isPositive
                              ? 'text-green-600'
                              : 'text-red-600'
                          }`}
                        >
                          {calculateScoreImprovement(section.currentScore, section.predictedScore)
                            .isPositive
                            ? '+'
                            : '-'}
                          {
                            calculateScoreImprovement(section.currentScore, section.predictedScore)
                              .percentage
                          }
                          %
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Voorspelde Score</p>
                        <p className="text-lg font-semibold text-gray-900">
                          {section.predictedScore}%
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      ))}
    </div>
  );
};
