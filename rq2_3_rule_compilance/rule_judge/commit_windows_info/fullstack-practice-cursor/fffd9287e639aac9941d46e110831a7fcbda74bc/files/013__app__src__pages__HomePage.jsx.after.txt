import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title">Welcome to Todo App</h1>
        <p className="home-description">
          A secure and feature-rich todo application with email verification
        </p>
        
        {isAuthenticated ? (
          <div className="authenticated-actions">
            <Link to="/todos" className="btn btn-primary">
              Go to My Todos
            </Link>
            <Link to="/login-success" className="btn btn-secondary">
              View Profile
            </Link>
          </div>
        ) : (
          <div className="guest-actions">
            <Link to="/login" className="btn btn-primary">
              Login
            </Link>
            <Link to="/register" className="btn btn-secondary">
              Register
            </Link>
          </div>
        )}
        
        <div className="features">
          <h2>Features</h2>
          <ul>
            <li>Secure user authentication with JWT</li>
            <li>Email verification system</li>
            <li>Personal todo management</li>
            <li>Responsive design</li>
            <li>Real-time updates</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
