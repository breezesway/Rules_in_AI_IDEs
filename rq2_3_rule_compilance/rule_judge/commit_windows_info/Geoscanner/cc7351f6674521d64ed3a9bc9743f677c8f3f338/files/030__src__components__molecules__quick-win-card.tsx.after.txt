'use client';

import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface QuickWinCardProps {
  module: string;
  impact: 'high' | 'medium' | 'low';
  description: string;
  fix: string;
}

const impactColors = {
  high: 'bg-danger-red/10 text-danger-red',
  medium: 'bg-warning-amber/10 text-warning-amber',
  low: 'bg-success-green/10 text-success-green',
};

const impactLabels = {
  high: 'Hoog',
  medium: 'Gemiddeld',
  low: 'Laag',
};

export function QuickWinCard({ module, impact, description, fix }: QuickWinCardProps) {
  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <Badge variant="outline" className={cn(impactColors[impact])}>
              {impactLabels[impact]}
            </Badge>
            <span className="text-sm text-muted-foreground">{module}</span>
          </div>
        </div>

        <p className="text-sm mb-4">{description}</p>

        <div className="bg-muted p-3 rounded-md">
          <pre className="text-sm overflow-x-auto">
            <code>{fix}</code>
          </pre>
        </div>
      </CardContent>
    </Card>
  );
}
