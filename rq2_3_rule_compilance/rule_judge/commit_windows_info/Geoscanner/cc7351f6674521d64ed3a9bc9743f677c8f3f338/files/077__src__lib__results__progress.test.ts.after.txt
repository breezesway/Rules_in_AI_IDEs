import { renderHook, act } from '@testing-library/react';
import { useProgress } from './progress';
import { useResultsStore } from './state';

const mockActions = [
  {
    id: 'action1',
    title: 'Test Action 1',
    description: 'Test Description 1',
    impact: 'high' as const,
    moduleId: 'module1',
  },
  {
    id: 'action2',
    title: 'Test Action 2',
    description: 'Test Description 2',
    impact: 'medium' as const,
    moduleId: 'module1',
  },
  {
    id: 'action3',
    title: 'Test Action 3',
    description: 'Test Description 3',
    impact: 'low' as const,
    moduleId: 'module2',
  },
];

describe('useProgress', () => {
  beforeEach(() => {
    const { result } = renderHook(() => useResultsStore());
    act(() => {
      result.current.completedActions = [];
    });
  });

  it('should mark action as completed', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
    });

    expect(result.current.isActionCompleted('action1')).toBe(true);
  });

  it('should mark action as incomplete', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
      result.current.markActionAsIncomplete('action1');
    });

    expect(result.current.isActionCompleted('action1')).toBe(false);
  });

  it('should calculate module progress correctly', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
    });

    const progress = result.current.calculateModuleProgress(mockActions, 'module1');
    expect(progress.totalActions).toBe(2);
    expect(progress.completedActions).toBe(1);
  });

  it('should calculate overall progress correctly', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
      result.current.markActionAsCompleted('action2');
    });

    const progress = result.current.calculateOverallProgress(mockActions);
    expect(progress).toBe(67); // 2 out of 3 actions completed
  });

  it('should get completed and incomplete actions', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
    });

    const completed = result.current.getCompletedActions(mockActions);
    const incomplete = result.current.getIncompleteActions(mockActions);

    expect(completed.length).toBe(1);
    expect(incomplete.length).toBe(2);
  });

  it('should export progress correctly', () => {
    const { result } = renderHook(() => useProgress());

    act(() => {
      result.current.markActionAsCompleted('action1');
    });

    const exported = result.current.exportProgress(mockActions);
    const parsed = JSON.parse(exported);

    expect(parsed.completedActions.length).toBe(1);
    expect(parsed.overallProgress).toBe(33);
    expect(parsed.exportDate).toBeDefined();
  });
});
