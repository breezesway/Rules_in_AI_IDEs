import { Pool } from 'pg';
import fs from 'fs';
import path from 'path';
import dotenv from 'dotenv';

dotenv.config();

const pool = new Pool({
  connectionString: process.env['DATABASE_URL'],
});

interface Migration {
  id: number;
  filename: string;
  sql: string;
}

/**
 * Create migrations table if it doesn't exist
 */
async function createMigrationsTable(): Promise<void> {
  const query = `
    CREATE TABLE IF NOT EXISTS migrations (
      id SERIAL PRIMARY KEY,
      filename VARCHAR(255) NOT NULL UNIQUE,
      executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `;
  
  await pool.query(query);
}

/**
 * Get list of executed migrations
 */
async function getExecutedMigrations(): Promise<string[]> {
  const result = await pool.query('SELECT filename FROM migrations ORDER BY id');
  return result.rows.map(row => row.filename);
}

/**
 * Get list of migration files
 */
function getMigrationFiles(): Migration[] {
  const migrationsDir = path.join(__dirname, 'migrations');
  const files = fs.readdirSync(migrationsDir)
    .filter(file => file.endsWith('.sql'))
    .sort();

  return files.map(filename => {
    const id = parseInt(filename.split('_')[0] || '0');
    const sql = fs.readFileSync(path.join(migrationsDir, filename), 'utf8');
    return { id, filename, sql };
  });
}

/**
 * Execute a migration
 */
async function executeMigration(migration: Migration): Promise<void> {
  const client = await pool.connect();
  
  try {
    await client.query('BEGIN');
    
    // Execute the migration SQL
    await client.query(migration.sql);
    
    // Record the migration as executed
    await client.query(
      'INSERT INTO migrations (filename) VALUES ($1)',
      [migration.filename]
    );
    
    await client.query('COMMIT');
    console.log(`✅ Executed migration: ${migration.filename}`);
  } catch (error) {
    await client.query('ROLLBACK');
    console.error(`❌ Failed to execute migration: ${migration.filename}`);
    throw error;
  } finally {
    client.release();
  }
}

/**
 * Run all pending migrations
 */
export async function runMigrations(): Promise<void> {
  try {
    console.log('🚀 Starting database migrations...');
    
    await createMigrationsTable();
    
    const executedMigrations = await getExecutedMigrations();
    const allMigrations = getMigrationFiles();
    
    const pendingMigrations = allMigrations.filter(
      migration => !executedMigrations.includes(migration.filename)
    );
    
    if (pendingMigrations.length === 0) {
      console.log('✅ No pending migrations');
      return;
    }
    
    console.log(`📋 Found ${pendingMigrations.length} pending migrations`);
    
    for (const migration of pendingMigrations) {
      await executeMigration(migration);
    }
    
    console.log('🎉 All migrations completed successfully');
  } catch (error) {
    console.error('💥 Migration failed:', error);
    throw error;
  }
}

/**
 * Reset database (drop all tables and re-run migrations)
 */
export async function resetDatabase(): Promise<void> {
  try {
    console.log('🔄 Resetting database...');
    
    // Drop all tables
    await pool.query(`
      DROP TABLE IF EXISTS bugs CASCADE;
      DROP TABLE IF EXISTS projects CASCADE;
      DROP TABLE IF EXISTS migrations CASCADE;
    `);
    
    console.log('🗑️  Dropped all tables');
    
    // Re-run migrations
    await runMigrations();
    
    console.log('✅ Database reset completed');
  } catch (error) {
    console.error('💥 Database reset failed:', error);
    throw error;
  }
}

// CLI interface
if (require.main === module) {
  const command = process.argv[2];
  
  if (command === 'reset') {
    resetDatabase()
      .then(() => process.exit(0))
      .catch(() => process.exit(1));
  } else {
    runMigrations()
      .then(() => process.exit(0))
      .catch(() => process.exit(1));
  }
}