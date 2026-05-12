import subprocess
from datetime import datetime

PIPELINE_STEPS = [
    ("Collect Remotive Jobs", "src/collect_remotive.py"),
    ("Collect Adzuna Jobs", "src/collect_adzuna.py"),
    ("Scrape Python.org Jobs", "src/scrape_company_jobs.py"),
    ("Clean Job Data", "src/clean_jobs.py"),
    ("Extract Skills", "src/extract_skills.py")
]

def run_script(name, script_path):

    print("\n" + "=" * 60)
    print(f"RUNNING: {name}")
    print("=" * 60)

    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print("ERRORS:")
        print(result.stderr)

    if result.returncode == 0:
        print(f"{name} completed successfully.")
    else:
        print(f"{name} failed.")

def main():

    start = datetime.now()

    print("\nSTARTING JOB MARKET PIPELINE")
    print(f"Start time: {start}")

    for name, script in PIPELINE_STEPS:
        run_script(name, script)

    end = datetime.now()

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)

    print(f"End time: {end}")
    print(f"Duration: {end - start}")

if __name__ == "__main__":
    main()