#!/usr/bin/env node

import { chmodSync, existsSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// List of files that need executable permissions
const executableFiles = [
  'dist/mcp-server/index.js',
  // Add more files here as needed
];

console.log('Setting executable permissions...');

executableFiles.forEach(file => {
  const filePath = join(__dirname, '..', file);

  // Skip if file doesn't exist yet (e.g., during npm install before build)
  if (!existsSync(filePath)) {
    console.log(`⊘ Skipping ${file} (not built yet)`);
    return;
  }

  try {
    chmodSync(filePath, '755');
    console.log(`✓ Made ${file} executable`);
  } catch (error) {
    console.error(`✗ Failed to make ${file} executable:`, error.message);
  }
});

console.log('Postinstall complete.');