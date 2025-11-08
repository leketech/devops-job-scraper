# WSL Setup Guide for DevOps Job Scraper

## Prerequisites

1. WSL2 with Ubuntu installed
2. GitHub account with the repository forked/cloned
3. SendGrid API key added to GitHub Secrets

## Moving Project to WSL

For better performance, move the project from Windows filesystem to WSL filesystem:

```bash
# Copy from Windows to WSL filesystem
cp -r /mnt/c/Users/Leke/devops-scraper ~/devops-scraper

# Navigate to the project directory
cd ~/devops-scraper/devops-job-scraper
```

## Setting Up the Environment

1. Make scripts executable:
   ```bash
   chmod +x setup_wsl.sh
   chmod +x run_scraper.sh
   chmod +x trigger_workflow.sh
   chmod +x wsl_migration_helper.sh
   ```

2. Run the setup script:
   ```bash
   ./setup_wsl.sh
   ```

## Triggering the GitHub Workflow

You have two options to trigger the workflow:

### Option 1: Using GitHub CLI (Recommended)

1. Install GitHub CLI:
   ```bash
   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
   sudo apt update
   sudo apt install gh
   ```

2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

3. Trigger the workflow:
   ```bash
   ./trigger_workflow.sh
   ```

### Option 2: Manual Trigger

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Daily Remote DevOps Scraper" workflow
4. Click "Run workflow" button
5. Confirm by clicking "Run workflow" in the dropdown

## Running the Scraper Locally

To run the scraper locally in WSL:

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Set your SendGrid API key:
   ```bash
   export SENDGRID_API_KEY='your-sendgrid-api-key'
   ```

3. Run the scraper:
   ```bash
   python devops_job_scraper.py
   ```

Or simply use the provided script:
```bash
./run_scraper.sh
```

## Development Workflow in WSL

1. Make changes to the code in WSL
2. Test locally using the run_scraper.sh script
3. Commit and push changes to GitHub
4. Optionally trigger the workflow manually to test