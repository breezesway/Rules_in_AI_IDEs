import { HtmlSnapshot } from '../scanner';

export interface SchemaAdvancedResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    completeness: {
      missingRecommendedProperties: Record<string, string[]>;
      averageCompleteness: number;
      schemaTypesFound: string[];
      missingContextualSchemas: string[];
    };
    technical: {
      hasErrors: boolean;
      syntaxErrors: string[];
      invalidProperties: string[];
      deprecatedProperties: string[];
    };
    semanticCoherence: {
      coherenceScore: number;
      inappropriateSchemas: string[];
      contradictions: string[];
      contextualRelevance: Record<string, number>;
    };
    hierarchy: {
      hasProperHierarchy: boolean;
      nestedSchemas: string[];
      missingParentTypes: Record<string, string>;
      nestedLevels: number;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeSchemaAdvanced(htmlSnapshot: HtmlSnapshot | null): SchemaAdvancedResult {
  const result: SchemaAdvancedResult = {
    score: 0,
    maxScore: 15,
    status: 'danger',
    details: {
      completeness: {
        missingRecommendedProperties: {},
        averageCompleteness: 0,
        schemaTypesFound: [],
        missingContextualSchemas: [],
      },
      technical: {
        hasErrors: false,
        syntaxErrors: [],
        invalidProperties: [],
        deprecatedProperties: [],
      },
      semanticCoherence: {
        coherenceScore: 0,
        inappropriateSchemas: [],
        contradictions: [],
        contextualRelevance: {},
      },
      hierarchy: {
        hasProperHierarchy: false,
        nestedSchemas: [],
        missingParentTypes: {},
        nestedLevels: 0,
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

  // Extraheer alle schema.org JSON-LD data
  const schemaObjects = extractSchemaObjects(html);

  if (schemaObjects.length === 0) {
    result.fixes.push({
      impact: 'high',
      description: 'Geen Schema.org markup gevonden',
      fix: 'Voeg Schema.org structured data toe via JSON-LD om uw content beter vindbaar te maken voor AI en zoekmachines',
    });
    return result;
  }

  // 1. Volledigheidscontrole Schema Types
  const completenessAnalysis = analyzeCompleteness(schemaObjects);
  result.details.completeness = completenessAnalysis;

  // Score voor volledigheid (max 5 punten)
  result.score += Math.round(completenessAnalysis.averageCompleteness * 5);

  if (completenessAnalysis.averageCompleteness < 0.7) {
    const missingProps = Object.entries(completenessAnalysis.missingRecommendedProperties)
      .map(([type, props]) => `${type}: ${props.join(', ')}`)
      .join('\n');

    result.fixes.push({
      impact: 'medium',
      description: 'Schema types missen aanbevolen eigenschappen',
      fix: `Voeg de volgende aanbevolen eigenschappen toe aan uw schema markup:\n${missingProps}`,
    });
  }

  if (completenessAnalysis.missingContextualSchemas.length > 0) {
    result.fixes.push({
      impact: 'medium',
      description: 'Ontbrekende contextuele schema types',
      fix: `Voeg de volgende schema types toe om uw structured data completer te maken: ${completenessAnalysis.missingContextualSchemas.join(
        ', '
      )}`,
    });
  }

  // 2. Technische validatie
  const technicalAnalysis = analyzeTechnical(schemaObjects);
  result.details.technical = technicalAnalysis;

  // Score voor technische validiteit (max 4 punten)
  // 4 punten als er geen fouten zijn, anders punten aftrekken
  let technicalScore = 4;
  if (technicalAnalysis.hasErrors) {
    technicalScore -= Math.min(
      4,
      technicalAnalysis.syntaxErrors.length +
        technicalAnalysis.invalidProperties.length +
        technicalAnalysis.deprecatedProperties.length
    );
  }
  result.score += Math.max(0, technicalScore);

  if (technicalAnalysis.hasErrors) {
    if (technicalAnalysis.syntaxErrors.length > 0) {
      result.fixes.push({
        impact: 'high',
        description: 'JSON-LD syntax fouten gevonden',
        fix: `Corrigeer de volgende syntax fouten:\n${technicalAnalysis.syntaxErrors.join('\n')}`,
      });
    }

    if (technicalAnalysis.invalidProperties.length > 0) {
      result.fixes.push({
        impact: 'medium',
        description: 'Ongeldige eigenschappen gevonden',
        fix: `De volgende eigenschappen zijn ongeldig voor de gebruikte schema types:\n${technicalAnalysis.invalidProperties.join(
          '\n'
        )}`,
      });
    }

    if (technicalAnalysis.deprecatedProperties.length > 0) {
      result.fixes.push({
        impact: 'low',
        description: 'Verouderde eigenschappen gebruikt',
        fix: `De volgende eigenschappen zijn verouderd en moeten worden vervangen:\n${technicalAnalysis.deprecatedProperties.join(
          '\n'
        )}`,
      });
    }
  }

  // 3. Semantische coherentie
  const semanticAnalysis = analyzeSemanticCoherence(schemaObjects, html);
  result.details.semanticCoherence = semanticAnalysis;

  // Score voor semantische coherentie (max 3 punten)
  result.score += Math.round(semanticAnalysis.coherenceScore * 3);

  if (semanticAnalysis.coherenceScore < 0.7) {
    if (semanticAnalysis.inappropriateSchemas.length > 0) {
      result.fixes.push({
        impact: 'medium',
        description: 'Ongepaste schema types gebruikt',
        fix: `De volgende schema types passen niet bij de inhoud van de pagina:\n${semanticAnalysis.inappropriateSchemas.join(
          '\n'
        )}`,
      });
    }

    if (semanticAnalysis.contradictions.length > 0) {
      result.fixes.push({
        impact: 'medium',
        description: 'Tegenstrijdige schema data gevonden',
        fix: `De volgende tegenstrijdigheden moeten worden opgelost:\n${semanticAnalysis.contradictions.join(
          '\n'
        )}`,
      });
    }
  }

  // 4. Schema hiërarchie
  const hierarchyAnalysis = analyzeHierarchy(schemaObjects);
  result.details.hierarchy = hierarchyAnalysis;

  // Score voor hiërarchie (max 3 punten)
  let hierarchyScore = 0;
  if (hierarchyAnalysis.hasProperHierarchy) hierarchyScore += 1;
  if (hierarchyAnalysis.nestedLevels >= 2) hierarchyScore += 1;
  if (Object.keys(hierarchyAnalysis.missingParentTypes).length === 0) hierarchyScore += 1;

  result.score += hierarchyScore;

  if (!hierarchyAnalysis.hasProperHierarchy) {
    result.fixes.push({
      impact: 'medium',
      description: 'Suboptimale schema hiërarchie',
      fix: 'Organiseer uw schema types in een betekenisvolle hiërarchie om hun betekenis te versterken',
    });
  }

  if (Object.keys(hierarchyAnalysis.missingParentTypes).length > 0) {
    const missingParents = Object.entries(hierarchyAnalysis.missingParentTypes)
      .map(([child, parent]) => `${child} zou moeten worden genest binnen ${parent}`)
      .join('\n');

    result.fixes.push({
      impact: 'medium',
      description: 'Ontbrekende ouder-schema types',
      fix: `Voeg de volgende ouderschema's toe voor een betere hiërarchie:\n${missingParents}`,
    });
  }

  // Bepaal algemene status op basis van score
  if (result.score >= 12) {
    result.status = 'success';
  } else if (result.score >= 7) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Helper functies

function extractSchemaObjects(html: string): any[] {
  const schemaObjects: any[] = [];

  // Extract JSON-LD script tags
  const jsonLdRegex = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let match;

  while ((match = jsonLdRegex.exec(html)) !== null) {
    try {
      const jsonData = JSON.parse(match[1]);
      // Handle both single objects and arrays of objects
      if (Array.isArray(jsonData)) {
        schemaObjects.push(...jsonData);
      } else {
        schemaObjects.push(jsonData);
      }
    } catch (_e) {
      // JSON parsing error, add as a syntax error later
    }
  }

  return schemaObjects;
}

function analyzeCompleteness(
  schemaObjects: any[]
): SchemaAdvancedResult['details']['completeness'] {
  const result = {
    missingRecommendedProperties: {} as Record<string, string[]>,
    averageCompleteness: 0,
    schemaTypesFound: [] as string[],
    missingContextualSchemas: [] as string[],
  };

  // Schema typen en hun aanbevolen eigenschappen
  // Dit zijn aanbevolen eigenschappen bovenop verplichte eigenschappen
  const recommendedProperties: Record<string, string[]> = {
    Product: ['brand', 'review', 'aggregateRating', 'offers', 'sku', 'gtin', 'mpn', 'productID'],
    LocalBusiness: [
      'address',
      'telephone',
      'openingHours',
      'priceRange',
      'paymentAccepted',
      'image',
    ],
    Article: [
      'author',
      'datePublished',
      'dateModified',
      'publisher',
      'image',
      'description',
      'articleBody',
    ],
    Person: ['jobTitle', 'worksFor', 'alumniOf', 'address', 'email', 'telephone', 'url', 'image'],
    Organization: ['logo', 'contactPoint', 'address', 'sameAs', 'url', 'founder', 'foundingDate'],
    Event: ['startDate', 'endDate', 'location', 'performer', 'organizer', 'offers', 'eventStatus'],
    Recipe: [
      'recipeIngredient',
      'recipeInstructions',
      'prepTime',
      'cookTime',
      'totalTime',
      'nutrition',
    ],
    FAQPage: ['mainEntity'],
    WebPage: ['breadcrumb', 'lastReviewed', 'mainContentOfPage', 'primaryImageOfPage', 'speakable'],
    BreadcrumbList: ['itemListElement'],
    Review: ['author', 'itemReviewed', 'reviewRating', 'datePublished'],
    VideoObject: ['thumbnailUrl', 'contentUrl', 'duration', 'uploadDate', 'embedUrl'],
  };

  // Schema typen die vaak samen voorkomen
  const contextualRelationships: Record<string, string[]> = {
    Product: ['Offer', 'Review', 'AggregateRating', 'Brand'],
    Recipe: ['NutritionInformation', 'Review', 'HowTo'],
    Article: ['Person', 'Organization', 'ImageObject'],
    LocalBusiness: ['PostalAddress', 'OpeningHoursSpecification', 'GeoCoordinates'],
    Event: ['Place', 'Offer', 'Organization', 'Person'],
    VideoObject: ['Person', 'Organization', 'InteractionCounter'],
    FAQPage: ['Question', 'Answer'],
  };

  // Verzamel alle typen
  schemaObjects.forEach(obj => {
    const type = getSchemaType(obj);
    if (type && !result.schemaTypesFound.includes(type)) {
      result.schemaTypesFound.push(type);
    }
  });

  // Controleer ontbrekende eigenschappen
  let totalCompleteness = 0;
  let typesWithRecommendations = 0;

  result.schemaTypesFound.forEach(type => {
    if (recommendedProperties[type]) {
      typesWithRecommendations++;

      // Zoek het object met dit type
      const obj = schemaObjects.find(o => getSchemaType(o) === type);
      if (!obj) return;

      const missing = recommendedProperties[type].filter(prop => !obj[prop]);

      if (missing.length > 0) {
        result.missingRecommendedProperties[type] = missing;
      }

      const completeness = 1 - missing.length / recommendedProperties[type].length;
      totalCompleteness += completeness;
    }
  });

  // Bereken gemiddelde volledigheid
  if (typesWithRecommendations > 0) {
    result.averageCompleteness = totalCompleteness / typesWithRecommendations;
  }

  // Controleer ontbrekende contextuele schema's
  result.schemaTypesFound.forEach(type => {
    if (contextualRelationships[type]) {
      const missingContextual = contextualRelationships[type].filter(
        relatedType => !result.schemaTypesFound.includes(relatedType)
      );

      if (missingContextual.length > 0) {
        result.missingContextualSchemas.push(...missingContextual);
      }
    }
  });

  // Verwijder duplicaten
  result.missingContextualSchemas = Array.from(new Set(result.missingContextualSchemas));

  return result;
}

function analyzeTechnical(schemaObjects: any[]): SchemaAdvancedResult['details']['technical'] {
  const result = {
    hasErrors: false,
    syntaxErrors: [] as string[],
    invalidProperties: [] as string[],
    deprecatedProperties: [] as string[],
  };

  // Lijst van verouderde eigenschappen per type
  const deprecatedProperties: Record<string, string[]> = {
    Product: ['availability', 'itemCondition'], // Nu: offers.availability, offers.itemCondition
    Person: ['faxNumber', 'title'], // Nu: honorificPrefix/honorificSuffix
    Organization: ['faxNumber', 'duns'], // Nu: identfier
    Event: ['doorTime'], // Nu: doorTime is een property van eventSchedule
    WebPage: ['reviewedBy'], // Nu: review.author
    Recipe: ['nutrition'], // Nu: nutrition als object
    LocalBusiness: ['paymentAccepted', 'priceRange'], // Beperkte ondersteuning
    Article: ['dateCreated'], // Nu: datePublished
  };

  // Functie om te controleren of een eigenschap geldig is voor een schema type
  const isValidProperty = (type: string, property: string): boolean => {
    // Vereenvoudigde implementatie - in werkelijkheid zou dit schema.org API calls vereisen
    // of een statische validatie tegen een lijst van geldige eigenschappen per type
    const validPropertiesMap: Record<string, string[]> = {
      Product: [
        'name',
        'description',
        'image',
        'brand',
        'offers',
        'review',
        'aggregateRating',
        'sku',
        'gtin',
      ],
      Person: [
        'name',
        'givenName',
        'familyName',
        'jobTitle',
        'address',
        'email',
        'telephone',
        'url',
      ],
      Organization: ['name', 'legalName', 'logo', 'address', 'contactPoint', 'sameAs', 'url'],
      Article: ['headline', 'author', 'publisher', 'datePublished', 'dateModified', 'articleBody'],
      WebPage: ['name', 'description', 'url', 'isPartOf', 'breadcrumb', 'lastReviewed'],
      Event: ['name', 'startDate', 'endDate', 'location', 'offers', 'performer', 'organizer'],
      LocalBusiness: ['name', 'address', 'telephone', 'openingHours', 'geo', 'priceRange'],
      Recipe: [
        'name',
        'recipeIngredient',
        'recipeInstructions',
        'prepTime',
        'cookTime',
        'totalTime',
      ],
      Review: ['reviewBody', 'author', 'itemReviewed', 'reviewRating', 'datePublished'],
      FAQPage: ['mainEntity'],
      Question: ['name', 'acceptedAnswer'],
      Answer: ['text'],
    };

    // Basis eigenschappen die voor alle types gelden
    const commonProperties = [
      '@type',
      '@context',
      '@id',
      'url',
      'name',
      'description',
      'image',
      'sameAs',
    ];

    return (
      commonProperties.includes(property) ||
      (validPropertiesMap[type] && validPropertiesMap[type].includes(property))
    );
  };

  // Controleer elk schema object
  schemaObjects.forEach(obj => {
    const type = getSchemaType(obj);
    if (!type) return;

    // Controleer verouderde eigenschappen
    if (deprecatedProperties[type]) {
      deprecatedProperties[type].forEach(prop => {
        if (obj[prop] !== undefined) {
          result.hasErrors = true;
          result.deprecatedProperties.push(`${type}.${prop} is verouderd`);
        }
      });
    }

    // Controleer ongeldige eigenschappen
    Object.keys(obj).forEach(prop => {
      // Sla @context, @type en andere speciale eigenschappen over
      if (prop.startsWith('@')) return;

      if (!isValidProperty(type, prop)) {
        result.hasErrors = true;
        result.invalidProperties.push(`${prop} is geen geldige eigenschap voor ${type}`);
      }
    });
  });

  return result;
}

function analyzeSemanticCoherence(
  schemaObjects: any[],
  html: string
): SchemaAdvancedResult['details']['semanticCoherence'] {
  const result = {
    coherenceScore: 0,
    inappropriateSchemas: [] as string[],
    contradictions: [] as string[],
    contextualRelevance: {} as Record<string, number>,
  };

  const pageText = extractMainText(html);

  // Scores voor contextuele relevantie
  schemaObjects.forEach(obj => {
    const type = getSchemaType(obj);
    if (!type) return;

    // Controleer of het schema type relevant is voor de pagina-inhoud
    result.contextualRelevance[type] = calculateContextualRelevance(type, obj, pageText);

    // Zoek ongepaste schema types (lage relevantie)
    if (result.contextualRelevance[type] < 0.3) {
      result.inappropriateSchemas.push(type);
    }
  });

  // Controleer op tegenstrijdigheden tussen schema's
  checkForContradictions(schemaObjects, result);

  // Bereken algemene coherentie score
  const relevanceValues = Object.values(result.contextualRelevance);
  if (relevanceValues.length > 0) {
    const averageRelevance =
      relevanceValues.reduce((sum, value) => sum + value, 0) / relevanceValues.length;

    // Coherentie score is gebaseerd op gemiddelde relevantie en afwezigheid van tegenstrijdigheden
    result.coherenceScore = averageRelevance * (1 - result.contradictions.length * 0.1);
    result.coherenceScore = Math.max(0, Math.min(1, result.coherenceScore)); // Begrens tussen 0 en 1
  }

  return result;
}

function analyzeHierarchy(schemaObjects: any[]): SchemaAdvancedResult['details']['hierarchy'] {
  const result = {
    hasProperHierarchy: false,
    nestedSchemas: [] as string[],
    missingParentTypes: {} as Record<string, string>,
    nestedLevels: 0,
  };

  // Ideale hiërarchische relaties tussen types
  const idealHierarchies: Record<string, string> = {
    Offer: 'Product',
    Review: 'Product',
    AggregateRating: 'Product',
    ImageObject: 'Article',
    Answer: 'Question',
    Question: 'FAQPage',
    ListItem: 'BreadcrumbList',
    OpeningHoursSpecification: 'LocalBusiness',
    PostalAddress: 'LocalBusiness',
    GeoCoordinates: 'Place',
    NutritionInformation: 'Recipe',
  };

  // Zoek geneste schema types
  result.nestedSchemas = findNestedSchemaTypes(schemaObjects);

  // Controleer diepte van nesting
  result.nestedLevels = calculateNestingDepth(schemaObjects);

  // Controleer of er een goede hiërarchie is
  result.hasProperHierarchy = result.nestedSchemas.length > 0 && result.nestedLevels >= 2;

  // Controleer op ontbrekende ouder-types
  const foundTypes = schemaObjects.map(obj => getSchemaType(obj)).filter(Boolean) as string[];

  // Voor elk gevonden type, controleer of zijn ideale ouder ook aanwezig is
  foundTypes.forEach(type => {
    if (idealHierarchies[type] && !foundTypes.includes(idealHierarchies[type])) {
      result.missingParentTypes[type] = idealHierarchies[type];
    }
  });

  return result;
}

function getSchemaType(obj: any): string | null {
  if (!obj || typeof obj !== 'object') return null;

  // Haal type uit @type of doorzoek de object boom
  if (obj['@type']) {
    return obj['@type'];
  }

  // In het geval van geneste arrays in JSON-LD
  if (Array.isArray(obj) && obj.length > 0 && obj[0]['@type']) {
    return obj[0]['@type'];
  }

  return null;
}

function extractMainText(html: string): string {
  // Verwijder script, style en andere niet-inhoudelijke tags
  const text = html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, ' ')
    .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ') // Verwijder alle HTML tags
    .replace(/\s+/g, ' ') // Zet meerdere spaties om naar één
    .trim();

  return text;
}

function calculateContextualRelevance(type: string, obj: any, pageText: string): number {
  // Deze functie zou in een echte implementatie NLP gebruiken om de relevantie
  // van schema types voor de pagina-inhoud te bepalen.
  // Voor deze demo gebruiken we een vereenvoudigde aanpak gebaseerd op eigenschappen en keywords.

  const typeRelevancePatterns: Record<string, RegExp[]> = {
    Product: [/koop/i, /prijs/i, /product/i, /artikel/i, /bestellen/i, /winkelwagen/i],
    LocalBusiness: [/winkel/i, /openingstijden/i, /adres/i, /bezoek/i, /locatie/i, /route/i],
    Article: [/artikel/i, /nieuws/i, /blog/i, /publicatie/i, /auteur/i],
    Recipe: [/recept/i, /bereiden/i, /ingrediënten/i, /kooktijd/i, /voedingswaarde/i],
    Event: [/evenement/i, /bijeenkomst/i, /concert/i, /festival/i, /datum/i, /locatie/i],
    FAQPage: [/faq/i, /veelgestelde vragen/i, /vraag en antwoord/i, /help/i],
    Person: [/persoon/i, /profiel/i, /over mij/i, /biografie/i, /cv/i, /team/i],
    Organization: [/bedrijf/i, /organisatie/i, /over ons/i, /contact/i, /team/i],
  };

  // Als er geen patterns zijn voor dit type, gebruik een gemiddelde score
  if (!typeRelevancePatterns[type]) {
    return 0.5;
  }

  // Tel hoeveel patronen voorkomen in de paginatekst
  const patterns = typeRelevancePatterns[type];
  const matchCount = patterns.filter(pattern => pattern.test(pageText)).length;

  // Bereken score op basis van match percentage
  return matchCount / patterns.length;
}

function checkForContradictions(
  schemaObjects: any[],
  result: SchemaAdvancedResult['details']['semanticCoherence']
) {
  // Controleer op objecten van hetzelfde type maar met tegenstrijdige informatie
  const typeMap: Record<string, any[]> = {};

  schemaObjects.forEach(obj => {
    const type = getSchemaType(obj);
    if (!type) return;

    if (!typeMap[type]) {
      typeMap[type] = [obj];
    } else {
      typeMap[type].push(obj);
    }
  });

  // Controleer op tegenstrijdigheden tussen objecten van hetzelfde type
  Object.entries(typeMap).forEach(([type, objects]) => {
    if (objects.length <= 1) return;

    // Controleer op inconsistenties tussen belangrijke eigenschappen
    const keyProperties = getKeyPropertiesForType(type);

    for (let i = 0; i < objects.length - 1; i++) {
      for (let j = i + 1; j < objects.length; j++) {
        const obj1 = objects[i];
        const obj2 = objects[j];

        keyProperties.forEach(prop => {
          if (obj1[prop] && obj2[prop] && obj1[prop] !== obj2[prop]) {
            result.contradictions.push(
              `Tegenstrijdige ${prop} waarden voor ${type}: "${obj1[prop]}" vs "${obj2[prop]}"`
            );
          }
        });
      }
    }
  });
}

function getKeyPropertiesForType(type: string): string[] {
  // Belangrijke eigenschappen die consistent moeten zijn voor objecten van hetzelfde type
  const keyPropertiesMap: Record<string, string[]> = {
    Product: ['name', 'brand', 'sku', 'productID'],
    Person: ['name', 'email', 'telephone'],
    Organization: ['name', 'legalName', 'url'],
    Article: ['headline', 'datePublished'],
    Event: ['name', 'startDate', 'location'],
    LocalBusiness: ['name', 'telephone', 'address'],
    Recipe: ['name', 'recipeYield', 'totalTime'],
  };

  return keyPropertiesMap[type] || ['name'];
}

function findNestedSchemaTypes(schemaObjects: any[]): string[] {
  const nestedSchemas: string[] = [];

  const findNested = (obj: any) => {
    if (!obj || typeof obj !== 'object') return;

    Object.entries(obj).forEach(([key, value]) => {
      // Sla @context, @type en andere speciale eigenschappen over
      if (key.startsWith('@')) return;

      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(item => {
            const nestedType = getSchemaType(item);
            if (nestedType && !nestedSchemas.includes(nestedType)) {
              nestedSchemas.push(nestedType);
            }
            findNested(item);
          });
        } else {
          const nestedType = getSchemaType(value);
          if (nestedType && !nestedSchemas.includes(nestedType)) {
            nestedSchemas.push(nestedType);
          }
          findNested(value);
        }
      }
    });
  };

  schemaObjects.forEach(findNested);

  return nestedSchemas;
}

function calculateNestingDepth(schemaObjects: any[]): number {
  let maxDepth = 0;

  const findMaxDepth = (obj: any, currentDepth: number) => {
    if (!obj || typeof obj !== 'object') return;

    // Als het object een schema type heeft, verhoog de diepte
    if (obj['@type']) {
      currentDepth++;
      maxDepth = Math.max(maxDepth, currentDepth);
    }

    // Doorzoek alle geneste objecten
    Object.entries(obj).forEach(([key, value]) => {
      // Sla @context, @type en andere speciale eigenschappen over
      if (key.startsWith('@')) return;

      if (typeof value === 'object' && value !== null) {
        if (Array.isArray(value)) {
          value.forEach(item => findMaxDepth(item, currentDepth));
        } else {
          findMaxDepth(value, currentDepth);
        }
      }
    });
  };

  schemaObjects.forEach(obj => findMaxDepth(obj, 0));

  return maxDepth;
}
