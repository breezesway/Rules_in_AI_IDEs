/**
 * Feature flags voor de GEO Scanner applicatie
 */

export const FEATURES = {
  NEW_RESULTS_UI: process.env.NEXT_PUBLIC_ENABLE_NEW_RESULTS_UI === 'true',
} as const;

export type FeatureKey = keyof typeof FEATURES;

/**
 * Controleert of een feature is ingeschakeld
 */
export const isFeatureEnabled = (feature: FeatureKey): boolean => {
  return FEATURES[feature] ?? false;
};

/**
 * Controleert of de nieuwe UI is ingeschakeld
 * Alleen afhankelijk van de environment variable
 */
export const isNewUIEnabled = (): boolean => {
  return FEATURES.NEW_RESULTS_UI;
};

/**
 * Schakelt de nieuwe UI in/uit voor de huidige gebruiker
 */
export const toggleNewUI = (enabled: boolean): void => {
  if (typeof window === 'undefined') return;

  window.localStorage.setItem('prefer-new-ui', enabled ? 'true' : 'false');
  // Trigger een page refresh om de wijziging door te voeren
  window.location.reload();
};
