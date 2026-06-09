import { HtmlSnapshot } from '../scanner';

export interface MultimodalResult {
  score: number;
  maxScore: number;
  status: 'success' | 'warning' | 'danger';
  details: {
    altText: {
      totalImages: number;
      missingAlt: number;
      poorQualityAlt: number;
    };
    transcripts: {
      totalMediaElements: number;
      withTranscript: number;
      withCaptions: number;
    };
    contentStructure: {
      hasHeadings: boolean;
      hasLists: boolean;
      hasTables: boolean;
      tableWithHeaders: boolean;
    };
  };
  fixes: Array<{
    impact: 'high' | 'medium' | 'low';
    description: string;
    fix: string;
  }>;
}

export function analyzeMultimodal(htmlSnapshot: HtmlSnapshot | null): MultimodalResult {
  const result: MultimodalResult = {
    score: 0,
    maxScore: 5,
    status: 'danger',
    details: {
      altText: {
        totalImages: 0,
        missingAlt: 0,
        poorQualityAlt: 0,
      },
      transcripts: {
        totalMediaElements: 0,
        withTranscript: 0,
        withCaptions: 0,
      },
      contentStructure: {
        hasHeadings: false,
        hasLists: false,
        hasTables: false,
        tableWithHeaders: false,
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

  // 1. Afbeeldingen met alt-tekst analyseren
  const altTextAnalysis = analyzeAltText(html);
  result.details.altText = altTextAnalysis;

  // Score berekenen op basis van alt-tekst kwaliteit
  if (altTextAnalysis.totalImages > 0) {
    const altTextScore = 1 - altTextAnalysis.missingAlt / altTextAnalysis.totalImages;
    // Max 2 punten voor alt-tekst
    result.score += Math.round(altTextScore * 2);

    if (altTextAnalysis.missingAlt > 0) {
      result.fixes.push({
        impact: 'high',
        description: `${altTextAnalysis.missingAlt} afbeelding(en) missen alt-tekst`,
        fix: 'Voeg beschrijvende alt-tekst toe aan alle afbeeldingen, bijvoorbeeld: <img src="voorbeeld.jpg" alt="Beschrijvende tekst over de afbeelding">',
      });
    }

    if (altTextAnalysis.poorQualityAlt > 0) {
      result.fixes.push({
        impact: 'medium',
        description: `${altTextAnalysis.poorQualityAlt} afbeelding(en) hebben lage kwaliteit alt-tekst`,
        fix: 'Verbeter de kwaliteit van de alt-tekst door specifieke, beschrijvende tekst te gebruiken in plaats van generieke woorden',
      });
    }
  }

  // 2. Transcripts en ondertitels voor media analyseren
  const transcriptsAnalysis = analyzeTranscripts(html);
  result.details.transcripts = transcriptsAnalysis;

  // Score berekenen op basis van transcripts
  if (transcriptsAnalysis.totalMediaElements > 0) {
    const transcriptScore =
      transcriptsAnalysis.withTranscript / transcriptsAnalysis.totalMediaElements;
    // Max 1.5 punten voor transcripts/ondertitels
    result.score += Math.round(transcriptScore * 1.5);

    if (transcriptsAnalysis.withTranscript < transcriptsAnalysis.totalMediaElements) {
      result.fixes.push({
        impact: 'medium',
        description: 'Niet alle media-elementen hebben transcripts of ondertitels',
        fix: 'Voeg transcripts toe aan audio- en video-elementen, of gebruik ondertitelingsbestanden (captions)',
      });
    }
  }

  // 3. Analyseer content structuur
  const contentStructureAnalysis = analyzeContentStructure(html);
  result.details.contentStructure = contentStructureAnalysis;

  // Score berekenen op basis van structuur
  let structureScore = 0;
  if (contentStructureAnalysis.hasHeadings) structureScore += 0.5;
  if (contentStructureAnalysis.hasLists) structureScore += 0.25;
  if (contentStructureAnalysis.hasTables && contentStructureAnalysis.tableWithHeaders)
    structureScore += 0.75;

  // Max 1.5 punten voor structuur
  result.score += Math.min(1.5, structureScore);

  if (!contentStructureAnalysis.hasHeadings) {
    result.fixes.push({
      impact: 'high',
      description: 'Pagina mist duidelijke koppenstructuur',
      fix: 'Gebruik koppenstructuur (h1, h2, h3) om content hierarchisch te organiseren',
    });
  }

  if (contentStructureAnalysis.hasTables && !contentStructureAnalysis.tableWithHeaders) {
    result.fixes.push({
      impact: 'medium',
      description: 'Tabellen zonder koprijen gevonden',
      fix: 'Gebruik <th> elementen in tabellen om kolomkoppen aan te geven voor betere toegankelijkheid',
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

function analyzeAltText(html: string): MultimodalResult['details']['altText'] {
  const result = {
    totalImages: 0,
    missingAlt: 0,
    poorQualityAlt: 0,
  };

  // Zoek alle img elementen
  const imgRegex = /<img[^>]*>/g;
  const imgMatches = html.match(imgRegex) || [];

  result.totalImages = imgMatches.length;

  // Controleer voor ontbrekende alt tekst
  const missingAltRegex = /<img[^>]*(?:alt=""|alt=''|alt=[^"'][^>]*|(?!alt)[^>]*)>/g;
  const missingAltMatches = html.match(missingAltRegex) || [];

  result.missingAlt = missingAltMatches.length;

  // Controleer voor lage kwaliteit alt tekst
  const poorQualityPhrases = [
    'image',
    'picture',
    'afbeelding',
    'foto',
    'plaatje',
    'graphic',
    'png',
    'jpg',
    'jpeg',
    'gif',
    'webp',
  ];

  for (const imgTag of imgMatches) {
    const altMatch = imgTag.match(/alt=["']([^"']*)["']/i);
    if (altMatch && altMatch[1]) {
      const altText = altMatch[1].toLowerCase();
      // Controleer of de alt-tekst alleen uit standaard woorden bestaat of te kort is
      if (
        altText.length < 5 ||
        poorQualityPhrases.some(phrase => altText === phrase) ||
        /^img\d+$/i.test(altText) // Detecteert patronen als "img1", "IMG2"
      ) {
        result.poorQualityAlt++;
      }
    }
  }

  return result;
}

function analyzeTranscripts(html: string): MultimodalResult['details']['transcripts'] {
  const result = {
    totalMediaElements: 0,
    withTranscript: 0,
    withCaptions: 0,
  };

  // Zoek alle audio en video elementen
  const audioRegex = /<audio[^>]*>/g;
  const videoRegex = /<video[^>]*>/g;
  const iframeRegex = /<iframe[^>]*(?:youtube|vimeo)[^>]*>/gi;

  const audioMatches = html.match(audioRegex) || [];
  const videoMatches = html.match(videoRegex) || [];
  const iframeMatches = html.match(iframeRegex) || [];

  result.totalMediaElements = audioMatches.length + videoMatches.length + iframeMatches.length;

  // Controleer voor ondertiteling/transcripts bij video
  // Dit is een simplistische benadering; in een echte implementatie zou je ook
  // track elementen, WebVTT bestanden, en transcript containers moeten controleren

  const trackRegex = /<track[^>]*kind=["'](?:captions|subtitles)["'][^>]*>/gi;
  const captionMatches = html.match(trackRegex) || [];
  result.withCaptions = captionMatches.length;

  // Controleer voor transcript secties
  const transcriptSectionRegex =
    /(?:<div[^>]*class=["'][^"']*transcript[^"']*["'][^>]*>|<details[^>]*>.*?<summary[^>]*>.*?transcript)/gi;
  const transcriptMatches = html.match(transcriptSectionRegex) || [];

  // Tel ze bij de captioned elementen op, maar niet dubbel tellen
  result.withTranscript = Math.min(
    result.totalMediaElements,
    result.withCaptions + transcriptMatches.length
  );

  return result;
}

function analyzeContentStructure(html: string): MultimodalResult['details']['contentStructure'] {
  const result = {
    hasHeadings: false,
    hasLists: false,
    hasTables: false,
    tableWithHeaders: false,
  };

  // Controleer koppen
  const headingsRegex = /<h[1-6][^>]*>/i;
  result.hasHeadings = headingsRegex.test(html);

  // Controleer lijsten
  const listsRegex = /<(?:ul|ol)[^>]*>/i;
  result.hasLists = listsRegex.test(html);

  // Controleer tabellen
  const tablesRegex = /<table[^>]*>/i;
  result.hasTables = tablesRegex.test(html);

  // Controleer voor tabelkoppen
  if (result.hasTables) {
    const tableHeadersRegex = /<th[^>]*>/i;
    result.tableWithHeaders = tableHeadersRegex.test(html);
  }

  return result;
}
