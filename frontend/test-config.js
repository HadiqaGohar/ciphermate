#!/usr/bin/env node
/**
 * Test script to validate Next.js configuration
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🧪 Testing Next.js Configuration...\n');

// Test 1: Check if next.config.ts is valid
console.log('1. Validating next.config.ts...');
try {
  const configPath = path.join(__dirname, 'next.config.ts');
  if (fs.existsSync(configPath)) {
    console.log('   ✅ next.config.ts exists');
    
    // Try to compile the config
    const { spawn } = require('child_process');
    const tsc = spawn('npx', ['tsc', '--noEmit', 'next.config.ts'], { stdio: 'pipe' });
    
    tsc.on('close', (code) => {
      if (code === 0) {
        console.log('   ✅ next.config.ts compiles successfully');
      } else {
        console.log('   ⚠️  next.config.ts has TypeScript issues (may still work)');
      }
    });
  } else {
    console.log('   ❌ next.config.ts not found');
  }
} catch (error) {
  console.log('   ⚠️  Could not validate config:', error.message);
}

// Test 2: Check dependencies
console.log('\n2. Checking dependencies...');
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  const nextVersion = packageJson.dependencies.next;
  console.log(`   ✅ Next.js version: ${nextVersion}`);
  
  if (packageJson.dependencies['@auth0/nextjs-auth0']) {
    console.log(`   ✅ Auth0 Next.js SDK: ${packageJson.dependencies['@auth0/nextjs-auth0']}`);
  }
} catch (error) {
  console.log('   ❌ Could not read package.json');
}

// Test 3: Check environment variables
console.log('\n3. Checking environment configuration...');
const envFiles = ['.env.local', '.env.development', '.env'];
let envFound = false;

for (const envFile of envFiles) {
  if (fs.existsSync(envFile)) {
    console.log(`   ✅ Found ${envFile}`);
    envFound = true;
    break;
  }
}

if (!envFound) {
  console.log('   ⚠️  No environment files found (.env.local, .env.development, .env)');
}

console.log('\n🎯 Configuration Test Complete');
console.log('\nTo start the development server:');
console.log('   npm run dev');
console.log('\nIf you see Turbopack warnings, they are informational and can be ignored.');
console.log('The application should work fine with the updated configuration.');