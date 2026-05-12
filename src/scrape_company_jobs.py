import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/database/jobs.db")

URL = "https://www.python.org/jobs/"

def scrape_python_jobs():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    listings = soup.select(".list-recent-jobs li")

    for job in listings:
        title_tag = job.select_one("h2 a")
        company_tag = job.select_one(".listing-company-name")
        location_tag = job.select_one(".listing-location")

        if title_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.python.org" + title_tag.get("href")

            company = company_tag.get_text(" ", strip=True) if company_tag else "Unknown"
            location = location_tag.get_text(" ", strip=True) if location_tag else "Unknown"

            jobs.append({
                "job_id": f"pythonorg_{title.lower().replace(' ', '_')[:50]}",
                "title": title,
                "company": company,
                "location": location,
                "category": "Technology",
                "job_type": None,
                "publication_date": None,
                "salary": None,
                "description": title,
                "url": link,
                "source": "Python.org Scrape"
            })

    return jobs

def insert_jobs(jobs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    collected_at = datetime.now().isoformat()
    inserted = 0

    for job in jobs:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs_raw (
                job_id,
                title,
                company,
                location,
                category,
                job_type,
                publication_date,
                salary,
                description,
                url,
                source,
                collected_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["job_id"],
            job["title"],
            job["company"],
            job["location"],
            job["category"],
            job["job_type"],
            job["publication_date"],
            job["salary"],
            job["description"],
            job["url"],
            job["source"],
            collected_at
        ))

        if cursor.rowcount > 0:
            inserted += 1

    cursor.execute("""
        INSERT INTO pipeline_runs (
            run_time,
            records_collected,
            source
        )
        VALUES (?, ?, ?)
    """, (
        collected_at,
        inserted,
        "Python.org Scrape"
    ))

    conn.commit()
    conn.close()

    print(f"Scraped {len(jobs)} jobs.")
    print(f"Inserted {inserted} new jobs.")

if __name__ == "__main__":
    jobs = scrape_python_jobs()
    insert_jobs(jobs)