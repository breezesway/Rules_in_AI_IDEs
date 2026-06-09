export type BugSeverity = 'low' | 'medium' | 'high' | 'critical';
export type BugStatus = 'open' | 'in_progress' | 'resolved' | 'closed';

export interface Bug {
  id: number;
  projectId: number;
  title: string;
  description: string;
  severity: BugSeverity;
  status: BugStatus;
  createdAt: Date;
}

export interface CreateBugRequest {
  title: string;
  description: string;
  severity: BugSeverity;
  status: BugStatus;
}

export interface UpdateBugRequest {
  title?: string;
  description?: string;
  severity?: BugSeverity;
  status?: BugStatus;
}

export interface BugFilters {
  severity?: BugSeverity;
  status?: BugStatus;
  sortBy?: 'title' | 'severity' | 'status' | 'created_at';
  sortOrder?: 'ASC' | 'DESC';
}

export const BUG_SEVERITIES: BugSeverity[] = ['low', 'medium', 'high', 'critical'];
export const BUG_STATUSES: BugStatus[] = ['open', 'in_progress', 'resolved', 'closed'];