import { HtmlSnapshot } from '../scanner';
import { createHash } from 'crypto';

export interface ContentAnalysisResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    language: {
      detected: string;
      confidence: number;
      isSupported: boolean;
    };
    keywords: {
      count: number;
      density: number;
      topKeywords: Array<{
        keyword: string;
        count: number;
        density: number;
      }>;
    };
    duplicateContent: {
      hasDuplicates: boolean;
      duplicateRatio: number;
      duplicateBlocks: Array<{
        text: string;
        hash: string;
        occurrences: number;
      }>;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeContent(htmlSnapshot: HtmlSnapshot | null): ContentAnalysisResult {
  const result: ContentAnalysisResult = {
    score: 0,
    maxScore: 25,
    status: 'success',
    details: {
      language: {
        detected: '',
        confidence: 0,
        isSupported: false,
      },
      keywords: {
        count: 0,
        density: 0,
        topKeywords: [],
      },
      duplicateContent: {
        hasDuplicates: false,
        duplicateRatio: 0,
        duplicateBlocks: [],
      },
    },
    fixes: [],
  };

  if (!htmlSnapshot) {
    result.status = 'danger';
    return result;
  }

  // Taal detectie
  const languageResult = detectLanguage(htmlSnapshot.content);
  result.details.language = languageResult;
  if (languageResult.isSupported) {
    result.score += 10;
  } else {
    result.fixes.push({
      impact: 'high',
      description: `Taal "${languageResult.detected}" wordt niet ondersteund.`,
      fix: 'Zorg ervoor dat de content in een ondersteunde taal is (Nederlands of Engels).',
    });
  }

  // Keyword analyse
  const keywordResult = analyzeKeywords(htmlSnapshot.content);
  result.details.keywords = keywordResult;

  // Score voor keywords
  if (keywordResult.count >= 10) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: 'Te weinig keywords gevonden in de content.',
      fix: 'Voeg meer relevante keywords toe aan de content voor betere vindbaarheid.',
    });
  }

  if (keywordResult.density >= 0.5 && keywordResult.density <= 3) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'medium',
      description: `Keyword density (${keywordResult.density.toFixed(2)}%) is niet optimaal.`,
      fix: 'Pas de keyword density aan naar tussen 0.5% en 3% voor optimale SEO.',
    });
  }

  // Duplicate content check
  const duplicateResult = checkDuplicateContent(htmlSnapshot.content);
  result.details.duplicateContent = duplicateResult;

  if (!duplicateResult.hasDuplicates) {
    result.score += 5;
  } else {
    result.fixes.push({
      impact: 'high',
      description: `Duplicate content ratio van ${(duplicateResult.duplicateRatio * 100).toFixed(
        1
      )}% gevonden.`,
      fix: 'Herzie de content en verwijder of herschrijf dubbele tekstblokken.',
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

function detectLanguage(content: string): ContentAnalysisResult['details']['language'] {
  // Verwijder HTML tags en speciale karakters
  const cleanContent = content
    .replace(/<[^>]*>/g, ' ')
    .replace(/[^\w\s]/g, ' ')
    .trim();

  // Eenvoudige taal detectie op basis van veel voorkomende woorden
  const dutchWords = ['de', 'het', 'en', 'van', 'in', 'is', 'dat', 'een', 'op', 'te'];
  const englishWords = ['the', 'and', 'of', 'to', 'in', 'is', 'that', 'a', 'on', 'for'];

  const words = cleanContent.toLowerCase().split(/\s+/);
  let dutchCount = 0;
  let englishCount = 0;

  for (const word of words) {
    if (dutchWords.includes(word)) dutchCount++;
    if (englishWords.includes(word)) englishCount++;
  }

  const total = dutchCount + englishCount;
  if (total === 0) {
    return {
      detected: 'unknown',
      confidence: 0,
      isSupported: false,
    };
  }

  const isDutch = dutchCount > englishCount;
  const confidence = Math.max(dutchCount, englishCount) / total;

  return {
    detected: isDutch ? 'nl' : 'en',
    confidence,
    isSupported: true, // Beide talen worden ondersteund
  };
}

function analyzeKeywords(content: string): ContentAnalysisResult['details']['keywords'] {
  // Verwijder HTML tags en speciale karakters
  const cleanContent = content
    .replace(/<[^>]*>/g, ' ')
    .replace(/[^\w\s]/g, ' ')
    .trim();

  // Verwijder stopwoorden
  const stopWords = new Set([
    'de',
    'het',
    'en',
    'van',
    'in',
    'is',
    'dat',
    'een',
    'op',
    'te',
    'voor',
    'bij',
    'met',
    'als',
    'naar',
    'om',
    'door',
    'over',
    'uit',
    'aan',
  ]);

  const words = cleanContent
    .toLowerCase()
    .split(/\s+/)
    .filter(word => word.length > 2 && !stopWords.has(word));

  // Tel woorden
  const wordCount = new Map<string, number>();
  for (const word of words) {
    wordCount.set(word, (wordCount.get(word) || 0) + 1);
  }

  // Bereken density
  const totalWords = words.length;
  const keywordCount = wordCount.size;
  const density = (keywordCount / totalWords) * 100;

  // Top keywords
  const topKeywords = Array.from(wordCount.entries())
    .map(([keyword, count]) => ({
      keyword,
      count,
      density: (count / totalWords) * 100,
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);

  return {
    count: keywordCount,
    density,
    topKeywords,
  };
}

function checkDuplicateContent(
  content: string
): ContentAnalysisResult['details']['duplicateContent'] {
  // Verwijder HTML tags en speciale karakters
  const cleanContent = content
    .replace(/<[^>]*>/g, ' ')
    .replace(/[^\w\s]/g, ' ')
    .trim();

  // Verdeel in tekstblokken van 50 woorden
  const words = cleanContent.split(/\s+/);
  const blocks: string[] = [];

  for (let i = 0; i < words.length; i += 50) {
    blocks.push(words.slice(i, i + 50).join(' '));
  }

  // Bereken hashes voor elk blok
  const blockHashes = blocks.map(block => createHash('sha256').update(block).digest('hex'));

  // Tel duplicaten
  const hashCount = new Map<string, number>();
  for (const hash of blockHashes) {
    hashCount.set(hash, (hashCount.get(hash) || 0) + 1);
  }

  // Identificeer duplicaten
  const duplicateBlocks = Array.from(hashCount.entries())
    .filter(([_, count]) => count > 1)
    .map(([hash, count]) => {
      const blockIndex = blockHashes.indexOf(hash);
      return {
        text: blocks[blockIndex],
        hash,
        occurrences: count,
      };
    });

  const duplicateRatio = duplicateBlocks.length / blocks.length;

  return {
    hasDuplicates: duplicateBlocks.length > 0,
    duplicateRatio,
    duplicateBlocks,
  };
}
