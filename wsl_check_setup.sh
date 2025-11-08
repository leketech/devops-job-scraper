#!/bin/bash

# Script to check if all necessary tools are installed for WSL setup

echo "Checking WSL setup for DevOps Job Scraper..."
echo "=========================================="

# Check if running in WSL
if grep -qE "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo "✓ Running in WSL environment"
else
    echo "⚠ Not running in WSL environment"
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python installed: $PYTHON_VERSION"
else
    echo "✗ Python not installed"
fi

# Check pip
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✓ pip installed: $PIP_VERSION"
else
    echo "✗ pip not installed"
fi

# Check Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "✓ Git installed: $GIT_VERSION"
else
    echo "✗ Git not installed"
fi

# Check if in project directory
if [ -f "devops_job_scraper.py" ] && [ -f "requirements.txt" ]; then
    echo "✓ In project directory"
else
    echo "⚠ Not in project directory"
fi

# Check virtual environment
if [ -d "venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "⚠ Virtual environment not found (run ./setup_wsl.sh to create)"
fi

# Check required files
REQUIRED_FILES=("devops_job_scraper.py" "requirements.txt" "setup_wsl.sh" "run_scraper.sh")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo "✓ All required files present"
else
    echo "✗ Missing files: ${MISSING_FILES[*]}"
fi

# Check GitHub CLI
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version | head -n 1)
    echo "✓ GitHub CLI installed: $GH_VERSION"
else
    echo "⚠ GitHub CLI not installed (needed for workflow triggering)"
fi

echo ""
echo "Setup check complete."
echo "If all checks pass, you're ready to use the DevOps Job Scraper in WSL!"