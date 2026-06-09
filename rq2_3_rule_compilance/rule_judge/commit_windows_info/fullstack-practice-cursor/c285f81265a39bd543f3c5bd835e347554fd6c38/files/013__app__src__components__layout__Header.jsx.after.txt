import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import LanguageSelector from '../common/LanguageSelector';
import './Header.css';

const Header = () => {
  const { t } = useTranslation('common');
  const { user, logout } = useAuth();
  const { currentLanguageInfo } = useLanguage();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <header className="header">
      <div className="header-container">
        <div className="header-left">
          <Link to="/" className="header-logo">
            <span className="logo-icon">📝</span>
            <span className="logo-text">{t('app_name')}</span>
          </Link>
        </div>

        <nav className="header-nav">
          <Link 
            to="/" 
            className={`nav-link ${isActive('/') ? 'active' : ''}`}
          >
            {t('nav.home')}
          </Link>
          
          {user && (
            <Link 
              to="/todos" 
              className={`nav-link ${isActive('/todos') ? 'active' : ''}`}
            >
              {t('nav.todos')}
            </Link>
          )}
        </nav>

        <div className="header-right">
          <div className="language-section">
            <LanguageSelector />
          </div>
          
          {user ? (
            <div className="user-section">
              <div className="user-info">
                <span className="user-name">
                  {user.firstName || user.username}
                </span>
                <span className="user-language">
                  {currentLanguageInfo.flag} {currentLanguageInfo.nativeName}
                </span>
              </div>
              
              <div className="user-actions">
                <Link to="/profile" className="profile-link">
                  {t('nav.profile')}
                </Link>
                <button onClick={handleLogout} className="logout-btn">
                  {t('nav.logout')}
                </button>
              </div>
            </div>
          ) : (
            <div className="auth-section">
              <Link to="/login" className="auth-link login">
                {t('auth.login')}
              </Link>
              <Link to="/register" className="auth-link register">
                {t('auth.register')}
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
