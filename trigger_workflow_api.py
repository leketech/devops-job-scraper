#!/usr/bin/env python3
"""
Script to trigger GitHub Actions workflow using GitHub API
"""

import requests
import os
import json

def trigger_workflow():
    # Repository information
    owner = "leketech"
    repo = "devops-job-scraper"
    workflow_file = "daily_job_scraper.yml"
    
    # GitHub API endpoint for triggering workflow
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/dispatches"
    
    # Get GitHub token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GITHUB_TOKEN environment variable not set")
        print("Please create a personal access token with 'repo' scope and set it:")
        print("In PowerShell: $env:GITHUB_TOKEN='your-github-token'")
        print("In bash: export GITHUB_TOKEN='your-github-token'")
        return False
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Data to send
    data = {
        'ref': 'main'  # or 'master' depending on your default branch
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 204:
            print("Workflow triggered successfully!")
            print("Check your GitHub Actions page to see the progress:")
            print(f"https://github.com/{owner}/{repo}/actions")
            return True
        else:
            print(f"Failed to trigger workflow: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error triggering workflow: {e}")
        return False

if __name__ == "__main__":
    print("Attempting to trigger GitHub Actions workflow...")
    success = trigger_workflow()
    if success:
        print("\nSuccess! The workflow should start running shortly.")
    else:
        print("\nFailed to trigger workflow. Please check the error messages above.")