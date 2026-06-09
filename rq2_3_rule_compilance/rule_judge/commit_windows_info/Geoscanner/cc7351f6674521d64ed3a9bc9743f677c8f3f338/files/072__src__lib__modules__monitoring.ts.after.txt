import { HtmlSnapshot } from '../scanner';

export interface MonitoringResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    analytics: {
      hasGoogleAnalytics: boolean;
      hasMicrosoftClarity: boolean;
      hasMatomo: boolean;
      hasOtherAnalytics: boolean;
      tools: string[];
    };
    monitoring: {
      hasRealUserMonitoring: boolean;
      hasErrorTracking: boolean;
      hasPerformanceMonitoring: boolean;
      tools: string[];
    };
    dataCollection: {
      hasConsent: boolean;
      hasCookieBanner: boolean;
      hasPrivacyControls: boolean;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeMonitoring(htmlSnapshot: HtmlSnapshot | null): MonitoringResult {
  const result: MonitoringResult = {
    score: 0,
    maxScore: 5,
    status: 'danger',
    details: {
      analytics: {
        hasGoogleAnalytics: false,
        hasMicrosoftClarity: false,
        hasMatomo: false,
        hasOtherAnalytics: false,
        tools: [],
      },
      monitoring: {
        hasRealUserMonitoring: false,
        hasErrorTracking: false,
        hasPerformanceMonitoring: false,
        tools: [],
      },
      dataCollection: {
        hasConsent: false,
        hasCookieBanner: false,
        hasPrivacyControls: false,
      },
    },
    fixes: [],
  };

  if (!htmlSnapshot) {
    return {
      ...result,
      fixes: [
        {
          impact: 'high',
          description: 'Geen HTML snapshot beschikbaar',
          fix: 'Controleer of de URL correct is en de pagina toegankelijk is',
        },
      ],
    };
  }

  const html = htmlSnapshot.content;

  // 1. Analytics tools analyseren
  const analyticsAnalysis = analyzeAnalytics(html);
  result.details.analytics = analyticsAnalysis;

  // Score berekenen op basis van analytics
  if (
    analyticsAnalysis.hasGoogleAnalytics ||
    analyticsAnalysis.hasMicrosoftClarity ||
    analyticsAnalysis.hasMatomo ||
    analyticsAnalysis.hasOtherAnalytics
  ) {
    // 2 punten voor analytics
    result.score += 2;
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen analytics tools gevonden',
      fix: `Voeg analytics tracking toe, bijvoorbeeld Google Analytics:
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>`,
    });
  }

  // 2. Monitoring tools analyseren
  const monitoringAnalysis = analyzeMonitoringTools(html);
  result.details.monitoring = monitoringAnalysis;

  // Score berekenen op basis van monitoring
  let monitoringScore = 0;
  if (monitoringAnalysis.hasRealUserMonitoring) monitoringScore += 1;
  if (monitoringAnalysis.hasErrorTracking) monitoringScore += 0.5;
  if (monitoringAnalysis.hasPerformanceMonitoring) monitoringScore += 0.5;

  // Max 2 punten voor monitoring
  result.score += Math.min(2, monitoringScore);

  if (monitoringScore === 0) {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen monitoring tools gevonden',
      fix: 'Overweeg het toevoegen van error tracking (zoals Sentry) en real user monitoring (zoals New Relic) om problemen tijdig te detecteren',
    });
  }

  // 3. Data collection en privacy analyseren
  const dataCollectionAnalysis = analyzeDataCollection(html);
  result.details.dataCollection = dataCollectionAnalysis;

  // Score berekenen op basis van privacy
  let privacyScore = 0;
  if (dataCollectionAnalysis.hasConsent) privacyScore += 0.5;
  if (dataCollectionAnalysis.hasCookieBanner) privacyScore += 0.25;
  if (dataCollectionAnalysis.hasPrivacyControls) privacyScore += 0.25;

  // Max 1 punt voor privacycontroles
  result.score += Math.min(1, privacyScore);

  if (!dataCollectionAnalysis.hasConsent || !dataCollectionAnalysis.hasCookieBanner) {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen cookie consent functionaliteit gevonden',
      fix: 'Implementeer een cookie consent banner om te voldoen aan privacywetgeving zoals GDPR/AVG',
    });
  }

  // Bepaal status op basis van score
  if (result.score >= 4) {
    result.status = 'success';
  } else if (result.score >= 2) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Hulpfuncties

