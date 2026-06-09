'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart2, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

interface FeatureBannerProps {
  className?: string;
}

export function FeatureBanner({ className }: FeatureBannerProps) {
  const [isVisible, setIsVisible] = useState(true);
  const [isMounted, setIsMounted] = useState(false);
  
  // Client-side alleen - voorkomt hydration mismatch
  useEffect(() => {
    setIsMounted(true);
    console.log('🎌 FeatureBanner component gemount');
  }, []);
  
  // Render niks tijdens SSR
  if (!isMounted) {
    return null;
  }

  if (!isVisible) return null;

  return (
    <motion.div
      className={`bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-lg shadow-lg mb-8 ${className}`}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className="mr-4 bg-white/20 p-2 rounded-full">
            <BarChart2 className="h-6 w-6" />
          </div>
          <div>
            <h3 className="font-semibold text-lg">Nieuwe Visualisatie Tools Beschikbaar!</h3>
            <p className="text-white/80">
              Ontdek interactieve grafieken en vergelijkende analyses in je scan resultaten.
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <Link href="/dashboard/scan123" passHref>
            <Button variant="secondary" className="whitespace-nowrap">
              Bekijk Demo
            </Button>
          </Link>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsVisible(false)}
            className="text-white hover:bg-white/20"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </motion.div>
  );
}
