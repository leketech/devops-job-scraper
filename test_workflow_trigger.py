#!/usr/bin/env python3
"""
Script to test triggering GitHub Actions workflow using GitHub API
This is an alternative method to trigger the workflow manually
"""

import requests
import os
import json

def trigger_workflow():
    # Get repository information from git
    try:
        # Get repository owner and name from remote URL
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, cwd='.')
        remote_url = result.stdout.strip()
        
        # Extract owner/repo from URL
        # Handle both https://github.com/owner/repo.git and git@github.com:owner/repo.git
        if 'github.com/' in remote_url:
            repo_path = remote_url.split('github.com/')[-1].replace('.git', '')
        elif 'github.com:' in remote_url:
            repo_path = remote_url.split('github.com:')[-1].replace('.git', '')
        else:
            print("Could not parse repository URL")
            return False
            
        owner, repo = repo_path.split('/')
        print(f"Repository: {owner}/{repo}")
        
    except Exception as e:
        print(f"Error getting repository info: {e}")
        return False

    # GitHub API endpoint for triggering workflow
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/daily_job_scraper.yml/dispatches"
    
    # Get GitHub token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("GITHUB_TOKEN environment variable not set")
        print("Please create a personal access token with 'repo' scope and set it:")
        print("export GITHUB_TOKEN='your-github-token'")
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
        print("Success! Check your GitHub Actions page to see the progress.")
    else:
        print("Failed to trigger workflow. Please check the error messages above.")