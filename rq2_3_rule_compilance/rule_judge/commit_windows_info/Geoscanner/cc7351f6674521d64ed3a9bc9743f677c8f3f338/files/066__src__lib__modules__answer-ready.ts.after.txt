import { HtmlSnapshot } from '../scanner';

export interface AnswerReadyResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    faq: {
      hasFaqStructure: boolean;
      faqCount: number;
      isSchemaMarkup: boolean;
    };
    featuredSnippet: {
      hasPotential: boolean;
      hasSummary: boolean;
      hasDefinition: boolean;
      hasStepByStep: boolean;
    };
    voiceSearch: {
      hasNaturalLanguage: boolean;
      hasShortAnswers: boolean;
      hasConversationalTone: boolean;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeAnswerReady(htmlSnapshot: HtmlSnapshot | null): AnswerReadyResult {
  const result: AnswerReadyResult = {
    score: 0,
    maxScore: 20,
    status: 'danger',
    details: {
      faq: {
        hasFaqStructure: false,
        faqCount: 0,
        isSchemaMarkup: false,
      },
      featuredSnippet: {
        hasPotential: false,
        hasSummary: false,
        hasDefinition: false,
        hasStepByStep: false,
      },
      voiceSearch: {
        hasNaturalLanguage: false,
        hasShortAnswers: false,
        hasConversationalTone: false,
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

  // 1. FAQ structuur analyse
  const faqAnalysis = analyzeFaqStructure(html);
  result.details.faq = faqAnalysis;
  if (faqAnalysis.hasFaqStructure) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'high',
      description: 'Geen FAQ structuur gevonden op de pagina',
      fix: 'Voeg een FAQ sectie toe met vraag-antwoord paren. Gebruik bij voorkeur een <dl>, <dt>, <dd> structuur of FAQ Schema markup',
    });
  }

  if (faqAnalysis.isSchemaMarkup) {
    result.score += 2;
  } else if (faqAnalysis.hasFaqStructure) {
    result.fixes.push({
      impact: 'medium',
      description: 'FAQ zonder Schema.org markup',
      fix: 'Voeg FAQ Schema.org markup toe aan de FAQ sectie: https://schema.org/FAQPage',
    });
  }

  // 2. Featured snippet potentie
  const snippetAnalysis = analyzeSnippetPotential(html);
  result.details.featuredSnippet = snippetAnalysis;

  if (snippetAnalysis.hasSummary) result.score += 2;
  if (snippetAnalysis.hasDefinition) result.score += 2;
  if (snippetAnalysis.hasStepByStep) result.score += 2;

  if (!snippetAnalysis.hasPotential) {
    result.fixes.push({
      impact: 'medium',
      description: 'Pagina is niet geoptimaliseerd voor featured snippets',
      fix: 'Voeg een duidelijke samenvatting toe bovenaan de pagina, gebruik definitie-lijsten voor termen, en gebruik genummerde stappen voor instructies',
    });
  }

  // 3. Voice search optimalisatie
  const voiceAnalysis = analyzeVoiceSearchOptimization(html);
  result.details.voiceSearch = voiceAnalysis;

  if (voiceAnalysis.hasNaturalLanguage) result.score += 2;
  if (voiceAnalysis.hasShortAnswers) result.score += 3;
  if (voiceAnalysis.hasConversationalTone) result.score += 2;

  if (!voiceAnalysis.hasNaturalLanguage || !voiceAnalysis.hasShortAnswers) {
    result.fixes.push({
      impact: 'medium',
      description: 'Content is niet geoptimaliseerd voor voice search',
      fix: 'Gebruik natuurlijke vraagzinnen (wie, wat, waar, wanneer, waarom, hoe) en geef directe, korte antwoorden binnen 30 woorden',
    });
  }

  // Bepaal overall status
  if (result.score >= 16) {
    result.status = 'success';
  } else if (result.score >= 10) {
    result.status = 'warning';
  } else {
    result.status = 'danger';
  }

  return result;
}

// Hulpfuncties

function analyzeFaqStructure(html: string): AnswerReadyResult['details']['faq'] {
  const result = {
    hasFaqStructure: false,
    faqCount: 0,
    isSchemaMarkup: false,
  };

  // Check voor FAQ Schema.org markup
  const hasSchemaFaq = html.includes('FAQPage') && html.includes('acceptedAnswer');
  result.isSchemaMarkup = hasSchemaFaq;

  // Check voor <dl><dt><dd> structuur
  const dlDtDdPattern = /<dl[^>]*>.*?<dt[^>]*>.*?<\/dt>.*?<dd[^>]*>.*?<\/dd>.*?<\/dl>/is;
  const hasDlStructure = dlDtDdPattern.test(html);

  // Check voor alternatieve FAQ structuren (div met vraag/antwoord classes, h3/p paren, etc.)
  const faqDivPattern = /<div[^>]*class="[^"]*faq[^"]*"[^>]*>/i;
  const hasFaqDiv = faqDivPattern.test(html);

  // Check voor vraag-antwoord patroon (<h3> gevolgd door <p>)
  const h3pPattern = /<h3[^>]*>[^<]*\?[^<]*<\/h3>\s*<p[^>]*>/gi;
  const h3pMatches = html.match(h3pPattern);
  const hasH3PStructure = h3pMatches != null && h3pMatches.length > 0;

  result.hasFaqStructure = hasSchemaFaq || hasDlStructure || hasFaqDiv || hasH3PStructure;

  // Tel het aantal FAQ items
  if (hasSchemaFaq) {
    const faqItemPattern = /"acceptedAnswer"/g;
    const matches = html.match(faqItemPattern);
    result.faqCount = matches ? matches.length : 0;
  } else if (hasDlStructure) {
    const dtPattern = /<dt[^>]*>/g;
    const matches = html.match(dtPattern);
    result.faqCount = matches ? matches.length : 0;
  } else if (hasH3PStructure) {
    result.faqCount = h3pMatches ? h3pMatches.length : 0;
  } else if (hasFaqDiv) {
    // Schatting: meestal zouden er minstens 3 items in een FAQ moeten zijn
    result.faqCount = 3;
  }

  return result;
}

function analyzeSnippetPotential(html: string): AnswerReadyResult['details']['featuredSnippet'] {
  const result = {
    hasPotential: false,
    hasSummary: false,
    hasDefinition: false,
    hasStepByStep: false,
  };

  // Check voor een duidelijke samenvatting (eerste of tweede paragraaf)
  const firstParagraphs = html.match(/<p[^>]*>([^<]{50,300})<\/p>/i);
  result.hasSummary = !!firstParagraphs;

  // Check voor definitielijsten
  const definitionPattern = /<dl[^>]*>.*?<dt[^>]*>.*?<\/dt>.*?<dd[^>]*>.*?<\/dd>.*?<\/dl>/is;
  result.hasDefinition = definitionPattern.test(html);

  // Check voor stap-voor-stap instructies (ol/ul met li, of genummerde kopjes)
  const orderedListPattern = /<ol[^>]*>.*?<li[^>]*>.*?<\/li>.*?<\/ol>/is;
  const numberedHeadingPattern = /<h[2-4][^>]*>\s*(?:\d+[\.\):]|Stap \d+)/i;

  result.hasStepByStep = orderedListPattern.test(html) || numberedHeadingPattern.test(html);

  // Als minimaal 2 van de 3 elementen aanwezig zijn, heeft de pagina featured snippet potentie
  const count =
    (result.hasSummary ? 1 : 0) + (result.hasDefinition ? 1 : 0) + (result.hasStepByStep ? 1 : 0);

  result.hasPotential = count >= 2;

  return result;
}

