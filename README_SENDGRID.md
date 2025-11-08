# SendGrid Configuration

To use the email functionality, you need to set your SendGrid API key as an environment variable.

## Setting the SendGrid API Key

### On Windows (Command Prompt):
```cmd
set SENDGRID_API_KEY=your-sendgrid-api-key-here
```

### On Windows (PowerShell):
```powershell
$env:SENDGRID_API_KEY="your-sendgrid-api-key-here"
```

### On Linux/macOS/WSL:
```bash
export SENDGRID_API_KEY="your-sendgrid-api-key-here"
```

## Running the Scripts

After setting the environment variable, you can run any of the scripts:

1. **Main job scraper**: `python devops_job_scraper.py`
2. **Test email**: `python test_email.py`
3. **Test job digest**: `python send_test_job_digest.py`

## Security Note

Never commit your SendGrid API key to version control. The scripts are designed to read the key from environment variables to prevent accidental exposure.