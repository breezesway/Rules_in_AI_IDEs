import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './TodoItem.css';

const TodoItem = ({ todo, onUpdate, onToggle, onDelete, onSetDeadline, onRemoveDeadline, loading }) => {
    const { t } = useTranslation('common');
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
            newErrors.title = t('todo_item.title_required');
        } else if (editData.title.length > 100) {
            newErrors.title = t('todo_item.title_too_long');
        }
        
        if (editData.description && editData.description.length > 500) {
            newErrors.description = t('todo_item.description_too_long');
        }

        // Validate deadline if set
        if (editData.deadline) {
            const selectedDate = new Date(editData.deadline);
            const now = getCurrentLocalTime();
            if (selectedDate <= now) {
                newErrors.deadline = t('todo_item.deadline_future');
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
        try {
            await onToggle(todo.id);
        } catch (error) {
            // Error is handled by the parent component
        }
    };

    const handleDelete = async () => {
        if (window.confirm(t('todo.confirm.delete'))) {
            try {
                await onDelete(todo.id);
            } catch (error) {
                // Error is handled by the parent component
            }
        }
    };

    const getDeadlineStatusClass = () => {
        if (!todo.hasDeadline) return '';
        if (todo.isOverdue) return 'overdue';
        if (todo.isDueSoon) return 'due-soon';
        return 'on-time';
    };

    const getDeadlineStatusText = () => {
        if (!todo.hasDeadline) return '';
        if (todo.isOverdue) return t('todo_item.overdue');
        if (todo.isDueSoon) return t('todo_item.due_soon');
        return t('todo_item.on_time');
    };

    const formatDeadline = (deadline) => {
        if (!deadline) return '';
        
        const now = new Date();
        const deadlineDate = new Date(deadline);
        const diffTime = deadlineDate - now;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays < 0) {
            return `${Math.abs(diffDays)} ${t('todo_item.days_left')}`;
        } else if (diffDays === 0) {
            return t('todo_item.days_left').replace('일', '시간').replace('days', 'hours');
        } else {
            return `${diffDays} ${t('todo_item.days_left')}`;
        }
    };

    const formatDate = (dateString) => {
        if (!dateString) return '';
        
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = now - date;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays === 0) {
            return '오늘';
        } else if (diffDays === 1) {
            return '어제';
        } else if (diffDays < 7) {
            return `${diffDays}일 전`;
        } else {
            return date.toLocaleDateString('ko-KR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    };

    if (isEditing) {
        return (
            <div className="todo-item editing">
                <form onSubmit={handleEditSubmit} className="edit-form">
                    <div className="form-group">
                        <label htmlFor="edit-title">{t('todo.form.title.label')}</label>
                        <input
                            type="text"
                            id="edit-title"
                            name="title"
                            value={editData.title}
                            onChange={handleEditChange}
                            className={editErrors.title ? 'error' : ''}
                            disabled={loading}
                        />
                        {editErrors.title && <span className="error-message">{editErrors.title}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="edit-description">{t('todo.form.description.label')}</label>
                        <textarea
                            id="edit-description"
                            name="description"
                            value={editData.description}
                            onChange={handleEditChange}
                            rows="3"
                            className={editErrors.description ? 'error' : ''}
                            disabled={loading}
                        />
                        {editErrors.description && <span className="error-message">{editErrors.description}</span>}
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="edit-deadline">{t('todo_item.deadline')}</label>
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
                </form>
                
                <div className="edit-actions">
                    <button 
                        type="submit" 
                        className="save-btn"
                        disabled={loading}
                        onClick={handleEditSubmit}
                    >
                        {loading ? t('todo_item.saving') : t('save')}
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
                        {t('cancel')}
                    </button>
                </div>
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
                            title={todo.completed ? t('todo_item.mark_incomplete') : t('todo_item.mark_complete')}
                        >
                            {todo.completed ? '✓' : '○'}
                        </button>
                        <button
                            onClick={() => setIsEditing(true)}
                            className="edit-btn"
                            disabled={loading}
                            title={t('todo_item.edit_todo')}
                        >
                            ✎
                        </button>
                        <button
                            onClick={handleDelete}
                            className="delete-btn"
                            disabled={loading}
                            title={t('todo_item.delete_todo')}
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
                            {t('todo_item.due')}: {formatDate(todo.deadline)}
                        </div>
                    </div>
                )}
                
                <div className="todo-meta">
                    <span className="todo-date">
                        {t('todo_item.created')}: {formatDate(todo.createdAt)}
                    </span>
                    {todo.updatedAt !== todo.createdAt && (
                        <span className="todo-date">
                            {t('todo_item.updated')}: {formatDate(todo.updatedAt)}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TodoItem;
