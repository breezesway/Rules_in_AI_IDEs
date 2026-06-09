import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Lijst van statische paden die gecached kunnen worden
const STATIC_PATHS = ['/hoe-werkt-het', '/faq', '/over-ons', '/prijzen', '/blog'];

// Paden die nooit gecached mogen worden
const DYNAMIC_PATHS = ['/api/', '/dashboard/'];

// Paden die altijd publiek toegankelijk zijn (geen login nodig)
const PUBLIC_PATHS = ['/login', '/register', '/_next', '/favicon.ico', '/robots.txt', '/api/trpc'];

// Caching TTL per route type (in seconden)
const CACHE_TIMES = {
  static: 60 * 60 * 24, // 24 uur voor statische pagina's
  api: 60 * 5, // 5 minuten voor API calls (behalve scan API)
  default: 60 * 60, // 1 uur voor overige routes
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const response = NextResponse.next();

  // Authenticatie check
  const session = request.cookies.get('session');
  const isPublicPath = PUBLIC_PATHS.some(path => pathname.startsWith(path));

  // Redirect naar login als er geen sessie is en het pad niet publiek is
  if (!session && !isPublicPath) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Als we hier zijn, gaat de gebruiker door naar de gewenste pagina
  // Nu passen we caching toe gebaseerd op de route

  // Voorkom caching voor alle API scan endpoints en dashboard routes
  if (DYNAMIC_PATHS.some(path => pathname.startsWith(path))) {
    response.headers.set('Cache-Control', 'no-store, max-age=0');
    return response;
  }

  // Speciale behandeling voor specifieke API routes die wel gecached mogen worden
  if (pathname.startsWith('/api/') && !pathname.includes('/scan')) {
    response.headers.set(
      'Cache-Control',
      `public, s-maxage=${CACHE_TIMES.api}, stale-while-revalidate`
    );
    return response;
  }

  // Langere cache voor statische pagina's
  if (STATIC_PATHS.includes(pathname) || pathname === '/') {
    response.headers.set(
      'Cache-Control',
      `public, s-maxage=${CACHE_TIMES.static}, stale-while-revalidate=${CACHE_TIMES.static * 2}`
    );
    return response;
  }

  // Standaard caching voor overige routes
  response.headers.set(
    'Cache-Control',
    `public, s-maxage=${CACHE_TIMES.default}, stale-while-revalidate`
  );

  return response;
}

export const config = {
  matcher: [
    /*
     * Match alle paden behalve:
     * 1. /_next/static (Next.js statische bestanden)
     * 2. /_vercel/ (Vercel interne routes)
     * 3. /favicon.ico, /robots.txt, etc.
     */
    '/((?!_next/static|_vercel/static|favicon.ico|robots.txt).*)',
  ],
};
