import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './TodoForm.css';

const TodoForm = ({ onSubmit, loading, initialData = null, isEdit = false }) => {
    const { t } = useTranslation('todo');
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
            newErrors.title = t('validation.title_required', { defaultValue: 'Title is required' });
        } else if (formData.title.length > 100) {
            newErrors.title = t('validation.title_too_long', { defaultValue: 'Title must not exceed 100 characters' });
        }
        
        if (formData.description && formData.description.length > 500) {
            newErrors.description = t('validation.description_too_long', { defaultValue: 'Description must not exceed 500 characters' });
        }

        // Validate deadline if set
        if (formData.deadline) {
            const selectedDate = new Date(formData.deadline);
            const now = getCurrentLocalTime();
            if (selectedDate <= now) {
                newErrors.deadline = t('validation.deadline_past', { defaultValue: 'Deadline must be in the future' });
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
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    return (
        <form onSubmit={handleSubmit} className="todo-form">
            <div className="form-header">
                <h2>{isEdit ? t('form.edit.title') : t('form.create_form.title')}</h2>
            </div>

            <div className="form-group">
                <label htmlFor="title">{t('form.title.label')}</label>
                <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    placeholder={t('form.title.placeholder')}
                    className={errors.title ? 'error' : ''}
                    disabled={loading}
                />
                {errors.title && <span className="error-message">{errors.title}</span>}
            </div>

            <div className="form-group">
                <label htmlFor="description">{t('form.description.label')}</label>
                <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    placeholder={t('form.description.placeholder')}
                    rows="3"
                    className={errors.description ? 'error' : ''}
                    disabled={loading}
                />
                {errors.description && <span className="error-message">{errors.description}</span>}
            </div>

            <div className="form-group">
                <label htmlFor="deadline">{t('form.deadline.label')}</label>
                <input
                    type="datetime-local"
                    id="deadline"
                    name="deadline"
                    value={formData.deadline}
                    onChange={handleChange}
                    className={errors.deadline ? 'error' : ''}
                    disabled={loading}
                />
                {errors.deadline && <span className="error-message">{errors.deadline}</span>}
                <small className="form-help">
                    {t('form.deadline.help')}
                </small>
            </div>

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
                    {t('form.completed')}
                </label>
            </div>

            <div className="form-actions">
                <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                >
                    {loading ? (
                        <span className="loading-text">
                            <span className="loading-spinner"></span>
                            {t('form.saving')}
                        </span>
                    ) : (
                        isEdit ? t('form.update') : t('form.create')
                    )}
                </button>
                
                {isEdit && (
                    <button
                        type="button"
                        className="btn btn-secondary"
                        onClick={() => window.history.back()}
                        disabled={loading}
                    >
                        {t('form.cancel')}
                    </button>
                )}
            </div>
        </form>
    );
};

export default TodoForm;
