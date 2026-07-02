# Project-2-Core-Tools-Pipeline
This repository is about my compliance on week 2 deliverables

An end-to-end ELT (Extract, Load, Transform) data pipeline engineered using standard Shell scripting, Apache PySpark, Pandas, and PostgreSQL. This project demonstrates foundational data engineering practices including infrastructure containerization, explicit schema enforcement, staging database implementation, and robust data cleaning.

---

## 📁 Project Structure

```text
core-tools-pipeline/
│
├── data/
│   └── raw/                    # Downloaded raw CSV datasets (Git-ignored)
│
├── drivers/
│   └── postgresql-42.7.3.jar   # JDBC driver for PySpark-to-PostgreSQL bridge (Git-ignored)
│
├── scripts/
│   └── download_data.sh        # Phase 1: Bash data ingestion script 
│
├── src/
│   ├── load_data.py            # Phase 2: PySpark strict-schema staging loader
│   └── clean_data.py           # Phase 3: Pandas database transformation script
│
├── sql/
│   └── analytics.sql           # Phase 4: Analytical SQL queries and insights
│
├── tests/
│   └── test_cleaning.py        # Phase 5: Pytest suite for cleaning operations
│
├── .gitignore                  # Protection rules preventing binary/massive file leaks
├── README.md                   # Project blueprint and execution manual
└── requirements.txt            # Python ecosystem dependencies
```

Run to initialize the database in your local machine
docker run --name bootcamp-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bootcamp \
  -p 5432:5432 \
  -d postgres:latest

# Initialize and activate isolated workspace
python3 -m venv .venv
source .venv/bin/activate

# Install processing engines, database connectors, and testing frameworks
pip install -r requirements.txt

# Data Pipeline Execution Guide
## Data Ingestion and Fetching
```text
bash scripts/download_data.sh
```
## Pyspark Staging Integration

```text
python src/load_data.py
```