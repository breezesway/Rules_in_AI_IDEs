export interface Project {
  id: number;
  name: string;
  createdAt: Date;
}

export interface CreateProjectRequest {
  name: string;
}

export interface ProjectWithBugCount extends Project {
  bugCount: number;
}