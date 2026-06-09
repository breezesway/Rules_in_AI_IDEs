'use client';

import { useState } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
  ComposedChart,
} from 'recharts';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

// Voorbeeld data structuur
export interface ScoreDataPoint {
  date: string;
  score: number;
  moduleId: string;
  moduleName: string;
  url?: string;
  scanId?: string;
}

interface InteractiveChartProps {
  data: ScoreDataPoint[];
  title?: string;
  className?: string;
}

type ChartType = 'line' | 'bar' | 'area' | 'composed';

export function InteractiveChart({
  data,
  title = 'Score Trend',
  className,
}: InteractiveChartProps) {
  const [chartType, setChartType] = useState<ChartType>('line');
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [timeRange, setTimeRange] = useState<string>('all');

  // Unieke modules extraheren uit data
  const modules = Array.from(new Set(data.map(item => item.moduleId))).map(moduleId => {
    const moduleData = data.find(item => item.moduleId === moduleId);
    return {
      id: moduleId,
      name: moduleData?.moduleName || moduleId,
    };
  });

  // Filter data op geselecteerde modules
  const filteredData = data.filter(
    item => selectedModules.length === 0 || selectedModules.includes(item.moduleId)
  );

  // Filter data op geselecteerde tijdsperiode
  const getTimeFilteredData = () => {
    if (timeRange === 'all') return filteredData;

    const now = new Date();
    const cutoffDate = new Date();

    switch (timeRange) {
      case 'week':
        cutoffDate.setDate(now.getDate() - 7);
        break;
      case 'month':
        cutoffDate.setMonth(now.getMonth() - 1);
        break;
      case 'quarter':
        cutoffDate.setMonth(now.getMonth() - 3);
        break;
      case 'year':
        cutoffDate.setFullYear(now.getFullYear() - 1);
        break;
      default:
        return filteredData;
    }

    return filteredData.filter(item => new Date(item.date) >= cutoffDate);
  };

  const timeFilteredData = getTimeFilteredData();

  // Sorteer data op datum
  const sortedData = [...timeFilteredData].sort(
    (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  // Genereert een unieke kleur voor elke module (simpel algoritme)
  const getModuleColor = (moduleId: string) => {
    const colors = [
      '#3498db', // Blauw
      '#2ecc71', // Groen
      '#e74c3c', // Rood
      '#f39c12', // Oranje
      '#9b59b6', // Paars
      '#1abc9c', // Turquoise
      '#34495e', // Donkerblauw
      '#7f8c8d', // Grijs
    ];

    // Hash functie voor moduleId om een consistente kleur te krijgen
    let hash = 0;
    for (let i = 0; i < moduleId.length; i++) {
      hash = moduleId.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
  };

  // Toggle module selection
  const toggleModule = (moduleId: string) => {
    setSelectedModules(prev =>
      prev.includes(moduleId) ? prev.filter(id => id !== moduleId) : [...prev, moduleId]
    );
  };

  // Group data by date and module for composed chart
  const groupDataByDate = () => {
    const groupedData: Record<string, any> = {};

    sortedData.forEach(item => {
      if (!groupedData[item.date]) {
        groupedData[item.date] = { date: item.date };
      }
      groupedData[item.date][item.moduleId] = item.score;
    });

    return Object.values(groupedData);
  };

  const groupedData = groupDataByDate();

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('nl-NL', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const renderChart = () => {
    switch (chartType) {
      case 'line':
        return (
          <LineChart data={sortedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={formatDate} />
            <YAxis domain={[0, 100]} />
            <Tooltip
              formatter={(value: number) => [`${value} punten`, 'Score']}
              labelFormatter={formatDate}
            />
            <Legend />
            {modules
              .filter(module => selectedModules.length === 0 || selectedModules.includes(module.id))
              .map(module => (
                <Line
                  key={module.id}
                  type="monotone"
                  dataKey="score"
                  data={sortedData.filter(item => item.moduleId === module.id)}
                  name={module.name}
                  stroke={getModuleColor(module.id)}
                  activeDot={{ r: 8 }}
                />
              ))}
          </LineChart>
        );

      case 'area':
        return (
          <AreaChart data={sortedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={formatDate} />
            <YAxis domain={[0, 100]} />
            <Tooltip
              formatter={(value: number) => [`${value} punten`, 'Score']}
              labelFormatter={formatDate}
            />
            <Legend />
            {modules
              .filter(module => selectedModules.length === 0 || selectedModules.includes(module.id))
              .map(module => (
                <Area
                  key={module.id}
                  type="monotone"
                  dataKey="score"
                  data={sortedData.filter(item => item.moduleId === module.id)}
                  name={module.name}
                  fill={getModuleColor(module.id)}
                  stroke={getModuleColor(module.id)}
                  fillOpacity={0.3}
                />
              ))}
          </AreaChart>
        );

      case 'bar':
        return (
          <BarChart data={sortedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={formatDate} />
            <YAxis domain={[0, 100]} />
            <Tooltip
              formatter={(value: number) => [`${value} punten`, 'Score']}
              labelFormatter={formatDate}
            />
            <Legend />
            {modules
              .filter(module => selectedModules.length === 0 || selectedModules.includes(module.id))
              .map(module => (
                <Bar
                  key={module.id}
                  dataKey="score"
                  data={sortedData.filter(item => item.moduleId === module.id) as any}
                  name={module.name}
                  fill={getModuleColor(module.id)}
                />
              ))}
          </BarChart>
        );

      case 'composed':
        return (
          <ComposedChart data={groupedData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" tickFormatter={formatDate} />
            <YAxis domain={[0, 100]} />
            <Tooltip
              formatter={(value: number) => [`${value} punten`, 'Score']}
              labelFormatter={formatDate}
            />
            <Legend />
            {modules
              .filter(module => selectedModules.length === 0 || selectedModules.includes(module.id))
              .map(module => (
                <Line
                  key={module.id}
                  type="monotone"
                  dataKey={module.id}
                  name={module.name}
                  stroke={getModuleColor(module.id)}
                  activeDot={{ r: 6 }}
                />
              ))}
          </ComposedChart>
        );

      default:
        return <div>Selecteer een grafiektype</div>;
    }
  };

  return (
    <Card className={cn('w-full', className)}>
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-bold">{title}</CardTitle>
        <div className="flex flex-wrap gap-2 mt-2">
          <div className="flex-1 min-w-[200px]">
            <Select value={chartType} onValueChange={(value: ChartType) => setChartType(value)}>
              <SelectTrigger>
                <SelectValue placeholder="Grafiek type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="line">Lijngrafiek</SelectItem>
                <SelectItem value="area">Gebiedsgrafiek</SelectItem>
                <SelectItem value="bar">Staafdiagram</SelectItem>
                <SelectItem value="composed">Gecombineerd</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="flex-1 min-w-[200px]">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger>
                <SelectValue placeholder="Tijdsperiode" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Alle data</SelectItem>
                <SelectItem value="week">Laatste week</SelectItem>
                <SelectItem value="month">Laatste maand</SelectItem>
                <SelectItem value="quarter">Laatste kwartaal</SelectItem>
                <SelectItem value="year">Laatste jaar</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="mb-4 flex flex-wrap gap-2">
          {modules.map(module => (
            <Button
              key={module.id}
              variant={selectedModules.includes(module.id) ? 'default' : 'outline'}
              onClick={() => toggleModule(module.id)}
              className="text-xs h-7"
            >
              <span
                className="mr-2 inline-block w-3 h-3 rounded-full"
                style={{ backgroundColor: getModuleColor(module.id) }}
              ></span>
              {module.name}
            </Button>
          ))}
        </div>
        <div className="h-[400px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
