#!/usr/bin/env python3
"""
Test runner script for CipherMate backend tests
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"✅ {description} passed")
        return True


def main():
    parser = argparse.ArgumentParser(description="Run CipherMate backend tests")
    parser.add_argument(
        "--type",
        choices=["unit", "integration", "e2e", "all"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run tests with coverage report"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--parallel",
        "-n",
        type=int,
        help="Number of parallel workers"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    
    # Add verbosity
    if args.verbose:
        pytest_cmd.append("-v")
    
    # Add parallel execution
    if args.parallel:
        pytest_cmd.extend(["-n", str(args.parallel)])
    
    # Add coverage
    if args.coverage:
        pytest_cmd.extend([
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under=80"
        ])
    
    success = True
    
    if args.type == "unit" or args.type == "all":
        cmd = pytest_cmd + ["tests/unit/"]
        success &= run_command(cmd, "Unit Tests")
    
    if args.type == "integration" or args.type == "all":
        cmd = pytest_cmd + ["tests/integration/"]
        success &= run_command(cmd, "Integration Tests")
    
    if args.type == "e2e" or args.type == "all":
        cmd = pytest_cmd + ["tests/e2e/"]
        success &= run_command(cmd, "End-to-End Tests")
    
    # Run linting and type checking
    if args.type == "all":
        print(f"\n{'='*60}")
        print("Running Code Quality Checks")
        print(f"{'='*60}")
        
        # Black formatting check
        black_cmd = ["python", "-m", "black", "--check", "app/", "tests/"]
        success &= run_command(black_cmd, "Black Formatting Check")
        
        # isort import sorting check
        isort_cmd = ["python", "-m", "isort", "--check-only", "app/", "tests/"]
        success &= run_command(isort_cmd, "isort Import Sorting Check")
        
        # Flake8 linting
        flake8_cmd = ["python", "-m", "flake8", "app/", "tests/"]
        success &= run_command(flake8_cmd, "Flake8 Linting")
        
        # MyPy type checking
        mypy_cmd = ["python", "-m", "mypy", "app/"]
        success &= run_command(mypy_cmd, "MyPy Type Checking")
    
    if success:
        print(f"\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()