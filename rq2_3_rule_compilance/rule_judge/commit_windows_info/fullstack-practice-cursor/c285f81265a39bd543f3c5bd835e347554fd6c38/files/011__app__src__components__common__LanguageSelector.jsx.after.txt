import React from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSelector.css';

const LanguageSelector = () => {
  const { i18n, t } = useTranslation();

  const languages = [
    { code: 'ko-KR', name: '한국어', nativeName: '한국어' },
    { code: 'en-US', name: 'English', nativeName: 'English' },
    { code: 'ja-JP', name: '日本語', nativeName: '日本語' },
    { code: 'es-ES', name: 'Español', nativeName: 'Español' },
    { code: 'fr-FR', name: 'Français', nativeName: 'Français' },
    { code: 'de-DE', name: 'Deutsch', nativeName: 'Deutsch' }
  ];

  const handleLanguageChange = (languageCode) => {
    i18n.changeLanguage(languageCode);
    localStorage.setItem('i18nextLng', languageCode);
  };

  const getCurrentLanguage = () => {
    return languages.find(lang => lang.code === i18n.language) || languages[0];
  };

  return (
    <div className="language-selector">
      <div className="language-selector__current">
        <span className="language-selector__label">{t('language')}:</span>
        <span className="language-selector__current-name">
          {getCurrentLanguage().nativeName}
        </span>
      </div>
      
      <div className="language-selector__dropdown">
        <button className="language-selector__button">
          <span>{t('select_language')}</span>
          <svg className="language-selector__arrow" viewBox="0 0 24 24">
            <path d="M7 10l5 5 5-5z" />
          </svg>
        </button>
        
        <div className="language-selector__menu">
          {languages.map((language) => (
            <button
              key={language.code}
              className={`language-selector__option ${
                i18n.language === language.code ? 'language-selector__option--active' : ''
              }`}
              onClick={() => handleLanguageChange(language.code)}
            >
              <span className="language-selector__option-native">{language.nativeName}</span>
              <span className="language-selector__option-english">({language.name})</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LanguageSelector;
