# Using WSL with DevOps Job Scraper

This document provides instructions on how to use this project with WSL (Windows Subsystem for Linux).

## Why Use WSL?

WSL provides a full Linux environment on Windows, which offers several advantages for this project:

1. Better performance for Python development
2. Native Linux tools and utilities
3. Consistent environment with the GitHub Actions runner (Ubuntu)
4. Better file system performance for development workflows

## Initial Setup

1. Install WSL2 with Ubuntu:
   ```powershell
   wsl --install
   ```

2. Move the project to the WSL file system (recommended):
   ```bash
   # From Windows CMD/PowerShell
   cd c:\Users\Leke\devops-scraper
   tar -czf devops-job-scraper.tar.gz devops-job-scraper
   
   # In WSL
   mkdir -p ~/projects
   cd ~/projects
   tar -xzf /mnt/c/Users/Leke/devops-scraper/devops-job-scraper.tar.gz
   cd devops-job-scraper
   ```

## Setting Up the Development Environment

1. Make the helper scripts executable:
   ```bash
   chmod +x *.sh
   ```

2. Run the WSL setup script:
   ```bash
   ./setup_wsl.sh
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Running the Scraper

You can run the scraper in two ways:

### Local Execution
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Set your SendGrid API key
export SENDGRID_API_KEY='your-sendgrid-api-key'

# Run the scraper
python devops_job_scraper.py
```

Or use the convenience script:
```bash
./run_scraper.sh
```

### GitHub Actions Workflow
The project includes a GitHub Actions workflow that runs daily. You can trigger it manually:

1. Using GitHub CLI:
   ```bash
   ./trigger_workflow.sh
   ```

2. Using the Python script:
   ```bash
   # Set your GitHub personal access token
   export GITHUB_TOKEN='your-github-token'
   
   # Run the test script
   python test_workflow_trigger.py
   ```

3. Manually from GitHub Actions web interface

## Development Workflow

1. Edit files in WSL using your preferred Linux editor (vim, nano, VS Code with WSL extension, etc.)
2. Test changes locally
3. Commit and push to GitHub
4. Monitor the GitHub Actions workflow for any issues

## Troubleshooting

### Permission Issues
If you encounter permission issues with the shell scripts:
```bash
chmod +x *.sh
```

### Path Issues
If you're still working from the Windows file system (/mnt/c/...), performance may be degraded. It's recommended to copy the files to the WSL file system (~).

### Missing Dependencies
If you encounter missing dependencies:
```bash
pip install -r requirements.txt
```

## Additional Resources

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [GitHub CLI Installation](https://cli.github.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)