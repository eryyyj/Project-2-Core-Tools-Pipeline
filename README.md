# Project-2-Core-Tools-Pipeline
This repository is about my compliance on week 2 deliverables

An end-to-end ELT (Extract, Load, Transform) data pipeline engineered using standard Shell scripting, Apache PySpark, Pandas, and PostgreSQL. This project demonstrates foundational data engineering practices including infrastructure containerization, explicit schema enforcement, staging database implementation, and robust data cleaning.

---

## Project Structure

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

# Local Database Deployment
```text
docker run --name bootcamp-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=bootcamp \
  -p 5432:5432 \
  -d postgres:latest
```

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

## Pandas Data Cleaning
```text
python src/clean_data.py
```

### How to Execute the SQL Queries

Because this pipeline uses a local PostgreSQL database container, you need a SQL client (like DBeaver or VS Code Database extensions) to view the analytical results. 

**Prerequisite:** Ensure your database container is running and you have successfully executed `clean_data.py` so the `staging_clean` table exists.

#### Option A: Using DBeaver (Recommended)
1. Open **DBeaver** and connect to the local `bootcamp` database (`localhost:5432`).
2. Go to **File** > **Open File...** and select `sql/analytics.sql` from this repository.
3. In the top toolbar of the SQL Editor, ensure the **Active DataSource** is set to your `postgres` connection and the `bootcamp` database.
4. Click inside any of the 5 query blocks and press **`Ctrl + Enter`** (Windows/Linux) or **`Cmd + Enter`** (Mac) to execute that specific query.
5. The results will populate in the data grid at the bottom of the screen.

#### Option B: Using VS Code (With Database Extension)
1. Ensure you have a SQL extension installed (e.g., *PostgreSQL* or *SQLTools*).
2. Create a new connection to `localhost:5432` (User: `postgres`, Password: `postgres`, Database: `bootcamp`).
3. Open `sql/analytics.sql` directly inside VS Code.
4. Highlight the query block you wish to run and click **"▷ Run on active connection"** (or use the extension's specific shortcut).
5. The results will appear in a split-pane view on the right side of your editor.
