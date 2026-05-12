CREATE TABLE IF NOT EXISTS jobs_raw (
    job_id TEXT PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    category TEXT,
    job_type TEXT,
    publication_date TEXT,
    salary TEXT,
    description TEXT,
    url TEXT,
    source TEXT,
    collected_at TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id TEXT,
    skill_id INTEGER,

    FOREIGN KEY(job_id) REFERENCES jobs_raw(job_id),
    FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_time TEXT,
    records_collected INTEGER,
    source TEXT
);
