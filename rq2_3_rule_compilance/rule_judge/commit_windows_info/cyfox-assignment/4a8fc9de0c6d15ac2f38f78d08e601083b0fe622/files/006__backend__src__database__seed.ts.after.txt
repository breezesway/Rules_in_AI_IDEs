import { transaction } from './connection';
import { clearAllData } from './utils';

interface SeedProject {
  name: string;
  bugs: SeedBug[];
}

interface SeedBug {
  title: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'in_progress' | 'resolved' | 'closed';
}

const seedData: SeedProject[] = [
  {
    name: 'E-commerce Website',
    bugs: [
      {
        title: 'Shopping cart not updating quantities',
        description: 'When users try to update item quantities in the shopping cart, the changes are not being saved. This affects the checkout process and user experience.',
        severity: 'high',
        status: 'open',
      },
      {
        title: 'Payment gateway timeout',
        description: 'Payment processing is timing out for transactions over $500. Users are getting error messages and transactions are failing.',
        severity: 'critical',
        status: 'in_progress',
      },
      {
        title: 'Product images not loading on mobile',
        description: 'Product images are not displaying correctly on mobile devices, showing broken image icons instead.',
        severity: 'medium',
        status: 'open',
      },
      {
        title: 'Search functionality case sensitivity',
        description: 'The search feature is case-sensitive, making it difficult for users to find products. Should be case-insensitive.',
        severity: 'low',
        status: 'resolved',
      },
      {
        title: 'Email notifications not sent',
        description: 'Order confirmation emails are not being sent to customers after successful purchases.',
        severity: 'medium',
        status: 'closed',
      },
    ],
  },
  {
    name: 'Mobile Banking App',
    bugs: [
      {
        title: 'Login fails with special characters in password',
        description: 'Users with special characters in their passwords cannot log in. The authentication system seems to have issues with character encoding.',
        severity: 'high',
        status: 'open',
      },
      {
        title: 'Balance display shows incorrect currency',
        description: 'Account balances are displaying in the wrong currency for international users. Should respect user locale settings.',
        severity: 'medium',
        status: 'in_progress',
      },
      {
        title: 'Transfer limits not enforced',
        description: 'Daily transfer limits are not being properly enforced, allowing users to exceed their set limits.',
        severity: 'critical',
        status: 'open',
      },
      {
        title: 'App crashes on iOS 15',
        description: 'The mobile app consistently crashes on iOS 15 devices when accessing the transaction history.',
        severity: 'high',
        status: 'resolved',
      },
    ],
  },
  {
    name: 'Project Management Tool',
    bugs: [
      {
        title: 'Task assignments not saving',
        description: 'When assigning tasks to team members, the assignments are not being saved to the database.',
        severity: 'high',
        status: 'open',
      },
      {
        title: 'Calendar view performance issues',
        description: 'The calendar view becomes very slow when loading projects with many tasks. Need to optimize the query performance.',
        severity: 'medium',
        status: 'in_progress',
      },
      {
        title: 'File upload size limit too small',
        description: 'Users cannot upload files larger than 5MB, but business requirements specify 50MB limit.',
        severity: 'low',
        status: 'open',
      },
      {
        title: 'Notification preferences not working',
        description: 'Users are receiving notifications even when they have disabled them in their preferences.',
        severity: 'medium',
        status: 'resolved',
      },
      {
        title: 'Export to PDF formatting issues',
        description: 'When exporting project reports to PDF, the formatting is broken and text is overlapping.',
        severity: 'low',
        status: 'closed',
      },
    ],
  },
  {
    name: 'Social Media Dashboard',
    bugs: [
      {
        title: 'Analytics data not refreshing',
        description: 'The analytics dashboard is showing stale data from yesterday. Real-time updates are not working.',
        severity: 'medium',
        status: 'open',
      },
      {
        title: 'Post scheduling fails for Instagram',
        description: 'Scheduled posts to Instagram are failing with API authentication errors.',
        severity: 'high',
        status: 'in_progress',
      },
    ],
  },
];



/**
 * Run the complete seeding process
 */
export async function seedDatabase(): Promise<void> {
  try {
    console.log('🚀 Starting database seeding...');
    
    await transaction(async (client) => {
      // Clear existing data
      await client.query('TRUNCATE TABLE bugs, projects RESTART IDENTITY CASCADE');
      console.log('🧹 Cleared existing data');
      
      // Seed projects first
      const projectResult = await client.query(`
        INSERT INTO projects (name) VALUES 
        ${seedData.map((_, index) => `($${index + 1})`).join(', ')}
        RETURNING id, name
      `, seedData.map(p => p.name));
      
      const projectIds = new Map<string, number>();
      projectResult.rows.forEach(row => {
        projectIds.set(row.name, row.id);
      });
      
      console.log(`✅ Created ${projectResult.rows.length} projects`);
      
      // Seed bugs for each project
      for (const project of seedData) {
        const projectId = projectIds.get(project.name);
        if (!projectId) continue;
        
        if (project.bugs.length > 0) {
          const bugValues = project.bugs.map((_bug, index) => {
            const baseIndex = index * 5;
            return `($${baseIndex + 1}, $${baseIndex + 2}, $${baseIndex + 3}, $${baseIndex + 4}, $${baseIndex + 5})`;
          }).join(', ');
          
          const bugParams = project.bugs.flatMap(bug => [
            projectId,
            bug.title,
            bug.description,
            bug.severity,
            bug.status,
          ]);
          
          await client.query(`
            INSERT INTO bugs (project_id, title, description, severity, status) 
            VALUES ${bugValues}
          `, bugParams);
        }
      }
      
      const totalBugs = seedData.reduce((sum, project) => sum + project.bugs.length, 0);
      console.log(`✅ Created ${totalBugs} bugs`);
    });
    
    console.log('🎉 Database seeding completed successfully!');
    
    // Print summary
    const projectCount = seedData.length;
    const bugCount = seedData.reduce((sum, project) => sum + project.bugs.length, 0);
    
    console.log('\n📊 Seeding Summary:');
    console.log(`  Projects: ${projectCount}`);
    console.log(`  Bugs: ${bugCount}`);
    console.log(`  Severities: ${getSeverityDistribution()}`);
    console.log(`  Statuses: ${getStatusDistribution()}`);
    
  } catch (error) {
    console.error('💥 Database seeding failed:', error);
    throw error;
  }
}

/**
 * Get severity distribution for summary
 */
function getSeverityDistribution(): string {
  const severities = seedData.flatMap(p => p.bugs.map(b => b.severity));
  const counts = severities.reduce((acc, severity) => {
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return Object.entries(counts)
    .map(([severity, count]) => `${severity}: ${count}`)
    .join(', ');
}

/**
 * Get status distribution for summary
 */
function getStatusDistribution(): string {
  const statuses = seedData.flatMap(p => p.bugs.map(b => b.status));
  const counts = statuses.reduce((acc, status) => {
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);
  
  return Object.entries(counts)
    .map(([status, count]) => `${status}: ${count}`)
    .join(', ');
}

/**
 * Reset database and reseed
 */
export async function resetAndSeed(): Promise<void> {
  await clearAllData();
  await seedDatabase();
}

// CLI interface
if (require.main === module) {
  const command = process.argv[2];
  
  if (command === 'reset') {
    resetAndSeed()
      .then(() => process.exit(0))
      .catch(() => process.exit(1));
  } else {
    seedDatabase()
      .then(() => process.exit(0))
      .catch(() => process.exit(1));
  }
}