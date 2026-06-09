import React from 'react';
import { useTranslation } from 'react-i18next';
import { useLanguage } from '../context/LanguageContext';
import LanguageSelector from '../components/common/LanguageSelector';
import './LanguageDemoPage.css';

const LanguageDemoPage = () => {
  const { t } = useTranslation();
  const { currentLanguage, currentLanguageInfo, supportedLanguages } = useLanguage();

  return (
    <div className="language-demo-page">
      <div className="demo-container">
        <header className="demo-header">
          <h1>🌍 {t('welcome')} - Multi-Language Demo</h1>
          <p>Experience the Todo app in multiple languages</p>
        </header>

        <section className="language-section">
          <h2>🔤 {t('language')} Selection</h2>
          <div className="language-selector-demo">
            <LanguageSelector />
          </div>
          
          <div className="current-language-info">
            <h3>Current Language: {currentLanguageInfo.flag} {currentLanguageInfo.nativeName}</h3>
            <div className="language-details">
              <p><strong>Code:</strong> {currentLanguageInfo.code}</p>
              <p><strong>Date Format:</strong> {currentLanguageInfo.dateFormat}</p>
              <p><strong>Time Format:</strong> {currentLanguageInfo.timeFormat}</p>
              <p><strong>Currency:</strong> {currentLanguageInfo.currency}</p>
              <p><strong>Direction:</strong> {currentLanguageInfo.direction}</p>
            </div>
          </div>
        </section>

        <section className="translation-examples">
          <h2>📝 Translation Examples</h2>
          
          <div className="example-grid">
            <div className="example-card">
              <h3>Common Phrases</h3>
              <ul>
                <li><strong>App Name:</strong> {t('app_name')}</li>
                <li><strong>Welcome:</strong> {t('welcome')}</li>
                <li><strong>Loading:</strong> {t('loading')}</li>
                <li><strong>Save:</strong> {t('save')}</li>
                <li><strong>Cancel:</strong> {t('cancel')}</li>
              </ul>
            </div>

            <div className="example-card">
              <h3>Todo Features</h3>
              <ul>
                <li><strong>Title:</strong> {t('todo:title')}</li>
                <li><strong>Create:</strong> {t('todo:form.create')}</li>
                <li><strong>Edit:</strong> {t('todo:form.update')}</li>
                <li><strong>Delete:</strong> {t('todo:actions.delete')}</li>
                <li><strong>Completed:</strong> {t('todo:status.completed')}</li>
              </ul>
            </div>

            <div className="example-card">
              <h3>Authentication</h3>
              <ul>
                <li><strong>Login:</strong> {t('auth:login.title')}</li>
                <li><strong>Register:</strong> {t('auth:register.title')}</li>
                <li><strong>Username:</strong> {t('auth:login.username')}</li>
                <li><strong>Password:</strong> {t('auth:login.password')}</li>
                <li><strong>Profile:</strong> {t('auth:profile.title')}</li>
              </ul>
            </div>

            <div className="example-card">
              <h3>Navigation</h3>
              <ul>
                <li><strong>Home:</strong> {t('nav.home', { defaultValue: 'Home' })}</li>
                <li><strong>Todos:</strong> {t('nav.todos', { defaultValue: 'Todos' })}</li>
                <li><strong>Profile:</strong> {t('nav.profile', { defaultValue: 'Profile' })}</li>
                <li><strong>Settings:</strong> {t('nav.settings', { defaultValue: 'Settings' })}</li>
                <li><strong>Logout:</strong> {t('nav.logout', { defaultValue: 'Logout' })}</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="supported-languages">
          <h2>🌐 Supported Languages</h2>
          <div className="languages-grid">
            {supportedLanguages.map((lang) => (
              <div 
                key={lang.code} 
                className={`language-card ${currentLanguage === lang.code ? 'active' : ''}`}
              >
                <div className="language-flag">{lang.flag}</div>
                <div className="language-info">
                  <h4>{lang.nativeName}</h4>
                  <p>{lang.name}</p>
                  <small>{lang.code}</small>
                  {lang.isDefault && <span className="default-badge">Default</span>}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="features-highlight">
          <h2>✨ Multi-Language Features</h2>
          <div className="features-list">
            <div className="feature-item">
              <span className="feature-icon">🇰🇷</span>
              <div>
                <h4>Korean as Default</h4>
                <p>Korean is the primary language with proper honorifics and cultural context</p>
              </div>
            </div>
            
            <div className="feature-item">
              <span className="feature-icon">🌍</span>
              <div>
                <h4>6 Supported Languages</h4>
                <p>Korean, English, Japanese, Spanish, French, and German</p>
              </div>
            </div>
            
            <div className="feature-item">
              <span className="feature-icon">💾</span>
              <div>
                <h4>Persistent Language</h4>
                <p>Language preference is saved and restored across sessions</p>
              </div>
            </div>
            
            <div className="feature-item">
              <span className="feature-icon">📱</span>
              <div>
                <h4>Responsive Design</h4>
                <p>Optimized for all devices with proper text expansion handling</p>
              </div>
            </div>
            
            <div className="feature-item">
              <span className="feature-icon">🎨</span>
              <div>
                <h4>Cultural Adaptation</h4>
                <p>Proper date formats, time formats, and currency for each locale</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default LanguageDemoPage;
