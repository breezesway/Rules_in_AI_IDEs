const fs = require('fs');
const path = require('path');

const sourceDir = path.join(__dirname, '..', 'src', 'public');
const targetDir = path.join(__dirname, '..', 'dist', 'public');

try {
  // Create target directory if it doesn't exist
  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  // Copy all files from src/public to dist/public
  const files = fs.readdirSync(sourceDir);
  files.forEach(file => {
    const sourcePath = path.join(sourceDir, file);
    const targetPath = path.join(targetDir, file);
    
    if (fs.statSync(sourcePath).isFile()) {
      fs.copyFileSync(sourcePath, targetPath);
      console.log(`Copied: ${file}`);
    }
  });

  console.log('✅ Public files copied successfully');
} catch (error) {
  console.error('❌ Error copying public files:', error.message);
  process.exit(1);
} 