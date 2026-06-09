import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Header.css';

const Header = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Extract user data from the nested structure
  const userData = user?.data || user;

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <Link to="/todos">Todo App</Link>
        </div>
        
        {userData && (
          <nav className="nav">
            <span className="welcome-text">
              Welcome, {userData.firstName || userData.username}!
            </span>
            <button onClick={handleLogout} className="logout-btn">
              Logout
            </button>
          </nav>
        )}
      </div>
    </header>
  );
};

export default Header;
