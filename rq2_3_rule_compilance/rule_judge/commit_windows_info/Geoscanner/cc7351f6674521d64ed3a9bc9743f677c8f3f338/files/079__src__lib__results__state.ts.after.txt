import { create, StateCreator } from 'zustand';
import { persist, PersistOptions } from 'zustand/middleware';

interface ResultsState {
  completedActions: string[];
  expandedModules: string[];
  copiedSnippets: string[];
  layout: 'grid' | 'list';
  addCompletedAction: (actionId: string) => void;
  removeCompletedAction: (actionId: string) => void;
  toggleModuleExpansion: (moduleId: string) => void;
  addCopiedSnippet: (snippetId: string) => void;
  removeCopiedSnippet: (snippetId: string) => void;
  setLayout: (layout: 'grid' | 'list') => void;
}

type ResultsStore = StateCreator<ResultsState>;

export const useResultsStore = create<ResultsState>()(
  persist(
    (set => ({
      completedActions: [],
      expandedModules: [],
      copiedSnippets: [],
      layout: 'grid',

      addCompletedAction: (actionId: string) =>
        set((state: ResultsState) => ({
          completedActions: [...state.completedActions, actionId],
        })),

      removeCompletedAction: (actionId: string) =>
        set((state: ResultsState) => ({
          completedActions: state.completedActions.filter((id: string) => id !== actionId),
        })),

      toggleModuleExpansion: (moduleId: string) =>
        set((state: ResultsState) => ({
          expandedModules: state.expandedModules.includes(moduleId)
            ? state.expandedModules.filter((id: string) => id !== moduleId)
            : [...state.expandedModules, moduleId],
        })),

      addCopiedSnippet: (snippetId: string) =>
        set((state: ResultsState) => ({
          copiedSnippets: [...state.copiedSnippets, snippetId],
        })),

      removeCopiedSnippet: (snippetId: string) =>
        set((state: ResultsState) => ({
          copiedSnippets: state.copiedSnippets.filter((id: string) => id !== snippetId),
        })),

      setLayout: (layout: 'grid' | 'list') =>
        set(() => ({
          layout,
        })),
    })) as ResultsStore,
    {
      name: 'geo-scanner-results',
      partialize: (state: ResultsState) => ({
        completedActions: state.completedActions,
        expandedModules: state.expandedModules,
        layout: state.layout,
      }),
    } as PersistOptions<ResultsState>
  )
);
