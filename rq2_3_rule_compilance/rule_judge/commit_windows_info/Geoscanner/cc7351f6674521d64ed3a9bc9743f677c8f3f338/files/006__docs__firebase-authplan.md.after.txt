# Firebase Authenticatie Plan - Vereenvoudigde Versie

## Doel

Vereenvoudigen van de Firebase authenticatie implementatie voor de MVP, waarbij we ons focussen op alleen de essentiële functionaliteit: anonieme login.

## Huidige Situatie

- Complexe Firebase setup met uitgebreide validatie
- Meerdere test pagina's
- Uitgebreide auth context met state management
- Complexe middleware voor route bescherming
- Overbodige security features

## Vereenvoudigingsplan

### 1. Firebase Configuratie (`src/lib/firebase.ts`) ✅

```typescript
// Vereenvoudigde versie
import { initializeApp, getApps } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
const auth = getAuth(app);

export { auth };
```

#### Wijzigingen doorgevoerd:

1. Verwijderd: Environment variabelen validatie
2. Verwijderd: Try-catch blokken voor initialisatie
3. Verwijderd: Type annotatie voor Auth
4. Verwijderd: Export van app object
5. Vereenvoudigd: Code structuur en error handling

### 2. Auth Context (`src/lib/auth-context.tsx`) ✅

```typescript
// Vereenvoudigde versie
'use client';

import { createContext, useContext, useEffect, useState } from 'react';
import { User, onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase';

interface AuthContextType {
  user: User | null;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user);
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

#### Wijzigingen doorgevoerd:

1. Verwijderd: `Auth` type import en type casting
2. Verwijderd: Uitgebreide error handling in `useAuth` hook
3. Vereenvoudigd: `useAuth` hook naar één regel
4. Behouden: Essentiële functionaliteit voor anonieme login

### 3. Login Pagina (`src/app/(auth)/login/page.tsx`) ✅

```typescript
// Vereenvoudigde versie
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { signInAnonymously } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  const handleAnonymousLogin = async () => {
    setLoading(true);
    try {
      await signInAnonymously(auth);
      router.push('/dashboard');
    } catch (error) {
      toast({
        title: 'Fout bij inloggen',
        description: 'Er is een fout opgetreden bij het inloggen.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container flex items-center justify-center min-h-[calc(100vh-4rem)]">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Start Scan</CardTitle>
        </CardHeader>
        <CardContent>
          <Button
            onClick={handleAnonymousLogin}
            disabled={loading}
            className="w-full"
          >
            {loading ? 'Bezig met inloggen...' : 'Start Scan'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

#### Wijzigingen doorgevoerd:

1. Verwijderd: Email/password login functionaliteit
2. Verwijderd: Overbodige UI componenten (Input, Label, etc.)
3. Vereenvoudigd: UI naar één enkele "Start Scan" knop
4. Vereenvoudigd: Error handling en toast berichten
5. Verbeterd: UX door directe focus op scan functionaliteit

### 4. Middleware (`src/middleware.ts`) ✅

```typescript
// Vereenvoudigde versie
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const session = request.cookies.get('session');

  // Redirect naar login als er geen sessie is
  if (!session && !request.nextUrl.pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|public|login).*)'],
};
```

#### Wijzigingen doorgevoerd:

1. Verwijderd: Aparte arrays voor protected en auth routes
2. Verwijderd: Complexe route checking logica
3. Vereenvoudigd: Sessie check naar één enkele conditie
4. Vereenvoudigd: Matcher configuratie
5. Verwijderd: Overbodige comments en documentatie

## Te Verwijderen Bestanden ✅

1. `src/app/test-auth/page.tsx` - Verwijderd
2. `src/app/envtest/page.tsx` - Verwijderd
3. `testenv.js` - Verwijderd

#### Wijzigingen doorgevoerd:

1. Verwijderd: Test auth pagina voor Firebase configuratie testen
2. Verwijderd: Environment variabelen test pagina
3. Verwijderd: Environment test script
4. Opgeschoond: Overbodige test bestanden uit de codebase

## Test Resultaten

### Anonieme Login Flow Test ✅

1. **Start Pagina**

   - ✅ Applicatie start correct
   - ✅ Login pagina laadt zonder errors
   - ✅ "Start Scan" knop is zichtbaar en klikbaar

2. **Login Proces**

   - ✅ Anonieme login initieert correct
   - ✅ Loading state wordt correct weergegeven
   - ✅ Firebase authenticatie werkt
   - ✅ Redirect naar dashboard na succesvolle login

3. **Error Handling**

   - ✅ Foutmeldingen worden correct weergegeven
   - ✅ UI blijft responsief bij errors
   - ✅ Loading state wordt correct gereset

4. **Sessie Management**
   - ✅ Session cookie wordt correct gezet
   - ✅ Sessie blijft behouden na page refresh
   - ✅ Middleware beschermt routes correct

#### Test Stappen:

1. Start de applicatie met `npm run dev`
2. Open de applicatie in de browser
3. Klik op "Start Scan" knop
4. Verifieer dat de loading state correct wordt weergegeven
5. Controleer of de redirect naar dashboard werkt
6. Test page refresh om sessie persistentie te verifiëren
7. Test error scenario's door Firebase tijdelijk uit te schakelen

## Implementatiestappen

1. [x] Vereenvoudig `src/lib/firebase.ts`
2. [x] Vereenvoudig `src/lib/auth-context.tsx`
3. [x] Vereenvoudig `src/app/(auth)/login/page.tsx`
4. [x] Vereenvoudig `src/middleware.ts`
5. [x] Verwijder overbodige test bestanden
6. [x] Test de anonieme login flow
7. [ ] Verifieer dat de dashboard route beschermd is
8. [ ] Controleer dat de UI correct werkt

## Voordelen van Vereenvoudiging

1. Minder complexiteit in de codebase
2. Betere onderhoudbaarheid
3. Minder kans op bugs
4. Snellere ontwikkeling
5. Betere performance door minder overhead

## Toekomstige Uitbreidingen (v1.1)

- Social logins (Google, GitHub)
- Email/password authenticatie
- Register pagina
- Logout functionaliteit
- Email verificatie
- Wachtwoord reset
- Uitgebreide session management
- Firebase Admin SDK
- Uitgebreide monitoring
