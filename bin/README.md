# Bin Directory

This directory contains utility scripts for the Myanmar Geo Coder project.

## Test Runner Scripts

### `run_tests.py`

A comprehensive Python test runner script that provides various options for running tests.

#### Usage

```bash
# Run all tests
python bin/run_tests.py

# Run with verbose output
python bin/run_tests.py --verbose

# Run with coverage report
python bin/run_tests.py --coverage

# Run specific test file
python bin/run_tests.py --file test_geo_coding.py

# Run linting checks
python bin/run_tests.py --lint

# Run type checking
python bin/run_tests.py --type-check

# Run everything (tests, linting, type checking)
python bin/run_tests.py --all

# Install dependencies and run tests
python bin/run_tests.py --install-deps --all

# Pass additional pytest arguments
python bin/run_tests.py -- -x --tb=short
```

#### Options

- `--verbose, -v`: Run tests with verbose output
- `--coverage, -c`: Run tests with coverage report
- `--file, -f`: Run specific test file
- `--lint, -l`: Run code linting checks (black, isort)
- `--type-check, -t`: Run type checking with mypy
- `--all, -a`: Run tests, linting, and type checking
- `--install-deps`: Install test dependencies before running tests
- `pytest_args`: Additional arguments to pass to pytest

### `run_tests.sh`

A simple shell script wrapper for the Python test runner. This script automatically changes to the project root directory before running tests.

#### Usage

```bash
# Run all tests
./bin/run_tests.sh

# Run with any options
./bin/run_tests.sh --verbose --coverage
```

## Examples

### Basic Test Run
```bash
python bin/run_tests.py
```

### Full Quality Check
```bash
python bin/run_tests.py --all --coverage
```

### Development Workflow
```bash
# Install dependencies and run full check
python bin/run_tests.py --install-deps --all --coverage
```

### Debugging Tests
```bash
# Run specific test with verbose output
python bin/run_tests.py --file test_geo_coding.py --verbose

# Run with pytest debugging options
python bin/run_tests.py -- -x --tb=long --pdb
```

## Requirements

The test runner requires the following packages (installed via `requirements.txt`):
- pytest
- pytest-cov (for coverage)
- black (for linting)
- isort (for import sorting)
- mypy (for type checking)

## Output

The script provides clear output with:
- Command being executed
- Test results
- Coverage reports (if enabled)
- Linting results
- Type checking results
- Overall success/failure status 