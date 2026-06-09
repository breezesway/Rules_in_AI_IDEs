import { Request, Response, NextFunction } from 'express';
import morgan from 'morgan';

/**
 * Custom token for response time in milliseconds
 */
morgan.token('response-time-ms', (req: Request, res: Response) => {
  const responseTime = res.getHeader('X-Response-Time');
  return responseTime ? `${responseTime}ms` : '-';
});

/**
 * Custom token for request ID (if available)
 */
morgan.token('request-id', (req: Request) => {
  return (req as any).id || '-';
});

/**
 * Development logging format
 */
const developmentFormat = ':method :url :status :response-time-ms - :res[content-length]';

/**
 * Production logging format
 */
const productionFormat = ':remote-addr - :remote-user [:date[clf]] ":method :url HTTP/:http-version" :status :res[content-length] ":referrer" ":user-agent" :response-time-ms';

/**
 * Create request logger middleware
 */
export function createRequestLogger() {
  const format = process.env.NODE_ENV === 'production' 
    ? productionFormat 
    : developmentFormat;

  return morgan(format, {
    skip: (req: Request, res: Response) => {
      // Skip logging for health check endpoints
      return req.url === '/health' || req.url === '/api/health';
    },
    stream: {
      write: (message: string) => {
        // Remove trailing newline and log
        console.log(message.trim());
      },
    },
  });
}

/**
 * Add response time header
 */
export function addResponseTime(req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    res.setHeader('X-Response-Time', duration);
  });
  
  next();
}