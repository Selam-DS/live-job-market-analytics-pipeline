import os
import time
import sqlite3
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

DB_PATH = Path("data/database/jobs.db")

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

ROLES = [
    "data analyst",
    "business analyst",
    "data scientist",
    "bi analyst",
    "data engineer",
    "analytics analyst"
]

def collect_adzuna_jobs():
    if not APP_ID or not APP_KEY:
        raise ValueError("Missing ADZUNA_APP_ID or ADZUNA_APP_KEY in .env file.")

    all_jobs = []

    for role in ROLES:
        for page in range(1, 6):
            url = f"https://api.adzuna.com/v1/api/jobs/ca/search/{page}"

            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "what": role,
                "results_per_page": 50,
                "content-type": "application/json"
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            for job in data.get("results", []):
                all_jobs.append({
                    "job_id": f"adzuna_{job.get('id')}",
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "category": job.get("category", {}).get("label"),
                    "job_type": job.get("contract_type"),
                    "publication_date": job.get("created"),
                    "salary": f"{job.get('salary_min')} - {job.get('salary_max')}",
                    "description": job.get("description"),
                    "url": job.get("redirect_url"),
                    "source": "Adzuna"
                })

            time.sleep(1)

    return all_jobs

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
        "Adzuna"
    ))

    conn.commit()
    conn.close()

    print(f"Collected {len(jobs)} jobs from Adzuna.")
    print(f"Inserted {inserted} new jobs.")

if __name__ == "__main__":
    jobs = collect_adzuna_jobs()
    insert_jobs(jobs)