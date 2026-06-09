# GEO Scanner v1.0 - Functionele Eisen & UX Specificatie

Dit document beschrijft de functionele eisen en gebruikerservaringen (UX) voor de GEO Scanner v1.0, een applicatie die webpagina's analyseert op hun geschiktheid voor AI zoekmachines en LLM-visibility.

## Inhoudsopgave

1. [Doelstellingen & Gebruikersgroepen](#1-doelstellingen--gebruikersgroepen)
2. [Functionele Eisen](#2-functionele-eisen)
3. [Gebruikersflows](#3-gebruikersflows)
4. [Schermontwerpen](#4-schermontwerpen)
5. [UX Componenten & Interacties](#5-ux-componenten--interacties)
6. [Feedbacksystemen](#6-feedbacksystemen)
7. [Rapportage & Exports](#7-rapportage--exports)
8. [Toegankelijkheid & Gebruiksgemak](#8-toegankelijkheid--gebruiksgemak)

## 1. Doelstellingen & Gebruikersgroepen

### 1.1 Kernbelofte

GEO Scanner biedt gebruikers de mogelijkheid om binnen 10 seconden te zien hoe _LLM-proof_ hun webpagina is, gemeten op acht cruciale criteria die de zichtbaarheid in AI chatbots en zoekmachines bepalen.

### 1.2 Doelgroepen & Behoeften

| Gebruikersgroep             | Primaire Behoefte                                                                           | GEO Scanner Waardepropositie                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Content-/SEO-specialist** | Inzicht krijgen of hun landingspagina's zichtbaar worden in ChatGPT, Gemini, Claude of Grok | Één dashboard met een duidelijke score in plaats van handmatig testen in elke AI tool |
| **Agency-consultant**       | Snel een audit-rapport kunnen genereren voor klanten                                        | White-label PDF exports en gedetailleerde fix-voorstellen                             |
| **Founder / marketeer**     | Zekerheid dat hun site toekomstbestendig is voor AI-zoekopdrachten                          | Kleurcodes, een overall score en een geprioriteerde fix-lijst                         |

### 1.3 Gebruikerscontext

Content- en SEO-specialisten:

- Hebben minimaal basiskennis van SEO en structured data
- Werken vaak onder tijdsdruk
- Willen vooral weten wat ze moeten veranderen, niet alleen wat er mis is
- Gebruiken de tool frequent (meerdere keren per week)

Agency-consultants:

- Hebben uitgebreide kennis van SEO en content-optimalisatie
- Scannen meerdere sites per dag
- Willen vooral professioneel ogende rapporten om aan klanten te presenteren
- Hebben behoefte aan white-label opties

Founders en marketeers:

- Hebben variërende technische kennis
- Zijn vooral geïnteresseerd in de "grote lijnen" en quick wins
- Willen inzicht zonder technisch jargon
- Gebruiken de tool minder frequent (maandelijks)

## 2. Functionele Eisen

### 2.1 Kernfunctionaliteiten

#### Scan Initiatie

- **F1.1** - Gebruikers kunnen een URL invoeren om een scan te starten
- **F1.2** - Systeem valideert URLs op geldigheid (HTTP/HTTPS formaat)
- **F1.3** - Optie om een volledige domeinscan te kiezen (meerdere pagina's)
- **F1.4** - Scan start met één klik na URL-invoer

#### Analyse Pipeline

- **F2.1** - Systeem haalt HTML, robots.txt en sitemap.xml op
- **F2.2** - Systeem voert 8 parallelle analysemodules uit (zoals gespecificeerd in [Module Specificaties](#24-module-specificaties))
- **F2.3** - Resultaten worden opgeslagen onder een unieke scan-ID
- **F2.4** - Voortgangsindicator toont real-time status van de scan

#### Resultaatweergave

- **F3.1** - Overall score tussen 0-100 punten met kleurcodering (rood, oranje, groen)
- **F3.2** - Radar chart visualiseert scores op alle 8 modules
- **F3.3** - Maximaal 5 quick-wins worden gepresenteerd, geordend op impact
- **F3.4** - Per module een uitklapbaar detailpaneel met score en verbetervoorstellen

#### Export & Monitoring

- **F4.1** - Export functie voor PDF-rapport
- **F4.2** - Export functie voor JSON data (voor ontwikkelaars)
- **F4.3** - Optie voor dagelijkse re-scan + waarschuwingen (pro-plan)
- **F4.4** - Historische resultaten bekijken en vergelijken

### 2.2 Gebruikersbeheer

- **F5.1** - Registratie met email/wachtwoord of social login (Google, GitHub)
- **F5.2** - Persoonlijk dashboard met scan geschiedenis
- **F5.3** - Plannen: Gratis (beperkt aantal scans), Pro (meer features) en Agency (white-label)
- **F5.4** - Profielinstellingen beheren (naam, bedrijf, email voorkeuren)

### 2.3 Admin & Analytics

- **F6.1** - Admin dashboard voor gebruikersbeheer (alleen voor systeembeheerders)
- **F6.2** - Gebruiksstatistieken (aantal scans, populaire features)
- **F6.3** - Systeem health monitoring

### 2.4 Module Specificaties

De 8 analysemodules die de scan uitvoert:

1. **Crawl-toegang** (0-25 punten)

   - Controleert robots.txt regels voor AI bots
   - Verifieert aanwezigheid en geldigheid van sitemap.xml
   - Controleert HTTP-status codes en meta-robots tags

2. **Structured Data** (0-25 punten)

   - Parseert JSON-LD blokken
   - Detecteert schema-types
   - Valideert verplichte velden

3. **Answer-ready content** (0-20 punten)

   - Controleert op TL;DR en optimale lengte
   - Beoordeelt vraag-en-antwoord structuur
   - Analyseert leesbaarheid (Flesch score)

4. **Autoriteit & citaties** (0-15 punten)

   - Controleert op auteur-bio met expertise-indicatoren
   - Analyseert outbound links naar autoriteitswebsites
   - Verifieert aanwezigheid van licentie statements

5. **Versheid** (0-10 punten)

   - Controleert datePublished & dateModified in HTML en JSON-LD
   - Valideert sitemap lastmod tegen dateModified
   - Detecteert "fake freshness"

6. **Cross-web footprint** (0-10 punten)

   - Parseert sameAs-links
   - Verifieert HTTP 200-status op gelinkte resources
   - Controleert aanwezigheid in Wikidata/Wikipedia

7. **Multimodale leesbaarheid** (0-5 punten)

   - Telt aantal afbeeldingen zonder alt-tekst
   - Controleert op transcripts voor audio/video
   - Onderzoekt gebruik van lazy-load attributen

8. **Monitoring-haakjes** (0-5 punten)
   - Controleert op JavaScript-beacon of logging snippet
   - Valideert webhook-URLs voor realtime alerts

### 2.5 Score Berekening

- Elke module heeft een eigen puntenschaal afgestemd op belang
- Drempelwaarden voor statuskleuren:
  - Groen: ≥ 80% van max module-score
  - Oranje: 40-79% van max
  - Rood: < 40%
- Overall score berekening:
  - Modules 1 & 2 = 25% elk
  - Module 3 = 20%
  - Module 4 = 15%
  - Module 5 = 10%
  - Modules 6-8 samen = 5%
- Overall kleurcodes:
  - Groen: ≥ 80/100 punten
  - Oranje: 50-79 punten
  - Rood: < 50 punten

## 3. Gebruikersflows

### 3.1 Hoofdflow: URL Scannen

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Homepage    │     │ URL         │     │ In-Progress │     │ Resultaten  │     │ Detail View │
│             │ ──► │ Invoer      │ ──► │ Scan        │ ──► │ Dashboard   │ ──► │ per Module  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                                        │                   │
                          │                                        │                   │
                          ▼                                        ▼                   ▼
                    ┌─────────────┐                        ┌─────────────┐     ┌─────────────┐
                    │ URL         │                        │ PDF Export  │     │ Fix         │
                    │ Validatie   │                        │             │     │ Implementatie│
                    └─────────────┘                        └─────────────┘     └─────────────┘
```

#### Gedetailleerde stappen:

1. **Homepage Bezoek**

   - Gebruiker landt op homepage
   - Ziet hero-sectie met grote URL-invoer en "Scan" knop
   - Korte uitleg van de tool is zichtbaar

2. **URL Invoer**

   - Gebruiker voert een URL in
   - Systeem valideert het URL-formaat real-time
   - Gebruiker selecteert optioneel "Volledige domeinscan"
   - Gebruiker klikt op "Scan"

3. **In-Progress Scan**

   - Systeem toont een voortgangsindicator
   - Live log updates tonen welke module momenteel wordt uitgevoerd
   - Geschatte tijd tot voltooiing wordt getoond

4. **Resultaten Dashboard**

   - Grote cirkel met overall score (bijv. "78/100")
   - Kleurcode (rood/oranje/groen) indiceert status
   - Radar chart toont scores per module
   - Top 5 quick-win suggesties worden getoond
   - "Download PDF" knop is prominent aanwezig

5. **Detail View per Module**
   - Gebruiker klapt een module uit om details te zien
   - Module-specifieke scores en aanbevelingen worden getoond
   - Code-snippets met fixes worden getoond waar relevant
   - Informatieve tooltips leggen technische termen uit

### 3.2 Gebruikersregistratie & Login Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Homepage    │     │ Registratie │     │ Email       │     │ Dashboard   │
│             │ ──► │ Formulier   │ ──► │ Verificatie │ ──► │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │
      │                    │
      ▼                    ▼
┌─────────────┐     ┌─────────────┐
│ Login       │     │ Social      │
│ Formulier   │     │ Login       │
└─────────────┘     └─────────────┘
```

### 3.3 Rapport Export Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Resultaten  │     │ Export      │     │ Download    │
│ Dashboard   │ ──► │ Opties      │ ──► │ Bestand     │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          │
                          ▼
                    ┌─────────────┐
                    │ Email       │
                    │ Rapport     │
                    └─────────────┘
```

## 4. Schermontwerpen

### 4.1 Homepage / Scan Initiatie

De homepage is minimalistisch en focust volledig op de hoofdfunctie: het scannen van een URL.

**Hoofdelementen:**

- **Hero Sectie**

  - Pakkende header: "Is jouw website LLM-proof?"
  - Subtekst: "Scan je pagina en ontdek in 10 seconden hoe goed jouw content zichtbaar is in ChatGPT, Claude en Google Gemini"
  - Groot URL-invoerveld
  - Prominente "Scan" knop in accentkleur
  - Toggle voor "Volledige domeinscan"

- **Info Sectie**

  - Korte uitleg van de 8 modules met iconen
  - "Hoe het werkt" stappenplan
  - Testimonials/social proof

- **Footer**
  - Links naar gebruiksvoorwaarden, privacy beleid
  - Contactinformatie
  - Verwijzing naar prijsplannen

### 4.2 Voortgangsscherm

Toont de real-time status van de scan met voldoende feedback om de gebruiker geïnformeerd te houden.

**Hoofdelementen:**

- **Voortgangsindicator**

  - Circulaire voortgangsbalk (0-100%)
  - Percentage voltooiing
  - Geschatte tijd tot voltooiing

- **Live Log**

  - Scrollend vak met updates: "Checking structured data..."
  - Laatste actie is altijd zichtbaar
  - Animaties houden het scherm levendig

- **URL Preview**
  - Verkleinde weergave van de gescande URL
  - Optie om scan te annuleren

### 4.3 Resultaten Dashboard

Het hart van de applicatie, waar alle scanresultaten overzichtelijk worden gepresenteerd.

**Hoofdelementen:**

- **Linker Paneel**

  - Grote cirkel-score (bijv. "78/100")
  - Kleurcodering (rood/oranje/groen)
  - "Download PDF" knop
  - "Deel Resultaten" knop
  - "Scan opnieuw" optie

- **Rechter Paneel**

  - Radar chart met 8 assen, één voor elke module
  - Kleurgecodeerde gebieden op de chart

- **Quick Wins Sectie**

  - Geprioriteerde lijst van maximaal 5 verbeterpunten
  - Impact-indicatie per verbeterpunt
  - Uitklapbare code-snippets met fixes

- **Module Details (accordeon stijl)**
  - Uitklapbare secties per module
  - Score en status per module
  - Gedetailleerde bevindingen
  - Fix-instructies met code voorbeelden

### 4.4 PDF Rapport

Het PDF rapport is professioneel vormgegeven en bevat alle relevante informatie in een presenteerbare vorm.

**Hoofdelementen:**

- **Cover Pagina**

  - GEO Scanner logo (of white-label optie)
  - URL van gescande pagina
  - Datum van scan
  - Overall score met kleurindicatie

- **Samenvatting Pagina**

  - Radar chart van alle modules
  - Top 5 quick wins in volgorde van prioriteit
  - Vergelijking met industrie benchmark (indien beschikbaar)

- **Detail Pagina's**

  - Eén pagina per module
  - Gedetailleerde bevindingen
  - Screenshots van problematische elementen
  - Code-snippets met fixes

- **Aanbevelingen Pagina**
  - Geconsolideerde lijst van alle verbeterpunten
  - Implementatie roadmap suggestie
  - Verwachte impact na implementatie

## 5. UX Componenten & Interacties

### 5.1 Primaire Interactie-elementen

De volgende interactie-elementen zijn cruciaal voor een soepele gebruikerservaring:

**URL Invoerveld**

- Real-time validatie met visuele feedback
- Suggesties bij typen (voor eerder gescande URLs)
- Duidelijke focus-state

**Scan Progress Indicator**

- Bewegende elementen om voortgang te tonen
- Voldoende detail over huidige activiteit
- Animaties die niet afleiden maar informeren

**Radar Chart**

- Interactieve hover states die module details tonen
- Kleurcoderingen consistent met rest van de UI
- Animatie bij eerste weergave voor visuele impact

**Score Cirkel**

- Grote, leesbare cijfers
- Kleurovergang van rood naar groen
- Animatie bij het laden voor aandacht

**Module Accordions**

- Soepele uitklap-animaties
- Duidelijke indicatie van huidige staat (open/gesloten)
- Voldoende witruimte voor leesbaarheid

### 5.2 Microinteracties

Microinteracties verbeteren de gebruikerservaring en maken de app meer intuïtief:

- **URL Validatie Feedback**: Subtiele shake-animatie en rood highlight bij ongeldige URL
- **Score Counters**: Cijfers tellen op van 0 naar eindwaarde bij eerste weergave
- **Hover States**: Alle interactieve elementen hebben duidelijke hover states
- **Toast Notifications**: Voor succesvolle acties (export, delen)
- **Loading States**: Skeletonschermen tijdens het laden van nieuwe content
- **Transitions**: Soepele overgangen tussen pagina's en staten

### 5.3 Responsive Design Principes

De applicatie is volledig responsief met specifieke optimalisaties voor verschillende schermformaten:

**Desktop (>1200px)**

- Volledige twee-kolom layout voor resultaten
- Radar chart naast score cirkel
- Volledige feature set zichtbaar

**Tablet (768-1200px)**

- Verticale layout waarbij radar chart onder score cirkel komt
- Compactere module accordions
- Alle features blijven beschikbaar

**Mobiel (<768px)**

- Single-column layout
- Vereenvoudigde radar chart
- Focus op score en quick wins
- Detail panels op aparte pagina's toegankelijk

### 5.4 UI Componenten Specificatie

| Component          | Functie                         | Gedrag                | Variant                                          |
| ------------------ | ------------------------------- | --------------------- | ------------------------------------------------ |
| **Score Cirkel**   | Toont overall score             | Animatie bij laden    | Success (groen), Warning (oranje), Danger (rood) |
| **Radar Chart**    | Visualiseert scores per module  | Interactief bij hover | Compact, Full                                    |
| **URL Input**      | Invoer voor te scannen URL      | Real-time validatie   | Default, Error, With Domain Toggle               |
| **Module Card**    | Container voor module info      | Uitklapbaar           | Collapsed, Expanded                              |
| **Progress Bar**   | Toont scan voortgang            | Real-time updates     | Linear, Circular                                 |
| **Quick Win Item** | Toont individuele fix suggestie | Uitklapbaar           | High Impact, Medium Impact                       |
| **Export Button**  | Initieert export flow           | Dropdown met opties   | PDF, JSON                                        |
| **Code Snippet**   | Toont fix voorbeelden           | Kopieerbaar           | HTML, JSON-LD, Meta                              |

## 6. Feedbacksystemen

### 6.1 Gebruikersfeedback Mechanismen

- **Scan Resultaten Feedback**: Gebruikers kunnen aangeven of suggesties nuttig waren
- **Fix Implementatie Bevestiging**: Gebruikers kunnen fixes markeren als "geïmplementeerd"
- **Rapport Evaluatie**: Rating system voor de kwaliteit van het rapport
- **NPS Survey**: Na 3 scans krijgen gebruikers een Net Promoter Score vraag

### 6.2 Error States & Berichten

De applicatie biedt duidelijke en actionable foutmeldingen:

**URL Validatie Errors**

- "Voer een geldige URL in beginnend met http:// of https://"
- "Deze URL lijkt niet bereikbaar. Controleer of de site online is."

**Scan Process Errors**

- "We kunnen geen toegang krijgen tot deze URL vanwege robots.txt restricties."
- "De scan is onderbroken. Probeer het opnieuw."

**Authentication Errors**

- "Onjuiste inloggegevens. Probeer het opnieuw."
- "Je sessie is verlopen. Log opnieuw in."

### 6.3 Empty States

Lege staten zijn ontworpen om instructief en aanmoedigend te zijn:

**Dashboard zonder Scans**

- Illustratie van een lege radar chart
- Tekst: "Nog geen scans uitgevoerd. Start je eerste scan om je LLM-score te ontdekken."
- Prominente "Start Scan" knop

**Geen Quick Wins**

- Illustratie van een trofee
- Tekst: "Gefeliciteerd! We hebben geen verbeterpunten gevonden. Jouw pagina is optimaal LLM-proof."

## 7. Rapportage & Exports

### 7.1 PDF Rapport Specificaties

- **Formaat**: A4, portrait
- **Branding**: Logo bovenaan elke pagina (white-label optie voor pro-gebruikers)
- **Secties**:
  1. Cover met URL en score
  2. Executive summary
  3. Module-by-module breakdown
  4. Aanbevelingen
  5. Technische appendix

### 7.2 JSON Export Specificaties

```json
{
  "scan_id": "s123456",
  "url": "https://example.com",
  "date": "2025-05-15T14:32:10Z",
  "overall_score": 78,
  "status": "orange",
  "modules": [
    {
      "id": "crawl_access",
      "name": "Crawl-toegang",
      "score": 20,
      "max_score": 25,
      "percentage": 80,
      "status": "green",
      "details": {...},
      "fixes": [...]
    },
    // Andere modules...
  ],
  "quick_wins": [
    {
      "module": "structured_data",
      "impact": "high",
      "description": "Voeg author property toe aan JSON-LD",
      "code_fix": "...",
      "urls_affected": [...]
    },
    // Andere quick wins...
  ]
}
```

### 7.3 White-label Opties (Pro Plan)

- Verwijdering van GEO Scanner branding
- Eigen logo toevoegen
- Eigen kleuren configureren
- Aangepaste intro en conclusie teksten
- Eigen domein voor gedeelde rapportlinks

## 8. Toegankelijkheid & Gebruiksgemak

### 8.1 Toegankelijkheidseisen

De applicatie voldoet aan WCAG 2.1 AA standaarden:

- **Kleurcontrast**: Minimaal 4.5:1 voor normale tekst, 3:1 voor grote tekst
- **Toetsenbordnavigatie**: Alle functies beschikbaar zonder muis
- **Screen Reader Compatibiliteit**: Aria-labels op alle interactieve elementen
- **Tekst Scaling**: UI blijft functioneel bij 200% zoom
- **No-motion Optie**: Animaties uitschakelbaar

### 8.2 Internationalisatie

- Initiële lancering in Nederlands en Engels
- UI tekstlabels in language files voor eenvoudige vertaling
- Datumformaten aangepast aan locale
- RTL ondersteuning voorbereid voor toekomstige talen

### 8.3 Onboarding & Tooltips

- **Eerste gebruik walkthrough**: Kort interactief overzicht van kernelementen
- **Contextuele tooltips**: Uitleg bij technische termen en scores
- **Inline help**: "i" iconen bij complexe concepten met korte uitleg
- **Kennisbank**: Uitgebreide artikelen over elke module en hoe te verbeteren

Dit document vormt de basis voor de ontwikkeling van GEO Scanner v1.0 MVP en kan worden gebruikt als referentie door het ontwikkelteam, ontwerpers en productmanagers.
