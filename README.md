# Piper
Auto-detects stack, installs deps, runs tests and generates adaptive CI pipelines.

## Local Development

### Setting up the environment

```bash
# Create virtual environment
python -m venv .venv

#activate virtual environment
source .venv/bin/activate

### Prerequisites
- Python 3.8+
- pre-commit (`pip install pre-commit`)

#run pre-commit checks on all files
pre-commit run --all-files

#scan current directory for project detection
piper scan --root .