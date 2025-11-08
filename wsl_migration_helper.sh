#!/bin/bash

# WSL Migration Helper Script
# Helps move the project to WSL filesystem for better performance

echo "WSL Migration Helper"
echo "===================="

# Get the current directory (Windows path)
WINDOWS_PATH=$(pwd)
echo "Current Windows path: $WINDOWS_PATH"

# Suggest moving to WSL home directory
WSL_HOME="/home/$(whoami)/devops-job-scraper"
echo "Suggested WSL path: $WSL_HOME"

echo ""
echo "To move this project to WSL:"
echo "1. Copy the project files to WSL:"
echo "   cp -r '$WINDOWS_PATH' '$WSL_HOME'"
echo ""
echo "2. Navigate to the WSL directory:"
echo "   cd $WSL_HOME"
echo ""
echo "3. Run the setup script:"
echo "   ./setup_wsl.sh"
echo ""
echo "4. Run the scraper:"
echo "   ./run_scraper.sh"
echo ""
echo "Note: Running Python projects from Windows filesystem in WSL"
echo "can be slower due to file system translation. It's recommended"
echo "to keep and run Python projects in the WSL filesystem."