#!/usr/bin/env python3
"""
Simple script to test SendGrid email functionality
"""

import smtplib
from email.message import EmailMessage
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

def send_test_email():
    # Check if API key is set
    if SMTP_PASS is None:
        print("Error: SENDGRID_API_KEY environment variable not set")
        return False
        
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Test Email from DevOps Job Scraper"
    msg.set_content("This is a test email to confirm that SendGrid is working correctly.")
    
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print("Test email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    print("Sending test email...")
    success = send_test_email()
    if success:
        print("Email functionality is working correctly!")
    else:
        print("Email functionality is not working. Please check the error above.")