import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginSuccessPage.css';

const LoginSuccessPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [countdown, setCountdown] = useState(5);
  const [isNewUser, setIsNewUser] = useState(false);

  useEffect(() => {
    // Check if user came from registration
    const fromRegistration = location.state?.fromRegistration;
    setIsNewUser(fromRegistration);

    // Auto-redirect to todos page after 5 seconds
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          navigate('/todos');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [navigate, location.state]);

  const handleGoToTodos = () => {
    navigate('/todos');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    navigate('/login');
    return null;
  }

  // Safe function to get avatar initial with fallbacks
  const getAvatarInitial = () => {
    if (user.firstName && user.firstName.trim()) {
      return user.firstName.charAt(0).toUpperCase();
    }
    if (user.username && user.username.trim()) {
      return user.username.charAt(0).toUpperCase();
    }
    return 'U'; // Default fallback
  };

  // Safe function to get display name
  const getDisplayName = () => {
    if (user.firstName && user.firstName.trim()) {
      const fullName = user.lastName ? `${user.firstName} ${user.lastName}` : user.firstName;
      return fullName.trim();
    }
    return user.username || 'User';
  };

  // Safe function to get user role
  const getUserRole = () => {
    if (user.roles && Array.isArray(user.roles)) {
      return user.roles.includes('ROLE_ADMIN') ? 'Administrator' : 'User';
    }
    return 'User';
  };

  return (
    <div className="login-success-container">
      <div className="success-card">
        <div className="success-icon">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" 
                  stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>

        <h1 className="success-title">
          {isNewUser ? 'Welcome to Todo App!' : 'Login Successful!'}
        </h1>

        <div className="user-info">
          <div className="avatar">
            {getAvatarInitial()}
          </div>
          <div className="user-details">
            <h3>{getDisplayName()}</h3>
            <p>{user.email || 'No email provided'}</p>
            <span className="user-role">
              {getUserRole()}
            </span>
          </div>
        </div>

        {isNewUser && (
          <div className="welcome-message">
            <h4>🎉 Account Created Successfully!</h4>
            <p>Your account has been created and you're now logged in. Welcome to the Todo App family!</p>
          </div>
        )}

        <div className="action-buttons">
          <button className="primary-btn" onClick={handleGoToTodos}>
            {isNewUser ? 'Start Creating Todos' : 'Go to My Todos'}
          </button>
          <button className="secondary-btn" onClick={handleLogout}>
            Logout
          </button>
        </div>

        <div className="auto-redirect">
          <p>Redirecting to todos page in <strong>{countdown}</strong> seconds...</p>
          <button className="skip-btn" onClick={handleGoToTodos}>
            Skip countdown
          </button>
        </div>

        <div className="features-preview">
          <h4>What you can do now:</h4>
          <ul>
            <li>✨ Create and manage your personal todos</li>
            <li>📝 Organize tasks with descriptions</li>
            <li>✅ Mark tasks as completed</li>
            <li>🔄 Update and delete todos</li>
            <li>👤 Manage your profile</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default LoginSuccessPage;
