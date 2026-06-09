import { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';

export const useLanguage = () => {
  const { i18n } = useTranslation();
  const [currentLanguage, setCurrentLanguage] = useState('ko-KR');
  const [isLoading, setIsLoading] = useState(false);

  const languages = [
    { code: 'ko-KR', name: '한국어', nativeName: '한국어', direction: 'ltr', dateFormat: 'yyyy년 MM월 dd일', timeFormat: '24h', currency: 'KRW', isDefault: true },
    { code: 'en-US', name: 'English', nativeName: 'English', direction: 'ltr', dateFormat: 'MM/dd/yyyy', timeFormat: '12h', currency: 'USD', isDefault: false },
    { code: 'ja-JP', name: 'Japanese', nativeName: '日本語', direction: 'ltr', dateFormat: 'yyyy年MM月dd日', timeFormat: '24h', currency: 'JPY', isDefault: false },
    { code: 'es-ES', name: 'Spanish', nativeName: 'Español', direction: 'ltr', dateFormat: 'dd/MM/yyyy', timeFormat: '24h', currency: 'EUR', isDefault: false },
    { code: 'fr-FR', name: 'French', nativeName: 'Français', direction: 'ltr', dateFormat: 'dd/MM/yyyy', timeFormat: '24h', currency: 'EUR', isDefault: false },
    { code: 'de-DE', name: 'German', nativeName: 'Deutsch', direction: 'ltr', dateFormat: 'dd.MM.yyyy', timeFormat: '24h', currency: 'EUR', isDefault: false }
  ];

  // Get current language info
  const getCurrentLanguageInfo = useCallback(() => {
    return languages.find(lang => lang.code === currentLanguage) || languages[0];
  }, [currentLanguage]);

  // Get supported languages
  const getSupportedLanguages = useCallback(() => {
    return languages;
  }, []);

  // Change language
  const changeLanguage = useCallback(async (languageCode) => {
    if (!languages.find(lang => lang.code === languageCode)) {
      throw new Error(`Unsupported language: ${languageCode}`);
    }

    setIsLoading(true);
    try {
      await i18n.changeLanguage(languageCode);
      setCurrentLanguage(languageCode);
      localStorage.setItem('i18nextLng', languageCode);
      
      // Update document direction if needed
      const languageInfo = languages.find(lang => lang.code === languageCode);
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
  }, [i18n, languages]);

  // Initialize language from storage or browser
  const initializeLanguage = useCallback(() => {
    const storedLanguage = localStorage.getItem('i18nextLng');
    const browserLanguage = navigator.language || navigator.userLanguage;
    
    let targetLanguage = 'ko-KR'; // Default to Korean
    
    if (storedLanguage && languages.find(lang => lang.code === storedLanguage)) {
      targetLanguage = storedLanguage;
    } else if (browserLanguage) {
      // Try to find a matching language
      const browserLangCode = browserLanguage.split('-')[0];
      const matchingLanguage = languages.find(lang => 
        lang.code.startsWith(browserLangCode) || 
        lang.code.toLowerCase().includes(browserLangCode.toLowerCase())
      );
      
      if (matchingLanguage) {
        targetLanguage = matchingLanguage.code;
      }
    }
    
    changeLanguage(targetLanguage);
  }, [changeLanguage, languages]);

  // Reset to default language (Korean)
  const resetToDefault = useCallback(() => {
    return changeLanguage('ko-KR');
  }, [changeLanguage]);

  // Get language-specific formatting options
  const getLanguageFormatting = useCallback(() => {
    const langInfo = getCurrentLanguageInfo();
    return {
      dateFormat: langInfo.dateFormat,
      timeFormat: langInfo.timeFormat,
      currency: langInfo.currency,
      direction: langInfo.direction
    };
  }, [getCurrentLanguageInfo]);

  // Check if current language is RTL
  const isRTL = useCallback(() => {
    const langInfo = getCurrentLanguageInfo();
    return langInfo.direction === 'rtl';
  }, [getCurrentLanguageInfo]);

  // Initialize on mount
  useEffect(() => {
    initializeLanguage();
  }, [initializeLanguage]);

  // Update current language when i18n language changes
  useEffect(() => {
    setCurrentLanguage(i18n.language || 'ko-KR');
  }, [i18n.language]);

  return {
    currentLanguage,
    currentLanguageInfo: getCurrentLanguageInfo(),
    supportedLanguages: getSupportedLanguages(),
    isLoading,
    changeLanguage,
    resetToDefault,
    getLanguageFormatting,
    isRTL,
    initializeLanguage
  };
};
