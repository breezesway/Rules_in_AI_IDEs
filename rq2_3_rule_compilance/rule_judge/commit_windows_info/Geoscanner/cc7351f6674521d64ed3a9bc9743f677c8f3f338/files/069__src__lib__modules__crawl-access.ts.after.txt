import { RobotsTxtRules, SitemapData, HtmlSnapshot } from '../scanner';

export interface CrawlAccessResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    robotsTxt: {
      exists: boolean;
      allowsBots: boolean;
      hasCrawlDelay: boolean;
    };
    sitemap: {
      exists: boolean;
      isValid: boolean;
      urlCount: number;
    };
    metaRobots: {
      exists: boolean;
      allowsIndexing: boolean;
      allowsFollowing: boolean;
    };
    httpStatus: {
      isOk: boolean;
      code: number;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeCrawlAccess(
  robotsRules: RobotsTxtRules | null,
  sitemapData: SitemapData | null,
  htmlSnapshot: HtmlSnapshot | null,
  httpStatus: number
): CrawlAccessResult {
  const result: CrawlAccessResult = {
    score: 0,
    maxScore: 100,
    status: 'success',
    details: {
      robotsTxt: {
        exists: false,
        allowsBots: false,
        hasCrawlDelay: false,
      },
      sitemap: {
        exists: false,
        isValid: false,
        urlCount: 0,
      },
      metaRobots: {
        exists: false,
        allowsIndexing: true,
        allowsFollowing: true,
      },
      httpStatus: {
        isOk: false,
        code: httpStatus,
      },
    },
    fixes: [],
  };

  // Check robots.txt
  if (robotsRules) {
    result.details.robotsTxt.exists = true;
    result.score += 20;

    // Check if bots are allowed
    const hasDisallowAll = robotsRules.rules.some(
      rule => rule.type === 'disallow' && rule.path === '/'
    );
    result.details.robotsTxt.allowsBots = !hasDisallowAll;
    if (result.details.robotsTxt.allowsBots) {
      result.score += 20;
    } else {
      result.fixes.push({
        impact: 'high',
        description:
          'Robots.txt blokkeert alle bots. Dit voorkomt dat zoekmachines de site kunnen indexeren.',
        fix: 'Verwijder of pas de "Disallow: /" regel aan in robots.txt om bots toe te staan.',
      });
    }

    // Check crawl delay
    result.details.robotsTxt.hasCrawlDelay = !!robotsRules.crawlDelay;
    if (result.details.robotsTxt.hasCrawlDelay) {
      result.score += 10;
    } else {
      result.fixes.push({
        impact: 'low',
        description:
          'Geen crawl-delay ingesteld in robots.txt. Dit kan leiden tot overmatige serverbelasting.',
        fix: 'Voeg een Crawl-delay directive toe aan robots.txt, bijvoorbeeld: "Crawl-delay: 10"',
      });
    }
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen robots.txt bestand gevonden. Dit kan leiden tot ongewenste indexering.',
      fix: 'Maak een robots.txt bestand aan in de root van je website.',
    });
  }

  // Check sitemap
  if (sitemapData) {
    result.details.sitemap.exists = true;
    result.score += 20;

    result.details.sitemap.isValid = sitemapData.urls.length > 0;
    result.details.sitemap.urlCount = sitemapData.urls.length;

    if (result.details.sitemap.isValid) {
      result.score += 20;
    } else {
      result.fixes.push({
        impact: 'medium',
        description: 'Sitemap.xml bevat geen geldige URLs.',
        fix: 'Voeg geldige URLs toe aan je sitemap.xml bestand.',
      });
    }
  } else {
    result.fixes.push({
      impact: 'medium',
      description:
        'Geen sitemap.xml bestand gevonden. Dit maakt het moeilijker voor zoekmachines om je site te indexeren.',
      fix: 'Maak een sitemap.xml bestand aan in de root van je website.',
    });
  }

  // Check meta robots
  if (htmlSnapshot?.metadata.robots) {
    result.details.metaRobots.exists = true;
    const robots = htmlSnapshot.metadata.robots.toLowerCase();

    result.details.metaRobots.allowsIndexing = !robots.includes('noindex');
    result.details.metaRobots.allowsFollowing = !robots.includes('nofollow');

    if (result.details.metaRobots.allowsIndexing) {
      result.score += 10;
    } else {
      result.fixes.push({
        impact: 'high',
        description: 'Meta robots tag blokkeert indexering van de pagina.',
        fix: 'Verwijder of pas de meta robots tag aan om indexering toe te staan.',
      });
    }

    if (result.details.metaRobots.allowsFollowing) {
      result.score += 10;
    } else {
      result.fixes.push({
        impact: 'medium',
        description: 'Meta robots tag blokkeert het volgen van links op de pagina.',
        fix: 'Verwijder of pas de meta robots tag aan om het volgen van links toe te staan.',
      });
    }
  }

  // Check HTTP status
  result.details.httpStatus.isOk = httpStatus >= 200 && httpStatus < 300;
  if (result.details.httpStatus.isOk) {
    result.score += 10;
  } else {
    result.fixes.push({
      impact: 'high',
      description: `HTTP status code ${httpStatus} geeft aan dat er een probleem is met de pagina.`,
      fix: 'Controleer de server configuratie en zorg ervoor dat de pagina correct wordt geserveerd.',
    });
  }

  // Determine overall status
  if (result.score >= 80) {
    result.status = 'success';
  } else if (result.score >= 50) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}
