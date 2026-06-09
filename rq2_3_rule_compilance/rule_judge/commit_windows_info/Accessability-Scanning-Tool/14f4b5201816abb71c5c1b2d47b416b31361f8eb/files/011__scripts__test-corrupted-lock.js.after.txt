#!/usr/bin/env node

const fs = require('fs');
const { execSync } = require('child_process');

console.log('🧪 Testing robust installation with corrupted package-lock.json...');

try {
  // Backup current package-lock.json
  if (fs.existsSync('package-lock.json')) {
    fs.copyFileSync('package-lock.json', 'package-lock.json.backup');
    console.log('✅ Backed up current package-lock.json');
  }

  // Create a corrupted package-lock.json with the problematic is@3.3.1 reference
  const corruptedLock = {
    "name": "accessability-scanning-tool",
    "version": "2.1.1",
    "lockfileVersion": 3,
    "requires": true,
    "packages": {
      "": {
        "name": "accessability-scanning-tool",
        "version": "2.1.1",
        "dependencies": {
          "is": "3.3.1"  // This version doesn't exist
        }
      }
    }
  };

  fs.writeFileSync('package-lock.json', JSON.stringify(corruptedLock, null, 2));
  console.log('⚠️  Created corrupted package-lock.json with is@3.3.1');

  // Test the robust installation
  console.log('🔧 Testing robust installation...');
  execSync('npm run install:robust', { stdio: 'inherit' });

  console.log('✅ Robust installation handled corrupted package-lock.json successfully');

} catch (error) {
  console.error('❌ Test failed:', error.message);
} finally {
  // Restore original package-lock.json
  if (fs.existsSync('package-lock.json.backup')) {
    fs.copyFileSync('package-lock.json.backup', 'package-lock.json');
    fs.unlinkSync('package-lock.json.backup');
    console.log('✅ Restored original package-lock.json');
  }
} 