import React, { useState } from 'react';
import './TodoForm.css';

const TodoForm = ({ onSubmit, loading, initialData = null, isEdit = false }) => {
    const [formData, setFormData] = useState({
        title: initialData?.title || '',
        description: initialData?.description || '',
        completed: initialData?.completed || false,
        deadline: initialData?.deadline ? formatDateForInput(initialData.deadline) : '' // Format for datetime-local input
    });
    const [errors, setErrors] = useState({});

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

    const validateForm = () => {
        const newErrors = {};
        
        if (!formData.title.trim()) {
            newErrors.title = 'Title is required';
        } else if (formData.title.length > 100) {
            newErrors.title = 'Title must not exceed 100 characters';
        }
        
        if (formData.description && formData.description.length > 500) {
            newErrors.description = 'Description must not exceed 500 characters';
        }

        // Validate deadline if set
        if (formData.deadline) {
            const selectedDate = new Date(formData.deadline);
            const now = getCurrentLocalTime();
            if (selectedDate <= now) {
                newErrors.deadline = 'Deadline must be in the future';
            }
        }
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        try {
            const submitData = {
                ...formData,
                deadline: formData.deadline ? new Date(formData.deadline).toISOString() : null
            };
            
            await onSubmit(submitData);
            
            if (!isEdit) {
                setFormData({ title: '', description: '', completed: false, deadline: '' });
            }
            setErrors({});
        } catch (error) {
            // Error is handled by the parent component
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    const clearDeadline = () => {
        setFormData(prev => ({ ...prev, deadline: '' }));
        if (errors.deadline) {
            setErrors(prev => ({ ...prev, deadline: '' }));
        }
    };

    const setQuickDeadline = (hours) => {
        // Use local time instead of UTC
        const now = getCurrentLocalTime();
        const deadline = new Date(now.getTime() + hours * 60 * 60 * 1000);
        
        // Format for datetime-local input (preserves local timezone)
        const formattedDeadline = formatDateForInput(deadline.toISOString());
        setFormData(prev => ({ ...prev, deadline: formattedDeadline }));
        if (errors.deadline) {
            setErrors(prev => ({ ...prev, deadline: '' }));
        }
    };

    return (
        <div className="todo-form-container">
            <h2>{isEdit ? 'Edit Todo' : 'Add New Todo'}</h2>
            <form onSubmit={handleSubmit} className="todo-form">
                <div className="form-group">
                    <label htmlFor="title">Title *</label>
                    <input
                        type="text"
                        id="title"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        placeholder="Enter todo title..."
                        className={errors.title ? 'error' : ''}
                        disabled={loading}
                    />
                    {errors.title && <span className="error-message">{errors.title}</span>}
                </div>

                <div className="form-group">
                    <label htmlFor="description">Description</label>
                    <textarea
                        id="description"
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        placeholder="Enter todo description (optional)..."
                        rows="3"
                        className={errors.description ? 'error' : ''}
                        disabled={loading}
                    />
                    {errors.description && <span className="error-message">{errors.description}</span>}
                </div>

                {isEdit && (
                    <div className="form-group checkbox-group">
                        <label className="checkbox-label">
                            <input
                                type="checkbox"
                                name="completed"
                                checked={formData.completed}
                                onChange={handleChange}
                                disabled={loading}
                            />
                            <span className="checkmark"></span>
                            Mark as completed
                        </label>
                    </div>
                )}

                <div className="form-group">
                    <label htmlFor="deadline">Deadline (Optional)</label>
                    <div className="deadline-input-group">
                        <input
                            type="datetime-local"
                            id="deadline"
                            name="deadline"
                            value={formData.deadline}
                            onChange={handleChange}
                            className={errors.deadline ? 'error' : ''}
                            disabled={loading}
                        />
                        {formData.deadline && (
                            <button
                                type="button"
                                onClick={clearDeadline}
                                className="clear-deadline-btn"
                                disabled={loading}
                            >
                                Clear
                            </button>
                        )}
                    </div>
                    {errors.deadline && <span className="error-message">{errors.deadline}</span>}
                    
                    <div className="quick-deadline-buttons">
                        <button
                            type="button"
                            onClick={() => setQuickDeadline(1)}
                            className="quick-deadline-btn"
                            disabled={loading}
                        >
                            +1 Hour
                        </button>
                        <button
                            type="button"
                            onClick={() => setQuickDeadline(24)}
                            className="quick-deadline-btn"
                            disabled={loading}
                        >
                            +1 Day
                        </button>
                        <button
                            type="button"
                            onClick={() => setQuickDeadline(168)}
                            className="quick-deadline-btn"
                            disabled={loading}
                        >
                            +1 Week
                        </button>
                    </div>
                </div>

                <button 
                    type="submit" 
                    className="submit-btn"
                    disabled={loading || !formData.title.trim()}
                >
                    {loading ? (isEdit ? 'Updating...' : 'Adding...') : (isEdit ? 'Update Todo' : 'Add Todo')}
                </button>
            </form>
        </div>
    );
};

export default TodoForm;
