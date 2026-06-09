import { HtmlSnapshot } from '../scanner';

export interface TechnicalSeoResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    performance: {
      loadTime: number;
      pageSize: number;
      resourceCount: number;
      metrics: {
        fcp?: number; // First Contentful Paint
        lcp?: number; // Largest Contentful Paint
        fid?: number; // First Input Delay
        cls?: number; // Cumulative Layout Shift
      };
    };
    mobileFriendly: {
      isMobileFriendly: boolean;
      viewport: boolean;
      responsiveImages: boolean;
      touchElements: boolean;
      fontSize: boolean;
      issues: string[];
    };
    security: {
      headers: {
        [key: string]: {
          present: boolean;
          value?: string;
        };
      };
      ssl: boolean;
      hsts: boolean;
      xss: boolean;
      csrf: boolean;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeTechnicalSeo(htmlSnapshot: HtmlSnapshot | null): TechnicalSeoResult {
  const result: TechnicalSeoResult = {
    score: 0,
    maxScore: 25,
    status: 'success',
    details: {
      performance: {
        loadTime: 0,
        pageSize: 0,
        resourceCount: 0,
        metrics: {},
      },
      mobileFriendly: {
        isMobileFriendly: false,
        viewport: false,
        responsiveImages: false,
        touchElements: false,
        fontSize: false,
        issues: [],
      },
      security: {
        headers: {
          'Content-Security-Policy': { present: false },
          'X-Frame-Options': { present: false },
          'X-Content-Type-Options': { present: false },
          'Referrer-Policy': { present: false },
          'Permissions-Policy': { present: false },
        },
        ssl: false,
        hsts: false,
        xss: false,
        csrf: false,
      },
    },
    fixes: [],
  };

  if (!htmlSnapshot) {
    result.status = 'danger';
    return result;
  }

  // Performance analyse
  const performanceResult = analyzePerformance(htmlSnapshot);
  result.details.performance = performanceResult;

  // Score voor performance
  if (performanceResult.loadTime < 2000) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'high',
      description: `Laadtijd (${performanceResult.loadTime}ms) is te hoog.`,
      fix: 'Optimaliseer de laadtijd door resources te comprimeren, caching te implementeren en onnodige scripts te verwijderen.',
    });
  }

  if (performanceResult.pageSize < 500000) {
    // 500KB
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: `Pagina grootte (${(performanceResult.pageSize / 1024).toFixed(
        1
      )}KB) is te groot.`,
      fix: 'Verklein de pagina door afbeeldingen te optimaliseren, CSS/JS te minificeren en onnodige content te verwijderen.',
    });
  }

  // Mobile-friendliness analyse
  const mobileResult = analyzeMobileFriendly(htmlSnapshot);
  result.details.mobileFriendly = mobileResult;

  if (mobileResult.isMobileFriendly) {
    result.score += 10;
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Pagina is niet volledig mobiel-vriendelijk.',
      fix: 'Los de volgende problemen op: ' + mobileResult.issues.join(', '),
    });
  }

  // Security analyse
  const securityResult = analyzeSecurity(htmlSnapshot);
  result.details.security = securityResult;

  if (securityResult.ssl && securityResult.hsts) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'SSL/TLS configuratie is niet optimaal.',
      fix: 'Implementeer HTTPS en HSTS voor betere beveiliging.',
    });
  }

  // Bepaal status
  if (result.score >= 20) {
    result.status = 'success';
  } else if (result.score >= 10) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

function analyzePerformance(
  htmlSnapshot: HtmlSnapshot
): TechnicalSeoResult['details']['performance'] {
  const content = htmlSnapshot.content;

  // Bereken pagina grootte
  const pageSize = new Blob([content]).size;

  // Tel resources
  const resourceCount =
    (content.match(/<link[^>]*>/g) || []).length +
    (content.match(/<script[^>]*>/g) || []).length +
    (content.match(/<img[^>]*>/g) || []).length;

  // Simuleer laadtijd (in een echte implementatie zou dit via Lighthouse of WebPageTest komen)
  const loadTime = Math.min(3000, 500 + pageSize / 1000 + resourceCount * 50);

  // Simuleer Core Web Vitals (in een echte implementatie zou dit via Lighthouse komen)
  const metrics = {
    fcp: Math.min(2000, 500 + pageSize / 2000),
    lcp: Math.min(2500, 1000 + pageSize / 1500),
    fid: Math.min(100, 20 + resourceCount * 2),
    cls: Math.min(0.25, 0.1 + resourceCount * 0.01),
  };

  return {
    loadTime,
    pageSize,
    resourceCount,
    metrics,
  };
}

function analyzeMobileFriendly(
  htmlSnapshot: HtmlSnapshot
): TechnicalSeoResult['details']['mobileFriendly'] {
  const content = htmlSnapshot.content;
  const issues: string[] = [];

  // Check viewport
  const hasViewport = content.includes('<meta name="viewport"');
  if (!hasViewport) {
    issues.push('Geen viewport meta tag');
  }

  // Check responsive images
  const hasResponsiveImages = content.includes('srcset=') || content.includes('sizes=');
  if (!hasResponsiveImages) {
    issues.push('Geen responsive afbeeldingen');
  }

  // Check touch elements
  const hasTouchElements = content.includes('touch-action') || content.includes('cursor: pointer');
  if (!hasTouchElements) {
    issues.push('Geen touch-vriendelijke elementen');
  }

  // Check font size
  const hasFontSize = content.includes('font-size:') || content.includes('font-size:');
  if (!hasFontSize) {
    issues.push('Geen expliciete font groottes');
  }

  return {
    isMobileFriendly: issues.length === 0,
    viewport: hasViewport,
    responsiveImages: hasResponsiveImages,
    touchElements: hasTouchElements,
    fontSize: hasFontSize,
    issues,
  };
}

function analyzeSecurity(htmlSnapshot: HtmlSnapshot): TechnicalSeoResult['details']['security'] {
  const content = htmlSnapshot.content;
  const headers = {
    'Content-Security-Policy': { present: false },
    'X-Frame-Options': { present: false },
    'X-Content-Type-Options': { present: false },
    'Referrer-Policy': { present: false },
    'Permissions-Policy': { present: false },
  };

  // Check security headers in meta tags
  if (content.includes('Content-Security-Policy')) {
    headers['Content-Security-Policy'].present = true;
  }
  if (content.includes('X-Frame-Options')) {
    headers['X-Frame-Options'].present = true;
  }
  if (content.includes('X-Content-Type-Options')) {
    headers['X-Content-Type-Options'].present = true;
  }
  if (content.includes('Referrer-Policy')) {
    headers['Referrer-Policy'].present = true;
  }
  if (content.includes('Permissions-Policy')) {
    headers['Permissions-Policy'].present = true;
  }

  // Simuleer SSL en HSTS (in een echte implementatie zou dit via de response headers komen)
  const ssl = true; // Aanname: we krijgen alleen HTTPS URLs
  const hsts = content.includes('Strict-Transport-Security');

  // Check voor XSS kwetsbaarheden
  const xss = !content.includes('onerror=') && !content.includes('onload=');

  // Check voor CSRF bescherming
  const csrf = content.includes('csrf-token') || content.includes('X-CSRF-Token');

  return {
    headers,
    ssl,
    hsts,
    xss,
    csrf,
  };
}
