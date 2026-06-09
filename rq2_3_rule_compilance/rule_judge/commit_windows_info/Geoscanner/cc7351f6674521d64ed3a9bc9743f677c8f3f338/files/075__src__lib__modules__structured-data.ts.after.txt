import { HtmlSnapshot } from '../scanner';

export interface StructuredDataResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    jsonLd: {
      exists: boolean;
      isValid: boolean;
      schemaTypes: string[];
      requiredFields: {
        [key: string]: boolean;
      };
    };
    openGraph: {
      exists: boolean;
      hasTitle: boolean;
      hasDescription: boolean;
      hasImage: boolean;
      hasType: boolean;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeStructuredData(htmlSnapshot: HtmlSnapshot | null): StructuredDataResult {
  const result: StructuredDataResult = {
    score: 0,
    maxScore: 25,
    status: 'success',
    details: {
      jsonLd: {
        exists: false,
        isValid: false,
        schemaTypes: [],
        requiredFields: {},
      },
      openGraph: {
        exists: false,
        hasTitle: false,
        hasDescription: false,
        hasImage: false,
        hasType: false,
      },
    },
    fixes: [],
  };

  if (!htmlSnapshot) {
    result.status = 'danger';
    return result;
  }

  // JSON-LD Analyse
  const jsonLdScripts = extractJsonLdScripts(htmlSnapshot.content);
  if (jsonLdScripts.length > 0) {
    result.details.jsonLd.exists = true;
    result.score += 10;

    for (const script of jsonLdScripts) {
      try {
        const jsonData = JSON.parse(script);
        if (jsonData['@type']) {
          result.details.jsonLd.schemaTypes.push(jsonData['@type']);
          result.details.jsonLd.isValid = true;
          result.score += 5;

          // Check required fields based on schema type
          const requiredFields = getRequiredFieldsForType(jsonData['@type']);
          for (const field of requiredFields) {
            result.details.jsonLd.requiredFields[field] = !!jsonData[field];
            if (jsonData[field]) {
              result.score += 2;
            }
          }
        }
      } catch (error) {
        result.fixes.push({
          impact: 'high',
          description: 'Ongeldige JSON-LD syntax gevonden.',
          fix: 'Zorg ervoor dat de JSON-LD syntax correct is en valideer deze met de Schema.org validator.',
        });
      }
    }
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen JSON-LD markup gevonden.',
      fix: 'Voeg JSON-LD markup toe aan je pagina voor betere structuur en AI-begrip.',
    });
  }

  // Open Graph Analyse
  const ogTags = extractOpenGraphTags(htmlSnapshot.content);
  if (ogTags.length > 0) {
    result.details.openGraph.exists = true;
    result.score += 5;

    result.details.openGraph.hasTitle = ogTags.some(tag => tag.property === 'og:title');
    result.details.openGraph.hasDescription = ogTags.some(tag => tag.property === 'og:description');
    result.details.openGraph.hasImage = ogTags.some(tag => tag.property === 'og:image');
    result.details.openGraph.hasType = ogTags.some(tag => tag.property === 'og:type');

    if (result.details.openGraph.hasTitle) result.score += 2;
    if (result.details.openGraph.hasDescription) result.score += 2;
    if (result.details.openGraph.hasImage) result.score += 2;
    if (result.details.openGraph.hasType) result.score += 2;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Geen Open Graph tags gevonden.',
      fix: 'Voeg Open Graph tags toe voor betere social media integratie.',
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

function extractJsonLdScripts(html: string): string[] {
  const scripts: string[] = [];
  const regex = /<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi;
  let match;

  while ((match = regex.exec(html)) !== null) {
    scripts.push(match[1].trim());
  }

  return scripts;
}

function extractOpenGraphTags(html: string): Array<{ property: string; content: string }> {
  const tags: Array<{ property: string; content: string }> = [];
  const regex = /<meta[^>]*property="og:([^"]*)"[^>]*content="([^"]*)"[^>]*>/gi;
  let match;

  while ((match = regex.exec(html)) !== null) {
    tags.push({
      property: `og:${match[1]}`,
      content: match[2],
    });
  }

  return tags;
}

function getRequiredFieldsForType(type: string): string[] {
  const requiredFields: { [key: string]: string[] } = {
    Article: ['headline', 'author', 'datePublished'],
    Product: ['name', 'description', 'offers'],
    Organization: ['name', 'url'],
    Person: ['name'],
    WebPage: ['name', 'description'],
    BlogPosting: ['headline', 'author', 'datePublished'],
    LocalBusiness: ['name', 'address'],
    Recipe: ['name', 'ingredients', 'instructions'],
  };

  return requiredFields[type] || [];
}
