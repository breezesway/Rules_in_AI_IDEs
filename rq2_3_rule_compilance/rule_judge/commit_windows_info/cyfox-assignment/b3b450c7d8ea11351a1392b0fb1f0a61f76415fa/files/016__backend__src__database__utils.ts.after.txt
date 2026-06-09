import { QueryResult } from 'pg';
import { query } from './connection';

/**
 * Check if a table exists
 */
export async function tableExists(tableName: string): Promise<boolean> {
  const result = await query(
    `SELECT EXISTS (
      SELECT FROM information_schema.tables 
      WHERE table_schema = 'public' 
      AND table_name = $1
    )`,
    [tableName]
  );
  
  return result.rows[0]?.exists || false;
}

/**
 * Get table row count
 */
export async function getRowCount(tableName: string): Promise<number> {
  const result = await query(`SELECT COUNT(*) as count FROM ${tableName}`);
  return parseInt(result.rows[0]?.count || '0');
}

/**
 * Check database health
 */
export async function checkDatabaseHealth(): Promise<{
  connected: boolean;
  tablesExist: boolean;
  projectCount: number;
  bugCount: number;
}> {
  try {
    // Test basic connection
    await query('SELECT 1');
    
    // Check if required tables exist
    const projectsExist = await tableExists('projects');
    const bugsExist = await tableExists('bugs');
    const tablesExist = projectsExist && bugsExist;
    
    // Get row counts if tables exist
    let projectCount = 0;
    let bugCount = 0;
    
    if (tablesExist) {
      projectCount = await getRowCount('projects');
      bugCount = await getRowCount('bugs');
    }
    
    return {
      connected: true,
      tablesExist,
      projectCount,
      bugCount,
    };
  } catch (error) {
    console.error('Database health check failed:', error);
    return {
      connected: false,
      tablesExist: false,
      projectCount: 0,
      bugCount: 0,
    };
  }
}

/**
 * Clear all data from tables (for testing)
 */
export async function clearAllData(): Promise<void> {
  await query('TRUNCATE TABLE bugs, projects RESTART IDENTITY CASCADE');
  console.log('🧹 Cleared all data from database');
}

/**
 * Build WHERE clause with parameters
 */
export function buildWhereClause(
  conditions: Record<string, any>
): { whereClause: string; params: any[] } {
  const keys = Object.keys(conditions).filter(key => conditions[key] !== undefined);
  
  if (keys.length === 0) {
    return { whereClause: '', params: [] };
  }
  
  const clauses = keys.map((key, index) => `${key} = $${index + 1}`);
  const params = keys.map(key => conditions[key]);
  
  return {
    whereClause: `WHERE ${clauses.join(' AND ')}`,
    params,
  };
}

/**
 * Build ORDER BY clause
 */
export function buildOrderByClause(
  sortBy?: string,
  sortOrder: 'ASC' | 'DESC' = 'ASC'
): string {
  if (!sortBy) {
    return '';
  }
  
  // Whitelist allowed sort columns to prevent SQL injection
  const allowedColumns = [
    'id', 'name', 'title', 'severity', 'status', 'created_at'
  ];
  
  if (!allowedColumns.includes(sortBy)) {
    throw new Error(`Invalid sort column: ${sortBy}`);
  }
  
  return `ORDER BY ${sortBy} ${sortOrder}`;
}

/**
 * Build LIMIT and OFFSET clause for pagination
 */
export function buildPaginationClause(
  page?: number,
  limit?: number
): { limitClause: string; offset: number } {
  if (!page || !limit) {
    return { limitClause: '', offset: 0 };
  }
  
  const offset = (page - 1) * limit;
  return {
    limitClause: `LIMIT ${limit} OFFSET ${offset}`,
    offset,
  };
}