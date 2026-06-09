import { HtmlSnapshot } from '../scanner';

export interface AuthorityResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    authorBio: {
      present: boolean;
      hasExpertiseIndicators: boolean;
      authorName: string | null;
    };
    outboundLinks: {
      totalCount: number;
      authorityDomainsCount: number;
      domains: string[];
    };
    licenseInfo: {
      present: boolean;
      type: string | null;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeAuthority(htmlSnapshot: HtmlSnapshot | null): AuthorityResult {
  const result: AuthorityResult = {
    score: 0,
    maxScore: 15,
    status: 'danger',
    details: {
      authorBio: {
        present: false,
        hasExpertiseIndicators: false,
        authorName: null,
      },
      outboundLinks: {
        totalCount: 0,
        authorityDomainsCount: 0,
        domains: [],
      },
      licenseInfo: {
        present: false,
        type: null,
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

  // 1. Auteur bio analyse
  const authorAnalysis = analyzeAuthorBio(html);
  result.details.authorBio = authorAnalysis;

  if (authorAnalysis.present) {
    result.score += 3;

    if (authorAnalysis.hasExpertiseIndicators) {
      result.score += 3;
    } else {
      result.fixes.push({
        impact: 'medium',
        description: 'Auteur bio bevat geen expertise-indicatoren',
        fix: 'Voeg professionele kwalificaties, ervaring, certificeringen of andere expertise-indicatoren toe aan de auteur bio',
      });
    }
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen auteur bio gevonden',
      fix: 'Voeg een auteur bio toe met naam, functie, en expertise. Gebruik schema.org Person markup voor betere AI-zichtbaarheid',
    });
  }

  // 2. Outbound links analyse
  const linksAnalysis = analyzeOutboundLinks(html);
  result.details.outboundLinks = linksAnalysis;

  if (linksAnalysis.totalCount > 0) {
    // Basis score voor het hebben van outbound links
    result.score += 1;

    // Extra punten voor links naar autoriteitsdomeinen
    if (linksAnalysis.authorityDomainsCount >= 5) {
      result.score += 4;
    } else if (linksAnalysis.authorityDomainsCount >= 2) {
      result.score += 2;
      result.fixes.push({
        impact: 'medium',
        description: 'Beperkt aantal links naar autoriteitsdomeinen',
        fix: 'Voeg meer links toe naar gerenommeerde bronnen zoals academische journals, Wikipedia, of industrie-autoriteiten',
      });
    } else {
      result.fixes.push({
        impact: 'high',
        description: 'Weinig tot geen links naar autoriteitsdomeinen',
        fix: 'Voeg links toe naar minstens 3-5 gerenommeerde bronnen om je content met betrouwbare bronnen te onderbouwen',
      });
    }
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen outbound links gevonden',
      fix: 'Voeg links toe naar externe, gezaghebbende bronnen om je content te onderbouwen',
    });
  }

  // 3. Licentie informatie analyse
  const licenseAnalysis = analyzeLicenseInfo(html);
  result.details.licenseInfo = licenseAnalysis;

  if (licenseAnalysis.present) {
    result.score += 3;
  } else {
    result.fixes.push({
      impact: 'low',
      description: 'Geen licentie informatie gevonden',
      fix: 'Voeg copyright of Creative Commons licentie-informatie toe aan de footer van je site',
    });
  }

  // Bepaal overall status
  if (result.score >= 12) {
    result.status = 'success';
  } else if (result.score >= 8) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Hulpfuncties

function analyzeAuthorBio(html: string): AuthorityResult['details']['authorBio'] {
  const result = {
    present: false,
    hasExpertiseIndicators: false,
    authorName: null as string | null,
  };

  // Zoek naar auteur informatie in HTML

  // 1. Schema.org Person markup
  const schemaPersonMatch = html.match(/"@type"\s*:\s*"Person".*?"name"\s*:\s*"([^"]*)"/s);
  const hasSchemaAuthor = !!schemaPersonMatch;

  // 2. Traditionele auteur bio secties
  const authorDivPattern = /<div[^>]*class="[^"]*author[^"]*"[^>]*>/i;
  const hasAuthorDiv = authorDivPattern.test(html);

  // 3. Autheurinformatie in meta tags
  const metaAuthorPattern = /<meta[^>]*name="author"[^>]*content="([^"]*)"[^>]*>/i;
  const metaAuthorMatch = html.match(metaAuthorPattern);

  // 4. Byline patronen
  const bylinePattern = /<p[^>]*class="[^"]*byline[^"]*"[^>]*>.*?<\/p>/i;
  const hasByline = bylinePattern.test(html);

  result.present = hasSchemaAuthor || hasAuthorDiv || !!metaAuthorMatch || hasByline;

  // Als we een auteur hebben gevonden, zoek naar de naam
  if (schemaPersonMatch) {
    result.authorName = schemaPersonMatch[1];
  } else if (metaAuthorMatch) {
    result.authorName = metaAuthorMatch[1];
  }

  // Zoek naar expertise-indicatoren
  const expertiseIndicators = [
    /(?:dr\.|professor|prof\.|phd|certified|expert|specialist|\d+ jaar ervaring|\d+ years? experience)/i,
    /diploma|degree|master|bachelor|doctorandus|ingenieur|drs\.|ir\.|mr\.|certified|gecertificeerd/i,
    /researcher|onderzoeker|journalist|author|auteur|professional|consultant|adviseur|specialist/i,
  ];

  const expertiseCheck = expertiseIndicators.some(pattern => pattern.test(html));
  result.hasExpertiseIndicators = expertiseCheck;

  return result;
}

