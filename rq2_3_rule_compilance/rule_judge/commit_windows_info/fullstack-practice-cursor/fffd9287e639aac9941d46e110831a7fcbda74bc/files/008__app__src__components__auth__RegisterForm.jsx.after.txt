import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './AuthForms.css';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    firstName: '',
    lastName: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear related errors when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    // Clear general error if it's related to the field being edited
    if (errors.general) {
      const generalError = errors.general.toLowerCase();
      const fieldName = name.toLowerCase();
      
      if (generalError.includes(fieldName) || 
          (fieldName === 'email' && generalError.includes('email')) ||
          (fieldName === 'username' && generalError.includes('username')) ||
          (fieldName === 'password' && generalError.includes('password'))) {
        setErrors(prev => ({
          ...prev,
          general: ''
        }));
      }
    }
    
    // Clear "User already exists" error when firstName or lastName is modified
    if ((name === 'firstName' || name === 'lastName') && 
        (errors.firstName === 'User already exists' || errors.lastName === 'User already exists')) {
      setErrors(prev => ({
        ...prev,
        firstName: prev.firstName === 'User already exists' ? '' : prev.firstName,
        lastName: prev.lastName === 'User already exists' ? '' : prev.lastName
      }));
    }
    
    // Real-time validation
    validateField(name, value);
  };

  const validateField = (fieldName, value) => {
    let error = '';
    
    switch (fieldName) {
      case 'username':
        if (!value.trim()) {
          error = 'Username is required';
        } else if (value.length < 3) {
          error = 'Username must be at least 3 characters';
        } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
          error = 'Username can only contain letters, numbers, and underscores';
        }
        break;
        
      case 'email':
        if (!value.trim()) {
          error = 'Email is required';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          error = 'Please enter a valid email address';
        }
        break;
        
      case 'password':
        if (!value) {
          error = 'Password is required';
        } else if (value.length < 8) {
          error = 'Password must be at least 8 characters';
        } else if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(value)) {
          error = 'Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character';
        }
        
        // Also validate confirm password if it has a value
        if (formData.confirmPassword && value !== formData.confirmPassword) {
          setErrors(prev => ({
            ...prev,
            confirmPassword: 'Passwords do not match'
          }));
        } else if (formData.confirmPassword && value === formData.confirmPassword) {
          setErrors(prev => ({
            ...prev,
            confirmPassword: ''
          }));
        }
        break;
        
      case 'confirmPassword':
        if (!value) {
          error = 'Please confirm your password';
        } else if (formData.password !== value) {
          error = 'Passwords do not match';
        }
        break;
        
      case 'firstName':
        if (value && value.length > 50) {
          error = 'First name must not exceed 50 characters';
        }
        break;
        
      case 'lastName':
        if (value && value.length > 50) {
          error = 'Last name must not exceed 50 characters';
        }
        break;
        
      default:
        break;
    }
    
    // If the field is now valid, clear any server errors that might be related
    if (!error && errors[fieldName]) {
      setErrors(prev => ({
        ...prev,
        [fieldName]: ''
      }));
    }
    
    setErrors(prev => ({
      ...prev,
      [fieldName]: error
    }));
  };

  const validateForm = () => {
    // Check if there are any existing errors
    const hasErrors = Object.values(errors).some(error => error && error !== '');
    
    if (hasErrors) {
      return false;
    }
    
    // Additional validation for required fields that might be empty
    const newErrors = {};
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    }
    
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(prev => ({
        ...prev,
        ...newErrors
      }));
      return false;
    }
    
    return true;
  };

  const clearServerErrors = () => {
    // Clear any server-related errors when form is being submitted
    const serverErrors = {};
    Object.keys(errors).forEach(key => {
      if (errors[key] && (
        errors[key].toLowerCase().includes('already exists') ||
        errors[key].toLowerCase().includes('invalid') ||
        errors[key].toLowerCase().includes('not found')
      )) {
        serverErrors[key] = '';
      }
    });
    
    if (Object.keys(serverErrors).length > 0) {
      setErrors(prev => ({
        ...prev,
        ...serverErrors
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Clear server errors before validation
    clearServerErrors();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    
    try {
      console.log('Submitting registration form with data:', {
        username: formData.username,
        email: formData.email,
        firstName: formData.firstName,
        lastName: formData.lastName
      });
      
      const result = await register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName || null,
        lastName: formData.lastName || null
      });
      
      console.log('Registration result:', result);
      
      if (result.success) {
        console.log('Registration successful, redirecting to email verification');
        // Redirect to email verification page
        navigate('/verify-email', { 
          state: { 
            email: formData.email,
            message: 'Registration successful! Please check your email for verification code.' 
          } 
        });
      } else {
        console.log('Registration failed with error:', result.error);
        // Map server errors to specific fields
        const fieldErrors = {};
        
        if (result.error) {
          if (result.error.toLowerCase().includes('username') && result.error.toLowerCase().includes('exists')) {
            fieldErrors.username = 'Username already exists';
          } else if (result.error.toLowerCase().includes('email') && result.error.toLowerCase().includes('exists')) {
            fieldErrors.email = 'Email already exists';
          } else if (result.error.toLowerCase().includes('user already exists')) {
            fieldErrors.firstName = 'User already exists';
            fieldErrors.lastName = 'User already exists';
          } else if (result.error.toLowerCase().includes('username')) {
            fieldErrors.username = result.error;
          } else if (result.error.toLowerCase().includes('email')) {
            fieldErrors.email = result.error;
          } else if (result.error.toLowerCase().includes('password')) {
            fieldErrors.password = result.error;
          } else {
            // If no specific field can be determined, show as general error
            fieldErrors.general = result.error;
          }
        }
        
        console.log('Setting field errors:', fieldErrors);
        setErrors(prev => ({
          ...prev,
          ...fieldErrors
        }));
      }
    } catch (error) {
      console.error('Unexpected error during registration:', error);
      setErrors({ general: 'An unexpected error occurred' });
    } finally {
      setIsLoading(false);
    }
  };

  const getInputClassName = (fieldName) => {
    if (errors[fieldName]) {
      return 'error';
    }
    if (formData[fieldName] && formData[fieldName].trim()) {
      // For password fields, only show valid if they meet requirements
      if (fieldName === 'password') {
        if (formData.password.length >= 8 && 
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(formData.password)) {
          return 'valid';
        }
      } else if (fieldName === 'confirmPassword') {
        if (formData.confirmPassword && formData.password === formData.confirmPassword) {
          return 'valid';
        }
      } else if (fieldName === 'username') {
        if (formData.username.length >= 3 && /^[a-zA-Z0-9_]+$/.test(formData.username)) {
          return 'valid';
        }
      } else if (fieldName === 'email') {
        if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          return 'valid';
        }
      } else if (fieldName === 'firstName' || fieldName === 'lastName') {
        if (formData[fieldName] && formData[fieldName].length <= 50) {
          return 'valid';
        }
      }
    }
    return '';
  };

  return (
    <div className="auth-container">
      <div className="auth-form">
        <h2>Register</h2>
        
        {errors.general && (
          <div className="error-message">
            {errors.general}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group name-row">
            <div className="name-field">
              <label htmlFor="firstName">First Name</label>
              <input
                type="text"
                id="firstName"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                onBlur={(e) => validateField('firstName', e.target.value)}
                className={getInputClassName('firstName')}
                placeholder="Enter your first name"
              />
              {errors.firstName && (
                <span className="error-text">{errors.firstName}</span>
              )}
            </div>
            <div className="name-field">
              <label htmlFor="lastName">Last Name</label>
              <input
                type="text"
                id="lastName"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                onBlur={(e) => validateField('lastName', e.target.value)}
                className={getInputClassName('lastName')}
                placeholder="Enter your last name"
              />
              {errors.lastName && (
                <span className="error-text">{errors.lastName}</span>
              )}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="username">Username *</label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              onBlur={(e) => validateField('username', e.target.value)}
              className={getInputClassName('username')}
              placeholder="Enter your username"
            />
            {errors.username && (
              <span className="error-text">{errors.username}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={(e) => validateField('email', e.target.value)}
              className={getInputClassName('email')}
              placeholder="Enter your email"
            />
            {errors.email && (
              <span className="error-text">{errors.email}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="password">Password *</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={(e) => validateField('password', e.target.value)}
              className={getInputClassName('password')}
              placeholder="Enter your password"
            />
            {errors.password && (
              <span className="error-text">{errors.password}</span>
            )}
          </div>

          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password *</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              onBlur={(e) => validateField('confirmPassword', e.target.value)}
              className={getInputClassName('confirmPassword')}
              placeholder="Confirm your password"
            />
            {errors.confirmPassword && (
              <span className="error-text">{errors.confirmPassword}</span>
            )}
          </div>

          <button 
            type="submit" 
            className="submit-btn" 
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="auth-links">
          <p>
            Already have an account? <Link to="/login">Login here</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;
