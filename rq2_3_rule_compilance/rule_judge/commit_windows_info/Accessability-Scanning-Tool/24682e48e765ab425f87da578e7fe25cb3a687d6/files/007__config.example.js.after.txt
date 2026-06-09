/**
 * Accessibility Testing Configuration
 * Copy this file to config.js and customize for your website
 */

module.exports = {
  // ===========================================
  // TARGET WEBSITE CONFIGURATION
  // ===========================================
  targetSiteUrl: 'https://your-website.com',

  // ===========================================
  // CRAWLING PERFORMANCE SETTINGS
  // ===========================================
  
  // Maximum number of pages to discover and test
  maxPages: 50,
  
  // Maximum depth to crawl (1 = homepage only, 2 = homepage + direct links, etc.)
  maxDepth: 4,
  
  // Delay between page requests in milliseconds (be respectful to the server)
  delayBetweenRequests: 300,
  
  // Number of retry attempts for failed pages
  maxRetries: 3,
  
  // Delay between retry attempts in milliseconds
  retryDelay: 1500,
  
  // Timeout for each page load in milliseconds
  pageTimeout: 20000,

  // ===========================================
  // TEST EXECUTION SETTINGS
  // ===========================================
  
  // Fail the entire test if critical accessibility violations are found
  failOnCriticalViolations: true,
  
  // Minimum compliance threshold (0-100%) to pass the test
  minimumComplianceThreshold: 80,

  // ===========================================
  // EXAMPLE CONFIGURATIONS FOR DIFFERENT SITE TYPES
  // ===========================================
  
  // For fast static sites:
  fastStaticSite: {
    pageTimeout: 10000,
    delayBetweenRequests: 200,
    maxRetries: 2,
  },
  
  // For complex web applications:
  complexWebApp: {
    pageTimeout: 30000,
    delayBetweenRequests: 500,
    maxRetries: 3,
  },
  
  // For very large sites:
  largeSite: {
    maxPages: 100,
    maxDepth: 5,
    pageTimeout: 45000,
  },

  // ===========================================
  // UNIVERSAL EXCLUSION PATTERNS
  // ===========================================
  
  // These patterns work for any website and exclude common non-content pages
  excludePatterns: [
    // Documents
    /\.(pdf|doc|docx|xls|xlsx|ppt|pptx|zip|rar|tar|gz|7z)$/i,
    
    // Images
    /\.(jpg|jpeg|png|gif|svg|webp|ico|bmp|tiff)$/i,
    
    // Media files
    /\.(mp4|avi|mov|wmv|flv|webm|mkv|mp3|wav|ogg)$/i,
    
    // Static resources
    /\.(css|js|json|xml|txt|csv)$/i,
    
    // Admin and authentication pages
    /\/wp-admin\//i,
    /\/admin\//i,
    /\/login\//i,
    /\/logout\//i,
    /\/signin\//i,
    /\/signup\//i,
    /\/register\//i,
    
    // E-commerce and search
    /\/search\?/i,
    /\/cart\//i,
    /\/checkout\//i,
    /\/payment\//i,
    
    // Technical pages
    /\/api\//i,
    /\/feed\//i,
    /\/feeds\//i,
    /\/rss\//i,
    /\/sitemap/i,
    /\/robots\.txt$/i,
    
    // Tracking and analytics
    /\?.*utm_/i,
    /\?.*fbclid/i,
    /\?.*gclid/i,
    
    // Links and fragments
    /#/i,
    /mailto:/i,
    /tel:/i,
    /ftp:/i,
    /javascript:/i,
    
    // Pagination patterns
    /\/\d{4}\/\d{2}\/\d{2}\//i,
    /\/page\/\d+/i,
    /\/p\/\d+/i,
    /\?page=/i,
    /\?p=/i,
  ],

  // ===========================================
  // CUSTOM EXCLUSION PATTERNS
  // ===========================================
  
  // Add site-specific patterns here
  customExcludePatterns: [
    // Example: /\/your-custom-pattern\//i,
    // Example: /\/another-exclusion\//i,
  ],
}; 