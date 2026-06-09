# GEO Scanner v1.0 - Design System & Visuele Identiteit

Dit document beschrijft de visuele taal en gebruikerservaring van GEO Scanner - een moderne, professionele en data-gedreven web applicatie voor het analyseren van webpagina's op AI-zichtbaarheid.

## Inhoudsopgave

1. [Design Concept & Filosofie](#1-design-concept--filosofie)
2. [Kleurensysteem](#2-kleurensysteem)
3. [Typografie](#3-typografie)
4. [Component Systeem](#4-component-systeem)
5. [Iconografie & Illustraties](#5-iconografie--illustraties)
6. [Datavisualisatie](#6-datavisualisatie)
7. [Motion Design](#7-motion-design)
8. [Voice & Tone](#8-voice--tone)
9. [Responsive Principes](#9-responsive-principes)
10. [Design Deliverables](#10-design-deliverables)

## 1. Design Concept & Filosofie

### 1.1 Kernprincipes

GEO Scanner combineert **data-precisie** met **visuele helderheid** in een interface die complexe technische informatie vertaalt naar actionable inzichten. Het design is gebaseerd op vier kernprincipes:

1. **Precisie met Eenvoud** - Complexe data helder en begrijpelijk presenteren
2. **Hiërarchische Duidelijkheid** - Prioritering van informatie op basis van impact
3. **Actionable Focus** - Elke weergave leidt tot een concrete volgende stap
4. **Technische Betrouwbaarheid** - Een visuele taal die expertise en vertrouwen uitstraalt

### 1.2 Visuele Metafoor

De interface is geïnspireerd door het concept van een **"modern dashboard"** en **"digitale radar"** - elementen die naadloos aansluiten bij de scanfunctie van de app. De radar chart als centraal element visualiseert hoe goed een website 'op de radar' van AI-systemen staat.

### 1.3 Moodboard Elementen

![GEO Scanner Moodboard](https://example.com/geo-scanner-moodboard.jpg)

Het moodboard combineert:

- Technische precisie (gridlines, datavisualisaties)
- Moderne AI-esthetiek (subtiele gradiënten, glow-effecten)
- Professionele dashboards (white space, duidelijke informatie hiërarchie)
- Analytische tools (charts, metrics, KPI's)

## 2. Kleurensysteem

### 2.1 Primaire Kleuren

Het kleurenpalet is gebaseerd op een moderne, tech-gerichte benadering met een primaire accent kleur die vertrouwen en technologie uitstraalt:

| Kleur           | Hex       | RGB             | Gebruik                               |
| --------------- | --------- | --------------- | ------------------------------------- |
| **Deep Blue**   | `#0F45C5` | `15, 69, 197`   | Primaire accent kleur, CTA's          |
| **Midnight**    | `#171A31` | `23, 26, 49`    | Headers, footer, donkere UI elementen |
| **Slate White** | `#F7F9FC` | `247, 249, 252` | Achtergrond, lichte UI elementen      |

### 2.2 Status Kleuren

De status kleuren zijn cruciaal in de applicatie en communiceren duidelijk de staat van verschillende elementen:

| Kleur             | Hex       | RGB            | Gebruik                       |
| ----------------- | --------- | -------------- | ----------------------------- |
| **Success Green** | `#14B870` | `20, 184, 112` | Goede scores (80-100%)        |
| **Warning Amber** | `#FF9F0A` | `255, 159, 10` | Middelmatige scores (40-79%)  |
| **Danger Red**    | `#FF3B5C` | `255, 59, 92`  | Slechte scores (<40%), fouten |
| **Info Teal**     | `#0ACDDA` | `10, 205, 218` | Informatieve elementen, tips  |

### 2.3 Neutrale Kleuren

| Kleur      | Hex       | RGB             | Gebruik                             |
| ---------- | --------- | --------------- | ----------------------------------- |
| **Carbon** | `#232429` | `35, 36, 41`    | Primaire tekst                      |
| **Steel**  | `#616A7D` | `97, 106, 125`  | Secundaire tekst, labels            |
| **Mist**   | `#A0A9B8` | `160, 169, 184` | Tertiaire tekst, placeholders       |
| **Cloud**  | `#E3E6EC` | `227, 230, 236` | Borders, dividers                   |
| **Snow**   | `#FFFFFF` | `255, 255, 255` | Kaarten, modals, contrast elementen |

### 2.4 Gradiënten

Subtiele gradiënten worden gebruikt voor accentelementen om een moderne, tech-forward look te creëren:

| Gradiënt         | CSS                                                 | Gebruik                              |
| ---------------- | --------------------------------------------------- | ------------------------------------ |
| **Primary Flow** | `linear-gradient(135deg, #0F45C5 0%, #44A5FF 100%)` | Call-to-actions, belangrijke knoppen |
| **Success Flow** | `linear-gradient(135deg, #14B870 0%, #6EE7A0 100%)` | Success states, hoge scores          |
| **Data Flow**    | `linear-gradient(135deg, #171A31 0%, #2C3154 100%)` | Gegevenskaarten, dashboard-elementen |

## 3. Typografie

### 3.1 Font Families

GEO Scanner gebruikt een combinatie van twee moderne, professionele en zeer leesbare fonts:

| Font                | Type       | Gebruik                             |
| ------------------- | ---------- | ----------------------------------- |
| **Inter**           | Sans-serif | UI elementen, body tekst, labels    |
| **Instrument Sans** | Sans-serif | Headers, grote cijfers, accenttekst |

**Implementatie:**

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Sans:wght@400;500;600;700&display=swap');

:root {
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-display: 'Instrument Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

### 3.2 Typografische Schaal

Een gestructureerde typografische schaal zorgt voor consistentie en harmonie:

| Element       | Font            | Weight | Size | Line Height | Gebruik                    |
| ------------- | --------------- | ------ | ---- | ----------- | -------------------------- |
| **Display 1** | Instrument Sans | 700    | 48px | 56px        | Grote headers, hero sectie |
| **Display 2** | Instrument Sans | 700    | 40px | 48px        | Sectie headers             |
| **Heading 1** | Instrument Sans | 600    | 32px | 40px        | Pagina titels              |
| **Heading 2** | Instrument Sans | 600    | 24px | 32px        | Sectie titels              |
| **Heading 3** | Instrument Sans | 600    | 20px | 28px        | Card titels, subsecties    |
| **Subtitle**  | Inter           | 600    | 18px | 26px        | Benadrukte tekst, labels   |
| **Body 1**    | Inter           | 400    | 16px | 24px        | Primaire body tekst        |
| **Body 2**    | Inter           | 400    | 14px | 22px        | Secundaire body tekst      |
| **Caption**   | Inter           | 500    | 12px | 18px        | Labels, timestamps         |
| **Code**      | Fira Code       | 400    | 14px | 20px        | Code snippets, JSON        |

### 3.3 Speciale Typografische Elementen

| Element               | Beschrijving                                                                   |
| --------------------- | ------------------------------------------------------------------------------ |
| **Score Numbers**     | Grote, vetgedrukte Instrument Sans cijfers voor scores met optische uitlijning |
| **Percentage Labels** | Compacte, geproportioneerde cijfers met superscript % teken                    |
| **Code Blocks**       | Syntax-highlighted code in monospace font met subtiele achtergrond             |
| **Navigation Items**  | Semi-bold Inter met subtiele underline effecten bij hover                      |

## 4. Component Systeem

### 4.1 Atomaire Design Hiërarchie

GEO Scanner volgt een atomaire designstructuur met een duidelijke hiërarchie van componenten:

```
Foundation → Atoms → Molecules → Organisms → Templates → Pages
```

### 4.2 Kern UI Componenten

#### Buttons

| Variant         | Gebruik                                          | Visuele Stijl                                          |
| --------------- | ------------------------------------------------ | ------------------------------------------------------ |
| **Primary**     | Belangrijkste acties (Scan starten, Downloaden)  | Gradient achtergrond, witte tekst, subtiele hover glow |
| **Secondary**   | Ondersteunende acties (Opnieuw scannen, Opslaan) | Outline, kleurovergang op hover, geen achtergrond      |
| **Tertiary**    | Minst belangrijke acties (Annuleren, Sluiten)    | Tekst alleen, subtiele hover underline                 |
| **Icon Button** | Compacte acties in UI (Delen, Info)              | Circulaire container met centraal icoon                |

#### Cards & Containers

| Component          | Gebruik                               | Visuele Stijl                                                  |
| ------------------ | ------------------------------------- | -------------------------------------------------------------- |
| **Data Card**      | Container voor module data            | Witte achtergrond, subtiele schaduw, 16px radius, 24px padding |
| **Stats Card**     | Individuele metriek weergave          | Compacte container, grote cijfers, ondersteunende label        |
| **Module Panel**   | Uitklapbaar paneel voor moduledetails | Accordeonstijl met vloeiende animatie, icoon transitie         |
| **Quick Win Item** | Individuele verbeteringstip           | Left border accent color, rank indicator, code collapse        |

#### Formulier Elementen

| Component        | Gebruik                          | Visuele Stijl                                           |
| ---------------- | -------------------------------- | ------------------------------------------------------- |
| **Text Input**   | URL invoer, zoeken               | Ruime padding, duidelijke focus state, inline validatie |
| **Toggle**       | Binaire opties (volledig domein) | Moderne pill shape toggle met duidelijke states         |
| **Dropdown**     | Selectie uit meerdere opties     | Minimalistisch met vloeiende dropdown animatie          |
| **Range Slider** | Configuratie opties              | Custom thumb, progress fill, tooltip met waarde         |

#### Navigatie & Layout

| Component          | Gebruik                 | Visuele Stijl                                    |
| ------------------ | ----------------------- | ------------------------------------------------ |
| **App Header**     | Primaire navigatie      | Sticky, glass-morfisme effect met blur           |
| **Tab Navigation** | Sectie navigatie        | Underline style, animated transitions            |
| **Breadcrumbs**    | Hiërarchische navigatie | Compacte chevron separators, truncatie op mobiel |
| **Sidebar**        | Contextuele navigatie   | Collapsible, subtle dividers, icon+text items    |

### 4.3 Unieke Custom Componenten

| Component             | Beschrijving                                    | Functie                                         |
| --------------------- | ----------------------------------------------- | ----------------------------------------------- |
| **Radar Score Chart** | 8-assige radar chart met animatie               | Centrale visualisatie van alle module scores    |
| **Score Circle**      | Circulaire progress indicator                   | Toont overall score met kleurcodering           |
| **Code Fix Card**     | Uitklapbare code editor met syntax highlighting | Toont implementeerbare code fixes               |
| **Scan Timeline**     | Horizontale flow indicator                      | Visualiseert het scan proces met states         |
| **Module Badge**      | Pill-vormige status indicator                   | Toont module status met kleurcode en percentage |

### 4.4 Component States

Elk component heeft consistent gedefinieerde states:

| State              | Visuele Behandeling                                        |
| ------------------ | ---------------------------------------------------------- |
| **Default**        | Basisweergave van het component                            |
| **Hover**          | Subtiele verhoging in helderheid/contrast, mogelijk schaal |
| **Active/Pressed** | Lichte schaalverkleining, hogere verzadiging               |
| **Focused**        | Prominente outine ring in primaire kleur                   |
| **Disabled**       | Verlaagde opacity, gray-out effect                         |
| **Loading**        | Pulse animatie of skeleton loading state                   |
| **Error**          | Rode accentkleur, informatief foutpictogram                |
| **Success**        | Groene accentkleur, check icoon                            |

## 5. Iconografie & Illustraties

### 5.1 Icoon Systeem

GEO Scanner gebruikt een consistent, modern icon system:

| Icoon Set                                        | Beschrijving                                     | Gebruik              |
| ------------------------------------------------ | ------------------------------------------------ | -------------------- |
| **[Phosphor Icons](https://phosphoricons.com/)** | Flexibele, moderne iconset met consistente stijl | Primaire UI iconen   |
| **Custom Module Icons**                          | Speciaal ontwikkelde iconen voor elke module     | Module identificatie |
| **Status Indicators**                            | Minimale succes/warning/error iconen             | Statusindicatie      |

Iconen volgen deze richtlijnen:

- 24px grid voor UI elementen
- 32px grid voor feature/module iconen
- 2px stroke weight voor outlined stijl
- Rounded caps en joins
- Consistente hoeken (4px radius)

### 5.2 Illustratie Stijl

| Illustratie Type      | Stijl                                                         | Gebruik                     |
| --------------------- | ------------------------------------------------------------- | --------------------------- |
| **Module Education**  | Semi-abstracte, technische illustraties met blue-accent color | Module uitleg pagina's      |
| **Empty States**      | Vriendelijke, lichte illustraties met subtiele gradients      | Lege dashboards, onboarding |
| **Success Scenarios** | Geanimeerde confetti/celebration graphics                     | Hoge scores, verbeteringen  |

### 5.3 Grafieken & Data Visualisatie

| Type                 | Stijl                                                 | Gebruik                      |
| -------------------- | ----------------------------------------------------- | ---------------------------- |
| **Radar Charts**     | Multi-axis plots met semitransparant fill, grid lines | Module scores visualiseren   |
| **Progress Circles** | Clean circular progress met percentage in center      | Overall scores               |
| **Bar Charts**       | Horizontal bars met custom rounded caps               | Vergelijking tussen modules  |
| **Line Graphs**      | Smooth curves met gradient underneath                 | Tijdreeks data (verbetering) |

## 6. Datavisualisatie

### 6.1 Data Display Principes

De visualisatie van gegevens in GEO Scanner volgt deze ontwerpprincipes:

1. **Clarity Over Decoration** - Functionaliteit gaat voor op decoratie
2. **Context With Data** - Getallen altijd voorzien van context (max waarde, benchmark)
3. **Consistent Color Meaning** - Kleuren hebben consistente betekenis (groen = goed)
4. **Progressive Disclosure** - Van overview naar detail
5. **Comparative View** - Mogelijkheid tot vergelijking waar zinvol

### 6.2 Score Visualisatie Systeem

| Score Type             | Visualisatie                        | Details                                 |
| ---------------------- | ----------------------------------- | --------------------------------------- |
| **Overall Score**      | Grote circulaire progress indicator | 0-100 schaal, kleurgradiënt, percentage |
| **Module Scores**      | Radar chart, 8 assen                | Per module score gevisualiseerd         |
| **Individual Metrics** | Horizontal bar charts               | Specifieke metrieken binnen modules     |
| **Binary Checks**      | Checkbox/X indicators               | Pass/fail items                         |

### 6.3 Dataformattering Richtlijnen

| Data Type       | Formatting                       | Voorbeeld                |
| --------------- | -------------------------------- | ------------------------ |
| **Percentages** | 1 decimaal, % teken              | 92.5%                    |
| **Scores**      | Gehele getallen, /[max]          | 23/25                    |
| **Datums**      | Leesbaar formaat                 | 15 mei 2025              |
| **Durations**   | Menselijk leesbaar               | 3 min geleden            |
| **URLs**        | Truncated met ellipsis in midden | example.com/...page.html |

## 7. Motion Design

### 7.1 Animatie Principes

Animaties binnen GEO Scanner volgen deze principes:

1. **Purposeful** - Ondersteunt gebruikersinteractie en begrip
2. **Swift but Visible** - Snel genoeg voor efficiëntie, langzaam genoeg voor begrip
3. **Consistent Physics** - Natuurlijke versnelling/vertraging
4. **Hierarchical** - Belangrijkere elementen krijgen meer uitgesproken animatie

### 7.2 Timing & Easing

| Snelheid       | Duur  | Easing                    | Gebruik                           |
| -------------- | ----- | ------------------------- | --------------------------------- |
| **Ultra Fast** | 100ms | ease-out                  | Micro-feedback (button clicks)    |
| **Fast**       | 200ms | ease-in-out               | UI state changes, toggles         |
| **Standard**   | 300ms | cubic-bezier(.19,1,.22,1) | Component transitions, accordions |
| **Expressive** | 500ms | cubic-bezier(.16,1,.3,1)  | Page transitions, celebrations    |

### 7.3 Micro-Interactions

| Element             | Animatie                                | Doel                              |
| ------------------- | --------------------------------------- | --------------------------------- |
| **Buttons**         | Subtle scale + shadow increase on hover | Feedback op interactiviteit       |
| **Score Numbers**   | Count-up animation                      | Engagement, focus op resultaat    |
| **Tabs**            | Smooth underline transition             | Visuele continuïteit              |
| **Charts**          | Sequential reveal of elements           | Storytelling met data             |
| **Quick Win Items** | Subtle bounce on reveal                 | Aandacht vestigen op prioriteiten |

### 7.4 Skeleton Loaders

Tijdens het laden van content worden speciaal ontworpen skeleton states getoond:

| Component         | Skeleton Style                                 |
| ----------------- | ---------------------------------------------- |
| **Score Cards**   | Pulsing circular placeholder for numbers       |
| **Radar Chart**   | Empty chart frame with gradient pulse          |
| **Module Panels** | Header placeholder + content lines             |
| **Code Blocks**   | Structured code-like lines with varying widths |

## 8. Voice & Tone

### 8.1 UX Writing Principes

Alle tekst in de interface volgt deze principes:

1. **Clear Over Clever** - Duidelijkheid boven creatief taalgebruik
2. **Action-Oriented** - Focus op wat gebruikers kunnen/moeten doen
3. **Concise But Complete** - Kort zonder belangrijke details te missen
4. **Technical Yet Accessible** - Vakjargon vermijden of uitleggen

### 8.2 Tone Per Context

| Context          | Tone                           | Voorbeeld                                                                            |
| ---------------- | ------------------------------ | ------------------------------------------------------------------------------------ |
| **Homepage**     | Professioneel, zelfverzekerd   | "Scan je pagina en zie binnen 10 seconden hoe LLM-proof jouw content is."            |
| **Scan Process** | Informatief, technisch         | "Analyzing JSON-LD structure and validating entity markup..."                        |
| **Results**      | Constructief, solution-focused | "Jouw pagina scoort goed op structuur maar mist key authority signalen."             |
| **Errors**       | Helder, behulpzaam             | "We kunnen deze URL niet bereiken. Controleer of de pagina publiek toegankelijk is." |
| **Success**      | Motiverend, celebratief        | "Uitstekend! Jouw pagina is optimaal voorbereid voor AI visibility."                 |

### 8.3 UI Text Richtlijnen

| Element            | Stijl                         | Voorbeeld                                                                        |
| ------------------ | ----------------------------- | -------------------------------------------------------------------------------- |
| **CTA Buttons**    | Actiewerkwoord + resultaat    | "Scan Starten" vs "Start"                                                        |
| **Labels**         | Kort, zelfstandig naamwoord   | "URL" vs "Voer URL in"                                                           |
| **Tooltips**       | Beknopte uitleg, max 2 zinnen | "JSON-LD geeft structuur aan je content zodat AI de betekenis begrijpt."         |
| **Error Messages** | Probleem + oplossing          | "Ongeldige URL. Voer een volledig webadres in beginnend met http:// of https://" |
| **Empty States**   | Vriendelijk, directief        | "Geen eerdere scans gevonden. Start je eerste scan om inzicht te krijgen."       |

## 9. Responsive Principes

### 9.1 Breakpoint Systeem

| Breakpoint  | Range           | Target Devices                              |
| ----------- | --------------- | ------------------------------------------- |
| **Mobile**  | 320px - 639px   | Smartphones (portrait)                      |
| **Tablet**  | 640px - 1023px  | Tablets (portrait), Smartphones (landscape) |
| **Desktop** | 1024px - 1439px | Tablets (landscape), Laptops                |
| **Wide**    | 1440px+         | Desktops, Large displays                    |

### 9.2 Layout Transformaties

| Component        | Mobile Adaptation                   | Tablet Adaptation                 |
| ---------------- | ----------------------------------- | --------------------------------- |
| **Dashboard**    | Verticale stack, simplified widgets | 2-column grid, compact widgets    |
| **Radar Chart**  | Smaller, fixed height               | Interactive, scalable             |
| **Navigation**   | Bottom tab bar                      | Side navigation                   |
| **Results Page** | Module tabs, swipe between          | All visible, accordion collapse   |
| **Data Tables**  | Collapse to cards, essential data   | Horizontally scrollable, all data |

### 9.3 Touch Optimalisaties

| Element                  | Touch Optimization                               |
| ------------------------ | ------------------------------------------------ |
| **Interactive Elements** | Minimum 44px x 44px touch target                 |
| **Scrolling Containers** | Support for momentum scrolling, kinetic behavior |
| **Hover States**         | Alternative touch states for hover effects       |
| **Charts**               | Enhanced tooltip areas for finger interaction    |
| **Code Blocks**          | Tap-to-copy vs hover-to-copy                     |

## 10. Design Deliverables

### 10.1 Design Systeem Assets

| Deliverable           | Format        | Purpose                     |
| --------------------- | ------------- | --------------------------- |
| **Design Tokens**     | JSON          | Code-ready design variables |
| **Component Library** | Figma Library | UI component documentatie   |
| **Icon Set**          | SVG sprites   | Optimized icon delivery     |
| **Animations**        | Lottie files  | Complex animations          |

### 10.2 Key Screens

De volgende schermen worden volledig uitgewerkt in het design systeem:

1. **Homepage / Scan Entry**
2. **Scan Progress / Loading**
3. **Results Dashboard**
4. **Module Detail View**
5. **PDF Report Layout**
6. **User Dashboard**
7. **Settings & Administration**
8. **Login / Registration**

### 10.3 Design-to-Development Handoff

Design assets worden beschikbaar gemaakt via:

1. **Zeplin/Figma Inspect** - Voor component specs en CSS details
2. **Storybook** - Voor interactieve component documentatie
3. **Motion Specs** - Voor animatie timing en interactie details

---

## UI Showcase

### Dashboard Concept

![GEO Scanner Dashboard](https://example.com/dashboard-concept.png)

_De dashboard interface toont de core elementen van het design systeem: de score cirkel, radar chart, module cards en quick win items in een overzichtelijke, data-gerichte layout._

### Mobile Experience

![GEO Scanner Mobile](https://example.com/mobile-concept.png)

_De mobiele ervaring behoudt de kernfunctionaliteit in een geoptimaliseerde interface met focus op de meest kritische data points._

### Component System Overview

![GEO Scanner Components](https://example.com/components-overview.png)

_Een overzicht van de kern UI componenten die de basis vormen van de interface, getoond in verschillende states en configuraties._

---

Dit design systeem vormt de visuele basis voor GEO Scanner v1.0, waarin technische nauwkeurigheid wordt gecombineerd met moderne, gebruiksvriendelijke interface elementen voor een unieke en effectieve gebruikerservaring.
