import React, { useState } from 'react';
import './TodoItem.css';

const TodoItem = ({ todo, onUpdate, onToggle, onDelete, loading }) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({
        title: todo.title,
        description: todo.description || ''
    });
    const [editErrors, setEditErrors] = useState({});

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
        
        setEditErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleEditSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateEditForm()) {
            return;
        }

        try {
            await onUpdate(todo.id, editData);
            setIsEditing(false);
            setEditErrors({});
        } catch (error) {
            // Error is handled by the parent component
        }
    };

    const handleEditChange = (e) => {
        const { name, value } = e.target;
        setEditData(prev => ({
            ...prev,
            [name]: value
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
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
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
                                setEditData({ title: todo.title, description: todo.description || '' });
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
        <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
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
