from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
#importing sensors
from airflow.sensors.filesystem import FileSensor

# making a list  of default arguments for the DAG
default_args = {
    "owner": "eryyy",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# defining the DAG
with DAG(
    dag_id="netflix_elt_pipeline",
    default_args=default_args,
    schedule_interval="@daily",      
    start_date=datetime(2026, 1, 1), 
    catchup=False,
) as dag:

    # this task for extracting the netflix dataset in the raw data folder using the kaggle API

    with TaskGroup("extract_task", tooltip="Tasks for extracting data") as extract_task:
        extract_data = BashOperator(
            task_id="extract",
            bash_command="bash /app/scripts/download_data.sh ",
        )

        check_file = FileSensor(
            task_id="check_file",
            filepath="/app/data/raw/netflix_titles.csv",
            poke_interval=10,
            timeout=60 * 5,
        )

        extract_data >> check_file


    # this task is for pushing the data into the staging_raw table in the database using Spark
    load = BashOperator(
        task_id="load",
        bash_command="python /app/scripts/load_data.py",
    )

    dbt_pipeline = BashOperator(
        task_id="transform",
        bash_command = "dbt build --project-dir /app/week34_project --profiles-dir /app/week34_project --target airflow",
    )

    # defining the dependencies
    extract_task >> load >> dbt_pipeline