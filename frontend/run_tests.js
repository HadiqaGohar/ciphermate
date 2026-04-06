#!/usr/bin/env node
/**
 * Test runner script for CipherMate frontend tests
 */

const { spawn } = require('child_process');
const path = require('path');

function runCommand(command, args, description) {
  return new Promise((resolve, reject) => {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Running: ${description}`);
    console.log(`Command: ${command} ${args.join(' ')}`);
    console.log(`${'='.repeat(60)}`);

    const child = spawn(command, args, {
      stdio: 'inherit',
      cwd: __dirname
    });

    child.on('close', (code) => {
      if (code === 0) {
        console.log(`✅ ${description} passed`);
        resolve();
      } else {
        console.log(`❌ ${description} failed with exit code ${code}`);
        reject(new Error(`${description} failed`));
      }
    });

    child.on('error', (error) => {
      console.error(`Error running ${description}:`, error);
      reject(error);
    });
  });
}

async function main() {
  const args = process.argv.slice(2);
  const testType = args.find(arg => ['unit', 'integration', 'e2e', 'all'].includes(arg)) || 'all';
  const coverage = args.includes('--coverage');
  const watch = args.includes('--watch');
  const verbose = args.includes('--verbose') || args.includes('-v');

  let success = true;

  try {
    // Base Jest command
    let jestArgs = [];
    
    if (coverage) {
      jestArgs.push('--coverage');
    }
    
    if (watch) {
      jestArgs.push('--watch');
    }
    
    if (verbose) {
      jestArgs.push('--verbose');
    }

    if (testType === 'unit' || testType === 'all') {
      const unitArgs = [...jestArgs, '--testPathPattern=__tests__'];
      await runCommand('npm', ['test', '--', ...unitArgs], 'Unit Tests');
    }

    if (testType === 'integration' || testType === 'all') {
      const integrationArgs = [...jestArgs, '--testPathPattern=integration'];
      await runCommand('npm', ['test', '--', ...integrationArgs], 'Integration Tests');
    }

    if (testType === 'e2e' || testType === 'all') {
      // For E2E tests, we would typically use Cypress or Playwright
      console.log('\n📝 E2E tests would run with Cypress/Playwright (not implemented in this demo)');
    }

    // Run linting and type checking
    if (testType === 'all') {
      console.log(`\n${'='.repeat(60)}`);
      console.log('Running Code Quality Checks');
      console.log(`${'='.repeat(60)}`);

      // ESLint
      await runCommand('npm', ['run', 'lint'], 'ESLint Check');

      // TypeScript type checking
      await runCommand('npx', ['tsc', '--noEmit'], 'TypeScript Type Check');
    }

    console.log('\n🎉 All tests passed!');
    process.exit(0);

  } catch (error) {
    console.log('\n❌ Some tests failed!');
    process.exit(1);
  }
}

// Show usage if help is requested
if (process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(`
Usage: node run_tests.js [options] [test-type]

Test Types:
  unit         Run unit tests only
  integration  Run integration tests only
  e2e          Run end-to-end tests only
  all          Run all tests (default)

Options:
  --coverage   Generate coverage report
  --watch      Run tests in watch mode
  --verbose    Verbose output
  -v           Verbose output (short form)
  --help       Show this help message
  -h           Show this help message (short form)

Examples:
  node run_tests.js unit --coverage
  node run_tests.js all --verbose
  node run_tests.js --watch
`);
  process.exit(0);
}

main();