from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# 1. Default settings for all tasks
default_args = {
    "owner": "intern",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# 2. Define the DAG
with DAG(
    dag_id="netflix_elt_pipeline",
    default_args=default_args,
    schedule_interval="@daily",      # Runs once a day
    start_date=datetime(2026, 1, 1), # Syncs with your project specs
    catchup=False,
) as dag:

    # Task 1: Extract (Download the Kaggle dataset)
    extract = BashOperator(
        task_id="extract",
        bash_command="bash /app/scripts/download.sh",
    )

    # Task 2: Load (Push the raw CSV into Postgres via PySpark)
    load = BashOperator(
        task_id="load",
        bash_command="python /app/scripts/load_pyspark.py",
    )

    # Task 3: Transform (Run your dbt SQL models)
    transform = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /app/week34_project --profiles-dir /app/week34_project",
    )

    # Task 4: Test (Run your dbt schema tests)
    test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /app/week34_project --profiles-dir /app/week34_project",
    )

    # 3. Define the execution order
    extract >> load >> transform >> test