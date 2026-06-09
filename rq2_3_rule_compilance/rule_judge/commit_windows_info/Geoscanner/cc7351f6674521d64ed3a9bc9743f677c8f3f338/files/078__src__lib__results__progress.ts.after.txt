import { useResultsStore } from './state';

export interface Action {
  id: string;
  title: string;
  description: string;
  impact: 'high' | 'medium' | 'low';
  moduleId: string;
  completedAt?: string;
}

export interface ModuleProgress {
  moduleId: string;
  totalActions: number;
  completedActions: number;
  lastUpdated: string;
}

export const useProgress = () => {
  const { completedActions, addCompletedAction, removeCompletedAction } = useResultsStore();

  const markActionAsCompleted = (actionId: string) => {
    addCompletedAction(actionId);
  };

  const markActionAsIncomplete = (actionId: string) => {
    removeCompletedAction(actionId);
  };

  const isActionCompleted = (actionId: string) => {
    return completedActions.includes(actionId);
  };

  const calculateModuleProgress = (actions: Action[], moduleId: string): ModuleProgress => {
    const moduleActions = actions.filter(action => action.moduleId === moduleId);
    const completedModuleActions = moduleActions.filter(action =>
      completedActions.includes(action.id)
    );

    return {
      moduleId,
      totalActions: moduleActions.length,
      completedActions: completedModuleActions.length,
      lastUpdated: new Date().toISOString(),
    };
  };

  const calculateOverallProgress = (actions: Action[]): number => {
    if (actions.length === 0) return 0;
    const completedCount = actions.filter(action => completedActions.includes(action.id)).length;
    return Math.round((completedCount / actions.length) * 100);
  };

  const getCompletedActions = (actions: Action[]): Action[] => {
    return actions.filter(action => completedActions.includes(action.id));
  };

  const getIncompleteActions = (actions: Action[]): Action[] => {
    return actions.filter(action => !completedActions.includes(action.id));
  };

  const exportProgress = (actions: Action[]): string => {
    const progress = {
      completedActions: getCompletedActions(actions).map(action => ({
        id: action.id,
        title: action.title,
        moduleId: action.moduleId,
        completedAt: new Date().toISOString(),
      })),
      overallProgress: calculateOverallProgress(actions),
      exportDate: new Date().toISOString(),
    };

    return JSON.stringify(progress, null, 2);
  };

  return {
    markActionAsCompleted,
    markActionAsIncomplete,
    isActionCompleted,
    calculateModuleProgress,
    calculateOverallProgress,
    getCompletedActions,
    getIncompleteActions,
    exportProgress,
  };
};
