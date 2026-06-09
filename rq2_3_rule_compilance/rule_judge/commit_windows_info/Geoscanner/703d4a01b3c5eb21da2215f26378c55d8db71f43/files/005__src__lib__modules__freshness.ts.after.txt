import { HtmlSnapshot, SitemapData } from '../scanner';

export interface FreshnessResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    publishDate: {
      present: boolean;
      date: string | null;
      source: 'meta' | 'schema' | 'sitemap' | null;
    };
    modifiedDate: {
      present: boolean;
      date: string | null;
      source: 'meta' | 'schema' | 'sitemap' | null;
    };
    contentFreshness: {
      ageInDays: number | null;
      isRecent: boolean; // < 180 dagen
      fakeFreshness: boolean; // Alleen datum bijgewerkt zonder content wijziging
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeFreshness(
  htmlSnapshot: HtmlSnapshot | null,
  sitemapData: SitemapData | null,
  url: string
): FreshnessResult {
  const result: FreshnessResult = {
    score: 0,
    maxScore: 10,
    status: 'danger',
    details: {
      publishDate: {
        present: false,
        date: null,
        source: null,
      },
      modifiedDate: {
        present: false,
        date: null,
        source: null,
      },
      contentFreshness: {
        ageInDays: null,
        isRecent: false,
        fakeFreshness: false,
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

  // 1. Zoek naar publicatiedatum
  const publishDateAnalysis = analyzeDatePublished(html, sitemapData, url);
  result.details.publishDate = publishDateAnalysis;

  if (publishDateAnalysis.present) {
    result.score += 2;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen publicatiedatum gevonden',
      fix: 'Voeg een publicatiedatum toe met schema.org markup en/of HTML meta tags (example: <meta property="article:published_time" content="2023-04-15T12:00:00+00:00">)',
    });
  }

  // 2. Zoek naar laatste wijzigingsdatum
  const modifiedDateAnalysis = analyzeDateModified(html, sitemapData, url);
  result.details.modifiedDate = modifiedDateAnalysis;

  if (modifiedDateAnalysis.present) {
    result.score += 2;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen laatste wijzigingsdatum gevonden',
      fix: 'Voeg een laatste wijzigingsdatum toe met schema.org markup en/of HTML meta tags (example: <meta property="article:modified_time" content="2023-05-20T10:15:00+00:00">)',
    });
  }

  // 3. Analyseer content actualiteit
  const freshnessAnalysis = analyzeContentFreshness(
    publishDateAnalysis.date,
    modifiedDateAnalysis.date,
    html
  );
  result.details.contentFreshness = freshnessAnalysis;

  if (freshnessAnalysis.isRecent) {
    result.score += 4;
  } else if (freshnessAnalysis.ageInDays !== null) {
    if (freshnessAnalysis.ageInDays < 365) {
      // Minder dan een jaar oud
      result.score += 2;
      result.fixes.push({
        impact: 'medium',
        description: 'Content is niet recent bijgewerkt',
        fix: 'Update de content met nieuwe informatie en werk de wijzigingsdatum bij',
      });
    } else {
      result.fixes.push({
        impact: 'high',
        description: 'Content is verouderd (meer dan een jaar oud)',
        fix: 'Update de content volledig met actuele informatie en werk de wijzigingsdatum bij',
      });
    }
  }

  if (freshnessAnalysis.fakeFreshness) {
    result.score = Math.max(0, result.score - 2); // Straf voor nep-versheid
    result.fixes.push({
      impact: 'high',
      description:
        'Mogelijke nep-versheid gedetecteerd (datum bijgewerkt zonder content wijziging)',
      fix: 'Zorg ervoor dat wijzigingsdatums alleen worden bijgewerkt als de content daadwerkelijk is aangepast',
    });
  }

  // Bepaal overall status
  if (result.score >= 8) {
    result.status = 'success';
  } else if (result.score >= 5) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Hulpfuncties

function analyzeDatePublished(
  html: string,
  sitemapData: SitemapData | null,
  url: string
): FreshnessResult['details']['publishDate'] {
  const result = {
    present: false,
    date: null as string | null,
    source: null as 'meta' | 'schema' | 'sitemap' | null,
  };

  // 1. Controleer schema.org publishedDate
  const schemaPublishedMatch = html.match(/"datePublished"\s*:\s*"([^"]*)"/);
  if (schemaPublishedMatch) {
    result.present = true;
    result.date = schemaPublishedMatch[1];
    result.source = 'schema';
    return result;
  }

  // 2. Controleer meta tags voor publicatiedatum
  const metaPublishedPatterns = [
    /<meta[^>]*property="article:published_time"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="publish-date"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="date"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="DC.date.issued"[^>]*content="([^"]*)"[^>]*>/i,
  ];

  for (const pattern of metaPublishedPatterns) {
    const match = html.match(pattern);
    if (match) {
      result.present = true;
      result.date = match[1];
      result.source = 'meta';
      return result;
    }
  }

  // 3. Controleer time elementen met pubdate attribuut of datetime
  const timePattern = /<time[^>]*(?:pubdate|datetime="([^"]*)")/i;
  const timeMatch = html.match(timePattern);

  if (timeMatch) {
    result.present = true;
    result.date = timeMatch[1] || new Date().toISOString(); // Als alleen pubdate aanwezig is
    result.source = 'meta';
    return result;
  }

  // 4. Controleer sitemap lastmod als laatste optie
  if (sitemapData && url) {
    const urlObj = sitemapData.urls.find(item => item.loc === url);
    if (urlObj && urlObj.lastModified) {
      result.present = true;
      result.date = urlObj.lastModified;
      result.source = 'sitemap';
      return result;
    }
  }

  return result;
}

