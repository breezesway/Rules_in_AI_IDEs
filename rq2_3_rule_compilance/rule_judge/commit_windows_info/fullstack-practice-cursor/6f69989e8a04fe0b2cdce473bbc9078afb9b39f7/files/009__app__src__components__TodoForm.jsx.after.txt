import React, { useState } from 'react';
import './TodoForm.css';

const TodoForm = ({ onSubmit, loading }) => {
    const [formData, setFormData] = useState({
        title: '',
        description: ''
    });
    const [errors, setErrors] = useState({});

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
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        try {
            await onSubmit(formData);
            setFormData({ title: '', description: '' });
            setErrors({});
        } catch (error) {
            // Error is handled by the parent component
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => ({
                ...prev,
                [name]: ''
            }));
        }
    };

    return (
        <div className="todo-form-container">
            <h2>Add New Todo</h2>
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

                <button 
                    type="submit" 
                    className="submit-btn"
                    disabled={loading || !formData.title.trim()}
                >
                    {loading ? 'Adding...' : 'Add Todo'}
                </button>
            </form>
        </div>
    );
};

export default TodoForm;
