'use client';

import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { Badge } from '@/components/ui/badge';

interface ModuleCardProps {
  module: {
    id: string;
    name: string;
    score: number;
    maxScore: number;
    status: 'success' | 'warning' | 'danger';
  };
}

const statusColors = {
  success: 'bg-success-green/10 text-success-green',
  warning: 'bg-warning-amber/10 text-warning-amber',
  danger: 'bg-danger-red/10 text-danger-red',
};

const statusIcons = {
  success: '✅',
  warning: '⚠️',
  danger: '❌',
};

export function ModuleCard({ module }: ModuleCardProps) {
  const percentage = (module.score / module.maxScore) * 100;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-medium">{module.name}</h3>
          <Badge variant="outline" className={cn(statusColors[module.status])}>
            {statusIcons[module.status]}
          </Badge>
        </div>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            Score: {module.score}/{module.maxScore}
          </div>
          <div className={cn('text-sm font-medium', statusColors[module.status])}>
            {Math.round(percentage)}%
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
