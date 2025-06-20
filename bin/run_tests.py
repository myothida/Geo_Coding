#!/usr/bin/env python3
"""
Test runner script for Myanmar Geo Coder project.

This script provides a convenient way to run tests with various options:
- Run all tests
- Run specific test files
- Run with coverage
- Run with verbose output
- Run with different pytest options

Usage:
    python bin/run_tests.py                    # Run all tests
    python bin/run_tests.py --verbose          # Run with verbose output
    python bin/run_tests.py --coverage         # Run with coverage report
    python bin/run_tests.py --file test_file   # Run specific test file
    python bin/run_tests.py --help             # Show help
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    if description:
        print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False
    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}")
        print("Please make sure pytest is installed: pip install pytest")
        return False


def install_dependencies():
    """Install required dependencies for testing."""
    print("Installing test dependencies...")
    requirements_file = get_project_root() / "requirements.txt"
    
    if requirements_file.exists():
        cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
        return run_command(cmd, "Installing dependencies from requirements.txt")
    else:
        print("requirements.txt not found, skipping dependency installation")
        return True


def run_tests(args):
    """Run the tests based on provided arguments."""
    project_root = get_project_root()
    tests_dir = project_root / "tests"
    
    # Change to project root directory
    os.chdir(project_root)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Add test directory
    cmd.append(str(tests_dir))
    
    # Add verbose flag if requested
    if args.verbose:
        cmd.append("-v")
    
    # Add coverage if requested
    if args.coverage:
        cmd.extend(["--cov=mm_geo_coder", "--cov-report=term-missing", "--cov-report=html"])
    
    # Add specific test file if provided
    if args.file:
        test_file = tests_dir / args.file
        if test_file.exists():
            cmd = [sys.executable, "-m", "pytest", str(test_file)]
            if args.verbose:
                cmd.append("-v")
            if args.coverage:
                cmd.extend(["--cov=mm_geo_coder", "--cov-report=term-missing"])
        else:
            print(f"Test file not found: {test_file}")
            return False
    
    # Add additional pytest options
    if args.pytest_args:
        cmd.extend(args.pytest_args)
    
    return run_command(cmd, "Running tests")


def run_linting():
    """Run code linting checks."""
    print("\nRunning code linting...")
    
    # Check if black is available
    try:
        subprocess.run([sys.executable, "-m", "black", "--check", "."], check=True)
        print("✓ Black formatting check passed")
    except subprocess.CalledProcessError:
        print("✗ Black formatting check failed")
        return False
    except FileNotFoundError:
        print("Black not installed, skipping formatting check")
    
    # Check if isort is available
    try:
        subprocess.run([sys.executable, "-m", "isort", "--check-only", "."], check=True)
        print("✓ Import sorting check passed")
    except subprocess.CalledProcessError:
        print("✗ Import sorting check failed")
        return False
    except FileNotFoundError:
        print("isort not installed, skipping import sorting check")
    
    return True


def run_type_checking():
    """Run type checking with mypy."""
    print("\nRunning type checking...")
    
    try:
        cmd = [sys.executable, "-m", "mypy", "mm_geo_coder"]
        subprocess.run(cmd, check=True)
        print("✓ Type checking passed")
        return True
    except subprocess.CalledProcessError:
        print("✗ Type checking failed")
        return False
    except FileNotFoundError:
        print("mypy not installed, skipping type checking")
        return True


def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(
        description="Run tests for Myanmar Geo Coder project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bin/run_tests.py                    # Run all tests
  python bin/run_tests.py --verbose          # Run with verbose output
  python bin/run_tests.py --coverage         # Run with coverage report
  python bin/run_tests.py --file test_geo_coding.py  # Run specific test file
  python bin/run_tests.py --lint             # Run linting checks
  python bin/run_tests.py --type-check       # Run type checking
  python bin/run_tests.py --all              # Run tests, linting, and type checking
        """
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Run tests with verbose output"
    )
    
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Run tests with coverage report"
    )
    
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Run specific test file"
    )
    
    parser.add_argument(
        "--lint", "-l",
        action="store_true",
        help="Run code linting checks"
    )
    
    parser.add_argument(
        "--type-check", "-t",
        action="store_true",
        help="Run type checking with mypy"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run tests, linting, and type checking"
    )
    
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install test dependencies before running tests"
    )
    
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Additional arguments to pass to pytest"
    )
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    success = True
    
    # Run linting if requested
    if args.lint or args.all:
        if not run_linting():
            success = False
    
    # Run type checking if requested
    if args.type_check or args.all:
        if not run_type_checking():
            success = False
    
    # Run tests (unless only linting/type-checking was requested)
    if not (args.lint or args.type_check) or args.all:
        if not run_tests(args):
            success = False
    
    if success:
        print("\n" + "="*60)
        print("✓ All checks passed successfully!")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("✗ Some checks failed!")
        print("="*60)
        sys.exit(1)


if __name__ == "__main__":
    main() 
