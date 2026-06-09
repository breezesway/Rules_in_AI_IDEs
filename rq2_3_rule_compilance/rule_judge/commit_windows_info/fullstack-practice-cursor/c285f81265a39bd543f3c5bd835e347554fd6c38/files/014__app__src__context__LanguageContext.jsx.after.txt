import React, { createContext, useContext, useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const { i18n } = useTranslation();
  const [currentLanguage, setCurrentLanguage] = useState('ko-KR');
  const [isLoading, setIsLoading] = useState(false);

  const supportedLanguages = [
    { 
      code: 'ko-KR', 
      name: '한국어', 
      nativeName: '한국어', 
      direction: 'ltr', 
      dateFormat: 'yyyy년 MM월 dd일', 
      timeFormat: '24h', 
      currency: 'KRW', 
      isDefault: true,
      flag: '🇰🇷'
    },
    { 
      code: 'en-US', 
      name: 'English', 
      nativeName: 'English', 
      direction: 'ltr', 
      dateFormat: 'MM/dd/yyyy', 
      timeFormat: '12h', 
      currency: 'USD', 
      isDefault: false,
      flag: '🇺🇸'
    },
    { 
      code: 'ja-JP', 
      name: 'Japanese', 
      nativeName: '日本語', 
      direction: 'ltr', 
      dateFormat: 'yyyy年MM月dd日', 
      timeFormat: '24h', 
      currency: 'JPY', 
      isDefault: false,
      flag: '🇯🇵'
    },
    { 
      code: 'es-ES', 
      name: 'Spanish', 
      nativeName: 'Español', 
      direction: 'ltr', 
      dateFormat: 'dd/MM/yyyy', 
      timeFormat: '24h', 
      currency: 'EUR', 
      isDefault: false,
      flag: '🇪🇸'
    },
    { 
      code: 'fr-FR', 
      name: 'French', 
      nativeName: 'Français', 
      direction: 'ltr', 
      dateFormat: 'dd/MM/yyyy', 
      timeFormat: '24h', 
      currency: 'EUR', 
      isDefault: false,
      flag: '🇫🇷'
    },
    { 
      code: 'de-DE', 
      name: 'German', 
      nativeName: 'Deutsch', 
      direction: 'ltr', 
      dateFormat: 'dd.MM.yyyy', 
      timeFormat: '24h', 
      currency: 'EUR', 
      isDefault: false,
      flag: '🇩🇪'
    }
  ];

  // Get current language info
  const getCurrentLanguageInfo = () => {
    return supportedLanguages.find(lang => lang.code === currentLanguage) || supportedLanguages[0];
  };

  // Change language
  const changeLanguage = async (languageCode) => {
    if (!supportedLanguages.find(lang => lang.code === languageCode)) {
      throw new Error(`Unsupported language: ${languageCode}`);
    }

    setIsLoading(true);
    try {
      await i18n.changeLanguage(languageCode);
      setCurrentLanguage(languageCode);
      localStorage.setItem('i18nextLng', languageCode);
      
      // Update document direction if needed
      const languageInfo = supportedLanguages.find(lang => lang.code === languageCode);
      if (languageInfo && languageInfo.direction) {
        document.documentElement.dir = languageInfo.direction;
      }
      
      // Update document language attribute
      document.documentElement.lang = languageCode;
      
      return true;
    } catch (error) {
      console.error('Failed to change language:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  // Initialize language from storage or browser
  const initializeLanguage = async () => {
    const storedLanguage = localStorage.getItem('i18nextLng');
    const browserLanguage = navigator.language || navigator.userLanguage;
    
    let targetLanguage = 'ko-KR'; // Default to Korean
    
    if (storedLanguage && supportedLanguages.find(lang => lang.code === storedLanguage)) {
      targetLanguage = storedLanguage;
    } else if (browserLanguage) {
      // Try to find a matching language
      const browserLangCode = browserLanguage.split('-')[0];
      const matchingLanguage = supportedLanguages.find(lang => 
        lang.code.startsWith(browserLangCode) || 
        lang.code.toLowerCase().includes(browserLangCode.toLowerCase())
      );
      
      if (matchingLanguage) {
        targetLanguage = matchingLanguage.code;
      }
    }
    
    await changeLanguage(targetLanguage);
  };

  // Reset to default language (Korean)
  const resetToDefault = async () => {
    return await changeLanguage('ko-KR');
  };

  // Get language-specific formatting options
  const getLanguageFormatting = () => {
    const langInfo = getCurrentLanguageInfo();
    return {
      dateFormat: langInfo.dateFormat,
      timeFormat: langInfo.timeFormat,
      currency: langInfo.currency,
      direction: langInfo.direction
    };
  };

  // Check if current language is RTL
  const isRTL = () => {
    const langInfo = getCurrentLanguageInfo();
    return langInfo.direction === 'rtl';
  };

  // Initialize on mount
  useEffect(() => {
    initializeLanguage();
  }, []);

  // Update current language when i18n language changes
  useEffect(() => {
    setCurrentLanguage(i18n.language || 'ko-KR');
  }, [i18n.language]);

  const value = {
    currentLanguage,
    currentLanguageInfo: getCurrentLanguageInfo(),
    supportedLanguages,
    isLoading,
    changeLanguage,
    resetToDefault,
    getLanguageFormatting,
    isRTL,
    initializeLanguage
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};
