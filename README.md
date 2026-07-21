# Netflix ELT Pipeline: Orchestrated with Apache Airflow & dbt

This repository contains an end-to-end ELT (Extract, Load, Transform) data pipeline engineered for automation. It transitions from a manual execution model to a fully orchestrated workflow using **Apache Airflow**, **Apache PySpark**, **dbt (data build tool)**, and **PostgreSQL**.

This project demonstrates advanced data engineering practices including infrastructure containerization, DAG-based orchestration, idempotency, data quality testing, and analytics engineering.

## 🏗️ Architecture & Tech Stack

* **Orchestration:** Apache Airflow
* **Extraction (Extract):** Bash & Kaggle CLI
* **Data Processing (Load):** Apache PySpark
* **Transformation & Testing (Transform):** dbt (Data Build Tool)
* **Data Warehouse:** PostgreSQL
* **Infrastructure:** Docker & Docker Compose

---

## 📂 Project Structure

```text
Project-2-Core-Tools-Pipeline/
│
├── dags/
│   └── data_pipeline.py            # Airflow DAG definition and task ordering
│
├── data/
│   └── raw/                        # Target directory for downloaded CSVs
│
├── drivers/
│   └── postgresql-42.7.12.jar      # PySpark PostgreSQL connection driver
│
├── scripts/
│   ├── download_data.sh            # Kaggle API extraction script
│   └── load_data.py                # PySpark script to load data to Postgres
│
├── week34_project/                 # dbt project directory
│   ├── models/                     # SQL transformation models
│   ├── dbt_project.yml             # dbt configuration
│   └── profiles.yml                # Database connection profiles for dbt
│
├── docker-compose.yml              # Multi-container orchestration (Airflow + Postgres)
├── Dockerfile                      # Custom Airflow image with PySpark/dbt installed
├── .gitignore                      # Protection rules preventing secret/data leaks
└── README.md                       # Project blueprint and execution manual

```

---

## ⚙️ System Prerequisites & Setup

This pipeline is fully containerized. You only need **Docker** and **Docker Compose** installed on your host machine.

### 1. Configure Kaggle API Credentials

To allow Airflow to securely download the dataset without human intervention, you must provide Kaggle API credentials via a local environment variable file.

1. Create a file named exactly **`.env`** in the root directory of this project.
2. Add your Kaggle credentials inside the file:

```text
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key

```

*(Note: Ensure `.env` is listed in your `.gitignore` to prevent leaking your keys to GitHub).*

### 2. Build and Launch the Cluster

Run the following command in the root directory to spin up the PostgreSQL database and the Airflow infrastructure simultaneously:

```bash
docker compose up -d --build

```

---

## 🚀 Pipeline Execution (Apache Airflow)

Because this pipeline is orchestrated, you no longer need to execute individual scripts manually. Airflow handles the scheduling, execution, and dependency mapping.

1. **Access the UI:** Open your web browser and navigate to `http://localhost:8080`.
2. **Login:** Use the default Airflow credentials (Username: `airflow` / Password: `airflow`).
3. **Locate the DAG:** Find the pipeline named **`netflix_elt_pipeline`** in the DAGs list.
4. **Enable the DAG:** Click the toggle switch on the far left to unpause the DAG (it will turn blue).
5. **Trigger a Run:** Click the **"▶" (Play)** button in the top right corner and select **Trigger DAG**.
6. **Monitor Execution:** Click on the DAG name and navigate to the **Graph** or **Grid** view to watch the pipeline execute in real-time.

**The pipeline will automatically execute the following steps in strict order:**

1. `extract`: Downloads the Netflix dataset via Kaggle API.
2. `load`: Uses PySpark to read the CSV and load it into PostgreSQL.
3. `dbt_run`: Executes dbt SQL models to transform the raw data into analytics-ready tables.
4. `dbt_test`: Runs automated data quality tests (e.g., checking for null values or duplicates) to validate the transformations.

---

## 📊 Analyzing the Data (DBeaver)

Once the Airflow pipeline successfully completes (all tasks turn green), the transformed data is ready for analysis in your PostgreSQL database.

**Connecting DBeaver:**

1. Open **DBeaver** and create a new **PostgreSQL** connection.
2. Under the **Main** tab, fill in the connection details:
* **Host:** `localhost`
* **Port:** `5432`
* **Database:** `bootcamp`
* **Username:** `postgres`
* **Password:** `postgres`


3. Click **Test Connection**, allow any driver downloads if prompted, and click **Finish**.
4. You can now query your final dbt models (tables/views) directly from the `bootcamp` database to generate analytical insights!

---

## 🧹 Environment Teardown

When you are finished running the pipeline and analyzing the data, you can safely shut down the Airflow webserver, scheduler, and database containers by running:

```bash
docker compose down

```