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

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <Link to="/todos">Todo App</Link>
        </div>
        
        {user && (
          <nav className="nav">
            <span className="welcome-text">
              Welcome, {user.firstName || user.username}!
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
