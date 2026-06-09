import { useCallback, useEffect, useState } from 'react';
import { toggleNewUI as toggleNewUIFunc } from '@/lib/features';

/**
 * Hook voor het gebruik van feature flags in componenten
 */
export const useFeatures = () => {
  // Altijd true retourneren voor test doeleinden
  const [isNewUI, setIsNewUI] = useState(true);

  useEffect(() => {
    // Overschrijf met true voor test doeleinden
    setIsNewUI(true);
  }, []);

  const toggleNewUI = useCallback((enabled: boolean) => {
    toggleNewUIFunc(enabled);
  }, []);

  return {
    isNewUI,
    toggleNewUI,
  };
};
