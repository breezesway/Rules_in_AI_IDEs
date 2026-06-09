'use client';

import { Inter, Instrument_Sans } from 'next/font/google';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { Toaster } from '@/components/ui/toaster';
import { AuthProvider } from '@/lib/auth-context';
import { useEffect } from 'react';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

const instrumentSans = Instrument_Sans({
  subsets: ['latin'],
  variable: '--font-display',
});

export default function RootClientLayout({ children }: { children: React.ReactNode }) {
  // Debug code om te zien of client-side code wordt uitgevoerd
  useEffect(() => {
    console.log('🔍 Root layout mounted');
    
    // Globale error handler toevoegen
    window.onerror = (msg, url, lineNo, columnNo, error) => {
      console.log('🚨 Global error:', { msg, url, lineNo, columnNo, error });
      return false;
    };
    
    // Controleer environment variabelen (alleen de eerste paar karakters tonen voor veiligheid)
    const envVars = {
      FIREBASE_API_KEY: process.env.NEXT_PUBLIC_FIREBASE_API_KEY?.substring(0, 3) + '...',
      FIREBASE_AUTH_DOMAIN: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN?.substring(0, 5) + '...',
      FIREBASE_PROJECT_ID: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID?.substring(0, 5) + '...',
    };
    console.log('📋 Environment vars available:', envVars);
    
    return () => {
      window.onerror = null;
    };
  }, []);

  return (
    <html lang="nl" suppressHydrationWarning>
      <body
        className={cn(
          'min-h-screen bg-background font-sans antialiased',
          inter.variable,
          instrumentSans.variable
        )}
      >
        <AuthProvider>
          <div className="relative flex min-h-screen flex-col">
            <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
              <div className="container flex h-14 items-center">
                <div className="mr-4 flex">
                  <Link className="mr-6 flex items-center space-x-2" href="/">
                    <span className="font-display font-bold text-midnight">GEO Scanner</span>
                  </Link>
                </div>
              </div>
            </header>
            <main className="flex-1">
              <div className="container py-6">{children}</div>
            </main>
          </div>
          <Toaster />
        </AuthProvider>
      </body>
    </html>
  );
}