function analyzeOutboundLinks(html: string): AuthorityResult['details']['outboundLinks'] {
  const result = {
    totalCount: 0,
    authorityDomainsCount: 0,
    domains: [] as string[],
  };

  // Extraheer alle outbound links
  const linkPattern = /<a[^>]*href="(https?:\/\/[^"]*)"[^>]*>/g;
  const matches = [...html.matchAll(linkPattern)];

  // Filter op unieke domeinen en niet-sociale media links
  const domains = new Set<string>();
  const authorityDomains = new Set<string>();

  for (const match of matches) {
    try {
      const url = new URL(match[1]);
      const domain = url.hostname;

      // Filter out sociale media en niet-inhoudelijke sites
      const socialMediaPatterns = [
        /facebook\.com/i,
        /twitter\.com/i,
        /linkedin\.com/i,
        /instagram\.com/i,
        /youtube\.com/i,
        /pinterest\.com/i,
        /tiktok\.com/i,
        /google\.com/i,
      ];

      const isSocialMedia = socialMediaPatterns.some(pattern => pattern.test(domain));

      if (!isSocialMedia) {
        domains.add(domain);

        // Check of het een autoriteitsdomein is
        const authorityPatterns = [
          /wikipedia\.org/i,
          /\.gov\b/i,
          /\.edu\b/i,
          /scholar\.google\.com/i,
          /ncbi\.nlm\.nih\.gov/i,
          /pubmed\.gov/i,
          /sciencedirect\.com/i,
          /nature\.com/i,
          /science\.org/i,
          /jstor\.org/i,
          /ieee\.org/i,
          /academia\.edu/i,
          /researchgate\.net/i,
          /nytimes\.com/i,
          /bbc\.co\.uk/i,
          /reuters\.com/i,
          /theguardian\.com/i,
          /who\.int/i,
          /rijksoverheid\.nl/i,
          /cbs\.nl/i,
        ];

        const isAuthority = authorityPatterns.some(pattern => pattern.test(domain));
        if (isAuthority) {
          authorityDomains.add(domain);
        }
      }
    } catch (_e) {
      // Ongeldige URL, negeren
    }
  }

  result.totalCount = domains.size;
  result.authorityDomainsCount = authorityDomains.size;
  result.domains = [...authorityDomains];

  return result;
}

function analyzeLicenseInfo(html: string): AuthorityResult['details']['licenseInfo'] {
  const result = {
    present: false,
    type: null as string | null,
  };

  // Zoek naar verschillende soorten licentie-informatie

  // 1. Copyright notice
  const copyrightPattern = /(?:©|&copy;|copyright)\s*(?:\d{4}|2\d{3})/i;
  const hasCopyright = copyrightPattern.test(html);

  // 2. Creative Commons licenties
  const ccPattern = /creative\s+commons|CC\s+BY(?:-(?:NC|SA|ND|NC-SA|NC-ND))?/i;
  const hasCC = ccPattern.test(html);

  // 3. Algemene voorwaarden en privacybeleid
  const termsPattern =
    /(?:terms\s+(?:of\s+(?:use|service))|gebruiksvoorwaarden|algemene\s+voorwaarden)/i;
  const hasTerms = termsPattern.test(html);

  result.present = hasCopyright || hasCC || hasTerms;

  // Bepaal het type licentie
  if (hasCC) {
    // Extract CC licentie type
    const ccMatch = html.match(/CC\s+BY(?:-(?:NC|SA|ND|NC-SA|NC-ND))?/i);
    result.type = ccMatch ? ccMatch[0] : 'Creative Commons';
  } else if (hasCopyright) {
    result.type = 'Copyright';
  } else if (hasTerms) {
    result.type = 'Terms of Use';
  }

  return result;
}
