# GEO Scanner v1.0 - Technisch Ontwerp

Dit document beschrijft het technisch ontwerp voor de GEO Scanner applicatie, gebaseerd op de gekozen techstack. Het ontwerp focust op optimale performance, schaalbaarheid en onderhoudbaarheid voor de MVP.

## Inhoudsopgave

1. [Architectuur Overzicht](#1-architectuur-overzicht)
2. [Frontend Architectuur](#2-frontend-architectuur)
3. [API Layer](#3-api-layer)
4. [Scan Engine](#4-scan-engine)
5. [Data Management](#5-data-management)
6. [Performance Optimalisaties](#6-performance-optimalisaties)
7. [Deployment Strategie](#7-deployment-strategie)
8. [Uitbreidingsmogelijkheden](#8-uitbreidingsmogelijkheden)

## 1. Architectuur Overzicht

### 1.1 Systeemcomponenten

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Browser                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Vercel Edge Network (CDN)                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Next.js App (Static + SSR)                     │
│                                                                  │
│   ┌─────────────────┐      ┌────────────────┐      ┌─────────┐  │
│   │  React UI Layer │      │  Server        │      │ Utility │  │
│   │  (components)   │      │  Components    │      │ Files   │  │
│   └─────────────────┘      └────────────────┘      └─────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer (tRPC)                          │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────┐
│                     Vercel Serverless + Fluid Compute              │
│                                                                    │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────┐   │
│  │ URL Crawler  │   │ Analysis     │   │ Report               │   │
│  │ Controller   │   │ Engine       │   │ Generator            │   │
│  └──────────────┘   └──────────────┘   └──────────────────────┘   │
└───────────┬───────────────┬────────────────────┬─────────────────┘
            │               │                    │
            ▼               ▼                    ▼
┌────────────────┐  ┌───────────────┐  ┌─────────────────────┐
│ Vercel Postgres │  │ Upstash Redis │  │ Vercel Blob Storage │
└────────────────┘  └───────────────┘  └─────────────────────┘
```

### 1.2 Dataflow

1. Gebruiker voert URL in en start scan
2. Request gaat naar Vercel Edge Network
3. Next.js app ontvangt request en plaatst scan job in Upstash Redis queue
4. Bevestiging van start wordt teruggegeven aan client
5. Client pollt voor scan status via tRPC
6. Vercel Serverless Functions met Fluid Compute:
   - Halen scan job uit queue
   - Crawlen URL en verzamelen data
   - Voeren parallelle analyses uit
   - Slaan resultaten op in Vercel Postgres
   - Genereren rapport en slaan dit op in Blob Storage
7. Client toont real-time updates en uiteindelijke resultaten

## 2. Frontend Architectuur

### 2.1 Routes en Pagina's

```
app/
├── (auth)/
│   ├── login/
│   │   └── page.tsx          # Login pagina
│   └── register/
│       └── page.tsx          # Registratie pagina
├── dashboard/
│   ├── page.tsx              # Overzicht van scans
│   └── [scanId]/
│       └── page.tsx          # Detail pagina voor scan
├── api/
│   └── trpc/[trpc]/
│       └── route.ts          # tRPC API routes
├── layout.tsx                # Root layout met providers
└── page.tsx                  # Homepage met scan formulier
```

### 2.2 Componenten Architectuur

Wij kiezen voor een Atomic Design patroon met:

1. **Atoms**: Basis UI elementen (Button, Input, Card)
2. **Molecules**: Combinaties van atoms (ScanForm, ScoreCard)
3. **Organisms**: Zelfstandige secties (ScanResults, NavigationBar)
4. **Templates**: Pagina layouts
5. **Pages**: Concrete implementaties

```
components/
├── ui/                       # Basis UI componenten (shadcn/ui)
├── atoms/                    # Kleine herbruikbare componenten
├── molecules/                # Middelgrote componenten
│   ├── ScanForm.tsx
│   ├── ScoreCard.tsx
│   └── ...
├── organisms/                # Grotere secties
│   ├── ScanResults.tsx
│   ├── ModuleDetailPanel.tsx
│   └── ...
└── templates/                # Pagina templates
    ├── DashboardTemplate.tsx
    └── ScanDetailTemplate.tsx
```

### 2.3 State Management

1. **Server State**: TanStack Query voor data fetching en caching
2. **Form State**: React Hook Form + Zod
3. **URL State**: URL parameters voor deelbare resultaten
4. **UI State**: React useState en useReducer
5. **Global State**: Context API (minimaal gebruiken)

### 2.4 Performance Optimalisatie

Om de kritiek op Next.js performance te adresseren:

1. **Aggressieve Statische Generatie**: Zoveel mogelijk pagina's statisch genereren
2. **React Server Components**: Voor data-intensieve componenten
3. **Code Splitting**: Automatisch via Next.js
4. **Bundle Size Optimalisatie**: Regelmatige analyse met `@next/bundle-analyzer`
5. **Optimistische UI Updates**: Voor betere gebruikerservaring
6. **Edge Caching**: Vercel's Edge netwerk benutten

## 3. API Layer

### 3.1 tRPC API Schema

```typescript
// server/api/router.ts
export const appRouter = router({
  scan: scanRouter,
  user: userRouter,
  report: reportRouter,
  dashboard: dashboardRouter,
});

// server/api/routers/scan.ts
export const scanRouter = router({
  start: publicProcedure
    .input(z.object({ url: z.string().url() }))
    .mutation(async ({ input, ctx }) => {
      // Start scan logic
    }),
  getStatus: publicProcedure
    .input(z.object({ scanId: z.string() }))
    .query(async ({ input, ctx }) => {
      // Get scan status logic
    }),
  getResults: publicProcedure
    .input(z.object({ scanId: z.string() }))
    .query(async ({ input, ctx }) => {
      // Get scan results logic
    }),
});
```

### 3.2 Authentication Flow

1. Clerk.js voor authenticatie (JWT-based)
2. Auth middleware voor beschermde routes
3. API rate limiting op user niveau

### 3.3 API Rate Limiting en Caching

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1m'),
});

export async function middleware(request: Request) {
  const ip = request.headers.get('x-forwarded-for') || 'anonymous';
  const { success, limit, reset, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return NextResponse.json(
      { error: 'Too many requests' },
      { status: 429, headers: { 'Retry-After': reset.toString() } }
    );
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/api/:path*',
};
```

## 4. Scan Engine

### 4.1 Parallelle Architectuur

De scan engine maakt gebruik van parallelle verwerking om de 8 analysemodules onafhankelijk uit te voeren:

```typescript
// server/scan/engine.ts
export async function runScan(url: string, scanId: string) {
  try {
    // 1. Crawl de URL
    const html = await crawlUrl(url);

    // 2. Parse de basis informatie
    const baseInfo = extractBaseInfo(html, url);

    // 3. Start parallel analyses
    const moduleResults = await Promise.allSettled([
      analyzeModule1(html, url), // Crawl-toegang
      analyzeModule2(html, url), // Structured Data
      analyzeModule3(html, url), // Answer-ready content
      analyzeModule4(html, url), // Autoriteit & citaties
      analyzeModule5(html, url), // Versheid
      analyzeModule6(html, url), // Cross-web footprint
      analyzeModule7(html, url), // Multimodale leesbaarheid
      analyzeModule8(html, url), // Monitoring-haakjes
    ]);

    // 4. Combineer resultaten
    const results = combineResults(moduleResults, baseInfo);

    // 5. Genereer rapport
    const reportUrl = await generateReport(results, scanId);

    // 6. Update scan status
    await updateScanStatus(scanId, 'completed', results, reportUrl);

    return results;
  } catch (error) {
    await updateScanStatus(scanId, 'failed', null, null, error);
    throw error;
  }
}
```

### 4.2 Crawler Component

Het crawler component maakt gebruik van Cheerio voor lichtgewicht HTML parsing en Puppeteer (via Vercel Browserless) voor JavaScript-rendered content wanneer nodig:

```typescript
// server/scan/crawler.ts
export async function crawlUrl(url: string) {
  // 1. Fetch robots.txt en sitemap.xml
  const robotsTxt = await fetchRobotsTxt(url);
  const sitemap = await fetchSitemap(url);

  // 2. Controleer of bots toegang hebben
  if (!canBotAccess(robotsTxt, url)) {
    throw new Error('URL blocks bots');
  }

  // 3. Fetch initial HTML
  let html = await fetchHtml(url);

  // 4. Check of JavaScript rendering nodig is
  const needsJS = checkIfNeedsJavaScript(html);

  if (needsJS) {
    // Gebruik Puppeteer via Vercel Browserless
    html = await fetchWithPuppeteer(url);
  }

  return {
    html,
    robotsTxt,
    sitemap,
    renderedWithJS: needsJS,
  };
}
```

### 4.3 Analysemodules

Elke analysemodule is geïmplementeerd als een aparte functie met een consistente interface:

```typescript
// server/scan/modules/module1.ts (voorbeeld)
export async function analyzeModule1(html: string, url: string) {
  // 1. Parse robots.txt
  const robotsRules = parseRobotsRules(html);

  // 2. Check bot toegang
  const botAccess = checkBotAccess(robotsRules);

  // 3. Valideer sitemap
  const sitemapValid = validateSitemap(html);

  // 4. Check HTTP status
  const httpStatus = await checkHttpStatus(url);

  // 5. Bereken score (0-25)
  const score = calculateModule1Score(botAccess, sitemapValid, httpStatus);

  // 6. Genereer fix suggesties
  const fixes = generateModule1Fixes(botAccess, sitemapValid, httpStatus);

  return {
    name: 'Crawl-toegang',
    score,
    maxScore: 25,
    percentage: (score / 25) * 100,
    status: getStatusFromPercentage(score / 25),
    details: {
      botAccess,
      sitemapValid,
      httpStatus,
    },
    fixes,
  };
}
```

### 4.4 Queue Management

Gebruik van Upstash Redis voor job queueing:

```typescript
// server/queue/index.ts
import { Queue } from '@upstash/redis/v4';

export const scanQueue = new Queue({
  redis: {
    url: process.env.UPSTASH_REDIS_URL,
    token: process.env.UPSTASH_REDIS_TOKEN,
  },
  name: 'scan-queue',
});

// Enqueue a scan job
export async function enqueueScan(url: string, userId: string) {
  const scanId = generateScanId();

  await scanQueue.enqueue({
    url,
    scanId,
    userId,
    createdAt: new Date().toISOString(),
  });

  // Create initial scan record in database
  await createScanRecord(scanId, url, userId);

  return scanId;
}

// Process scan jobs
export async function processScanJob(job) {
  const { url, scanId, userId } = job;

  try {
    await updateScanStatus(scanId, 'processing');
    const results = await runScan(url, scanId);
    return results;
  } catch (error) {
    await updateScanStatus(scanId, 'failed', null, null, error);
    throw error;
  }
}
```

## 5. Data Management

### 5.1 Database Schema (Drizzle ORM)

```typescript
// db/schema.ts
import { pgTable, serial, text, timestamp, integer, json } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey(), // Clerk user ID
  email: text('email').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
  planId: text('plan_id').default('free'),
});

export const scans = pgTable('scans', {
  id: text('id').primaryKey(),
  url: text('url').notNull(),
  userId: text('user_id').references(() => users.id),
  status: text('status').notNull().default('queued'),
  createdAt: timestamp('created_at').defaultNow(),
  completedAt: timestamp('completed_at'),
  htmlSnapshot: text('html_snapshot').references(() => blobs.id),
  reportBlob: text('report_blob').references(() => blobs.id),
});

export const scanResults = pgTable('scan_results', {
  id: serial('id').primaryKey(),
  scanId: text('scan_id').references(() => scans.id),
  overallScore: integer('overall_score'),
  moduleScores: json('module_scores').$type<Record<string, number>>(),
  details: json('details').$type<ScanDetails>(),
  quickWins: json('quick_wins').$type<QuickWin[]>(),
});

export const blobs = pgTable('blobs', {
  id: text('id').primaryKey(),
  path: text('path').notNull(),
  size: integer('size').notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});
```

### 5.2 Caching Strategie

1. **Edge Caching**: Statische assets en pagina's
2. **Redis Caching**: API responses en scan resultaten
3. **Client Caching**: TanStack Query voor optimalistische UI updates

```typescript
// utils/cache.ts
import { Redis } from '@upstash/redis/v4';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_URL,
  token: process.env.UPSTASH_REDIS_TOKEN,
});

export async function cachedFetch<T>(
  key: string,
  fetchFn: () => Promise<T>,
  ttl: number = 3600 // 1 hour default
): Promise<T> {
  const cached = await redis.get<T>(key);

  if (cached) return cached;

  const fresh = await fetchFn();
  await redis.set(key, fresh, { ex: ttl });

  return fresh;
}
```

### 5.3 Storage Management

We gebruiken Vercel Blob Storage voor HTML snapshots en rapporten:

```typescript
// server/storage/blob.ts
import { put, del } from '@vercel/blob';

export async function storeHtmlSnapshot(scanId: string, html: string) {
  const blob = await put(`html-snapshots/${scanId}.html`, html, {
    contentType: 'text/html',
  });

  return blob.url;
}

export async function storePdfReport(scanId: string, pdfBuffer: Buffer) {
  const blob = await put(`reports/${scanId}.pdf`, pdfBuffer, {
    contentType: 'application/pdf',
  });

  return blob.url;
}
```

## 6. Performance Optimalisaties

### 6.1 Serverless Function Optimalisaties

Om de maximale efficiëntie uit Vercel Serverless Functions te halen:

1. **Cold Start Reductie**:
   - Minimale dependencies per functie
   - Gebruik van ES modules
   - Edge Runtime waar mogelijk

```typescript
// Voorbeeld van een Edge Runtime functie
export const config = {
  runtime: 'edge',
};

export default async function handler(req) {
  // Edge function code (minimale dependencies)
}
```

2. **Efficiënt Memory Management**:

```typescript
// server/utils/memory.ts
export function optimizeMemoryUsage(data) {
  // Alleen essentiële data bijhouden
  const { html, ...rest } = data;

  // HTML alleen in snapshot opslaan, niet in memory
  await storeHtmlSnapshot(data.scanId, html);

  return rest; // Ga verder met gereduceerde data
}
```

### 6.2 Next.js Specifieke Optimalisaties

1. **Dynamic vs. Static Rendering**:

```typescript
// app/dashboard/page.tsx
export const dynamic = 'force-dynamic'; // Voor realtime data

// app/scans/[id]/page.tsx
export const revalidate = 3600; // Vernieuwen op uurbasis

// app/blog/page.tsx
export const dynamic = 'force-static'; // Volledig statisch
```

2. **Image Optimalisatie**:

```tsx
import Image from 'next/image';

export function OptimizedImage({ src, alt }) {
  return (
    <Image
      src={src}
      alt={alt}
      width={600}
      height={400}
      placeholder="blur"
      blurDataURL="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFGQIZI+wP/gAAAABJRU5ErkJggg=="
      priority={false}
    />
  );
}
```

### 6.3 Progressieve Rendering

Voor snellere perceived performance:

```tsx
// components/ScanResult.tsx
'use client';

import { Suspense, lazy } from 'react';
import { useQuery } from '@tanstack/react-query';

// Basis resultaten meteen laden
const SimpleScore = () => {
  /* Lichtgewicht component */
};

// Zware componenten lazy loaden
const DetailedAnalysis = lazy(() => import('./DetailedAnalysis'));
const RadarChart = lazy(() => import('./RadarChart'));

export function ScanResult({ scanId }) {
  const { data, isLoading } = useQuery({
    queryKey: ['scan', scanId],
    queryFn: () => getScanResults(scanId),
  });

  if (isLoading) return <LoadingSkeleton />;

  return (
    <div>
      {/* Direct zichtbare content */}
      <SimpleScore score={data.overallScore} />

      {/* Progressief geladen content */}
      <Suspense fallback={<ChartSkeleton />}>
        <RadarChart data={data.moduleScores} />
      </Suspense>

      <Suspense fallback={<DetailsSkeleton />}>
        <DetailedAnalysis data={data.details} />
      </Suspense>
    </div>
  );
}
```

## 7. Deployment Strategie

### 7.1 Vercel Project Configuration

```json
// vercel.json
{
  "framework": "nextjs",
  "regions": ["arn1"], // Amsterdam region voor GDPR compliance
  "functions": {
    "api/analyze-*.js": {
      "memory": 1024,
      "maxDuration": 60
    },
    "api/crawler.js": {
      "memory": 1024,
      "maxDuration": 60
    },
    "api/trpc/*.js": {
      "memory": 256,
      "maxDuration": 10
    }
  },
  "crons": [
    {
      "path": "/api/cron/clean-old-snapshots",
      "schedule": "0 0 * * *"
    }
  ]
}
```

### 7.2 CI/CD Pipeline

GitHub Actions workflow voor deployment:

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Typecheck
        run: npm run typecheck

      - name: Lint
        run: npm run lint

      - name: Test
        run: npm test

      - name: Deploy to Vercel
        if: github.event_name == 'push'
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## 8. Uitbreidingsmogelijkheden

De architectuur is ontworpen met toekomstige uitbreiding in gedachten:

1. **Plugin Systeem**: Extensies voor CMS-integraties
   - Connector interfaces voor WordPress, Webflow etc.
2. **Multi-tenant Support**: Voor agencies
   - Eigen whitelabel rapporten
   - Team management
3. **Monitoring Service**: Voor continue scans
   - Webhook notificaties
   - Scheduled scans
4. **API voor Externe Integraties**:
   - Publieke API voor third-party tools
   - Webhooks voor automation platforms

Dit technisch ontwerp biedt een solide basis voor het MVP terwijl het alle benodigde optimalisaties bevat om Next.js performant te maken voor de GEO Scanner use-case.
