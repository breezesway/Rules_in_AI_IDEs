/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // Tijdens de build worden de ESLint fouten behandeld als waarschuwingen
    ignoreDuringBuilds: true,
  },
};

module.exports = nextConfig;
