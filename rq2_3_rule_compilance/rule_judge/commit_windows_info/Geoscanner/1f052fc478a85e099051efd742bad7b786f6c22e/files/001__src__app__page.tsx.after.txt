'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Toggle } from '@/components/ui/toggle';
import { Label } from '@/components/ui/label';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { useState, useEffect } from 'react';
import { ScanResults } from '@/components/scan-results';
import { useToast } from '@/components/ui/use-toast';
import { FeatureBanner } from '@/components/molecules/feature-banner';

// Demo resultaat voor testen
// const demoResult = { // Commented out as it's unused
// overallScore: 78,
// modules: [
// ... (rest of the object commented out)
// ],
// };

export default function Home() {
  const [isScanning, setIsScanning] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [url, setUrl] = useState('');
  const [fullDomainScan, setFullDomainScan] = useState(false);
  const [scanResult, setScanResult] = useState<any>(null);
  const { toast } = useToast();
  
  // Debug informatie
  useEffect(() => {
    console.log('📱 Home page component geladen');
    
    // Test of UI elementen worden gerenderd
    setTimeout(() => {
      const uiElements = {
        card: document.querySelector('.card'),
        form: document.querySelector('form'),
        button: document.querySelector('button[type="submit"]'),
        input: document.querySelector('input[type="url"]')
      };
      console.log('📱 UI elementen gevonden:', 
        Object.keys(uiElements).map(key => `${key}: ${!!uiElements[key as keyof typeof uiElements]}`).join(', ')
      );
    }, 1000);
  }, []);

  const isValidUrl = (url: string) => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('🚀 Form submission met URL:', url);
    
    if (!isValidUrl(url)) {
      toast({
        title: 'Ongeldige URL',
        description: 'Voer een geldige URL in (inclusief http(s)://)',
        variant: 'destructive',
      });
      console.log('❌ Ongeldige URL gedetecteerd');
      return;
    }
    setIsScanning(true);
    setProgress(0);

    try {
      console.log('🔄 API call starten naar /api/scan');
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, fullDomainScan }),
      });

      if (!response.ok) {
        const error = await response.json();
        console.log('❌ API error:', error);
        throw new Error(error.error || 'Er is een fout opgetreden');
      }

      const result = await response.json();
      console.log('✅ API resultaat ontvangen:', result);

      if (result.error) {
        console.log('❌ Error in resultaat:', result.error);
        throw new Error(result.error);
      }

      setScanResult(result);
      setShowResults(true);
    } catch (error) {
      console.log('❌ Exception opgetreden:', error);
      toast({
        title: 'Fout',
        description: error instanceof Error ? error.message : 'Er is een fout opgetreden',
        variant: 'destructive',
      });
    } finally {
      setIsScanning(false);
    }
  };

  const handleNewScan = () => {
    setShowResults(false);
    setUrl('');
    setFullDomainScan(false);
    setScanResult(null);
    setProgress(0);
    setIsScanning(false);
  };

  if (showResults && scanResult) {
    return (
      <div className="container py-8">
        <ScanResults result={scanResult} onNewScan={handleNewScan} />
      </div>
    );
  }

  // Voeg extra debug render toe
  console.log('🎨 Rendering homepage UI');

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] bg-slate-50">
      <Card className="w-full max-w-2xl shadow-lg">
        <CardHeader>
          <CardTitle className="text-3xl font-display font-bold text-midnight">
            Is jouw website LLM-proof?
          </CardTitle>
          <CardDescription className="text-lg text-steel">
            Scan je pagina en ontdek in 10 seconden hoe goed jouw content zichtbaar is in ChatGPT,
            Claude en Google Gemini
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="url" className="text-steel">
                URL
              </Label>
              <Input
                id="url"
                type="url"
                placeholder="https://voorbeeld.nl"
                className="w-full h-12 text-lg"
                disabled={isScanning}
                value={url}
                onChange={e => setUrl(e.target.value)}
                required
              />
            </div>
            <div className="flex items-center space-x-2">
              <Toggle
                id="domain-scan"
                aria-label="Volledige domeinscan"
                disabled={isScanning}
                pressed={fullDomainScan}
                onPressedChange={setFullDomainScan}
              >
                Volledige domeinscan
              </Toggle>
              <Label htmlFor="domain-scan" className="text-sm text-steel">
                Scan alle pagina's binnen dit domein
              </Label>
            </div>
            <Button type="submit" className="w-full h-12 text-lg" disabled={isScanning}>
              {isScanning ? 'Bezig met scannen...' : 'Start Scan'}
            </Button>
          </form>
          {isScanning && (
            <div className="mt-4">
              <Progress value={progress} className="h-2" />
            </div>
          )}
        </CardContent>
      </Card>

      {/* Feature Banner */}
      <FeatureBanner className="w-full max-w-2xl mt-12" />

      {/* Info Sectie */}
      <div className="w-full max-w-2xl mt-12 space-y-8">
        <div className="text-center">
          <h2 className="text-2xl font-display font-bold text-midnight mb-4">Hoe het werkt</h2>
          <p className="text-steel">
            We analyseren je website op 8 cruciale criteria voor LLM-visibility
          </p>
        </div>

        <div className="grid grid-cols-1 gap-4">
          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">🔍</span>
              <h3 className="font-semibold text-lg text-midnight">Crawl-toegang</h3>
            </div>
            <p className="text-steel">
              Kan Google en andere zoekmachines mijn website goed vinden en lezen? Dit criterium
              kijkt of je website toegankelijk is voor zoekmachines, zodat je gevonden kunt worden.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">🔄</span>
              <h3 className="font-semibold text-lg text-midnight">Structured Data</h3>
            </div>
            <p className="text-steel">
              Begrijpen zoekmachines waar mijn pagina over gaat? Dit controleert of je extra
              informatie hebt toegevoegd, zodat zoekmachines en AI je pagina beter snappen.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">❓</span>
              <h3 className="font-semibold text-lg text-midnight">Answer-ready content</h3>
            </div>
            <p className="text-steel">
              Geeft mijn pagina direct antwoord op vragen van bezoekers? Dit kijkt of je teksten
              duidelijk en direct antwoord geven, zodat je kans maakt op een prominente plek in
              zoekresultaten.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">🏆</span>
              <h3 className="font-semibold text-lg text-midnight">Autoriteit & citaties</h3>
            </div>
            <p className="text-steel">
              Komt mijn website betrouwbaar en deskundig over? Dit criterium meet of je pagina
              verwijzingen of citaties bevat, wat je betrouwbaarheid vergroot.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">🕒</span>
              <h3 className="font-semibold text-lg text-midnight">Versheid</h3>
            </div>
            <p className="text-steel">
              Is de informatie op mijn website actueel? Dit controleert of je pagina recent is
              bijgewerkt, zodat bezoekers en zoekmachines weten dat de informatie up-to-date is.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">🌐</span>
              <h3 className="font-semibold text-lg text-midnight">Cross-web footprint</h3>
            </div>
            <p className="text-steel">
              Wordt mijn content ook op andere plekken op het internet genoemd? Dit kijkt of je
              website of content ook op andere relevante websites of platforms te vinden is.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">👁️</span>
              <h3 className="font-semibold text-lg text-midnight">Multimodale leesbaarheid</h3>
            </div>
            <p className="text-steel">
              Is mijn website goed te begrijpen voor iedereen, ook voor mensen met een beperking?
              Dit criterium kijkt of je pagina duidelijk is, met bijvoorbeeld goede afbeeldingen,
              video's en teksten.
            </p>
          </div>

          <div className="criterion-item p-4 bg-white rounded-lg shadow-sm border border-gray-100">
            <div className="flex items-center mb-2">
              <span className="text-2xl mr-3">📊</span>
              <h3 className="font-semibold text-lg text-midnight">Monitoring-haakjes</h3>
            </div>
            <p className="text-steel">
              Kan ik meten hoe goed mijn website presteert? Dit controleert of je tools hebt
              geïnstalleerd om te zien hoeveel bezoekers je hebt en hoe je pagina's scoren.
            </p>
          </div>
        </div>

        <Separator className="my-8" />

        {/* Footer */}
        <footer className="text-center text-steel text-sm">
          <div className="space-x-4 mb-4">
            <a href="/voorwaarden" className="hover:text-midnight">
              Gebruiksvoorwaarden
            </a>
            <a href="/privacy" className="hover:text-midnight">
              Privacy
            </a>
            <a href="/contact" className="hover:text-midnight">
              Contact
            </a>
          </div>
          <p>© 2024 GEO Scanner. Alle rechten voorbehouden.</p>
        </footer>
      </div>
    </div>
  );
}
