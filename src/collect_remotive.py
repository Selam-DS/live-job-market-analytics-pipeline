import requests
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/database/jobs.db")

def collect_remotive_jobs():
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    jobs = data.get("jobs", [])

    return jobs

def insert_jobs(jobs):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    collected_at = datetime.now().isoformat()
    inserted = 0

    for job in jobs:
        job_id = f"remotive_{job.get('id')}"

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
            job_id,
            job.get("title"),
            job.get("company_name"),
            job.get("candidate_required_location"),
            job.get("category"),
            job.get("job_type"),
            job.get("publication_date"),
            job.get("salary"),
            job.get("description"),
            job.get("url"),
            "Remotive",
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
        "Remotive"
    ))

    conn.commit()
    conn.close()

    print(f"Collected {len(jobs)} jobs.")
    print(f"Inserted {inserted} new jobs.")

if __name__ == "__main__":
    jobs = collect_remotive_jobs()
    insert_jobs(jobs)