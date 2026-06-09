'use client';

import { useState, useEffect } from 'react';

// Type om bekende feature flags te definiëren
type FeatureFlag = 'enhancedUI' | 'pdf-export' | 'advanced-analytics';

/**
 * Hook om feature flags te controleren
 * @param flag - De naam van de feature flag om te controleren
 * @param defaultValue - Optionele standaardwaarde als de flag niet gevonden wordt
 * @returns Boolean die aangeeft of de feature actief is
 */
export function useFeatureFlag(flag: FeatureFlag, defaultValue: boolean = false): boolean {
  const [isEnabled, setIsEnabled] = useState<boolean>(defaultValue);

  useEffect(() => {
    // In een echte applicatie zou dit een API call of lokale storage check kunnen zijn
    const flags: Record<FeatureFlag, boolean> = {
      enhancedUI: true, // Altijd aan voor deze demo
      'pdf-export': false,
      'advanced-analytics': false,
    };

    setIsEnabled(flags[flag] ?? defaultValue);
  }, [flag, defaultValue]);

  return isEnabled;
}
