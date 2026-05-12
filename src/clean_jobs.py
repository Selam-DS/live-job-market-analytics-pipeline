import sqlite3
import pandas as pd
import re
from pathlib import Path

DB_PATH = Path("data/database/jobs.db")
OUTPUT_PATH = Path("data/processed/jobs_cleaned.csv")

def clean_text(text):
    if pd.isna(text):
        return ""

    text = re.sub(r"<.*?>", " ", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def standardize_role(title):
    title = str(title).lower()

    if "data scientist" in title:
        return "Data Scientist"
    elif "data engineer" in title:
        return "Data Engineer"
    elif "business analyst" in title:
        return "Business Analyst"
    elif "bi analyst" in title or "business intelligence" in title:
        return "BI Analyst"
    elif "machine learning" in title or "ml " in title:
        return "Machine Learning"
    elif "data analyst" in title or "analyst" in title:
        return "Data Analyst"
    else:
        return "Other"

def remote_type(text):
    text = str(text).lower()

    if "remote" in text:
        return "Remote"
    elif "hybrid" in text:
        return "Hybrid"
    elif "on-site" in text or "onsite" in text:
        return "On-site"
    else:
        return "Not specified"

def main():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("SELECT * FROM jobs_raw", conn)

    conn.close()

    df["description_clean"] = df["description"].apply(clean_text)
    df["title_clean"] = df["title"].str.strip()
    df["company_clean"] = df["company"].fillna("Unknown").str.strip()
    df["location_clean"] = df["location"].fillna("Unknown").str.strip()

    df["publication_date"] = pd.to_datetime(
        df["publication_date"],
        errors="coerce"
    )

    df["role_category"] = df["title_clean"].apply(standardize_role)

    df["remote_type"] = (
        df["title_clean"].fillna("") + " " +
        df["location_clean"].fillna("") + " " +
        df["description_clean"].fillna("")
    ).apply(remote_type)

    df = df.drop_duplicates(
        subset=["title_clean", "company_clean", "location_clean"],
        keep="first"
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Cleaned jobs saved to {OUTPUT_PATH}")
    print(f"Rows after cleaning: {len(df)}")

if __name__ == "__main__":
    main()