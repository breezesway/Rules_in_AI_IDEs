'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowUp, ArrowDown, Minus, TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { ScoreCircle } from '@/components/atoms/score-circle';
import { cn } from '@/lib/utils';
import { getStatusFromScore } from '@/lib/utils/scores';

// Type definities
export interface ModuleScore {
  id: string;
  name: string;
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
}

export interface ScanResult {
  id: string;
  url: string;
  date: string;
  overallScore: number;
  modules: ModuleScore[];
}

interface ComparativeAnalysisProps {
  scans: ScanResult[];
  primaryScanId?: string;
  className?: string;
}

// Helper functie om status naar variant om te zetten
const getVariantFromStatus = (
  status: 'success' | 'warning' | 'danger'
): 'default' | 'secondary' | 'destructive' => {
  switch (status) {
    case 'success':
      return 'default';
    case 'warning':
      return 'secondary';
    case 'danger':
      return 'destructive';
    default:
      return 'default';
  }
};

// Helper functie om score percentage te berekenen en status te bepalen
// const calculateStatus = (score: number, maxScore: number) => { // Commented out as it's unused
// const percentage = Math.round((score / maxScore) * 100);
// return getStatusFromScore(percentage);
// };

export function ComparativeAnalysis({ scans, primaryScanId, className }: ComparativeAnalysisProps) {
  // Als er geen primaryScanId is opgegeven, gebruik de meest recente scan
  const [selectedPrimaryScanId, setSelectedPrimaryScanId] = useState<string>(
    primaryScanId || (scans.length > 0 ? scans[0].id : '')
  );
  const [selectedComparisonScanId, setSelectedComparisonScanId] = useState<string>(
    scans.length > 1 ? scans[1].id : ''
  );

  if (scans.length === 0) {
    return (
      <Card className={className}>
        <CardContent className="pt-6">
          <p className="text-center text-muted-foreground">
            Geen scan gegevens beschikbaar voor vergelijking.
          </p>
        </CardContent>
      </Card>
    );
  }

  // De geselecteerde scans ophalen
  const primaryScan = scans.find(scan => scan.id === selectedPrimaryScanId) || scans[0];
  const comparisonScan = scans.find(scan => scan.id === selectedComparisonScanId);

  // Functie om het verschil tussen twee scores te berekenen
  const calculateDifference = (current: number, previous: number | undefined) => {
    if (previous === undefined) return { value: 0, isPositive: false, percentage: 0 };
    const diff = current - previous;
    const percentage = previous !== 0 ? Math.round((diff / previous) * 100) : 0;
    return {
      value: diff,
      isPositive: diff > 0,
      percentage,
    };
  };

  // Functie om kleur op basis van verschil te bepalen
  const getComparisonColor = (diff: number) => {
    if (diff > 0) return 'text-green-600';
    if (diff < 0) return 'text-red-600';
    return 'text-gray-500';
  };

  // Functie om icoon op basis van verschil te bepalen
  const getComparisonIcon = (diff: number) => {
    if (diff > 0) return <ArrowUp className="h-4 w-4 text-green-600" />;
    if (diff < 0) return <ArrowDown className="h-4 w-4 text-red-600" />;
    return <Minus className="h-4 w-4 text-gray-500" />;
  };

  // Functie om de trend te bepalen
  const getTrendIcon = (diff: number) => {
    if (diff > 0) return <TrendingUp className="h-5 w-5 text-green-600" />;
    if (diff < 0) return <TrendingDown className="h-5 w-5 text-red-600" />;
    return <ArrowRight className="h-5 w-5 text-gray-500" />;
  };

  // Datums formatteren
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('nl-NL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  // Voor elk moduleId in primaryScan, vind de overeenkomstige module in comparisonScan
  const moduleComparisons = primaryScan.modules.map(module => {
    const comparisonModule = comparisonScan?.modules.find(m => m.id === module.id);
    const difference = calculateDifference(module.score, comparisonModule?.score);

    return {
      ...module,
      comparisonScore: comparisonModule?.score,
      difference,
    };
  });

  // Bereken het totale verschil
  const overallDifference = calculateDifference(
    primaryScan.overallScore,
    comparisonScan?.overallScore
  );

  return (
    <Card className={cn('w-full', className)}>
      <CardHeader>
        <CardTitle className="text-xl font-bold">Vergelijkende Analyse</CardTitle>
        <CardDescription>Vergelijk scan resultaten om voortgang te zien</CardDescription>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">Primaire Scan</label>
            <Select value={selectedPrimaryScanId} onValueChange={setSelectedPrimaryScanId}>
              <SelectTrigger>
                <SelectValue placeholder="Selecteer scan" />
              </SelectTrigger>
              <SelectContent>
                {scans.map(scan => (
                  <SelectItem key={scan.id} value={scan.id}>
                    {scan.url} ({formatDate(scan.date)})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700 mb-1 block">Vergelijking met</label>
            <Select value={selectedComparisonScanId} onValueChange={setSelectedComparisonScanId}>
              <SelectTrigger>
                <SelectValue placeholder="Selecteer scan voor vergelijking" />
              </SelectTrigger>
              <SelectContent>
                {scans
                  .filter(scan => scan.id !== selectedPrimaryScanId)
                  .map(scan => (
                    <SelectItem key={scan.id} value={scan.id}>
                      {scan.url} ({formatDate(scan.date)})
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <Tabs defaultValue="overview">
          <TabsList className="mb-4">
            <TabsTrigger value="overview">Overzicht</TabsTrigger>
            <TabsTrigger value="modules">Per Module</TabsTrigger>
            <TabsTrigger value="trends">Trends</TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex flex-col items-center justify-center p-6 bg-gray-50 rounded-lg">
                <p className="text-sm font-medium text-gray-700 mb-1">{primaryScan.url}</p>
                <p className="text-xs text-gray-500 mb-4">{formatDate(primaryScan.date)}</p>
                <ScoreCircle score={primaryScan.overallScore} maxScore={100} size="lg" />
              </div>

              {comparisonScan && (
                <div className="flex flex-col items-center justify-center p-6 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-2 mb-1">
                    <p className="text-sm font-medium text-gray-700">
                      Verschil t.o.v. {formatDate(comparisonScan.date)}
                    </p>
                    {getTrendIcon(overallDifference.value)}
                  </div>
                  <div
                    className={cn(
                      'text-2xl font-bold mb-4',
                      getComparisonColor(overallDifference.value)
                    )}
                  >
                    {overallDifference.value > 0 ? '+' : ''}
                    {overallDifference.value} punten
                  </div>
                  <div className="flex items-center space-x-8">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Vorige score</p>
                      <p className="text-xl font-semibold">{comparisonScan.overallScore}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Huidige score</p>
                      <p className="text-xl font-semibold">{primaryScan.overallScore}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="modules">
            <div className="space-y-4">
              {moduleComparisons.map(module => (
                <div key={module.id} className="p-4 border rounded-lg">
                  <div className="flex justify-between items-center">
                    <h3 className="font-medium text-lg">{module.name}</h3>
                    <Badge variant={getVariantFromStatus(module.status)}>
                      {module.score}/{module.maxScore}
                    </Badge>
                  </div>

                  {comparisonScan && (
                    <div className="mt-3">
                      <div className="flex items-center space-x-2">
                        <div
                          className={cn(
                            'flex items-center',
                            getComparisonColor(module.difference.value)
                          )}
                        >
                          {getComparisonIcon(module.difference.value)}
                          <span className="ml-1">
                            {module.difference.value > 0 ? '+' : ''}
                            {module.difference.value} punten
                          </span>
                        </div>
                        <span className="text-xs text-gray-500">
                          {module.comparisonScore !== undefined &&
                            `(${module.comparisonScore} → ${module.score})`}
                        </span>
                      </div>
                    </div>
                  )}

                  <div className="mt-2 bg-gray-100 h-2 rounded-full overflow-hidden">
                    <div
                      className={cn(
                        'h-full rounded-full',
                        getVariantFromStatus(module.status) === 'default'
                          ? 'bg-green-500'
                          : getVariantFromStatus(module.status) === 'secondary'
                            ? 'bg-amber-500'
                            : 'bg-red-500'
                      )}
                      style={{ width: `${(module.score / module.maxScore) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="trends">
            {comparisonScan ? (
              <div className="space-y-4">
                <p className="text-sm text-gray-700">
                  Resultaten van {formatDate(comparisonScan.date)} vergeleken met{' '}
                  {formatDate(primaryScan.date)}
                </p>

                {/* Verbeterde modules */}
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium text-green-600 mb-2">Verbeterde Modules</h3>
                  {moduleComparisons.filter(m => m.difference.value > 0).length > 0 ? (
                    <div className="space-y-2">
                      {moduleComparisons
                        .filter(m => m.difference.value > 0)
                        .sort((a, b) => b.difference.value - a.difference.value)
                        .map(module => (
                          <div
                            key={module.id}
                            className="flex justify-between items-center p-2 bg-green-50 rounded"
                          >
                            <span>{module.name}</span>
                            <span className="text-green-600 font-medium">
                              +{module.difference.value} punten
                            </span>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Geen verbeteringen gevonden</p>
                  )}
                </div>

                {/* Verslechterde modules */}
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium text-red-600 mb-2">Verslechterde Modules</h3>
                  {moduleComparisons.filter(m => m.difference.value < 0).length > 0 ? (
                    <div className="space-y-2">
                      {moduleComparisons
                        .filter(m => m.difference.value < 0)
                        .sort((a, b) => a.difference.value - b.difference.value)
                        .map(module => (
                          <div
                            key={module.id}
                            className="flex justify-between items-center p-2 bg-red-50 rounded"
                          >
                            <span>{module.name}</span>
                            <span className="text-red-600 font-medium">
                              {module.difference.value} punten
                            </span>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Geen verslechteringen gevonden</p>
                  )}
                </div>

                {/* Ongewijzigde modules */}
                <div className="p-4 border rounded-lg">
                  <h3 className="font-medium text-gray-600 mb-2">Ongewijzigde Modules</h3>
                  {moduleComparisons.filter(m => m.difference.value === 0).length > 0 ? (
                    <div className="space-y-2">
                      {moduleComparisons
                        .filter(m => m.difference.value === 0)
                        .map(module => (
                          <div
                            key={module.id}
                            className="flex justify-between items-center p-2 bg-gray-50 rounded"
                          >
                            <span>{module.name}</span>
                            <span className="text-gray-600 font-medium">{module.score} punten</span>
                          </div>
                        ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500">Geen ongewijzigde modules gevonden</p>
                  )}
                </div>
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-4">
                Selecteer een scan om mee te vergelijken om trends te zien.
              </p>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
