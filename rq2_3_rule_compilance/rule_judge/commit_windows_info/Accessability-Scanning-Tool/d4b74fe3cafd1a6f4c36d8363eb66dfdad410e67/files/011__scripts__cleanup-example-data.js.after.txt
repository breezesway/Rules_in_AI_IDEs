#!/usr/bin/env node

/**
 * Manual Cleanup Script for Example.com Test Data
 * 
 * This script manually removes all reports for example.com from the database
 * since these are clearly test data that weren't properly identified by the cleanup service.
 */

const { MongoClient } = require('mongodb');

async function cleanupExampleData() {
    // Load environment variables from .env.local if it exists
    try {
        require('dotenv').config({ path: '.env.local' });
    } catch (error) {
        // .env.local doesn't exist, use defaults
    }
    
    const uri = process.env.MONGODB_URL || 'mongodb://admin:password123@localhost:27017/?authSource=admin';
    const dbName = process.env.MONGODB_DB_NAME || 'accessibility_testing';
    
    console.log('🧹 Starting manual cleanup of example.com test data...');
    console.log(`📊 Database: ${dbName}`);
    console.log(`🔗 Connection: ${uri}`);
    
    let client;
    
    try {
        // Connect to MongoDB
        client = new MongoClient(uri);
        await client.connect();
        console.log('✅ Connected to MongoDB');
        
        const db = client.db(dbName);
        const collection = db.collection('accessibility_reports');
        
        // Find all reports for example.com
        const exampleReports = await collection.find({
            $or: [
                { siteUrl: 'https://example.com' },
                { siteUrl: 'http://example.com' },
                { 'data.siteUrl': 'https://example.com' },
                { 'data.siteUrl': 'http://example.com' }
            ]
        }).toArray();
        
        console.log(`📋 Found ${exampleReports.length} reports for example.com`);
        
        if (exampleReports.length === 0) {
            console.log('✅ No example.com reports found to clean up');
            return;
        }
        
        // Show some details about what we're about to delete
        console.log('\n📝 Reports to be deleted:');
        exampleReports.slice(0, 5).forEach((report, index) => {
            console.log(`  ${index + 1}. ID: ${report._id}`);
            console.log(`     Site: ${report.siteUrl || report.data?.siteUrl || 'Unknown'}`);
            console.log(`     Date: ${new Date(report.lastModified || report.createdAt || report.timestamp).toLocaleString('en-GB')}`);
            console.log(`     Type: ${report.reportType || 'Unknown'}`);
        });
        
        if (exampleReports.length > 5) {
            console.log(`     ... and ${exampleReports.length - 5} more reports`);
        }
        
        // Confirm deletion
        console.log('\n⚠️  WARNING: This will permanently delete all example.com reports!');
        console.log('Press Ctrl+C to cancel, or wait 5 seconds to proceed...');
        
        // Wait 5 seconds for user to cancel
        await new Promise(resolve => setTimeout(resolve, 5000));
        
        // Delete all example.com reports
        const deleteResult = await collection.deleteMany({
            $or: [
                { siteUrl: 'https://example.com' },
                { siteUrl: 'http://example.com' },
                { 'data.siteUrl': 'https://example.com' },
                { 'data.siteUrl': 'http://example.com' }
            ]
        });
        
        console.log(`✅ Successfully deleted ${deleteResult.deletedCount} example.com reports`);
        
        // Verify cleanup
        const remainingExampleReports = await collection.find({
            $or: [
                { siteUrl: 'https://example.com' },
                { siteUrl: 'http://example.com' },
                { 'data.siteUrl': 'https://example.com' },
                { 'data.siteUrl': 'http://example.com' }
            ]
        }).toArray();
        
        if (remainingExampleReports.length === 0) {
            console.log('✅ Verification: All example.com reports have been cleaned up');
        } else {
            console.log(`⚠️  Warning: ${remainingExampleReports.length} example.com reports still remain`);
        }
        
        // Show updated statistics
        const totalReports = await collection.countDocuments();
        console.log(`\n📊 Updated database statistics:`);
        console.log(`   Total reports remaining: ${totalReports}`);
        
    } catch (error) {
        console.error('❌ Error during cleanup:', error.message);
        process.exit(1);
    } finally {
        if (client) {
            await client.close();
            console.log('🔌 Disconnected from MongoDB');
        }
    }
}

// Run the cleanup if this script is executed directly
if (require.main === module) {
    cleanupExampleData()
        .then(() => {
            console.log('🎉 Cleanup completed successfully!');
            process.exit(0);
        })
        .catch((error) => {
            console.error('💥 Cleanup failed:', error);
            process.exit(1);
        });
}

module.exports = { cleanupExampleData }; 