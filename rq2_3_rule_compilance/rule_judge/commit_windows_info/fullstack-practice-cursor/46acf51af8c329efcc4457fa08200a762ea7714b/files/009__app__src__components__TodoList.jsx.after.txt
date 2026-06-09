import React, { useState, useEffect } from 'react';
import { useTodo } from '../context/TodoContext';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = () => {
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
                    <p>Loading your todos...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="todo-list-container">
                <div className="error-state">
                    <div className="error-icon">❌</div>
                    <h3>Error loading todos</h3>
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
                    <h3>No todos yet</h3>
                    <p>Create your first todo to get started!</p>
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
                        <span className="stat-label">Active</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{completedTodos.length}</span>
                        <span className="stat-label">Completed</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{stats.todosWithDeadlines}</span>
                        <span className="stat-label">With Deadlines</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{stats.overdueTodos}</span>
                        <span className="stat-label">Overdue</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{stats.dueSoonTodos}</span>
                        <span className="stat-label">Due Soon</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-number">{Math.round(stats.deadlineCompletionRate)}%</span>
                        <span className="stat-label">Completion Rate</span>
                    </div>
                </div>
            )}

            {/* Overdue Todos Section */}
            {overdueTodos.length > 0 && (
                <div className="todo-section overdue-section">
                    <h2 className="section-title overdue-title" onClick={() => setShowOverdue(!showOverdue)}>
                        <span className="overdue-icon">⚠️</span>
                        Overdue Todos ({overdueTodos.length})
                        <span className="toggle-icon">{showOverdue ? '▼' : '▶'}</span>
                    </h2>
                    {showOverdue && overdueTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={updateTodo}
                            onToggle={toggleTodoCompletion}
                            onDelete={deleteTodo}
                            onSetDeadline={setTodoDeadline}
                            onRemoveDeadline={removeTodoDeadline}
                            loading={loading}
                        />
                    ))}
                </div>
            )}

            {/* Due Soon Todos Section */}
            {dueSoonTodos.length > 0 && (
                <div className="todo-section due-soon-section">
                    <h2 className="section-title due-soon-title" onClick={() => setShowDueSoon(!showDueSoon)}>
                        <span className="due-soon-icon">⏰</span>
                        Due Soon ({dueSoonTodos.length})
                        <span className="toggle-icon">{showDueSoon ? '▼' : '▶'}</span>
                    </h2>
                    {showDueSoon && dueSoonTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={updateTodo}
                            onToggle={toggleTodoCompletion}
                            onDelete={deleteTodo}
                            onSetDeadline={setTodoDeadline}
                            onRemoveDeadline={removeTodoDeadline}
                            loading={loading}
                        />
                    ))}
                </div>
            )}

            {/* Active Todos Section */}
            {activeTodos.length > 0 && (
                <div className="todo-section">
                    <h2 className="section-title">Active Todos</h2>
                    {activeTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={updateTodo}
                            onToggle={toggleTodoCompletion}
                            onDelete={deleteTodo}
                            onSetDeadline={setTodoDeadline}
                            onRemoveDeadline={removeTodoDeadline}
                            loading={loading}
                        />
                    ))}
                </div>
            )}

            {/* Completed Todos Section */}
            {completedTodos.length > 0 && (
                <div className="todo-section">
                    <h2 className="section-title">Completed Todos</h2>
                    {completedTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={updateTodo}
                            onToggle={toggleTodoCompletion}
                            onDelete={deleteTodo}
                            onSetDeadline={setTodoDeadline}
                            onRemoveDeadline={removeTodoDeadline}
                            loading={loading}
                        />
                    ))}
                </div>
            )}

            {loading && todos.length > 0 && (
                <div className="loading-overlay">
                    <div className="loading-spinner"></div>
                    <p>Updating...</p>
                </div>
            )}
        </div>
    );
};

export default TodoList;