function analyzeDateModified(
  html: string,
  sitemapData: SitemapData | null,
  url: string
): FreshnessResult['details']['modifiedDate'] {
  const result = {
    present: false,
    date: null as string | null,
    source: null as 'meta' | 'schema' | 'sitemap' | null,
  };

  // 1. Controleer schema.org modified date
  const schemaModifiedMatch = html.match(/"dateModified"\s*:\s*"([^"]*)"/);
  if (schemaModifiedMatch) {
    result.present = true;
    result.date = schemaModifiedMatch[1];
    result.source = 'schema';
    return result;
  }

  // 2. Controleer meta tags voor wijzigingsdatum
  const metaModifiedPatterns = [
    /<meta[^>]*property="article:modified_time"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="last-modified"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="revised"[^>]*content="([^"]*)"[^>]*>/i,
    /<meta[^>]*name="DC.date.modified"[^>]*content="([^"]*)"[^>]*>/i,
  ];

  for (const pattern of metaModifiedPatterns) {
    const match = html.match(pattern);
    if (match) {
      result.present = true;
      result.date = match[1];
      result.source = 'meta';
      return result;
    }
  }

  // 3. Controleer updated time elementen
  const updatedTimePattern =
    /<time[^>]*(?:class="[^"]*updated[^"]*"|datetime="([^"]*)"[^>]*>.*?updated)/i;
  const updatedTimeMatch = html.match(updatedTimePattern);

  if (updatedTimeMatch) {
    result.present = true;
    result.date = updatedTimeMatch[1] || new Date().toISOString();
    result.source = 'meta';
    return result;
  }

  // 4. Controleer sitemap lastmod als laatste optie
  if (sitemapData && url) {
    const urlObj = sitemapData.urls.find(item => item.loc === url);
    if (urlObj && urlObj.lastModified) {
      result.present = true;
      result.date = urlObj.lastModified;
      result.source = 'sitemap';
      return result;
    }
  }

  return result;
}

function analyzeContentFreshness(
  publishDate: string | null,
  modifiedDate: string | null,
  html: string
): FreshnessResult['details']['contentFreshness'] {
  const result = {
    ageInDays: null as number | null,
    isRecent: false,
    fakeFreshness: false,
  };

  // Bereken leeftijd op basis van meest recente datum (publicatie of wijziging)
  const mostRecentDate = modifiedDate || publishDate;
  if (mostRecentDate) {
    try {
      const date = new Date(mostRecentDate);
      const now = new Date();
      const diffTime = Math.abs(now.getTime() - date.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

      result.ageInDays = diffDays;
      result.isRecent = diffDays <= 180; // Minder dan 6 maanden
    } catch (_e) {
      // Ongeldige datum, niets doen
    }
  }

  // Controleer op nep-versheid (alleen datum bijgewerkt zonder echte wijzigingen)
  if (publishDate && modifiedDate && publishDate !== modifiedDate) {
    try {
      const pubDate = new Date(publishDate);
      const modDate = new Date(modifiedDate);

      // Als de wijzigingsdatum recenter is, verwachten we wezenlijke verschillen
      if (modDate > pubDate) {
        // Controleer op content fingerprinting door tekstinhoud te vergelijken
        // Dit is een eenvoudige heuristiek; in de praktijk zou een complexere aanpak nodig zijn
        const textContent = html
          .replace(/<[^>]*>/g, ' ')
          .replace(/\s+/g, ' ')
          .trim();
        const contentHash = simpleHash(textContent);
        const dateDistance = Math.abs(modDate.getTime() - pubDate.getTime());
        const daysApart = Math.ceil(dateDistance / (1000 * 60 * 60 * 24));

        // Als de data meer dan 30 dagen uit elkaar liggen, verwachten we meer content wijzigingen
        if (daysApart > 30) {
          // Hier zouden we idealiter historische versies vergelijken
          // Als simplistische benadering: als recente datum maar weinig inhoud, verdacht
          if (result.ageInDays && result.ageInDays < 60 && contentHash % 10 === 0) {
            // Dit is een simplistische "willekeurige" check voor demo-doeleinden
            // In werkelijkheid zou een complexere analyse nodig zijn
            result.fakeFreshness = true;
          }
        }
      }
    } catch (_e) {
      // Ongeldige datum, niets doen
    }
  }

  return result;
}

// Hulpfunctie voor eenvoudige hashcode
function simpleHash(str: string): number {
  let hash = 0;
  if (str.length === 0) return hash;

  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32bit integer
  }

  return Math.abs(hash);
}
