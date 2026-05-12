import pandas as pd
from pathlib import Path

INPUT_PATH = Path("data/processed/jobs_cleaned.csv")
OUTPUT_PATH = Path("data/processed/job_skills.csv")
SKILL_COUNTS_PATH = Path("data/processed/skill_counts.csv")

SKILLS = {
    "Programming": ["Python", "R", "SQL", "Java", "JavaScript"],
    "Data Analysis": ["Excel", "Statistics", "A/B Testing", "EDA"],
    "Visualization": ["Tableau", "Power BI", "Looker", "Matplotlib", "Seaborn"],
    "Machine Learning": ["Machine Learning", "Scikit-learn", "TensorFlow", "PyTorch", "XGBoost"],
    "Data Engineering": ["ETL", "Spark", "Airflow", "Snowflake", "BigQuery", "Databricks"],
    "Cloud": ["AWS", "Azure", "GCP"],
    "Tools": ["Git", "Jupyter", "Docker", "SQL Server"]
}

def find_skills(text):
    text_lower = str(text).lower()
    found = []

    for category, skills in SKILLS.items():
        for skill in skills:
            if skill.lower() in text_lower:
                found.append({
                    "skill": skill,
                    "skill_category": category
                })

    return found

def main():
    jobs = pd.read_csv(INPUT_PATH)

    rows = []

    for _, row in jobs.iterrows():
        text = f"{row.get('title_clean', '')} {row.get('description_clean', '')}"
        skills_found = find_skills(text)

        for item in skills_found:
            rows.append({
                "job_id": row["job_id"],
                "title": row["title_clean"],
                "company": row["company_clean"],
                "role_category": row["role_category"],
                "source": row["source"],
                "skill": item["skill"],
                "skill_category": item["skill_category"]
            })

    job_skills = pd.DataFrame(rows)

    job_skills.to_csv(OUTPUT_PATH, index=False)

    skill_counts = (
        job_skills
        .groupby(["skill_category", "skill"])
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    skill_counts.to_csv(SKILL_COUNTS_PATH, index=False)

    print(f"Job skills saved to {OUTPUT_PATH}")
    print(f"Skill counts saved to {SKILL_COUNTS_PATH}")
    print(f"Total skill mentions: {len(job_skills)}")

if __name__ == "__main__":
    main()