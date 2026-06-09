import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../context/AuthContext';
import './HomePage.css';

const HomePage = () => {
  const { t } = useTranslation('common');
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>{t('loading')}</p>
      </div>
    );
  }

  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title">{t('home.title')}</h1>
        <p className="home-description">
          {t('home.description')}
        </p>
        
        {isAuthenticated ? (
          <div className="authenticated-actions">
            <Link to="/todos" className="btn btn-primary">
              {t('home.go_to_todos')}
            </Link>
            <Link to="/login-success" className="btn btn-secondary">
              {t('home.view_profile')}
            </Link>
          </div>
        ) : (
          <div className="guest-actions">
            <Link to="/login" className="btn btn-primary">
              {t('home.login')}
            </Link>
            <Link to="/register" className="btn btn-secondary">
              {t('home.register')}
            </Link>
          </div>
        )}
        
        <div className="features">
          <h2>{t('home.features')}</h2>
          <ul>
            <li>{t('home.feature_jwt')}</li>
            <li>{t('home.feature_email')}</li>
            <li>{t('home.feature_todo')}</li>
            <li>{t('home.feature_responsive')}</li>
            <li>{t('home.feature_realtime')}</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
