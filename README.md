# Project-2-Core-Tools-Pipeline
This repository contains my compliance for the Week 2 deliverables.

An end-to-end ELT (Extract, Load, Transform) data pipeline engineered using standard Shell scripting, Apache PySpark, Pandas, and PostgreSQL. This project demonstrates foundational data engineering practices including infrastructure containerization, explicit schema enforcement, staging database implementation, and robust data cleaning.


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
│   ├── clean_data.py           # Phase 3: Pandas database transformation script
│   └── testings.py             # Pytest suite for cleaning operations
│
├── sql/
│   └── analytics.sql           # Phase 4: Analytical SQL queries and insights
│
├── docker-compose.yml          # Multi-container orchestration (App + Database)
├── Dockerfile                  # Pipeline execution environment blueprint
├── .gitignore                  # Protection rules preventing binary/massive file leaks
├── README.md                   # Project blueprint and execution manual
└── requirements.txt            # Python ecosystem dependencies

```

## System Prerequisites & Infrastructure Setup

This pipeline is fully containerized. You do not need to install Python, Java, or PostgreSQL locally on your machine. You only need **Docker** and **Docker Compose** installed.

### 1. Build and Launch the Environment

Run the following command in the root directory to spin up the PostgreSQL database and the Python/PySpark execution environment simultaneously:

```bash
docker-compose up -d --build

```

* **Database Service (`db`):** Hosts the PostgreSQL `bootcamp` database mapped to `localhost:5432`.
* **Application Service (`app`):** Runs an isolated container (`bootcamp-pipeline-app`) with Python, Java, PySpark, and Pandas installed.

---

## Data Pipeline Execution Guide

Because the pipeline relies on the containerized environment, all scripts must be executed *inside* the running application container using `docker exec`.

### Phase 1: Data Ingestion

Downloads the remote structured dataset through a raw-text boundary.

```bash
docker exec -it bootcamp-pipeline-app bash scripts/download_data.sh

```

### Phase 2: PySpark Staging Integration

Reads the downloaded CSV and strictly enforces the schema before loading it into the Postgres `staging_raw` table.

```bash
docker exec -it bootcamp-pipeline-app python src/load_data.py

```

### Phase 3: Pandas Data Cleaning

Extracts data from the raw table, applies deduplication, handles nulls, formats dates, and loads it into the `staging_clean` table.

```bash
docker exec -it bootcamp-pipeline-app python src/clean_data.py

```

### Phase 4: Unit Testing (Stretch Goal)

Runs Pytest to validate that the Pandas text and null-cleaning logic performs exactly as expected.

```bash
docker exec -it bootcamp-pipeline-app pytest src/testings.py

```

---

## Phase 5: Analytical SQL Execution

Because this pipeline maps the containerized PostgreSQL database directly to your host machine's port, you can use any local SQL client to view the analytical results.

**Prerequisite:** Ensure the `docker-compose` environment is running and you have successfully executed Phase 3 (`clean_data.py`) so the `staging_clean` table exists.

#### Option A: Using DBeaver (Recommended)

1. Open **DBeaver** and connect to the local `bootcamp` database (`localhost:5432` | User: `postgres` | Password: `postgres`).
2. Go to **File** > **Open File...** and select `sql/analytics.sql` from this repository.
3. In the top toolbar of the SQL Editor, ensure the **Active DataSource** is set to your `postgres` connection and the `bootcamp` database.
4. Click inside any of the query blocks and press **`Ctrl + Enter`** (Windows/Linux) or **`Cmd + Enter`** (Mac) to execute that specific query.
5. The results will populate in the data grid at the bottom of the screen.

#### Option B: Using VS Code (With Database Extension)

1. Ensure you have a SQL extension installed (e.g., *PostgreSQL* or *SQLTools*).
2. Create a new connection to `localhost:5432` (User: `postgres`, Password: `postgres`, Database: `bootcamp`).
3. Open `sql/analytics.sql` directly inside VS Code.
4. Highlight the query block you wish to run and click **"▷ Run on active connection"**.
5. The results will appear in a split-pane view on the right side of your editor.

---

## Environment Teardown

When you are finished running the pipeline and analyzing the data, you can safely shut down the containers and clean up your Docker network by running:

```bash
docker-compose down

```