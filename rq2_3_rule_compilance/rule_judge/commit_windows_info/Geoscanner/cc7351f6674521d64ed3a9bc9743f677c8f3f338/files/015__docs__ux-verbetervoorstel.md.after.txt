# UX Verbetervoorstel: Gebruiksvriendelijke Terminologie

## 🎯 Doel

Het vereenvoudigen van technische termen en concepten om de GEO Scanner toegankelijker te maken voor niet-technische gebruikers.

## 📊 Huidige Situatie

De huidige interface gebruikt veel technische termen die voor niet-technische gebruikers moeilijk te begrijpen zijn:

- "Crawl Access"
- "Structured Data"
- "JSON-LD"
- "Technical SEO"
- "Content Analysis"

## 💡 Voorgestelde Verbeteringen

### 1. Module Namen Vereenvoudigen

| Technische Term  | Gebruiksvriendelijke Term | Uitleg                                                     |
| ---------------- | ------------------------- | ---------------------------------------------------------- |
| Crawl Access     | Zichtbaarheid voor AI     | Hoe goed AI-systemen je website kunnen vinden en begrijpen |
| Structured Data  | Content Structuur         | Hoe duidelijk je content is opgebouwd voor AI              |
| Content Analysis | Content Kwaliteit         | Hoe goed je content is voor AI-begrip                      |
| Technical SEO    | Website Basis             | Hoe goed je website technisch is ingericht                 |

### 2. Score Terminologie

| Technische Term | Gebruiksvriendelijke Term |
| --------------- | ------------------------- |
| Score           | Prestatie                 |
| Impact Level    | Belang                    |
| High Impact     | Zeer Belangrijk           |
| Medium Impact   | Belangrijk                |
| Low Impact      | Minder Belangrijk         |

### 3. Status Indicators

| Technische Term | Gebruiksvriendelijke Term | Icon |
| --------------- | ------------------------- | ---- |
| Success         | Goed                      | ✅   |
| Warning         | Let Op                    | ⚠️   |
| Error           | Aandacht Nodig            | ❌   |

### 4. Actie Terminologie

| Technische Term | Gebruiksvriendelijke Term |
| --------------- | ------------------------- |
| Quick Wins      | Snelle Verbeteringen      |
| Fix             | Oplossing                 |
| Implementation  | Toepassing                |
| Optimization    | Verbetering               |

## 🎨 Implementatie Voorstel

### 1. Component Aanpassingen

```typescript
// Voorbeeld van nieuwe interface definities
interface ModuleCardProps {
  module: {
    id: string;
    name: string; // Gebruiksvriendelijke naam
    description: string; // Duidelijke uitleg
    score: number;
    status: 'goed' | 'let-op' | 'aandacht-nodig';
  };
}

// Voorbeeld van nieuwe constanten
const moduleNames = {
  'crawl-access': {
    displayName: 'Zichtbaarheid voor AI',
    description: 'Hoe goed AI-systemen je website kunnen vinden en begrijpen',
  },
  'structured-data': {
    displayName: 'Content Structuur',
    description: 'Hoe duidelijk je content is opgebouwd voor AI',
  },
  // ... andere modules
};
```

### 2. Help Teksten

Voor elke module en term wordt een korte, duidelijke uitleg toegevoegd:

```typescript
const helpTexts = {
  'zichtbaarheid-voor-ai': {
    title: 'Wat betekent dit?',
    description:
      'Dit laat zien hoe goed AI-systemen je website kunnen vinden en begrijpen. Hoe hoger de score, hoe beter AI je content kan gebruiken.',
    example:
      'Net zoals een goede etalage je winkel vindbaar maakt, maakt een goede website structuur je content vindbaar voor AI.',
  },
  // ... andere modules
};
```

### 3. Tooltips

Korte, duidelijke tooltips bij technische termen:

```typescript
const tooltips = {
  'content-structuur': 'De manier waarop je content is opgebouwd, zodat AI het beter kan begrijpen',
  'website-basis': 'De technische fundamenten van je website die belangrijk zijn voor AI',
};
```

## 📱 Responsive Tekst

- Desktop: Volledige uitleg en voorbeelden
- Tablet: Korte uitleg met iconen
- Mobile: Korte, kernachtige uitleg

## 🎯 Success Criteria

1. **Begrijpelijkheid**

   - 90% van de gebruikers begrijpt de terminologie
   - Minder dan 5% zoekt naar uitleg
   - Positieve feedback op duidelijkheid

2. **Gebruiksvriendelijkheid**

   - Snellere navigatie door duidelijke labels
   - Minder vragen over betekenis
   - Hogere tevredenheidsscore

3. **Effectiviteit**
   - Hogere conversie naar actie
   - Minder support vragen
   - Betere gebruikerservaring

## 📅 Implementatie Plan

### Fase 1: Basis Terminologie (Week 1)

- [ ] Implementeer nieuwe module namen
- [ ] Voeg basis help teksten toe
- [ ] Update status indicators

### Fase 2: Uitgebreide Uitleg (Week 2)

- [ ] Implementeer tooltips
- [ ] Voeg voorbeelden toe
- [ ] Update actie terminologie

### Fase 3: Optimalisatie (Week 3)

- [ ] Test met gebruikers
- [ ] Verfijn teksten
- [ ] Implementeer feedback

## 🔄 Evaluatie

Na implementatie wordt de nieuwe terminologie geëvalueerd op:

1. Gebruikersbegrip
2. Navigatie-efficiëntie
3. Tevredenheid
4. Support vragen

## 📝 Notities

- Houd teksten kort en bondig
- Gebruik actieve taal
- Vermijd jargon
- Focus op praktische betekenis
- Gebruik herkenbare metaforen
