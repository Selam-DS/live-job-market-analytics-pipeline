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

    remote_keywords = [
        "remote",
        "work from home",
        "wfh",
        "virtual",
        "distributed",
        "remote-first",
        "fully remote",
        "anywhere",
        "telecommute"
    ]

    hybrid_keywords = [
        "hybrid"
    ]

    onsite_keywords = [
        "on-site",
        "onsite",
        "in office",
        "office-based"
    ]

    if any(keyword in text for keyword in remote_keywords):
        return "Remote"

    elif any(keyword in text for keyword in hybrid_keywords):
        return "Hybrid"

    elif any(keyword in text for keyword in onsite_keywords):
        return "On-site"

    else:
        return "Not Specified"


def main():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        "SELECT * FROM jobs_raw",
        conn
    )

    conn.close()

    # ----------------------------
    # Clean raw text
    # ----------------------------

    df["title_clean"] = (
        df["title"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["company_clean"] = (
        df["company"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["location_clean"] = (
        df["location"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["description_clean"] = (
        df["description"]
        .fillna("")
        .apply(clean_text)
    )

    # ----------------------------
    # Standardized categories
    # ----------------------------

    df["role_category"] = (
        df["title_clean"]
        .apply(standardize_role)
    )

    df["remote_type"] = (
        df["title_clean"] + " " +
        df["location_clean"] + " " +
        df["description_clean"]
    ).apply(remote_type)

    # ----------------------------
    # Missing values
    # ----------------------------

    df["salary"] = (
        df["salary"]
        .fillna("Not Provided")
    )

    df["job_type"] = (
        df["job_type"]
        .fillna("Not Specified")
    )

    # ----------------------------
    # Dates
    # ----------------------------

    df["publication_date"] = pd.to_datetime(
        df["publication_date"],
        errors="coerce"
    )

    # ----------------------------
    # Remove duplicates
    # ----------------------------

    df = df.drop_duplicates(
        subset=[
            "title_clean",
            "company_clean",
            "location_clean"
        ],
        keep="first"
    )

    # ----------------------------
    # Remove invalid rows
    # ----------------------------

    df = df.dropna(
        subset=["title_clean"]
    )

    df = df[
        df["title_clean"].str.strip() != ""
    ]

    # ----------------------------
    # Dashboard-safe columns only
    # ----------------------------

    dashboard_columns = [
        "job_id",
        "title_clean",
        "company_clean",
        "location_clean",
        "role_category",
        "remote_type",
        "source",
        "category",
        "job_type",
        "publication_date",
        "salary",
        "url",
        "collected_at"
    ]

    dashboard_df = df[dashboard_columns].copy()

    # ----------------------------
    # Save cleaned dataset
    # ----------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dashboard_df.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8"
    )

    print(f"Cleaned jobs saved to {OUTPUT_PATH}")
    print(f"Rows after cleaning: {len(dashboard_df)}")


if __name__ == "__main__":
    main()