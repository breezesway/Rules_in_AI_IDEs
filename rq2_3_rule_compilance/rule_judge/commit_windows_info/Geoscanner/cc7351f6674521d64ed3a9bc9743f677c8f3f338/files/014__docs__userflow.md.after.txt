# GeoScanner Userflow

## Hoofdflow

```mermaid
graph TD
    A[Start] --> B[URL Invoer]
    B --> C[Scan Starten]
    C --> D[Resultaten Pagina]
    D --> E{Accordion Secties}

    E --> F[Crawl-toegang]
    E --> G[Structured Data]
    E --> H[Robots.txt]
    E --> I[Sitemap.xml]
    E --> J[HTML Snapshot]
    E --> K[Content Analyse]
    E --> L[Technical SEO]

    F --> M[Verbeterpunten]
    G --> M
    H --> M
    I --> M
    J --> M
    K --> M
    L --> M

    M --> N[Nieuwe Scan]
    N --> B
```

## Detail Flow per Sectie

```mermaid
graph TD
    subgraph "Crawl-toegang"
        F1[Robots.txt Check] --> F2[Sitemap Validatie]
        F2 --> F3[Meta Robots Analyse]
        F3 --> F4[HTTP Status Check]
    end

    subgraph "Structured Data"
        G1[JSON-LD Validatie] --> G2[Open Graph Check]
        G2 --> G3[Schema Types Analyse]
    end

    subgraph "Content Analyse"
        K1[Taal Detectie] --> K2[Keyword Analyse]
        K2 --> K3[Duplicate Content Check]
    end

    subgraph "Technical SEO"
        L1[Performance Metrics] --> L2[Mobile Friendly Check]
        L2 --> L3[Security Analyse]
    end
```

## Status Flow

```mermaid
graph LR
    A[Score < 50] -->|Danger| B[Rood]
    C[Score 50-80] -->|Warning| D[Amber]
    E[Score > 80] -->|Success| F[Groen]
```

## Interactie Flow

```mermaid
graph TD
    A[Accordion Item] -->|Klik| B[Expand/Collapse]
    B --> C[Toon Details]
    C --> D[Scroll Content]
    D --> E[Lees Verbeterpunten]
    E --> F[Implementeer Fixes]
    F --> G[Nieuwe Scan]
```

## Visuele Elementen

- **Status Indicators**

  - Success: Groen badge
  - Warning: Amber badge
  - Danger: Rood badge

- **Layout**

  - Responsive grid system
  - Scrollbare content areas
  - Collapsible sections

- **Interactie**
  - Accordion navigatie
  - Badge status indicators
  - Action buttons
  - Scrollable areas
