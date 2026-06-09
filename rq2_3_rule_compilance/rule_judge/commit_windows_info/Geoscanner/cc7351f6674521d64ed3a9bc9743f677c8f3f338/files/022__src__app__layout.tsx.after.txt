// src/app/layout.tsx (Server Component)
import type { Metadata } from 'next';
import RootClientLayout from './root-client-layout'; // Importeer je client layout
import './globals.css'; // Behoud globale stijlen hier

export const metadata: Metadata = {
  title: 'GEO Scanner',
  description: 'Analyseer en optimaliseer uw website voor Google E-A-T',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <RootClientLayout>{children}</RootClientLayout>;
}
