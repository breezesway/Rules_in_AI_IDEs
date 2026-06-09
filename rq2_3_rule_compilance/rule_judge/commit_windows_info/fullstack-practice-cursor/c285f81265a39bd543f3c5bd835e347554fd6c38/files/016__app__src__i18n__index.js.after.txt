import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';

// Import translation files
import koKR from './locales/ko-KR/common.json';
import enUS from './locales/en-US/common.json';
import jaJP from './locales/ja-JP/common.json';
import esES from './locales/es-ES/common.json';
import frFR from './locales/fr-FR/common.json';
import deDE from './locales/de-DE/common.json';

// Import todo translations
import koKRTodo from './locales/ko-KR/todo.json';
import enUSTodo from './locales/en-US/todo.json';
import jaJPTodo from './locales/ja-JP/todo.json';
import esESTodo from './locales/es-ES/todo.json';
import frFRTodo from './locales/fr-FR/todo.json';
import deDETodo from './locales/de-DE/todo.json';

// Import auth translations
import koKRAuth from './locales/ko-KR/auth.json';
import enUSAuth from './locales/en-US/auth.json';
import jaJPAuth from './locales/ja-JP/auth.json';
import esESAuth from './locales/es-ES/auth.json';
import frFRAuth from './locales/fr-FR/auth.json';
import deDEAuth from './locales/de-DE/auth.json';

const resources = {
  'ko-KR': {
    common: koKR,
    todo: koKRTodo,
    auth: koKRAuth,
  },
  'en-US': {
    common: enUS,
    todo: enUSTodo,
    auth: enUSAuth,
  },
  'ja-JP': {
    common: jaJP,
    todo: jaJPTodo,
    auth: jaJPAuth,
  },
  'es-ES': {
    common: esES,
    todo: esESTodo,
    auth: esESAuth,
  },
  'fr-FR': {
    common: frFR,
    todo: frFRTodo,
    auth: frFRAuth,
  },
  'de-DE': {
    common: deDE,
    todo: deDETodo,
    auth: deDEAuth,
  },
};

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'ko-KR', // Korean as default
    debug: process.env.NODE_ENV === 'development',
    
    interpolation: {
      escapeValue: false, // React already escapes values
    },
    
    detection: {
      order: ['localStorage', 'sessionStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage', 'sessionStorage'],
    },
    
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
    
    ns: ['common', 'todo', 'auth'],
    defaultNS: 'common',
  });

export default i18n;
