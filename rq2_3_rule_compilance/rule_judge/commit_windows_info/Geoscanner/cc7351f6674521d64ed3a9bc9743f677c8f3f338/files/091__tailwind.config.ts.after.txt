import type { Config } from 'tailwindcss';

const config: Config = {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        // Primaire kleuren
        'deep-blue': '#0F45C5',
        midnight: '#171A31',
        'slate-white': '#F7F9FC',

        // Status kleuren
        'success-green': '#14B870',
        'warning-amber': '#FF9F0A',
        'danger-red': '#FF3B5C',
        'info-teal': '#0ACDDA',

        // Neutrale kleuren
        carbon: '#232429',
        steel: '#616A7D',
        mist: '#A0A9B8',
        cloud: '#E3E6EC',
        snow: '#FFFFFF',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Instrument Sans', 'sans-serif'],
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};

export default config;
