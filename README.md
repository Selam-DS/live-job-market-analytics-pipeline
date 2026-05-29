# Live Job Market Analytics Pipeline

## Overview

The Live Job Market Analytics Pipeline is an end-to-end data analytics project that automates the collection, storage, processing, analysis, and visualization of live job market data.

The pipeline gathers job postings from multiple online sources using APIs and web scraping, stores the data in a SQLite database, applies data cleaning and text mining techniques, and delivers actionable labor market insights through interactive Tableau dashboards.

This project demonstrates practical skills in data engineering, analytics, automation, and business intelligence while solving a real-world problem: understanding current job market trends and skill demand.

---

## Business Problem

Job seekers, career changers, and aspiring data professionals often struggle to answer key questions:

* Which technical skills are currently most in demand?
* Which data-related roles have the highest number of openings?
* How common are remote opportunities?
* Which companies are hiring most actively?
* How do skill requirements vary by role?

This project automates the collection and analysis of job posting data to provide data-driven answers to these questions.

---

## Pipeline Architecture

---

## Technology Stack

### Data Collection

* Python
* Requests
* BeautifulSoup
* REST APIs

### Data Storage

* SQLite

### Data Processing

* Pandas
* Regular Expressions
* ETL Pipelines

### Analytics

* Text Mining
* Skill Extraction
* Role Classification

### Visualization

* Tableau Public

### Automation

* Python Workflow Scripts

---

## Data Sources

| Source          | Collection Method |
| --------------- | ----------------- |
| Adzuna          | API               |
| Remotive        | API               |
| Python.org Jobs | Web Scraping      |

---

## Pipeline Workflow

### 1. Data Collection

Live job postings are collected from multiple online sources using APIs and web scraping techniques.

### 2. Data Storage

Raw job postings are stored in a SQLite database to enable reproducible analysis and automated updates.

### 3. Data Cleaning

Job records are standardized and cleaned using Python and Pandas. Missing values, duplicates, inconsistent formatting, and text noise are addressed during this stage.

### 4. Skill Extraction

Natural language processing techniques are applied to job descriptions to identify and extract in-demand technical skills.

### 5. Analytical Dataset Creation

Cleaned datasets are generated for reporting and dashboard development.

### 6. Business Intelligence

Interactive Tableau dashboards visualize labor market trends and skill demand patterns.

---

## Dashboard Overview

### Job Market Overview

This dashboard provides:

* Total jobs collected
* Companies actively hiring
* Remote job availability
* Role distribution
* Hiring source distribution
* Top hiring organizations

---

### Skills Intelligence Dashboard

This dashboard provides:

* Most requested technical skills
* Skill demand by role category
* Skill frequency analysis
* Emerging market trends

---

## Key Insights

The dashboard reveals valuable labor market intelligence including:

* Distribution of Data Analyst, Data Scientist, Data Engineer, and BI roles
* Remote and hybrid work trends
* Most frequently requested technical skills
* Companies with the highest hiring activity
* Relationships between job categories and skill requirements

---

## Project Structure

```text
live-job-market-analytics-pipeline/
│
├── data/
│   ├── database/
│   ├── processed/
│   └── raw/
│
├── dashboard/
│
├── images/
│   ├── job-market-overview.png
│   ├── skills-intelligence.png
│   └── job_market_pipeline_redesign_fixed.png
│
├── notebooks/
│
├── sql/
│   └── create_tables.sql
│
├── src/
│   ├── collect_adzuna.py
│   ├── collect_remotive.py
│   ├── scrape_python_jobs.py
│   ├── clean_jobs.py
│   ├── extract_skills.py
│   ├── database.py
│   └── update_pipeline.py
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/live-job-market-analytics-pipeline.git

cd live-job-market-analytics-pipeline
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Pipeline

Run the complete workflow:

```bash
python3 src/update_pipeline.py
```

The pipeline will:

1. Collect new job postings
2. Update the SQLite database
3. Clean and standardize records
4. Extract technical skills
5. Generate analytical datasets
6. Refresh dashboard-ready outputs

---

## Tableau Dashboard

View the interactive dashboard:

**Tableau Public Dashboard:**
PASTE_TABLEAU_PUBLIC_LINK_HERE

---

## Skills Demonstrated

### Data Engineering

* API Integration
* Web Scraping
* SQLite Database Design
* Automated ETL Pipelines

### Data Analytics

* Data Cleaning
* Feature Engineering
* Exploratory Analysis

### Data Science

* Text Mining
* Skill Extraction
* Labor Market Analysis

### Business Intelligence

* Dashboard Design
* KPI Development
* Interactive Visualizations

### Software Development

* Python Project Structure
* Version Control with Git
* Automation Workflows

---

## Future Enhancements

Potential future improvements include:

* Salary normalization and analysis
* Geographic trend analysis
* Automated dashboard refresh scheduling
* Historical trend tracking
* Machine learning skill-demand forecasting
* Additional job board integrations

---

## Author

**Selam Saleh**

Honours Bachelor of Data Science and Analytics

Passionate about leveraging data, analytics, and technology to solve real-world business problems.
