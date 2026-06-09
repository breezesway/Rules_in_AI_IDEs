const express = require('express');
const path = require('path');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Basic routes for testing
app.get('/', (req, res) => {
  // Serve the actual HTML file for testing
  const filePath = path.join(__dirname, '../src/public/index.html');
  console.log('Serving file:', filePath);
  res.sendFile(filePath, (err) => {
    if (err) {
      console.error('Error serving file:', err);
      res.status(500).send('Error loading page');
    }
  });
});

// Serve static files from public directory (after routes to avoid conflicts)
app.use(express.static(path.join(__dirname, '../src/public')));

// API endpoints for testing
app.post('/api/scan', (req, res) => {
  const { url, scanType } = req.body;
  
  // Mock response for testing
  res.json({
    success: true,
    scanId: 'test-scan-' + Date.now(),
    url: url,
    scanType: scanType,
    status: 'completed',
    results: {
      violations: [],
      passes: 10,
      incomplete: 2,
      inapplicable: 5
    }
  });
});

app.get('/api/status/:scanId', (req, res) => {
  res.json({
    scanId: req.params.scanId,
    status: 'completed',
    progress: 100
  });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Start server
app.listen(PORT, () => {
  console.log(`Test server running on http://localhost:${PORT}`);
  console.log('Press Ctrl+C to stop');
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down test server...');
  process.exit(0);
}); 