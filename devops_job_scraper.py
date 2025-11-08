#!/usr/bin/env python3
"""
Daily worldwide remote DevOps job scraper + emailer
"""

import requests
import smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage
from datetime import datetime
from urllib.parse import urljoin
from typing import Optional
import os
import time

# === CONFIG ===
# Email configuration for SendGrid
# SMTP_USER must be "apikey" for SendGrid
# SMTP_PASS should be set via environment variable SENDGRID_API_KEY
JOB_SITES = {
    "FeedCoyote": "https://feedcoyote.com/jobs?search=devops",
    "JustRemote": "https://justremote.co/remote-devops-jobs",
    "Himalayas": "https://himalayas.app/jobs?search=devops",
    "Wellfound": "https://wellfound.com/role/devops-engineer",
    "WorkingNomads": "https://www.workingnomads.com/jobs?category=devops",
    "JobBoardSearch": "https://jobboardsearch.com/?s=devops",
    "Remotive": "https://remotive.com/remote-jobs/devops",
    "WeWorkRemotely": "https://weworkremotely.com/remote-jobs/search?term=devops",
    "RemoteOK": "https://remoteok.com/remote-devops-jobs",
    "FlexJobs": "https://www.flexjobs.com/search?search=devops&location=remote",
    "Remote.co": "https://remote.co/remote-jobs/devops/",
    "EuropeRemotely": "https://europeremotely.com/jobs",
    "Jobspresso": "https://jobspresso.co/?s=devops",
    "DynamiteJobs": "https://dynamitejobs.com/jobs?search=devops",
    "NoDesk": "https://nodesk.co/remote-jobs/devops/",
    "Outsourcely": "https://www.outsourcely.com/remote-devops-jobs",
    "Arc": "https://arc.dev/remote-jobs/devops-engineer",
    "Lemon": "https://lemon.io/for-developers/",
}

FROM_EMAIL = "noreply@example.com"
TO_EMAIL = "aaduraleke@aol.com"

SMTP_HOST = "smtp.sendgrid.net"
SMTP_PORT = 587
SMTP_USER = "apikey"   # literal string "apikey" for SendGrid
SMTP_PASS: Optional[str] = None       # set via environment SENDGRID_API_KEY

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}


def scrape_site(name, url):
    jobs = []
    r = None
    # Try up to 3 times with a small delay between attempts
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            break  # Success, break out of retry loop
        except requests.exceptions.Timeout:
            print(f"[{name}] request timed out (attempt {attempt + 1}/3)")
            if attempt < 2:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except requests.exceptions.ConnectionError:
            print(f"[{name}] connection error (attempt {attempt + 1}/3)")
            if attempt < 2:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except requests.exceptions.RequestException as e:
            # Check if we have a response object to access status code
            if e.response is not None and hasattr(e.response, 'status_code') and e.response.status_code == 403:
                print(f"[{name}] access forbidden (403) - site may be blocking automated requests")
                break  # Don't retry on 403
            else:
                print(f"[{name}] request failed (attempt {attempt + 1}/3):", e)
                if attempt < 2:  # Don't sleep on the last attempt
                    time.sleep(2 ** attempt)  # Exponential backoff
            continue
        except Exception as e:
            print(f"[{name}] unexpected error (attempt {attempt + 1}/3):", e)
            if attempt < 2:  # Don't sleep on the last attempt
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
    else:
        # All attempts failed
        return jobs
    
    # Check if we have a successful response
    if r is None:
        return jobs
        
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        href = urljoin(url, str(a["href"]))
        if any(k in text.lower() for k in ["devops", "sre", "infrastructure", "site reliability"]):
            # Check if job is explicitly tagged as remote/worldwide
            if any(tag in text.lower() for tag in ["work from anywhere", "worldwide remote"]):
                jobs.append({
                    "company": name,
                    "title": text.strip()[:150],
                    "link": href
                })
    print(f"[{name}] found {len(jobs)} jobs")
    return jobs

    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        href = urljoin(url, str(a["href"]))
        if any(k in text.lower() for k in ["devops", "sre", "infrastructure", "site reliability"]):
            # Check if job is explicitly tagged as remote/worldwide
            if any(tag in text.lower() for tag in ["work from anywhere", "worldwide remote"]):
                jobs.append({
                    "company": name,
                    "title": text.strip()[:150],
                    "link": href
                })
    print(f"[{name}] found {len(jobs)} jobs")
    return jobs


def infer_keywords_and_skills(title):
    keywords = ["remote", "worldwide", "devops", "infrastructure", "automation"]
    skills = ["AWS", "Terraform", "Kubernetes", "Docker", "CI/CD"]
    return keywords, skills


def build_html(jobs):
    html = f"<h2>Worldwide Remote DevOps Jobs — {datetime.utcnow().strftime('%Y-%m-%d')}</h2>"
    html += "<table border=1 cellspacing=0 cellpadding=4>"
    html += "<tr><th>Company</th><th>Job Title / Link</th><th>Keywords</th><th>Skills</th></tr>"
    for j in jobs:
        kw, sk = infer_keywords_and_skills(j["title"])
        html += (
            f"<tr><td>{j['company']}</td>"
            f"<td><a href='{j['link']}'>{j['title']}</a></td>"
            f"<td>{', '.join(kw)}</td>"
            f"<td>{', '.join(sk)}</td></tr>"
        )
    html += "</table>"
    return html


def send_email(html, job_count=0):
    # If no SMTP password is set, don't try to send email
    if SMTP_PASS is None:
        print("No SendGrid API key set. Skipping email send.")
        return
        
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    
    # Customize subject based on job count
    if job_count > 0:
        msg["Subject"] = f"Daily Worldwide Remote DevOps Job Digest - {job_count} jobs found"
    else:
        msg["Subject"] = "Daily Worldwide Remote DevOps Job Digest - No jobs found today"
        
    msg.add_alternative(html, subtype="html")

    try:
        # Small delay to ensure proper connection
        time.sleep(1)
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            if SMTP_PASS is not None:
                s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
        print("Email sent to", TO_EMAIL)
    except Exception as e:
        print(f"Failed to send email: {e}")
        print("This could be due to:")
        print("1. Incorrect SendGrid API key")
        print("2. Network connectivity issues")
        print("3. SendGrid service temporary issues")
        print("4. Incorrect SMTP configuration")
        print("Continuing with script execution...")


def main():
    all_jobs = []
    for name, url in JOB_SITES.items():
        all_jobs.extend(scrape_site(name, url))
    print(f"Total jobs found: {len(all_jobs)}")
    if not all_jobs:
        html = "<p>No DevOps jobs found today.</p><p>Note: Many job sites may block automated scraping. Consider checking the sites manually or adjusting the scraping approach.</p>"
    else:
        html = build_html(all_jobs)
    try:
        send_email(html, len(all_jobs))
    except Exception as e:
        print(f"Email function failed: {e}")
    print("Script completed successfully (email may have failed, but scraping completed).")


if __name__ == "__main__":
    import os
    SMTP_PASS = os.getenv("SENDGRID_API_KEY")
    if SMTP_PASS is None:
        print("Warning: SENDGRID_API_KEY environment variable not set. Email will not be sent.")
    else:
        print("SENDGRID_API_KEY is set. Email functionality enabled.")
    main()