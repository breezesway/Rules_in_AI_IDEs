export type Impact = 'high' | 'medium' | 'low';
export type Status = 'success' | 'warning' | 'danger';
export type Layout = 'grid' | 'list';

export interface BaseAction {
  id: string;
  title: string;
  description: string;
  impact: Impact;
  moduleId: string;
}

export interface Action extends BaseAction {
  completedAt?: string;
}

export interface QuickWin extends BaseAction {
  impact: Impact;
  estimatedTime: string;
  code: string;
}

export interface Module {
  id: string;
  name: string;
  score: number;
  maxScore: number;
  status: Status;
  lastUpdated: string;
}

export interface CodeSnippet {
  id: string;
  language: string;
  code: string;
  description: string;
}

export interface AnalysisSection {
  id: string;
  title: string;
  description: string;
  codeSnippets: CodeSnippet[];
  currentScore: number;
  predictedScore: number;
}

export interface ModuleProgress {
  moduleId: string;
  totalActions: number;
  completedActions: number;
  lastUpdated: string;
}
