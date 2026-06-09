'use client';

import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Text,
} from 'recharts';
import { cn } from '@/lib/utils';
import { getStatusFromScore } from '@/lib/utils/scores';

interface ModuleScore {
  name: string;
  score: number;
  maxScore: number;
}

interface RadarChartProps {
  modules: ModuleScore[];
  className?: string;
  showLegend?: boolean;
}

// Helper functie voor scorepercentage berekening
export const calculateScorePercentage = (score: number, maxScore: number): number => {
  return Math.round((score / maxScore) * 100);
};

// Helper functie om kleur te bepalen op basis van status
export const getColorForStatus = (status: 'success' | 'warning' | 'danger'): string => {
  switch (status) {
    case 'success':
      return '#10b981'; // groen
    case 'warning':
      return '#f59e0b'; // oranje
    case 'danger':
      return '#ef4444'; // rood
    default:
      return '#3B82F6'; // blauw (fallback)
  }
};

// Aangepaste component voor betere tekstweergave
const CustomAxisTick = (props: any) => {
  const { x, y, payload, cx, cy } = props;

  // Bereken de hoek voor de tekst
  const angle = (Math.atan2(y - cy, x - cx) * 180) / Math.PI;

  // Bepaal de textAnchor op basis van de positie
  let textAnchor = x > cx ? 'start' : 'end';
  if (Math.abs(angle) > 80 && Math.abs(angle) < 100) {
    textAnchor = 'middle';
  }

  // Voeg padding toe voor betere leesbaarheid
  const xPadding = x > cx ? 8 : -8;
  const yPadding = Math.abs(angle) > 80 && Math.abs(angle) < 100 ? (y > cy ? 10 : -10) : 0;

  // Zorg dat naam intact blijft, geen verkorting
  const name = payload.value;

  // Bepaal de lettergrootte op basis van de naam lengte
  const fontSize = name.length > 15 ? '10' : '11';

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={xPadding}
        y={yPadding}
        textAnchor={textAnchor}
        fill="hsl(var(--foreground))"
        fontSize={fontSize}
        fontWeight="500"
        style={{ filter: 'drop-shadow(0px 0px 2px rgba(255, 255, 255, 0.9))' }}
      >
        {name}
      </text>
    </g>
  );
};

export function ModuleRadarChart({ modules, className, showLegend = true }: RadarChartProps) {
  // Bereken percentages voor de chart
  const data = modules.map(module => {
    const percentage = calculateScorePercentage(module.score, module.maxScore);
    const status = getStatusFromScore(percentage);

    return {
      name: module.name,
      score: percentage,
      status,
    };
  });

  // Bepaal de kleur op basis van het gemiddelde percentage
  const avgPercentage = data.reduce((sum, item) => sum + item.score, 0) / data.length;
  const overallStatus = getStatusFromScore(avgPercentage);
  const chartColor = getColorForStatus(overallStatus);

  return (
    <div className={cn('w-full', className)}>
      <div className="h-[500px]">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart
            cx="50%"
            cy="50%"
            outerRadius="70%"
            data={data}
            margin={{ top: 20, right: 30, bottom: 20, left: 30 }}
          >
            <PolarGrid stroke="hsl(var(--border))" strokeWidth={0.8} />
            <PolarAngleAxis dataKey="name" tick={<CustomAxisTick />} tickLine={false} />
            <PolarRadiusAxis
              angle={30}
              domain={[0, 100]}
              tick={{ fill: 'hsl(var(--foreground))', fontSize: 11 }}
              tickCount={5}
              stroke="hsl(var(--border))"
              strokeWidth={0.8}
            />
            <Radar
              name="Score"
              dataKey="score"
              stroke={chartColor}
              fill={chartColor}
              fillOpacity={0.7}
              strokeWidth={2}
              animationDuration={1000}
              animationEasing="ease-in-out"
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {showLegend && (
        <div className="mt-4 flex flex-wrap justify-center gap-4">
          <div className="flex items-center">
            <div
              className="w-4 h-4 mr-2 rounded-full"
              style={{ backgroundColor: getColorForStatus('success') }}
            />
            <span className="text-sm font-medium">Goed (≥80%)</span>
          </div>
          <div className="flex items-center">
            <div
              className="w-4 h-4 mr-2 rounded-full"
              style={{ backgroundColor: getColorForStatus('warning') }}
            />
            <span className="text-sm font-medium">Aandacht Nodig (40-79%)</span>
          </div>
          <div className="flex items-center">
            <div
              className="w-4 h-4 mr-2 rounded-full"
              style={{ backgroundColor: getColorForStatus('danger') }}
            />
            <span className="text-sm font-medium">Actie Vereist (&lt;40%)</span>
          </div>
        </div>
      )}
    </div>
  );
}