function analyzeVoiceSearchOptimization(html: string): AnswerReadyResult['details']['voiceSearch'] {
  const result = {
    hasNaturalLanguage: false,
    hasShortAnswers: false,
    hasConversationalTone: false,
  };

  // Verwijder HTML tags voor tekstanalyse
  const text = html
    .replace(/<[^>]*>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();

  // Check voor vraagwoorden (wie, wat, waar, wanneer, waarom, hoe)
  const questionPattern = /\b(wie|wat|waar|wanneer|waarom|hoe|which|what|where|when|why|how)\b/i;
  result.hasNaturalLanguage = questionPattern.test(text);

  // Check voor korte antwoorden (zinnen van 8-30 woorden)
  const sentences = text.split(/[.!?]+/);
  let shortAnswerCount = 0;

  for (const sentence of sentences) {
    const words = sentence.trim().split(/\s+/);
    if (words.length >= 8 && words.length <= 30) {
      shortAnswerCount++;
    }
  }

  result.hasShortAnswers = shortAnswerCount >= 3;

  // Check voor conversatietaal (persoonlijke voornaamwoorden, directe aanspreking)
  const conversationalPattern = /\b(je|jij|jouw|je|u|uw|we|wij|onze|I|you|your|we|our|us)\b/i;
  result.hasConversationalTone = conversationalPattern.test(text);

  return result;
}
