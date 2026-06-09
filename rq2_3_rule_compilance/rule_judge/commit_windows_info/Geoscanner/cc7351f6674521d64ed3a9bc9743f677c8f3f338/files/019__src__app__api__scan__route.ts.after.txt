import { NextResponse } from 'next/server';
import { Scanner } from '@/lib/scanner';

export async function POST(request: Request) {
  try {
    const { url, fullDomainScan } = await request.json();

    if (!url) {
      return NextResponse.json({ error: 'URL is verplicht' }, { status: 400 });
    }

    const result = await Scanner.scan(url, { fullDomainScan });

    // Bereken overall score en modules
    const modules = [];
    let totalScore = 0;
    let maxTotalScore = 0;

    if (result.crawlAccess) {
      modules.push({
        id: 'crawl-access',
        name: 'Crawl-toegang',
        score: result.crawlAccess.score,
        maxScore: result.crawlAccess.maxScore,
        status: result.crawlAccess.status,
        details: [
          result.crawlAccess.details.robotsTxt.exists
            ? 'Robots.txt is aanwezig'
            : 'Robots.txt ontbreekt',
          result.crawlAccess.details.sitemap.exists
            ? 'Sitemap.xml is aanwezig'
            : 'Sitemap.xml ontbreekt',
          result.crawlAccess.details.metaRobots.exists
            ? 'Meta robots tags zijn aanwezig'
            : 'Meta robots tags ontbreken',
        ],
      });
      totalScore += result.crawlAccess.score;
      maxTotalScore += result.crawlAccess.maxScore;
    }

    if (result.structuredData) {
      modules.push({
        id: 'structured-data',
        name: 'Structured Data',
        score: result.structuredData.score,
        maxScore: result.structuredData.maxScore,
        status: result.structuredData.status,
        details: [
          result.structuredData.details.jsonLd.exists ? 'JSON-LD is aanwezig' : 'JSON-LD ontbreekt',
          result.structuredData.details.openGraph.exists
            ? 'Open Graph tags zijn aanwezig'
            : 'Open Graph tags ontbreken',
          result.structuredData.details.jsonLd.schemaTypes.length > 0
            ? `Schema.org types gevonden: ${result.structuredData.details.jsonLd.schemaTypes.join(
                ', '
              )}`
            : 'Geen Schema.org types gevonden',
        ],
      });
      totalScore += result.structuredData.score;
      maxTotalScore += result.structuredData.maxScore;
    }

    if (result.contentAnalysis) {
      modules.push({
        id: 'content-analysis',
        name: 'Content Analyse',
        score: result.contentAnalysis.score,
        maxScore: result.contentAnalysis.maxScore,
        status: result.contentAnalysis.status,
        details: [
          `Taal gedetecteerd: ${result.contentAnalysis.details.language.detected}`,
          `Aantal keywords: ${result.contentAnalysis.details.keywords.count}`,
          result.contentAnalysis.details.duplicateContent.hasDuplicates
            ? 'Duplicatie gedetecteerd'
            : 'Geen duplicatie gedetecteerd',
        ],
      });
      totalScore += result.contentAnalysis.score;
      maxTotalScore += result.contentAnalysis.maxScore;
    }

    if (result.technicalSeo) {
      modules.push({
        id: 'technical-seo',
        name: 'Technical SEO',
        score: result.technicalSeo.score,
        maxScore: result.technicalSeo.maxScore,
        status: result.technicalSeo.status,
        details: [
          `Laadtijd: ${result.technicalSeo.details.performance.loadTime}ms`,
          result.technicalSeo.details.mobileFriendly.isMobileFriendly
            ? 'Mobiel-vriendelijk'
            : 'Niet mobiel-vriendelijk',
          result.technicalSeo.details.security.ssl
            ? 'SSL beveiliging aanwezig'
            : 'SSL beveiliging ontbreekt',
        ],
      });
      totalScore += result.technicalSeo.score;
      maxTotalScore += result.technicalSeo.maxScore;
    }

    // Nieuwe modules toevoegen
    if (result.answerReady) {
      modules.push({
        id: 'answer-ready',
        name: 'Answer-ready Content',
        score: result.answerReady.score,
        maxScore: result.answerReady.maxScore,
        status: result.answerReady.status,
        details: [
          result.answerReady.details.faq.hasFaqStructure
            ? `FAQ structuur gevonden (${result.answerReady.details.faq.faqCount} vragen)`
            : 'Geen FAQ structuur gevonden',
          result.answerReady.details.featuredSnippet.hasPotential
            ? 'Content heeft snippet potentieel'
            : 'Content mist snippet potentieel',
          result.answerReady.details.voiceSearch.hasNaturalLanguage
            ? 'Natuurlijke taal voor voice search aanwezig'
            : 'Natuurlijke taal voor voice search ontbreekt',
        ],
      });
      totalScore += result.answerReady.score;
      maxTotalScore += result.answerReady.maxScore;
    }

    if (result.authority) {
      modules.push({
        id: 'authority',
        name: 'Autoriteit & Citaties',
        score: result.authority.score,
        maxScore: result.authority.maxScore,
        status: result.authority.status,
        details: [
          result.authority.details.authorBio.present
            ? `Auteur bio aanwezig (${result.authority.details.authorBio.authorName || 'naamloos'})`
            : 'Geen auteur bio gevonden',
          `${result.authority.details.outboundLinks.totalCount} outbound links, waarvan ${result.authority.details.outboundLinks.authorityDomainsCount} naar autoriteitsdomeinen`,
          result.authority.details.licenseInfo.present
            ? `Licentie informatie aanwezig (${result.authority.details.licenseInfo.type})`
            : 'Geen licentie informatie gevonden',
        ],
      });
      totalScore += result.authority.score;
      maxTotalScore += result.authority.maxScore;
    }

    if (result.freshness) {
      modules.push({
        id: 'freshness',
        name: 'Versheid Analyse',
        score: result.freshness.score,
        maxScore: result.freshness.maxScore,
        status: result.freshness.status,
        details: [
          result.freshness.details.publishDate.present
            ? `Publicatiedatum: ${result.freshness.details.publishDate.date}`
            : 'Geen publicatiedatum gevonden',
          result.freshness.details.modifiedDate.present
            ? `Laatst bijgewerkt: ${result.freshness.details.modifiedDate.date}`
            : 'Geen wijzigingsdatum gevonden',
          result.freshness.details.contentFreshness.ageInDays !== null
            ? `Content leeftijd: ${result.freshness.details.contentFreshness.ageInDays} dagen`
            : 'Content leeftijd onbekend',
        ],
      });
      totalScore += result.freshness.score;
      maxTotalScore += result.freshness.maxScore;
    }

    if (result.crossWeb) {
      modules.push({
        id: 'cross-web',
        name: 'Cross-web Footprint',
        score: result.crossWeb.score,
        maxScore: result.crossWeb.maxScore,
        status: result.crossWeb.status,
        details: [
          result.crossWeb.details.sameAsLinks.present
            ? `SameAs links gevonden: ${
                result.crossWeb.details.sameAsLinks.count
              } (${result.crossWeb.details.sameAsLinks.platforms.join(', ')})`
            : 'Geen SameAs links gevonden',
          result.crossWeb.details.externalMentions.hasWikipedia ||
          result.crossWeb.details.externalMentions.hasWikidata
            ? `Vermeldingen: ${[
                result.crossWeb.details.externalMentions.hasWikipedia ? 'Wikipedia' : '',
                result.crossWeb.details.externalMentions.hasWikidata ? 'Wikidata' : '',
              ]
                .filter(Boolean)
                .join(', ')}`
            : 'Geen vermeldingen op Wikipedia/Wikidata',
          `Backlinks: ${result.crossWeb.details.backlinks.count} (${result.crossWeb.details.backlinks.authorityDomains.length} autoriteitsdomeinen)`,
        ],
      });
      totalScore += result.crossWeb.score;
      maxTotalScore += result.crossWeb.maxScore;
    }

    if (result.multimodal) {
      modules.push({
        id: 'multimodal',
        name: 'Multimodale Toegankelijkheid',
        score: result.multimodal.score,
        maxScore: result.multimodal.maxScore,
        status: result.multimodal.status,
        details: [
          `Afbeeldingen: ${
            result.multimodal.details.altText.totalImages -
            result.multimodal.details.altText.missingAlt
          }/${result.multimodal.details.altText.totalImages} met alt tekst`,
          `Media: ${result.multimodal.details.transcripts.withTranscript}/${result.multimodal.details.transcripts.totalMediaElements} met transcripts/ondertitels`,
          `Structuur: ${[
            result.multimodal.details.contentStructure.hasHeadings ? 'Koppen' : '',
            result.multimodal.details.contentStructure.hasLists ? 'Lijsten' : '',
            result.multimodal.details.contentStructure.hasTables ? 'Tabellen' : '',
          ]
            .filter(Boolean)
            .join(', ')}`,
        ],
      });
      totalScore += result.multimodal.score;
      maxTotalScore += result.multimodal.maxScore;
    }

    if (result.monitoring) {
      modules.push({
        id: 'monitoring',
        name: 'Monitoring & Analytics',
        score: result.monitoring.score,
        maxScore: result.monitoring.maxScore,
        status: result.monitoring.status,
        details: [
          result.monitoring.details.analytics.tools.length > 0
            ? `Analytics: ${result.monitoring.details.analytics.tools.join(', ')}`
            : 'Geen analytics tools gevonden',
          result.monitoring.details.monitoring.tools.length > 0
            ? `Monitoring: ${result.monitoring.details.monitoring.tools.join(', ')}`
            : 'Geen monitoring tools gevonden',
          `Privacy: ${
            [
              result.monitoring.details.dataCollection.hasConsent ? 'Consent Manager' : '',
              result.monitoring.details.dataCollection.hasCookieBanner ? 'Cookie Banner' : '',
              result.monitoring.details.dataCollection.hasPrivacyControls ? 'Privacy Controls' : '',
            ]
              .filter(Boolean)
              .join(', ') || 'Geen privacy controles gevonden'
          }`,
        ],
      });
      totalScore += result.monitoring.score;
      maxTotalScore += result.monitoring.maxScore;
    }

    if (result.schemaAdvanced) {
      modules.push({
        id: 'schema-advanced',
        name: 'Diepgaande Schema.org Analyse',
        score: result.schemaAdvanced.score,
        maxScore: result.schemaAdvanced.maxScore,
        status: result.schemaAdvanced.status,
        details: [
          `Volledigheid: ${Math.round(
            result.schemaAdvanced.details.completeness.averageCompleteness * 100
          )}% (${result.schemaAdvanced.details.completeness.schemaTypesFound.length} types)`,
          result.schemaAdvanced.details.technical.hasErrors
            ? `Technisch: ${
                result.schemaAdvanced.details.technical.syntaxErrors.length +
                result.schemaAdvanced.details.technical.invalidProperties.length +
                result.schemaAdvanced.details.technical.deprecatedProperties.length
              } fouten gevonden`
            : 'Technisch: Geen fouten gevonden',
          `Hiërarchie: ${
            result.schemaAdvanced.details.hierarchy.hasProperHierarchy
              ? 'Goede structuur'
              : 'Verbetering nodig'
          } (${result.schemaAdvanced.details.hierarchy.nestedLevels} niveaus)`,
        ],
      });
      totalScore += result.schemaAdvanced.score;
      maxTotalScore += result.schemaAdvanced.maxScore;
    }

    // Bereken overall score
    const overallScore = maxTotalScore > 0 ? Math.round((totalScore / maxTotalScore) * 100) : 0;

    // Genereer quick wins
    const quickWins = [];

    if (result.structuredData?.fixes) {
      quickWins.push(
        ...result.structuredData.fixes.map(fix => ({
          module: 'Structured Data',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.contentAnalysis?.fixes) {
      quickWins.push(
        ...result.contentAnalysis.fixes.map(fix => ({
          module: 'Content Analyse',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.technicalSeo?.fixes) {
      quickWins.push(
        ...result.technicalSeo.fixes.map(fix => ({
          module: 'Technical SEO',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    // Quick wins van nieuwe modules toevoegen
    if (result.answerReady?.fixes) {
      quickWins.push(
        ...result.answerReady.fixes.map(fix => ({
          module: 'Answer-ready Content',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.authority?.fixes) {
      quickWins.push(
        ...result.authority.fixes.map(fix => ({
          module: 'Autoriteit & Citaties',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.freshness?.fixes) {
      quickWins.push(
        ...result.freshness.fixes.map(fix => ({
          module: 'Versheid Analyse',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.crossWeb?.fixes) {
      quickWins.push(
        ...result.crossWeb.fixes.map(fix => ({
          module: 'Cross-web Footprint',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.multimodal?.fixes) {
      quickWins.push(
        ...result.multimodal.fixes.map(fix => ({
          module: 'Multimodale Toegankelijkheid',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.monitoring?.fixes) {
      quickWins.push(
        ...result.monitoring.fixes.map(fix => ({
          module: 'Monitoring & Analytics',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    if (result.schemaAdvanced?.fixes) {
      quickWins.push(
        ...result.schemaAdvanced.fixes.map(fix => ({
          module: 'Diepgaande Schema.org Analyse',
          impact: fix.impact,
          description: fix.description,
          fix: fix.fix,
        }))
      );
    }

    return NextResponse.json({
      ...result,
      overallScore,
      modules,
      quickWins,
    });
  } catch (error) {
    console.error('Scan error:', error);
    return NextResponse.json(
      { error: 'Er is een fout opgetreden tijdens het scannen' },
      { status: 500 }
    );
  }
}
