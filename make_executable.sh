#!/bin/bash

# Script to make all shell scripts executable
# This should be run in WSL

echo "Making shell scripts executable..."

chmod +x setup_wsl.sh
chmod +x run_scraper.sh
chmod +x trigger_workflow.sh
chmod +x wsl_migration_helper.sh
chmod +x wsl_check_setup.sh

echo "All shell scripts are now executable!"
echo "You can now run:"
echo "  ./setup_wsl.sh        # To set up the environment"
echo "  ./run_scraper.sh      # To run the scraper"
echo "  ./trigger_workflow.sh # To trigger GitHub workflow (requires GitHub CLI)"
echo "  ./wsl_check_setup.sh  # To check if everything is set up correctly"