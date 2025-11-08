#!/bin/bash

# Script to trigger the GitHub Actions workflow manually
# This requires GitHub CLI to be installed

echo "Checking if GitHub CLI is installed..."
if ! command -v gh &> /dev/null
then
    echo "GitHub CLI could not be found"
    echo "Please install it from: https://cli.github.com/"
    echo "Or trigger the workflow manually from GitHub Actions page"
    exit 1
fi

echo "GitHub CLI found. Triggering workflow..."

# Trigger the workflow
gh workflow run "Daily Remote DevOps Scraper" --repo "$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')"

echo "Workflow triggered successfully!"
echo "Check your GitHub Actions page to see the progress."