import React from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = ({ todos, loading, onUpdate, onToggle, onDelete }) => {
    if (loading && todos.length === 0) {
        return (
            <div className="todo-list-container">
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Loading todos...</p>
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
            <div className="todo-stats">
                <div className="stat-item">
                    <span className="stat-number">{activeTodos.length}</span>
                    <span className="stat-label">Active</span>
                </div>
                <div className="stat-item">
                    <span className="stat-number">{completedTodos.length}</span>
                    <span className="stat-label">Completed</span>
                </div>
                <div className="stat-item">
                    <span className="stat-number">{todos.length}</span>
                    <span className="stat-label">Total</span>
                </div>
            </div>

            {activeTodos.length > 0 && (
                <div className="todo-section">
                    <h2 className="section-title">Active Todos</h2>
                    {activeTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={onUpdate}
                            onToggle={onToggle}
                            onDelete={onDelete}
                            loading={loading}
                        />
                    ))}
                </div>
            )}

            {completedTodos.length > 0 && (
                <div className="todo-section">
                    <h2 className="section-title">Completed Todos</h2>
                    {completedTodos.map(todo => (
                        <TodoItem
                            key={todo.id}
                            todo={todo}
                            onUpdate={onUpdate}
                            onToggle={onToggle}
                            onDelete={onDelete}
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