function analyzeAnalytics(html: string): MonitoringResult['details']['analytics'] {
  const result = {
    hasGoogleAnalytics: false,
    hasMicrosoftClarity: false,
    hasMatomo: false,
    hasOtherAnalytics: false,
    tools: [] as string[],
  };

  // Controleer Google Analytics
  const gaPatterns = [
    /google-analytics\.com\/analytics\.js/i,
    /googletagmanager\.com\/gtag/i,
    /gtag\('config'/i,
    /ga\('create'/i,
    /_gaq\.push/i,
  ];

  for (const pattern of gaPatterns) {
    if (pattern.test(html)) {
      result.hasGoogleAnalytics = true;
      if (!result.tools.includes('Google Analytics')) {
        result.tools.push('Google Analytics');
      }
      break;
    }
  }

  // Controleer Microsoft Clarity
  if (/clarity\.ms\/tag/i.test(html)) {
    result.hasMicrosoftClarity = true;
    result.tools.push('Microsoft Clarity');
  }

  // Controleer Matomo (voorheen Piwik)
  const matomoPatterns = [/matomo\.js/i, /piwik\.js/i, /_paq\.push/i];

  for (const pattern of matomoPatterns) {
    if (pattern.test(html)) {
      result.hasMatomo = true;
      if (!result.tools.includes('Matomo')) {
        result.tools.push('Matomo');
      }
      break;
    }
  }

  // Controleer andere analytics tools
  const otherAnalyticsPatterns = [
    { pattern: /plausible\.io/i, name: 'Plausible' },
    { pattern: /analytics\.tiktok\.com/i, name: 'TikTok Analytics' },
    { pattern: /connect\.facebook\.net.*fbevents\.js/i, name: 'Facebook Pixel' },
    { pattern: /snap\.licdn\.com/i, name: 'LinkedIn Insight Tag' },
    { pattern: /static\.hotjar\.com/i, name: 'Hotjar' },
    { pattern: /js\.hs-scripts\.com/i, name: 'HubSpot' },
    { pattern: /sc-static\.net/i, name: 'Snapchat Pixel' },
    { pattern: /cdn\.amplitude\.com/i, name: 'Amplitude' },
    { pattern: /cdn\.heapanalytics\.com/i, name: 'Heap' },
  ];

  for (const { pattern, name } of otherAnalyticsPatterns) {
    if (pattern.test(html)) {
      result.hasOtherAnalytics = true;
      if (!result.tools.includes(name)) {
        result.tools.push(name);
      }
    }
  }

  return result;
}

function analyzeMonitoringTools(html: string): MonitoringResult['details']['monitoring'] {
  const result = {
    hasRealUserMonitoring: false,
    hasErrorTracking: false,
    hasPerformanceMonitoring: false,
    tools: [] as string[],
  };

  // Controleer RUM tools
  const rumPatterns = [
    { pattern: /newrelic\.com/i, name: 'New Relic' },
    { pattern: /dynatrace\.com/i, name: 'Dynatrace' },
    { pattern: /cdn\.datadog\.com/i, name: 'Datadog RUM' },
    { pattern: /cdn\.logrocket\.com/i, name: 'LogRocket' },
    { pattern: /fullstory\.com/i, name: 'FullStory' },
  ];

  for (const { pattern, name } of rumPatterns) {
    if (pattern.test(html)) {
      result.hasRealUserMonitoring = true;
      if (!result.tools.includes(name)) {
        result.tools.push(name);
      }
    }
  }

  // Controleer error tracking
  const errorTrackingPatterns = [
    { pattern: /browser\.sentry-cdn\.com/i, name: 'Sentry' },
    { pattern: /bugsnag\.com/i, name: 'Bugsnag' },
    { pattern: /rollbar\.com/i, name: 'Rollbar' },
    { pattern: /trackjs\.com/i, name: 'TrackJS' },
  ];

  for (const { pattern, name } of errorTrackingPatterns) {
    if (pattern.test(html)) {
      result.hasErrorTracking = true;
      if (!result.tools.includes(name)) {
        result.tools.push(name);
      }
    }
  }

  // Controleer performance monitoring
  const perfMonitoringPatterns = [
    { pattern: /web-vitals\.js/i, name: 'Web Vitals' },
    { pattern: /cdn\.speedcurve\.com/i, name: 'SpeedCurve' },
    { pattern: /rum-static\.pingdom\.net/i, name: 'Pingdom RUM' },
    { pattern: /boomerang\.js/i, name: 'Boomerang' },
  ];

  for (const { pattern, name } of perfMonitoringPatterns) {
    if (pattern.test(html)) {
      result.hasPerformanceMonitoring = true;
      if (!result.tools.includes(name)) {
        result.tools.push(name);
      }
    }
  }

  return result;
}

function analyzeDataCollection(html: string): MonitoringResult['details']['dataCollection'] {
  const result = {
    hasConsent: false,
    hasCookieBanner: false,
    hasPrivacyControls: false,
  };

  // Controleer voor consent management tools
  const consentPatterns = [
    /cookieconsent/i,
    /gdpr/i,
    /consent.*manager/i,
    /cookie.*consent/i,
    /consent.*mode/i,
    /osano\.com/i,
    /cookiebot\.com/i,
    /usercentrics\.eu/i,
    /onetrust\.com/i,
    /trustarc\.com/i,
    /consentmanager\.net/i,
  ];

  for (const pattern of consentPatterns) {
    if (pattern.test(html)) {
      result.hasConsent = true;
      break;
    }
  }

  // Controleer voor cookie banners
  const cookieBannerPatterns = [
    /cookie.*banner/i,
    /cookie.*dialog/i,
    /cookie.*notice/i,
    /cookie.*message/i,
    /cookie.*popup/i,
    /cookie.*modal/i,
    /cookie.*notif/i,
    /cookiemelding/i,
    /cookieverklaring/i,
  ];

  for (const pattern of cookieBannerPatterns) {
    if (pattern.test(html)) {
      result.hasCookieBanner = true;
      break;
    }
  }

  // Controleer voor privacy controls
  const privacyControlPatterns = [
    /privacy.*settings/i,
    /privacy.*control/i,
    /privacy.*preferences/i,
    /privacy.*options/i,
    /privacy.*dashboard/i,
    /data.*settings/i,
    /cookie.*preferences/i,
    /cookieinstellingen/i,
    /privacyinstellingen/i,
  ];

  for (const pattern of privacyControlPatterns) {
    if (pattern.test(html)) {
      result.hasPrivacyControls = true;
      break;
    }
  }

  return result;
}
