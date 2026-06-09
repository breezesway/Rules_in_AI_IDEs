import { ModuleScore, ScanResult } from '@/components/molecules/comparative-analysis';
import { getStatusFromScore } from '@/lib/utils/scores';

// Helper functie om de status te berekenen op basis van score
const calculateStatus = (score: number, maxScore: number) => {
  const percentage = Math.round((score / maxScore) * 100);
  return getStatusFromScore(percentage);
};

/**
 * Haal scan resultaat op voor een specifieke scan ID
 */
export async function fetchScanResult(scanId: string): Promise<any> {
  try {
    const response = await fetch(`/api/scans/${scanId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fout bij ophalen scan resultaat:', error);
    throw error;
  }
}

/**
 * Haal scan geschiedenis op voor een specifieke URL
 */
export async function fetchScanHistory(url: string): Promise<ScanResult[]> {
  try {
    const response = await fetch(`/api/scans/history`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Fout bij ophalen scan geschiedenis:', error);
    return [];
  }
}
