import { HtmlSnapshot } from '../scanner';

export interface CrossWebResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    sameAsLinks: {
      present: boolean;
      count: number;
      platforms: string[];
    };
    externalMentions: {
      hasWikipedia: boolean;
      hasWikidata: boolean;
      otherPlatforms: string[];
    };
    backlinks: {
      count: number;
      authorityDomains: string[];
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeCrossWeb(htmlSnapshot: HtmlSnapshot | null, url: string): CrossWebResult {
  const result: CrossWebResult = {
    score: 0,
    maxScore: 10,
    status: 'danger',
    details: {
      sameAsLinks: {
        present: false,
        count: 0,
        platforms: [],
      },
      externalMentions: {
        hasWikipedia: false,
        hasWikidata: false,
        otherPlatforms: [],
      },
      backlinks: {
        count: 0,
        authorityDomains: [],
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
  const hostname = new URL(url).hostname;

  // 1. Zoek naar sameAs links in JSON-LD
  const sameAsAnalysis = analyzeSameAsLinks(html);
  result.details.sameAsLinks = sameAsAnalysis;

  if (sameAsAnalysis.present) {
    // 2 punten als er sameAs links aanwezig zijn
    result.score += Math.min(2, sameAsAnalysis.count);
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen sameAs links gevonden in structured data',
      fix: `<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Uw Bedrijfsnaam",
  "sameAs": [
    "https://www.facebook.com/uwbedrijf",
    "https://www.linkedin.com/company/uwbedrijf",
    "https://twitter.com/uwbedrijf",
    "https://www.instagram.com/uwbedrijf"
  ]
}
</script>`,
    });
  }

  // 2. Controleer op Wikipedia/Wikidata vermeldingen
  const externalMentionsAnalysis = analyzeExternalMentions(html, hostname);
  result.details.externalMentions = externalMentionsAnalysis;

  if (externalMentionsAnalysis.hasWikipedia) {
    result.score += 3;
  }

  if (externalMentionsAnalysis.hasWikidata) {
    result.score += 2;
  }

  if (externalMentionsAnalysis.otherPlatforms.length > 0) {
    // Max 1 punt voor andere vermeldingen
    result.score += Math.min(1, externalMentionsAnalysis.otherPlatforms.length);
  }

  if (!externalMentionsAnalysis.hasWikipedia && !externalMentionsAnalysis.hasWikidata) {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen Wikipedia of Wikidata vermeldingen gevonden',
      fix: 'Overweeg een Wikipedia-pagina voor uw organisatie aan te maken of een Wikidata-item toe te voegen met relevante informatie over uw bedrijf of merk',
    });
  }

  // 3. Simuleer backlinks analyse (in de echte implementatie zou dit een externe API aanroepen)
  const backlinksAnalysis = simulateBacklinksAnalysis(hostname);
  result.details.backlinks = backlinksAnalysis;

  if (backlinksAnalysis.count > 0) {
    // Max 2 punten voor backlinks
    result.score += Math.min(2, Math.floor(backlinksAnalysis.count / 5));
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Weinig backlinks naar uw website gevonden',
      fix: 'Werk aan uw linkbuilding strategie door waardevolle content te creëren, gastbloggen, of partnerschappen aan te gaan met relevante websites in uw branche',
    });
  }

  // Bepaal status op basis van score
  if (result.score >= 8) {
    result.status = 'success';
  } else if (result.score >= 4) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Hulpfuncties

function analyzeSameAsLinks(html: string): CrossWebResult['details']['sameAsLinks'] {
  const result = {
    present: false,
    count: 0,
    platforms: [] as string[],
  };

  // Zoek naar sameAs in JSON-LD
  const sameAsRegex = /"sameAs"\s*:\s*\[(.*?)\]/g;
  const match = html.match(sameAsRegex);

  if (match) {
    result.present = true;

    // Probeer de links te extraheren
    const linksRegex = /"(https?:\/\/[^"]+)"/g;
    let linksMatch;
    const seenPlatforms = new Set<string>();
    const linksArr = [];

    while ((linksMatch = linksRegex.exec(match[0])) !== null) {
      linksArr.push(linksMatch[1]);
      try {
        const url = new URL(linksMatch[1]);
        const domain = url.hostname.replace(/^www\./, '');
        const platform = domainToPlatform(domain);
        if (platform && !seenPlatforms.has(platform)) {
          seenPlatforms.add(platform);
          result.platforms.push(platform);
        }
      } catch (e) {
        // Ongeldige URL, negeren
      }
    }

    result.count = linksArr.length;
  }

  return result;
}

function analyzeExternalMentions(
  html: string,
  hostname: string
): CrossWebResult['details']['externalMentions'] {
  const result = {
    hasWikipedia: false,
    hasWikidata: false,
    otherPlatforms: [] as string[],
  };

  try {
    // Echte API call voor externe vermeldingen
    // Gebruik de externe verwijzingsdata API van de backend
    const response = fetch(
      `/api/references/external-mentions?hostname=${encodeURIComponent(hostname)}`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
      .then(async res => {
        if (!res.ok) return result;

        const data = await res.json();
        result.hasWikipedia = data.hasWikipedia || false;
        result.hasWikidata = data.hasWikidata || false;
        result.otherPlatforms = data.otherPlatforms || [];
      })
      .catch(err => {
        console.error('Fout bij ophalen externe vermeldingen:', err);
      });
  } catch (error) {
    console.error('Fout bij analyseExternalMentions:', error);
  }

  return result;
}

function simulateBacklinksAnalysis(hostname: string): CrossWebResult['details']['backlinks'] {
  const result = {
    count: 0,
    authorityDomains: [] as string[],
  };

  try {
    // Echte API call om backlinks te analyseren
    // Gebruik een backlinkservice zoals Moz/Ahrefs/SEMrush via een backend API
    const response = fetch(`/api/references/backlinks?hostname=${encodeURIComponent(hostname)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(async res => {
        if (!res.ok) return result;

        const data = await res.json();
        result.count = data.count || 0;
        result.authorityDomains = data.authorityDomains || [];
      })
      .catch(err => {
        console.error('Fout bij ophalen backlinks:', err);
      });
  } catch (error) {
    console.error('Fout bij analyseBacklinks:', error);
  }

  return result;
}

function domainToPlatform(domain: string): string | null {
  const platformMap: Record<string, string> = {
    'facebook.com': 'Facebook',
    'linkedin.com': 'LinkedIn',
    'twitter.com': 'Twitter',
    'instagram.com': 'Instagram',
    'youtube.com': 'YouTube',
    'github.com': 'GitHub',
    'medium.com': 'Medium',
    'pinterest.com': 'Pinterest',
    'tiktok.com': 'TikTok',
  };

  for (const [key, value] of Object.entries(platformMap)) {
    if (domain.includes(key)) {
      return value;
    }
  }

  return null;
}
