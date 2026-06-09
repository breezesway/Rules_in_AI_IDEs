'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/skeleton';
import { ModuleOverview } from '@/components/results/ModuleOverview/ModuleOverview';
import { ScoreHero } from '@/components/results/ScoreHero/ScoreHero';
import { QuickWinsPanel } from '@/components/results/QuickWinsPanel/QuickWinsPanel';
import { DetailedAnalysis } from '@/components/results/DetailedAnalysis/DetailedAnalysis';
import { InteractiveChart } from '@/components/molecules/interactive-chart';
import { ComparativeAnalysis } from '@/components/molecules/comparative-analysis';
import { fetchScanResult } from '@/lib/utils/api';
import { fetchScanHistory } from '@/lib/utils/api';
import { useFeatureFlag } from '@/hooks/use-feature-flag';

export default function ScanDetailPage() {
  const { scanId } = useParams<{ scanId: string }>();
  const [loading, setLoading] = useState(true);
  const [scanResult, setScanResult] = useState<any>(null);
  const [scanHistory, setScanHistory] = useState<any[]>([]);
  const [scoreHistory, setScoreHistory] = useState<any[]>([]);
  const showEnhancedUI = useFeatureFlag('enhancedUI');

  useEffect(() => {
    async function loadScanData() {
      try {
        setLoading(true);
        const result = await fetchScanResult(scanId as string);
        setScanResult(result);

        // Haal scangeschiedenis op
        const history = await fetchScanHistory(result.url);
        setScanHistory(history);

        // Genereer scoregeschiedenis data voor de grafiek
        const scoreData = [];
        for (const scan of history) {
          const date = new Date(scan.date).toISOString();

          // Voeg totale score toe
          scoreData.push({
            date,
            score: scan.overallScore,
            moduleId: 'overall',
            moduleName: 'Totale Score',
          });

          // Voeg individuele module scores toe
          for (const module of scan.modules) {
            scoreData.push({
              date,
              score: module.score,
              moduleId: module.id,
              moduleName: module.name,
              scanId: scan.id,
            });
          }
        }
        setScoreHistory(scoreData);
      } catch (error) {
        console.error('Fout bij het laden van scan resultaat:', error);
      } finally {
        setLoading(false);
      }
    }

    if (scanId) {
      loadScanData();
    }
  }, [scanId]);

  if (loading) {
    return (
      <div className="container mx-auto py-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1">
            <Skeleton className="h-64 w-full rounded-lg" />
          </div>
          <div className="md:col-span-2">
            <Skeleton className="h-64 w-full rounded-lg" />
          </div>
        </div>
        <Skeleton className="h-48 w-full rounded-lg" />
        <Skeleton className="h-96 w-full rounded-lg" />
      </div>
    );
  }

  if (!scanResult) {
    return (
      <div className="container mx-auto py-8">
        <h1 className="text-2xl font-bold mb-4">Scan niet gevonden</h1>
        <p>
          De opgevraagde scan kon niet worden gevonden. Controleer het scanID of probeer een nieuwe
          scan uit te voeren.
        </p>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <ScoreHero score={scanResult.overallScore} url={scanResult.url} date={scanResult.date} />
        </div>
        <div className="md:col-span-2">
          <ModuleOverview modules={scanResult.modules} />
        </div>
      </div>

      <QuickWinsPanel quickWins={scanResult.quickWins} />

      <Tabs defaultValue="detailed" className="w-full">
        <TabsList>
          <TabsTrigger value="detailed">Gedetailleerde Analyse</TabsTrigger>
          <TabsTrigger value="history">Score Geschiedenis</TabsTrigger>
          <TabsTrigger value="comparison">Vergelijkende Analyse</TabsTrigger>
        </TabsList>

        <TabsContent value="detailed" className="mt-4">
          <DetailedAnalysis
            sections={scanResult.modules.map((module: any) => ({
              id: module.id,
              title: module.name,
              description: `Analyse van de ${module.name.toLowerCase()} aspecten van je website.`,
              codeSnippets:
                module.fixes?.map((fix: any) => ({
                  code: fix.fix,
                  language: 'html',
                  title: fix.description,
                })) || [],
              currentScore: Math.round((module.score / module.maxScore) * 100),
              predictedScore: Math.min(
                100,
                Math.round((module.score / module.maxScore) * 100) + 15
              ),
            }))}
          />
        </TabsContent>

        <TabsContent value="history" className="mt-4">
          <InteractiveChart data={scoreHistory} title="Score Verloop" />
        </TabsContent>

        <TabsContent value="comparison" className="mt-4">
          <ComparativeAnalysis scans={scanHistory} primaryScanId={scanId as string} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
