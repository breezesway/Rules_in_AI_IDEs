import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';

import { createRequestLogger, addResponseTime } from './middleware/request-logger';
import { errorHandler, notFoundHandler } from './middleware/error-handler';
// Database connection is initialized in index.ts
import { checkDatabaseHealth } from './database/utils';

// Import routes
import projectRoutes from './routes/project-routes';
import bugRoutes from './routes/bug-routes';

// Load environment variables
dotenv.config();

const app = express();

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  crossOriginEmbedderPolicy: false,
}));

// CORS configuration
app.use(cors({
  origin: process.env['CORS_ORIGIN'] || 'http://localhost:3001',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// Request parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging and monitoring middleware
app.use(addResponseTime);
app.use(createRequestLogger());

// Health check endpoint
app.get('/health', async (_req, res) => {
  try {
    const dbHealth = await checkDatabaseHealth();
    
    res.json({
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      database: dbHealth,
      environment: process.env['NODE_ENV'] || 'development',
    });
  } catch (error) {
    res.status(503).json({
      status: 'error',
      timestamp: new Date().toISOString(),
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

// API routes
app.get('/api', (_req, res) => {
  res.json({
    message: 'Bug Tracker API',
    version: '1.0.0',
    endpoints: {
      projects: '/api/projects',
      bugs: '/api/projects/:projectId/bugs',
      health: '/health',
    },
  });
});

// Mount API routes
app.use('/api/projects', projectRoutes);
app.use('/api/projects', bugRoutes);

// Error handling middleware (must be last)
app.use(notFoundHandler);
app.use(errorHandler);

export default app;