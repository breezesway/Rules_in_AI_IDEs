import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useTodo } from '../context/TodoContext';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = () => {
    const { t } = useTranslation('todo');
    const { 
        todos, 
        loading, 
        error, 
        stats,
        updateTodo, 
        toggleTodoCompletion, 
        deleteTodo,
        setTodoDeadline,
        removeTodoDeadline,
        getOverdueTodos,
        getDueSoonTodos
    } = useTodo();

    const [overdueTodos, setOverdueTodos] = useState([]);
    const [dueSoonTodos, setDueSoonTodos] = useState([]);
    const [showOverdue, setShowOverdue] = useState(false);
    const [showDueSoon, setShowDueSoon] = useState(false);

    useEffect(() => {
        if (todos.length > 0) {
            loadSpecialTodos();
        }
    }, [todos]);

    const loadSpecialTodos = async () => {
        try {
            const [overdue, dueSoon] = await Promise.all([
                getOverdueTodos(),
                getDueSoonTodos()
            ]);
            setOverdueTodos(overdue);
            setDueSoonTodos(dueSoon);
        } catch (error) {
            console.error('Failed to load special todos:', error);
        }
    };

    if (loading && todos.length === 0) {
        return (
            <div className="todo-list-container">
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>{t('loading', { defaultValue: '할 일을 불러오는 중...' })}</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="todo-list-container">
                <div className="error-state">
                    <div className="error-icon">❌</div>
                    <h3>{t('error.title', { defaultValue: '할 일을 불러오는 중 오류가 발생했습니다' })}</h3>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    if (todos.length === 0) {
        return (
            <div className="todo-list-container">
                <div className="empty-state">
                    <div className="empty-icon">📝</div>
                    <h3>{t('empty.title')}</h3>
                    <p>{t('empty.description')}</p>
                </div>
            </div>
        );
    }

    const completedTodos = todos.filter(todo => todo.completed);
    const activeTodos = todos.filter(todo => !todo.completed);

    return (
        <div className="todo-list-container">
            {/* Enhanced Statistics */}
            {stats && (
                <div className="todo-stats enhanced">
                    <div className="stat-item">
                        <span className="stat-number">{activeTodos.length}</span>
                        <span className="stat-label">{t('stats.pending')}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{completedTodos.length}</span>
                        <span className="stat-label">{t('stats.completed')}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{stats.todosWithDeadlines}</span>
                        <span className="stat-label">{t('stats.with_deadlines')}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{stats.completionRate}%</span>
                        <span className="stat-label">{t('stats.completion_rate')}</span>
                    </div>
                </div>
            )}

            {/* Special Todo Sections */}
            {overdueTodos.length > 0 && (
                <div className="special-todos-section overdue">
                    <div className="section-header" onClick={() => setShowOverdue(!showOverdue)}>
                        <h3>⚠️ {t('deadline.overdue')} ({overdueTodos.length})</h3>
                        <span className="toggle-icon">{showOverdue ? '▼' : '▶'}</span>
                    </div>
                    {showOverdue && (
                        <div className="special-todos-list">
                            {overdueTodos.map(todo => (
                                <TodoItem
                                    key={todo.id}
                                    todo={todo}
                                    onUpdate={updateTodo}
                                    onToggle={toggleTodoCompletion}
                                    onDelete={deleteTodo}
                                    onSetDeadline={setTodoDeadline}
                                    onRemoveDeadline={removeTodoDeadline}
                                    isSpecial={true}
                                />
                            ))}
                        </div>
                    )}
                </div>
            )}

            {dueSoonTodos.length > 0 && (
                <div className="special-todos-section due-soon">
                    <div className="section-header" onClick={() => setShowDueSoon(!showDueSoon)}>
                        <h3>⏰ {t('deadline.due_soon')} ({dueSoonTodos.length})</h3>
                        <span className="toggle-icon">{showDueSoon ? '▼' : '▶'}</span>
                    </div>
                    {showDueSoon && (
                        <div className="special-todos-list">
                            {dueSoonTodos.map(todo => (
                                <TodoItem
                                    key={todo.id}
                                    todo={todo}
                                    onUpdate={updateTodo}
                                    onToggle={toggleTodoCompletion}
                                    onDelete={deleteTodo}
                                    onSetDeadline={setTodoDeadline}
                                    onRemoveDeadline={removeTodoDeadline}
                                    isSpecial={true}
                                />
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Main Todo List */}
            <div className="todo-sections">
                {/* Active Todos */}
                {activeTodos.length > 0 && (
                    <div className="todo-section active">
                        <h3>{t('status.pending')} ({activeTodos.length})</h3>
                        <div className="todo-items">
                            {activeTodos.map(todo => (
                                <TodoItem
                                    key={todo.id}
                                    todo={todo}
                                    onUpdate={updateTodo}
                                    onToggle={toggleTodoCompletion}
                                    onDelete={deleteTodo}
                                    onSetDeadline={setTodoDeadline}
                                    onRemoveDeadline={removeTodoDeadline}
                                />
                            ))}
                        </div>
                    </div>
                )}

                {/* Completed Todos */}
                {completedTodos.length > 0 && (
                    <div className="todo-section completed">
                        <h3>{t('status.completed')} ({completedTodos.length})</h3>
                        <div className="todo-items">
                            {completedTodos.map(todo => (
                                <TodoItem
                                    key={todo.id}
                                    todo={todo}
                                    onUpdate={updateTodo}
                                    onToggle={toggleTodoCompletion}
                                    onDelete={deleteTodo}
                                    onSetDeadline={setTodoDeadline}
                                    onRemoveDeadline={removeTodoDeadline}
                                />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TodoList;
