import { Request, Response, NextFunction } from 'express';
import morgan from 'morgan';

/**
 * Custom token for response time in milliseconds
 */
morgan.token('response-time-ms', (_req: Request, res: Response) => {
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
  const format = process.env['NODE_ENV'] === 'production' 
    ? productionFormat 
    : developmentFormat;

  return morgan(format, {
    skip: (req: Request, _res: Response) => {
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
export function addResponseTime(_req: Request, res: Response, next: NextFunction): void {
  const start = Date.now();
  
  // Store the original end method
  const originalEnd = res.end;
  
  // Override the end method
  res.end = function(this: Response, chunk?: any, encoding?: BufferEncoding, callback?: () => void): Response {
    const duration = Date.now() - start;
    
    // Only set the header if headers haven't been sent yet
    if (!res.headersSent) {
      res.setHeader('X-Response-Time', duration.toString());
    }
    
    // Call the original end method with proper type handling
    return originalEnd.call(this, chunk, encoding as BufferEncoding, callback);
  } as any;
  
  next();
}