#!/bin/bash
# Simple wrapper script for running tests
# This script makes it easy to run tests from any directory

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root directory
cd "$PROJECT_ROOT"

# Run the Python test script with all arguments passed to it
python3 "$SCRIPT_DIR/run_tests.py" "$@" 
