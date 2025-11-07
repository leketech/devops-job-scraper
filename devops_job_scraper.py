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

# === CONFIG ===
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

HEADERS = {"User-Agent": "Mozilla/5.0 (JobScraper)"}


def scrape_site(name, url):
    jobs = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        print(f"[{name}] request timed out")
        return jobs
    except requests.exceptions.ConnectionError:
        print(f"[{name}] connection error")
        return jobs
    except requests.exceptions.RequestException as e:
        print(f"[{name}] request failed:", e)
        return jobs
    except Exception as e:
        print(f"[{name}] unexpected error:", e)
        return jobs

    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True)
        href = urljoin(url, a["href"])
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


def send_email(html):
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg["Subject"] = "Daily Worldwide Remote DevOps Job Digest"
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        if SMTP_PASS is not None:
            s.login(SMTP_USER, SMTP_PASS)
        s.send_message(msg)
    print("Email sent to", TO_EMAIL)


def main():
    all_jobs = []
    for name, url in JOB_SITES.items():
        all_jobs.extend(scrape_site(name, url))
    if not all_jobs:
        html = "<p>No DevOps jobs found today.</p>"
    else:
        html = build_html(all_jobs)
    send_email(html)


if __name__ == "__main__":
    import os
    SMTP_PASS = os.getenv("SENDGRID_API_KEY")
    main()