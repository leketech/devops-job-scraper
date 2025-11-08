#!/bin/bash

# DevOps Job Scraper Setup Script for WSL

echo "Setting up DevOps Job Scraper in WSL..."

# Update package lists
echo "Updating package lists..."
sudo apt update

# Install Python and pip if not already installed
echo "Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install project dependencies
echo "Installing project dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To run the scraper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Set your SendGrid API key: export SENDGRID_API_KEY='your-api-key'"
echo "3. Run the scraper: python devops_job_scraper.py"
echo ""
echo "To deactivate the virtual environment: deactivate"