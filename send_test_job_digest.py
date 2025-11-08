#!/usr/bin/env python3
"""
Script to send a test job digest email using SendGrid
"""

import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

# Email configuration
FROM_EMAIL = "aaduraleke@aol.com"
TO_EMAIL = "aaduraleke@aol.com"
SMTP_HOST = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USER = "apikey"
SMTP_PASS = os.getenv("SENDGRID_API_KEY")

# Check if API key is set
if SMTP_PASS is None:
    raise ValueError("SENDGRID_API_KEY environment variable not set")

def build_test_html():
    html = f"<h2>Worldwide Remote DevOps Jobs — {datetime.utcnow().strftime('%Y-%m-%d')}</h2>"
    html += "<p><em>This is a test email to confirm SendGrid integration is working.</em></p>"
    html += "<table border=1 cellspacing=0 cellpadding=4>"
    html += "<tr><th>Company</th><th>Job Title / Link</th><th>Keywords</th><th>Skills</th></tr>"
    html += "<tr><td>Test Company</td><td><a href='https://example.com'>Test DevOps Engineer - Remote</a></td><td>remote, devops</td><td>AWS, Docker</td></tr>"
    html += "</table>"
    html += "<p><em>Note: The job scraper is working, but many sites are blocking automated access. Consider checking sites manually.</em></p>"
    return html

def send_email(html):
    # Check if API key is set
    if SMTP_PASS is None:
        print("Error: SENDGRID_API_KEY environment variable not set")
        return False
        
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Daily Worldwide Remote DevOps Job Digest - Test Email"
    msg.add_alternative(html, subtype="html")
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print("Test job digest email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main():
    print("Building test job digest...")
    html = build_test_html()
    
    print("Sending test job digest email...")
    success = send_email(html)
    
    if success:
        print("Test email sent successfully! Check your inbox.")
    else:
        print("Failed to send test email. Please check the error above.")

if __name__ == "__main__":
    main()