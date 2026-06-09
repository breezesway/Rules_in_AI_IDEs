import React, { useState } from 'react';
import './TodoItem.css';

const TodoItem = ({ todo, onUpdate, onToggle, onDelete, onSetDeadline, onRemoveDeadline, loading }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({
        title: todo.title,
        description: todo.description || '',
        completed: todo.completed,
        deadline: todo.deadline ? formatDateForInput(todo.deadline) : ''
    });
    const [editErrors, setEditErrors] = useState({});

    // Helper function to format date for datetime-local input (preserves local timezone)
    function formatDateForInput(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        // Convert to local timezone and format for datetime-local input
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }

    // Helper function to get current local time
    function getCurrentLocalTime() {
        const now = new Date();
        // Get local time components
        const year = now.getFullYear();
        const month = now.getMonth();
        const day = now.getDate();
        const hours = now.getHours();
        const minutes = now.getMinutes();
        const seconds = now.getSeconds();
        const milliseconds = now.getMilliseconds();
        
        // Create new date in local timezone
        return new Date(year, month, day, hours, minutes, seconds, milliseconds);
    }

    const validateEditForm = () => {
        const newErrors = {};
        
        if (!editData.title.trim()) {
            newErrors.title = 'Title is required';
        } else if (editData.title.length > 100) {
            newErrors.title = 'Title must not exceed 100 characters';
        }
        
        if (editData.description && editData.description.length > 500) {
            newErrors.description = 'Description must not exceed 500 characters';
        }

        // Validate deadline if set
        if (editData.deadline) {
            const selectedDate = new Date(editData.deadline);
            const now = getCurrentLocalTime();
            if (selectedDate <= now) {
                newErrors.deadline = 'Deadline must be in the future';
            }
        }
        
        setEditErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateEditForm()) {
            return;
        }

        try {
            const submitData = {
                ...editData,
                deadline: editData.deadline ? new Date(editData.deadline).toISOString() : null
            };
            
            await onUpdate(todo.id, submitData);
            setIsEditing(false);
            setEditErrors({});
        } catch (error) {
            // Error is handled by the parent component
        }
    };

    const handleEditChange = (e) => {
        const { name, value, type, checked } = e.target;
        setEditData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        
        if (editErrors[name]) {
            setEditErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const handleToggle = async () => {
        if (!loading) {
            await onToggle(todo.id);
        }
    };

    const handleDelete = async () => {
        if (!loading && window.confirm('Are you sure you want to delete this todo?')) {
            await onDelete(todo.id);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('ko-KR', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const formatDeadline = (deadlineString) => {
        const deadline = new Date(deadlineString);
        const now = getCurrentLocalTime();
        const diffTime = deadline - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
        
        if (diffDays > 1) {
            return `${diffDays} days left`;
        } else if (diffHours > 1) {
            return `${diffHours} hours left`;
        } else {
            return 'Less than 1 hour left';
        }
    };

    const getDeadlineStatusClass = () => {
        if (!todo.hasDeadline) return 'no-deadline';
        if (todo.isOverdue) return 'overdue';
        if (todo.isDueSoon) return 'due-soon';
        return 'on-time';
    };

    const getDeadlineStatusText = () => {
        if (!todo.hasDeadline) return 'No Deadline';
        if (todo.isOverdue) return 'Overdue';
        if (todo.isDueSoon) return 'Due Soon';
        return 'On Time';
    };

    if (isEditing) {
        return (
            <div className="todo-item editing">
                <form onSubmit={handleEditSubmit} className="edit-form">
                    <div className="edit-form-content">
                        <div className="form-group">
                            <input
                                type="text"
                                name="title"
                                value={editData.title}
                                onChange={handleEditChange}
                                className={editErrors.title ? 'error' : ''}
                                disabled={loading}
                            />
                            {editErrors.title && <span className="error-message">{editErrors.title}</span>}
                        </div>
                        
                        <div className="form-group">
                            <textarea
                                name="description"
                                value={editData.description}
                                onChange={handleEditChange}
                                rows="2"
                                className={editErrors.description ? 'error' : ''}
                                disabled={loading}
                                placeholder="Description (optional)"
                            />
                            {editErrors.description && <span className="error-message">{editErrors.description}</span>}
                        </div>

                        <div className="form-group checkbox-group">
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    name="completed"
                                    checked={editData.completed}
                                    onChange={handleEditChange}
                                    disabled={loading}
                                />
                                <span className="checkmark"></span>
                                Mark as completed
                            </label>
                        </div>

                        <div className="form-group">
                            <label htmlFor="edit-deadline">Deadline</label>
                            <input
                                type="datetime-local"
                                id="edit-deadline"
                                name="deadline"
                                value={editData.deadline}
                                onChange={handleEditChange}
                                className={editErrors.deadline ? 'error' : ''}
                                disabled={loading}
                            />
                            {editErrors.deadline && <span className="error-message">{editErrors.deadline}</span>}
                        </div>
                    </div>
                    
                    <div className="edit-actions">
                        <button 
                            type="submit" 
                            className="save-btn"
                            disabled={loading}
                        >
                            {loading ? 'Saving...' : 'Save'}
                        </button>
                        <button 
                            type="button" 
                            className="cancel-btn"
                            onClick={() => {
                                setIsEditing(false);
                                setEditData({ 
                                    title: todo.title, 
                                    description: todo.description || '',
                                    completed: todo.completed,
                                    deadline: todo.deadline ? formatDateForInput(todo.deadline) : ''
                                });
                                setEditErrors({});
                            }}
                            disabled={loading}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        );
    }

    return (
        <div className={`todo-item ${todo.completed ? 'completed' : ''} ${getDeadlineStatusClass()}`}>
            <div className="todo-content">
                <div className="todo-header">
                    <h3 className="todo-title">{todo.title}</h3>
                    <div className="todo-actions">
                        <button
                            onClick={handleToggle}
                            className={`toggle-btn ${todo.completed ? 'completed' : ''}`}
                            disabled={loading}
                            title={todo.completed ? 'Mark as incomplete' : 'Mark as complete'}
                        >
                            {todo.completed ? '✓' : '○'}
                        </button>
                        <button
                            onClick={() => setIsEditing(true)}
                            className="edit-btn"
                            disabled={loading}
                            title="Edit todo"
                        >
                            ✎
                        </button>
                        <button
                            onClick={handleDelete}
                            className="delete-btn"
                            disabled={loading}
                            title="Delete todo"
                        >
                            ×
                        </button>
                    </div>
                </div>
                
                {todo.description && (
                    <p className="todo-description">{todo.description}</p>
                )}
                
                {todo.hasDeadline && (
                    <div className="deadline-info">
                        <div className={`deadline-status ${getDeadlineStatusClass()}`}>
                            <span className="deadline-icon">
                                {todo.isOverdue ? '⚠️' : todo.isDueSoon ? '⏰' : '📅'}
                            </span>
                            <span className="deadline-text">
                                {getDeadlineStatusText()}: {formatDeadline(todo.deadline)}
                            </span>
                        </div>
                        <div className="deadline-date">
                            Due: {formatDate(todo.deadline)}
                        </div>
                    </div>
                )}
                
                <div className="todo-meta">
                    <span className="todo-date">
                        Created: {formatDate(todo.createdAt)}
                    </span>
                    {todo.updatedAt !== todo.createdAt && (
                        <span className="todo-date">
                            Updated: {formatDate(todo.updatedAt)}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TodoItem;
