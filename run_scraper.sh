#!/bin/bash

# Run DevOps Job Scraper

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run setup_wsl.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if SENDGRID_API_KEY is set
if [ -z "$SENDGRID_API_KEY" ]; then
    echo "SENDGRID_API_KEY environment variable not set."
    echo "Please set it with: export SENDGRID_API_KEY='your-api-key'"
    exit 1
fi

# Run the scraper
echo "Running DevOps Job Scraper..."
python devops_job_scraper.py

echo "Scraping complete!"